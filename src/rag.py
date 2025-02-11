import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class RagService:
    def __init__(self, path: Path):
        self.class_data = json.loads(path.read_text(encoding="utf-8"))

    def search(self, query: str, n_results: int = 5) -> list[str]:
        """
        RAGを用いて検索を行い、上位n_results件の結果を返す

        Args:
            query (str): 検索クエリ
            n_results (int): 上位n_results件の結果を返す

        Returns:
            list: 上位n_results件の結果
        """
        return []

    def _embedding_query(self, query: str):
        """
        クエリを埋め込む

        Args:
            query (str): クエリ
        Returns:
            np.ndarray: 埋め込まれたクエリ
        """
        pass


if __name__ == "__main__":
    path = Path("..") / "data" / "class_data_embeddings.json"
    rag = RagService(path)
    print(rag.class_data)
