from __future__ import annotations

from typing import Any, Sequence, Type

from sqlalchemy import func, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from agent_scaffold.infra.db.models import BaseModel


class SQLAlchemyRepository:
    def __init__(self, model: Type[BaseModel], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def get(self, id: Any) -> BaseModel | None:
        return await self._session.get(self._model, id)

    async def get_multi(self, *, offset: int = 0, limit: int = 100) -> Sequence[BaseModel]:
        stmt = select(self._model).offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj: BaseModel) -> BaseModel:
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return obj

    async def update(self, id: Any, obj: BaseModel) -> BaseModel | None:
        existing = await self._session.get(self._model, id)
        if existing is None:
            return None
        mapper = inspect(self._model)
        for col in mapper.columns:
            if col.name == "id":
                continue
            value = getattr(obj, col.name, None)
            if value is not None:
                setattr(existing, col.name, value)
        await self._session.flush()
        await self._session.refresh(existing)
        return existing

    async def delete(self, id: Any) -> bool:
        obj = await self._session.get(self._model, id)
        if obj is None:
            return False
        await self._session.delete(obj)
        await self._session.flush()
        return True

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self._model)
        result = await self._session.execute(stmt)
        return result.scalar() or 0
