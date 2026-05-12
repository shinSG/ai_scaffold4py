from abc import ABC, abstractmethod

from agent.abstractions.context import AgentContext


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, context: AgentContext) -> str:
        raise NotImplementedError


class EchoAgent(BaseAgent):
    name = "echo"

    async def run(self, context: AgentContext) -> str:
        return f"Echo: {context.user_input}"
