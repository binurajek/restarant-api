"""Integration tests for Repository layer."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import UserRole
from app.models.restaurant import Restaurant
from app.models.user import User
from app.repositories.restaurant import RestaurantRepository
from app.repositories.user import UserRepository


@pytest.mark.asyncio
async def test_user_repository_crud(db_session: AsyncSession) -> None:
    """Test UserRepository create and get_by_email."""
    repo = UserRepository(db_session)

    user = User(
        email="testuser@domain.com",
        hashed_password="fakehashedpassword",
        full_name="John Doe",
        role=UserRole.CUSTOMER,
    )
    created = await repo.create(user)
    assert created.id is not None

    found = await repo.get_by_email("testuser@domain.com")
    assert found is not None
    assert found.id == created.id
    assert found.full_name == "John Doe"

    # Case insensitive lookup
    found_upper = await repo.get_by_email("TESTUSER@DOMAIN.COM")
    assert found_upper is not None


@pytest.mark.asyncio
async def test_restaurant_repository_slug(db_session: AsyncSession) -> None:
    """Test RestaurantRepository get_by_slug."""
    repo = RestaurantRepository(db_session)

    restaurant = Restaurant(
        name="Sakura Sushi",
        slug="sakura-sushi",
        description="Fresh sushi and ramen",
    )
    await repo.create(restaurant)

    found = await repo.get_by_slug("sakura-sushi")
    assert found is not None
    assert found.name == "Sakura Sushi"

    not_found = await repo.get_by_slug("non-existent-slug")
    assert not_found is None
