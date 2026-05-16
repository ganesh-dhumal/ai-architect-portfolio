"""WebSocket streaming API for real-time AI responses."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Streaming AI API")


class ConnectionManager:
    """Manage active websocket connections."""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, message: str) -> None:
        await websocket.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket) -> None:
    """Stream simulated AI token responses."""

    await manager.connect(websocket)

    try:
        while True:
            prompt = await websocket.receive_text()

            simulated_tokens = [
                "Agentic ",
                "AI ",
                "systems ",
                "support ",
                "autonomous ",
                "decision-making.",
            ]

            for token in simulated_tokens:
                payload = {
                    "token": token,
                    "timestamp": datetime.now(UTC).isoformat(),
                }

                await manager.send_message(
                    websocket,
                    str(payload),
                )

                await asyncio.sleep(0.2)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
