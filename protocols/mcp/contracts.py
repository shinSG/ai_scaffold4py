from pydantic import BaseModel


class MCPRequest(BaseModel):
    method: str
    params: dict


class MCPResponse(BaseModel):
    result: dict
    error: str | None = None
