from typing import Any

from pydantic import BaseModel, Field


class LLMRunOptions(BaseModel):
    model: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    max_tokens: int | None = None
    enable_thinking: bool | None = None
    show_reasoning: bool | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class AgentRunRequest(BaseModel):
    session_id: str = Field(default="default")
    user_input: str
    llm_options: LLMRunOptions | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    session_id: str
    output: str
    metadata: dict[str, Any] = Field(default_factory=dict)
