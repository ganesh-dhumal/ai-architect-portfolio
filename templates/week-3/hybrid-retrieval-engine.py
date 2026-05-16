"""Hybrid retrieval engine combining semantic and keyword retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievalResult:
    document_id: str
    content: str
    semantic_score: float
    keyword_score: float
    combined_score: float


class HybridRetrievalEngine:
    """Combine vector and keyword retrieval strategies."""

    def __init__(
        self,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3,
    ) -> None:
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

    def semantic_search(self, query: str) -> list[dict[str, Any]]:
        """Simulated semantic retrieval."""

        return [
            {
                "document_id": "doc-1",
                "content": "Semantic retrieval uses embeddings.",
                "semantic_score": 0.92,
            },
            {
                "document_id": "doc-2",
                "content": "Hybrid search improves retrieval quality.",
                "semantic_score": 0.84,
            },
        ]

    def keyword_search(self, query: str) -> list[dict[str, Any]]:
        """Simulated BM25-style retrieval."""

        return [
            {
                "document_id": "doc-1",
                "keyword_score": 0.61,
            },
            {
                "document_id": "doc-2",
                "keyword_score": 0.74,
            },
        ]

    def hybrid_search(self, query: str) -> list[RetrievalResult]:
        """Combine retrieval scores."""

        semantic_results = self.semantic_search(query)
        keyword_results = self.keyword_search(query)

        keyword_map = {
            result["document_id"]: result["keyword_score"]
            for result in keyword_results
        }

        combined_results: list[RetrievalResult] = []

        for result in semantic_results:
            keyword_score = keyword_map.get(result["document_id"], 0.0)

            combined_score = round(
                (
                    result["semantic_score"] * self.semantic_weight
                    + keyword_score * self.keyword_weight
                ),
                2,
            )

            combined_results.append(
                RetrievalResult(
                    document_id=result["document_id"],
                    content=result["content"],
                    semantic_score=result["semantic_score"],
                    keyword_score=keyword_score,
                    combined_score=combined_score,
                )
            )

        return sorted(
            combined_results,
            key=lambda item: item.combined_score,
            reverse=True,
        )


if __name__ == "__main__":
    engine = HybridRetrievalEngine()

    results = engine.hybrid_search("Explain hybrid retrieval")

    for result in results:
        print(result)
