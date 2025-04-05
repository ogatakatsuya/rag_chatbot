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
    st.header("大阪大学 履修支援チャットボット")

    if prompt := st.chat_input("何かお困りですか？"):
        st.session_state.chat_history.append(Message(role="user", content=prompt))

        for message in st.session_state.chat_history:
            with st.chat_message(message.role):
                st.markdown(message.content)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            rag_result = asyncio.run(rag.search(prompt, "全学教育推進機構"))
            response = llm.get_response_with_context(
                st.session_state.chat_history, placeholder, rag_result
            )

        st.session_state.chat_history.append(
            Message(role="assistant", content=response)
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

    chat_page(rag_client, llm_client)
