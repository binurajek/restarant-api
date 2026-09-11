"""Payment Gateway Integration Interface."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class PaymentGatewayInterface(ABC):
    """Contract for payment processing providers (e.g. Stripe)."""

    @abstractmethod
    async def create_payment_intent(
        self, amount: Decimal, currency: str, customer_id: str, metadata: dict[str, Any]
    ) -> dict[str, Any]:
        """Create a payment intent for checkout."""
        pass

    @abstractmethod
    async def refund_payment(
        self, payment_intent_id: str, amount: Decimal | None = None
    ) -> dict[str, Any]:
        """Process a refund for a previously captured payment."""
        pass
