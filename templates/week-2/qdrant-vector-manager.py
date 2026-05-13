"""Qdrant vector database abstraction layer for RAG systems."""

from __future__ import annotations

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams


class QdrantVectorManager:
    """Production-ready Qdrant manager."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "ai_documents",
    ) -> None:
        self.collection_name = collection_name

        self.client = QdrantClient(host=host, port=port)

    def create_collection(self, vector_size: int = 1536) -> None:
        """Create vector collection."""

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_document(
        self,
        document_id: int,
        embedding: list[float],
        payload: dict[str, Any],
    ) -> None:
        """Insert vectorized document."""

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=document_id,
                    vector=embedding,
                    payload=payload,
                )
            ],
        )

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[Any]:
        """Perform semantic vector search."""

        return self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit,
        )


if __name__ == "__main__":
    manager = QdrantVectorManager()

    manager.create_collection()

    print("Qdrant collection initialized successfully")
