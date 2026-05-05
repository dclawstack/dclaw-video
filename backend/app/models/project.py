import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    script_text = Column(Text, nullable=False)
    status = Column(Enum("draft", "storyboard", "rendering", "done", name="project_status"), nullable=False, default="draft")
    video_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    template = Column(String, default="youtube_explainer")
    voice_profile_id = Column(UUID(as_uuid=True), nullable=True)
    character_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
