# Experience Tier Matching — Rollout Guide

This document is the operational checklist for rolling out experience tier matching after the code has been merged. For product intent and design rationale, see [experience_tier_guidance.md](experience_tier_guidance.md).

## What was built

A domain-agnostic experience ladder (`INTERN`, `NEW_GRAD`, `JUNIOR`, `MID`, `SENIOR`, `ABOVE_SENIOR`, `UNKNOWN`) on:

- **Jobs** — LLM-extracted at enrichment time as `normalized_jobs.experience_tier` (separate from existing `seniority`)
- **Candidates** — derived deterministically into `candidate_profiles.constraints.current_experience_tier`

Two recommendation mechanisms (both behind feature flags, default **off**):

1. **Visibility gate** — hides jobs above a configurable ceiling
2. **Ranking signal** — ladder distance affects personal score; `UNKNOWN` jobs score neutrally

When flags are on, experience tier **replaces** legacy seniority filtering/scoring (`target_seniority` + `seniority_score_multiplier`). The `seniority` column and enrichment field are unchanged and still populated.

---

## Prerequisites

- Code deployed across:
  - `job_ingestion` (migration + v8 enrichment)
  - `profile_service` (tier derivation on profile writes)
  - `recommendation_service` (gate + scoring)
  - `web` (onboarding questions on job-intent screen)
- Enrichment worker pool running for job backfill
- Database backup taken before migration (production)

---

## Phase 1 — Database migration

From `job_ingestion/`:

```bash
alembic upgrade head
```

Migration: `20260627_0017_experience_tier.py`

Adds `experience_tier VARCHAR(32)` to:

- `normalized_jobs` (NOT NULL, default `UNKNOWN`)
- `job_enrichments` (nullable)
- `job_archive` (nullable)

Verify:

```sql
SELECT column_name FROM information_schema.columns
WHERE table_name = 'normalized_jobs' AND column_name = 'experience_tier';
```

---

## Phase 2 — Deploy ingestion (flags still off)

Ensure `job_ingestion` is running with:

- `EXTRACTION_VERSION=v8` (default in code after deploy)

New jobs ingested after deploy will get `experience_tier` from LLM enrichment. Existing jobs remain `UNKNOWN` until backfill.

Quick check after a fresh ingest:

```sql
SELECT experience_tier, extraction_version, COUNT(*)
FROM normalized_jobs
WHERE is_active
GROUP BY 1, 2
ORDER BY 3 DESC;
```

---

## Phase 3 — Backfill existing jobs (~40K)

Script: [`scripts/backfill_experience_tier.py`](scripts/backfill_experience_tier.py)

**Requires enrichment workers running** (start `job_ingestion` service).

```bash
# Preview counts
python scripts/backfill_experience_tier.py --dry-run

# Re-queue all jobs needing v8 / non-UNKNOWN tier
python scripts/backfill_experience_tier.py

# Or in batches
python scripts/backfill_experience_tier.py --limit 5000
```

Monitor progress:

```sql
SELECT
  COUNT(*) FILTER (WHERE is_active AND experience_tier != 'UNKNOWN') AS classified,
  COUNT(*) FILTER (WHERE is_active AND experience_tier = 'UNKNOWN') AS unknown,
  COUNT(*) FILTER (WHERE is_active AND extraction_version = 'v8') AS on_v8
FROM normalized_jobs
WHERE processing_state IN ('success', 'partial_success', 'pending');
```

**Cost note:** full backfill re-runs LLM enrichment for all active jobs. Watch Gemini quota / spend.

---

## Phase 4 — Backfill candidate profiles

Script: [`scripts/backfill_profile_experience_tier.py`](scripts/backfill_profile_experience_tier.py)

From repo root (uses `profile_service` DB connection):

```bash
python scripts/backfill_profile_experience_tier.py --dry-run
python scripts/backfill_profile_experience_tier.py
```

Verify:

```sql
SELECT
  constraints->>'current_experience_tier' AS tier,
  COUNT(*)
FROM candidate_profiles
WHERE is_current
GROUP BY 1
ORDER BY 2 DESC;
```

New users going through onboarding will also get tier derived when they complete the job-intent step (years of experience + enrollment questions).

---

## Phase 5 — Quality spot-check (before enabling flags)

Manually review ~50 jobs across domains (SWE, finance, ops, design). Sample query:

```sql
SELECT title, company_name, seniority, experience_tier, job_domain
FROM normalized_jobs
WHERE is_active AND experience_tier != 'UNKNOWN'
ORDER BY random()
LIMIT 50;
```

Checklist per row:

- [ ] Tier matches responsibilities more than title inflation
- [ ] Internships → `INTERN`
- [ ] New grad programs → `NEW_GRAD`
- [ ] Staff/principal/director → `ABOVE_SENIOR`
- [ ] Genuinely ambiguous postings → `UNKNOWN` (not forced guesses)

Also spot-check a few candidate profiles:

```sql
SELECT
  candidate_id,
  constraints->>'full_time_experience_years' AS years,
  constraints->>'is_currently_enrolled' AS enrolled,
  constraints->>'current_experience_tier' AS tier
FROM candidate_profiles
WHERE is_current
LIMIT 20;
```

---

## Phase 6 — Enable in staging

Add to `recommendation_service/.env` (staging):

```env
EXPERIENCE_TIER_VISIBILITY_ENABLED=true
EXPERIENCE_TIER_VISIBILITY_CEILING=SENIOR
EXPERIENCE_TIER_SCORE_ENABLED=false
SCORE_EXPERIENCE_TIER_WEIGHT=0.15
```

Restart recommendation service.

### Validate visibility gate

- `ABOVE_SENIOR` jobs should not appear in recommended/browse results
- `UNKNOWN` jobs should still appear
- Direct job URL (`GET /dashboard/jobs/{job_id}`) should 404 for above-ceiling jobs

Run recommendations for a test user:

```bash
python scripts/run_user_recommendations.py --candidate-id <uuid>
```

### Enable scoring (staging, after gate looks good)

```env
EXPERIENCE_TIER_SCORE_ENABLED=true
```

Validate:

- MID-tier candidate sees MID jobs ranked above SENIOR jobs
- Unknown-tier jobs sit in the middle of the score range (not top, not bottom)
- Seniority multiplier is **not** applied when tier scoring is on

---

## Phase 7 — Production rollout

Recommended order:

| Step | Action | Env change |
|------|--------|------------|
| 1 | Deploy all services (migration + code) | None for rec flags |
| 2 | Run job backfill | — |
| 3 | Run profile backfill | — |
| 4 | Spot-check quality | — |
| 5 | Enable visibility gate | `EXPERIENCE_TIER_VISIBILITY_ENABLED=true` |
| 6 | Monitor 24–48h | Check notification quality, user feedback |
| 7 | Enable scoring | `EXPERIENCE_TIER_SCORE_ENABLED=true` |
| 8 | Monitor rank order | Compare before/after via `run_user_recommendations.py` |

---

## Environment variables reference

### job_ingestion

| Variable | Default | Notes |
|----------|---------|-------|
| `EXTRACTION_VERSION` | `v8` | Bump triggers re-enrichment on next ingest/backfill |

### recommendation_service

| Variable | Default | Notes |
|----------|---------|-------|
| `EXPERIENCE_TIER_VISIBILITY_ENABLED` | `false` | When `true`, replaces seniority hard filters |
| `EXPERIENCE_TIER_VISIBILITY_CEILING` | `SENIOR` | Hides tiers strictly above this (`ABOVE_SENIOR` hidden by default) |
| `EXPERIENCE_TIER_SCORE_ENABLED` | `false` | When `true`, adds tier distance to personal score; skips seniority multiplier |
| `SCORE_EXPERIENCE_TIER_WEIGHT` | `0.15` | Weight of tier component in score sum |

See also [`recommendation_service/.env.example`](recommendation_service/.env.example).

---

## Key files (for debugging)

| Area | Path |
|------|------|
| Job tier taxonomy + LLM prompt | `job_ingestion/app/ingestion/extractor/experience_tier.py` |
| Enrichment schema | `job_ingestion/app/ingestion/extractor/llm.py` |
| Job backfill script | `scripts/backfill_experience_tier.py` |
| Candidate derivation | `profile_service/app/experience_tier.py` |
| Candidate sync on write | `profile_service/app/experience_tier_sync.py` |
| Profile backfill script | `scripts/backfill_profile_experience_tier.py` |
| Visibility gate | `recommendation_service/app/notification/retrieval.py` |
| Distance scoring | `recommendation_service/app/scoring/experience_tier.py` |
| Score integration | `recommendation_service/app/scoring/recommendation.py` |
| Onboarding UI | `web/components/profile/screens/job-intent-screen.tsx` |

---

## Tests to run before prod

```bash
# job_ingestion
cd job_ingestion && python -m pytest tests/test_experience_tier.py -q

# profile_service
cd profile_service && python -m pytest tests/test_experience_tier.py -q

# recommendation_service (use the service venv)
cd recommendation_service && python -m pytest tests/test_experience_tier_scoring.py -q
```

---

## Rollback

If something goes wrong:

1. **Fast rollback (no code deploy):** set both flags to `false` in recommendation service — reverts to legacy seniority behavior immediately
2. **Partial rollback:** keep visibility gate on, turn scoring off (or vice versa) — the two mechanisms are independent
3. **Data rollback:** not required; `experience_tier` is additive. Old `seniority` field is untouched

To change the ceiling without code deploy:

```env
EXPERIENCE_TIER_VISIBILITY_CEILING=MID   # more aggressive hiding
EXPERIENCE_TIER_VISIBILITY_CEILING=ABOVE_SENIOR  # only hide top tier (minimal gate)
```

---

## What is intentionally unchanged

- `normalized_jobs.seniority` enrichment and column
- `/filters` Experience Level UI (`target_seniority` job preference)
- LLM does **not** extract literal years from job postings for tier

---

## Open follow-ups (optional, post-rollout)

- [ ] Expose `experience_tier` in job cards on the web dashboard
- [ ] Show derived tier read-only on job-intent screen ("Based on your inputs, you're at **Mid** level")
- [ ] Tune `SCORE_EXPERIENCE_TIER_WEIGHT` and distance step (`TIER_DISTANCE_STEP = 0.2`) based on A/B results
- [ ] Extract shared taxonomy into a single package to avoid three copies of the ladder
