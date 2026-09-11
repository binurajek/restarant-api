"""Health Check Endpoints."""

import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dependencies import get_db
from app.schemas.common import DatabaseHealthResponse, HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse, summary="Service liveness probe")
async def health_check() -> HealthResponse:
    """Basic health probe confirming API service availability."""
    return HealthResponse(status="ok")


@router.get(
    "/database", response_model=DatabaseHealthResponse, summary="Database connectivity check"
)
async def database_health_check(db: AsyncSession = Depends(get_db)) -> DatabaseHealthResponse:
    """Verifies PostgreSQL / Neon connectivity without exposing internal credentials."""
    start_time = time.perf_counter()
    try:
        # Perform simple lightweight query
        result = await db.execute(text("SELECT 1"))
        _ = result.scalar()
        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return DatabaseHealthResponse(
            status="ok",
            database="connected",
            latency_ms=latency_ms,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connectivity check failed.",
        ) from exc
