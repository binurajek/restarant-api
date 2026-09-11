"""Application Configuration Settings via Pydantic Settings v2."""

import json
from typing import Annotated, Any

from pydantic import BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import Environment


def parse_cors_origins(v: Any) -> list[str]:
    """Parse CORS origins whether supplied as JSON string or comma-separated list."""
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, str) and v.startswith("["):
        return json.loads(v)
    elif isinstance(v, list):
        return v
    return ["*"]


class Settings(BaseSettings):
    """Centralized application settings loaded from environment or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --------------------------------------------------------------------------
    # Base Application
    # --------------------------------------------------------------------------
    APP_NAME: str = "restaurant-platform"
    APP_ENV: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "insecure_dev_secret_key_at_least_32_chars_long_12345"

    CORS_ORIGINS: Annotated[list[str], BeforeValidator(parse_cors_origins)] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # --------------------------------------------------------------------------
    # PostgreSQL / Neon Database
    # --------------------------------------------------------------------------
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "restaurant_db"
    DATABASE_URL: str | None = None
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Computed asynchronous PostgreSQL connection URI."""
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            # Normalize schemes for asyncpg
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url

        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # --------------------------------------------------------------------------
    # Redis Cache & Broker
    # --------------------------------------------------------------------------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"

    # --------------------------------------------------------------------------
    # Authentication & JWT Security
    # --------------------------------------------------------------------------
    JWT_SECRET: str = "change_me_to_a_secure_jwt_secret_minimum_32_characters"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # OAuth2 (Optional in development)
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    APPLE_CLIENT_ID: str | None = None
    APPLE_TEAM_ID: str | None = None
    APPLE_KEY_ID: str | None = None
    APPLE_PRIVATE_KEY: str | None = None

    # --------------------------------------------------------------------------
    # Third-Party Integrations (Optional in initial foundation)
    # --------------------------------------------------------------------------
    OPENAI_API_KEY: str | None = None
    STRIPE_SECRET_KEY: str | None = None
    STRIPE_PUBLISHABLE_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None
    AZURE_STORAGE_CONNECTION_STRING: str | None = None
    AZURE_STORAGE_CONTAINER_NAME: str = "restaurant-media"
    GOOGLE_MAPS_API_KEY: str | None = None
    SMTP_HOST: str | None = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str = "noreply@restaurantplatform.com"
    FCM_SERVER_KEY: str | None = None


# Cached settings singleton
settings = Settings()
