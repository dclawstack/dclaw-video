from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str | None
    subscription_tier: str
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class AIChatMessage(BaseModel):
    role: str
    content: str


class AIChatRequest(BaseModel):
    messages: list[AIChatMessage]
    temperature: float = 0.7


class ScriptToScenesRequest(BaseModel):
    script: str
    tone: str = "professional"
    max_scenes: int = 10


class SceneSuggestion(BaseModel):
    scene_number: int
    narration_text: str
    visual_prompt: str
    duration_seconds: float


class ScriptToScenesResponse(BaseModel):
    scenes: list[SceneSuggestion]
