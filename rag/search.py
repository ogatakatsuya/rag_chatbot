from weaviate.classes.query import MetadataQuery
from weaviate.collections.classes.internal import QueryReturn

from rag.model import ClassInfo
from src.rag.client import client


def search(
    query: str, limit: int = 10, collection_name: str = "text_search_model_sample"
) -> list[ClassInfo]:
    """
    RAGで検索を行う

    Args:
        query: 検索文字列
        limit: 検索結果の上限
        collection_name: コレクション名(DBの名前)
    Returns:
        検索結果のリスト
    """
    collections = client.collections.get(collection_name)
    response = collections.query.near_text(
        query=query,  # The model provider integration will automatically vectorize the query
        limit=limit,
    )
    assert isinstance(response, QueryReturn)
    return [ClassInfo(**obj.properties) for obj in response.objects]  # type: ignore


def search_with_filter(
    query: str,
    limit: int = 10,
    collection_name: str = "text_search_model_sample",
    certainty_threshold: float | None = None,
) -> list[ClassInfo]:  # ベクトル検索
    """
    通常の検索に加えて近似値の閾値でフィルタリングを行う

    Args:
        query: 検索文字列
        limit: 検索結果の上限
        collection_name: コレクション名(DBの名前)
        certainty_threshold: 閾値
    Returns:
        検索結果のリスト
    """
    collections = client.collections.get(collection_name)

    response = collections.query.near_text(
        query=query, limit=limit, return_metadata=MetadataQuery.full()
    )
    assert isinstance(response, QueryReturn)

    # 閾値でのフィルター
    if certainty_threshold is not None:
        response.objects = [
            obj
            for obj in response.objects
            if obj.metadata.certainty is not None
            and certainty_threshold <= obj.metadata.certainty
        ]

    return [ClassInfo(**obj.properties) for obj in response.objects]  # type: ignore


def search_hybrid(
    query: str,
    limit: int = 10,
    collection_name: str = "text_search_model_sample",
    certainty_threshold: float | None = None,
) -> list[ClassInfo]:  # ハイブリッド検索
    """
    ハイブリッド検索(あんま普通の検索と何が違うかわかってない)

    Args:
        query: 検索文字列
        limit: 検索結果の上限
        collection_name: コレクション名(DBの名前)
        certainty_threshold: 閾値
    Returns:
        検索結果のリスト
    """
    collections = client.collections.get(collection_name)

    response = collections.query.hybrid(
        query=query, limit=limit, return_metadata=MetadataQuery.full()
    )
    assert isinstance(response, QueryReturn)

    # 閾値でのフィルター
    if certainty_threshold is not None:
        response.objects = [
            obj
            for obj in response.objects
            if obj.metadata.certainty is not None
            and certainty_threshold <= obj.metadata.certainty
        ]

    return [ClassInfo(**obj.properties) for obj in response.objects]  # type: ignore


def search_bm25(
    query: str,
    limit: int = 10,
    collection_name: str = "text_search_model_sample",
    certainty_threshold: float | None = None,
) -> list[ClassInfo]:  # BM25
    """
    BM25での検索(これもあんまよくわかってない)

    Args:
        query: 検索文字列
        limit: 検索結果の上限
        collection_name: コレクション名(DBの名前)
        certainty_threshold: 閾値
    Returns:
        検索結果のリスト
    """
    collections = client.collections.get(collection_name)

    response = collections.query.bm25(
        query=query, limit=limit, return_metadata=MetadataQuery.full()
    )
    assert isinstance(response, QueryReturn)

    # 閾値でのフィルター
    if certainty_threshold is not None:
        response.objects = [
            obj
            for obj in response.objects
            if obj.metadata.certainty is not None
            and certainty_threshold <= obj.metadata.certainty
        ]

    return [ClassInfo(**obj.properties) for obj in response.objects]  # type: ignore


if __name__ == "__main__":
    queries = ["プログラミング", "統計"]
    for query in queries:
        print(search(query, 1))
        print(search_with_filter(query, 1))
        print(search_hybrid(query, 1))
        print(search_bm25(query, 1))
    client.close()
