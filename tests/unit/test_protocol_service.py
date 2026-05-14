import pytest

from agent_scaffold.api.services.protocol_service import ProtocolService
from agent_scaffold.protocols.a2a.contracts import A2ARequest
from agent_scaffold.protocols.acp.contracts import ACPRequest
from agent_scaffold.protocols.mcp.contracts import MCPRequest


@pytest.mark.asyncio
async def test_protocol_service_dispatches_protocols() -> None:
    service = ProtocolService()

    mcp_resp = await service.handle_mcp(MCPRequest(method="ping", params={"x": 1}))
    a2a_resp = await service.handle_a2a(A2ARequest(action="sync", payload={"k": "v"}))
    acp_resp = await service.handle_acp(ACPRequest(command="status"))

    assert mcp_resp.result["echo_method"] == "ping"
    assert a2a_resp.status == "ok"
    assert acp_resp.data["command"] == "status"
