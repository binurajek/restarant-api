"""API tests for Restaurant endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_restaurant_lifecycle(client: AsyncClient) -> None:
    """Test creating, listing, and retrieving a restaurant via REST API."""
    payload = {
        "name": "Bistro Parisien",
        "slug": "bistro-parisien",
        "description": "French contemporary dining",
        "branches": [
            {
                "name": "Downtown Branch",
                "address_line": "123 Main Street",
                "city": "Metropolis",
                "country_code": "US",
            }
        ],
    }

    # 1. Create
    create_res = await client.post("/api/v1/restaurants", json=payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["name"] == "Bistro Parisien"
    assert created_data["slug"] == "bistro-parisien"
    assert len(created_data["branches"]) == 1
    restaurant_id = created_data["id"]

    # 2. List
    list_res = await client.get("/api/v1/restaurants")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] >= 1
    assert any(r["id"] == restaurant_id for r in list_data["items"])

    # 3. Get by ID
    get_res = await client.get(f"/api/v1/restaurants/{restaurant_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Bistro Parisien"

    # 4. Get by Slug
    slug_res = await client.get("/api/v1/restaurants/by-slug/bistro-parisien")
    assert slug_res.status_code == 200
    assert slug_res.json()["id"] == restaurant_id
