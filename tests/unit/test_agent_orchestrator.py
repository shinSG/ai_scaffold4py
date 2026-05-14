import pytest

from agent_scaffold.agent.orchestrator.agent_orchestrator import AgentOrchestrator
from agent_scaffold.api.models.agent import AgentRunRequest
from agent_scaffold.core.config import get_settings


@pytest.mark.asyncio
async def test_orchestrator_run(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "echo")
    get_settings.cache_clear()
    orchestrator = AgentOrchestrator()
    result = await orchestrator.run(AgentRunRequest(user_input="hello"))
    assert "Echo" in result.output
    get_settings.cache_clear()
