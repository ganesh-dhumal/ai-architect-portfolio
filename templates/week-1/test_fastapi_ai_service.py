"""Integration tests for the FastAPI AI starter service.

Validation Goals:
- health endpoint validation
- AI inference endpoint validation
- middleware validation
- response schema validation
- error handling verification
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from fastapi_ai_service_template import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Validate health endpoint response."""

    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "healthy"
    assert payload["service"] == "ai-engineering-platform"
    assert payload["version"] == "0.1.0"


def test_ai_chat_endpoint() -> None:
    """Validate AI inference endpoint."""

    request_payload = {
        "query": "Explain RAG architecture",
        "session_id": "test-session",
        "metadata": {
            "source": "pytest",
        },
    }

    response = client.post(
        "/api/v1/ai/chat",
        json=request_payload,
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["success"] is True
    assert "Processed query" in payload["response"]
    assert payload["provider"] == "foundation-template"
    assert isinstance(payload["latency_ms"], float)


def test_system_info_endpoint() -> None:
    """Validate system information endpoint."""

    response = client.get("/api/v1/system/info")

    assert response.status_code == 200

    payload = response.json()

    assert payload["service"] == "AI Engineering Platform"
    assert isinstance(payload["uptime_seconds"], float)
    assert "FastAPI" in payload["features"]


def test_request_timing_middleware() -> None:
    """Validate request timing middleware."""

    response = client.get("/health")

    assert "X-Process-Time-MS" in response.headers


EXPECTED_HEALTH_RESPONSE = {
    "status": "healthy",
    "service": "ai-engineering-platform",
    "version": "0.1.0",
    "environment": "development",
}


EXPECTED_AI_RESPONSE_EXAMPLE = {
    "success": True,
    "response": (
        "Processed query: Explain RAG architecture. "
        "This endpoint is ready for LLM integration."
    ),
    "latency_ms": 0.25,
    "provider": "foundation-template",
}
