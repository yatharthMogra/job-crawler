# Career Match AI — Web App

Unified Next.js frontend for job discovery and profile management.

## Backends

- **profile_service** (`:8001`) — candidate signup, resume upload, profile patches
- **recommendation_service** (`:8002`) — job feed, recommendations, pool subscriptions

## Setup

```bash
cp .env.example .env.local
pnpm install
```

## Run locally

```bash
./scripts/dev-profile-service.sh           # :8001
./scripts/dev-recommendation-service.sh    # :8002
./scripts/dev-web.sh                       # :3000
```

Mock mode: `NEXT_PUBLIC_USE_MOCK_DATA=true` in `.env.local`

## Navigation

| Route | Purpose |
|-------|---------|
| `/jobs/recommended` | Personalized job feed |
| `/jobs/liked` | Saved/liked jobs |
| `/jobs/applied` | Applied jobs |
| `/resume` | Resume library |
| `/profile` | Tabbed profile (Personal, Education, Experience, Skills, EEO) |
| `/filters` | Full job criteria editor |
| `/onboarding` | Signup |
| `/profile/upload` → `/profile/review` → `/profile/job-intent` → `/jobs/recommended` | Onboarding flow |

## Role catalog

Users select display labels (e.g. "Full Stack Engineer"); backend maps to ingestion pools via `preferences.role_pool_ids` (e.g. `SWE_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`).
