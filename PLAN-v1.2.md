# DClaw Video — YC W24 Strategic Plan

> **Target:** Y Combinator W24 Batch | **Domain:** AI Video Production for B2B Content Teams
> **Pitch:** "Loom for AI video — turn scripts into publishable videos in 3 minutes"
> **Git:** `sureshOC` | **Commits:** `616e240` (C0.1 infra), `HEAD` (lint fix)

---

## 1. YC Gap Analysis: Why Current Product Won't Get In

### The Brutal Truth

YC accepts ~2% of applicants. For B2B SaaS, they look for:
1. **"Hair on fire" problem** — Customers are desperate enough to pay TODAY
2. **Rapid distribution** — $1M ARR path within 12–18 months
3. **Defensible moat** — Not easily replicable by OpenAI/Anthropic
4. **Working product** — Demo must work in the interview room
5. **Team velocity** — Can ship 10x faster than incumbents

### Our 7 Critical Gaps

| # | Gap | Severity | YC Interview Risk |
|---|-----|----------|-------------------|
| 1 | **No authenticated product** — Anyone can access, no user accounts | 🔴 CRITICAL | "Who's your user? Show me their dashboard." → **FAIL** |
| 2 | **No AI pipeline working** — Script → video is manual mockup | 🔴 CRITICAL | "Show me the AI working." → **FAIL** |
| 3 | **No subscription model** — Can't charge money | 🔴 CRITICAL | "How do you make money?" → **FAIL** |
| 4 | **Positioning too broad** — "AI video editor" vs. specific persona | 🟡 HIGH | "Who exactly pays for this and why?" → **WEAK** |
| 5 | **No collaboration** — Single user only, no team features | 🟡 HIGH | "How do teams use this?" → **FAIL** |
| 6 | **No video export** — Can't download actual MP4 file | 🟡 HIGH | "Can I download the video?" → **FAIL** |
| 7 | **No onboarding** — No demo, no templates, no tutorial | 🟡 HIGH | "Show me a new user using this." → **FAIL** |

### The Winning Wedge: "AI Video Briefing Tool for Customer-Facing Teams"

**Specific persona:** Customer success managers, sales engineers, and onboarding specialists who need to create personalized video walkthroughs at scale.

**Why they have hair on fire:**
- Current workflow: Record screen with Loom → edit in Descript → export → upload to CRM → send to customer
- Time per video: 30–45 minutes
- With DClaw Video: Paste script → AI generates scenes + voiceover → download MP4 → 3 minutes
- **10x faster = $200+/hour saved per CSM**

**Why this is defensible:**
- Template library specific to SaaS onboarding workflows
- CRM integrations (Salesforce, HubSpot) for 1-click sending
- Analytics on video engagement (who watched, for how long)
- Voice cloning maintains brand consistency across team

---

## 2. Required Features for Top Position in AI Video Domain

### Must-Have for YC (Ship in 2 Weeks)

| Feature | Why It Matters | File Target |
|---------|----------------|-------------|
| **User Auth (JWT)** | Every YC demo starts with "sign up and log in" | `backend/app/api/routes/auth.py` |
| **Real AI Script Parser** | OpenRouter LLM parses script into scenes | `backend/app/services/ai_service.py` |
| **Cloud Video Render** | FFmpeg assembles scenes into downloadable MP4 | `backend/app/services/video_assembler.py` |
| **Subscription Tiers** | Free/Pro/Enterprise with Stripe | `backend/app/services/billing.py` |
| **Template Gallery** | Pre-built onboarding/demo scripts | `frontend/src/app/templates/page.tsx` |
| **MP4 Export & Download** | Actually download the final video | `frontend/src/app/projects/[id]/render/page.tsx` |
| **Project Sharing** | Public link to view video without login | `backend/app/api/routes/share.py` |

### Should-Have for Demo Day (Month 2–3)

| Feature | Why It Matters | File Target |
|---------|----------------|-------------|
| **AI Voice Cloning** | Clone a team member's voice | `backend/app/services/voice_clone.py` |
| **Screen Recording Upload** | Import existing screen recordings | `backend/app/api/routes/upload.py` |
| **CRM Integration** | Send videos via Salesforce/HubSpot | `backend/app/integrations/salesforce.py` |
| **Video Analytics** | Track views, completion rates | `backend/app/services/analytics.py` |
| **Collaborative Comments** | Team reviews on video timeline | `frontend/src/components/comment-thread.tsx` |
| **Multi-Language Export** | Auto-translate for global teams | `backend/app/services/translation.py` |
| **AI Copilot Chat** | "Add a scene about pricing" | `frontend/src/components/ai-copilot.tsx` |

### Could-Have for Series A (Month 6+)

| Feature | Why It Matters | File Target |
|---------|----------------|-------------|
| **Real-Time Collaboration** | Multiple editors, Figma-style | WebSocket + Yjs CRDT |
| **Custom AI Avatars** | HeyGen-style avatar generation | `backend/app/services/avatar_gen.py` |
| **Live Stream with AI** | Auto-caption live streams | `backend/app/services/live_stream.py` |
| **Mobile App** | Record + edit on phone | React Native or Tauri mobile |
| **API for Enterprises** | Programmatic video generation | `backend/app/api/v2/` |

---

## 3. Implementation Roadmap (Reality-Based)

| Week | Focus | Deliverables | Complexity |
|------|-------|--------------|------------|
| **W1** | Auth + AI Pipeline | JWT auth, OpenRouter script parser, user-scoped projects | 1 |
| **W2** | Real Render + Export | FFmpeg MP4 assembly, download button, render queue | 1 |
| **W3** | Templates + Billing | 3 templates, Stripe checkout, subscription gates | 1 |
| **W4** | Polish + Share | Public share links, email notifications, onboarding flow | 0 |
| **W5** | Voice + Screen | Screen recording import, voice selection, preview player | 1 |
| **W6** | Integrations | HubSpot/Salesforce embed, analytics dashboard | 2 |
| **W7** | AI Copilot | Chat interface for editing, auto-suggestions | 2 |
| **W8** | YC Demo Prep | Demo video, metrics, pitch deck, practice | — |

---

## 4. Database Schema (Updated for YC)

```
users (NEW)
├── id (uuid, pk)
├── email (string, unique, not null)
├── hashed_password (string, not null)
├── full_name (string)
├── subscription_tier (enum: free/pro/enterprise, default=free)
├── stripe_customer_id (string, nullable)
├── team_id (uuid, fk -> teams, nullable)
├── created_at (datetime)
└── updated_at (datetime)

teams (NEW)
├── id (uuid, pk)
├── name (string, not null)
├── owner_id (uuid, fk -> users)
├── subscription_tier (enum: free/pro/enterprise)
├── stripe_subscription_id (string, nullable)
├── created_at (datetime)
└── updated_at (datetime)

projects
├── id (uuid, pk)
├── user_id (uuid, fk -> users, not null) ← NEW
├── team_id (uuid, fk -> teams, nullable) ← NEW
├── title (string, not null)
├── script_text (text, not null)
├── status (enum: draft/storyboard/rendering/done)
├── video_url (string, nullable)
├── duration (integer, nullable)
├── template (string, default="youtube_explainer")
├── is_public (boolean, default=false) ← NEW
├── public_slug (string, unique, nullable) ← NEW
├── voice_profile_id (uuid, fk -> voice_profiles)
├── character_id (uuid, fk -> characters, nullable)
├── created_at (datetime)
└── updated_at (datetime)

scenes (unchanged)
storyboards (unchanged)
render_jobs (unchanged)
characters (unchanged)
voice_profiles (unchanged)
```

---

## 5. YC Success Checklist

- [x] Working SQLite database
- [x] Repository pattern + clean models
- [x] Frontend build passes (Next.js + Tailwind)
- [x] ESLint passes
- [x] Tests pass (5/5)
- [ ] **User authentication**
- [ ] **OpenRouter AI integration (script parser)**
- [ ] **Real FFmpeg video render**
- [ ] **Stripe billing**
- [ ] **Template gallery**
- [ ] **MP4 download**
- [ ] **Public share links**
- [ ] **Landing page + pricing**
- [ ] **Demo video (2 min)**
- [ ] **10+ beta users**

---

*Updated: 2026-05-16 | Next: Implement W1 (Auth + AI Pipeline)*
