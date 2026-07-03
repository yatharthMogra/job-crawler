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

Before starting, create accounts and gather credentials:

| Requirement | Purpose |
|---------------|---------|
| [Supabase](https://supabase.com) project | Postgres + Storage for resumes |
| [GCP](https://cloud.google.com) project with billing enabled | Cloud Run + Secret Manager (billing required even for free tier) |
| [Vercel](https://vercel.com) project | Host `web/` frontend |
| [Google AI Studio](https://aistudio.google.com) | Gemini API key (enrichment + resume parsing) |
| Google OAuth credentials | Login via NextAuth |
| Gmail app password | SMTP for notification emails |

**Local tools:**

```bash
./scripts/setup-env.sh
source job-crawler/bin/activate

# macOS
brew install google-cloud-sdk docker
gcloud auth login
gcloud auth application-default login
```

Docker must be running before Cloud Run deploy.

**Recommended setup order:** Supabase → migrations → GCP/Cloud Run → Google OAuth → Vercel → CORS → home machine → verify.

---

## Step-by-step deployment guide

### Phase 0 — Local Python environment

From the repo root:

```bash
./scripts/setup-env.sh
source job-crawler/bin/activate
```

---

### Phase 1 — Supabase

#### 1.1 Create project

1. Supabase dashboard → **New project**
2. Choose a region close to your users (e.g. `us-east-1`)
3. Set and save a strong database password

Note your **project ref** (the subdomain), e.g. `abcdefghij` from `https://abcdefghij.supabase.co`.

#### 1.2 Get connection strings

Go to **Project Settings → Database → Connection string**.

You need **two** URLs. Both must use the `postgresql+asyncpg://` scheme for this codebase.

**A. Direct connection** (migrations + home machine) — port `5432`:

```text
postgresql+asyncpg://postgres.[ref]:[PASSWORD]@db.[ref].supabase.co:5432/postgres
```

**B. Transaction pooler** (Cloud Run) — port `6543`:

```text
postgresql+asyncpg://postgres.[ref]:[PASSWORD]@aws-0-[region].pooler.supabase.com:6543/postgres
```

In the Supabase UI, select **Session mode → Transaction** when copying the pooler string.

If your password contains special characters (`@`, `#`, `%`, etc.), URL-encode them.

Save both URLs — you'll use them in different places:

| Target | URL type |
|--------|----------|
| Alembic migrations | Direct `:5432` |
| Home machine (`job_ingestion`, notification worker) | Direct `:5432` |
| Cloud Run (`profile_service`, `recommendation_service`) | Pooler `:6543` |

#### 1.3 Run database migrations

From repo root with venv activated:

```bash
export DIRECT_URL="postgresql+asyncpg://postgres.[ref]:[PASSWORD]@db.[ref].supabase.co:5432/postgres"

# Order matters — later migrations reference tables from earlier services
DATABASE_URL="$DIRECT_URL" bash -c 'cd profile_service && alembic upgrade head'
DATABASE_URL="$DIRECT_URL" bash -c 'cd job_ingestion && alembic upgrade head'
DATABASE_URL="$DIRECT_URL" bash -c 'cd recommendation_service && alembic upgrade head'
```

Each command should finish without errors. All three services share one Postgres database but use separate Alembic version tables — that is expected.

**Verify:** Supabase → **Table Editor** should show tables such as `companies`, `normalized_jobs`, `candidates`, `user_pool_subscriptions`.

#### 1.4 (Optional) Seed job data

**Option A — Fresh start:** Skip this. After the home machine is running, trigger ingestion (Phase 6) and wait for enrichment to complete.

**Option B — Copy local dev data:** If you have an existing local dump:

```bash
./scripts/export-dev-db.sh   # if you need a fresh export

# Restore to Supabase using pg_restore (use plain postgresql:// URL for pg_restore)
pg_restore --clean --if-exists --no-owner \
  --dbname="postgresql://postgres.[ref]:[PASSWORD]@db.[ref].supabase.co:5432/postgres" \
  exports/your-dump.dump
```

See [`snapshots/README.md`](snapshots/README.md) for dump variants.

#### 1.5 Create Storage bucket

1. Supabase → **Storage** → **New bucket**
2. Name: `resumes`
3. Set to **Private** (not public)
4. No extra RLS policies needed for v1 — `profile_service` uses the service role key, which bypasses RLS

#### 1.6 Note API credentials

From **Project Settings → API**:

| Value | Env var |
|-------|---------|
| Project URL (`https://[ref].supabase.co`) | `SUPABASE_URL` |
| `service_role` key (secret — never expose to frontend) | `SUPABASE_SERVICE_ROLE_KEY` |

---

### Phase 2 — Google Cloud + Cloud Run

#### 2.1 Create GCP project

Project IDs are **globally unique**. Pick any available ID (e.g. `job-crawler-243-55`), not necessarily `job-crawler-prod`:

```bash
gcloud projects create YOUR_PROJECT_ID --name="Job Crawler"
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

Enable billing on the project in the GCP Console, then link it:

```bash
gcloud billing projects link YOUR_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID
```

#### 2.2 Enable APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com
```

#### 2.3 Generate and store secrets

Generate a profile API key:

```bash
openssl rand -hex 32
# Save this — used as PROFILE_API_KEY on Vercel and profile-api-key in GCP
```

Store secrets in Secret Manager:

```bash
PROJECT=YOUR_PROJECT_ID

# Supabase transaction pooler URL (for Cloud Run) — always double-quote; URL-encode special chars in password
echo -n "postgresql+asyncpg://postgres.[ref]:[PASSWORD]@....pooler.supabase.com:6543/postgres" | \
  gcloud secrets create database-url --project=$PROJECT --data-file=-

echo -n "YOUR_GEMINI_API_KEY" | \
  gcloud secrets create gemini-api-key --data-file=-

echo -n "YOUR_PROFILE_API_KEY" | \
  gcloud secrets create profile-api-key --data-file=-

echo -n "https://[ref].supabase.co" | \
  gcloud secrets create supabase-url --data-file=-

echo -n "YOUR_SUPABASE_SERVICE_ROLE_KEY" | \
  gcloud secrets create supabase-service-role-key --data-file=-
```

Grant Cloud Run's default service account access to secrets:

```bash
PROJECT_NUMBER=$(gcloud projects describe $PROJECT --format='value(projectNumber)')
SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

for SECRET in database-url gemini-api-key profile-api-key supabase-url supabase-service-role-key; do
  gcloud secrets add-iam-policy-binding $SECRET \
    --member="serviceAccount:${SA}" \
    --role="roles/secretmanager.secretAccessor"
done
```

#### 2.4 Deploy both services

From repo root (Docker must be running):

```bash
GCP_PROJECT=YOUR_PROJECT_ID GCP_REGION=us-central1 ./scripts/deploy-cloud-run.sh
```

On **Apple Silicon Macs**, the script builds with `--platform linux/amd64` (required for Cloud Run). If deploy fails, see [Troubleshooting](#troubleshooting--lessons-from-first-deploy).

This script:

1. Creates an Artifact Registry repo (if missing)
2. Builds and pushes Docker images for `profile_service` and `recommendation_service`
3. Deploys both to Cloud Run as **`profile-service`** and **`recommendation-service`** with:
   - `min-instances=0`, `max-instances=3`
   - `profile_service`: 1Gi memory, Supabase resume storage enabled
   - `recommendation_service`: 512Mi memory, `ENABLE_NOTIFICATION_SCHEDULER=false`

First deploy may take several minutes.

#### 2.5 Save Cloud Run URLs

```bash
gcloud run services describe profile-service \
  --project=YOUR_PROJECT_ID --region=us-central1 --format='value(status.url)'

gcloud run services describe recommendation-service \
  --project=YOUR_PROJECT_ID --region=us-central1 --format='value(status.url)'
```

Example output:

```text
https://profile-service-xxxxx-uc.a.run.app
https://recommendation-service-xxxxx-uc.a.run.app
```

#### 2.6 Smoke test Cloud Run (before Vercel)

```bash
curl https://profile-service-xxxxx-uc.a.run.app/health
# → {"status":"ok"}

curl https://recommendation-service-xxxxx-uc.a.run.app/health
# → {"status":"ok"}

# Notification endpoint must be disabled on Cloud Run:
curl -X POST https://recommendation-service-xxxxx-uc.a.run.app/notifications/run
# → 404 (expected)
```

The codebase auto-detects Supabase pooler URLs and disables prepared statement caching.

---

### Phase 3 — Google OAuth

Complete this before or immediately after the Vercel deploy — you need the final Vercel URL for redirect URIs.

#### 3.1 OAuth consent screen

1. [Google Cloud Console](https://console.cloud.google.com) → **APIs & Services → OAuth consent screen**
2. Choose **External** (or Internal if using Google Workspace)
3. Fill in app name, support email, developer contact
4. Scopes: `email`, `profile`, `openid` (defaults are sufficient)

#### 3.2 Create OAuth client

1. **Credentials → Create credentials → OAuth client ID**
2. Application type: **Web application**
3. **Authorized redirect URIs:**
   ```text
   https://your-app.vercel.app/api/auth/callback/google
   http://localhost:3000/api/auth/callback/google
   ```
   (Add the localhost URI if you still develop locally with Google login.)
4. Save the **Client ID** and **Client Secret**

#### 3.3 Generate AUTH_SECRET

```bash
openssl rand -base64 32
```

Use this for NextAuth on Vercel (`AUTH_SECRET`).

---

### Phase 4 — Vercel (frontend)

#### 4.1 Connect repository

1. Vercel → **Add New Project**
2. Import your Git repository
3. Set **Root Directory** to `web`
4. Framework preset: Next.js (auto-detected)

#### 4.2 Set environment variables

In Vercel → Project → **Settings → Environment Variables** (Production scope):

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_RECOMMENDATION_API_URL` | Cloud Run recommendation service URL |
| `PROFILE_API_URL` | Cloud Run profile service URL |
| `PROFILE_API_KEY` | Same random key from Phase 2.3 |
| `AUTH_SECRET` | Output of `openssl rand -base64 32` |
| `AUTH_URL` | `https://your-app.vercel.app` |
| `GOOGLE_CLIENT_ID` | From OAuth client |
| `GOOGLE_CLIENT_SECRET` | From OAuth client |
| `NEXT_PUBLIC_USE_MOCK_DATA` | `false` |

Do **not** set `NEXT_PUBLIC_PROFILE_API_URL` in production — profile calls are proxied server-side via `PROFILE_API_URL` and `PROFILE_API_KEY`.

See also [`web/.env.example`](web/.env.example).

#### 4.3 Deploy

Deploy from Vercel. Note your live URL (e.g. `https://career-match-ai.vercel.app`).

#### 4.4 Update OAuth redirect (if needed)

If you created the OAuth client before knowing the Vercel URL, go back to Google Cloud Console and add:

```text
https://career-match-ai.vercel.app/api/auth/callback/google
```

Ensure `AUTH_URL` in Vercel matches this URL exactly.

---

### Phase 5 — Wire CORS

The browser calls the recommendation API directly (`NEXT_PUBLIC_RECOMMENDATION_API_URL`). Without CORS, job pages will fail in the browser.

Update both Cloud Run services after Vercel is live:

```bash
VERCEL_URL="https://your-app.vercel.app"

gcloud run services update profile-service \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --update-env-vars="CORS_ORIGINS=${VERCEL_URL}"

gcloud run services update recommendation-service \
  --project=YOUR_PROJECT_ID \
  --region=us-central1 \
  --update-env-vars="CORS_ORIGINS=${VERCEL_URL}"
```

---

### Phase 6 — Home machine

The home machine runs batch/async work (~22h/day uptime). When it is off, ingestion, enrichment, and emails pause — but the Vercel app and Cloud Run APIs remain available for existing data.

#### 6.1 Python environment

```bash
cd /path/to/job-crawler
./scripts/setup-env.sh
source job-crawler/bin/activate
```

#### 6.2 Configure `job_ingestion/.env`

```bash
cp job_ingestion/.env.example job_ingestion/.env
```

Minimum production values:

```env
DATABASE_URL=postgresql+asyncpg://postgres.[ref]:[PASSWORD]@db.[ref].supabase.co:5432/postgres
# Optional — omit FETCH_SCHEDULE_JSON to use built-in tiered defaults (10 min tick, sharded batches)
# FETCH_SCHEDULE_JSON={"tick_minutes":10,"batch_cap":200,...}
GEMINI_API_KEY=your-gemini-key
# Optional — throttle fetch when enrichment backlog is large (defaults in .env.example)
# FETCH_BACKPRESSURE_ENABLED=true
# FETCH_BACKPRESSURE_QUEUE_THRESHOLD=2000
```

Use the **direct** `:5432` URL, not the pooler.

Watch `GET http://localhost:8000/stats` → `fetch_backpressure.active`. When true, scheduled fetches are skipping tier-3 (or all companies in `halt_all` mode) until pending queue depth drops below the threshold.

#### 6.3 Configure `recommendation_service/.env` (notification worker)

```bash
cp recommendation_service/.env.example recommendation_service/.env
```

```env
DATABASE_URL=postgresql+asyncpg://postgres.[ref]:[PASSWORD]@db.[ref].supabase.co:5432/postgres
ENABLE_NOTIFICATION_SCHEDULER=true
NOTIFICATION_CADENCE_HOURS=24
SMTP_USERNAME=you@gmail.com
SMTP_PASSWORD=your-gmail-app-password
EMAIL_FROM=Career Match AI <you@gmail.com>
APP_BASE_URL=https://your-app.vercel.app
```

**Gmail app password:** Google Account → Security → 2-Step Verification → App passwords → generate one for "Mail".

#### 6.4 Start processes

Use two terminals (or systemd — see Phase 6.6):

```bash
# Terminal 1 — ingestion, enrichment, global scoring, H1B, YC crawl, cleanup
./scripts/run-job-ingestion-prod.sh

# Terminal 2 — scheduled email notifications (localhost only)
./scripts/run-notification-worker.sh
```

Verify locally:

```bash
curl http://localhost:8000/docs     # ingestion API (Swagger)
curl http://localhost:8002/health # notification worker
```

#### 6.5 Trigger first ingestion

```bash
curl -X POST http://localhost:8000/pipeline/trigger
```

Watch the Terminal 1 logs. Enrichment runs in the same process and drains the queue over time. On a fresh database, users won't see jobs until ingestion and enrichment complete.

#### 6.6 Admin dashboard (optional, local only)

```bash
cd job-ingestion-dashboard
npm install
# Optional: .env.local with NEXT_PUBLIC_JOB_INGESTION_API_URL=http://localhost:8000
npm run dev
```

Open `http://localhost:3000` on the home machine.

#### 6.7 Auto-restart with systemd (optional)

Edit paths in [`deploy/systemd/job-ingestion.service`](deploy/systemd/job-ingestion.service) and [`deploy/systemd/recommendation-worker.service`](deploy/systemd/recommendation-worker.service), then:

```bash
sudo cp deploy/systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now job-ingestion recommendation-worker
```

Verify services on the Linux machine:

```bash
./scripts/verify-home-machine.sh
```

#### 6.8 Remote ops from dev machine (Mac)

When ingestion and the notification worker run on the home machine, use an SSH tunnel to reach their APIs from your Mac as if they were local.

**One-time SSH setup**

1. Generate a key on your Mac (skip if you already have one):

   ```bash
   ssh-keygen -t ed25519 -C "mac-to-job-crawler-home"
   ```

2. Install the public key on Linux:

   ```bash
   ssh-copy-id USER@LINUX_HOST
   ```

3. Add a host block to `~/.ssh/config` — see [`deploy/ssh/config.example`](deploy/ssh/config.example). Replace `LINUX_HOST` and `USER`, then test:

   ```bash
   ssh job-crawler-home 'echo ok'
   ```

4. Copy remote ops config:

   ```bash
   cp deploy/home-remote.env.example deploy/home-remote.env
   ```

   Edit `HOME_SSH_HOST` if your SSH alias differs.

**Daily workflow (from repo root on Mac)**

```bash
# Terminal 1 — keep open
./scripts/tunnel-home-services.sh

# Terminal 2 — any of:
./scripts/home-health.sh
./scripts/home-trigger-ingestion.sh
./scripts/home-trigger-notifications.sh
./scripts/dev-ingestion-dashboard.sh   # http://localhost:3000
open http://localhost:8000/docs        # Swagger
```

**Key read endpoints** (via tunnel): `GET /stats`, `GET /pipeline/runs`, `GET /events`, `GET /enrichment/queue`.

**Security:** Do not expose port `8000` to the public internet without authentication. The ingestion API has no auth today; the SSH tunnel is the intended access path.

**Logs on Linux:**

```bash
ssh job-crawler-home 'sudo journalctl -u job-ingestion -f'
ssh job-crawler-home 'sudo journalctl -u recommendation-worker -f'
```

---

### Phase 7 — End-to-end verification

#### Cloud layer

- [ ] `GET /health` on both Cloud Run services returns `{"status":"ok"}`
- [ ] `POST /notifications/run` on Cloud Run returns **404** (scheduler disabled)

#### Auth and profile

- [ ] Open Vercel URL → sign in with Google
- [ ] Complete onboarding / upload a resume
- [ ] Resume appears in Supabase → Storage → `resumes` bucket

#### Jobs and recommendations

- [ ] Home machine ingestion has run; rows exist in Supabase `normalized_jobs`
- [ ] Vercel `/jobs/recommended` loads without CORS errors (check browser DevTools → Network)
- [ ] Personal scores appear (requires profile, jobs, and pool subscriptions)

#### Notifications (home machine must be running)

- [ ] User has active pool subscriptions in the database
- [ ] Manual trigger: `curl -X POST http://localhost:8002/notifications/run`
- [ ] Email arrives; row appears in `notification_batches`

#### Home machine offline

- [ ] Vercel app still loads and shows **existing** jobs
- [ ] No new ingestion or emails while machine is off (expected)

---

## Common gotchas

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| CORS error on job page | Missing `CORS_ORIGINS` on Cloud Run | Phase 5 |
| Google login fails | Wrong redirect URI or `AUTH_URL` | Match Vercel URL exactly in OAuth client + Vercel env |
| Profile API returns 401 | `PROFILE_API_KEY` mismatch | Same key in Vercel and GCP `profile-api-key` secret |
| Resume upload fails on Cloud Run | Storage bucket or service role misconfigured | Check `resumes` bucket exists; verify Supabase secrets |
| Cloud Run DB connection errors | Wrong URL type | Pooler `:6543` on Cloud Run; direct `:5432` on home machine |
| No jobs in the app | Ingestion not run yet | `POST http://localhost:8000/pipeline/trigger` |
| Slow first page load (2–5s) | Cloud Run scale-to-zero cold start | Normal at launch; set `min-instances=1` on recommendation service later |
| Alembic migration fails | Special characters in DB password | URL-encode the password in the connection string |
| Migration FK errors | Wrong migration order | Run `profile_service` → `job_ingestion` → `recommendation_service` |
| `exec format error` on Cloud Run | ARM64 image built on Apple Silicon Mac | Rebuild with `--platform linux/amd64` (see Troubleshooting) |
| Cloud Run name rejected | Underscores in service name | Use `profile-service`, not `profile_service` |
| Deploy script hangs with no output | `gcloud` waiting for `y/N` | Enable APIs with `gcloud services enable ...` first (non-interactive) |
| `Billing account ... not found` | Billing not linked to GCP project | Link billing in GCP Console or `gcloud billing projects link` |
| Root URL returns `Not Found` | No route at `/` | Expected — use `/health` instead |

---

## Troubleshooting — lessons from first deploy

This section captures real failures hit during the initial Cloud Run bring-up. Use it when the happy path above does not work.

### GCP project ID is globally unique

`gcloud projects create job-crawler-prod` may fail with **"Project ID already in use"** even if you never created it — another Google account owns that ID globally.

**Fix:** Pick a unique ID (e.g. `job-crawler-243-55`) and use it consistently for `GCP_PROJECT`, billing, secrets, and deploy commands. Do not assume a name from docs is available.

Verify access:

```bash
gcloud projects describe YOUR_PROJECT_ID
```

Permission denied means the project is not yours.

### Billing must be linked before enabling APIs

```
FAILED_PRECONDITION: Billing account for project '...' is not found
```

Cloud Run, Artifact Registry, and Secret Manager require billing even on the free tier.

**Fix:**

```bash
gcloud billing accounts list
gcloud billing projects link YOUR_PROJECT_ID --billing-account=YOUR_BILLING_ACCOUNT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
```

### gcloud hangs silently (interactive prompts)

If a command prints nothing for minutes, it may be waiting for:

```text
Would you like to enable and retry (this will take a few minutes)? (y/N)?
```

Cursor's integrated terminal and non-interactive scripts cannot answer that prompt.

**Fix:** Run `gcloud services enable ...` explicitly first. Prefer an **external terminal** (Terminal.app, iTerm) for long deploys so you can respond if prompted.

### ADC quota project warning

After `gcloud config set project`, you may see:

```text
Your active project does not match the quota project in your Application Default Credentials file.
```

**Fix:**

```bash
gcloud auth application-default set-quota-project YOUR_PROJECT_ID
```

### Apple Silicon (M1/M2/M3) — build for `linux/amd64`

**Symptom** in Cloud Run logs:

```text
failed to load /bin/sh: exec format error
Application exec likely failed
Default STARTUP TCP probe failed ... on port 8080
```

Docker Desktop on Mac builds **ARM64** images by default. Cloud Run runs **linux/amd64**.

**Fix:** Always build with an explicit platform:

```bash
docker build --platform linux/amd64 \
  --build-arg SERVICE=profile_service \
  -t us-central1-docker.pkg.dev/YOUR_PROJECT/job-crawler/profile_service:latest \
  .
```

Same for `recommendation_service`. The deploy script passes this flag automatically.

### Cloud Run service names use dashes, not underscores

**Symptom:**

```text
Invalid resource name [profile_service]. The name must use only lowercase alphanumeric characters and dashes
```

| Docker image folder | Cloud Run service name |
|---------------------|------------------------|
| `profile_service` | `profile-service` |
| `recommendation_service` | `recommendation-service` |

Image paths in Artifact Registry can keep underscores; only the **Cloud Run service name** must use dashes.

### `deploy-cloud-run.sh` — known issues (manual fallback)

If the script fails, deploy manually. Common script failures we hit:

1. **Multiple secret flags** — `gcloud run deploy` allows only one of `--set-secrets` / `--update-secrets` per command. Merge all secrets into a single `--set-secrets` string.

2. **Wrong project in env** — secrets and billing on `job-crawler-243-55` but `GCP_PROJECT=job-crawler-prod` in the command deploys to a project you do not control.

**Manual deploy — profile-service** (after build + push):

```bash
gcloud run deploy profile-service \
  --project YOUR_PROJECT_ID \
  --region us-central1 \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/job-crawler/profile_service:latest \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 3 \
  --cpu 1 \
  --memory 1Gi \
  --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest,API_KEY=profile-api-key:latest,SUPABASE_URL=supabase-url:latest,SUPABASE_SERVICE_ROLE_KEY=supabase-service-role-key:latest" \
  --set-env-vars "RESUME_STORAGE_BACKEND=supabase,SUPABASE_STORAGE_BUCKET=resumes"
```

**Manual deploy — recommendation-service:**

```bash
gcloud run deploy recommendation-service \
  --project YOUR_PROJECT_ID \
  --region us-central1 \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/job-crawler/recommendation_service:latest \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 3 \
  --cpu 1 \
  --memory 512Mi \
  --set-secrets "DATABASE_URL=database-url:latest,GEMINI_API_KEY=gemini-api-key:latest" \
  --set-env-vars "ENABLE_NOTIFICATION_SCHEDULER=false"
```

Do not paste literal `...` from examples — that is shorthand, not a valid gcloud argument.

### Creating secrets in zsh — quote passwords

**Symptom:** `echo -n postgresql+asyncpg://...password...` splits or errors; password truncated at `&`.

Unquoted passwords with `&`, `,`, `!`, or spaces break zsh.

**Fix:** Always double-quote the full value:

```bash
echo -n "postgresql+asyncpg://postgres.[ref]:[PASSWORD]@....pooler.supabase.com:6543/postgres" | \
  gcloud secrets create database-url --data-file=-
```

URL-encode special characters in the password itself (`&` → `%26`, `,` → `%2C`) inside the connection string.

### Smoke tests — what responses mean

| Request | Expected | Meaning |
|---------|----------|---------|
| `GET /health` | `{"status":"ok"}` | Service is up |
| `GET /` (recommendation-service) | `{"detail":"Not Found"}` | Normal — no root route |
| `POST /notifications/run` on Cloud Run | **404** | Scheduler correctly disabled |
| `POST /notifications/run` on home worker | `{"status":"started"}` | Worker mode |

```bash
gcloud run services describe profile-service \
  --project YOUR_PROJECT_ID --region us-central1 --format='value(status.url)'
```

Use dashed service names in `gcloud run services describe`.

### Secret rotation and redeploy

Rotating a secret in Supabase or Google AI Studio is not enough — update GCP Secret Manager, then **create a new Cloud Run revision** that picks up the new secret version.

```bash
echo -n "NEW_VALUE" | gcloud secrets versions add database-url --project=YOUR_PROJECT_ID --data-file=-
```

**Prefer the deploy script** so secrets, env vars (including CORS), and a fresh Docker image stay in sync:

```bash
GCP_PROJECT=YOUR_PROJECT_ID GCP_REGION=us-central1 ./scripts/deploy-cloud-run.sh
```

The script rebuilds and pushes both service images, then deploys with `--set-secrets` and `--set-env-vars`. It hardcodes production CORS in `scripts/deploy-cloud-run.sh` (`CORS_ORIGINS="https://career-match-gcp.vercel.app"`). The same URL is also in the default allow list in `profile_service/app/config.py` and `recommendation_service/app/config.py`. If your Vercel URL changes, update all three before redeploying.

Manual `gcloud run deploy` works for secret-only rotations (same image is fine), but **must still pass `CORS_ORIGINS`** — otherwise a redeploy can wipe the env var and the browser will only get localhost origins from an older image:

```bash
VERCEL_URL="https://career-match-gcp.vercel.app"

gcloud run deploy profile-service --project YOUR_PROJECT_ID --region us-central1 \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/job-crawler/profile_service:latest \
  --set-secrets "DATABASE_URL=database-url:latest,..." \
  --set-env-vars "RESUME_STORAGE_BACKEND=supabase,SUPABASE_STORAGE_BUCKET=resumes,CORS_ORIGINS=${VERCEL_URL}"

gcloud run deploy recommendation-service --project YOUR_PROJECT_ID --region us-central1 \
  --image us-central1-docker.pkg.dev/YOUR_PROJECT_ID/job-crawler/recommendation_service:latest \
  --set-secrets "DATABASE_URL=database-url:latest,..." \
  --set-env-vars "ENABLE_NOTIFICATION_SCHEDULER=false,CORS_ORIGINS=${VERCEL_URL}"
```

Bare `gcloud run services update profile-service` with no flags errors with **"No configuration change requested"**. Either full `gcloud run deploy` (or `./scripts/deploy-cloud-run.sh`) or add a noop env bump:

```bash
gcloud run services update profile-service --region us-central1 --project=YOUR_PROJECT_ID \
  --update-env-vars="SECRET_ROTATED_AT=$(date +%s)"
```

**Verify CORS after redeploy** — a successful preflight returns **200** and includes `access-control-allow-origin` matching your Vercel URL. **400** with `vary: Origin` but no `access-control-allow-origin` means the origin is not allowed on the running revision (stale image and/or missing `CORS_ORIGINS`):

```bash
curl -sI -X OPTIONS \
  "https://recommendation-service-XXXX.us-central1.run.app/dashboard/jobs/recommended" \
  -H "Origin: https://career-match-gcp.vercel.app" \
  -H "Access-Control-Request-Method: GET"
```

Confirm the env var on the new revision:

```bash
gcloud run services describe recommendation-service \
  --project YOUR_PROJECT_ID --region us-central1 \
  --format='yaml(spec.template.spec.containers[0].env)'
```

Also update Vercel env vars and redeploy the frontend; restart home-machine processes after updating local `.env` files.

### Secrets in terminal logs

Avoid piping raw secrets in **Cursor's integrated terminal** if the session may be logged. Prefer an external terminal for `echo -n "..." | gcloud secrets create`. Rotation invalidates leaked values; closing a terminal tab does not erase history or chat logs.

**Rotate if exposed:** Supabase DB password, Supabase service role key, Gemini API key, profile API key.

### Google OAuth — reuse local client

You do not need a separate OAuth client for production. Add Vercel URLs to the **same** OAuth client used locally:

- Authorized redirect URI: `https://your-app.vercel.app/api/auth/callback/google`
- `AUTH_URL` on Vercel must match exactly

If the consent screen is in **Testing** mode, add each pilot user's Gmail under test users until the app is published.

---

## Quick reference — which URL goes where

| Deployment target | `DATABASE_URL` | Other critical vars |
|-------------------|----------------|---------------------|
| Cloud Run `profile_service` | Pooler `:6543` | `RESUME_STORAGE_BACKEND=supabase`, API/storage secrets |
| Cloud Run `recommendation_service` | Pooler `:6543` | `ENABLE_NOTIFICATION_SCHEDULER=false`, `CORS_ORIGINS` |
| Home `job_ingestion` | Direct `:5432` | `FETCH_SCHEDULE_JSON` (optional), `GEMINI_API_KEYS` |
| Home notification worker | Direct `:5432` | `ENABLE_NOTIFICATION_SCHEDULER=true`, SMTP vars, `APP_BASE_URL` |
| Vercel `web/` | N/A | Cloud Run URLs, OAuth creds, `AUTH_SECRET`, `PROFILE_API_KEY` |

---

## One-time setup (summary)

The phases above expand these five areas:

1. **Supabase** — project, migrations, Storage bucket, API credentials
2. **Cloud Run** — GCP project, secrets, `./scripts/deploy-cloud-run.sh`
3. **Google OAuth** — consent screen, OAuth client, `AUTH_SECRET`
4. **Vercel** — deploy `web/`, set env vars, wire CORS on Cloud Run
5. **Home machine** — `.env` files, `./scripts/run-job-ingestion-prod.sh`, `./scripts/run-notification-worker.sh`

## Environment variable reference

### Home — job_ingestion

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | direct Supabase `:5432` | |
| `FETCH_SCHEDULE_JSON` | (optional JSON blob) | Tiered fetch scheduler: tick interval, batch cap, per-platform/tier intervals, throttles. Built-in defaults when unset. Replaces legacy `FETCH_CADENCE_*`. |
| `JOB_MAX_AGE_DAYS` | `7` | Fresh job window: Workday/Oracle fetch filter, active cleanup, and notification retrieval (must match recommendation service). |
| `GEMINI_API_KEYS` | `key1,key2,...` | Comma-separated keys; one enrichment worker per key |
| `GEMINI_API_KEY` | | Single-key fallback when `GEMINI_API_KEYS` unset |
| `ENRICHMENT_WORKER_COUNT` | (optional) | Cap workers; defaults to key count. Throughput ≈ N × `ENRICHMENT_LLM_MAX_RPM` |

### Home — recommendation worker

| Variable | Example | Notes |
|----------|---------|-------|
| `DATABASE_URL` | direct Supabase `:5432` | |
| `ENABLE_NOTIFICATION_SCHEDULER` | `true` | Must be true on home worker |
| `NOTIFICATION_CADENCE_MINUTES` | `720` | Optional; 12h example |
| `NOTIFICATION_CADENCE_HOURS` | `24` | Fallback when minutes unset |
| `JOB_MAX_AGE_DAYS` | `7` | Must match job_ingestion; limits jobs in email retrieval |
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
| SSH tunnel (Mac → home machine) | `./scripts/tunnel-home-services.sh` |
| Home machine status | `./scripts/home-health.sh` |
| Verify Linux systemd + health | `./scripts/verify-home-machine.sh` (on Linux) |
| Trigger ingestion manually | `./scripts/home-trigger-ingestion.sh` or `POST http://localhost:8000/pipeline/trigger` |
| Trigger notification manually | `./scripts/home-trigger-notifications.sh` or `POST http://localhost:8002/notifications/run` |
| Ops admin dashboard (Mac) | `./scripts/dev-ingestion-dashboard.sh` |
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
- [`scripts/deploy-cloud-run.sh`](scripts/deploy-cloud-run.sh) — `linux/amd64` builds, dashed Cloud Run names, single `--set-secrets`
- [`scripts/run-job-ingestion-prod.sh`](scripts/run-job-ingestion-prod.sh)
- [`scripts/run-notification-worker.sh`](scripts/run-notification-worker.sh)
- [`deploy/systemd/`](deploy/systemd/) — example systemd units

### Tests
- [`job_ingestion/tests/test_cadence_config.py`](job_ingestion/tests/test_cadence_config.py)
- [`recommendation_service/tests/test_cadence_config.py`](recommendation_service/tests/test_cadence_config.py)
- [`profile_service/tests/test_storage.py`](profile_service/tests/test_storage.py)
- Updated [`profile_service/tests/test_extractor.py`](profile_service/tests/test_extractor.py)

### Env templates and docs
- Updated `.env.example` in `job_ingestion/`, `profile_service/`, `recommendation_service/`, `web/`
- [`DEPLOYMENT.md`](DEPLOYMENT.md) — troubleshooting section from first Cloud Run bring-up

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
- [ ] `FETCH_SCHEDULE_JSON` (or defaults) schedules sharded fetch ticks as expected
- [ ] `ENABLE_NOTIFICATION_SCHEDULER=false` skips scheduler; `/notifications/run` returns 404
- [ ] `ENABLE_NOTIFICATION_SCHEDULER=true` sends test email via Gmail
- [ ] Resume upload with `RESUME_STORAGE_BACKEND=local` and `supabase`
- [ ] Pooler URL connects from Cloud Run
- [ ] Vercel frontend loads jobs (CORS verified)
- [ ] All pytest suites pass for touched services
