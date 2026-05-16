import pytest
from httpx import AsyncClient, ASGITransport

from app.api.main import app


@pytest.mark.asyncio
async def test_create_project(db_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/projects",
            json={"title": "Test Video", "script_text": "Hello world"},
        )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Video"
    assert data["status"] == "draft"
