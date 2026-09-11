"""Menu Item Database Model."""

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.menu_category import MenuCategory


class MenuItem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Dish or product offered on a menu."""

    __tablename__ = "menu_items"

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("menu_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Monetary amounts MUST use Numeric/Decimal to avoid floating-point rounding errors
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)

    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    preparation_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    category: Mapped["MenuCategory"] = relationship("MenuCategory", back_populates="items")

    def __repr__(self) -> str:
        return f"<MenuItem id={self.id} name={self.name} price={self.price} {self.currency}>"
