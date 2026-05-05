# DClaw Video

AI Video Director & Editor — script to publishable video without touching a timeline.

## Features
- **Script-to-Scene Pipeline**: Write a script, AI breaks it into scenes
- **Local Generation**: ComfyUI + FLUX + AnimateDiff + LivePortrait
- **Character Consistency**: IP-Adapter face lock across scenes
- **Auto-Voiceover**: Kokoro TTS + subtitle burn-in
- **Template Workflows**: YouTube Explainer, Product Demo, Social Reel

## Development

### Prerequisites
- Docker + Docker Compose
- Node.js 20 (for frontend)
- Python 3.11 (for backend)
- ComfyUI running locally (or in Docker on GPU host)
- Ollama running locally

### Quick Start
```bash
# Start infra
docker compose -f docker-compose.dev.yml up redis minio db

# Backend
cd backend
pip install -e ".[dev]"
uvicorn app.api.main:app --reload --port 8094

# Celery worker (in another terminal)
celery -A app.core.celery_app worker -l info -Q dclaw

# Frontend
cd frontend
npm install
npm run dev
```

### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `DCLAW_DATABASE_URL` | `postgresql+asyncpg://...` | Postgres connection |
| `DCLAW_REDIS_URL` | `redis://localhost:6379/0` | Redis broker |
| `DCLAW_COMFYUI_URL` | `http://localhost:8188` | ComfyUI API |
| `DCLAW_OLLAMA_URL` | `http://localhost:11434` | Ollama API |
| `DCLAW_MINIO_ENDPOINT` | `localhost:9000` | MinIO S3 endpoint |

## Project Structure
```
backend/      FastAPI + Celery + SQLAlchemy
frontend/     Next.js 14 + Tailwind + Remotion
src-tauri/    Tauri v2 desktop wrapper
helm/         Kubernetes Helm chart
.github/      CI/CD workflows
```

## License
MIT
