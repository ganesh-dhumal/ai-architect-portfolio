"""Citation-aware generation engine for grounded RAG responses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Citation:
    source_id: str
    source_text: str


@dataclass
class GroundedResponse:
    answer: str
    citations: list[Citation]


class CitationAwareGenerator:
    """Generate grounded AI responses with citations."""

    def generate_response(
        self,
        query: str,
        retrieved_documents: list[dict],
    ) -> GroundedResponse:
        """Generate citation-aware response."""

        answer_fragments = []
        citations = []

        for document in retrieved_documents:
            answer_fragments.append(document["content"])

            citations.append(
                Citation(
                    source_id=document["document_id"],
                    source_text=document["content"][:100],
                )
            )

        combined_answer = " ".join(answer_fragments)

        return GroundedResponse(
            answer=f"Grounded response for '{query}': {combined_answer}",
            citations=citations,
        )


if __name__ == "__main__":
    generator = CitationAwareGenerator()

    sample_docs = [
        {
            "document_id": "policy-1",
            "content": "Hybrid retrieval combines semantic and keyword search.",
        },
        {
            "document_id": "policy-2",
            "content": "Reranking improves retrieval quality.",
        },
    ]

    result = generator.generate_response(
        query="Explain hybrid retrieval",
        retrieved_documents=sample_docs,
    )

    print(result)
