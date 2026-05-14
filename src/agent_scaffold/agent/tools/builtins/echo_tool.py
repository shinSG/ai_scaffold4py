from agent_scaffold.agent.tools.base_tool import BaseTool, ToolResult


class EchoTool(BaseTool):
    name = "echo"
    description = "Echo back the input text"

    async def run(self, **kwargs) -> ToolResult:
        text = kwargs.get("text", "")
        return ToolResult(success=True, output=str(text))
