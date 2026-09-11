"""Restaurant Repository Implementation."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.restaurant import Restaurant
from app.repositories.base import BaseRepository


class RestaurantRepository(BaseRepository[Restaurant]):
    """Data access repository for Restaurant entity."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Restaurant, session)

    async def get_by_slug(self, slug: str) -> Restaurant | None:
        """Find restaurant by URL slug."""
        query = select(Restaurant).where(Restaurant.slug == slug)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_with_branches(self, id: uuid.UUID) -> Restaurant | None:
        """Find restaurant with branches eagerly loaded."""
        query = (
            select(Restaurant).options(selectinload(Restaurant.branches)).where(Restaurant.id == id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
