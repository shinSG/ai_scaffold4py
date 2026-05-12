from app.schemas.agent import AgentRunRequest, AgentRunResponse
from agent.abstractions.context import AgentContext
from agent.registry.agent_registry import AgentRegistry


class AgentOrchestrator:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self._registry = registry or AgentRegistry()

    async def run(self, request: AgentRunRequest) -> AgentRunResponse:
        agent = self._registry.get("echo")
        context = AgentContext(
            session_id=request.session_id,
            user_input=request.user_input,
            metadata=request.metadata,
        )
        output = await agent.run(context)
        return AgentRunResponse(session_id=request.session_id, output=output, metadata={"agent": agent.name})
