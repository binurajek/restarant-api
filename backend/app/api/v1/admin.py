"""Platform Administration API Router (Architecture Foundation)."""

from fastapi import APIRouter

from app.schemas.common import MessageResponse

router = APIRouter(prefix="/admin", tags=["Platform Admin"])


@router.get("/metrics", response_model=MessageResponse, summary="Platform metrics (stub)")
async def get_metrics() -> MessageResponse:
    """Placeholder for platform-wide analytics, tenant onboarding, and system metrics."""
    return MessageResponse(
        message="Admin service foundation ready. Business logic to be implemented in phase 2.",
        details={"status": "foundation_ready"},
    )
