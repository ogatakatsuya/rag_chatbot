import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class RagService:
    def __init__(self):
        # TODO: どこでembeddingするかは要検討
        self.class_data = ClassData()

    def get_class_data(self):
        return self.class_data.data

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


class ClassData:
    def __init__(self):
        self.data = pd.read_csv(Path("..") / "data" / "class_data.csv")
        self.client = OpenAI(api_key=os.getenv("GEMINI_API_KEY", ""))

    def pre_process(self):
        """
        読み込んだCSVファイルに対して、なんらかの前処理を行う
        """
        pass

    def embedding(self):
        """
        読み込んだCSVファイルに対して、埋め込みを行う
        """
        pass


if __name__ == "__main__":
    rag_service = RagService()
    print(rag_service.get_class_data())
