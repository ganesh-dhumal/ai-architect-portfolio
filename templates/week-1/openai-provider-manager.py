"""OpenAI provider abstraction layer with streaming support."""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncOpenAI


class OpenAIProvider:
    """Production-ready OpenAI abstraction manager."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
    ) -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        """Generate non-streaming response."""

        start_time = time.perf_counter()

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

        return {
            "success": True,
            "provider": "openai",
            "model": self.model,
            "latency_ms": latency_ms,
            "response": response.choices[0].message.content,
        }

    async def stream_response(
        self,
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        """Stream token responses."""

        stream = await self.client.chat.completions.create(
            model=self.model,
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta.content

            if delta:
                yield delta


async def main() -> None:
    """Streaming example."""

    provider = OpenAIProvider(api_key="replace-me")

    async for token in provider.stream_response(
        "Explain agentic AI systems"
    ):
        print(token, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
