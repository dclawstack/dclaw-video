from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.character import Character


class CharacterRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        project_id: str,
        name: str,
        reference_image_url: str,
        face_embedding: str | None = None,
    ) -> Character:
        character = Character(
            project_id=project_id,
            name=name,
            reference_image_url=reference_image_url,
            face_embedding=face_embedding,
        )
        self._session.add(character)
        await self._session.commit()
        await self._session.refresh(character)
        return character

    async def get_by_id(self, character_id: str) -> Character | None:
        result = await self._session.execute(
            select(Character).where(Character.id == character_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: str) -> list[Character]:
        result = await self._session.execute(
            select(Character).where(Character.project_id == project_id)
        )
        return list(result.scalars().all())

    async def update(self, character: Character, **kwargs: object) -> Character:
        for key, value in kwargs.items():
            if hasattr(character, key):
                setattr(character, key, value)
        await self._session.commit()
        await self._session.refresh(character)
        return character

    async def delete(self, character_id: str) -> bool:
        result = await self._session.execute(
            delete(Character).where(Character.id == character_id)
        )
        await self._session.commit()
        return bool(result.rowcount > 0)  # type: ignore[attr-defined]
