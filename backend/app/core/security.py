"""Security Utilities: Argon2id Hashing and JWT Token Management."""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

from app.core.config import settings

# Initialize Argon2id password hasher with secure defaults
_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,  # 64 MB
    parallelism=4,
    hash_len=32,
    salt_len=16,
)


def hash_password(password: str) -> str:
    """Hash plaintext password using Argon2id."""
    return _hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plaintext password against an Argon2id hash."""
    try:
        return _hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError):
        return False


def create_jwt_token(
    subject: str | Any,
    expires_delta: timedelta,
    token_type: str = "access",
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Generate signed JWT token."""
    now = datetime.now(UTC)
    expire = now + expires_delta

    payload: dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,
        "type": token_type,
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(
    subject: str | Any,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create short-lived JWT access token."""
    expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_jwt_token(
        subject=subject,
        expires_delta=expires_delta,
        token_type="access",
        additional_claims=additional_claims,
    )


def create_refresh_token(
    subject: str | Any,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """Create long-lived JWT refresh token."""
    expires_delta = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    return create_jwt_token(
        subject=subject,
        expires_delta=expires_delta,
        token_type="refresh",
        additional_claims=additional_claims,
    )


def decode_jwt_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT token."""
    return jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )
