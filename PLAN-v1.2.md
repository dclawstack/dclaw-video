# DClaw Video — v1.2 Strategic Plan

> 📘 **REVISED PRD v2.3 available:** See `REVISED-PRD.md` for complete gap analysis, current state, and full feature roadmap.


> Y Combinator Gap Analysis & Prioritized Implementation Roadmap
> Git username: `sureshOC` | Commit ready: ✅ | Database: SQLite (local dev)

---

## Executive Summary

DClaw Video is an **AI Video Director & Editor** — script to publishable video without touching a timeline. It targets creators, marketers, and educators who need rapid video production at scale.

This plan identifies five mission-critical gaps that must be closed before this product can graduate from scaffold to YC-investible startup.

---

## Phase 1: Critical Infrastructure Debt (Fix Before Any Feature Work)

### 🚨 C0.1 — Fix Core Model & Database Infrastructure
**Complexity: 0 | Status: BLOCKING ALL DEVELOPMENT**

The codebase has **4 architecture violations** that will cause cascading failures. These MUST be fixed before any feature implementation.

| Violation | File | Severity | Fix |
|---|---|---|---|
| `declarative_base()` used instead of `DeclarativeBase` | `app/core/db.py` | 🔴 CRITICAL | Remove `Base = declarative_base()`, import from `app.models.base` |
| Models use legacy `Column()` instead of `Mapped[]`+`mapped_column()` | All model files | 🔴 CRITICAL | Rewrite all 6 models to use SQLAlchemy 2.0 mapped syntax |
| No `repositories/` directory — DB access via inline ORM | Missing | 🔴 CRITICAL | Create repository layer per AGENTS.md spec |
| Zero alembic migration infrastructure | Missing | 🟡 HIGH | Initialize alembic, generate initial migration |
| Frontend directory structure doesn't match AGENTS.md spec | `app/`, `components/` | 🟡 HIGH | Move to `src/app/`, `src/components/ui/`, create `src/lib/api.ts` |
| Pre-built UI components missing | `components/ui/` empty | 🟡 HIGH | Add button, card, input, label, badge, select, dialog, table, tabs, avatar |
| Missing `fastapi lifespan` handler | `app/api/main.py` | 🟡 HIGH | Add lifespan for engine disposal |

**Deliverables:**
- `backend/app/core/db.py` — refactored
- `backend/app/models/*.py` — all 6 models rewritten (project, scene, storyboard, render_job, character, voice_profile)
- `backend/app/repositories/` — 6 repository modules with CRUD
- `backend/alembic/` — initialized with initial migration
- `frontend/src/` — restructured with `lib/api.ts`, `components/ui/`

---

## Phase 2: YC Gap Analysis

### Gap 1: Not a Working Product — Just a Scaffold
**Severity: 🔴 CRITICAL**

YC reviews **working demos**, not architecture diagrams. The current codebase has:
- Skeleton CRUD routes (no real business logic)
- Empty service implementations
- No end-to-end AI pipeline working
- No actual video generation

> **YC Question:** "Can I sign up and generate a video in 5 minutes?"
> **Current Answer:** No.

### Gap 2: No Clear "Hair on Fire" Problem
**Severity: 🔴 CRITICAL**

- **Descript** solves: "Transcription + text-based editing"
- **Runway** solves: "AI magic for Hollywood creators"
- **Loom** solves: "Quick async video messages"
- **Synthesia** solves: "AI avatars for enterprise training"

**DClaw Video's positioning is too generic.** We need a razor-sharp wedge:

> **Proposed Wedge:** "AI Video Director for Content Teams" — Marketing/social media teams who need 10x video output with zero editing skills. Script → auto-scene generation → auto-voiceover → auto-render → publish.

### Gap 3: No Competitive Moat / Differentiator
**Severity: 🟡 HIGH**

Current feature list is a subset of existing tools. Differentiators needed:
1. **Local-first pipeline** — ComfyUI + FLUX runs locally = no cloud costs, no data leakage (privacy moat)
2. **Character consistency** — IP-Adapter face lock across scenes (unique for local tools)
3. **Template system** — Pre-built YouTube Explainer / Product Demo / Social Reel templates with one-click generation
4. **Script-to-publish in 3 minutes** — End-to-end speed benchmark others can't match

### Gap 4: No Business Model or Metrics
**Severity: 🟡 HIGH**

YC expects: pricing, ideal customer profile, estimated CAC/LTV. Current plan has none.

> **Proposed Model:** Freemium SaaS
> - Free tier: 5 videos/month, 720p, watermark
> - Pro ($29/mo): Unlimited, 1080p, no watermark, custom templates, team collaboration
> - Enterprise ($99/seat/mo): On-prem ComfyUI, SSO, API access, priority support

### Gap 5: Incomplete Frontend — No Actual User Experience
**Severity: 🟡 HIGH**

Current frontend has basic pages but:
- No component library (shadcn components missing)
- No typed API client (`src/lib/api.ts` missing)
- No layout/styling framework consistency
- No error boundaries, loading states, or optimistic UI

---

## Phase 3: Prioritized Feature Roadmap (Complexity-Based)

### Complexity Legend
- **0**: Low complexity / Core foundational (Quick wins, infrastructure)
- **1**: Medium complexity / Core differentiators (Product-defining features)
- **2**: High complexity / Advanced (AI pipelines, real-time, rendering farms)

---

### complexity = 0 — Infrastructure & Foundation (Do First)

#### C0.1 — Fix Core Database & Model Infrastructure
Already detailed in Phase 1. This is the must-fix-before-anything-else item.

- [ ] Fix `db.py` to use `DeclarativeBase` from `app.models.base`
- [ ] Rewrite all models: `project.py`, `scene.py`, `storyboard.py`, `render_job.py`, `character.py`, `voice_profile.py`
- [ ] Create `repositories/` with CRUD for each entity
- [ ] Initialize alembic, generate initial migration
- [ ] Fix `main.py` to add lifespan handler
- [ ] Fix `config.py` database_url to support both Postgres and SQLite

**Files:** `backend/app/core/db.py`, `backend/app/models/*.py`, `backend/app/repositories/*.py`, `backend/alembic/`

#### C0.2 — SQLite Local Development Database
**Description:** Configure the application to run with SQLite for local development without requiring Docker/Postgres.
- [ ] Add `sqlite+aiosqlite` support in `config.py` (auto-detect if Postgres is unavailable)
- [ ] Create `backend/dev.db` with proper initialization
- [ ] Add `scripts/init_db.py` for bootstrapping local SQLite
- [ ] Update `conftest.py` to support SQLite test mode

**Files:** `backend/app/core/config.py`, `backend/scripts/init_db.py`, `backend/tests/conftest.py`

#### C0.3 — Frontend Infrastructure (Component Library + API Client)
**Description:** Build the foundational UI components and typed API client so feature pages can be built rapidly.
- [ ] Restructure frontend: `app/` → `src/app/`, `components/` → `src/components/`
- [ ] Create `src/components/ui/` with pre-built components:
  - [ ] Button (variants: default, destructive, outline, secondary, ghost, link)
  - [ ] Card (Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter)
  - [ ] Input (standard text input)
  - [ ] Label (form label)
  - [ ] Badge (variants: default, secondary, destructive, outline)
  - [ ] Select (native select with onValueChange)
  - [ ] Dialog (modal with trigger, content, header, title)
  - [ ] Table (Table, TableHeader, TableBody, TableRow, TableHead, TableCell)
  - [ ] Tabs (Tabs, TabsList, TabsTrigger, TabsContent)
  - [ ] Avatar (Avatar, AvatarImage, AvatarFallback)
- [ ] Create `src/lib/api.ts` typed fetch wrapper with error handling
- [ ] Ensure `tailwindcss-animate` is in dependencies (not devDependencies)
- [ ] Create consistent layout: `src/app/layout.tsx` with proper metadata

**Files:** `frontend/src/components/ui/*.tsx`, `frontend/src/lib/api.ts`, `frontend/src/app/layout.tsx`

#### C0.4 — Backend Tests & Healthchecks
**Description:** Comprehensive test coverage for all repositories and routes. Docker healthcheck verification.
- [ ] Tests for all 6 repositories (CRUD operations)
- [ ] Tests for all API routes (create, read, update, delete)
- [ ] Docker compose healthcheck verification
- [ ] Dockerfile `ARG NEXT_PUBLIC_API_URL` verification

**Files:** `backend/tests/test_*.py`

#### C0.5 — Project Dashboard (Frontend)
**Description:** A functional project dashboard listing all video projects with create/edit/delete flow.
- [ ] Projects list page at `/projects`
- [ ] Create project form with template selection
- [ ] Edit project details
- [ ] Delete with confirmation
- [ ] Status badges (draft, storyboard, rendering, done)

**Files:** `frontend/src/app/projects/page.tsx`, `frontend/src/app/projects/[id]/page.tsx`, `frontend/src/app/projects/new/page.tsx`

---

### complexity = 1 — Core Differentiators

#### C1.1 — AI Script-to-Scene Pipeline
**Description:** The killer feature. User writes a script → AI breaks into scenes → generates visual prompts → creates scene records.
- **Backend:** `/api/v1/ai/script-to-scenes` endpoint. Ollama integration for parsing scripts into structured scene data.
- **Frontend:** Script editor page with AI "Generate Scenes" button, scene preview cards.
- **Files:** `backend/app/services/script_parser.py`, `frontend/src/app/editor/script.tsx`

#### C1.2 — Scene Storyboard Generation with ComfyUI
**Description:** Generate 3 storyboard images per scene using ComfyUI + FLUX. User picks the best.
- **Backend:** ComfyUI workflow triggering, image upload to MinIO/S3, storyboard CRUD.
- **Frontend:** Storyboard gallery with image picker per scene.
- **Files:** `backend/app/services/comfyui_client.py`, `frontend/src/app/storyboard/page.tsx`

#### C1.3 — AI Voiceover & TTS Pipeline
**Description:** Generate narration audio for each scene using Kokoro TTS. Preview and regenerate capability.
- **Backend:** TTS service integration, audio file storage, voice profile selection.
- **Frontend:** Voice preview player, voice profile selector.
- **Files:** `backend/app/services/tts_service.py`, `frontend/src/components/voice-player.tsx`

#### C1.4 — Auto-Captions & Subtitles
**Description:** Generate SRT/VTT subtitles from narration. Editable transcript synced to video.
- **Backend:** Transcription pipeline (Kokoro → text), subtitle file generation.
- **Frontend:** Caption editor with timestamps.
- **Files:** `backend/app/services/subtitle_generator.py`, `frontend/src/components/caption-editor.tsx`

#### C1.5 — Video Assembly & Render Engine
**Description:** Assemble scenes + audio + captions into final video. Background render via Celery.
- **Backend:** ffmpeg-based video assembler, Celery render pipeline, progress tracking via WebSocket.
- **Frontend:** Render queue, progress bar, download button.
- **Files:** `backend/app/services/video_assembler.py`, `backend/app/tasks/render_tasks.py`, `frontend/src/app/render-queue/page.tsx`

---

### complexity = 2 — Advanced Differentiators

#### C2.1 — Character Consistency (IP-Adapter Face Lock)
**Description:** Upload a face image. AI locks character appearance across all scenes via IP-Adapter.
- **Backend:** Face embedding generation, IP-Adapter workflow injection, character reference storage.
- **Frontend:** Character manager, face upload, preview across scenes.

#### C2.2 — Template System
**Description:** One-click YouTube Explainer, Product Demo, Social Reel templates.
- Pre-built scripts + scene structures + style presets
- User can fork templates

#### C2.3 — Collaboration & Review (Comments on Timestamps)
**Description:** Share project link → reviewers comment on timestamps → approval workflow.
- **Backend:** Comment system with timestamp anchoring, reviewer role, approval status.
- **Frontend:** Review mode with comment threads.

#### C2.4 — Multi-Platform Export
**Description:** Auto-format for YouTube (16:9), TikTok/Instagram Reels (9:16), LinkedIn (1:1).
- ffmpeg auto-crop/reframe + platform-specific subtitles.

#### C2.5 — AI Video Copilot (Chat Assistant)
**Description:** Chat interface for editing. "Make scene 3 shorter." "Add dramatic music to scene 2."
- LLM-powered command parser → automated edits.

---

## Phase 4: Database Schema (SQLite for Local Development)

```
projects
├── id (uuid, pk)
├── title (string, not null)
├── script_text (text, not null)
├── status (enum: draft/storyboard/rendering/done)
├── video_url (string, nullable)
├── duration (integer, nullable)
├── template (string, default="youtube_explainer")
├── voice_profile_id (uuid, fk -> voice_profiles)
├── character_id (uuid, fk -> characters, nullable)
├── created_at (datetime)
└── updated_at (datetime)

scenes
├── id (uuid, pk)
├── project_id (uuid, fk -> projects, cascade)
├── scene_number (integer, not null)
├── narration_text (text, not null)
├── visual_prompt (text, not null)
├── duration_seconds (float, default=5.0)
├── status (enum: pending/generating/done/error)
├── video_clip_url (string, nullable)
├── scene_metadata (json, default={})
├── created_at (datetime)
└── updated_at (datetime)

storyboards
├── id (uuid, pk)
├── scene_id (uuid, fk -> scenes, cascade)
├── frame_number (integer, not null)
├── image_url (string, not null)
├── prompt_used (text, nullable)
├── selected (boolean, default=false)
└── created_at (datetime)

render_jobs
├── id (uuid, pk)
├── project_id (uuid, fk -> projects, cascade)
├── celery_task_id (string, not null)
├── progress_percent (integer, default=0)
├── status (enum: pending/started/success/failure)
├── logs (text, nullable)
├── result_url (string, nullable)
├── created_at (datetime)
└── updated_at (datetime)

characters
├── id (uuid, pk)
├── project_id (uuid, fk -> projects, cascade)
├── name (string, not null)
├── reference_image_url (string, not null)
├── face_embedding (string, nullable)
└── created_at (datetime)

voice_profiles
├── id (uuid, pk)
├── name (string, not null)
├── language (string, default="en")
├── gender (string, nullable)
├── sample_url (string, nullable)
└── created_at (datetime)
```

---

## Implementation Order (Week-by-Week)

| Week | Tasks | Complexity |
|------|-------|------------|
| Week 1 | C0.1 Fix DB/models, C0.2 SQLite local setup, C0.3 Frontend infrastructure | 0 |
| Week 2 | C0.4 Tests, C0.5 Project Dashboard, C1.1 AI Script-to-Scene | 0 + 1 |
| Week 3 | C1.2 Storyboard Generation, C1.3 Voiceover Pipeline | 1 |
| Week 4 | C1.4 Auto-Captions, C1.5 Video Assembly & Render | 1 |
| Week 5 | C2.1 Character Consistency (IP-Adapter) | 2 |
| Week 6 | C2.2 Template System, C2.3 Collaboration | 2 |
| Week 7 | C2.4 Multi-Platform Export, C2.5 AI Copilot | 2 |
| Week 8 | Polish, performance, onboarding flow, YC demo video | All |

---

## Success Criteria (for YC Submission)

1. ✅ Working local database (SQLite) — no Docker required for demo
2. ✅ Full CRUD for projects, scenes, storyboards
3. ✅ AI script parser producing structured scenes
4. ✅ ComfyUI integration generating storyboard images
5. ✅ TTS pipeline producing voiceover audio
6. ✅ Video assembly rendering final output
7. ✅ Functional frontend with all core screens
8. ✅ Test coverage > 60% for backend
9. ✅ Clean README with quick-start
10. ✅ One-line pitch: "AI Video Director for content teams — script to publishable video in 3 minutes"

---

## Current Blockers (Must Resolve Before Coding)

1. **AGENTS.md says `backend Port: 8067` but README says `8094`** — need to reconcile
2. **Models use legacy `Column()` and `declarative_base()`** — will cause SQLAlchemy 2.0 conflicts
3. **No `repositories/` directory** — direct ORM usage violates DClaw architecture rules
4. **Frontend structure doesn't match spec** — missing `src/` directory
5. **No pre-built UI components** — need to add shadcn-style components

---

*Plan generated: 2026-05-16 | Next step: Begin autonomous implementation starting with C0.1*
