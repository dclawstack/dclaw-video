from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    title: str
    script_text: str
    template: str = "youtube_explainer"
    voice_profile_id: UUID | None = None
    character_id: UUID | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    script_text: str | None = None
    status: str | None = None
    template: str | None = None
    voice_profile_id: str | None = None
    character_id: str | None = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    script_text: str
    status: str
    video_url: str | None
    duration: int | None
    template: str
    voice_profile_id: UUID | None
    character_id: UUID | None
    created_at: datetime
    updated_at: datetime
