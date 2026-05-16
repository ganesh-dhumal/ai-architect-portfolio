"""Workflow checkpointing manager for long-running agent systems."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class WorkflowCheckpointManager:
    """Persist and restore workflow state."""

    def __init__(self, checkpoint_dir: str = "checkpoints") -> None:
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)

    def save_checkpoint(
        self,
        workflow_id: str,
        state: dict[str, Any],
    ) -> Path:
        """Persist workflow state."""

        checkpoint_path = self.checkpoint_dir / f"{workflow_id}.json"

        with checkpoint_path.open("w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)

        return checkpoint_path

    def load_checkpoint(
        self,
        workflow_id: str,
    ) -> dict[str, Any]:
        """Restore workflow state."""

        checkpoint_path = self.checkpoint_dir / f"{workflow_id}.json"

        if not checkpoint_path.exists():
            raise FileNotFoundError(
                f"Checkpoint not found: {workflow_id}"
            )

        with checkpoint_path.open("r", encoding="utf-8") as file:
            return json.load(file)


if __name__ == "__main__":
    manager = WorkflowCheckpointManager()

    sample_state = {
        "query": "Explain RAG evaluation",
        "retrieved_documents": 5,
        "generation_complete": False,
    }

    manager.save_checkpoint(
        workflow_id="workflow-1",
        state=sample_state,
    )

    restored_state = manager.load_checkpoint("workflow-1")

    print(restored_state)
