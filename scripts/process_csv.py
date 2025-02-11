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


if __name__ == "__main__":
    load_and_embed_csv()
