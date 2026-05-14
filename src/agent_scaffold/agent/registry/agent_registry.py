from agent_scaffold.agent.abstractions.base_agent import BaseAgent
from agent_scaffold.agent.agents.echo_agent import EchoAgent
from agent_scaffold.agent.agents.llm_agent import LLMAgent
from agent_scaffold.infra.llm.factory import get_llm_provider


class AgentRegistry:
    def __init__(self) -> None:
        llm_agent = LLMAgent(get_llm_provider())
        self._agents: dict[str, BaseAgent] = {
            llm_agent.name: llm_agent,
            EchoAgent.name: EchoAgent(),
        }

    def get(self, name: str) -> BaseAgent:
        return self._agents[name]
