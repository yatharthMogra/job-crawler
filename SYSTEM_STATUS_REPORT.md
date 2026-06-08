# System Status Report — Job Crawler & Recommendation Platform

**Date:** June 8, 2026  
**Audience:** External engineering advisors / product guidance stakeholders  
**Tone:** Semi-technical (engineering-manager level)  
**Scope:** `job_ingestion`, recommendation engine (`recommendation_service`), and email notification pipeline

---

## 1. Purpose of this report

This document summarizes **ground reality** as of early June 2026: what is built, what has been validated with real data and real users, what broke along the way and how it was fixed, and what remains intentionally out of scope or unfinished.

It is meant to keep advisor planning aligned with implementation progress across the three pillars that feed the product loop:

```
job_ingestion → enriched job index → recommendation_service → email briefing
                      ↑
              profile_service (user profiles & capabilities)
```

---

## 2. Executive summary

| Pillar | Status | One-line assessment |
|--------|--------|---------------------|
| **Job ingestion** | **Operational** | 889/889 jobs enriched successfully across 3 ATS platforms; queue drained |
| **Recommendation engine** | **Functional, validated** | Personalized ranking works end-to-end for 2 real users; major ranking bugs fixed |
| **Email notifications** | **Live (pilot)** | SMTP delivery confirmed for 2 pilot users with PDF-style dark briefing template |

**Bottom line:** The V1 recommendation loop described in the engineering spec is **working end-to-end in local/staging conditions**. We are past “can it rank?” and into “does the output match product intent?” — with known gaps documented below.

**Not yet production-grade for:** scale, deliverability hardening, unsubscribe/preferences UX, or automated CI-backed regression of ranking quality.

---

## 3. Architecture snapshot

### Services (monorepo, shared Postgres `jobingestion`)

| Service | Port (local) | Responsibility |
|---------|--------------|----------------|
| `job_ingestion` | 8000 | Fetch, normalize, enrich jobs; compute `opportunity_score` + `retrieval_pools` |
| `profile_service` | 8001 | Candidate profiles, capabilities, constraints, preferences |
| `recommendation_service` | 8002 | Pool subscriptions, dashboard API, personalized scoring, scheduled email pipeline |

### Data flow for a notification send

1. User has active **pool subscriptions** (`user_pool_subscriptions`).
2. Pipeline loads **profile** (capabilities, skills, constraints, location preferences).
3. **Retrieval:** all unsent, constraint-passing jobs in subscribed pools (safety cap 500).
4. **Ranking:** weighted personal score → dedup by company+title → top 4.
5. **Render:** Jinja2 dark-theme daily briefing HTML.
6. **Send:** SMTP; record `notification_batches` + `notification_job_history` (no resend of same job).

---

## 4. Job ingestion — status

### 4.1 What’s delivered (per V2 + recommendation extensions)

- **Multi-platform connectors:** Greenhouse, Ashby, Lever (public boards).
- **Company source of truth:** `data/companies.json` with strict seed/sync.
- **Decoupled enrichment:** queue + batch worker + Gemini structured extraction (`EXTRACTION_VERSION=v2`).
- **Recommendation fields at ingestion:** `normalized_roles`, `job_capabilities`, `tech_stack`, `skills`, `application_effort`, `retrieval_pools`, `opportunity_score`.
- **Operational layer:** pipeline runs, per-company results, events, reprocessing APIs, dashboard review/cost endpoints (see `JOB_CRAWLER_PHASE_STATUS.md`).

### 4.2 Current inventory (DB, June 8 2026)

| Metric | Value |
|--------|-------|
| Companies configured | 12 (10 active) |
| Jobs `processing_state=success` | **889 / 889 (100%)** |
| Jobs with `opportunity_score` | 889 |
| Jobs with non-empty `skills` | 712 (80%) |
| Jobs with `tech_stack` | 397 |
| Jobs with `job_capabilities` | 594 |

**By platform (success jobs):**

| Platform | Jobs | With description text |
|----------|------|---------------------|
| Greenhouse | 358 | 358 |
| Ashby | 281 | 281 |
| Lever | 250 | 250 |

Active company sources include ScaleAI, Figma (Greenhouse); Ramp, Notion, Linear (Ashby); Palantir, Basis, Achievers, Slate (Lever).

### 4.3 Recent engineering work (recommendation-unblocking)

| Issue | Root cause | Resolution |
|-------|------------|------------|
| Ashby jobs missing skills/descriptions | Connector did not fetch `descriptionHtml`; GraphQL field names wrong | Ashby connector fixed + 281-job description backfill |
| Enrichment failures / stalls | Gemini quota + batch sizing | Model switch (`gemini-3.1-flash-lite`), rate-window caps, queue pause/backfill scripts |
| Flat personal scores | Empty `tech_stack`/`skills` on many jobs | Prompt/schema gap fixed; full re-enrichment pass |

### 4.4 Ingestion — known gaps

- **177 jobs** have no extracted skills (often non-engineering roles or thin descriptions).
- **Anthropic / OpenAI** companies exist in seed data but are **inactive** — not contributing jobs.
- Enrichment is **Gemini-rate-limited**; production cadence needs monitoring/alerts on queue depth.
- `opportunity_score` is global (freshness + comp + effort) — not personalized; used for dashboard sort and formerly biased email pre-filter (fixed in recommendation layer).

---

## 5. Recommendation engine — status

### 5.1 Implemented (per `recommendation_system_engineering_spec.md`)

| Component | Status |
|-----------|--------|
| Pool subscriptions API | ✅ |
| Dashboard job retrieval (`GET /dashboard/jobs`) | ✅ |
| Personal scoring (`score_job`) | ✅ |
| Explainability (deterministic, no LLM) | ✅ |
| Location alignment | ✅ (segment-aware matcher) |
| Notification dedup (company + normalized title) | ✅ |
| Unit tests (scoring, location, ranker, renderer) | ✅ 21 tests passing |

### 5.2 Scoring model (current weights)

| Signal | Weight |
|--------|--------|
| Capability overlap | 40% |
| Skill overlap | 25% |
| Location alignment | 20% |
| Compensation vs min salary | 15% |

**Location matcher (June 2026 fix):** Segment-aware parsing with NY/NYC/New York aliases; strips parentheticals like `(HQ)`. Multi-location strings (`SF; New York, NY`, `SF • NY • US`) score full credit when user prefers NY.

### 5.3 Validation — two pilot users

Full ranked exports: [`exports/user_recommendations.json`](exports/user_recommendations.json)  
Human-readable summary: [`testing_results.md`](testing_results.md)

| User | Email | Matching jobs | Personal score tiers | Top-4 character (post-fix) |
|------|-------|---------------|----------------------|----------------------------|
| Yatharth | yatharthmogra@gmail.com | 317 | 57 unique scores | ScaleAI + Ramp + Figma; NY-heavy |
| Ram | ramparekh208@gmail.com | 321 | 15 unique scores | Ramp data platform + Figma DS + Ramp ML |

**Pools subscribed (full-time engineering/data):**

- Yatharth: `SWE`, `BACKEND_ENGINEER`, `ML_ENGINEER`, `FULLSTACK_ENGINEER`
- Ram: `DATA_ENGINEER`, `DATA_SCIENTIST`, `ML_ENGINEER`, `SWE`

### 5.4 Ranking fixes shipped (June 2026)

| Problem | Before | After |
|---------|--------|-------|
| Location prefs ignored (`NY, USA` vs `New York, NY`) | All jobs `loc_score=0` | NY-listed jobs get `loc_score=1.0` |
| Email pre-filtered top 50 by `opportunity_score` | ScaleAI-dominated emails | All pool jobs ranked personally (cap 500) |
| Duplicate titles in top-4 (e.g. two ScaleAI Robotics) | Possible | Dedup keeps highest personal score |

### 5.5 Recommendation — known gaps / product debt

| Item | Notes |
|------|-------|
| `"Anywhere in the United States"` | Scores as NY match via USA alias — overly broad |
| Compensation neutral `0.5` | Flattens scores when salary missing (many Ramp/Ashby postings) |
| `remote_type=unclear` | No remote-preference boost/penalty yet |
| Ram has no `preferred_locations` | Location weight is neutral (0.5) for all jobs |
| Dashboard vs email | Dashboard sorts by `opportunity_score` only; email uses personal score |
| No seniority / role-type hard filters in scoring | Only constraint filters (sponsorship, salary floor, etc.) |
| No LLM explanations in notifications | By design for V1 |

---

## 6. Email / mailing — status

### 6.1 Pipeline

| Piece | Status |
|-------|--------|
| APScheduler (default every 3h) | ✅ Runs on service startup |
| Manual trigger `POST /notifications/run` | ✅ |
| Per-user batch + job history | ✅ |
| Skip reasons (`no_new_jobs`, `email_failed`, etc.) | ✅ |
| SMTP sender (Gmail app password in local `.env`) | ✅ Validated |

### 6.2 Template (June 2026)

- **Format:** Jinja2 HTML email, table layout + inline CSS (email-client safe).
- **Design:** Dark theme aligned to product PDF mock (`Career Match AI - Daily Briefing.pdf`).
- **Palette extracted from PDF:** green `#67bb6b`, orange `#de6900`, gold `#d1a84b`, dark surfaces `#07090b` / `#171a1f`.
- **Per-job blocks:** rank, CTA (APPLY NOW / APPLY SOON), velocity/competition/visa heuristics, market signals, profile-match tags, effort estimate.
- **Preview script:** `scripts/preview_daily_briefing.py` → `exports/preview_daily_briefing.html`

### 6.3 Delivery record (pilot)

| Recipient | Last successful send | Top-4 snapshot |
|-----------|---------------------|----------------|
| yatharthmogra@gmail.com | 2026-06-08 05:24 UTC | ScaleAI Infra GenAI, Ramp Backend Ops, Figma Distributed Systems, ScaleAI Full-Stack |
| ramparekh208@gmail.com | 2026-06-08 05:25 UTC | Ramp Data Platform, Figma DS PhD, Ramp Credit Risk Scientist, ScaleAI Frontier Agents (APPLY SOON) |

**DB:** 3 successful batches (12 jobs emailed total across pilot + 1 test account). Earlier SMTP config failures (June 7) resolved.

### 6.4 Mailing — known gaps

| Item | Spec / product intent | Current state |
|------|----------------------|---------------|
| Unsubscribe / manage preferences links | Required for production | URLs point to `localhost:3000` placeholders |
| Per-user manual send API | Useful for ops | Only full-pipeline or ad-hoc script |
| Email dark-mode in Gmail mobile | UX risk | Some clients may flatten/invert colors |
| Metric copy (velocity, competition, visa) | Rich in PDF mock | Rule-based heuristics, not ML |
| `detected Xm after` on old jobs | Looks odd at scale (e.g. 17175m) | Uses `created_at - posted_at` literally |
| Push / Discord / browser notifications | Spec mentions | Not implemented |
| Deliverability (SPF/DKIM, production domain) | Production need | Using personal/ university SMTP for pilot |

---

## 7. Cross-system validation performed

| Validation | Evidence |
|------------|----------|
| Full enrichment pass | 889/889 success |
| Ashby description backfill | 281/281 with `description_text` |
| Personalized ranking script | `scripts/run_user_recommendations.py` |
| Location + dedup unit tests | `recommendation_service/tests/` |
| Live email send (2 users) | `notification_batches.email_delivered = true` |
| Ranking parity email ↔ script | After retrieval fix, top-4 align with `testing_results.md` |

---

## 8. Alignment with advisor specs

| Spec document | Alignment |
|---------------|-----------|
| `recommendation_system_engineering_spec.md` | **Core V1 implemented** — ingestion extensions, recommendation service, notification pipeline, deterministic explainability |
| `job_recommendations_system.md` | **Philosophy matched** — top-4, pool-based retrieval, no LLM at notification time |
| `JOB_CRAWLER_PHASE_STATUS.md` | **Ingestion V2.2 complete** at functional level; recommendation fields added on top |
| Product PDF (Daily Briefing) | **Visual parity ~80%** — layout and colors; some metrics are heuristic stubs |

---

## 9. Suggested next steps (for planning sync)

**Near-term (quality & pilot readiness)**

1. Set `preferred_locations` on all pilot profiles; tighten USA-wide location matching.
2. Wire production `APP_BASE_URL` + unsubscribe/preferences pages (or stub endpoints).
3. Fix `detected after` display for backfilled jobs (cap or use ingestion event time).
4. Production SMTP domain + deliverability setup.

**Medium-term (product fidelity)**

5. Compensation scoring when `salary_max` is null (neutral hurts Ramp/Ashby rankings).
6. Dashboard personal sort option (or blended score) for parity with email.
7. Seniority / role-type preference filters in ranking.
8. Richer market-signal generation from enrichment metadata (still deterministic).

**Scale / ops**

9. Enrichment quota monitoring + auto-throttle alerts.
10. CI job running recommendation tests + smoke notification render on PRs.
11. Pagination-at-scale hardening on ingestion list APIs (per crawler status doc).

---

## 10. Key artifacts & entry points

| Artifact | Path |
|----------|------|
| This report | `SYSTEM_STATUS_REPORT.md` |
| Crawler phase report | `JOB_CRAWLER_PHASE_STATUS.md` |
| Ingestion V2 detail | `job_ingestion/IMPLEMENTATION_STATUS_V2.md` |
| Recommendation spec | `recommendation_system_engineering_spec.md` |
| User ranking results | `testing_results.md`, `exports/user_recommendations.json` |
| Email HTML preview | `exports/preview_daily_briefing.html` |
| Run recommendations | `scripts/run_user_recommendations.py` |
| Preview email | `scripts/preview_daily_briefing.py` |
| Unified web app | `web/README.md` |

### Unified web app (`web/`)

A single Next.js app merges the job dashboard and profile-review flow:

| Route group | Routes |
|-------------|--------|
| Profile onboarding (no sidebar) | `/onboarding`, `/profile/upload`, `/profile/processing`, `/profile/review`, `/profile/confirm` |
| Dashboard (sidebar) | `/jobs`, `/recommended`, `/saved`, `/applied`, `/profile`, `/preferences` |

- **Session:** `localStorage.profile_candidate_id` (email-only signup; no password in V1)
- **Backends:** `profile_service` :8001 (`X-API-Key`), `recommendation_service` :8002 (`candidate_id` query param)
- **Subscriptions:** pools auto-sync from profile preferences on dashboard boot and after profile commit
- **Recommended feed:** `GET /dashboard/jobs/recommended` returns `personal_score` + `match_reasons`

See `web/README.md` for env vars and dev workflow.

### Local service commands

```bash
./scripts/dev-profile-service.sh          # :8001
./scripts/dev-recommendation-service.sh   # :8002
./scripts/dev-web.sh                      # :3000 (Next.js)
curl -X POST http://localhost:8002/notifications/run   # trigger all subscribed users
```

---

## 11. Risk register (honest)

| Risk | Likelihood | Impact | Mitigation direction |
|------|------------|--------|----------------------|
| Gemini quota exhaustion on re-enrichment | Medium | High | Rate windows, monitoring, fallback model |
| Email treated as spam / promo tab | Medium | Medium | Dedicated domain, DKIM, smaller pilot list |
| Ranking feels “wrong” for users without location prefs | Medium | Medium | Profile onboarding for preferences |
| `opportunity_score` vs personal score confusion in UI | Low | Medium | Clear labeling in dashboard |
| Old jobs surface in first-ever email | Low | Low | `since` filter + history; first send is intentionally broad |

---

*Report generated from live database queries, pilot user runs, and implementation review on June 8, 2026. For deeper technical detail on a single pillar, see the linked artifacts above.*
