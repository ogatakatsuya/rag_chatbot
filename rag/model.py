from pydantic import BaseModel


class ClassInfo(BaseModel):
    """RAGに格納する履修情報の構造化データ"""

    class_name: str
    info: str

    def __str__(self) -> str:
        return f"""
        Class Name: {self.class_name}
        Info: {self.info}
        """
