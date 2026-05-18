from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DClaw Video"
    debug: bool = False

    database_url: str = "sqlite+aiosqlite:///./dev.db"
    redis_url: str = "redis://localhost:6379/0"

    comfyui_url: str = "http://localhost:8188"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    openrouter_api_key: str = ""
    openrouter_model: str = "meta-llama/llama-3.1-8b-instruct"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "dclaw"
    minio_secure: bool = False

    kokoro_model_path: str = "./models/kokoro-v1.0.onnx"
    kokoro_voices_path: str = "./models/voices.bin"

    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    celery_result_backend: str | None = None
    celery_task_serializer: str = "json"
    celery_accept_content: list[str] = ["json"]

    model_config = SettingsConfigDict(env_prefix="DCLAW_", env_file=".env")


settings = Settings()
