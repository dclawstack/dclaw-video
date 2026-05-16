from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.models.project import Project


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, title: str, script_text: str, template: str = "youtube_explainer") -> Project:
        project = Project(title=title, script_text=script_text, template=template)
        self._session.add(project)
        await self._session.commit()
        await self._session.refresh(project)
        return project

    async def get_by_id(self, project_id: str) -> Project | None:
        result = await self._session.execute(select(Project).where(Project.id == project_id))
        return result.scalar_one_or_none()

    async def list_all(self, limit: int = 50, offset: int = 0):
        result = await self._session.execute(
            select(Project).order_by(Project.created_at.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def update(self, project: Project, **kwargs) -> Project:
        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)
        await self._session.commit()
        await self._session.refresh(project)
        return project

    async def delete(self, project_id: str) -> bool:
        result = await self._session.execute(delete(Project).where(Project.id == project_id))
        await self._session.commit()
        return result.rowcount > 0
