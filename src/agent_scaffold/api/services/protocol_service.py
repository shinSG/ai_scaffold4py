from agent_scaffold.protocols.a2a.adapter import A2AAdapter
from agent_scaffold.protocols.a2a.contracts import A2ARequest, A2AResponse
from agent_scaffold.protocols.acp.adapter import ACPAdapter
from agent_scaffold.protocols.acp.contracts import ACPRequest, ACPResponse
from agent_scaffold.protocols.mcp.adapter import MCPAdapter
from agent_scaffold.protocols.mcp.contracts import MCPRequest, MCPResponse


class ProtocolService:
    def __init__(self) -> None:
        self._mcp_adapter = MCPAdapter()
        self._a2a_adapter = A2AAdapter()
        self._acp_adapter = ACPAdapter()

    async def handle_mcp(self, payload: MCPRequest) -> MCPResponse:
        return await self._mcp_adapter.handle(payload)

    async def handle_a2a(self, payload: A2ARequest) -> A2AResponse:
        return await self._a2a_adapter.handle(payload)

    async def handle_acp(self, payload: ACPRequest) -> ACPResponse:
        return await self._acp_adapter.handle(payload)
