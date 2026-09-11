"""Generic Asynchronous Base Repository for SQLAlchemy 2.x."""

import uuid
from collections.abc import Sequence
from typing import Any, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository[ModelType: Base]:
    """Generic CRUD repository with asynchronous SQLAlchemy 2.x session."""

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, id: uuid.UUID | Any) -> ModelType | None:
        """Fetch single entity by primary key."""
        result = await self.session.get(self.model, id)
        return result

    async def get_multi(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> Sequence[ModelType]:
        """Fetch multiple entities with pagination."""
        query = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def count(self) -> int:
        """Count total entities of this type."""
        query = select(func.count()).select_from(self.model)
        result = await self.session.execute(query)
        return result.scalar() or 0

    async def create(self, entity: ModelType) -> ModelType:
        """Persist new entity."""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: ModelType) -> ModelType:
        """Commit changes to existing entity."""
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity: ModelType) -> None:
        """Remove entity from database."""
        await self.session.delete(entity)
        await self.session.commit()
