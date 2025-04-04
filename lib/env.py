import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_PROJECT_NUMBER: int
    OPENAI_API_KEY: str

    CHROME_DRIVER_PATH: str = "chromedriver"

    SUPABASE_URL: str
    SUPABASE_KEY: str

    model_config = SettingsConfigDict(
        env_file=f"{os.path.dirname(os.path.abspath(__file__))}/../.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


env = Env()  # type: ignore
