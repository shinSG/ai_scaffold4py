from abc import ABC, abstractmethod
from typing import Any


class NacosPort(ABC):
    @abstractmethod
    async def register(self, metadata: dict[str, Any] | None = None, service_name: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def deregister(self, service_name: str | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def discover(self, service_name: str) -> list[dict]:
        raise NotImplementedError
