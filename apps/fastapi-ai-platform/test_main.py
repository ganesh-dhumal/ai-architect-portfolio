"""Integration tests for integrated FastAPI AI platform."""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "healthy"


def test_integrated_query_workflow() -> None:
    request_payload = {
        "query": "Explain hybrid retrieval",
        "session_id": "session-1",
    }

    response = client.post(
        "/api/v1/query",
        json=request_payload,
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["success"] is True
    assert "retrieved context" in payload["response"]
    assert payload["cached"] is False


def test_cache_hit_workflow() -> None:
    request_payload = {
        "query": "Explain hybrid retrieval",
        "session_id": "session-1",
    }

    client.post(
        "/api/v1/query",
        json=request_payload,
    )

    cached_response = client.post(
        "/api/v1/query",
        json=request_payload,
    )

    payload = cached_response.json()

    assert payload["cached"] is True
