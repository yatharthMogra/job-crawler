# Current Job Ranking Algorithm — Technical Specification

This documents the **as-is** ranking system across `recommendation_service` and `web`. There is no RRF, no embedding/vector search, and no learned model. Ranking is a deterministic pipeline: SQL hard filters → retrieval ordering by `opportunity_score` → weighted overlap scoring → tie-breakers → dedup/diversification.

---

## 1. Scores in the System

Two independent scores exist:

| Score | Computed where | Used for |
|-------|----------------|----------|
| **`opportunity_score`** | Job ingestion (`job_ingestion`) | SQL retrieval ordering, tie-breaker in ranking |
| **`personal_score`** | Recommendation service (`score_job`) | Primary personalized rank, UI display |

---

## 2. `opportunity_score` (Job-Level, Pre-Computed at Ingestion)

Computed once per job at enrichment time. Not personalized.

```
freshness = exp(-λ × hours_since_reference_at)     where λ = 0.01 (OPPORTUNITY_SCORE_FRESHNESS_DECAY)

compensation = (clamp(midpoint, 40_000, 250_000) - 40_000) / (250_000 - 40_000)
             = 0.5  if salary_min and salary_max are both null

effort = { LOW: 1.0, MEDIUM: 0.6, HIGH: 0.2 }[application_effort]  or 0.5 if unknown

opportunity_score = round(0.40 × freshness + 0.40 × compensation + 0.20 × effort, 4)
```

`reference_at` = posting freshness anchor (falls back to `posted_at`, then `created_at`).

---

## 3. Retrieval (Candidate → Job Set)

Before any personalized scoring, jobs are fetched from PostgreSQL.

### 3.1 Pool membership (hard)

```
retrieval_pools(job) ∩ active_subscribed_pools(candidate) ≠ ∅
```

Pools are strings like `{ROLE}_{ROLE_TYPE}` (e.g. `SOFTWARE_ENGINEER_FULLTIME`), assigned at ingestion from `normalized_roles × {INTERNSHIP|NEW_GRAD|FULLTIME}`.

### 3.2 Base SQL filters (always applied)

```
is_active = true
processing_state = 'success'
opportunity_score IS NOT NULL
```

### 3.3 Profile hard constraint filters (`build_constraint_filters`)

Applied as SQL `WHERE` clauses. Failing jobs are **excluded entirely** (not down-ranked).

| Constraint | SQL condition |
|------------|---------------|
| **Clearance** (if `has_clearance = false`) | `requires_clearance = false` |
| **Sponsorship required** | `requires_clearance = false` AND `sponsorship_status != 'no'` |
| **Internship only** | `is_internship = true` |
| **Fulltime only** | `is_internship = false` |
| **Minimum salary** | `salary_max IS NULL OR salary_max >= minimum_salary` |
| **Role intent** (if `ROLE_INTENT_FILTER_ENABLED`) | `role_intent IN effective_role_intents(preferences)` |
| **Domain** (if `DOMAIN_FILTER_ENABLED`) | job domain ∈ candidate primary/secondary domain |
| **Seniority** (default mode) | `seniority IN (target_seniority ∪ {UNKNOWN})` AND `seniority NOT IN hard_block` where hard_block = `{MANAGEMENT, STAFF, PRINCIPAL} \ target_seniority` |
| **Experience tier ceiling** (if `EXPERIENCE_TIER_VISIBILITY_ENABLED`) | hide tiers above ceiling (default ceiling = `SENIOR`, i.e. block `ABOVE_SENIOR`) |

Default `target_seniority` if unset: `{INTERN, NEW_GRAD, ENTRY, MID, JUNIOR}`.

### 3.4 Retrieval ordering

```sql
ORDER BY opportunity_score DESC
LIMIT scan_batch OFFSET cursor_offset
```

Default `scan_batch = 200`. **Ranking is batch-local**: each API page scores only the current 200-job slice ordered by `opportunity_score`, not the full eligible corpus.

### 3.5 Notification-only hard filters

**Digest emails** additionally apply:
- `reference_at >= now - 7 days` (`JOB_MAX_AGE_DAYS`)
- Exclude jobs already sent in `notification_job_history` for that channel
- Optional digest filters: location ILIKE, salary, domain, employment type

**Company Watch** additionally applies `job_matches_location_constraints()` — a hard location gate when the user has location prefs.

---

## 4. `personal_score` (Personalized Fit Score)

Computed per (job, candidate) in `score_job()`.

### 4.1 Component scores (each ∈ [0, 1])

**Capability overlap**
```
cap_score = |job_capabilities ∩ user_capabilities| / |user_capabilities|
          = 0  if user has no capabilities
```

**Skill overlap**
```
job_skills = tech_stack ∪ skills  (case-insensitive)
user_skills = languages ∪ frameworks ∪ tools ∪ databases ∪ other

skill_score = min(|job_skills ∩ user_skills| / |user_skills|, 1.0)
            = 0  if user has no skills
```

**Location alignment** (`loc_score`)

Structured prefs (country/state/city) take precedence:

| Condition | `loc_score` |
|-----------|-------------|
| Remote + candidate accepts remote | 1.0 |
| Remote + candidate does not accept | 0.7 |
| Country match, no state prefs | 0.75 |
| State match, no city prefs | 0.9 |
| State + city match | 1.0 |
| State match, city mismatch | 0.8 |
| State mismatch (country ok) | 0.55 |
| Country mismatch | 0.15 |
| Country unknown | 0.4 |
| No structured prefs, no location prefs | 0.5 |

Free-text fallback (when no structured prefs):
- Preferred location match → 1.0
- Acceptable location match → 0.5
- No match → 0.0
- Remote job with "remote" in preferred_locations → 1.0; else 0.7

**Compensation alignment** (`comp_score`)
```
if no minimum_salary and no minimum_hourly_rate → 0.5
if salary_max is null → 0.5
if salary_max >= minimum_salary → 1.0
else → 0.2
```

**Experience tier distance** (`tier_score`, only when `EXPERIENCE_TIER_SCORE_ENABLED=true`)
```
tier_order = [INTERN, NEW_GRAD, JUNIOR, MID, SENIOR, ABOVE_SENIOR]
distance = |index(job_tier) - index(candidate_tier)|
tier_score = max(0, 1 - distance × 0.2)
           = 0.5  if either tier is UNKNOWN
```

### 4.2 Base score (weighted linear combination)

**Default mode** (`EXPERIENCE_TIER_SCORE_ENABLED=false`, sponsorship scoring disabled):

```
base_score = 0.40 × cap_score
           + 0.25 × skill_score
           + 0.20 × loc_score
           + 0.15 × comp_score
```

**With experience tier scoring** (`EXPERIENCE_TIER_SCORE_ENABLED=true`):

```
base_score = 0.34 × cap_score
           + 0.21 × skill_score
           + 0.17 × loc_score
           + 0.13 × comp_score
           + 0.15 × tier_score
```

**Sponsorship scoring branch** (exists in code, **hard-disabled** via `use_sponsorship = False` in `score_job()` regardless of `SPONSORSHIP_SCORE_ENABLED`):

```
base_score = 0.35×cap + 0.22×skill + 0.18×loc + 0.13×comp + 0.12×sponsorship [+ tier if enabled]
```

Sponsorship component (when enabled): top sponsor → 1.0; LCA ≥20 → 0.8; ≥5 → 0.5; else 0.2; no data → 0.1; not required → 0.5.

### 4.3 Seniority multiplier (default mode only)

When tier scoring is off, seniority is a **multiplicative penalty**, not a hard filter for `SENIOR`:

```
if job_seniority ∈ target_seniority OR job_seniority = UNKNOWN → ×1.0
if job_seniority = SENIOR (not in target) → ×0.6
else → ×1.0
```

### 4.4 Final personal score

```
personal_score = base_score × seniority_multiplier
```

Range: theoretically [0, 1], but typical values cluster lower due to partial overlaps.

---

## 5. Sort Key and Post-Processing

### 5.1 Primary sort (`rank_jobs`)

After scoring all jobs in the batch:

```
sort_key = (personal_score, opportunity_score, reference_timestamp)   descending
```

### 5.2 Deduplication

Keep first occurrence per `(company_name_lower, normalize_title(title))`.
`normalize_title` = lowercase, collapse whitespace, strip trailing `.,;:`.

### 5.3 Company diversification (dashboard recommended feed)

```
base_cap = 5 per company  (RECOMMENDATION_MAX_JOBS_PER_COMPANY)
unlock_batch = 5 applications to same company  (RECOMMENDATION_COMPANY_UNLOCK_BATCH)

allowed_per_company = base_cap + floor(applications_to_company / unlock_batch) × unlock_batch
```

Walk sorted list; skip jobs that exceed per-company visible cap.

### 5.4 Surface-specific selection

| Surface | Post-rank selection |
|---------|---------------------|
| **Dashboard `/jobs/recommended`** | dedup → diversify (cap=5, unlock batch=5) |
| **Email digest** | dedup → `select_top_jobs(top_k=4, max_per_company=1)` |
| **Company Watch** | score filter `personal_score >= 0.5` → sort → top 5 |
| **Dashboard `/jobs` (browse)** | no `personal_score`; `ORDER BY opportunity_score DESC` only |

---

## 6. Frontend (`web`) — What Happens After the API

The recommended feed calls `GET /dashboard/jobs/recommended`. The server returns jobs with `personal_score` and `match_reasons`.

### 6.1 Client-side filtering (does not re-score)

Applied in `NeuralRecommendationsPage` before display:
- Exclude applied jobs
- Exclude "not interested" (localStorage)
- Text search (title, company, skills)
- Employment type, date posted, location filters
- Advanced filters (salary, work model, experience level) via `filterJobsByState`
- Catalog role filter (primary/secondary roles from profile)

Profile constraints (`sponsorship_required`, `fulltime_only`, `internship_only`, salary minimum) are enforced **server-side** on profile save + refresh; not passed as query params on each fetch.

### 6.2 Client-side re-sort

After filtering:
```
display_order = sort by personal_score DESC
```

This can **override** server diversification ordering (company caps are not re-applied client-side).

### 6.3 Display thresholds (UI only, not ranking)

```
matchTier:   ≥0.88 TOP MATCH, ≥0.80 STRONG MATCH, ≥0.72 GOOD MATCH
isPremiumRole: personal_score ≥ 0.86 AND senior/staff title
coreSkillsMatchPercent: min(99, round(personal_score × 100 + 3))
```

### 6.4 Pagination

- Server: cursor over `opportunity_score`-ordered batches (200 jobs/batch)
- Client: shows 8 jobs at a time; fetches next server batch when local list exhausted

---

## 7. End-to-End Pipeline (Dashboard Recommended)

```
1. active_pools(candidate)
2. load profile → build_constraint_filters(profile)        [hard SQL filters]
3. SELECT jobs WHERE pools ∩ active AND filters
   ORDER BY opportunity_score DESC
   LIMIT 200 OFFSET cursor
4. FOR EACH job: personal_score = score_job(job, profile)
5. SORT BY (personal_score, opportunity_score, reference_at) DESC
6. DEDUP BY (company, normalized_title)
7. DIVERSIFY: max 5/company (+5 unlock per 5 applications)
8. ATTACH match_reasons (explainability only, no score impact)
9. RETURN to frontend
10. Frontend: filter → re-sort by personal_score DESC → paginate 8 at a time
```

---

## 8. Configurable Weights (Env Vars)

### Recommendation service defaults

```
SCORE_CAPABILITY_WEIGHT=0.40
SCORE_SKILL_WEIGHT=0.25
SCORE_LOCATION_WEIGHT=0.20
SCORE_COMPENSATION_WEIGHT=0.15

# Tier mode (off by default):
EXPERIENCE_TIER_SCORE_ENABLED=false
SCORE_CAPABILITY_WEIGHT_WITH_TIER=0.34
SCORE_SKILL_WEIGHT_WITH_TIER=0.21
SCORE_LOCATION_WEIGHT_WITH_TIER=0.17
SCORE_COMPENSATION_WEIGHT_WITH_TIER=0.13
SCORE_EXPERIENCE_TIER_WEIGHT=0.15

RECOMMENDATION_MAX_JOBS_PER_COMPANY=5
RECOMMENDATION_COMPANY_UNLOCK_BATCH=5
NOTIFICATION_MAX_JOBS_PER_COMPANY=1
NOTIFICATION_JOBS_PER_EMAIL=4
COMPANY_WATCH_MIN_SCORE=0.5
JOB_MAX_AGE_DAYS=7
```

### Job ingestion (`opportunity_score`)

```
FRESHNESS_WEIGHT=0.40
COMPENSATION_WEIGHT=0.40
EFFORT_WEIGHT=0.20
OPPORTUNITY_SCORE_FRESHNESS_DECAY=0.01
COMP_FLOOR=40000
COMP_CEILING=250000
```

---

## 9. What Is Not in the Current Algorithm

- No RRF or rank fusion across multiple retrievers
- No vector/embedding similarity
- No collaborative filtering or ML model
- H-1B sponsor history is **not** used in scoring (`use_sponsorship = False`); sponsorship is a hard filter on `sponsorship_status` only
- `fetch_jobs_with_pool_floors()` (per-pool minimum representation) is implemented but **not wired** into production paths
- `clearance_filter_enabled` config exists but clearance is always filtered when user lacks clearance

---

## 10. Summary Formula (Production Default Path)

For a candidate C and job J in the same retrieval batch:

```
eligible(J, C) = pool_match ∧ hard_filters(profile_C)

retrieval_order(J) = opportunity_score(J)     [used for batch selection + tie-break]

personal_score(J, C) =
  (0.40 × |caps_J ∩ caps_C|/|caps_C|
 + 0.25 × min(|skills_J ∩ skills_C|/|skills_C|, 1)
 + 0.20 × loc_align(J, prefs_C)
 + 0.15 × comp_align(J, constraints_C))
 × seniority_mult(J, constraints_C)

final_rank(J) = sort descending:
  (personal_score, opportunity_score, reference_timestamp)

output(J) = dedup(company, title) → diversify(≤5/company)
```

Frontend then applies client filters and re-sorts by `personal_score` only.

---

**Source files**: `recommendation_service/app/scoring/recommendation.py`, `ranker.py`, `retrieval.py`, `location.py`, `seniority.py`, `experience_tier.py`, `api/dashboard.py`; `job_ingestion/app/ingestion/recommendation_fields.py`; `web/components/jobs/neural-recommendations-page.tsx`.