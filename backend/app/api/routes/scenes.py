from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.scene import SceneRepository
from app.schemas.scene import SceneUpdate, SceneOut

router = APIRouter(tags=["scenes"])


@router.get("/projects/{project_id}/scenes", response_model=list[SceneOut])
async def list_scenes(project_id: str, db: AsyncSession = Depends(get_db)) -> list:
    repo = SceneRepository(db)
    return await repo.list_by_project(project_id)


@router.get("/scenes/{scene_id}", response_model=SceneOut)
async def get_scene(scene_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    repo = SceneRepository(db)
    scene = await repo.get_by_id(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")
    return scene


@router.put("/scenes/{scene_id}", response_model=SceneOut)
async def update_scene(scene_id: str, data: SceneUpdate, db: AsyncSession = Depends(get_db)) -> dict:
    repo = SceneRepository(db)
    scene = await repo.get_by_id(scene_id)
    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    updates = data.model_dump(exclude_unset=True)
    updated = await repo.update(scene, **updates)
    return updated


@router.delete("/scenes/{scene_id}", status_code=204)
async def delete_scene(scene_id: str, db: AsyncSession = Depends(get_db)) -> None:
    repo = SceneRepository(db)
    deleted = await repo.delete(scene_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scene not found")
    return None
