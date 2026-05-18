# DClaw Video

> **AI Video Production for Customer-Facing Teams** — Turn scripts into publishable videos in 3 minutes.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black)](https://nextjs.org)

---

## The Problem

Customer Success Managers, Sales Engineers, and Onboarding Specialists spend **30–45 minutes** creating a single personalized video walkthrough:

1. Record screen with Loom
2. Edit out mistakes in Descript
3. Export, upload to CRM
4. Send to customer

**Result:** 5–10 videos/day max. Scale is impossible.

## The Solution

DClaw Video replaces the entire workflow with a script:

```
Paste script → AI breaks into scenes → Auto-voiceover → Download MP4 → Send
```

**3 minutes. Not 45.**

### Key Differentiators

| Feature | DClaw Video | Loom + Descript |
|---------|-------------|-----------------|
| Time per video | **3 min** | 30–45 min |
| Personalization at scale | **Yes** (script variables) | No (manual re-record) |
| Voice consistency | **Yes** (voice cloning) | Varies per recording |
| Analytics | **Built-in** (views, completion) | Limited |
| CRM Integration | **HubSpot, Salesforce** | Manual export |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- FFmpeg (for video assembly)
- OpenRouter API key (for AI script parsing)

### 1. Clone & Setup

```bash
git clone https://github.com/dclawstack/dclaw-video.git
cd dclaw-video
```

### 2. Backend

```bash
cd backend
pip install -e ".[dev]"

# Create .env file
cat > .env << 'EOF'
DCLAW_DATABASE_URL=sqlite+aiosqlite:///./dev.db
DCLAW_OPENROUTER_API_KEY=your-openrouter-key-here
DCLAW_OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct
DCLAW_SECRET_KEY=change-me-in-production
EOF

# Start server
uvicorn app.api.main:app --reload --port 8067
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3067](http://localhost:3067)

---

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Next.js    │────▶│   FastAPI    │────▶│   SQLite/        │
│  Frontend    │     │   Backend    │     │   PostgreSQL     │
└──────────────┘     └──────────────┘     └──────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │        AI Layer         │
              │  OpenRouter (GPT-4/etc) │
              │  Kokoro TTS (voice)     │
              │  FFmpeg (video render)  │
              └─────────────────────────┘
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DCLAW_DATABASE_URL` | No | `sqlite+aiosqlite:///./dev.db` | Database connection |
| `DCLAW_OPENROUTER_API_KEY` | **Yes** | — | OpenRouter API key for AI |
| `DCLAW_OPENROUTER_MODEL` | No | `meta-llama/llama-3.1-8b-instruct` | LLM model |
| `DCLAW_SECRET_KEY` | No | `change-me` | JWT signing key |
| `DCLAW_STRIPE_SECRET_KEY` | No | — | Stripe API key (billing) |

---

## Tech Stack

**Backend:**
- FastAPI + SQLAlchemy 2.0 (async)
- SQLite (dev) / PostgreSQL (prod)
- JWT authentication
- Celery (background jobs)
- OpenRouter (AI)
- FFmpeg (video assembly)

**Frontend:**
- Next.js 14 (App Router)
- Tailwind CSS + shadcn/ui components
- React Query (data fetching)
- Lucide icons

---

## Roadmap

- [x] Core infrastructure (DB, models, repositories)
- [x] Frontend component library
- [x] Lint & type checks pass
- [ ] User authentication (JWT)
- [ ] OpenRouter AI script parser
- [ ] FFmpeg video render pipeline
- [ ] Stripe billing (Free/Pro/Enterprise)
- [ ] Template gallery
- [ ] MP4 export & download
- [ ] HubSpot / Salesforce integration
- [ ] Video analytics dashboard

---

## Contributors

- [@sureshOC](https://github.com/sureshOC)

## License

MIT
