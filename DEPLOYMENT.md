# Deployment Guide

Hybrid deployment for Career Match AI: cloud services for user-facing sync paths, home machine for batch/async work.

## Architecture

```mermaid
flowchart TB
  subgraph cloud [Cloud - always on]
    Vercel["web/ — Vercel"]
    ProfileAPI["profile_service — Cloud Run"]
    RecoAPI["recommendation_service API — Cloud Run"]
    SupabaseDB[("Supabase Postgres")]
    SupabaseStorage["Supabase Storage"]
  end

  subgraph home [Home machine - ~22h/day]
    JobIngestion["job_ingestion :8000"]
    NotifWorker["recommendation_service worker :8002"]
    AdminDash["job-ingestion-dashboard"]
  end

  Vercel --> ProfileAPI
  Vercel -->|"direct CORS"| RecoAPI
  ProfileAPI --> SupabaseDB
  ProfileAPI --> SupabaseStorage
  RecoAPI --> SupabaseDB
  JobIngestion --> SupabaseDB
  NotifWorker --> SupabaseDB
  AdminDash --> JobIngestion
```

### What runs where

| Component | Location | Purpose |
|-----------|----------|---------|
| **Supabase Postgres** | Cloud | Shared database for all services |
| **Supabase Storage** | Cloud | Resume PDFs (`profile_service` on Cloud Run) |
| **profile_service** | Cloud Run | OAuth-linked profiles, resume upload, constraints |
| **recommendation_service API** | Cloud Run | Job feed, personal scoring, subscriptions (scheduler **off**) |
| **web/** | Vercel | User-facing Next.js app |
| **job_ingestion** | Home machine | Connectors, enrichment, global scoring, H1B, YC crawl, cleanup |
| **recommendation_service worker** | Home machine | Scheduled email notifications via Gmail SMTP |
| **job-ingestion-dashboard** | Home machine | Internal ops UI (localhost only) |

### When the home machine is off (~2h/day)

Users can still log in, browse existing jobs with personal scores, and edit profiles. New job ingestion, enrichment, and email notifications pause until the machine returns.

---

## Prerequisites

- [Supabase](https://supabase.com) project (Postgres + Storage bucket named `resumes`)
- [GCP](https://cloud.google.com) project with Cloud Run and Artifact Registry enabled
- [Vercel](https://vercel.com) project linked to the `web/` directory
- Google OAuth credentials (Google Cloud Console)
- Gmail app password for SMTP notifications
- Gemini API key (local enrichment + cloud resume parsing)

---

## One-time setup

### 1. Supabase database

Run all three Alembic migration chains against your Supabase **direct** connection URL (`db.<ref>.supabase.co:5432`):

```bash
source job-crawler/bin/activate

DATABASE_URL="postgresql+asyncpg://postgres.[ref]:[password]@db.[ref].supabase.co:5432/postgres" \
  bash -c 'cd job_ingestion && alembic upgrade head'

DATABASE_URL="postgresql+asyncpg://postgres.[ref]:[password]@db.[ref].supabase.co:5432/postgres" \
  bash -c 'cd profile_service && alembic upgrade head'

DATABASE_URL="postgresql+asyncpg://postgres.[ref]:[password]@db.[ref].supabase.co:5432/postgres" \
  bash -c 'cd recommendation_service && alembic upgrade head'
```

### 2. Supabase Storage

1. Create a bucket named `resumes` (private).
2. Allow service-role access from `profile_service` (default with service role key).
3. Note `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` from project settings.

### 3. Cloud Run (profile + recommendation API)

Build and deploy using the helper script (requires Docker, gcloud, and Secret Manager secrets):

```bash
# Create secrets (once):
#   database-url       → Supabase transaction pooler URL (:6543)
#   gemini-api-key
#   profile-api-key
#   supabase-url
#   supabase-service-role-key

GCP_PROJECT=your-project GCP_REGION=us-central1 ./scripts/deploy-cloud-run.sh
```

**Connection URLs:**
- **Cloud Run services:** transaction pooler — `...@...pooler.supabase.com:6543/postgres`
- **Home machine:** direct — `...@db.<ref>.supabase.co:5432/postgres`

The codebase auto-detects pooler URLs and disables prepared statement caching.

**Cloud Run settings (applied by deploy script):**
- `min-instances=0`, `max-instances=3`
- `profile_service`: 1Gi memory (PDF parsing)
- `recommendation_service`: `ENABLE_NOTIFICATION_SCHEDULER=false`

### 4. Vercel (frontend)

Deploy the `web/` directory. Set environment variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_RECOMMENDATION_API_URL` | Cloud Run recommendation service URL |
| `PROFILE_API_URL` | Cloud Run profile service URL |
| `PROFILE_API_KEY` | Same as `API_KEY` in profile_service |
| `AUTH_SECRET` | `openssl rand -base64 32` |
| `AUTH_URL` | `https://your-app.vercel.app` |
| `GOOGLE_CLIENT_ID` | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console |

Set `CORS_ORIGINS=https://your-app.vercel.app` on both Cloud Run services.

### 5. Home machine

Copy and configure env files from `.env.example` in each service directory.

Start processes:

```bash
./scripts/run-job-ingestion-prod.sh          # :8000 — ingestion + enrichment
./scripts/run-notification-worker.sh         # :8002 — email scheduler (localhost only)
```

Optional: install systemd units from [`deploy/systemd/`](deploy/systemd/) for auto-restart.

Open admin dashboard when needed:

```bash
cd job-ingestion-dashboard && npm run dev    # → http://localhost:3000
```

---

## Environment variable reference

### Home — job_ingestion

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | direct Supabase `:5432` | |
| `FETCH_CADENCE_MINUTES` | `30` | Overrides `FETCH_CADENCE_HOURS` when set |
| `FETCH_CADENCE_HOURS` | `6` | Fallback when minutes unset |
| `GEMINI_API_KEY` | | Required for enrichment |

### Home — recommendation worker

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | direct Supabase `:5432` | |
| `ENABLE_NOTIFICATION_SCHEDULER` | `true` | Must be true on home worker |
| `NOTIFICATION_CADENCE_MINUTES` | `720` | Optional; 12h example |
| `NOTIFICATION_CADENCE_HOURS` | `24` | Fallback when minutes unset |
| `SMTP_USERNAME` | Gmail address | |
| `SMTP_PASSWORD` | Gmail app password | |
| `APP_BASE_URL` | `https://your-app.vercel.app` | Links in emails |

### Cloud Run — profile_service

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | pooler `:6543` | Via Secret Manager |
| `API_KEY` | | Via Secret Manager |
| `GEMINI_API_KEY` | | Via Secret Manager |
| `RESUME_STORAGE_BACKEND` | `supabase` | |
| `SUPABASE_URL` | | |
| `SUPABASE_SERVICE_ROLE_KEY` | | |
| `SUPABASE_STORAGE_BUCKET` | `resumes` | |
| `CORS_ORIGINS` | Vercel URL | |

### Cloud Run — recommendation_service API

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | pooler `:6543` | Via Secret Manager |
| `ENABLE_NOTIFICATION_SCHEDULER` | `false` | Critical — disables email batch |
| `CORS_ORIGINS` | Vercel URL | Required for browser calls |

### Vercel — web/

See [`web/.env.example`](web/.env.example).

---

## Operational runbook

| Action | Command |
|--------|---------|
| Trigger ingestion manually | `POST http://localhost:8000/pipeline/trigger` |
| Trigger notification manually | `POST http://localhost:8002/notifications/run` (home worker only) |
| View pipeline runs | Admin dashboard → Pipeline tab, or `GET /pipeline/runs` |
| Check recommendation API | `GET https://<reco-api>/health` |
| Check profile API | `GET https://<profile-api>/health` |

---

## Changes log (deployment infrastructure implementation)

### Configuration and scheduling
- [`job_ingestion/app/config.py`](job_ingestion/app/config.py) — added `fetch_cadence_minutes`, `pipeline_interval_kwargs()`
- [`job_ingestion/app/scheduler.py`](job_ingestion/app/scheduler.py) — minute-based pipeline cadence
- [`recommendation_service/app/config.py`](recommendation_service/app/config.py) — added `notification_cadence_minutes`, `enable_notification_scheduler`, `notification_interval_kwargs()`
- [`recommendation_service/app/scheduler.py`](recommendation_service/app/scheduler.py) — minute-based notification cadence
- [`recommendation_service/app/main.py`](recommendation_service/app/main.py) — conditional scheduler startup; gated `/notifications/run`

### Database
- [`job_ingestion/app/database.py`](job_ingestion/app/database.py) — Supabase pooler detection
- [`profile_service/app/database.py`](profile_service/app/database.py) — same
- [`recommendation_service/app/database.py`](recommendation_service/app/database.py) — same

### Resume storage
- [`profile_service/app/storage/`](profile_service/app/storage/) — local + Supabase backends
- [`profile_service/app/api/candidates.py`](profile_service/app/api/candidates.py) — upload via storage abstraction
- [`profile_service/app/pipeline/extractor.py`](profile_service/app/pipeline/extractor.py) — bytes-based PDF extraction
- [`profile_service/app/pipeline/patch_engine.py`](profile_service/app/pipeline/patch_engine.py) — read resume via storage

### Deployment artifacts
- [`Dockerfile`](Dockerfile) — multi-service Cloud Run build
- [`.dockerignore`](.dockerignore)
- [`scripts/deploy-cloud-run.sh`](scripts/deploy-cloud-run.sh)
- [`scripts/run-job-ingestion-prod.sh`](scripts/run-job-ingestion-prod.sh)
- [`scripts/run-notification-worker.sh`](scripts/run-notification-worker.sh)
- [`deploy/systemd/`](deploy/systemd/) — example systemd units

### Tests
- [`job_ingestion/tests/test_cadence_config.py`](job_ingestion/tests/test_cadence_config.py)
- [`recommendation_service/tests/test_cadence_config.py`](recommendation_service/tests/test_cadence_config.py)
- [`profile_service/tests/test_storage.py`](profile_service/tests/test_storage.py)
- Updated [`profile_service/tests/test_extractor.py`](profile_service/tests/test_extractor.py)

### Env templates
- Updated `.env.example` in `job_ingestion/`, `profile_service/`, `recommendation_service/`, `web/`

---

## Future scope

| Milestone | Trigger | Likely changes |
|-----------|---------|----------------|
| **Cold start UX** | 10–50 active users report slow first load | Set `min-instances=1` on recommendation Cloud Run |
| **Recommendation API auth** | Opening beyond pilot | Session token or API key on `/dashboard/*` |
| **Email deliverability** | ~100+ users | SendGrid/Resend/Postmark; unsubscribe UX |
| **Resume storage scale** | Many large PDFs | Review Supabase Storage quotas; lifecycle rules |
| **Ingestion reliability** | Home downtime hurts freshness | Cloud Scheduler + Cloud Run Job for ingestion only |
| **DB tier** | Connection limits or size on free tier | Supabase Pro |
| **CI/CD** | Frequent deploys | GitHub Actions for test + deploy |
| **Observability** | Production debugging | Cloud Logging, pipeline/enrichment alerts |
| **Multi-home HA** | Second machine | DB-backed leader lock before dual ingestion |
| **IaC** | Team grows | Terraform for Supabase + Cloud Run + Vercel |

---

## Verification checklist

- [ ] Local dev works with docker-compose Postgres (default env files)
- [ ] `FETCH_CADENCE_MINUTES=30` schedules pipeline as expected
- [ ] `ENABLE_NOTIFICATION_SCHEDULER=false` skips scheduler; `/notifications/run` returns 404
- [ ] `ENABLE_NOTIFICATION_SCHEDULER=true` sends test email via Gmail
- [ ] Resume upload with `RESUME_STORAGE_BACKEND=local` and `supabase`
- [ ] Pooler URL connects from Cloud Run
- [ ] Vercel frontend loads jobs (CORS verified)
- [ ] All pytest suites pass for touched services
