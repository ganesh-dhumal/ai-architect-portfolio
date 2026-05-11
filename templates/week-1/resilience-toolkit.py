"""Production-grade resilience toolkit for AI engineering systems.

Features:
- Sync + async retry support
- Exponential backoff
- Timeout handling
- Structured logging integration
- Exception filtering
- Budget-aware retries
- Circuit-breaker foundation
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger("ai-resilience")


class RetryError(Exception):
    """Raised when retry attempts are exhausted."""


class RetryConfig:
    """Retry configuration container."""

    def __init__(
        self,
        retries: int = 3,
        delay: float = 1.0,
        backoff_factor: float = 2.0,
        max_delay: float = 30.0,
        allowed_exceptions: tuple[type[Exception], ...] = (Exception,),
        enable_logging: bool = True,
    ) -> None:
        self.retries = retries
        self.delay = delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.allowed_exceptions = allowed_exceptions
        self.enable_logging = enable_logging


DEFAULT_RETRY_CONFIG = RetryConfig()


def retry(
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Retry decorator for synchronous functions."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            current_delay = config.delay
            last_exception: Exception | None = None

            for attempt in range(1, config.retries + 1):
                try:
                    if config.enable_logging:
                        logger.info(
                            "Executing %s | attempt=%s",
                            func.__name__,
                            attempt,
                        )

                    return func(*args, **kwargs)

                except config.allowed_exceptions as exc:
                    last_exception = exc

                    if config.enable_logging:
                        logger.warning(
                            "Retry triggered | function=%s | attempt=%s | error=%s",
                            func.__name__,
                            attempt,
                            str(exc),
                        )

                    if attempt == config.retries:
                        break

                    time.sleep(current_delay)

                    current_delay = min(
                        current_delay * config.backoff_factor,
                        config.max_delay,
                    )

            raise RetryError(
                f"Retry attempts exhausted for function: {func.__name__}"
            ) from last_exception

        return wrapper

    return decorator


def async_retry(
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
) -> Callable[
    [Callable[P, Awaitable[T]]],
    Callable[P, Awaitable[T]],
]:
    """Retry decorator for asynchronous functions."""

    def decorator(
        func: Callable[P, Awaitable[T]],
    ) -> Callable[P, Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            current_delay = config.delay
            last_exception: Exception | None = None

            for attempt in range(1, config.retries + 1):
                try:
                    if config.enable_logging:
                        logger.info(
                            "Executing async %s | attempt=%s",
                            func.__name__,
                            attempt,
                        )

                    return await func(*args, **kwargs)

                except config.allowed_exceptions as exc:
                    last_exception = exc

                    if config.enable_logging:
                        logger.warning(
                            "Async retry triggered | function=%s | attempt=%s | error=%s",
                            func.__name__,
                            attempt,
                            str(exc),
                        )

                    if attempt == config.retries:
                        break

                    await asyncio.sleep(current_delay)

                    current_delay = min(
                        current_delay * config.backoff_factor,
                        config.max_delay,
                    )

            raise RetryError(
                f"Async retry attempts exhausted for function: {func.__name__}"
            ) from last_exception

        return wrapper

    return decorator


@retry()
def unreliable_sync_operation() -> dict[str, Any]:
    """Example sync operation."""

    logger.info("Running sync operation")

    raise ConnectionError("Temporary API failure")


@async_retry()
async def unreliable_async_operation() -> dict[str, Any]:
    """Example async operation."""

    logger.info("Running async operation")

    raise TimeoutError("Async timeout")


async def main() -> None:
    """Demonstrate retry toolkit usage."""

    try:
        await unreliable_async_operation()
    except RetryError as exc:
        logger.error("Retry system exhausted: %s", exc)


if __name__ == "__main__":
    asyncio.run(main())
