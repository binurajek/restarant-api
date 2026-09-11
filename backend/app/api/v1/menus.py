"""Menus Management API Router."""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from app.services.menu import MenuService

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.post(
    "",
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new menu",
)
async def create_menu(
    menu_in: MenuCreate,
    db: AsyncSession = Depends(get_db),
) -> MenuResponse:
    """Create a new digital menu for a restaurant."""
    service = MenuService(db)
    menu = await service.create(menu_in)
    return MenuResponse.model_validate(menu)


@router.get(
    "/{menu_id}",
    response_model=MenuResponse,
    summary="Get menu by ID with categories and items",
)
async def get_menu(
    menu_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> MenuResponse:
    """Retrieve full menu structure including nested categories and menu items."""
    service = MenuService(db)
    menu = await service.get_by_id(menu_id)
    return MenuResponse.model_validate(menu)


@router.get(
    "/restaurant/{restaurant_id}",
    response_model=list[MenuResponse],
    summary="List all menus for a restaurant",
)
async def list_restaurant_menus(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[MenuResponse]:
    """Retrieve all menus configured for a given restaurant."""
    service = MenuService(db)
    menus = await service.list_by_restaurant(restaurant_id)
    return [MenuResponse.model_validate(m) for m in menus]


@router.patch(
    "/{menu_id}",
    response_model=MenuResponse,
    summary="Update menu details",
)
async def update_menu(
    menu_id: uuid.UUID,
    menu_in: MenuUpdate,
    db: AsyncSession = Depends(get_db),
) -> MenuResponse:
    """Update title, description, or status of a menu."""
    service = MenuService(db)
    menu = await service.update(menu_id, menu_in)
    return MenuResponse.model_validate(menu)
