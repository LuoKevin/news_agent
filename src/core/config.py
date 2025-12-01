
from pydantic import BaseSettings

class Settings(BaseSettings):
    news_api_key: str
    openai_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"