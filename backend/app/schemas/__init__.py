"""Pydantic Schemas Package."""

from app.schemas.common import (
    BaseSchema,
    DatabaseHealthResponse,
    HealthResponse,
    MessageResponse,
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.menu import (
    MenuBase,
    MenuCategoryBase,
    MenuCategoryCreate,
    MenuCategoryResponse,
    MenuCreate,
    MenuResponse,
    MenuUpdate,
)
from app.schemas.menu_item import (
    MenuItemBase,
    MenuItemCreate,
    MenuItemResponse,
    MenuItemUpdate,
)
from app.schemas.restaurant import (
    RestaurantBase,
    RestaurantBranchBase,
    RestaurantBranchCreate,
    RestaurantBranchResponse,
    RestaurantCreate,
    RestaurantResponse,
    RestaurantUpdate,
)
from app.schemas.user import (
    TokenResponse,
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)

__all__ = [
    "BaseSchema",
    "HealthResponse",
    "DatabaseHealthResponse",
    "MessageResponse",
    "PaginationParams",
    "PaginatedResponse",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "TokenResponse",
    "RestaurantBase",
    "RestaurantCreate",
    "RestaurantUpdate",
    "RestaurantResponse",
    "RestaurantBranchBase",
    "RestaurantBranchCreate",
    "RestaurantBranchResponse",
    "MenuBase",
    "MenuCreate",
    "MenuUpdate",
    "MenuResponse",
    "MenuCategoryBase",
    "MenuCategoryCreate",
    "MenuCategoryResponse",
    "MenuItemBase",
    "MenuItemCreate",
    "MenuItemUpdate",
    "MenuItemResponse",
]
