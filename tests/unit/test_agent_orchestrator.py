import pytest

from agent.orchestrator.agent_orchestrator import AgentOrchestrator
from app.schemas.agent import AgentRunRequest


@pytest.mark.asyncio
async def test_orchestrator_run() -> None:
    orchestrator = AgentOrchestrator()
    result = await orchestrator.run(AgentRunRequest(user_input="hello"))
    assert "Echo" in result.output
