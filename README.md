# Minari · 実成

> **Autonomous Flaky-Test Repair Agent**  
> GitLab Track · Google Cloud Rapid Agent Hackathon 2026

[![Live App](https://img.shields.io/badge/Live%20App-minari--eight.vercel.app-34d399?style=flat-square)](https://minari-eight.vercel.app)
[![API Health](https://img.shields.io/badge/API-Cloud%20Run%20Tokyo-60a5fa?style=flat-square)](https://minari-api-1063669194601.asia-northeast1.run.app/api/v1/healthz)
[![Demo Repo](https://img.shields.io/badge/Demo-GitLab%20Project-fbbf24?style=flat-square)](https://gitlab.com/francisdanielgenese-group/francisdanielgenese-project)
[![License: MIT](https://img.shields.io/badge/License-MIT-white?style=flat-square)](LICENSE)

---

## What is Minari?

Minari is a five-stage autonomous agent that detects a flaky test, diagnoses its root cause using Gemini 2.5, generates a fix, proves the fix green in five isolated GitLab CI runs, and opens a reviewed merge request — all without a human touching the code.

**Detect → Diagnose → Fix → Verify → Deliver**

The complete loop runs in under two minutes.

---

## Hackathon Details

| Field | Value |
|---|---|
| **Hackathon** | Google Cloud Rapid Agent Hackathon 2026 |
| **Track** | GitLab |
| **Developer** | Francis Daniel Genese (Mizu) |
| **Submission deadline** | June 11, 2026 · 2:00 PM PT |
| **Live app** | https://minari-eight.vercel.app |
| **Source repo** | https://github.com/Mizunandayo/minari |
| **Demo GitLab project** | https://gitlab.com/francisdanielgenese-group/francisdanielgenese-project |

---

## Key Features

- **Five-stage LangGraph pipeline** — conditional edges, early exit on low confidence, no wasted CI minutes
- **Assertion-safety gate** — tree-sitter syntax check + AST walk confirms every original assertion is preserved; enforced at the database level. The fix can never weaken a test.
- **Real CI verification** — five isolated GitLab CI runs required before a fix is accepted. No synthetic results.
- **Never auto-merges** — Minari opens a merge request with a reviewer assigned, CI proof attached, and the full diagnosis report. A human approves.
- **Bidirectional GitLab MCP** — Minari consumes the GitLab MCP server to read code and drive CI. It also exposes itself as an MCP server so other agents can call `detect`, `diagnose`, `fix`, and `verify` as tools.
- **pgvector similarity recall** — 768-dimensional Gemini embeddings over past diagnoses. Accuracy compounds with every run.
- **Live SSE dashboard** — each agent stage streams live to the Next.js frontend. Observers watch the AI reason in real time.

---

## Tech Stack

### Agent & LLM
| Tool | Role |
|---|---|
| LangGraph | Agent orchestration |
| Gemini 2.5 Pro | Diagnosis reasoning |
| Gemini 2.5 Flash | Fix generation |
| gemini-embedding-001 | 768-d embeddings |
| GitLab MCP server | Bidirectional integration |

### Backend
| Tool | Role |
|---|---|
| Python 3.12 | Runtime |
| FastAPI | Async API |
| Pydantic v2 | Typed schemas |
| tree-sitter | Syntax gate |
| defusedxml | XXE-hardened JUnit parsing |
| sse-starlette | Live SSE stream |
| asyncpg | Postgres driver |
| slowapi | Rate limiting |
| uv | Packaging |

### Data & Infrastructure
| Tool | Role |
|---|---|
| Supabase Postgres | Primary store |
| pgvector (HNSW) | Similarity search |
| Upstash Redis | Shared rate-limit store |
| Google Cloud Run (Tokyo) | Backend deployment |
| Vercel | Frontend deployment |

### Frontend
| Tool | Role |
|---|---|
| Next.js 15 | Framework |
| Tailwind CSS v4 | Styling |
| Framer Motion | Animations |
| Recharts | Charts |
| lucide-react | Icons |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│         Next.js Dashboard (Vercel)          │
│         live SSE stream · HTTPS             │
└───────────────────┬─────────────────────────┘
                    │  SSE / HTTPS · API-key + HMAC
┌───────────────────▼─────────────────────────┐
│      FastAPI + LangGraph Agent              │
│      Google Cloud Run · Tokyo               │
│                                             │
│  [Detect] → [Diagnose] → [Fix] →           │
│  [Verify] → [Deliver]                       │
└──┬──────────┬──────────┬────────────────────┘
   │          │          │
   ▼          ▼          ▼
GitLab MCP  Gemini 2.5  Supabase
(read/CI/MR) Pro+Flash  Postgres+pgvector
             Embeddings
                        Upstash Redis
                        (rate limits)
```

### Safety guarantees
1. **Syntax gate** — tree-sitter parses the fix before it is accepted
2. **AST walk** — confirms original assertions are a subset of the rewritten test
3. **DB constraint** — assertion preservation enforced at write time
4. **5× CI verification** — five fresh isolated pipeline runs, no cache, no parallelism
5. **No auto-merge** — merge request requires human approval

---

## Project Structure

```
minari/
├── apps/
│   ├── api/                        # FastAPI backend
│   │   ├── app/
│   │   │   ├── agents/             # LangGraph graph, nodes, state
│   │   │   │   └── nodes/          # detect, diagnose, fix, verify, deliver
│   │   │   ├── api/v1/             # REST endpoints + SSE stream
│   │   │   ├── core/               # Config, logging, rate limiting, security
│   │   │   ├── db/                 # Supabase session
│   │   │   ├── mcp_server/         # Minari as MCP tool server
│   │   │   ├── repositories/       # Data access layer
│   │   │   ├── schemas/            # Pydantic models
│   │   │   └── services/           # Business logic (delivery, reviewer, etc.)
│   │   ├── scripts/
│   │   │   └── seed_demo_history.py
│   │   └── tests/                  # pytest test suite
│   └── web/                        # Next.js frontend
│       └── src/
│           ├── app/
│           │   ├── page.tsx         # Landing page
│           │   └── dashboard/       # Dashboard + test detail pages
│           ├── components/
│           │   ├── landing/         # Hero, Problem, Features, Architecture...
│           │   ├── dashboard/       # MetricGridLive, ActivityFeed, ForecastPanel
│           │   ├── reasoning/       # ReasoningPanel, EventCard, StageTracker
│           │   ├── fixes/           # FixCandidateCard, DiffView
│           │   ├── delivery/        # MergeRequestCard, ConfidenceCascade
│           │   └── ui/              # GlassCard, Button, SectionHeading
│           └── lib/
│               ├── api.ts           # API client
│               └── types.ts         # Shared TypeScript types
├── infra/
│   └── migrations/                 # Postgres migration files
└── edge/                           # Edge config
```

---

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Clone
```bash
git clone https://github.com/Mizunandayo/minari.git
cd minari
```

### 2. API setup
```bash
cd apps/api
cp .env.example .env
# Fill in your keys: MINARI_GEMINI_API_KEY, MINARI_GITLAB_TOKEN,
# MINARI_DATABASE_URL, MINARI_REDIS_URL
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

### 3. Web setup
```bash
cd apps/web
cp .env.example .env.local
# Set NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
npm install
npm run dev
```

Open http://localhost:3000

### 4. Seed demo data (optional)
```bash
cd apps/api
uv run python scripts/seed_demo_history.py
```

---

## Environment Variables

### API (`apps/api/.env`)
```env
MINARI_ENV=development
MINARI_DEMO_API_KEY=<your-api-key>
MINARI_CORS_ORIGINS=http://localhost:3000

# Database
MINARI_DATABASE_URL=postgresql://...

# Redis
MINARI_REDIS_URL=rediss://...

# GitLab
MINARI_GITLAB_MCP_URL=https://gitlab.com/api/v4/mcp
MINARI_GITLAB_TOKEN=glpat-...
MINARI_DEMO_PROJECT_ID=namespace/project
MINARI_DEMO_TEST_FILE=tests/test_flaky.py

# LLM
MINARI_GEMINI_API_KEY=...

# Demo
MINARI_VALIDATOR_DRY_RUN=false   # true = offline mode, false = live CI
MINARI_MR_TARGET_BRANCH=main
MINARI_DEFAULT_REVIEWER_ID=<gitlab-user-id>
```

### Web (`apps/web/.env.local`)
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## MCP Server

Minari exposes itself as an MCP server so other agents can call it as a tool:

```bash
cd apps/api
uv run python -m app.mcp_server
```

Available tools: `detect`, `diagnose`, `fix`, `verify`

---

## Running Tests

```bash
cd apps/api
uv run pytest tests/ -v
```

---

## Deployment

### Backend — Google Cloud Run
```bash
cd apps/api
gcloud run deploy minari-api \
  --source . \
  --region asia-northeast1 \
  --allow-unauthenticated
```

### Frontend — Vercel
```bash
cd apps/web
vercel --prod
```

Set `NEXT_PUBLIC_API_BASE_URL` to your Cloud Run URL in the Vercel dashboard.

---

## Roadmap

| Phase | Status | Focus |
|---|---|---|
| Phase 1 | ✅ Live | Five-stage pipeline, Python/pytest, GitLab CI, MCP server |
| Phase 2 | Planned | JavaScript/TypeScript/Go, GitHub Actions, org-wide analytics |
| Phase 3 | Planned | Pre-merge flakiness gating, auto-quarantine, prevention |

---

## License

MIT — see [LICENSE](LICENSE)

---

## Acknowledgements

Built with [Gemini 2.5](https://deepmind.google/technologies/gemini/) · [LangGraph](https://langchain-ai.github.io/langgraph/) · [GitLab MCP](https://docs.gitlab.com/ee/user/gitlab_duo/mcp.html) · [Google Cloud Run](https://cloud.google.com/run) · [Supabase](https://supabase.com) · [Upstash Redis](https://upstash.com)

---

*Minari · 実成 · "forming from water" · Built by Francis Daniel Genese for the Google Cloud Rapid Agent Hackathon 2026*
