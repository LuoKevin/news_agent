from newsdataapi import NewsDataApiClient
from pydantic import BaseModel

class NewsArticle(BaseModel):
    title: str
    description: str
    link: str
    content: str

class NewsResponse(BaseModel):
    status: str
    totalResults: int
    results: list[NewsArticle]

class NewsClient:
    client: NewsDataApiClient
    
    def __init__(self, api_key: str):
        self.client = NewsDataApiClient(apikey=api_key)
    
    def _api_to_news_response_map(self, api_response: dict) -> NewsResponse:
        return NewsResponse(
            status=api_response.get("status", ""),
            totalResults=api_response.get("totalResults", 0),
            results=[
                NewsArticle(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    link=article.get("link", ""),
                    content=article.get("content", "")
                ) for article in api_response.get("results", [])
            ]
        )

    def get_latest_news(self, query: str) -> NewsResponse:
        try:
            api_response = self.client.latest_api(q=query, language='en', sort="relevancy")
            news_response = self._api_to_news_response_map(api_response)
        except Exception as e:
            news_response = NewsResponse(status="error", totalResults=0, results=[])    
        return news_response
