# Career Match AI — Web App

Unified Next.js frontend for job discovery and profile review. Talks to:

- **profile_service** (`:8001`) — candidate signup, resume upload, profile patches
- **recommendation_service** (`:8002`) — job feed, recommendations, pool subscriptions

## Setup

```bash
cp .env.example .env.local
# Edit .env.local with your profile API key
pnpm install
```

## Run locally

Start both backends, then the web app:

```bash
./scripts/dev-profile-service.sh           # :8001
./scripts/dev-recommendation-service.sh    # :8002
./scripts/dev-web.sh                       # :3000
```

Or from this directory:

```bash
pnpm dev
```

## Session

Identity is stored in `localStorage` as `profile_candidate_id` (UUID from `POST /candidates`). No password auth in V1.

## Routes

| Route | Purpose |
|-------|---------|
| `/onboarding` | Name + email signup |
| `/profile/upload` | Resume PDF upload |
| `/profile/processing` | Analysis in progress |
| `/profile/review` | Approve/reject patch operations |
| `/profile/confirm` | Post-commit summary |
| `/jobs` | All jobs feed |
| `/recommended` | Personal-score ranked feed |
| `/saved` / `/applied` | Client-only state (localStorage) |
| `/profile` | Profile home |
| `/preferences` | Edit constraints & preferences |

Root `/` redirects based on session state (onboarding → upload → review → jobs).

## Mock mode

Set `NEXT_PUBLIC_USE_MOCK_DATA=true` to use static job data without backends.
