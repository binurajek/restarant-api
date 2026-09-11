"""Authentication API Router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.database.dependencies import get_db
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account",
)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Register a new customer, staff, or manager user."""
    service = UserService(db)
    user = await service.register(user_in)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and obtain JWT tokens",
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Validate credentials and return access and refresh JWT tokens."""
    service = UserService(db)
    user = await service.authenticate(credentials.email, credentials.password)

    claims = {"role": user.role, "email": user.email}
    access_token = create_access_token(user.id, additional_claims=claims)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
