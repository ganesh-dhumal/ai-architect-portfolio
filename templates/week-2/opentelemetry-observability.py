"""OpenTelemetry observability instrumentation for AI systems."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any


class ObservabilityTracer:
    """Lightweight tracing manager."""

    def __init__(self) -> None:
        self.metrics: list[dict[str, Any]] = []

    @contextmanager
    def trace(self, operation_name: str):
        """Trace operation latency."""

        start_time = time.perf_counter()

        try:
            yield

            status = "success"

        except Exception:
            status = "failed"
            raise

        finally:
            latency_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            metric = {
                "operation": operation_name,
                "status": status,
                "latency_ms": latency_ms,
            }

            self.metrics.append(metric)

            print(f"TRACE: {metric}")

    def get_metrics(self) -> list[dict[str, Any]]:
        return self.metrics


if __name__ == "__main__":
    tracer = ObservabilityTracer()

    with tracer.trace("embedding_generation"):
        time.sleep(0.2)

    with tracer.trace("semantic_search"):
        time.sleep(0.1)

    print(tracer.get_metrics())
