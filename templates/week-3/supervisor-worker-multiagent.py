"""Supervisor-worker multi-agent orchestration architecture."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    task_id: str
    description: str
    assigned_agent: str | None = None
    status: str = "pending"


class WorkerAgent:
    """Worker agent execution unit."""

    def __init__(self, name: str) -> None:
        self.name = name

    def execute(self, task: Task) -> dict[str, Any]:
        task.assigned_agent = self.name
        task.status = "completed"

        return {
            "task_id": task.task_id,
            "worker": self.name,
            "status": task.status,
            "result": (
                f"Completed task: {task.description}"
            ),
        }


class SupervisorAgent:
    """Supervisor responsible for orchestration."""

    def __init__(self) -> None:
        self.workers = {
            "retrieval": WorkerAgent("retrieval-agent"),
            "generation": WorkerAgent("generation-agent"),
            "evaluation": WorkerAgent("evaluation-agent"),
        }

    def assign_task(
        self,
        task_type: str,
        task: Task,
    ) -> dict[str, Any]:
        if task_type not in self.workers:
            raise ValueError(f"Unknown worker type: {task_type}")

        worker = self.workers[task_type]

        return worker.execute(task)


if __name__ == "__main__":
    supervisor = SupervisorAgent()

    retrieval_task = Task(
        task_id="task-1",
        description="Retrieve enterprise policy documents",
    )

    result = supervisor.assign_task(
        task_type="retrieval",
        task=retrieval_task,
    )

    print(result)
