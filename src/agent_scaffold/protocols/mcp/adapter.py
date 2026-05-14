from agent_scaffold.protocols.mcp.contracts import MCPRequest, MCPResponse


class MCPAdapter:
    async def handle(self, request: MCPRequest) -> MCPResponse:
        return MCPResponse(result={"echo_method": request.method, "params": request.params})
