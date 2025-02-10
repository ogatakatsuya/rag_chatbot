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
        text = " ".join(map(str, row.values))
        # 一番安いモデルで埋め込み
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        embedding_vector = response["data"][0]["embedding"]
        embeddings.append({"text": text, "embedding": embedding_vector})

    # とりまJSONに保存
    output_path = Path("..") / "data" / "class_data_embeddings.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=4)

    print(f"埋め込みデータを {output_path} に保存しました。")


if __name__ == "__main__":
    load_and_embed_csv()
