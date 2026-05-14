"""Agent memory manager for conversational AI workflows."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


class AgentMemoryManager:
    """Session-aware conversational memory."""

    def __init__(self) -> None:
        self.memory_store: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def add_interaction(
        self,
        session_id: str,
        user_query: str,
        ai_response: str,
    ) -> None:
        """Store conversation interaction."""

        self.memory_store[session_id].append(
            {
                "user_query": user_query,
                "ai_response": ai_response,
            }
        )

    def get_memory(
        self,
        session_id: str,
    ) -> list[dict[str, Any]]:
        """Retrieve session memory."""

        return self.memory_store.get(session_id, [])

    def clear_memory(self, session_id: str) -> None:
        """Clear session memory."""

        self.memory_store.pop(session_id, None)


if __name__ == "__main__":
    manager = AgentMemoryManager()

    manager.add_interaction(
        session_id="session-1",
        user_query="Explain LangGraph",
        ai_response="LangGraph enables agent workflows.",
    )

    print(manager.get_memory("session-1"))
