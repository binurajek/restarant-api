"""User Pydantic Schemas."""

import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from app.core.constants import UserRole, UserStatus
from app.schemas.common import BaseSchema


class UserBase(BaseSchema):
    """Base user properties."""

    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=128)
    phone: str | None = Field(default=None, max_length=32)
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=128, description="Plaintext password")


class UserUpdate(BaseSchema):
    """Schema for updating user profile."""

    full_name: str | None = Field(default=None, min_length=2, max_length=128)
    phone: str | None = Field(default=None, max_length=32)
    is_active: bool | None = None


class UserResponse(UserBase):
    """Schema for public user profile return."""

    id: uuid.UUID
    status: UserStatus
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseSchema):
    """Credentials for authentication."""

    email: EmailStr
    password: str


class TokenResponse(BaseSchema):
    """JWT tokens return schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
