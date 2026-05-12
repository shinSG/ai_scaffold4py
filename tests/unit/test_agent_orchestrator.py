import pytest

from agent.orchestrator.agent_orchestrator import AgentOrchestrator
from app.schemas.agent import AgentRunRequest
from core.config import get_settings


@pytest.mark.asyncio
async def test_orchestrator_run(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "echo")
    get_settings.cache_clear()
    orchestrator = AgentOrchestrator()
    result = await orchestrator.run(AgentRunRequest(user_input="hello"))
    assert "Echo" in result.output
    get_settings.cache_clear()
