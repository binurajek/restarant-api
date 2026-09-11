"""Unit tests for Pydantic v2 schemas validation."""

import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.menu_item import MenuItemCreate
from app.schemas.user import UserCreate


def test_user_create_validation() -> None:
    """Test UserCreate valid and invalid payloads."""
    valid_data = {
        "email": "chef@ristorante.com",
        "full_name": "Mario Rossi",
        "password": "supersecretpassword123",
    }
    user = UserCreate(**valid_data)
    assert user.email == "chef@ristorante.com"

    with pytest.raises(ValidationError):
        # Short password
        UserCreate(email="chef@ristorante.com", full_name="Mario", password="short")

    with pytest.raises(ValidationError):
        # Invalid email
        UserCreate(email="not-an-email", full_name="Mario", password="validpassword123")


def test_menu_item_price_decimal_validation() -> None:
    """Validate price requires Decimal and greater than zero."""
    cat_id = uuid.uuid4()
    item = MenuItemCreate(
        name="Truffle Pasta",
        price=Decimal("24.50"),
        category_id=cat_id,
    )
    assert item.price == Decimal("24.50")
    assert isinstance(item.price, Decimal)

    with pytest.raises(ValidationError):
        # Negative or zero price
        MenuItemCreate(
            name="Free Item",
            price=Decimal("0.00"),
            category_id=cat_id,
        )
