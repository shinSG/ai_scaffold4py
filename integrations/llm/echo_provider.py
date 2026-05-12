from typing import Any

from integrations.llm.ports import LLMProvider


class EchoLLMProvider(LLMProvider):
    name = "echo"

    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        return f"Echo: {prompt}"