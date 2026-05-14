import pytest

from agent_scaffold.agent.callbacks.base_callback import BaseCallback
from agent_scaffold.agent.callbacks.callback_manager import CallbackManager
from agent_scaffold.agent.callbacks.logging_callback import LoggingCallback


class RecordingCallback(BaseCallback):
    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    async def on_agent_start(self, agent_name: str, input_data: dict) -> None:
        self.events.append(("agent_start", {"agent_name": agent_name}))

    async def on_agent_end(self, agent_name: str, output: str, metadata: dict) -> None:
        self.events.append(("agent_end", {"agent_name": agent_name}))

    async def on_tool_start(self, tool_name: str, kwargs: dict) -> None:
        self.events.append(("tool_start", {"tool_name": tool_name}))

    async def on_tool_end(self, tool_name: str, result) -> None:
        self.events.append(("tool_end", {"tool_name": tool_name}))

    async def on_error(self, error: Exception, context: dict | None = None) -> None:
        self.events.append(("error", {"error": str(error)}))


@pytest.mark.asyncio
async def test_callback_manager_dispatches_to_all_callbacks() -> None:
    cb1 = RecordingCallback()
    cb2 = RecordingCallback()
    manager = CallbackManager([cb1, cb2])

    await manager.on_agent_start("test-agent", {"input": "hello"})
    await manager.on_agent_end("test-agent", "output", {})

    assert len(cb1.events) == 2
    assert len(cb2.events) == 2
    assert cb1.events[0] == ("agent_start", {"agent_name": "test-agent"})
    assert cb1.events[1] == ("agent_end", {"agent_name": "test-agent"})


@pytest.mark.asyncio
async def test_callback_manager_add_and_remove() -> None:
    cb = RecordingCallback()
    manager = CallbackManager()
    manager.add(cb)

    await manager.on_agent_start("test", {})
    assert len(cb.events) == 1

    manager.remove(cb)
    await manager.on_agent_start("test2", {})
    assert len(cb.events) == 1


@pytest.mark.asyncio
async def test_logging_callback() -> None:
    callback = LoggingCallback()
    await callback.on_agent_start("test-agent", {"input": "hello"})
    await callback.on_agent_end("test-agent", "output", {})
    await callback.on_tool_start("echo", {"text": "hi"})
    await callback.on_tool_end("echo", "result")
    await callback.on_llm_start("openai", "prompt")
    await callback.on_llm_end("openai", "response")
    await callback.on_error(ValueError("test error"))
