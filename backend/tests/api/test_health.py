"""API tests for Health Endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient) -> None:
    """Test GET /api/v1/health returns status ok."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "ok"}
    assert "X-Request-ID" in response.headers


@pytest.mark.asyncio
async def test_database_health_endpoint(client: AsyncClient) -> None:
    """Test GET /api/v1/health/database validates database connection."""
    response = await client.get("/api/v1/health/database")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    assert "latency_ms" in data
    assert isinstance(data["latency_ms"], float)
