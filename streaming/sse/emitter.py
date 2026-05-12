import asyncio
from collections.abc import AsyncIterator

from streaming.events import StreamEvent


async def demo_sse_stream() -> AsyncIterator[dict[str, str]]:
    for idx in range(3):
        event = StreamEvent(event="chunk", data={"index": idx, "text": f"token-{idx}"})
        yield {"event": event.event, "data": str(event.to_dict())}
        await asyncio.sleep(0.1)
    yield {"event": "end", "data": "done"}
