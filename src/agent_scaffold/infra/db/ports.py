from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, TypeVar

from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(ABC, Generic[ModelT]):
    @abstractmethod
    async def get(self, id: Any) -> ModelT | None: ...

    @abstractmethod
    async def get_multi(self, *, offset: int = 0, limit: int = 100) -> Sequence[ModelT]: ...

    @abstractmethod
    async def create(self, obj: ModelT) -> ModelT: ...

    @abstractmethod
    async def update(self, id: Any, obj: ModelT) -> ModelT | None: ...

    @abstractmethod
    async def delete(self, id: Any) -> bool: ...

    @abstractmethod
    async def count(self) -> int: ...
