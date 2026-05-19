# Deployment Guide — DClaw Video

## Frontend (Vercel) ✅ DEPLOYED

**URL:** https://dclaw-video.vercel.app
**Project:** dclaw-video
**Git:** https://github.com/dclawstack/dclaw-video

Last deployed: 2026-05-19 via `vercel deploy --prod`

### How to redeploy frontend
```bash
cd /home/oc/suresh/Project-video/frontend
vercel deploy --prod --yes
```

## Backend (Needs Hosting)

The backend FastAPI app needs a server. Recommended options:

### Option A: Render.com (Free Tier)
1. Go to https://render.com
2. "New Web Service" → Connect your GitHub repo
3. Root directory: `backend`
4. Build command: `pip install -e ".[dev]"`
5. Start command: `uvicorn app.api.main:app --host 0.0.0.0 --port 8067`
6. Add environment variables:
   - `DCLAW_DATABASE_URL` → Render Postgres URL (or keep SQLite for testing)
   - `DCLAW_SECRET_KEY` → Generate a strong random key
   - `DCLAW_OPENROUTER_API_KEY` → Your API key

### Option B: Railway.app (Free Tier)
1. Go to https://railway.app → "New Project" → "Deploy from GitHub"
2. Configure:
   - Build: `pip install -e ".[dev]"`
   - Start: `uvicorn app.api.main:app --host 0.0.0.0 --port 8067`
3. Add Postgres service or keep SQLite

### Option C: Self-hosted (VPS)
```bash
# On your server
git clone https://github.com/dclawstack/dclaw-video.git
cd dclaw-video/backend
pip install -e ".[dev]"
DCLAW_DATABASE_URL=sqlite+aiosqlite:///./dev.db \
DCLAW_SECRET_KEY=$(openssl rand -hex 32) \
uvicorn app.api.main:app --host 0.0.0.0 --port 8067
```

## Environment Variables for Backend

| Variable | Required | Value |
|----------|----------|-------|
| `DCLAW_DATABASE_URL` | Yes | SQLite or Postgres URL |
| `DCLAW_SECRET_KEY` | Yes | JWT signing key |
| `DCLAW_OPENROUTER_API_KEY` | Yes | Your API key |
| `DCLAW_OPENROUTER_MODEL` | No | `meta-llama/llama-3.1-8b-instruct` |

## Vercel CLI Commands

```bash
# Deploy frontend
vercel --prod

# Check deployments
vercel list

# Logs
vercel logs --tail

# Remove deployment
vercel remove dclaw-video
```

## Vercel Account
- **Username:** sureshbabu-1109
- **CLI:** Already authenticated
