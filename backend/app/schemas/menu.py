"""Menu and Menu Category Pydantic Schemas."""

import uuid
from datetime import datetime

from pydantic import Field

from app.core.constants import MenuStatus
from app.schemas.common import BaseSchema
from app.schemas.menu_item import MenuItemResponse


# ------------------------------------------------------------------------------
# Category Schemas
# ------------------------------------------------------------------------------
class MenuCategoryBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=64)
    description: str | None = None
    display_order: int = Field(default=0, ge=0)


class MenuCategoryCreate(MenuCategoryBase):
    menu_id: uuid.UUID


class MenuCategoryResponse(MenuCategoryBase):
    id: uuid.UUID
    menu_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    items: list[MenuItemResponse] = []


# ------------------------------------------------------------------------------
# Menu Schemas
# ------------------------------------------------------------------------------
class MenuBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = None


class MenuCreate(MenuBase):
    restaurant_id: uuid.UUID


class MenuUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None
    status: MenuStatus | None = None
    is_active: bool | None = None


class MenuResponse(MenuBase):
    id: uuid.UUID
    restaurant_id: uuid.UUID
    status: MenuStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    categories: list[MenuCategoryResponse] = []
