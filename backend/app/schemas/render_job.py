from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RenderJobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    celery_task_id: str
    progress_percent: int
    status: str
    logs: str | None
    result_url: str | None
    created_at: datetime
    updated_at: datetime
