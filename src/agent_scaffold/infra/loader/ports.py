from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class LoadedDocument:
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    source: str = ""


class DocumentLoader(ABC):
    @abstractmethod
    async def load(self, source: str) -> list[LoadedDocument]:
        raise NotImplementedError

    @abstractmethod
    async def load_bytes(self, data: bytes, filename: str = "") -> list[LoadedDocument]:
        raise NotImplementedError
