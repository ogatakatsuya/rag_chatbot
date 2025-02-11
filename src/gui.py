import streamlit as st

from src.llm import LLM
from src.model import Message


def main():
    st.title("Chatbot")
    llm = LLM()

    if prompt := st.chat_input("何かお困りですか？"):
        # 入力内容を履歴に追加
        st.session_state.chat_history.append(Message(role="user", content=prompt))

        # チャット履歴を表示
        for message in st.session_state.chat_history:
            with st.chat_message(message.role):
                st.markdown(message.content)

        # LLM からの応答を取得
        with st.chat_message("assistant"):
            placeholder = st.empty()
            response: str = llm.get_response_with_context(
                st.session_state.chat_history, placeholder
            )

        st.session_state.chat_history.append(
            Message(role="assistant", content=response)
        )


def initialize():
    """session_stateの初期化処理を行う"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


if __name__ == "__main__":
    initialize()
    main()
