"""RAG evaluation framework with retrieval quality scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaluationResult:
    query: str
    relevance_score: float
    faithfulness_score: float
    latency_ms: float
    passed: bool


class RAGEvaluationFramework:
    """Evaluate retrieval and generation quality."""

    def evaluate(
        self,
        query: str,
        retrieved_context: str,
        generated_response: str,
        latency_ms: float,
    ) -> EvaluationResult:
        """Evaluate RAG pipeline quality."""

        relevance_score = self.compute_relevance(
            query,
            retrieved_context,
        )

        faithfulness_score = self.compute_faithfulness(
            generated_response,
            retrieved_context,
        )

        passed = (
            relevance_score >= 0.7
            and faithfulness_score >= 0.7
        )

        return EvaluationResult(
            query=query,
            relevance_score=relevance_score,
            faithfulness_score=faithfulness_score,
            latency_ms=latency_ms,
            passed=passed,
        )

    @staticmethod
    def compute_relevance(query: str, context: str) -> float:
        """Simulate relevance scoring."""

        query_terms = set(query.lower().split())
        context_terms = set(context.lower().split())

        overlap = query_terms.intersection(context_terms)

        return round(len(overlap) / max(len(query_terms), 1), 2)

    @staticmethod
    def compute_faithfulness(response: str, context: str) -> float:
        """Simulate faithfulness scoring."""

        response_terms = set(response.lower().split())
        context_terms = set(context.lower().split())

        overlap = response_terms.intersection(context_terms)

        return round(len(overlap) / max(len(response_terms), 1), 2)


if __name__ == "__main__":
    evaluator = RAGEvaluationFramework()

    result = evaluator.evaluate(
        query="Explain semantic retrieval",
        retrieved_context="Semantic retrieval uses embeddings for search.",
        generated_response="Semantic retrieval uses embeddings.",
        latency_ms=120.4,
    )

    print(result)
