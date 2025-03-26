import weaviate.classes as wvc
from weaviate.collections.collection import Collection

from rag.client import client


def vector_db_setup(collection_name: str) -> Collection:
    """
    RAG DBの初期化を行う

    Args:
        collection_name: コレクション名(DBの名前)
    """
    if client.collections.exists(collection_name):
        print(f"Collection {collection_name} already exists")
        return client.collections.get(collection_name)

    collection = client.collections.create(
        name=collection_name,
        vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(model="text-embedding-3-small"),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        generative_config=wvc.config.Configure.Generative.openai(),  # Ensure the `generative-openai` module is used for generative queries
        properties=[
            wvc.config.Property(name="text", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="course_code", data_type=wvc.config.DataType.INT),
        ],
    )

    return collection

def full_text_db_setup(collection_name: str) -> Collection:
    """
    RAG DBの初期化を行う

    Args:
        collection_name: コレクション名(DBの名前)
    """
    if client.collections.exists(collection_name):
        print(f"Collection {collection_name} already exists")
        return client.collections.get(collection_name)

    collection = client.collections.create(
        name=collection_name,
        vectorizer_config=wvc.config.Configure.Vectorizer.none(),  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
        properties=[
            wvc.config.Property(name="text", data_type=wvc.config.DataType.TEXT),
            wvc.config.Property(name="course_code", data_type=wvc.config.DataType.INT),
        ],
    )

    return collection


if __name__ == "__main__":
    collection = vector_db_setup("text_search_model_sample")
    assert isinstance(collection, Collection)
    client.close()
