from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SceneUpdate(BaseModel):
    narration_text: str | None = None
    visual_prompt: str | None = None
    duration_seconds: float | None = None


class SceneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    scene_number: int
    narration_text: str
    visual_prompt: str
    duration_seconds: float
    status: str
    video_clip_url: str | None
    scene_metadata: dict[str, object]
    created_at: datetime
    updated_at: datetime
