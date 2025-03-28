from rag.search import search, search_course_code
from rag.client import client
from dotenv import load_dotenv

load_dotenv()


class RagService:
    def __init__(self, embed_collection_name: str, full_text_collection_name: str):
        self.embed_collection_name = embed_collection_name
        self.full_text_collection_name = full_text_collection_name

    def search(self, query: str, n_results: int = 5) -> str:
        """
        RAGを用いて検索を行い、上位n_results件の結果を返す

        Args:
            query (str): 検索クエリ
            n_results (int): 上位n_results件の結果を返す

        Returns:
            str: フォーマットされた検索結果
        """
        embed_variation = 4
        results = search(query, n_results*embed_variation, "class_data_vector")

        course_codes = set()
        for result in results:
            course_codes.add(result.course_code)
            if len(course_codes) >= n_results:
                break

        results = []
        for code in course_codes:
            results.append(search_course_code(code))
        return self._format_docs(results)

    def _format_docs(self, docs: list[str]) -> str:
        return "\n\n".join(docs)


if __name__ == "__main__":
    embed_name = "class_data_vector"
    full_text_name = "Class_data_full_text"
    rag = RagService(embed_name, full_text_name)
    query = "データベースを学べる授業を教えて"
    results = rag.search(query)
    print(f"query: {query}")
    print(results)
    client.close()