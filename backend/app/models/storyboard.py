import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Storyboard(Base):
    __tablename__ = "storyboards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id", ondelete="CASCADE"), nullable=False)
    frame_number = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    prompt_used = Column(Text, nullable=True)
    selected = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
