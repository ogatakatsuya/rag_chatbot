from weaviate.collections.collection import Collection
import weaviate.classes as wvc
import re

from rag.client import client
from rag.model import ClassInfo
from rag.setup import vector_db_setup, full_text_db_setup
from rag.insert import insert
import pandas as pd

import sys
sys.path.append('../scraping/syllabus')


def load_and_embed_csv():
    """
    CSVファイルを読み込んで埋め込みを行い、JSONで保存する
    """
    # CSVの読み込み
    csv_path = '../scraping/syllabus/syllabus.csv'
    department = '基礎工学部'
    data = pd.read_csv(csv_path)

    # 曜日・時間の整形
    data["day_and_period"] = data["day_and_period"].apply(format_schedule)
    data['course_code'] = data['course_code'].str.extract(r'(\d+)')

    embeddings = []
    full_texts = []

    # collectionのセットアップ
    vector_db_collection = vector_db_setup("class_data_vector")
    full_text_db_collection = full_text_db_setup("class_data_full_text")

    for i, row in data.iterrows():
        print(row['day_and_period'])
        #すでに埋め込み済みのデータはスキップ
        result = vector_db_collection.query.fetch_objects(
            filters=wvc.query.Filter.by_property("course_code").equal(int(row['course_code'])),
            limit=1
        )

        if result.objects:
            print(f"Skipping: {row['course_code']}")
            continue

        # 前処理: 1授業につき全文と履修の情報と履修の内容の4種類を埋め込み
        full_text = (
            f"{department}が開講する科目である科目番号{row['course_code']}の「{row['course_name_jp']}」は、"
            f"{row['semester']}に開講され、{row['day_and_period']}に行われる。対象は{row['student_year']}生であり、"
            f"{row['course_objectives']} 本講義の履修には、{row['requirements_prerequisites']}。"
        )
        info_text = (
            f"{department}が開講する科目である科目番号{row['course_code']}の「{row['course_name_jp']}」は、"
            f"{row['semester']}に開講され、{row['day_and_period']}に行われる。対象は{row['student_year']}生であり、"
            f"本講義の履修には、{row['requirements_prerequisites']}。"
        )
        date_text = (
            f"{row['day_and_period']}に開講される授業である。"
        )
        content_text = (
            f"「{row['course_name_jp']}」は、"
            f"{row['course_objectives']} "
        )

        texts = [full_text, info_text, date_text, content_text]

        # # 一番安いモデルで埋め込み
        for text in texts:
            embeddings.append(ClassInfo(text=text, course_code=int(row['course_code'])))
        
        full_texts.append(ClassInfo(text=full_text, course_code=int(row['course_code'])))

    # データの挿入
    insert(vector_db_collection, embeddings)
    insert(full_text_db_collection, full_texts)
    
    

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
            print(f"Warning: 不明な曜日データ '{day}' をスキップ")
            if day == "他":
                return "その他の時間"
            continue

        if not time.isdigit():
            print(f"Warning: 不明な時間データ '{time}' をスキップ")
            continue

        formatted_parts.append(f"{day_dict[day]}{time}時間目")

    return "、".join(formatted_parts)


if __name__ == "__main__":
    load_and_embed_csv()
    collection_name = "class_data_vector"  # 確認したいコレクション名を設定

    result = client.collections.get(collection_name).query.fetch_objects(limit=100)
    print(len(result.objects))


    #client終了
    client.close()