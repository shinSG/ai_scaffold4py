from agent.abstractions.base_agent import BaseAgent, EchoAgent, LLMAgent
from integrations.llm.factory import get_llm_provider


class AgentRegistry:
    def __init__(self) -> None:
        llm_agent = LLMAgent(get_llm_provider())
        self._agents: dict[str, BaseAgent] = {
            llm_agent.name: llm_agent,
            EchoAgent.name: EchoAgent(),
        }

    def get(self, name: str) -> BaseAgent:
        return self._agents[name]
