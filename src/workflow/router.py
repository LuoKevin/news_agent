"""
Routes user messages to the appropriate handler based on intent.
"""

from src.core.intent import Intent, classify_intent
from src.workflow.handlers import (
    HandlerResult,
    handle_general_query,
    handle_news_request,
    handle_small_talk,
    handle_unknown,
)


def route_message(user_message: str) -> HandlerResult:
    intent_result = classify_intent(user_message)

    if intent_result.intent == Intent.NEWS_REQUEST:
        return handle_news_request(intent_result)
    if intent_result.intent == Intent.GENERAL_QUERY:
        return handle_general_query(intent_result)
    if intent_result.intent == Intent.SMALL_TALK:
        return handle_small_talk(intent_result)
    return handle_unknown(intent_result)
