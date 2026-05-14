from __future__ import annotations

import logging
from typing import Any

from agent_scaffold.agent.callbacks.base_callback import BaseCallback


class LoggingCallback(BaseCallback):
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

    async def on_agent_start(self, agent_name: str, input_data: dict[str, Any]) -> None:
        self._logger.info("agent_start agent=%s input=%s", agent_name, input_data)

    async def on_agent_end(self, agent_name: str, output: str, metadata: dict[str, Any]) -> None:
        self._logger.info("agent_end agent=%s output_length=%d", agent_name, len(output))

    async def on_tool_start(self, tool_name: str, kwargs: dict[str, Any]) -> None:
        self._logger.info("tool_start tool=%s", tool_name)

    async def on_tool_end(self, tool_name: str, result: Any) -> None:
        self._logger.info("tool_end tool=%s", tool_name)

    async def on_llm_start(self, provider: str, prompt: str, metadata: dict[str, Any] | None = None) -> None:
        self._logger.info("llm_start provider=%s prompt_length=%d", provider, len(prompt))

    async def on_llm_end(self, provider: str, output: str) -> None:
        self._logger.info("llm_end provider=%s output_length=%d", provider, len(output))

    async def on_error(self, error: Exception, context: dict[str, Any] | None = None) -> None:
        self._logger.error("error=%s context=%s", error, context)
