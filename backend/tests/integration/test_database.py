"""Integration tests for database session and model persistence."""

from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Menu
from app.models.menu_category import MenuCategory
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant


@pytest.mark.asyncio
async def test_create_and_query_restaurant_hierarchy(db_session: AsyncSession) -> None:
    """Validate full relationship cascade from Restaurant -> Menu -> Category -> MenuItem."""
    # 1. Create Restaurant
    restaurant = Restaurant(
        name="Trattoria Romana",
        slug="trattoria-romana",
        description="Authentic Italian cuisine",
    )
    db_session.add(restaurant)
    await db_session.commit()
    await db_session.refresh(restaurant)
    assert restaurant.id is not None

    # 2. Create Menu
    menu = Menu(
        restaurant_id=restaurant.id,
        name="Dinner Menu",
        description="Evening specials",
    )
    db_session.add(menu)
    await db_session.commit()
    await db_session.refresh(menu)

    # 3. Create Category
    category = MenuCategory(
        menu_id=menu.id,
        name="Primi Piatti",
        display_order=1,
    )
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)

    # 4. Create MenuItem
    item = MenuItem(
        category_id=category.id,
        name="Carbonara Classica",
        price=Decimal("18.50"),
        currency="USD",
        calories=850,
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    # 5. Query and verify
    query = select(MenuItem).where(MenuItem.name == "Carbonara Classica")
    result = await db_session.execute(query)
    fetched_item = result.scalar_one()

    assert fetched_item.price == Decimal("18.50")
    assert fetched_item.category_id == category.id
