from abc import ABCMeta, abstractmethod

from supabase import AsyncClient

from supabase_rag.client import DBAsyncClient
from supabase_rag.model import FullTextModel


class Search(metaclass=ABCMeta):
    """
    Attributes:
        client(DBClient): DBクライアント
    """

    @abstractmethod
    async def search(
        self, query: list[float], category_name: str
    ) -> list[FullTextModel]:
        """
        DBから履修情報をsemantic searchするメソッド
        """
        raise NotImplementedError()


class SearchSupabase(Search):
    """
    supabaseのsearch用クライアント
    """

    def __init__(self, client: AsyncClient):
        self.client = client

    @classmethod
    async def new(cls, client: DBAsyncClient):
        """ここからインスタンス作る"""
        conn = await client.get_client()
        return cls(conn)

    async def search(
        self, query: list[float], category_name: str
    ) -> list[FullTextModel]:
        """
        DBから履修情報をsemantic searchするメソッド
        """
        res = await self.client.rpc(
            "search_full_texts",
            {
                "category_name": category_name,
                "query": query,
            },
        ).execute()
        return [FullTextModel(**item) for item in res.data]
