"""
Handlers for each intent type.

These are stubs; wire them to real services (news API, LLM, etc.) later.
"""

from dataclasses import dataclass
from typing import Optional
from openai import OpenAI

from src.core.config import Settings
from src.core.intent import IntentResult, Intent

@dataclass
class HandlerResult:
    message: str
    source: Optional[str] = None
    error: Optional[str] = None

settings = Settings()

openai_client = OpenAI(api_key=settings.openai_api_key)


def handle_news_request(intent: IntentResult) -> HandlerResult:
    """
    Placeholder news handler.

    TODO: integrate news API + summarization.
    """
    topic = intent.topic or "general"
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an expert news assistant.\n"
                "You fetch and summarize the latest news based on user queries."
                f"Focus on delivering new around this topic: {topic}."
                )
            },
            {"role": "user", "content": intent.query},
        ],
    )
    return HandlerResult(
        message = response.choices[0].message.content,
        source = "news_handler_stub",
    )


def handle_general_query(intent: IntentResult) -> HandlerResult:
    """
    Placeholder general QA handler.

    TODO: call LLM or search + synthesis.
    """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI powered information and news assistant.\n"
                " You answer general queries to help users navigate today's fast-paced digital landscape"
                )
            },
            {"role": "user", "content": intent.query},
        ],
    )

    return HandlerResult(
        message=response.choices[0].message.content
    )


def handle_small_talk(intent: IntentResult) -> HandlerResult:
    """
    Placeholder small-talk handler.
    """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI powered information and news assistant.\n"
                " You engage in friendly small talk to make users feel welcome."
                )
            },
            {"role": "user", "content": intent.query},
        ],
    )

    return HandlerResult(
        message="Hi! I can fetch news or answer questions. What would you like to know?",
        source="small_talk_handler_stub",
    )


def handle_unknown(intent: IntentResult) -> HandlerResult:
    """
    Default handler when intent is unclear or classification failed.
    """
    note = f" (error: {intent.error})" if intent.error else ""
    return HandlerResult(
        message=f"I'm not sure what you need.{note} Please ask for news on a topic or any question.",
        source="unknown_handler_stub",
        error=intent.error,
    )
