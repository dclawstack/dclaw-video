from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.project import Project
from app.models.scene import Scene
from app.schemas.project import ProjectCreate, ProjectOut

router = APIRouter(tags=["projects"])


@router.post("/projects", response_model=ProjectOut, status_code=201)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)) -> Project:
    project = Project(
        title=data.title,
        script_text=data.script_text,
        template=data.template,
        voice_profile_id=data.voice_profile_id,
        character_id=data.character_id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)

    # Auto-detect scenes from paragraph breaks
    paragraphs = [p.strip() for p in data.script_text.split("\n\n") if p.strip()]
    for idx, paragraph in enumerate(paragraphs, start=1):
        scene = Scene(
            project_id=project.id,
            scene_number=idx,
            narration_text=paragraph,
            visual_prompt="",
            duration_seconds=5.0,
        )
        db.add(scene)
    await db.commit()
    return project


@router.get("/projects", response_model=list[ProjectOut])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list[Project]:
    result = await db.execute(select(Project).order_by(Project.created_at.desc()))
    return list(result.scalars().all())


@router.get("/projects/{project_id}", response_model=ProjectOut)
async def get_project(project_id: UUID, db: AsyncSession = Depends(get_db)) -> Project:
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
