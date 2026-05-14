import pytest

from agent_scaffold.agent.tools.base_tool import ToolResult
from agent_scaffold.agent.tools.builtins.echo_tool import EchoTool
from agent_scaffold.agent.tools.builtins.http_tool import HTTPTool
from agent_scaffold.agent.tools.registry import ToolRegistry


@pytest.mark.asyncio
async def test_echo_tool() -> None:
    tool = EchoTool()
    result = await tool.run(text="hello world")
    assert result.success is True
    assert result.output == "hello world"


@pytest.mark.asyncio
async def test_echo_tool_empty() -> None:
    tool = EchoTool()
    result = await tool.run()
    assert result.success is True
    assert result.output == ""


@pytest.mark.asyncio
async def test_http_tool_missing_url() -> None:
    tool = HTTPTool()
    result = await tool.run()
    assert result.success is False
    assert "URL is required" in result.error


def test_tool_registry_register_and_get() -> None:
    registry = ToolRegistry()
    echo = EchoTool()
    registry.register(echo)

    assert registry.get("echo") is echo
    assert registry.get("nonexistent") is None


def test_tool_registry_list_tools() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())
    registry.register(HTTPTool())

    tools = registry.list_tools()
    assert len(tools) == 2
    names = {t.name for t in tools}
    assert names == {"echo", "http_request"}


def test_tool_registry_list_schemas() -> None:
    registry = ToolRegistry()
    registry.register(EchoTool())

    schemas = registry.list_schemas()
    assert len(schemas) == 1
    assert schemas[0]["name"] == "echo"
    assert "description" in schemas[0]


def test_tool_result_dataclass() -> None:
    result = ToolResult(success=True, output="ok", metadata={"code": 200})
    assert result.success is True
    assert result.output == "ok"
    assert result.error is None
    assert result.metadata["code"] == 200
