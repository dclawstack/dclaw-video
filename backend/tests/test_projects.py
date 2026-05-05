import pytest
from httpx import AsyncClient
from app.api.main import app


@pytest.mark.asyncio
async def test_create_project():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/projects", json={
            "title": "Test Project",
            "script_text": "Scene one.\n\nScene two.",
            "template": "youtube_explainer",
        })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Project"
    assert data["status"] == "draft"
