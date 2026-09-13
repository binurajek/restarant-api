"""FastAPI Application Entrypoint and Lifecycle Configuration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.database.session import async_engine
from app.middleware import (
    RequestIDMiddleware,
    StructuredLoggingMiddleware,
    register_error_handlers,
)

# Initialize logging
setup_logging(debug=settings.DEBUG)
logger = get_logger("app.main")

# OpenAPI Tags Metadata for Swagger UI Organization
OPENAPI_TAGS: list[dict[str, Any]] = [
    {
        "name": "Health",
        "description": "Liveness probes, database connectivity checks, and latency metrics.",
    },
    {
        "name": "Authentication",
        "description": "User account registration and JWT credential exchange (Access & Refresh tokens).",
    },
    {
        "name": "Users",
        "description": "User profile retrieval and personal account detail management.",
    },
    {
        "name": "Restaurants",
        "description": "Multi-tenant restaurant entity lifecycle and physical branch geographic management.",
    },
    {
        "name": "Menus",
        "description": "Digital restaurant menu catalogs and nested category structures.",
    },
    {
        "name": "Menu Items",
        "description": "Individual dish items, monetary pricing, nutritional facts, and availability (86-toggle).",
    },
    {
        "name": "Orders",
        "description": "Customer order placement, kitchen tracking, and status lifecycle (Phase 2).",
    },
    {
        "name": "Reservations",
        "description": "Table bookings, party size coordination, and dining reservations (Phase 2).",
    },
    {
        "name": "Platform Admin",
        "description": "Administrative metrics, system overview, and tenant onboarding (Phase 2).",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Application lifespan manager for graceful resource startup and teardown."""
    logger.info("Starting up %s (env: %s)", settings.APP_NAME, settings.APP_ENV.value)
    yield
    logger.info("Shutting down %s: Disposing database connection pool...", settings.APP_NAME)
    await async_engine.dispose()
    logger.info("Shutdown complete.")


def create_application() -> FastAPI:
    """Application factory configuring routes, middleware, and documentation."""
    app = FastAPI(
        title="Restaurant Platform API",
        description=(
            "### Production-Grade Restaurant Discovery & Management API\n\n"
            "This API powers the restaurant ecosystem, including customer discovery, "
            "digital QR dining, table reservations, and restaurant branch management.\n\n"
            "#### Authentication\n"
            "Secured endpoints require a valid JWT Access Token. Click **Authorize 🔓** "
            "above and input your token obtained from `/api/v1/auth/login`."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=OPENAPI_TAGS,
        swagger_ui_parameters={
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
            "docExpansion": "list",
            "syntaxHighlight.theme": "monokai",
        },
        lifespan=lifespan,
    )

    # Custom OpenAPI Generator with JWT Bearer Security Scheme for Swagger UI
    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
            tags=OPENAPI_TAGS,
        )
        # Configure components and BearerAuth security scheme
        components = openapi_schema.setdefault("components", {})
        components["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": (
                    "Enter your JWT Access Token (without 'Bearer ' prefix). "
                    "Example: eyJhbGciOiJIUzI1NiIs..."
                ),
            }
        }
        # Add BearerAuth to global security so Swagger displays the Authorize button
        openapi_schema["security"] = [{"BearerAuth": []}]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]

    # 1. Custom and Starlette Middlewares (Order: outermost executed first)
    app.add_middleware(StructuredLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # 2. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 3. Global Exception Handling
    register_error_handlers(app)

    # 4. Mount API Routers
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)

    # 5. Root routes redirecting to /docs (Swagger UI)
    @app.get("/", include_in_schema=False)
    @app.get("/swagger", include_in_schema=False)
    async def root_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    return app


app = create_application()

