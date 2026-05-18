from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.storyboard import Storyboard


class StoryboardRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        scene_id: str,
        frame_number: int,
        image_url: str,
        prompt_used: str | None = None,
    ) -> Storyboard:
        sb = Storyboard(
            scene_id=scene_id,
            frame_number=frame_number,
            image_url=image_url,
            prompt_used=prompt_used,
        )
        self._session.add(sb)
        await self._session.commit()
        await self._session.refresh(sb)
        return sb

    async def get_by_id(self, sb_id: str) -> Storyboard | None:
        result = await self._session.execute(
            select(Storyboard).where(Storyboard.id == sb_id)
        )
        return result.scalar_one_or_none()

    async def list_by_scene(self, scene_id: str) -> list[Storyboard]:
        result = await self._session.execute(
            select(Storyboard)
            .where(Storyboard.scene_id == scene_id)
            .order_by(Storyboard.frame_number)
        )
        return list(result.scalars().all())

    async def select_storyboard(self, sb_id: str) -> Storyboard | None:
        sb = await self.get_by_id(sb_id)
        if sb:
            sb.selected = True
            await self._session.commit()
            await self._session.refresh(sb)
        return sb

    async def delete(self, sb_id: str) -> bool:
        result = await self._session.execute(
            delete(Storyboard).where(Storyboard.id == sb_id)
        )
        await self._session.commit()
        return bool(result.rowcount > 0)  # type: ignore[attr-defined]
