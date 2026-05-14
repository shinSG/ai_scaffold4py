import pytest

from agent_scaffold.protocols.a2a.adapter import A2AAdapter
from agent_scaffold.protocols.a2a.contracts import A2ARequest


@pytest.mark.asyncio
async def test_a2a_adapter() -> None:
    adapter = A2AAdapter()
    resp = await adapter.handle(A2ARequest(action="sync", payload={"k": "v"}))
    assert resp.status == "ok"
