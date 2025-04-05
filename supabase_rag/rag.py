import asyncio
from abc import ABCMeta, abstractmethod

from supabase_rag.client import SupabaseClient
from supabase_rag.embedding import Embedding, OpenAIEmbedding
from supabase_rag.insert import Insert, InsertSupabase
from supabase_rag.model import Category, Document, FullText, FullTextModel
from supabase_rag.search import Search, SearchSupabase


class Rag(metaclass=ABCMeta):
    """
    Attributes:
        insert_client(Insert): データ挿入用クライアント
        search_client(Search): データ検索用クライアント
        embedding_client(Embedding): 埋め込み用クライアント
    """

    @abstractmethod
    async def insert_document(
        self, text: str, category_id: int, full_text_id: int
    ) -> int:
        """
        DBに履修情報を挿入するメソッド
        """
        raise NotImplementedError()

    @abstractmethod
    async def insert_category(self, name: str):
        """
        DBに履修区分を挿入するメソッド
        """
        raise NotImplementedError()

    @abstractmethod
    async def insert_full_text(self, text: str):
        """
        DBに履修情報の全文を挿入するメソッド
        """
        raise NotImplementedError()

    @abstractmethod
    async def search(self, query: str, category_name: str) -> list[FullTextModel]:
        """
        DBから履修情報をsemantic searchするメソッド
        """
        raise NotImplementedError()


class RagV1(Rag):
    """
    RAGクライアント ver.1
    """

    def __init__(
        self, insert_client: Insert, search_client: Search, embedding_client: Embedding
    ):
        self.insert_client = insert_client
        self.search_client = search_client
        self.embedding_client = embedding_client

    async def insert_document(
        self, text: str, category_id: int, full_text_id: int
    ) -> int:
        embedding = self.embedding_client.exec(text)
        return await self.insert_client.insert_document(
            Document(
                content=text,
                embedding=embedding,
                category_id=category_id,
                full_text_id=full_text_id,
            )
        )

    async def insert_category(self, name: str) -> int:
        return await self.insert_client.insert_category(Category(name=name))

    async def insert_full_text(self, text: str) -> int:
        return await self.insert_client.insert_full_text(FullText(content=text))

    async def search(self, query: str, category_name: str) -> list[FullTextModel]:
        embedding = self.embedding_client.exec(query)
        return await self.search_client.search(embedding, category_name)


async def main():
    """デバッグ用"""
    client = SupabaseClient()
    insert_client = await InsertSupabase.new(client)
    search_client = await SearchSupabase.new(client)
    embedding_client = OpenAIEmbedding()

    rag = RagV1(insert_client, search_client, embedding_client)

    documents = [
        "Example Document 1",
        "Example Document 2",
        "Example Document 3",
        "Example Document 4",
        "Example Document 5",
    ]
    category_id = await rag.insert_category("Example Category")
    full_text_id = await rag.insert_full_text("Example Full Text")
    for doc in documents:
        document_id = await rag.insert_document(
            text=doc, category_id=category_id, full_text_id=full_text_id
        )
    print(f"Inserted document with ID: {document_id}")


async def main2():
    client = SupabaseClient()
    insert_client = await InsertSupabase.new(client)
    search_client = await SearchSupabase.new(client)
    embedding_client = OpenAIEmbedding()

    rag = RagV1(insert_client, search_client, embedding_client)

    result = await rag.search(
        query="スポーツ",
        category_name="全学教育推進機構",
    )
    for item in result:
        print(f"result{item.id} : {item.content}")


if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(main2())
