from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.voice_profile import VoiceProfile


class VoiceProfileRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        name: str,
        kokoro_voice_id: str,
        speed: float = 1.0,
        language: str = "en",
    ) -> VoiceProfile:
        vp = VoiceProfile(
            name=name,
            kokoro_voice_id=kokoro_voice_id,
            speed=speed,
            language=language,
        )
        self._session.add(vp)
        await self._session.commit()
        await self._session.refresh(vp)
        return vp

    async def get_by_id(self, vp_id: str) -> VoiceProfile | None:
        result = await self._session.execute(select(VoiceProfile).where(VoiceProfile.id == vp_id))
        return result.scalar_one_or_none()

    async def list_all(self, limit: int = 50, offset: int = 0):
        result = await self._session.execute(
            select(VoiceProfile).order_by(VoiceProfile.created_at.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def update(self, vp: VoiceProfile, **kwargs) -> VoiceProfile:
        for key, value in kwargs.items():
            if hasattr(vp, key):
                setattr(vp, key, value)
        await self._session.commit()
        await self._session.refresh(vp)
        return vp

    async def delete(self, vp_id: str) -> bool:
        result = await self._session.execute(delete(VoiceProfile).where(VoiceProfile.id == vp_id))
        await self._session.commit()
        return result.rowcount > 0
