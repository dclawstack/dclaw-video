from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.render_job import RenderJob


class RenderJobRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, project_id: str, celery_task_id: str) -> RenderJob:
        job = RenderJob(project_id=project_id, celery_task_id=celery_task_id)
        self._session.add(job)
        await self._session.commit()
        await self._session.refresh(job)
        return job

    async def get_by_id(self, job_id: str) -> RenderJob | None:
        result = await self._session.execute(
            select(RenderJob).where(RenderJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def list_by_project(self, project_id: str) -> list[RenderJob]:
        result = await self._session.execute(
            select(RenderJob)
            .where(RenderJob.project_id == project_id)
            .order_by(RenderJob.created_at.desc())
        )
        return list(result.scalars().all())

    async def update(self, job: RenderJob, **kwargs: object) -> RenderJob:
        for key, value in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, value)
        await self._session.commit()
        await self._session.refresh(job)
        return job

    async def delete(self, job_id: str) -> bool:
        result = await self._session.execute(
            delete(RenderJob).where(RenderJob.id == job_id)
        )
        await self._session.commit()
        return bool(result.rowcount > 0)  # type: ignore[attr-defined]
