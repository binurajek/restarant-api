"""Notification Services Integration Interface."""

from abc import ABC, abstractmethod
from typing import Any


class NotificationServiceInterface(ABC):
    """Contract for Email, SMS, and Push Notifications."""

    @abstractmethod
    async def send_email(self, to_email: str, subject: str, body_html: str) -> bool:
        """Dispatch transactional email."""
        pass

    @abstractmethod
    async def send_push(
        self, device_token: str, title: str, message: str, data: dict[str, Any] | None = None
    ) -> bool:
        """Dispatch push notification via FCM / APNs."""
        pass
