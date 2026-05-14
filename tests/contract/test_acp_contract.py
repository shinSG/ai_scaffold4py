import pytest

from agent_scaffold.protocols.acp.adapter import ACPAdapter
from agent_scaffold.protocols.acp.contracts import ACPRequest


@pytest.mark.asyncio
async def test_acp_adapter() -> None:
    adapter = ACPAdapter()
    resp = await adapter.handle(ACPRequest(command="status", arguments={"verbose": True}))
    assert resp.status == "ok"
    assert resp.data["command"] == "status"
    assert resp.data["arguments"] == {"verbose": True}
