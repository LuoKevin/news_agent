"""
OpenAI-backed intent classification for NewsGenie.

Detects whether a message is a news request or a general query. If the OpenAI API
key is missing, falls back to UNKNOWN with an error message so the caller can
surface a helpful notice.
"""

import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import openai


class Intent(str, Enum):
    NEWS_REQUEST = "news_request"
    GENERAL_QUERY = "general_query"
    SMALL_TALK = "small_talk"
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    intent: Intent
    confidence: float
    query: str
    topic: Optional[str] = None
    error: Optional[str] = None


def _build_prompt(user_message: str) -> str:
    # Constrain the model to a JSON response for easier downstream parsing.
    return (
        "You classify user messages into intents.\n"
        "Allowed intents: news_request, general_query, small_talk, unknown.\n"
        "If it is clearly asking for news about a topic or category (tech, finance, sports, politics, etc.), "
        "mark news_request and include the topic string. Otherwise general_query. "
        "Return JSON with keys: intent, confidence (0-1), topic (string or null).\n"
        f"User message: {user_message!r}"
    )


def _parse_response(text: str, query: str) -> IntentResult:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return IntentResult(
            intent=Intent.UNKNOWN,
            confidence=0.0,
            query=query,
            topic=None,
            error=f"parse_error: {exc}",
        )

    intent_str = str(data.get("intent", "unknown"))
    intent = Intent(intent_str) if intent_str in Intent._value2member_map_ else Intent.UNKNOWN
    confidence = float(data.get("confidence", 0.0) or 0.0)
    topic = data.get("topic")
    return IntentResult(
        intent=intent,
        confidence=max(0.0, min(confidence, 1.0)),
        query=query,
        topic=topic if topic else None,
        error=None if intent is not Intent.UNKNOWN else data.get("error"),
    )


def classify_intent(user_message: str) -> IntentResult:
    """
    Classify a user message using the OpenAI ChatCompletion API.

    Env:
    - OPENAI_API_KEY must be set.
    - Model defaults to gpt-3.5-turbo unless OPENAI_MODEL is set.
    """
    query = user_message.strip()
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    if not api_key:
        return IntentResult(
            intent=Intent.UNKNOWN,
            confidence=0.0,
            query=query,
            topic=None,
            error="missing OPENAI_API_KEY",
        )

    openai.api_key = api_key
    prompt = _build_prompt(query)
    try:
        completion = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a precise intent classifier."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=150,
        )
        text = completion["choices"][0]["message"]["content"]
        return _parse_response(text, query)
    except Exception as exc:  # noqa: BLE001
        return IntentResult(
            intent=Intent.UNKNOWN,
            confidence=0.0,
            query=query,
            topic=None,
            error=str(exc),
        )
