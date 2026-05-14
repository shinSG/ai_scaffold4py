from agent_scaffold.agent.abstractions.context import AgentContext
from agent_scaffold.agent.registry.agent_registry import AgentRegistry
from agent_scaffold.api.models.agent import AgentRunRequest, AgentRunResponse


class AgentOrchestrator:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self._registry = registry or AgentRegistry()

    async def run(self, request: AgentRunRequest) -> AgentRunResponse:
        agent_name = request.metadata.get("agent", "llm")
        if not isinstance(agent_name, str):
            agent_name = "llm"
        agent = self._registry.get(agent_name)
        metadata = dict(request.metadata)
        if request.llm_options is not None:
            metadata["llm_options"] = request.llm_options.model_dump(exclude_none=True)
        context = AgentContext(
            session_id=request.session_id,
            user_input=request.user_input,
            metadata=metadata,
        )
        output = await agent.run(context)
        return AgentRunResponse(session_id=request.session_id, output=output, metadata={"agent": agent.name})
