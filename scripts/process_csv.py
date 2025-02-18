import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def load_and_embed_csv():
    """
    CSVファイルを読み込んで埋め込みを行い、JSONで保存する
    """
    # CSVの読み込み
    csv_path = Path("..") / "data" / "class_data.csv"
    data = pd.read_csv(csv_path)

    # 曜日・時間の整形
    data["曜日・時間"] = data["曜日・時間"].apply(format_schedule)

    # OpenAIクライアントの初期化
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    embeddings = []
    for _, row in data.iterrows():
        # ここで前処理(今は適当に行を連結するのみ)
        text = (
            f"{row['開講所属']}が開講する科目である科目番号{row['科目番号']}の「{row['開講科目名']}」は、"
            f"{row['開講区分']}に開講され、{row['曜日・時間']}に行われる。対象は{row['年次']}生であり、"
            f"{row['授業の目的と概要']} 本講義の履修には、{row['履修条件・受講条件']}。"
        )
        # 一番安いモデルで埋め込み
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        embedding_vector = response.data[0].embedding
        embeddings.append({"text": text, "embedding": embedding_vector})

    # とりまJSONに保存
    output_path = Path("..") / "data" / "class_data_embeddings.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=4)

    print(f"埋め込みデータを {output_path} に保存しました。")

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
            continue

        if not time.isdigit():
            print(f"Warning: 不明な時間データ '{time}' をスキップ")
            continue

        formatted_parts.append(f"{day_dict[day]}{time}時間目")

    return "、".join(formatted_parts)


if __name__ == "__main__":
    load_and_embed_csv()
