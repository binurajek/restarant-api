"""Menu Items API Router."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.models.menu_category import MenuCategory
from app.models.menu_item import MenuItem
from app.schemas.menu_item import MenuItemCreate, MenuItemResponse, MenuItemUpdate

router = APIRouter(prefix="/menu-items", tags=["Menu Items"])


@router.post(
    "",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a menu item",
)
async def create_menu_item(
    item_in: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
) -> MenuItemResponse:
    """Add a new item to a menu category."""
    category = await db.get(MenuCategory, item_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu category not found.",
        )

    item = MenuItem(
        category_id=item_in.category_id,
        name=item_in.name,
        description=item_in.description,
        price=item_in.price,
        currency=item_in.currency,
        image_url=item_in.image_url,
        is_available=item_in.is_available,
        calories=item_in.calories,
        preparation_time_minutes=item_in.preparation_time_minutes,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return MenuItemResponse.model_validate(item)


@router.get(
    "/{item_id}",
    response_model=MenuItemResponse,
    summary="Get menu item by ID",
)
async def get_menu_item(
    item_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> MenuItemResponse:
    """Retrieve specific dish/product item."""
    item = await db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found.",
        )
    return MenuItemResponse.model_validate(item)


@router.patch(
    "/{item_id}",
    response_model=MenuItemResponse,
    summary="Update menu item",
)
async def update_menu_item(
    item_id: uuid.UUID,
    item_in: MenuItemUpdate,
    db: AsyncSession = Depends(get_db),
) -> MenuItemResponse:
    """Update price, availability, or details of a menu item."""
    item = await db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found.",
        )

    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return MenuItemResponse.model_validate(item)
