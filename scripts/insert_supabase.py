import asyncio
import os

import pandas as pd

from supabase_rag.client import SupabaseClient
from supabase_rag.embedding import OpenAIEmbedding
from supabase_rag.insert import InsertSupabase
from supabase_rag.rag import RagV1
from supabase_rag.search import SearchSupabase

# sys.path.append("../scraping/syllabus")


async def load_and_embed_csv(file_name: str, category_id: int):
    """
    CSVファイルを読み込んで埋め込みを行い、JSONで保存する
    """
    # CSVの読み込み
    csv_folder = "./scraping/syllabus"
    csv_path = os.path.join(csv_folder, file_name)
    data = pd.read_csv(csv_path)

    # 曜日・時間の整形
    data["day_and_period"] = data["day_and_period"].apply(format_schedule)
    data["course_code"] = data["course_code"].astype(str).str.extract(r"(\d+)")

    for i, row in data.iterrows():
        # 前処理: 1授業につき全文と履修の情報と履修の内容の4種類を埋め込み
        full_text = (
            f"科目番号{row['course_code']}の「{row['course_name_jp']}」は、"
            f"{row['semester']}に開講され、{row['day_and_period']}に行われる。担当教員は{row['instructor']}である。対象は{row['student_year']}生であり、"
            f"{row['course_objectives']} 本講義の履修には、{row['requirements_prerequisites']}。"
            f"授業で使用する教材は{row['textbooks']}である。"
        )
        info_text = (
            f"科目番号{row['course_code']}の「{row['course_name_jp']}」は、"
            f"{row['semester']}に開講され、{row['day_and_period']}に行われる。対象は{row['student_year']}生であり、"
            f"本講義の履修には、{row['requirements_prerequisites']}。"
        )

        instructor_text = (
            f"「{row['course_name_jp']}」の担当教員は{row['instructor']}である。"
        )

        content_text = f"「{row['course_name_jp']}」は、{row['course_objectives']} "

        texts = [full_text, info_text, instructor_text, content_text]

        await insert_data(texts, category_id)


async def insert_data(texts: list[str], category_id: int):
    """
    データを挿入する

    Args:
        texts (list[str]): 挿入するテキストのリスト
    """
    client = SupabaseClient()
    insert_client = await InsertSupabase.new(client)
    search_client = await SearchSupabase.new(client)
    embedding_client = OpenAIEmbedding()

    rag = RagV1(insert_client, search_client, embedding_client)
    full_text_id = await rag.insert_full_text(texts[0])
    for doc in texts:
        document_id = await rag.insert_document(
            text=doc, category_id=category_id, full_text_id=full_text_id
        )
        print(f"Inserted document with ID: {document_id}")


def format_schedule(schedule: str) -> str:
    """
    曜日・時間の文字列を整形する

    Args:
        schedule (str): 曜日・時間の文字列

    Returns:
        str: 整形された曜日・時間の文字列
    """

    # 曜日変換用の辞書
    day_dict = {
        "月": "月曜日",
        "火": "火曜日",
        "水": "水曜日",
        "木": "木曜日",
        "金": "金曜日",
        "土": "土曜日",
        "日": "日曜日",
    }

    schedule = schedule.strip().replace("\t", "")

    parts = schedule.split(",")
    formatted_parts = []
    for part in parts:
        part = part.strip()

        if not part:
            continue

        day = part[0]
        time = part[1:]

        if day not in day_dict:
            if day == "他":
                return "その他の時間"
            continue

        if not time.isdigit():
            continue

        formatted_parts.append(f"{day_dict[day]}{time}時間目")

    return "、".join(formatted_parts)


if __name__ == "__main__":
    embedding_csvs = [
        ("bungaku.csv", 4),
        ("ningenkagaku.csv", 5),
        ("hougaku.csv", 6),
        ("keizaigaku.csv", 7),
        ("rigaku.csv", 8),
        ("igaku_igakuka.csv", 9),
        ("igaku_hoken.csv", 10),
        ("shigaku.csv", 11),
        ("yakugaku.csv", 12),
        ("kogaku.csv", 13),
        ("gaigo.csv", 14),
    ]

    for file_name, category_id in embedding_csvs:
        print(f"Embedding {file_name}...")
        asyncio.run(load_and_embed_csv(file_name, category_id))
        print(f"Finished embedding {file_name}.")
