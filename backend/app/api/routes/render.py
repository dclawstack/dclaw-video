from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.core.db import get_db
from app.models.project import Project
from app.models.render_job import RenderJob
from app.schemas.render_job import RenderJobOut

router = APIRouter(tags=["render"])


@router.post("/projects/{project_id}/render", status_code=202)
async def queue_render(
    project_id: UUID, db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    result = await db.execute(select(Project).where(Project.id == str(project_id)))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    task = celery_app.send_task("tasks.render_project", args=[str(project_id)])

    job = RenderJob(
        project_id=str(project_id),
        celery_task_id=task.id,
        status="pending",
    )
    db.add(job)
    await db.commit()

    return {"job_id": task.id}


@router.get("/projects/{project_id}/render-status", response_model=RenderJobOut)
async def get_status(
    project_id: UUID, db: AsyncSession = Depends(get_db)
) -> RenderJobOut:
    result = await db.execute(
        select(RenderJob)
        .where(RenderJob.project_id == str(project_id))
        .order_by(RenderJob.created_at.desc())
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="No render job found")
    return job  # type: ignore[return-value]
