import json
import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class RagService:
    def __init__(self, embed_file_path: Path, full_text_file_path: Path):
        self.class_data = json.loads(embed_file_path.read_text(encoding="utf-8"))
        self.full_text_data = json.loads(full_text_file_path.read_text(encoding="utf-8"))
        self.dim = len(self.class_data[0]["embedding"])
        self.faiss_index = self._create_faiss_index(self.dim)

    def search(self, query: str, n_results: int = 5) -> str:
        """
        RAGを用いて検索を行い、上位n_results件の結果を返す

        Args:
            query (str): 検索クエリ
            n_results (int): 上位n_results件の結果を返す

        Returns:
            str: フォーマットされた検索結果
        """
        query_embedding = self._embedding_query(query).reshape(1, -1)
        distances, indices = self.faiss_index.search(query_embedding, n_results * 4)

        results_index = set()
        for index in indices[0]:
            results_index.add(self.class_data[index]["full_text_id"])
            if len(results_index) >= n_results:
                break
        
        results = []
        for index in results_index:
            results.append(self.full_text_data[index]["text"])
        return self._format_docs(results)

    def _embedding_query(self, query: str):
        """
        クエリを埋め込む

        Args:
            query (str): クエリ
        Returns:
            np.ndarray: 埋め込まれたクエリ
        """
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=openai_api_key)
        embedding = (
            client.embeddings.create(input=query, model="text-embedding-3-small")
            .data[0]
            .embedding
        )
        return np.array(embedding).astype("float32")

    def _create_faiss_index(self, dim: int) -> faiss.Index:
        """
        faissのインデックスを作成する
        """
        index = faiss.IndexFlatL2(dim)
        embeddings = np.array(
            [data["embedding"] for data in self.class_data], dtype="float32"
        )
        index.add(embeddings)
        return index

    def _format_docs(self, docs: list[str]) -> str:
        return "\n\n".join(docs)


if __name__ == "__main__":
    embed_path = Path("../data/class_data_embeddings.json")
    full_text_path = Path("../data/class_data_full_texts.json")
    rag = RagService(embed_path, full_text_path)
    query = "データベースを学べる授業を教えて"
    results = rag.search(query)
    print(f"query: {query}")
    print(results)
