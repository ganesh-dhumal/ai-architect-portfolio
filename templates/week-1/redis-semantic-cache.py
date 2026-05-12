"""Redis semantic cache manager for AI inference systems."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import redis


class RedisSemanticCache:
    """Semantic caching manager for LLM responses."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        ttl_seconds: int = 3600,
    ) -> None:
        self.client = redis.from_url(redis_url)
        self.ttl_seconds = ttl_seconds

    @staticmethod
    def build_cache_key(prompt: str, model: str) -> str:
        """Create deterministic cache key."""

        raw_key = f"{model}:{prompt}"

        return hashlib.sha256(raw_key.encode()).hexdigest()

    def get_cached_response(
        self,
        prompt: str,
        model: str,
    ) -> dict[str, Any] | None:
        """Fetch cached response if available."""

        cache_key = self.build_cache_key(prompt, model)

        cached_value = self.client.get(cache_key)

        if not cached_value:
            return None

        return json.loads(cached_value)

    def store_response(
        self,
        prompt: str,
        model: str,
        response_payload: dict[str, Any],
    ) -> None:
        """Store AI response in Redis cache."""

        cache_key = self.build_cache_key(prompt, model)

        self.client.setex(
            cache_key,
            self.ttl_seconds,
            json.dumps(response_payload),
        )

    def invalidate_cache(
        self,
        prompt: str,
        model: str,
    ) -> None:
        """Delete cached entry."""

        cache_key = self.build_cache_key(prompt, model)

        self.client.delete(cache_key)


if __name__ == "__main__":
    cache = RedisSemanticCache()

    sample_response = {
        "response": "Agentic AI uses autonomous workflows.",
        "provider": "openai",
    }

    cache.store_response(
        prompt="Explain agentic AI",
        model="gpt-4o-mini",
        response_payload=sample_response,
    )

    result = cache.get_cached_response(
        prompt="Explain agentic AI",
        model="gpt-4o-mini",
    )

    print(result)
