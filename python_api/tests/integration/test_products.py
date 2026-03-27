import pytest
from httpx import AsyncClient


async def _get_token(client: AsyncClient, email: str, password: str = "secret123") -> str:
    await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    res = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return res.json()["access_token"]


PRODUCT_PAYLOAD = {
    "name": "Test Sneaker",
    "description": "Great shoe",
    "price": 99.99,
    "stock": 50,
    "category": "footwear",
}


@pytest.mark.asyncio
async def test_list_products_public(client: AsyncClient):
    response = await client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_create_product_requires_admin(client: AsyncClient):
    token = await _get_token(client, "regular@example.com")
    response = await client.post(
        "/api/v1/products",
        json=PRODUCT_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/api/v1/products/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_products_by_name(client: AsyncClient):
    response = await client.get("/api/v1/products?q=sneaker")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_products_by_category(client: AsyncClient):
    response = await client.get("/api/v1/products?category=footwear")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_products_price_range(client: AsyncClient):
    response = await client.get("/api/v1/products?min_price=10&max_price=200")
    assert response.status_code == 200
