from pydantic import BaseModel


class ClassInfo(BaseModel):
    """RAGに格納する履修情報の構造化データ"""

    text: str
    course_code: int

    def __str__(self) -> str:
        return f"""
        text: {self.text}
        course_code: {self.course_code}
     """
