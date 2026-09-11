"""Maps and Geolocation Integration Interface."""

from abc import ABC, abstractmethod


class MapsServiceInterface(ABC):
    """Contract for geolocation, geocoding, and distance calculations."""

    @abstractmethod
    async def geocode_address(self, address: str) -> tuple[float, float]:
        """Convert address text to (latitude, longitude)."""
        pass

    @abstractmethod
    async def calculate_distance(
        self, origin: tuple[float, float], destination: tuple[float, float]
    ) -> float:
        """Calculate distance in meters between two coordinate points."""
        pass
