from functools import lru_cache
from typing import Optional, Tuple

from openai import OpenAI
from src.core.config import Settings
from src.services.news_client import NewsClient

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_news_client() -> Tuple[Optional[NewsClient], Optional[str]]:
    try:
        settings = get_settings()
        if not settings.NEWS_API_KEY:
            return None, "news_api_key_missing"
        news_client = NewsClient(api_key=settings.NEWS_API_KEY)
        return news_client, None
    except Exception as e:
        return None, str(e)
    
def get_openai_client() -> Tuple[Optional[OpenAI], Optional[str]]:
    try:
        settings = get_settings()
        if not settings.OPENAI_API_KEY:
            return None, "openai_api_key_missing"
        openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return openai_client, None
    except Exception as e:
        return None, str(e) 