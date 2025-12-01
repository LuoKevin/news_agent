from dataclasses import dataclass
from typing import Optional

from src.core.intent import IntentResult 
from src.services.factories import get_news_client, get_openai_client

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
    try:
        news_client = get_news_client()[0]
        if news_client is None:
            return HandlerResult(
                message="Sorry, the news service is currently unavailable.",
                source="news_handler",
                error="news_client_unavailable",
            )


        news_response = news_client.get_latest_news(query=intent.topic or "general")
        if news_response.totalResults == 0:
            return HandlerResult(
                message=f"Sorry, I couldn't find any news articles about {intent.topic}.",
                source="news_handler_stub",
            )

        
        topic = intent.topic or "general"
        articles_summary = "\n".join(
            f"- {article.title}: {article.link}" for article in news_response.results[:5]
        )
    except Exception as e:
        return HandlerResult(
            message="Sorry, there was an error processing your request.",
            source="news_handler",
            error=str(e),
        )

    
    try:

        openai_client = get_openai_client()[0]
        if openai_client is None:
            return HandlerResult(
                message="Sorry, the AI service is currently unavailable.",
                source="news_handler",
                error="openai_client_unavailable",
            )


        chat_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are an expert news assistant.\n"
                    "Summarize these latest news articles."
                    f"Focus on delivering new around this topic: {topic}."
                    )
                },
                {"role": "user", "content": f"Summarize the following news articles:\n{articles_summary}"},
            ],
        )
    except Exception as e:
        return HandlerResult(
            message="Sorry, there was an error processing your request.",
            source="news_handler",
            error=str(e),
        )
    return HandlerResult(
        message = chat_response.choices[0].message.content,
        source = "news_handler_stub",
    )


def handle_general_query(intent: IntentResult) -> HandlerResult:
    """
    Placeholder general QA handler.

    TODO: call LLM or search + synthesis.
    """
    try:
        openai_client = get_openai_client()[0]
        if openai_client is None:
            return HandlerResult(
                message="Sorry, the AI service is currently unavailable.",
                source="general_query_handler",
                error="openai_client_unavailable",
            )

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
    except Exception as e:
        return HandlerResult(
            message="Sorry, there was an error processing your request.",
            source="general_query_handler",
            error=str(e),
        )

    return HandlerResult(
        message=response.choices[0].message.content
    )


def handle_small_talk(intent: IntentResult) -> HandlerResult:
    """
    Placeholder small-talk handler.
    """
    try:
        openai_client = get_openai_client()[0]
        if openai_client is None:
            return HandlerResult(
                message="Sorry, the AI service is currently unavailable.",
                source="general_query_handler",
                error="openai_client_unavailable",
            )


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
    except Exception as e:
        return HandlerResult(
            message="Sorry, there was an error processing your request.",
            source="small_talk_handler",
            error=str(e),
        )

    return HandlerResult(
        message=response.choices[0].message.content,
        source="small_talk_handler",
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
