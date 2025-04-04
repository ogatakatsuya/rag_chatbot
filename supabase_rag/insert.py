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
    def insert_document(self, data: Document, table_name: str):
        """
        DBに履修情報を挿入するメソッド
        """
        pass

    @abstractmethod
    def insert_category(self, data: Category, table_name: str):
        """
        DBに履修区分を挿入するメソッド
        """
        pass

    @abstractmethod
    def insert_fulltext(self, data: FullText, table_name: str):
        """
        DBに履修情報の全文を挿入するメソッド
        """
        pass


class InsertSupbase(Insert):
    """
    supabaseのdbクライアント
    """

    def __init__(self, client: AsyncClient):
        self.client = client

    @classmethod
    async def new(cls, client: DBAsyncClient):
        """ここからインスタンス作る"""
        conn = await client.get_client()
        return cls(conn)

    async def insert_document(self, data: Document, table_name: str = "documents"):
        return await self.client.table(table_name).insert(data.model_dump()).execute()

    async def insert_category(self, data: Category, table_name: str = "categories"):
        return await self.client.table(table_name).insert(data.model_dump()).execute()

    async def insert_fulltext(self, data: FullText, table_name: str = "full_texts"):
        return await self.client.table(table_name).insert(data.model_dump()).execute()


async def main():
    db_conn = SupabaseClient()
    inser_client = await InsertSupbase.new(db_conn)
    await inser_client.insert_category(data=Category(name="test_category"))


if __name__ == "__main__":
    asyncio.run(main())
