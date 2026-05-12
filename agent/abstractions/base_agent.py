from abc import ABC, abstractmethod

from agent.abstractions.context import AgentContext
from integrations.llm.ports import LLMProvider


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, context: AgentContext) -> str:
        raise NotImplementedError


class EchoAgent(BaseAgent):
    name = "echo"

    async def run(self, context: AgentContext) -> str:
        return f"Echo: {context.user_input}"


class LLMAgent(BaseAgent):
    name = "llm"

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def run(self, context: AgentContext) -> str:
        system_prompt = context.metadata.get("system_prompt")
        if system_prompt is not None and not isinstance(system_prompt, str):
            system_prompt = None
        return await self._provider.generate(
            context.user_input,
            system_prompt=system_prompt,
            metadata=context.metadata,
        )
