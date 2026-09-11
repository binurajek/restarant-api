"""Menu Database Model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import MenuStatus
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.menu_category import MenuCategory
    from app.models.restaurant import Restaurant


class Menu(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Digital restaurant menu."""

    __tablename__ = "menus"

    restaurant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[MenuStatus] = mapped_column(
        SQLEnum(MenuStatus, native_enum=False, values_callable=lambda obj: [e.value for e in obj], length=32),
        default=MenuStatus.ACTIVE,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    restaurant: Mapped["Restaurant"] = relationship("Restaurant", back_populates="menus")
    categories: Mapped[list["MenuCategory"]] = relationship(
        "MenuCategory",
        back_populates="menu",
        cascade="all, delete-orphan",
        order_by="MenuCategory.display_order",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Menu id={self.id} name={self.name} status={self.status}>"
