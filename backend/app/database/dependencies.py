"""FastAPI Database Dependencies."""

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Dependency for injecting an async database session into API endpoints."""
    async for session in get_session():
        yield session


# Type alias for cleaner router signatures
DatabaseSession = Depends(get_db)
