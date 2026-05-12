from agent.abstractions.base_agent import BaseAgent, EchoAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {EchoAgent.name: EchoAgent()}

    def get(self, name: str) -> BaseAgent:
        return self._agents[name]
