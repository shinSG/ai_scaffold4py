from agent_scaffold.agent.orchestrator.agent_orchestrator import AgentOrchestrator
from agent_scaffold.api.models.agent import AgentRunRequest, AgentRunResponse


class AgentService:
    def __init__(self) -> None:
        self._orchestrator = AgentOrchestrator()

    async def run(self, payload: AgentRunRequest) -> AgentRunResponse:
        return await self._orchestrator.run(payload)
