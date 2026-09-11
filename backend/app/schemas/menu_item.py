"""Menu Item Pydantic Schemas."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.common import BaseSchema


class MenuItemBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = None
    price: Decimal = Field(
        ..., gt=Decimal("0.00"), decimal_places=2, description="Price in currency units"
    )
    currency: str = Field(default="USD", min_length=3, max_length=3)
    image_url: str | None = None
    is_available: bool = True
    calories: int | None = Field(default=None, ge=0)
    preparation_time_minutes: int | None = Field(default=None, ge=0)


class MenuItemCreate(MenuItemBase):
    category_id: uuid.UUID


class MenuItemUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=Decimal("0.00"), decimal_places=2)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    image_url: str | None = None
    is_available: bool | None = None
    calories: int | None = Field(default=None, ge=0)
    preparation_time_minutes: int | None = Field(default=None, ge=0)


class MenuItemResponse(MenuItemBase):
    id: uuid.UUID
    category_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
