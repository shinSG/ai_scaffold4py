from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RAGResult:
    content: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class RAGPort(ABC):
    @abstractmethod
    async def retrieve(self, query: str, top_k: int = 5) -> list[RAGResult]:
        raise NotImplementedError

    @abstractmethod
    async def index(self, texts: list[str], metadata: list[dict[str, Any]] | None = None) -> None:
        raise NotImplementedError
