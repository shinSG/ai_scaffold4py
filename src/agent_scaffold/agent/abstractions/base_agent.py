from abc import ABC, abstractmethod

from agent_scaffold.agent.abstractions.context import AgentContext


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, context: AgentContext) -> str:
        raise NotImplementedError
