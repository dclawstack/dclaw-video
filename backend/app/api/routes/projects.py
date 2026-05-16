from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.project import ProjectRepository
from app.repositories.scene import SceneRepository
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut

router = APIRouter(tags=["projects"])


@router.post("/projects", response_model=ProjectOut, status_code=201)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)) -> dict:
    repo = ProjectRepository(db)
    scene_repo = SceneRepository(db)
    project = await repo.create(
        title=data.title,
        script_text=data.script_text,
        template=data.template,
    )

    paragraphs = [p.strip() for p in data.script_text.split("\n\n") if p.strip()]
    for idx, paragraph in enumerate(paragraphs, start=1):
        await scene_repo.create(
            project_id=project.id,
            scene_number=idx,
            narration_text=paragraph,
            visual_prompt="",
            duration_seconds=5.0,
        )

    result = await repo.get_by_id(project.id)
    return result


@router.get("/projects", response_model=list[ProjectOut])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list:
    repo = ProjectRepository(db)
    return await repo.list_all()


@router.get("/projects/{project_id}", response_model=ProjectOut)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    repo = ProjectRepository(db)
    project = await repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/projects/{project_id}", response_model=ProjectOut)
async def update_project(project_id: str, data: ProjectUpdate, db: AsyncSession = Depends(get_db)) -> dict:
    repo = ProjectRepository(db)
    project = await repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    updates = data.model_dump(exclude_unset=True)
    updated = await repo.update(project, **updates)
    return updated


@router.delete("/projects/{project_id}", status_code=204)
async def delete_project(project_id: str, db: AsyncSession = Depends(get_db)) -> None:
    repo = ProjectRepository(db)
    project = await repo.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    scene_repo = SceneRepository(db)
    await scene_repo.delete_by_project(project_id)
    await repo.delete(project_id)
    return None
