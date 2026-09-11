"""Restaurant Business Logic Service."""

import uuid
from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.branch import RestaurantBranch
from app.models.restaurant import Restaurant
from app.repositories.restaurant import RestaurantRepository
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    """Service handling restaurant operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = RestaurantRepository(session)

    async def create(
        self, restaurant_in: RestaurantCreate, owner_id: uuid.UUID | None = None
    ) -> Restaurant:
        """Create restaurant and any initial branches."""
        existing = await self.repository.get_by_slug(restaurant_in.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A restaurant with slug '{restaurant_in.slug}' already exists.",
            )

        restaurant = Restaurant(
            name=restaurant_in.name,
            slug=restaurant_in.slug,
            description=restaurant_in.description,
            logo_url=restaurant_in.logo_url,
            cover_image_url=restaurant_in.cover_image_url,
            owner_id=owner_id,
        )

        for b in restaurant_in.branches:
            branch = RestaurantBranch(
                name=b.name,
                address_line=b.address_line,
                city=b.city,
                state_or_province=b.state_or_province,
                postal_code=b.postal_code,
                country_code=b.country_code,
                latitude=b.latitude,
                longitude=b.longitude,
                phone=b.phone,
            )
            restaurant.branches.append(branch)

        created = await self.repository.create(restaurant)
        return await self.get_by_id(created.id)

    async def get_by_id(self, restaurant_id: uuid.UUID) -> Restaurant:
        """Get restaurant by ID with branches."""
        restaurant = await self.repository.get_with_branches(restaurant_id)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found.",
            )
        return restaurant

    async def get_by_slug(self, slug: str) -> Restaurant:
        """Get restaurant by slug."""
        restaurant = await self.repository.get_by_slug(slug)
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Restaurant '{slug}' not found.",
            )
        return restaurant

    async def list_restaurants(
        self, offset: int = 0, limit: int = 20
    ) -> tuple[Sequence[Restaurant], int]:
        """List restaurants with total count."""
        items = await self.repository.get_multi(offset=offset, limit=limit)
        total = await self.repository.count()
        return items, total

    async def update(self, restaurant_id: uuid.UUID, restaurant_in: RestaurantUpdate) -> Restaurant:
        """Update restaurant details."""
        restaurant = await self.get_by_id(restaurant_id)
        update_data = restaurant_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(restaurant, field, value)
        return await self.repository.update(restaurant)
