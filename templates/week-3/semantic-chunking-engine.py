"""Semantic chunking engine for intelligent document segmentation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SemanticChunk:
    chunk_id: int
    content: str
    topic: str


class SemanticChunkingEngine:
    """Generate semantically coherent document chunks."""

    def __init__(self, max_chunk_size: int = 300) -> None:
        self.max_chunk_size = max_chunk_size

    def detect_topic(self, sentence: str) -> str:
        """Very lightweight topic detector."""

        lowered = sentence.lower()

        if "retrieval" in lowered or "embedding" in lowered:
            return "retrieval"

        if "agent" in lowered or "workflow" in lowered:
            return "agentic_ai"

        return "general"

    def chunk_document(self, document: str) -> list[SemanticChunk]:
        """Chunk by semantic topic continuity."""

        sentences = [sentence.strip() for sentence in document.split(".") if sentence.strip()]

        chunks: list[SemanticChunk] = []

        current_topic = None
        current_chunk = []
        chunk_id = 1

        for sentence in sentences:
            detected_topic = self.detect_topic(sentence)

            if current_topic and detected_topic != current_topic:
                chunks.append(
                    SemanticChunk(
                        chunk_id=chunk_id,
                        content=". ".join(current_chunk),
                        topic=current_topic,
                    )
                )

                chunk_id += 1
                current_chunk = []

            current_topic = detected_topic
            current_chunk.append(sentence)

        if current_chunk:
            chunks.append(
                SemanticChunk(
                    chunk_id=chunk_id,
                    content=". ".join(current_chunk),
                    topic=current_topic or "general",
                )
            )

        return chunks


if __name__ == "__main__":
    engine = SemanticChunkingEngine()

    sample_document = (
        "Retrieval systems use embeddings for semantic search. "
        "Hybrid retrieval improves ranking quality. "
        "Agent workflows enable autonomous execution. "
        "Supervisor agents coordinate worker agents."
    )

    results = engine.chunk_document(sample_document)

    for chunk in results:
        print(chunk)
