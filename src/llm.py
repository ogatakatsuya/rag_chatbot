import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from jinja2 import Template
from openai import OpenAI

from src.model import Message
from src.prompt import SYSTEM_PROMPT
from src.rag import RagService

load_dotenv()


class LLM:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.openai_client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/",
        )
        self.model = "gemini-2.0-flash-exp"
        self.rag_client = RagService(Path("./data/class_data_embeddings.json"))

    def get_response(self, prompt: str) -> str:
        """
        LLMから返答分を取得する

        Args:
            prompt(str): LLMに投げるプロンプト
        Returns:
            str: LLMが生成した返答文
        """
        response = self.gemini_client.models.generate_content(
            model=self.model, contents=f"{SYSTEM_PROMPT}\n\nprompt: {prompt}"
        )
        return response.text

    def get_response_with_context(self, context: list[Message], placeholder) -> str:
        """
        会話の文脈を考慮してLLMから返答文を取得する

        Args:
            context (list[Message]): 会話履歴
            placeholder (): Streamlit のプレースホルダー
        Returns:
            str: LLMが生成した返答文
        """
        # queryを用いてRAGで検索
        rag_result = self.rag_client.search(context[-1].content)
        sysytem_prompt = Template(SYSTEM_PROMPT).render(rag_result=rag_result)
        prompt = [Message(role="system", content=sysytem_prompt)] + context
        response = self.openai_client.chat.completions.create(
            model=self.model,
            n=1,
            messages=[message.cast_to_openai_schema() for message in prompt],
            stream=True,
        )

        accumulated_text = ""
        for chunk in response:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                accumulated_text += delta_content
                placeholder.markdown(accumulated_text)

        return accumulated_text
