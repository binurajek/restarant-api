"""Menu Repository Implementation."""

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.menu import Menu
from app.models.menu_category import MenuCategory
from app.repositories.base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    """Data access repository for Menu entity."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Menu, session)

    async def get_by_restaurant_id(self, restaurant_id: uuid.UUID) -> Sequence[Menu]:
        """Fetch all menus belonging to a restaurant."""
        query = select(Menu).where(Menu.restaurant_id == restaurant_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_with_categories_and_items(self, menu_id: uuid.UUID) -> Menu | None:
        """Fetch menu with categories and items eagerly loaded."""
        query = (
            select(Menu)
            .options(selectinload(Menu.categories).selectinload(MenuCategory.items))
            .where(Menu.id == menu_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
