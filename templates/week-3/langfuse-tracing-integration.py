"""LangFuse-style tracing integration for GenAI observability."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class TraceEvent:
    operation: str
    latency_ms: float
    metadata: dict[str, Any]


class LangFuseTracer:
    """Minimal tracing manager for AI workflows."""

    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    def trace(
        self,
        operation: str,
        metadata: dict[str, Any],
    ) -> TraceEvent:
        """Create trace event."""

        start_time = time.perf_counter()

        time.sleep(0.05)

        latency_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        event = TraceEvent(
            operation=operation,
            latency_ms=latency_ms,
            metadata=metadata,
        )

        self.events.append(event)

        return event

    def export_traces(self) -> list[dict[str, Any]]:
        """Export tracing payloads."""

        return [
            {
                "operation": event.operation,
                "latency_ms": event.latency_ms,
                "metadata": event.metadata,
            }
            for event in self.events
        ]


if __name__ == "__main__":
    tracer = LangFuseTracer()

    tracer.trace(
        operation="rag_retrieval",
        metadata={
            "query": "Explain hybrid retrieval",
            "documents_retrieved": 5,
        },
    )

    tracer.trace(
        operation="response_generation",
        metadata={
            "model": "gpt-4o-mini",
            "tokens": 320,
        },
    )

    print(tracer.export_traces())
