# Profile Review UX — Integration Testing

## Prerequisites

1. Postgres running (`cd ../job_ingestion && docker compose up -d postgres`)
2. Profile service on port 8001 (`cd ../profile_service && uvicorn app.main:app --port 8001 --reload`)
3. Frontend env configured

## Setup

```bash
cd profile-review-ux
cp .env.local.example .env.local
pnpm install
pnpm dev --port 3001
```

`.env.local`:

```env
NEXT_PUBLIC_PROFILE_API_URL=http://localhost:8001
NEXT_PUBLIC_PROFILE_API_KEY=dev-key-change-me
NEXT_PUBLIC_USE_MOCK_DATA=false
```

For UI-only development without backend:

```env
NEXT_PUBLIC_USE_MOCK_DATA=true
```

## Manual test flow

1. Open http://localhost:3001
2. **Onboarding** — enter name + email → creates candidate, stores ID in localStorage
3. **Upload** — select PDF → processing screen waits on real upload API
4. **Review** — approve/reject proposed changes from pending patch
5. **Save** — commits approved operation IDs → confirmation with API capabilities
6. **Profile home** — shows candidate name, constraints, preferences, evidence, capabilities
7. **Edit** — use Edit on Constraints/Preferences sections → PATCH endpoints
8. **Re-upload** — upload new resume; if pending patch exists, redirects to review

## Return visit

Refresh the page with a stored candidate_id:

- Profile exists → lands on Profile Home
- No profile → lands on Upload

## Clear session

```js
localStorage.removeItem('profile_candidate_id')
```
