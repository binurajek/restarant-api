"""Common Pydantic Schemas."""

from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with orm_mode / from_attributes enabled."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str = "ok"


class DatabaseHealthResponse(BaseModel):
    """Database connectivity health check response schema."""

    status: str
    database: str
    latency_ms: float


class MessageResponse(BaseModel):
    """Generic message response schema."""

    message: str
    details: dict[str, Any] | None = None


class PaginationParams(BaseModel):
    """Query parameters for pagination."""

    page: int = Field(default=1, ge=1, description="Page number starting at 1")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginatedResponse[T](BaseSchema):
    """Standard paginated container."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int
