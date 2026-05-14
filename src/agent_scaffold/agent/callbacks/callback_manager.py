from __future__ import annotations

from typing import Any

from agent_scaffold.agent.callbacks.base_callback import BaseCallback


class CallbackManager:
    def __init__(self, callbacks: list[BaseCallback] | None = None) -> None:
        self._callbacks = callbacks or []

    def add(self, callback: BaseCallback) -> None:
        self._callbacks.append(callback)

    def remove(self, callback: BaseCallback) -> None:
        self._callbacks = [cb for cb in self._callbacks if cb is not callback]

    async def on_agent_start(self, agent_name: str, input_data: dict[str, Any]) -> None:
        for cb in self._callbacks:
            await cb.on_agent_start(agent_name, input_data)

    async def on_agent_end(self, agent_name: str, output: str, metadata: dict[str, Any]) -> None:
        for cb in self._callbacks:
            await cb.on_agent_end(agent_name, output, metadata)

    async def on_tool_start(self, tool_name: str, kwargs: dict[str, Any]) -> None:
        for cb in self._callbacks:
            await cb.on_tool_start(tool_name, kwargs)

    async def on_tool_end(self, tool_name: str, result: Any) -> None:
        for cb in self._callbacks:
            await cb.on_tool_end(tool_name, result)

    async def on_llm_start(self, provider: str, prompt: str, metadata: dict[str, Any] | None = None) -> None:
        for cb in self._callbacks:
            await cb.on_llm_start(provider, prompt, metadata)

    async def on_llm_end(self, provider: str, output: str) -> None:
        for cb in self._callbacks:
            await cb.on_llm_end(provider, output)

    async def on_error(self, error: Exception, context: dict[str, Any] | None = None) -> None:
        for cb in self._callbacks:
            await cb.on_error(error, context)
