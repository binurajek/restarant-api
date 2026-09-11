"""Menu Business Logic Service."""

import uuid
from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Menu
from app.repositories.menu import MenuRepository
from app.repositories.restaurant import RestaurantRepository
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuService:
    """Service handling menu and menu category operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = MenuRepository(session)
        self.restaurant_repo = RestaurantRepository(session)

    async def create(self, menu_in: MenuCreate) -> Menu:
        """Create new menu for a restaurant."""
        restaurant = await self.restaurant_repo.get(menu_in.restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )

        menu = Menu(
            restaurant_id=menu_in.restaurant_id,
            name=menu_in.name,
            description=menu_in.description,
        )
        return await self.repository.create(menu)

    async def get_by_id(self, menu_id: uuid.UUID) -> Menu:
        """Get menu with categories and items."""
        menu = await self.repository.get_with_categories_and_items(menu_id)
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu not found.",
            )
        return menu

    async def list_by_restaurant(self, restaurant_id: uuid.UUID) -> Sequence[Menu]:
        """List all menus for a specific restaurant."""
        return await self.repository.get_by_restaurant_id(restaurant_id)

    async def update(self, menu_id: uuid.UUID, menu_in: MenuUpdate) -> Menu:
        """Update menu details."""
        menu = await self.get_by_id(menu_id)
        update_data = menu_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(menu, field, value)
        return await self.repository.update(menu)
