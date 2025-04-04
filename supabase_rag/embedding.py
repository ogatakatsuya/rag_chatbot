from abc import ABCMeta, abstractmethod

from openai import OpenAI

from lib.env import env


class Embedding(metaclass=ABCMeta):
    """
    Attributes:
        client(DBClient): DBクライアント
    """

    @abstractmethod
    def exec(self, data: str) -> list[float]:
        """
        埋め込みを取得するメソッド
        """
        raise NotImplementedError()


class OpenAIEmbedding(Embedding):
    """
    OpenAIの埋め込みクライアント
    """

    def __init__(self):
        self.client = OpenAI(api_key=env.OPENAI_API_KEY)

    def exec(self, text: str) -> list[float]:
        res = self.client.embeddings.create(input=text, model="text-embedding-3-small")
        return res.data[0].embedding
