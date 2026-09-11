"""Unit tests for configuration loading and validation."""

from app.core.config import Settings


def test_default_settings() -> None:
    """Validate default settings parameters."""
    settings = Settings()
    assert settings.APP_NAME == "restaurant-platform"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DATABASE_POOL_SIZE == 10
    assert "postgresql+asyncpg://" in settings.SQLALCHEMY_DATABASE_URI


def test_cors_parsing() -> None:
    """Validate CORS origins parsing from string or list."""
    settings = Settings(CORS_ORIGINS=["http://example.com"])
    assert "http://example.com" in settings.CORS_ORIGINS
