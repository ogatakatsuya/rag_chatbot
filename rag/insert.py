from weaviate.collections.collection import Collection

from rag.client import client
from rag.model import ClassInfo
from rag.setup import vector_db_setup, full_text_db_setup


def insert(
    collection: Collection,
    data: list[ClassInfo],
) -> None:
    """
    RAGにデータを挿入する

    Args:
        collection: RAGのコレクション(テーブルみたいなの)
        data: 挿入するデータ(リスト形式で)
    """
    data_for_insert = [info.model_dump() for info in data]
    collection.data.insert_many(data_for_insert)


if __name__ == "__main__":
    data = [
        ClassInfo(class_name="src/data/dog.png", info="This is a picture of dog"),
        ClassInfo(class_name="src/data/cat.png", info="This is a picture of cat"),
    ]
    collection = vector_db_setup("text_search_model_sample")
    insert(collection, data)
    client.close()
