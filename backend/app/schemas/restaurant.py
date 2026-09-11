"""Restaurant and Branch Pydantic Schemas."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.core.constants import RestaurantStatus
from app.schemas.common import BaseSchema


# ------------------------------------------------------------------------------
# Branch Schemas
# ------------------------------------------------------------------------------
class RestaurantBranchBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=128)
    address_line: str = Field(..., max_length=255)
    city: str = Field(..., max_length=64)
    state_or_province: str | None = Field(default=None, max_length=64)
    postal_code: str | None = Field(default=None, max_length=32)
    country_code: str = Field(default="US", min_length=2, max_length=2)
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    phone: str | None = Field(default=None, max_length=32)


class RestaurantBranchCreate(RestaurantBranchBase):
    pass


class RestaurantBranchResponse(RestaurantBranchBase):
    id: uuid.UUID
    restaurant_id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ------------------------------------------------------------------------------
# Restaurant Schemas
# ------------------------------------------------------------------------------
class RestaurantBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=128)
    slug: str = Field(..., min_length=2, max_length=128)
    description: str | None = None
    logo_url: str | None = None
    cover_image_url: str | None = None


class RestaurantCreate(RestaurantBase):
    branches: list[RestaurantBranchCreate] = []


class RestaurantUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=2, max_length=128)
    description: str | None = None
    logo_url: str | None = None
    cover_image_url: str | None = None
    is_active: bool | None = None
    status: RestaurantStatus | None = None


class RestaurantResponse(RestaurantBase):
    id: uuid.UUID
    status: RestaurantStatus
    is_active: bool
    owner_id: uuid.UUID | None = None
    created_at: datetime
    updated_at: datetime
    branches: list[RestaurantBranchResponse] = []
