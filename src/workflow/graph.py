from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from src.workflow.nodes import classify_intent


SYSTEM_PROMPT="""You are an expert in news and information.

You have access to two tools:

- classify_intent: use this to get the intent of the user query
- handle_news_request: use this to handle requests regarding news
- handle_general_query: use this to answer general queries from the user

You respond based on the intent. If its a news query, get the latest news and summarize the headlines. 
Otherwise answer normally for general queries.
"""
class NewsGraph:
    
    def __init__(self, openai: ChatOpenAI):
        self.graph = create_agent(
            model=openai,
            tools=[classify_intent, ],
            system_prompt=SYSTEM_PROMPT
        )

