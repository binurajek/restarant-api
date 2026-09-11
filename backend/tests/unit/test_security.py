"""Unit tests for Argon2id hashing and JWT tokens."""

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    hash_password,
    verify_password,
)


def test_argon2id_password_hashing() -> None:
    """Test Argon2id password hashing and verification."""
    raw_password = "SecurePassword#2026!"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert hashed.startswith("$argon2id$")
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_access_token_lifecycle() -> None:
    """Test JWT access token creation, claims, and decoding."""
    subject_id = "11111111-2222-3333-4444-555555555555"
    token = create_access_token(
        subject=subject_id,
        additional_claims={"role": "admin", "email": "admin@example.com"},
    )

    payload = decode_jwt_token(token)
    assert payload["sub"] == subject_id
    assert payload["role"] == "admin"
    assert payload["email"] == "admin@example.com"
    assert payload["type"] == "access"


def test_jwt_refresh_token_lifecycle() -> None:
    """Test JWT refresh token creation and claims."""
    subject_id = "11111111-2222-3333-4444-555555555555"
    token = create_refresh_token(subject=subject_id)

    payload = decode_jwt_token(token)
    assert payload["sub"] == subject_id
    assert payload["type"] == "refresh"
