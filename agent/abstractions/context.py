from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentContext:
    session_id: str
    user_input: str
    metadata: dict[str, Any] = field(default_factory=dict)
