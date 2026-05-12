from fastapi import WebSocket


class ConnectionManager:
    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

    async def send(self, websocket: WebSocket, message: str) -> None:
        await websocket.send_text(message)

    async def close(self, websocket: WebSocket) -> None:
        await websocket.close()
