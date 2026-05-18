from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.core.db import get_db
from app.models.project import Project
from app.models.scene import Scene
from app.schemas.scene import SceneOut

router = APIRouter(tags=["storyboard"])


@router.post("/projects/{project_id}/storyboard", status_code=202)
async def generate_storyboard(
    project_id: UUID, db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    result = await db.execute(select(Project).where(Project.id == str(project_id)))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    task = celery_app.send_task("tasks.generate_storyboard", args=[str(project_id)])
    return {"job_id": task.id}


@router.get("/projects/{project_id}/storyboard", response_model=list[SceneOut])
async def list_storyboard_scenes(
    project_id: UUID, db: AsyncSession = Depends(get_db)
) -> list[Scene]:
    result = await db.execute(
        select(Scene)
        .where(Scene.project_id == str(project_id))
        .order_by(Scene.scene_number)
    )
    return list(result.scalars().all())
