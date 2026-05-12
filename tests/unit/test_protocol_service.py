import pytest

from app.service.protocol_service import ProtocolService
from protocols.a2a.contracts import A2ARequest
from protocols.acp.contracts import ACPRequest
from protocols.mcp.contracts import MCPRequest


@pytest.mark.asyncio
async def test_protocol_service_dispatches_protocols() -> None:
    service = ProtocolService()

    mcp_resp = await service.handle_mcp(MCPRequest(method="ping", params={"x": 1}))
    a2a_resp = await service.handle_a2a(A2ARequest(action="sync", payload={"k": "v"}))
    acp_resp = await service.handle_acp(ACPRequest(command="status"))

    assert mcp_resp.result["echo_method"] == "ping"
    assert a2a_resp.status == "ok"
    assert acp_resp.data["command"] == "status"
