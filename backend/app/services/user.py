"""User Business Logic Service."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service encapsulating user registration, authentication, and management."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def register(self, user_in: UserCreate) -> User:
        """Register a new user account after validating email uniqueness."""
        existing = await self.repository.get_by_email(user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        user = User(
            email=user_in.email.lower(),
            hashed_password=hash_password(user_in.password),
            full_name=user_in.full_name,
            phone=user_in.phone,
            role=user_in.role,
        )
        return await self.repository.create(user)

    async def authenticate(self, email: str, password: str) -> User:
        """Authenticate user credentials."""
        user = await self.repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        """Fetch user by ID or raise 404."""
        user = await self.repository.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    async def update(self, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        """Update user profile."""
        user = await self.get_by_id(user_id)
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        return await self.repository.update(user)
