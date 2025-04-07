from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

EMBEDDING_DIM = 1536


class EmbedType(Enum):
    FULL_TEXT = "full_text"
    INFO_TEXT = "info_text"
    INSTRUCTOR_TEXT = "instructor_text"
    CONTENT_TEXT = "content_text"


class Category(BaseModel):
    """
    履修区分

    Attributes:
        name(str): カテゴリ名
    """

    name: str = Field(max_length=50)


class CategoryModel(Category):
    """
    supabaseに保存されている履修区分のデータ型

    Attributes:
        id(int): 履修区分のID
    """

    id: int


class FullText(BaseModel):
    """
    履修情報の全文

    Attributes:
        content(str): 履修情報の全文
    """

    content: str
    category_id: int
    course_code: str


class FullTextModel(FullText):
    """
    supabaseに保存されている履修情報の全文のデータ型

    Attributes:
        id(int): 履修情報のID
    """

    id: int


class Document(BaseModel):
    """
    履修情報

    Attributes:
        content(str): ドキュメントの内容
        category_id(int): 履修区分のID
        full_text_id(int): 履修情報のID
        embedding(list[float]): ドキュメントの埋め込み
    """

    embedding: list[float] = Field(min_length=EMBEDDING_DIM, max_length=EMBEDDING_DIM)
    full_text_id: int
    type: str


class DocumentModel(Document):
    """
    supabaseのvector dbに格納されるデータ型

    Attributes:
        id: int
    """

    id: int
    created_at: datetime
