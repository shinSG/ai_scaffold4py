from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ProtocolAdapter(ABC):
    @abstractmethod
    async def handle(self, request: Any) -> Any:
        raise NotImplementedError
