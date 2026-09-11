"""Menu Category Database Model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.menu import Menu
    from app.models.menu_item import MenuItem


class MenuCategory(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Category grouping items within a menu (e.g. Appetizers, Mains, Drinks)."""

    __tablename__ = "menu_categories"

    menu_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("menus.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    menu: Mapped["Menu"] = relationship("Menu", back_populates="categories")
    items: Mapped[list["MenuItem"]] = relationship(
        "MenuItem",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<MenuCategory id={self.id} name={self.name} order={self.display_order}>"
