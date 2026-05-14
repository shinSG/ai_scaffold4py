from __future__ import annotations

from abc import ABC
from typing import Any


class BaseCallback(ABC):
    async def on_agent_start(self, agent_name: str, input_data: dict[str, Any]) -> None:
        pass

    async def on_agent_end(self, agent_name: str, output: str, metadata: dict[str, Any]) -> None:
        pass

    async def on_tool_start(self, tool_name: str, kwargs: dict[str, Any]) -> None:
        pass

    async def on_tool_end(self, tool_name: str, result: Any) -> None:
        pass

    async def on_llm_start(self, provider: str, prompt: str, metadata: dict[str, Any] | None = None) -> None:
        pass

    async def on_llm_end(self, provider: str, output: str) -> None:
        pass

    async def on_error(self, error: Exception, context: dict[str, Any] | None = None) -> None:
        pass
