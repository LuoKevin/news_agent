from langchain.tools import tool

from src.services.factories import get_news_client
from src.workflow.nodes.handlers import HandlerResult
from src.workflow.nodes.intent import IntentResult

@tool
def get_news(intent:IntentResult) -> HandlerResult:
    client = get_news_client()
    client.han
    

    