import asyncio

import streamlit as st

from src.llm import LLM, GeminiLLM
from src.model import Message
from supabase_rag.client import SupabaseClient
from supabase_rag.embedding import OpenAIEmbedding
from supabase_rag.insert import InsertSupabase
from supabase_rag.rag import Rag, RagV1
from supabase_rag.search import SearchSupabase


def chat_page(rag: Rag, llm: LLM):
    """チャットボットのページ"""
    st.subheader("💬 Chatbot")

    if prompt := st.chat_input("何かお困りですか？"):
        st.session_state.chat_history.append(Message(role="user", content=prompt))

        for message in st.session_state.chat_history:
            with st.chat_message(message.role):
                st.markdown(message.content)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            rag_result = asyncio.run(rag.search(prompt, "全学教育推進機構"))
            st.write(rag_result)
            response = llm.get_response_with_context(
                st.session_state.chat_history, placeholder, rag_result
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


async def initialize() -> tuple[RagV1, LLM]:
    """session_stateの初期化"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    client = SupabaseClient()
    insert_client = await InsertSupabase.new(client)
    search_client = await SearchSupabase.new(client)
    embedding_client = OpenAIEmbedding()
    rag = RagV1(insert_client, search_client, embedding_client)
    llm = GeminiLLM()

    return rag, llm


if __name__ == "__main__":
    rag_client, llm_client = asyncio.run(initialize())

    # タブの作成
    tab1, tab2 = st.tabs(["💬 Chatbot", "📚 概要"])

    # タブの切り替え
    with tab1:
        chat_page(rag_client, llm_client)

    with tab2:
        explanation_page()
