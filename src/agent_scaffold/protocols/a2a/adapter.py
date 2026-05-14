from agent_scaffold.protocols.a2a.contracts import A2ARequest, A2AResponse


class A2AAdapter:
    async def handle(self, request: A2ARequest) -> A2AResponse:
        return A2AResponse(status="ok", data={"action": request.action, "payload": request.payload})
