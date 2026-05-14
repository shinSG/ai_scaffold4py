from typing import Any

from pydantic import BaseModel, Field


class ACPRequest(BaseModel):
    command: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    context: dict[str, Any] = Field(default_factory=dict)


class ACPResponse(BaseModel):
    status: str
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
