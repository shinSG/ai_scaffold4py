from fastapi import APIRouter, WebSocket
from sse_starlette.sse import EventSourceResponse

from agent_scaffold.api.services.stream_service import StreamService

router = APIRouter(prefix="/api/stream", tags=["stream"])
_service = StreamService()


@router.get("/sse")
async def sse_stream() -> EventSourceResponse:
    return await _service.sse_stream()


@router.websocket("/ws")
async def ws_stream(websocket: WebSocket) -> None:
    await _service.ws_stream(websocket)
