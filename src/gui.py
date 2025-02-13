from pathlib import Path

import pandas as pd
import streamlit as st

from src.llm import LLM
from src.model import Message


@st.cache_data
def load_csv():
    """CSVデータを読み込む"""
    df = pd.read_csv(Path("./data/class_data.csv"))
    return df


def chat_page(llm: LLM):
    """チャットボットのページ"""
    st.subheader("💬 Chatbot")

    if prompt := st.chat_input("何かお困りですか？"):
        st.session_state.chat_history.append(Message(role="user", content=prompt))

        for message in st.session_state.chat_history:
            with st.chat_message(message.role):
                st.markdown(message.content)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            response: str = llm.get_response_with_context(
                st.session_state.chat_history, placeholder
            )

        st.session_state.chat_history.append(
            Message(role="assistant", content=response)
        )


def explanation_page():
    """概要のページ"""
    st.subheader("概要")
    st.write(
        "このアプリケーションは、RAGデータを用いて履修登録支援チャットボットを実装したものです。"
    )
    st.write("以下の機能があります。")
    st.write("- 履修登録支援チャットボット")
    st.write("- RAGデータの閲覧(一旦、基礎工学部3年秋冬の授業のみ)")
    st.write("- 履修登録以外のことには答えない")
    st.write("- 登録されている授業以外については答えない(存在しない授業は答えない)")

    st.subheader("入出力例")
    with st.chat_message("user"):
        st.markdown("データベースを学べる授業を教えて")
    with st.chat_message("assistant"):
        st.markdown(
            """
                基礎工学部で開講されているデータベースを学べる授業は、科目番号90046の「データベース」です。この授業は秋～冬学期に火曜4限に行われ、3,4年生が対象です。
                
                「データベース」では、実世界から収集されたデータを複数のアプリケーションから共有できるよう統合したデータベースに関する基本的な概念を学びます。また、データベースの操作言語として標準的なＳＱＬの実習も行います。
                
                ただし、この授業は計算機科学コース、および、ソフトウェア科学コース以外の学生の履修は原則認められていませんのでご注意ください。また、授業時間中に数回、演習室での演習があるため、「プログラミングC」、「プログラミングD」または「演習C」を受講することを強く推奨します。
            """
        )


def csv_page():
    """CSVデータのページ"""
    st.subheader("📊 RAGデータビュー")
    st.write("現在格納されているデータを確認できます。")

    df = load_csv()
    st.dataframe(df)


def initialize():
    """session_stateの初期化"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


if __name__ == "__main__":
    initialize()
    llm = LLM()

    # タブの作成
    tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "📚 概要", "📊 RAGデータ"])

    # タブの切り替え
    with tab1:
        chat_page(llm)

    with tab2:
        explanation_page()

    with tab3:
        csv_page()
