"""FastAPI Application Entrypoint and Lifecycle Configuration."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
            "Centralized REST API for Restaurant Discovery, Menus, QR Ordering, "
            "Table Reservations, and Multi-tenant Restaurant Management."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

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

    # 5. Root route redirecting to /docs
    @app.get("/", include_in_schema=False)
    async def root_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    return app


app = create_application()
