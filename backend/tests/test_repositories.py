import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import ProjectRepository
from app.repositories.scene import SceneRepository


@pytest.mark.asyncio
async def test_project_repository_crud(db_session: AsyncSession):
    repo = ProjectRepository(db_session)

    # Create
    project = await repo.create(
        title="My Video", script_text="Hello world", template="social_reel"
    )
    assert project.title == "My Video"
    assert project.status == "draft"

    # Read
    fetched = await repo.get_by_id(project.id)
    assert fetched is not None
    assert fetched.id == project.id

    # Update
    updated = await repo.update(fetched, title="Updated Video")
    assert updated.title == "Updated Video"

    # List
    projects = await repo.list_all()
    assert len(projects) == 1

    # Delete
    deleted = await repo.delete(project.id)
    assert deleted is True
    assert await repo.get_by_id(project.id) is None


@pytest.mark.asyncio
async def test_scene_repository_crud(db_session: AsyncSession):
    project_repo = ProjectRepository(db_session)
    scene_repo = SceneRepository(db_session)

    project = await project_repo.create(title="Test", script_text="Test script")

    # Create
    scene = await scene_repo.create(
        project_id=project.id,
        scene_number=1,
        narration_text="Narration 1",
        visual_prompt="A sunny day",
        duration_seconds=5.0,
    )
    assert scene.narration_text == "Narration 1"

    # List by project
    scenes = await scene_repo.list_by_project(project.id)
    assert len(scenes) == 1
    assert scenes[0].scene_number == 1

    # Update
    updated = await scene_repo.update(scene, duration_seconds=10.0)
    assert updated.duration_seconds == 10.0

    # Delete
    deleted = await scene_repo.delete(scene.id)
    assert deleted is True
    assert await scene_repo.get_by_id(scene.id) is None


@pytest.mark.asyncio
async def test_project_delete_cascades_scenes(db_session: AsyncSession):
    project_repo = ProjectRepository(db_session)
    scene_repo = SceneRepository(db_session)

    project = await project_repo.create(title="Cascade Test", script_text="Test")
    await scene_repo.create(
        project_id=project.id, scene_number=1, narration_text="Scene 1"
    )
    await scene_repo.create(
        project_id=project.id, scene_number=2, narration_text="Scene 2"
    )

    scenes_before = await scene_repo.list_by_project(project.id)
    assert len(scenes_before) == 2

    await scene_repo.delete_by_project(project.id)
    await project_repo.delete(project.id)

    scenes_after = await scene_repo.list_by_project(project.id)
    assert len(scenes_after) == 0
