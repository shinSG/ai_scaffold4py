from agent_scaffold.agent.abstractions.base_agent import BaseAgent
from agent_scaffold.agent.abstractions.context import AgentContext
from agent_scaffold.infra.llm.ports import LLMProvider


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
