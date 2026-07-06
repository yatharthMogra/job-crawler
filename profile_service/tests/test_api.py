import pytest
from httpx import ASGITransport, AsyncClient

from app.config import get_settings
from app.main import app


@pytest.fixture
def api_headers() -> dict[str, str]:
    settings = get_settings()
    return {"X-API-Key": settings.api_key}


@pytest.mark.asyncio
async def test_health_no_auth() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_requires_api_key() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/auth/signup/request",
            json={"email": "x@y.com", "name": "X", "password": "password123"},
        )
    assert response.status_code == 401
