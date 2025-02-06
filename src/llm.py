import os

from google import genai
from dotenv import load_dotenv
from src.prompt import SYSTEM_PROMPT

load_dotenv()


class LLM:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash-exp"

    def get_response(self, prompt: str) -> str:
        """
        LLMから返答分を取得する

        Args:
            prompt(str): LLMに投げるプロンプト
        Returns:
            str: LLMが生成した返答文
        """
        response = self.client.models.generate_content(
            model=self.model, contents=f"{SYSTEM_PROMPT}\n\nprompt: {prompt}"
        )
        return response.text
