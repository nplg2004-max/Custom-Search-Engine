import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    score: float = 0.0


class Searcher:
    def __init__(self, max_results: int = 5) -> None:
        self.max_results = max_results
        api_key = os.getenv("TAVILY_API_KEY", "")

        if not api_key:
            raise ValueError(
                "TAVILY_API_KEY not set. Get a free key at https://tavily.com"
            )

        from tavily import TavilyClient
        self._client = TavilyClient(api_key=api_key)

    def search(self, query: str) -> List[SearchResult]:
        response = self._client.search(
            query=query,
            max_results=self.max_results,
            search_depth="basic",
            include_answer=False,
        )

        return [
            SearchResult(
                title=item.get("title", "No title"),
                url=item.get("url", ""),
                content=item.get("content", ""),
                score=item.get("score", 0.0),
            )
            for item in response.get("results", [])
        ]
