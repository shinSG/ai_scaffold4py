from typing import Any

import httpx

from agent_scaffold.agent.tools.base_tool import BaseTool, ToolResult


class HTTPTool(BaseTool):
    name = "http_request"
    description = "Make an HTTP request to a URL"

    async def run(self, **kwargs: Any) -> ToolResult:
        url = kwargs.get("url", "")
        method = kwargs.get("method", "GET").upper()
        headers = kwargs.get("headers", {})
        body = kwargs.get("body")

        if not url:
            return ToolResult(success=False, output="", error="URL is required")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body if isinstance(body, dict) else None,
                    content=body if isinstance(body, str) else None,
                )
                return ToolResult(
                    success=response.is_success,
                    output=response.text,
                    metadata={"status_code": response.status_code},
                )
        except Exception as e:
            return ToolResult(success=False, output="", error=str(e))
