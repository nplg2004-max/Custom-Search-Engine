import os
from typing import List

from dotenv import load_dotenv

from search_engine.searcher import SearchResult

load_dotenv()

SYSTEM_PROMPT = """You are a helpful search assistant.
Answer the user's question using ONLY the provided search results.
Be concise and factual. If the results don't contain enough information, say so.
Always cite sources using [1], [2], etc."""


def build_context(results: List[SearchResult]) -> str:
    parts = []
    for i, r in enumerate(results, start=1):
        snippet = r.content[:800] if len(r.content) > 800 else r.content
        parts.append(f"[{i}] {r.title}\nURL: {r.url}\n{snippet}")
    return "\n\n".join(parts)


class LLMClient:
    def __init__(self, model: str = "") -> None:
        self.model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
        api_key = os.getenv("GEMINI_API_KEY", "")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not set. Get a free key at https://aistudio.google.com"
            )

        from google import genai
        self._client = genai.Client(api_key=api_key)

    def answer(self, query: str, results: List[SearchResult]) -> str:
        if not results:
            return "No search results found. Cannot generate an answer."

        context = build_context(results)
        prompt = (
            f"Question: {query}\n\n"
            f"Search Results:\n{context}\n\n"
            f"Answer the question based on the search results above. "
            f"Cite sources with [1], [2], etc."
        )

        response = self._client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.3,
                "max_output_tokens": 2048,
            },
        )
        return response.text.strip()
