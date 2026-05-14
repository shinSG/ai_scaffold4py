from fastapi import WebSocket
from sse_starlette.sse import EventSourceResponse

from agent_scaffold.streaming.sse.emitter import demo_sse_stream
from agent_scaffold.streaming.websocket.connection_manager import ConnectionManager


class StreamService:
    def __init__(self) -> None:
        self._manager = ConnectionManager()

    async def sse_stream(self) -> EventSourceResponse:
        return EventSourceResponse(demo_sse_stream())

    async def ws_stream(self, websocket: WebSocket) -> None:
        await self._manager.connect(websocket)
        try:
            await self._manager.send(websocket, "stream-start")
            await self._manager.send(websocket, "stream-chunk: token-1")
            await self._manager.send(websocket, "stream-end")
        finally:
            await self._manager.close(websocket)
