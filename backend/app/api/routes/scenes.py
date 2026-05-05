from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.celery_app import celery_app
from app.models.scene import Scene
from app.schemas.scene import SceneUpdate, SceneOut

router = APIRouter(tags=["scenes"])


@router.get("/projects/{project_id}/scenes", response_model=list[SceneOut])
async def list_scenes(project_id: UUID, db: AsyncSession = Depends(get_db)) -> list[Scene]:
    result = await db.execute(
        select(Scene).where(Scene.project_id == project_id).order_by(Scene.scene_number)
    )
    return list(result.scalars().all())


@router.put("/scenes/{scene_id}", response_model=SceneOut)
async def update_scene(scene_id: UUID, data: SceneUpdate, db: AsyncSession = Depends(get_db)) -> Scene:
    result = await db.execute(select(Scene).where(Scene.id == scene_id))
    scene = result.scalar_one_or_none()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(scene, field, value)

    await db.commit()
    await db.refresh(scene)
    return scene


@router.post("/scenes/{scene_id}/regenerate", status_code=202)
async def regenerate_scene(scene_id: UUID, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    result = await db.execute(select(Scene).where(Scene.id == scene_id))
    scene = result.scalar_one_or_none()
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    task = celery_app.send_task("tasks.render_scene", args=[str(scene_id)])
    return {"job_id": task.id}
