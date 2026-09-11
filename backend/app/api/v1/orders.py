"""Orders API Router (Architecture Foundation)."""

from fastapi import APIRouter

from app.schemas.common import MessageResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=MessageResponse, summary="List orders (stub)")
async def list_orders() -> MessageResponse:
    """Placeholder for order placement, tracking, and kitchen display endpoints."""
    return MessageResponse(
        message="Orders service foundation ready. Business logic to be implemented in phase 2.",
        details={"status": "foundation_ready"},
    )
