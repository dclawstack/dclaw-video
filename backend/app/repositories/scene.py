from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scene import Scene


class SceneRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        project_id: str,
        scene_number: int,
        narration_text: str = "",
        visual_prompt: str = "",
        duration_seconds: float = 5.0,
    ) -> Scene:
        scene = Scene(
            project_id=project_id,
            scene_number=scene_number,
            narration_text=narration_text,
            visual_prompt=visual_prompt,
            duration_seconds=duration_seconds,
        )
        self._session.add(scene)
        await self._session.commit()
        await self._session.refresh(scene)
        return scene

    async def get_by_id(self, scene_id: str) -> Scene | None:
        result = await self._session.execute(
            select(Scene).where(Scene.id == scene_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: str) -> list[Scene]:
        result = await self._session.execute(
            select(Scene)
            .where(Scene.project_id == project_id)
            .order_by(Scene.scene_number)
        )
        return list(result.scalars().all())

    async def update(self, scene: Scene, **kwargs: object) -> Scene:
        for key, value in kwargs.items():
            if hasattr(scene, key):
                setattr(scene, key, value)
        await self._session.commit()
        await self._session.refresh(scene)
        return scene

    async def delete(self, scene_id: str) -> bool:
        result = await self._session.execute(
            delete(Scene).where(Scene.id == scene_id)
        )
        await self._session.commit()
        return bool(result.rowcount > 0)  # type: ignore[attr-defined]

    async def delete_by_project(self, project_id: str) -> bool:
        result = await self._session.execute(
            delete(Scene).where(Scene.project_id == project_id)
        )
        await self._session.commit()
        return bool(result.rowcount > 0)  # type: ignore[attr-defined]
