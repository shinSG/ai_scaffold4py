from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class StreamEvent:
    event: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
