from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] = field(default_factory=list)
    id: str = ""


@dataclass
class SearchResult:
    document: Document
    score: float


class VectorStore(ABC):
    @abstractmethod
    async def add(self, documents: list[Document]) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, ids: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError
