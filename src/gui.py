import asyncio

import streamlit as st

from src.llm import LLM, GeminiLLM
from src.model import Message
from supabase_rag.client import SupabaseClient
from supabase_rag.embedding import OpenAIEmbedding
from supabase_rag.insert import InsertSupabase
from supabase_rag.rag import Rag, RagV1
from supabase_rag.search import SearchSupabase


@st.fragment
def header():
    st.header("大阪大学 履修支援チャットボット")


def chat(rag: Rag, llm: LLM):
    """チャットボットのページ"""

    if prompt := st.chat_input("何かお困りですか？"):
        st.session_state.chat_history.append(Message(role="user", content=prompt))

    for message in st.session_state.chat_history:
        with st.chat_message(message.role):
            st.markdown(message.content)

    if prompt:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            rag_result = asyncio.run(
                rag.search(prompt, st.session_state.selected_option)
            )
            response = llm.get_response_with_context(
                st.session_state.chat_history, placeholder, rag_result
            )

        st.session_state.chat_history.append(
            Message(role="assistant", content=response)
        )


def select_form():
    OPTIONS = [
        "全学教育推進機構",
        "マルチリンガル教育センター",
        "文学部",
        "人間科学部",
        "法学部",
        "経済学部",
        "理学部",
        "医学科",
        "保健学科",
        "歯学部",
        "薬学部",
        "工学部",
        "基礎工学部",
        "外国語学部",
    ]
    selected_option = st.selectbox("履修区分を選択してください", OPTIONS)
    st.session_state.selected_option = selected_option


async def initialize() -> tuple[RagV1, LLM]:
    """session_stateの初期化"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = "全学教育推進機構"

    client = SupabaseClient()
    insert_client = await InsertSupabase.new(client)
    search_client = await SearchSupabase.new(client)
    embedding_client = OpenAIEmbedding()
    rag = RagV1(insert_client, search_client, embedding_client)
    llm = GeminiLLM()

    return rag, llm


def reset_state():
    """会話履歴と選択肢をリセット"""
    st.session_state.chat_history = []
    st.session_state.selected_option = "全学教育推進機構"


if __name__ == "__main__":
    rag_client, llm_client = asyncio.run(initialize())

    header()

    select_form()

    chat(rag_client, llm_client)
