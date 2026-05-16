"""Cross-encoder style reranking engine for RAG pipelines."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RankedDocument:
    document_id: str
    content: str
    initial_score: float
    reranked_score: float


class RerankingEngine:
    """Rerank retrieved documents for better relevance."""

    def rerank(
        self,
        query: str,
        documents: list[dict],
    ) -> list[RankedDocument]:
        """Apply simulated reranking logic."""

        reranked_documents: list[RankedDocument] = []

        for document in documents:
            bonus = 0.1 if query.lower() in document["content"].lower() else 0.0

            reranked_score = round(document["score"] + bonus, 2)

            reranked_documents.append(
                RankedDocument(
                    document_id=document["document_id"],
                    content=document["content"],
                    initial_score=document["score"],
                    reranked_score=reranked_score,
                )
            )

        return sorted(
            reranked_documents,
            key=lambda item: item.reranked_score,
            reverse=True,
        )


if __name__ == "__main__":
    engine = RerankingEngine()

    retrieved_docs = [
        {
            "document_id": "doc-1",
            "content": "Hybrid retrieval improves search relevance.",
            "score": 0.81,
        },
        {
            "document_id": "doc-2",
            "content": "Agentic AI enables autonomous workflows.",
            "score": 0.77,
        },
    ]

    results = engine.rerank(
        query="hybrid retrieval",
        documents=retrieved_docs,
    )

    for result in results:
        print(result)
