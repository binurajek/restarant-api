"""Restaurants Management API Router."""

import math
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.services.restaurant import RestaurantService

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.post(
    "",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new restaurant",
)
async def create_restaurant(
    restaurant_in: RestaurantCreate,
    db: AsyncSession = Depends(get_db),
) -> RestaurantResponse:
    """Create a new restaurant entity with optional initial branches."""
    service = RestaurantService(db)
    restaurant = await service.create(restaurant_in)
    return RestaurantResponse.model_validate(restaurant)


@router.get(
    "",
    response_model=PaginatedResponse[RestaurantResponse],
    summary="List restaurants with pagination",
)
async def list_restaurants(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[RestaurantResponse]:
    """Retrieve paginated restaurants list."""
    service = RestaurantService(db)
    offset = (page - 1) * page_size
    items, total = await service.list_restaurants(offset=offset, limit=page_size)

    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return PaginatedResponse(
        items=[RestaurantResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Get restaurant by ID",
)
async def get_restaurant(
    restaurant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> RestaurantResponse:
    """Retrieve complete restaurant information including physical branches."""
    service = RestaurantService(db)
    restaurant = await service.get_by_id(restaurant_id)
    return RestaurantResponse.model_validate(restaurant)


@router.get(
    "/by-slug/{slug}",
    response_model=RestaurantResponse,
    summary="Get restaurant by URL slug",
)
async def get_restaurant_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> RestaurantResponse:
    """Retrieve restaurant profile by its unique URL slug."""
    service = RestaurantService(db)
    restaurant = await service.get_by_slug(slug)
    return RestaurantResponse.model_validate(restaurant)


@router.patch(
    "/{restaurant_id}",
    response_model=RestaurantResponse,
    summary="Update restaurant profile",
)
async def update_restaurant(
    restaurant_id: uuid.UUID,
    restaurant_in: RestaurantUpdate,
    db: AsyncSession = Depends(get_db),
) -> RestaurantResponse:
    """Update details of an existing restaurant."""
    service = RestaurantService(db)
    restaurant = await service.update(restaurant_id, restaurant_in)
    return RestaurantResponse.model_validate(restaurant)
