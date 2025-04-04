import asyncio
from abc import ABCMeta, abstractmethod

from supabase import AsyncClient

from supabase_rag.client import DBAsyncClient, SupabaseClient
from supabase_rag.model import Category, Document, FullText


class Insert(metaclass=ABCMeta):
    """
    Attributes:
        client(DBClient): DBクライアント
    """

    @abstractmethod
    async def insert_document(
        self, data: Document, table_name: str = "documents"
    ) -> int:
        """
        DBに履修情報を挿入するメソッド
        """
        raise NotImplementedError()

    @abstractmethod
    async def insert_category(
        self, data: Category, table_name: str = "categories"
    ) -> int:
        """
        DBに履修区分を挿入するメソッド
        """
        raise NotImplementedError()

    @abstractmethod
    async def insert_full_text(
        self, data: FullText, table_name: str = "full_texts"
    ) -> int:
        """
        DBに履修情報の全文を挿入するメソッド
        """
        raise NotImplementedError()


class InsertSupabase(Insert):
    """
    supabaseのinsert用クライアント
    """

    def __init__(self, client: AsyncClient):
        self.client = client

    @classmethod
    async def new(cls, client: DBAsyncClient):
        """ここからインスタンス作る"""
        conn = await client.get_client()
        return cls(conn)

    async def insert_document(
        self, data: Document, table_name: str = "documents"
    ) -> int:
        result = await self.client.table(table_name).insert(data.model_dump()).execute()
        return result.data[0]["id"]

    async def insert_category(
        self, data: Category, table_name: str = "categories"
    ) -> int:
        result = await self.client.table(table_name).insert(data.model_dump()).execute()
        return result.data[0]["id"]

    async def insert_full_text(
        self, data: FullText, table_name: str = "full_texts"
    ) -> int:
        result = await self.client.table(table_name).insert(data.model_dump()).execute()
        return result.data[0]["id"]


async def main():
    """デバッグ用"""
    db_conn = SupabaseClient()
    inser_client = await InsertSupabase.new(db_conn)
    result = await inser_client.insert_category(data=Category(name="test_category"))
    # data=[{'id': 2, 'name': 'test_category'}] count=None
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
