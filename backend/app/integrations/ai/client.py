"""AI and OCR Integration Interface."""

from abc import ABC, abstractmethod
from typing import Any


class AIServiceInterface(ABC):
    """Contract for AI menu digitization and OCR parsing."""

    @abstractmethod
    async def extract_menu_from_image(self, image_bytes: bytes) -> dict[str, Any]:
        """Extract structured menu items and categories from photo/PDF."""
        pass

    @abstractmethod
    async def generate_recommendations(
        self, user_id: str, context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Generate personalized food recommendations based on profile and history."""
        pass
