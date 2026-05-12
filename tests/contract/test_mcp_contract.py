import pytest

from protocols.mcp.adapter import MCPAdapter
from protocols.mcp.contracts import MCPRequest


@pytest.mark.asyncio
async def test_mcp_adapter() -> None:
    adapter = MCPAdapter()
    resp = await adapter.handle(MCPRequest(method="ping", params={"x": 1}))
    assert resp.result["echo_method"] == "ping"
