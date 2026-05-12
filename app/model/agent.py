from typing import Any

from pydantic import BaseModel, Field


class AgentRunRequest(BaseModel):
    session_id: str = Field(default="default")
    user_input: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    session_id: str
    output: str
    metadata: dict[str, Any] = Field(default_factory=dict)
