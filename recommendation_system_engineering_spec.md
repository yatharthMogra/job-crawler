# Job Recommendation System — Engineering Specification (V1)

---

## 1. What This Covers

This spec covers two things:

**Part A — Job Ingestion Pipeline Extensions**
New fields and computation added to the existing `job_ingestion` service to support recommendation. These run at ingestion time, once per job.

**Part B — Recommendation Service**
A new standalone FastAPI service responsible for:
- User pool subscriptions
- Dashboard job retrieval
- Periodic personalized notification generation
- Email delivery

---

## 2. Shared Taxonomy (Source of Truth)

Both jobs and users reference the same controlled lists. These are defined once and shared across services.

### Normalized Role Taxonomy

```python
NORMALIZED_ROLES = [
    "SWE",
    "BACKEND_ENGINEER",
    "FRONTEND_ENGINEER",
    "FULLSTACK_ENGINEER",
    "ML_ENGINEER",
    "DATA_ENGINEER",
    "DATA_SCIENTIST",
    "DEVOPS_ENGINEER",
    "SECURITY_ENGINEER",
    "MOBILE_ENGINEER",
    "PRODUCT_MANAGER",
    "OTHER",
]
```

### Capability Taxonomy (same as profile system)

```python
CAPABILITY_TAXONOMY = [
    "Backend Engineering",
    "Frontend Engineering",
    "Full Stack Development",
    "AI Systems",
    "Machine Learning",
    "Machine Learning Research",
    "Data Engineering",
    "Distributed Systems",
    "Cloud Infrastructure",
    "Platform Engineering",
    "DevOps",
    "Product Engineering",
    "Mobile Development",
    "Security Engineering",
    "Analytics Engineering",
    "Research",
]
```

### Retrieval Pool Convention

Pools are derived strings, never stored in a separate table.

Format: `{NORMALIZED_ROLE}_{ROLE_TYPE}`

Examples:
```
SWE_INTERNSHIP
BACKEND_ENGINEER_FULLTIME
ML_ENGINEER_INTERNSHIP
DATA_SCIENTIST_FULLTIME
```

A job may belong to multiple pools. A user subscribes to one or more pools.

---

# PART A — Job Ingestion Pipeline Extensions

---

## 3. What Changes in the Ingestion Pipeline

The existing enrichment pipeline already extracts:
- seniority, is_internship, is_new_grad
- sponsorship_status, sponsorship_confidence
- remote_type, tech_stack, skills

Three new fields are added to LLM extraction:
1. `normalized_roles` — which roles from the taxonomy this job maps to
2. `job_capabilities` — which capabilities from the taxonomy this job requires
3. `application_effort` — how much effort the application requires

Two new fields are computed deterministically post-extraction:
4. `retrieval_pools` — derived from normalized_roles + role_type
5. `opportunity_score` — shared ranking signal

---

## 4. Schema Changes to Job Ingestion

### `job_enrichments` table — new columns

| Column | Type | Notes |
|---|---|---|
| normalized_roles | VARCHAR[] | From NORMALIZED_ROLES taxonomy |
| job_capabilities | VARCHAR[] | From CAPABILITY_TAXONOMY |
| application_effort | VARCHAR | "LOW" / "MEDIUM" / "HIGH" |
| retrieval_pools | VARCHAR[] | Derived: role + role_type combos |
| opportunity_score | FLOAT | Computed deterministically |
| opportunity_score_computed_at | TIMESTAMP | |

GIN index on `retrieval_pools` for fast pool-based queries.
GIN index on `normalized_roles` for filtering.
GIN index on `job_capabilities` for capability overlap queries.

**New Alembic migration:** `YYYYMMDD_XXXX_recommendation_enrichment_fields.py`

---

## 5. Updated LLM Extraction Schema

Add to the existing `JobEnrichment` Pydantic model:

```python
from typing import Literal
from pydantic import BaseModel

NormalizedRole = Literal[
    "SWE", "BACKEND_ENGINEER", "FRONTEND_ENGINEER", "FULLSTACK_ENGINEER",
    "ML_ENGINEER", "DATA_ENGINEER", "DATA_SCIENTIST", "DEVOPS_ENGINEER",
    "SECURITY_ENGINEER", "MOBILE_ENGINEER", "PRODUCT_MANAGER", "OTHER",
]

CapabilityName = Literal[
    "Backend Engineering", "Frontend Engineering", "Full Stack Development",
    "AI Systems", "Machine Learning", "Machine Learning Research",
    "Data Engineering", "Distributed Systems", "Cloud Infrastructure",
    "Platform Engineering", "DevOps", "Product Engineering",
    "Mobile Development", "Security Engineering", "Analytics Engineering",
    "Research",
]

ApplicationEffort = Literal["LOW", "MEDIUM", "HIGH"]

# Added to existing JobEnrichment:
class JobEnrichmentV2(BaseModel):
    # ... existing fields ...
    normalized_roles: list[NormalizedRole]
    job_capabilities: list[CapabilityName]
    application_effort: ApplicationEffort
```

**Application effort guidance for LLM prompt:**
```
application_effort rules:
- LOW: one-click apply, resume upload only, no cover letter required
- MEDIUM: resume + standard questions, short cover letter optional
- HIGH: cover letter required, portfolio required, screening questions,
         multi-step application form
```

**Normalized roles guidance:**
```
normalized_roles rules:
- Assign ALL applicable roles from the taxonomy, not just the primary one
- A "ML Infrastructure Engineer" gets both ML_ENGINEER and BACKEND_ENGINEER
- When uncertain, assign OTHER rather than forcing an incorrect role
- Never assign roles not in the taxonomy
```

---

## 6. Retrieval Pool Assignment (Deterministic)

Computed immediately after LLM extraction succeeds. No LLM involved.

```python
# ingestion/recommendation_fields.py

def assign_retrieval_pools(
    normalized_roles: list[str],
    is_internship: bool,
    is_new_grad: bool,
) -> list[str]:
    role_type = _resolve_role_type(is_internship, is_new_grad)
    pools = []
    for role in normalized_roles:
        pools.append(f"{role}_{role_type}")
    return pools

def _resolve_role_type(is_internship: bool, is_new_grad: bool) -> str:
    if is_internship:
        return "INTERNSHIP"
    if is_new_grad:
        return "NEW_GRAD"
    return "FULLTIME"
```

Example:
```
normalized_roles: [ML_ENGINEER, BACKEND_ENGINEER]
is_internship: true
→ retrieval_pools: [ML_ENGINEER_INTERNSHIP, BACKEND_ENGINEER_INTERNSHIP]
```

---

## 7. Opportunity Score Computation (Deterministic)

Computed once per job after enrichment. Shared globally — not personalized.

```python
# ingestion/recommendation_fields.py

import math
from datetime import datetime, timezone

FRESHNESS_WEIGHT = 0.40
COMPENSATION_WEIGHT = 0.40
EFFORT_WEIGHT = 0.20

EFFORT_SCORES = {
    "LOW": 1.0,
    "MEDIUM": 0.6,
    "HIGH": 0.2,
}

# Compensation normalization anchors (annual salary)
COMP_FLOOR = 40_000
COMP_CEILING = 250_000

def compute_opportunity_score(
    posted_at: datetime,
    salary_min: int | None,
    salary_max: int | None,
    application_effort: str,
) -> float:
    freshness = _freshness_score(posted_at)
    compensation = _compensation_score(salary_min, salary_max)
    effort = EFFORT_SCORES.get(application_effort, 0.5)

    return round(
        FRESHNESS_WEIGHT * freshness
        + COMPENSATION_WEIGHT * compensation
        + EFFORT_WEIGHT * effort,
        4,
    )

def _freshness_score(posted_at: datetime) -> float:
    """Exponential decay. Score = 1.0 at posting, ~0.5 at 72 hours."""
    now = datetime.now(timezone.utc)
    hours_old = (now - posted_at).total_seconds() / 3600
    return math.exp(-0.01 * hours_old)  # decay constant tunable via config

def _compensation_score(salary_min: int | None, salary_max: int | None) -> float:
    """Normalize midpoint against anchors. Returns 0.0–1.0."""
    if salary_min is None and salary_max is None:
        return 0.5  # unknown compensation → neutral
    midpoint = (salary_min or salary_max) if not (salary_min and salary_max) \
               else (salary_min + salary_max) / 2
    clamped = max(COMP_FLOOR, min(COMP_CEILING, midpoint))
    return (clamped - COMP_FLOOR) / (COMP_CEILING - COMP_FLOOR)
```

---

## 8. Ingestion Pipeline Integration Points

The enrichment pipeline already has a step sequence. Two new steps are appended after LLM enrichment succeeds:

```
[existing] LLM enrichment → write job_enrichments row
    ↓
[NEW] assign_retrieval_pools() → write retrieval_pools to job_enrichments
    ↓
[NEW] compute_opportunity_score() → write opportunity_score to job_enrichments
```

If LLM enrichment fails (processing_state = partial_success), retrieval pools and opportunity score are NOT computed — the job is invisible to the recommendation system until reprocessed.

---

# PART B — Recommendation Service

---

## 9. Service Overview

A new standalone FastAPI service. Shares the same PostgreSQL instance.

**Two responsibilities:**
1. **Dashboard API** — fast interactive job retrieval for users
2. **Notification Scheduler** — periodic personalized email generation

Both live in the same FastAPI app for V1. Can be split later.

---

## 10. Database Schema (New Tables)

### `user_pool_subscriptions`

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| pool_name | VARCHAR | e.g. "ML_ENGINEER_INTERNSHIP" |
| is_active | BOOLEAN | |
| created_at | TIMESTAMP | |

Unique constraint on `(candidate_id, pool_name)`.

---

### `notification_batches`

One row per notification send attempt per user.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| triggered_at | TIMESTAMP | When scheduler fired |
| sent_at | TIMESTAMP | nullable — when email was sent |
| status | VARCHAR | "pending / sent / failed / skipped" |
| jobs_in_pools | INTEGER | Jobs found in user's pools |
| jobs_after_filter | INTEGER | After constraint SQL filters |
| jobs_new_since_last | INTEGER | After deduplication against history |
| jobs_ranked | INTEGER | Candidate set for personalized ranking |
| jobs_sent | INTEGER | Actual jobs in email (max 4) |
| skip_reason | VARCHAR | nullable — "no_new_jobs" / "email_failed" |
| email_delivered | BOOLEAN | |
| created_at | TIMESTAMP | |

---

### `notification_job_history`

One row per job per user per batch. Permanent record of what was sent.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| batch_id | UUID FK → notification_batches | |
| job_id | UUID FK → normalized_jobs | |
| rank_in_batch | INTEGER | 1–4 |
| recommendation_score | FLOAT | Personalized score at time of send |
| explanation | VARCHAR[] | Match reason strings shown in email |
| created_at | TIMESTAMP | |

Unique constraint on `(candidate_id, job_id)` — ensures a job is never sent twice to the same user.

---

## 11. Project Structure

```
recommendation_service/
├── pyproject.toml
├── .env
├── .env.example
├── alembic/
│   └── versions/
│
└── app/
    ├── main.py                    # FastAPI app + lifespan + scheduler start
    ├── config.py                  # pydantic-settings
    ├── database.py                # async engine, session factory
    ├── scheduler.py               # APScheduler — notification job
    │
    ├── models/
    │   ├── subscription.py        # user_pool_subscriptions
    │   ├── notification.py        # notification_batches + notification_job_history
    │   └── shared.py             # read-only models for normalized_jobs, candidates
    │
    ├── schemas/
    │   ├── dashboard.py
    │   ├── subscription.py
    │   └── notification.py
    │
    ├── api/
    │   ├── dashboard.py           # job retrieval endpoints
    │   └── subscriptions.py       # user subscription management
    │
    ├── scoring/
    │   ├── opportunity.py         # shared opportunity score (read from DB)
    │   ├── recommendation.py      # personalized scoring
    │   └── explainability.py      # match explanation generation
    │
    ├── notification/
    │   ├── pipeline.py            # per-user notification orchestrator
    │   ├── retrieval.py           # pool query + SQL filtering
    │   ├── ranker.py              # personalized ranking
    │   ├── sender.py              # SMTP email sender
    │   └── renderer.py            # Jinja2 HTML template rendering
    │
    ├── templates/
    │   └── daily_briefing.html    # Email HTML template
    │
    └── constants.py               # shared taxonomy lists
```

---

## 12. Dashboard API

### Endpoints

```
GET  /dashboard/jobs                    # retrieve jobs from user's pools
GET  /dashboard/jobs/{job_id}           # single job detail
POST /subscriptions                     # subscribe user to pools
GET  /subscriptions/{candidate_id}      # get user's pool subscriptions
PATCH /subscriptions/{candidate_id}     # update subscriptions
```

### Dashboard Retrieval Flow

`GET /dashboard/jobs?candidate_id={id}&location=&remote=&salary_min=&role_type=&limit=50&offset=0`

```python
# api/dashboard.py

async def get_dashboard_jobs(candidate_id, filters, db):
    # Step 1: get user's active pool subscriptions
    pools = await get_active_pools(candidate_id, db)
    if not pools:
        return []

    # Step 2: query jobs in those pools with SQL filters
    jobs = await query_jobs_in_pools(pools, filters, db)

    # Step 3: sort by shared opportunity_score DESC
    # (already computed at ingestion time — no computation here)
    return jobs
```

**Core SQL (via SQLAlchemy):**
```sql
SELECT nj.*, je.*
FROM normalized_jobs nj
JOIN job_enrichments je ON je.normalized_job_id = nj.id
WHERE je.retrieval_pools && ARRAY[:pools]     -- GIN index hit
  AND nj.is_active = true
  AND nj.processing_state = 'success'
  AND (:location IS NULL OR nj.location ILIKE :location)
  AND (:salary_min IS NULL OR je.salary_min >= :salary_min)
  AND (:remote_type IS NULL OR je.remote_type = :remote_type)
ORDER BY je.opportunity_score DESC
LIMIT :limit OFFSET :offset
```

The dashboard never computes anything at retrieval time. It reads and filters pre-computed scores.

---

## 13. Notification Pipeline

### Trigger

APScheduler fires every `NOTIFICATION_CADENCE_HOURS` (default: 3, configurable).

One scheduler job loops over all active candidates with subscriptions.

```python
# scheduler.py
scheduler.add_job(
    run_notification_pipeline,
    trigger="interval",
    hours=settings.notification_cadence_hours,
    id="notification_pipeline",
)
```

---

### Per-User Notification Flow

```python
# notification/pipeline.py

async def run_notification_for_user(candidate_id, db):
    # Step 1: create pending batch record
    batch = await create_batch(candidate_id, db)

    # Step 2: get user's subscribed pools
    pools = await get_active_pools(candidate_id, db)
    if not pools:
        await skip_batch(batch, "no_pool_subscriptions", db)
        return

    # Step 3: get last notification time
    last_notified_at = await get_last_notification_time(candidate_id, db)

    # Step 4: retrieve jobs in pools, ingested after last_notified_at
    candidate_jobs = await retrieval.fetch_new_jobs_in_pools(
        pools=pools,
        since=last_notified_at,
        db=db,
    )

    await update_batch(batch, jobs_in_pools=len(candidate_jobs), db=db)

    if not candidate_jobs:
        await skip_batch(batch, "no_new_jobs", db)
        return

    # Step 5: apply hard constraint filters (SQL)
    user_profile = await get_candidate_profile(candidate_id, db)
    filtered_jobs = retrieval.apply_constraint_filters(candidate_jobs, user_profile)

    await update_batch(batch, jobs_after_filter=len(filtered_jobs), db=db)

    if not filtered_jobs:
        await skip_batch(batch, "no_jobs_after_filter", db)
        return

    # Step 6: personalized ranking
    ranked_jobs = ranker.rank(filtered_jobs, user_profile)

    # Step 7: select top 4
    top_jobs = ranked_jobs[:4]

    # Step 8: generate explanations
    jobs_with_explanations = [
        (job, explainability.generate(job, user_profile))
        for job in top_jobs
    ]

    # Step 9: render email
    html = renderer.render(jobs_with_explanations, user_profile)

    # Step 10: send email
    delivered = await sender.send(
        to=user_profile.email,
        subject="Your job opportunities — Career Match AI",
        html=html,
    )

    # Step 11: record history
    for rank, (job, explanation) in enumerate(jobs_with_explanations, start=1):
        await record_job_sent(candidate_id, batch.id, job.id, rank, explanation, db)

    await finalize_batch(batch, sent=delivered, jobs_sent=len(top_jobs), db=db)
```

---

### Retrieval Query (Notification)

```python
# notification/retrieval.py

async def fetch_new_jobs_in_pools(pools, since, db):
    """
    Fetch jobs that:
    - are in user's pools
    - were ingested after the user's last notification
    - have NOT been sent to this user before
    - are active and fully processed
    """
    # SQL:
    # WHERE je.retrieval_pools && ARRAY[:pools]
    # AND nj.is_active = true
    # AND nj.processing_state = 'success'
    # AND je.opportunity_score IS NOT NULL
    # AND nj.created_at > :since
    # AND nj.id NOT IN (
    #     SELECT job_id FROM notification_job_history
    #     WHERE candidate_id = :candidate_id
    # )
    # ORDER BY je.opportunity_score DESC
    # LIMIT 50   ← cap retrieval set
```

---

### Constraint Filters (Hard Filters, Deterministic)

```python
# notification/retrieval.py

def apply_constraint_filters(jobs, user_profile):
    constraints = user_profile.constraints
    filtered = []
    for job in jobs:
        enrichment = job.enrichment

        # Sponsorship: if user requires sponsorship, job must indicate yes/unclear
        if constraints.sponsorship_required:
            if enrichment.sponsorship_status == "no":
                continue

        # Role type: internship_only or fulltime_only
        if constraints.internship_only and not enrichment.is_internship:
            continue
        if constraints.fulltime_only and enrichment.is_internship:
            continue

        # Minimum salary
        if constraints.minimum_salary and enrichment.salary_max:
            if enrichment.salary_max < constraints.minimum_salary:
                continue

        filtered.append(job)
    return filtered
```

---

## 14. Personalized Ranking

```python
# scoring/recommendation.py

CAPABILITY_WEIGHT = 0.40
SKILL_WEIGHT = 0.25
LOCATION_WEIGHT = 0.20
COMPENSATION_WEIGHT = 0.15

def score(job, user_profile) -> float:
    cap_score = _capability_overlap(
        job.enrichment.job_capabilities,
        user_profile.capabilities,
    )
    skill_score = _skill_overlap(
        job.enrichment.tech_stack + job.enrichment.skills,
        user_profile.skills,
    )
    loc_score = _location_alignment(
        job.location,
        job.enrichment.remote_type,
        user_profile.preferences,
    )
    comp_score = _compensation_alignment(
        job.enrichment.salary_min,
        job.enrichment.salary_max,
        user_profile.constraints,
    )

    return (
        CAPABILITY_WEIGHT * cap_score
        + SKILL_WEIGHT * skill_score
        + LOCATION_WEIGHT * loc_score
        + COMPENSATION_WEIGHT * comp_score
    )

def _capability_overlap(job_caps, user_caps) -> float:
    """Jaccard-like: intersection / user capability count."""
    if not user_caps:
        return 0.0
    user_cap_names = {c.capability_name for c in user_caps}
    overlap = len(set(job_caps) & user_cap_names)
    return overlap / len(user_cap_names)

def _skill_overlap(job_skills, user_skills) -> float:
    """Normalized intersection count."""
    if not user_skills:
        return 0.0
    all_user_skills = _flatten_skills(user_skills)
    job_skills_normalized = {s.lower() for s in job_skills}
    user_skills_normalized = {s.lower() for s in all_user_skills}
    overlap = len(job_skills_normalized & user_skills_normalized)
    return min(overlap / max(len(user_skills_normalized), 1), 1.0)

def _location_alignment(job_location, remote_type, preferences) -> float:
    if remote_type == "remote":
        if "Remote" in preferences.preferred_locations:
            return 1.0
        return 0.7  # remote is still flexible

    for loc in preferences.preferred_locations:
        if loc.lower() in (job_location or "").lower():
            return 1.0
    for loc in preferences.acceptable_locations:
        if loc.lower() in (job_location or "").lower():
            return 0.5
    return 0.0

def _compensation_alignment(salary_min, salary_max, constraints) -> float:
    if not constraints.minimum_salary and not constraints.minimum_hourly_rate:
        return 0.5  # no preference stated → neutral
    if salary_max is None:
        return 0.5  # unknown compensation → neutral
    if constraints.minimum_salary and salary_max >= constraints.minimum_salary:
        return 1.0
    return 0.2
```

---

## 15. Explainability

Generated deterministically. No LLM.

```python
# scoring/explainability.py

def generate(job, user_profile) -> list[str]:
    """
    Returns 3–5 strings explaining why this job matches this user.
    Shown in email as profile match bullets.
    Example: ["Walmart backend experience", "AWS", "RAG Systems"]
    """
    reasons = []

    # Matching capabilities
    user_cap_names = {c.capability_name for c in user_profile.capabilities}
    for cap in job.enrichment.job_capabilities:
        if cap in user_cap_names:
            reasons.append(cap)

    # Matching skills (top 3)
    all_user_skills = _flatten_skills(user_profile.skills)
    user_skills_lower = {s.lower(): s for s in all_user_skills}
    for skill in job.enrichment.tech_stack:
        if skill.lower() in user_skills_lower:
            reasons.append(skill)
        if len(reasons) >= 5:
            break

    # Matching evidence keywords (from experiences/projects)
    if len(reasons) < 3:
        user_keywords = _collect_evidence_keywords(user_profile.evidence)
        for kw in job.enrichment.skills:
            if kw.lower() in {k.lower() for k in user_keywords}:
                reasons.append(kw)
            if len(reasons) >= 5:
                break

    return reasons[:5]
```

---

## 16. Email Template

Rendered via Jinja2. HTML email matching the daily briefing format.

Each job block contains:
- Job title (large, linked to posting URL)
- Company name
- Salary range (if available)
- Location + remote type
- Posted X ago / Detected Y after posting
- Application effort badge (Quick Apply / Standard / Detailed)
- Profile Match section: list of explanation strings
- "Apply Now" button

Footer:
- "Why only N jobs? We scanned X total. We recommended N because they offered the strongest combination of relevance, freshness, and application efficiency."
- Manage preferences link (future)
- Unsubscribe link (future)

---

## 17. Email Sending

V1 uses SMTP. Configurable credentials.

```python
# notification/sender.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def send(to: str, subject: str, html: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            if settings.smtp_use_tls:
                server.starttls()
            if settings.smtp_username:
                server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.email_from, [to], msg.as_string())
        return True
    except Exception as e:
        log.error("email_send_failed", to=to, error=str(e))
        return False
```

---

## 18. Configuration

### Job Ingestion additions (`.env`)
```
# Recommendation enrichment
OPPORTUNITY_SCORE_FRESHNESS_DECAY=0.01    # decay constant for freshness score
COMP_FLOOR=40000
COMP_CEILING=250000
```

### Recommendation Service (`.env`)
```
# Database (shared instance)
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion

# Notification scheduling
NOTIFICATION_CADENCE_HOURS=3

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=your@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=Career Match AI <your@gmail.com>

# Scoring weights (all must sum to 1.0)
SCORE_CAPABILITY_WEIGHT=0.40
SCORE_SKILL_WEIGHT=0.25
SCORE_LOCATION_WEIGHT=0.20
SCORE_COMPENSATION_WEIGHT=0.15

# Logging
LOG_LEVEL=INFO
```

---

## 19. Build Sequence

**Part A — Ingestion Extensions (do first)**

1. New Alembic migration: add recommendation fields to `job_enrichments`
2. Update `JobEnrichment` Pydantic model with new fields
3. Update LLM extraction prompt with normalized_roles, capabilities, application_effort guidance
4. Implement `assign_retrieval_pools()` and `compute_opportunity_score()`
5. Wire into enrichment pipeline after LLM extraction step
6. Validate on existing 12 companies — confirm pools and scores are populated
7. Add GIN indexes on `retrieval_pools`, `job_capabilities`, `normalized_roles`

**Part B — Recommendation Service**

8. Project scaffold, models, Alembic migrations
9. Subscription API endpoints
10. Dashboard retrieval API
11. `scoring/recommendation.py` — unit test scoring functions in isolation
12. `scoring/explainability.py` — unit test explanation generation
13. `notification/retrieval.py` — pool query + constraint filter
14. `notification/ranker.py` — ranking pipeline
15. `notification/renderer.py` — Jinja2 email template
16. `notification/sender.py` — SMTP sender
17. `notification/pipeline.py` — full per-user orchestration
18. APScheduler wiring
19. End-to-end validation with 2 seed user profiles against live job data

---

## 20. Key Design Rules

- **Opportunity score is computed at ingestion time.** Dashboard and notification never recompute it.
- **Notification only considers jobs newer than the user's last notification.** Never re-sends a job. `notification_job_history` is the deduplication source.
- **Hard constraint filters are SQL-layer, not Python-layer.** Sponsorship, role type, salary minimum — eliminated before the candidate set reaches the ranking function.
- **Personalized ranking operates on a small candidate set (≤50 jobs).** The retrieval cap prevents runaway computation.
- **Explainability is deterministic.** Generated from structured field intersections. No LLM at notification time.
- **Scoring weights are configurable.** Stored in `.env`, not hardcoded. Tuning happens without a code change.
- **If a job's enrichment failed (no opportunity_score), it is invisible to recommendation.** Incomplete jobs never surface to users.
- **A job is never sent to the same user twice.** Enforced by unique constraint on `(candidate_id, job_id)` in `notification_job_history`.