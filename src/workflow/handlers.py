"""
Handlers for each intent type.

These are stubs; wire them to real services (news API, LLM, etc.) later.
"""

from dataclasses import dataclass
from typing import Optional

from src.core.intent import IntentResult, Intent


@dataclass
class HandlerResult:
    message: str
    source: Optional[str] = None
    error: Optional[str] = None


def handle_news_request(intent: IntentResult) -> HandlerResult:
    """
    Placeholder news handler.

    TODO: integrate news API + summarization.
    """
    topic = intent.topic or "general news"
    return HandlerResult(
        message=f"(stub) Fetching latest news about {topic}.",
        source="news_handler_stub",
    )


def handle_general_query(intent: IntentResult) -> HandlerResult:
    """
    Placeholder general QA handler.

    TODO: call LLM or search + synthesis.
    """
    return HandlerResult(
        message=f"(stub) Answering general question: {intent.query}",
        source="general_handler_stub",
    )


def handle_small_talk(intent: IntentResult) -> HandlerResult:
    """
    Placeholder small-talk handler.
    """
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
