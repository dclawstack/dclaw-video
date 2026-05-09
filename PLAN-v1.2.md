# DClaw Video — v1.2 Feature Roadmap

> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (peertube, jitsi), AI product research (Loom, Descript, Runway, Synthesia)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Video project CRUD
- [ ] Timeline editor
- [ ] Asset library
- [ ] Basic export/render
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Video Copilot (Editor Assistant)
**Description:** AI assistant that edits video from text commands. "Remove all ums and ahs. Add captions."
- **AI Angle:** Text-to-edit commands. Auto-editing (silence removal, filler word detection).
- **Backend:** `/api/v1/ai/video-chat` endpoint. Edit command parser.
- **Frontend:** Chat panel with preview. Command history.
- **Files:** `backend/app/services/video_ai.py`, `frontend/src/components/video-copilot.tsx`

#### 2. Auto-Captions & Transcription
**Description:** Generate accurate captions in multiple languages. Editable transcript synced to video.
- **AI Angle:** Whisper STT + translation.
- **Backend:** Transcription pipeline. SRT/VTT generation.
- **Frontend:** Transcript editor with video sync.
- **Files:** `backend/app/services/transcription.py`

#### 3. Text-Based Video Editor
**Description:** Edit video by editing the transcript. Delete text to cut video. Type to add B-roll.
- **Backend:** Transcript-to-timeline mapping.
- **Frontend:** Transcript editor with video preview.
- **Files:** `frontend/src/app/editor/transcript.tsx`

#### 4. Screen & Camera Recording
**Description:** Record screen, camera, or both. Multi-track timeline with independent editing.
- **Backend:** Recording ingestion. Multi-track sync.
- **Frontend:** Recorder widget. Multi-track timeline.
- **Files:** `frontend/src/app/recorder/`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Scene Detection & B-Roll Suggestions
**Description:** Auto-detect scene changes. Suggest stock B-roll for context.
- **AI Angle:** Scene detection (CV). B-roll recommendation (semantic matching).
- **Backend:** Scene analysis pipeline.
- **Frontend:** Scene markers with B-roll suggestions.

#### 6. AI Avatars & Voice Cloning
**Description:** Generate video with AI avatars from text. Clone your voice for narration.
- **AI Angle:** TTS + avatar animation (HeyGen-style).
- **Backend:** Avatar generation pipeline.
- **Frontend:** Avatar creator with preview.

#### 7. Collaboration & Review
**Description:** Share drafts. Comment on specific timestamps. Approval workflow.
- **Backend:** Comment system with timestamp anchoring.
- **Frontend:** Review mode with comment threads.

#### 8. Multi-Platform Export
**Description:** Export optimized for YouTube, TikTok, Instagram, LinkedIn with auto-formatting.
- **Backend:** Render farm with format templates.
- **Frontend:** Export presets with platform-specific settings.

### P2 — Could Have (v1.3+)

#### 9. AI-Generated Video from Script
**Description:** Write a script. AI generates complete video with avatars, B-roll, and music.

#### 10. Real-Time Collaboration Editing
**Description:** Multiple editors working on same timeline simultaneously.

#### 11. Motion Tracking & Effects
**Description:** Auto motion tracking for text overlays and effects.

#### 12. Live Streaming with AI Moderation
**Description:** Stream live with real-time AI captioning and content moderation.

---

## Implementation Priority

1. **Week 1–2:** AI Video Copilot (P0.1) + Auto-Captions (P0.2)
2. **Week 3–4:** Text-Based Editor (P0.3) + Screen Recording (P0.4)
3. **Week 5–6:** Scene Detection (P1.5) + AI Avatars (P1.6)
4. **Week 7–8:** Collaboration (P1.7) + Multi-Platform Export (P1.8)
