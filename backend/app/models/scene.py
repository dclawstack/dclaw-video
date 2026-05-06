import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    scene_number = Column(Integer, nullable=False)
    narration_text = Column(Text, nullable=False, default="")
    visual_prompt = Column(Text, nullable=False, default="")
    duration_seconds = Column(Float, nullable=False, default=5.0)
    status = Column(Enum("pending", "generating", "done", "error", name="scene_status"), nullable=False, default="pending")
    video_clip_url = Column(String, nullable=True)
    scene_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
