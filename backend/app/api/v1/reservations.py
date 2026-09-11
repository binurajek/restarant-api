"""Table Reservations API Router (Architecture Foundation)."""

from fastapi import APIRouter

from app.schemas.common import MessageResponse

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("", response_model=MessageResponse, summary="List reservations (stub)")
async def list_reservations() -> MessageResponse:
    """Placeholder for table availability, booking, and guest reservations."""
    return MessageResponse(
        message="Reservations service foundation ready. Business logic to be implemented in phase 2.",
        details={"status": "foundation_ready"},
    )
