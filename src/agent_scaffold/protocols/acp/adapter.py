from agent_scaffold.protocols.acp.contracts import ACPRequest, ACPResponse


class ACPAdapter:
    async def handle(self, request: ACPRequest) -> ACPResponse:
        return ACPResponse(status="ok", data={"command": request.command, "arguments": request.arguments, "context": request.context})
