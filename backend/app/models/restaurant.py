"""Restaurant Database Model."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import RestaurantStatus
from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.branch import RestaurantBranch
    from app.models.menu import Menu
    from app.models.user import User


class Restaurant(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Restaurant enterprise entity."""

    __tablename__ = "restaurants"

    name: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    status: Mapped[RestaurantStatus] = mapped_column(
        SQLEnum(
            RestaurantStatus,
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj],
            length=32,
        ),
        default=RestaurantStatus.ACTIVE,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    owner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    owner: Mapped["User | None"] = relationship("User", back_populates="owned_restaurants")
    branches: Mapped[list["RestaurantBranch"]] = relationship(
        "RestaurantBranch",
        back_populates="restaurant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    menus: Mapped[list["Menu"]] = relationship(
        "Menu",
        back_populates="restaurant",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Restaurant id={self.id} name={self.name} slug={self.slug}>"
