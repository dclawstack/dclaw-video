import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class VoiceProfile(Base):
    __tablename__ = "voice_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    kokoro_voice_id = Column(String, nullable=False)
    speed = Column(Float, nullable=False, default=1.0)
    language = Column(String, nullable=False, default="en")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
