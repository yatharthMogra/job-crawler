# Consultant Review — Planned Changes

Tracking doc for quality fixes identified from the 2026-06-13 recommendation review
(Ram + Yatharth, ~1,640 / ~1,571 matching jobs). Source: consultant feedback on
`testing_results.md`, plus follow-up design decisions.

**Diagnosis:** Scale is working; recommendation algorithm is fine. Issues are corpus
curation — wrong role types (educator jobs matching engineers) and clearance-required
jobs polluting mid-tier rankings after adding many defense contractors.

**Principle:** Ingestion can stay permissive. Recommendation retrieval is the gate.

---

## Validated (architecture confirmed)

- **Three-layer model** is architecturally correct: `role_intent` → `normalized_roles` →
  `retrieval_pools`.
- **Cardinality** is right: job has one `role_intent`, user has many `role_intents`.
- **Filter stack ordering** is correct — coarsest filter first:
  `role_intent` → domain → clearance → sponsorship/salary/seniority → pools → scoring.
- **Touch points** across ingestion and recommendation services are comprehensive.
- **Implementation order** (constants → enrichment → backfill → profile → retrieval →
  tests → validate) is correct.

---

## Three-layer model (coarse → granular)

```text
role_intent          career track (NEW)     engineer, educator, investment_banker, analyst
        ↓
normalized_roles     function / hat         ML_ENGINEER, SWE, FINANCE, DATA_ANALYST  (multiple per job)
        ↓
retrieval_pools      subscription unit      ML_ENGINEER_FULLTIME, FINANCE_FULLTIME  (multiple per job)
```

| Layer | Cardinality (job) | Cardinality (user) | Purpose |
|-------|-------------------|--------------------|---------|
| `role_intent` | **one** | **many** (`role_intents`) | Coarse career-track fit — hard filter |
| `normalized_roles` | many | — (derived from resume) | Technical/business function taxonomy |
| `retrieval_pools` | many | many (subscriptions) | Granular feed match + scoring input |

**Why pools alone can't fix Per Scholas:** A "Technical Instructor (AWS ML)" job gets
`normalized_roles = [ML_ENGINEER]` and pool `ML_ENGINEER_FULLTIME` — identical to a real
ML engineer at the pool level. `role_intent = educator` is the gate pools cannot provide.

**Naming:** Use `role_intent` / `role_intents` in code — not `role`. The codebase already
has `normalized_roles` and `primary_roles`; a third thing called "role" causes confusion.

---

## Change 1 — `requires_clearance` (job enrichment)

**Status:** Planned

Add a boolean `requires_clearance` extracted by the LLM during enrichment.

**Meaning:**

| `requires_clearance` | When |
|----------------------|------|
| `true` | Must already hold clearance: "must hold active TS/SCI", "active Secret clearance required", "existing clearance required" |
| `false` | No active clearance required: "clearance sponsorship available", "clearance preferred", "able to obtain clearance", or no mention |

**Important:** "Clearance sponsorship available" is **not** `requires_clearance: true`.
That phrase means the company will sponsor a US citizen who doesn't currently hold
clearance — an invitation, not a requirement. US-citizen CS grads are exactly the target
audience for those jobs.

**Fixes:** Captivation, CACI, Northrop Grumman, GDMS, AMERICAN SYSTEMS mid-tier pollution
for users without clearance.

### LLM prompt disambiguation (add before implementation)

```
requires_clearance:
- true ONLY when the posting requires an ACTIVE, EXISTING clearance at time of application
  ("must hold TS/SCI", "active Secret clearance required", "existing clearance required")
- false when clearance is sponsorable, preferred, or obtainable
  ("clearance sponsorship available", "clearance preferred", "must be able to obtain clearance")
- false when clearance is not mentioned
```

### Touch points

| Layer | File(s) | Work |
|-------|---------|------|
| DB schema | Alembic migration on `normalized_jobs` (+ `job_archive`) | `requires_clearance BOOLEAN NOT NULL DEFAULT false` |
| Pydantic schema | `job_ingestion/app/ingestion/extractor/llm.py` | Add to `JobEnrichment` and `BatchJobEnrichment` |
| LLM prompt | Same file, `ENRICHMENT_SYSTEM_PROMPT` | Disambiguation block above |
| Write-back | `job_ingestion/app/ingestion/enrichment_worker.py` | `_apply_enrichment_to_job`, `_recommendation_fields_from_enrichment` |
| Archive sync | `job_ingestion/app/ingestion/job_archive_sync.py` | Pass through on archive rows |
| Read model | `recommendation_service/app/models/shared.py` | Add column to mirrored `NormalizedJob` |
| Tests | `job_ingestion/tests/test_extractors.py` (+ new cases) | Include sponsorship-available → `false` cases |
| Backfill | One-off script | Re-enrich active jobs or clearance-only re-extraction pass |

**Current gap:** `NormalizedJob` and `JobEnrichment` have no `requires_clearance` today.

---

## Change 2 — Wire clearance filter into recommendation retrieval

**Status:** Planned (pairs with Change 1)

Filter clearance-required jobs at retrieval time based on candidate profile.

### Decision: use `has_clearance`, not `exclude_security_clearance`

**Resolved.** For a CS-grad platform where most users can't hold clearances (non-citizens)
or don't have one, the current default (`exclude_security_clearance: false` → clearance
jobs show by default) is wrong.

**Replace** `exclude_security_clearance` with **`has_clearance: bool = false`** on the
profile. Positive-sense ("do you have it?") rather than double-negative ("exclude?").

| Field | Default | Semantics |
|-------|---------|-----------|
| `has_clearance` | `false` | User does not hold an active security clearance |

Migrate or deprecate `exclude_security_clearance` in profile schema and web UI.

### Filter logic

```python
# In build_constraint_filters(), after domain filter:
if not constraints.get("has_clearance", False):
    filters.append(NormalizedJob.requires_clearance.is_(False))
```

Users with `has_clearance: true` see all jobs including clearance-required ones.

### What exists today (to migrate)

- `exclude_security_clearance` in `profile_service/app/schemas/profile.py`
- Web UI toggle in `web/app/(dashboard)/filters/page.tsx`
- Default `excludeSecurityClearance: false` in `web/lib/profile/job-filters.ts`

### What's missing

- `has_clearance` field on profile constraints
- `build_constraint_filters()` does not apply clearance filter
- No job-side `requires_clearance` field (blocked on Change 1)

### Tests

Add cases in `recommendation_service/tests/` (similar to `test_domain_filter.py`):
- `has_clearance=false` → excludes `requires_clearance=true` jobs
- `has_clearance=true` → includes them
- Sponsorship-available jobs (`requires_clearance=false`) visible to all

---

## Change 3 — `role_intent` (dual-sided, job + user)

**Status:** Planned — structural fix for Per Scholas and similar misclassification

Replaces company-level Per Scholas deactivation (`company_type`) as the primary fix.
Ingestion stays permissive; recommendation retrieval filters by career track.

### Consultant's original proposal (superseded)

```python
role_intent: Literal["PRACTITIONER", "EDUCATOR", "CONSULTANT", "OPERATOR", "OTHER"]
```

### Our refined taxonomy

Career-track oriented enum in a shared constants file (like `NORMALIZED_ROLES` in
`job_ingestion/app/ingestion/constants_taxonomy.py`):

```python
ROLE_INTENTS = [
    "engineer",           # SWE, ML, DE, DevOps, platform, infra — hands-on building
    "researcher",         # research scientist, R&D, academic-style technical work
    "consultant",         # client-facing advisory / professional services
    "educator",           # instructor, trainer, curriculum, instructional assistant
    "manager",            # people/product/program management as primary function
    "analyst",            # business, data, financial analyst (non-IB)
    "accountant",
    "auditor",
    "investment_banker",  # IB, capital markets, M&A advisory
    "sales",              # AE, BDR, SDR, enterprise sales, pre-sales (non-engineering)
    "operations",         # business ops, RevOps, PMO, supply chain (non-engineering)
    "legal",              # counsel, compliance, GRC, privacy
    "other",              # catch-all — prevents misfit into wrong category
]
```

Without `sales`, `operations`, `legal`, and `other`, the LLM forces misfit roles into
the closest wrong category (e.g. "Enterprise Sales Engineer" → `engineer`).

Many `normalized_roles` collapse into one intent (e.g. `ML_ENGINEER`, `SWE` → `engineer`).
One intent can span several normalized roles (e.g. `analyst` → `DATA_ANALYST`, `FINANCE`).

### Dual-sided design

| Side | Field | Cardinality | Example |
|------|-------|-------------|---------|
| Job | `role_intent` | **one** (single primary purpose per posting) | Per Scholas instructor → `educator` |
| User | `role_intents` | **many** (career tracks they're open to) | CS grad → `["engineer", "researcher"]` |

**Match rule:**

```python
NormalizedJob.role_intent.in_(user_profile.role_intents)
```

### Analyst / engineer / researcher boundary

`engineer` and `analyst` are separate intents. Data Scientist roles map to `researcher`
in the prompt (research-oriented) or `engineer` (production ML shipping — pick dominant).

**Implication:** A user with default `role_intents: ["engineer", "researcher"]` who
subscribes to `DATA_ANALYST_FULLTIME` pool will see data scientist roles (`researcher`)
but **not** pure data analyst roles (`analyst`). That's correct for CS grads looking for
engineering/research — they shouldn't get business analyst jobs by default.

Users who want data analyst roles must include `"analyst"` in their intent set:
`["engineer", "researcher", "analyst"]`.

**Profile-specific defaults:**

| User | Suggested default `role_intents` | Rationale |
|------|----------------------------------|-----------|
| General CS grad (Yatharth) | `["engineer", "researcher"]` | SWE / ML / backend focus |
| Data-focused (Ram) | `["engineer", "researcher", "analyst"]` | Subscribes to DATA_SCIENTIST + DATA_ANALYST pools; needs analyst intent for pure analyst roles |

Onboarding should derive or suggest intents from subscribed pools and resume signals.

### LLM prompt (job enrichment)

Add to `ENRICHMENT_SYSTEM_PROMPT` in `job_ingestion/app/ingestion/extractor/llm.py`:

```
role_intent: The primary CAREER TRACK of this role — what kind of professional is being
hired? Choose exactly one value from the taxonomy.

- engineer — building, developing, shipping software/systems hands-on
- researcher — research as primary output (research scientist, R&D, lab work)
- consultant — advising or implementing for clients as a service
- educator — teaching or training others as the primary function
- manager — coordination/leadership as primary function (EM, PM, TPM, ops leadership)
- analyst — analysis/reporting focus (business analyst, data analyst, financial analyst)
- accountant / auditor / investment_banker — finance track roles
- sales — revenue/sales as primary function (AE, BDR, SDR, enterprise sales)
- operations — business operations, RevOps, PMO, supply chain (non-engineering)
- legal — counsel, compliance, GRC, privacy
- other — does not fit any category above

Critical disambiguation:
"Technical Instructor (AWS Machine Learning)" → educator
"Data Engineering Instructor" → educator
"Machine Learning Engineer" → engineer
"Research Data Scientist" → researcher (or engineer if shipping production systems)
"Data Analyst" / "Business Analyst" → analyst
"Enterprise Sales Engineer" (quota-carrying sales) → sales
"Solutions Engineer" (technical demo/PoC) → engineer
"Solutions Consultant" (client advisory) → consultant
"Engineering Manager" with people-management focus → manager
```

### User profile — `role_intents`

Add to profile `constraints` or `preferences`:

```python
role_intents: list[str]  # e.g. ["engineer", "researcher"]
```

**How users get it:**

1. **Explicit** — onboarding / filters UI (multi-select career tracks)
2. **Derived** — LLM from resume + subscribed pools, user can edit
3. **Default** — profile-type-specific (see table above); never "show all"

**Distinct from existing fields:**

- `preferences.role_type` (`ic` | `manager`) — IC vs management *preference*
- `role_intents` — which career *tracks* the user is open to

### Backfill null handling

**Resolved:** Exclude nulls during rollout. Filter is null-safe:

```python
role_intents = user_profile.role_intents or DEFAULT_ROLE_INTENTS
filters.append(
    and_(
        NormalizedJob.role_intent.isnot(None),
        NormalizedJob.role_intent.in_(role_intents),
    )
)
```

Jobs with `role_intent = null` are not served until backfilled. Conservative during
rollout — temporarily lose some valid jobs, but Per Scholas won't leak through. After
backfill completes, null becomes an error state monitorable via taxonomy health dashboard.

DB column: nullable during migration, enforce non-null after backfill completes.

### Job-side touch points

| Layer | File(s) | Work |
|-------|---------|------|
| Constants | `job_ingestion/app/ingestion/constants_taxonomy.py` (or new file) | `ROLE_INTENTS` enum + coercion |
| DB schema | Alembic migration on `normalized_jobs` (+ `job_archive`) | `role_intent VARCHAR(64)` nullable until backfill |
| Pydantic schema | `job_ingestion/app/ingestion/extractor/llm.py` | Add to `JobEnrichment` and `BatchJobEnrichment` |
| LLM prompt | Same file, `ENRICHMENT_SYSTEM_PROMPT` | Prompt block above |
| Write-back | `job_ingestion/app/ingestion/enrichment_worker.py` | `_apply_enrichment_to_job`, `_recommendation_fields_from_enrichment` |
| Archive sync | `job_ingestion/app/ingestion/job_archive_sync.py` | Pass through |
| Read model | `recommendation_service/app/models/shared.py` | Add column to mirrored `NormalizedJob` |
| Tests | `job_ingestion/tests/test_extractors.py` (+ Per Scholas cases) | Parsing + write-back |
| Backfill | One-off script | Re-enrich active jobs |

### User-side touch points

| Layer | File(s) | Work |
|-------|---------|------|
| Profile schema | `profile_service/app/schemas/profile.py` | `role_intents: list[str] \| None` |
| Profile storage | `candidate_profiles.preferences` JSONB | Store `role_intents` array |
| Derivation | profile derivation from resume + pools | LLM or rules; Ram gets `analyst` |
| Web UI | `web/lib/profile/job-filters.ts`, filters/onboarding | Multi-select career tracks |
| Profile loader | `recommendation_service/app/services/profile_loader.py` | Expose `role_intents` on `UserProfile` |
| Retrieval filter | `recommendation_service/app/notification/retrieval.py` | Null-safe filter in `build_constraint_filters()` |
| Tests | `recommendation_service/tests/` | Intent filter + null exclusion cases |

### What this fixes

| Problem | Fixed by `role_intent`? |
|---------|-------------------------|
| Per Scholas instructors in ML/DE rankings | ✅ `educator` filtered out |
| Internal L&D instructor at a tech company | ✅ job-specific, not company blanket |
| Captivation / CACI cleared SWE roles | ❌ still `engineer` — needs Change 1+2 |
| Enterprise sales roles surfacing to engineers | ✅ `sales` intent + filter |

### Per Scholas — keep active as validation canary

**Resolved:** Keep Per Scholas **active** in `companies.json` (board: `perscholashires`).
Do not deactivate as interim insurance.

After backfill and retrieval filters are enabled, re-run recommendations for Ram/Yatharth
and verify Per Scholas instructor jobs:
- Are tagged `role_intent = educator` (not `engineer`)
- Drop out of rankings for users with `role_intents: ["engineer", "researcher", …]`
- No longer appear in email top-4

This is the end-to-end proof that `role_intent` fixes the misclassification without
company-level curation. `company_type` on `companies` is **deprecated** in favor of
job-level `role_intent`.

---

## Change 4 — Defense contractor corpus review

**Status:** Backlog (partially addressed by Change 1+2)

Mid-tier pollution from cleared contractors: CACI, Northrop Grumman, GDMS, AMERICAN
SYSTEMS, Captivation, Latitude, Wyetech. Per-job `requires_clearance` is the main fix;
company-level review may still be needed for contractors whose entire board is
clearance-gated and adds noise even after filtering.

---

## Filter stack (full recommendation gate)

Order of hard constraints in `build_constraint_filters()`:

```text
1. role_intent ∈ user.role_intents (null jobs excluded)  ← Change 3
2. job_domain ∈ user domains                             ← existing
3. requires_clearance=false if not has_clearance         ← Change 2
4. sponsorship, internship, salary, seniority            ← existing
5. job pools ∩ user subscribed pools                     ← existing
6. personalized scoring                                    ← existing
```

**Do not enable steps 1 or 3 in production until backfill is ≥80% complete** — otherwise
matching pool craters for test users during rollout.

---

## What's working (no change needed)

- Company dedup in emails (4 distinct companies each)
- Top 3 matches for both users are legitimate
- Score ceiling dip with larger pool is expected, not a concern
- Domain filter (`domain_filter_enabled`) — helps aerospace/defense domain jobs but does
  **not** catch Software-domain SWE roles that still require clearance

---

## Resolved decisions

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Clearance default | **`has_clearance: false`** — replace `exclude_security_clearance` |
| 2 | Clearance sponsorship wording | **Not** `requires_clearance: true`; sponsorship-available → `false` |
| 3 | Backfill null `role_intent` | **Exclude nulls** until backfilled; monitor nulls post-backfill |
| 4 | Full `ROLE_INTENTS` enum | Add **`sales`, `operations`, `legal`, `other`** to initial list |
| 5 | Analyst default gap | Data-focused profiles (Ram) get **`analyst`** in default intents |
| 6 | Retrieval filter timing | Wire filters only after **≥80% backfill** complete |
| 7 | Enrichment batching | **One pass** — ship Change 1+3 together; single prompt update, single backfill, one `extraction_version` bump |
| 8 | Per Scholas | **Keep active** — do not deactivate; use as a validation canary to confirm `role_intent` + `requires_clearance` filters work in live recommendation results |

---

## Suggested implementation order

1. **Constants + schema** — `ROLE_INTENTS`, `requires_clearance`, `has_clearance`; DB migrations
2. **Enrichment** — prompt blocks for both fields (with clearance disambiguation); write-back
3. **Backfill** — single pass on active jobs for `requires_clearance` + `role_intent`
4. **User profile** — `role_intents` + `has_clearance` fields, defaults, UI (parallel with 2–3)
5. **Wait for ≥80% backfill** before enabling retrieval filters
6. **Retrieval filters** — wire Change 2 + Change 3 in `build_constraint_filters()`
7. **Tests** — enrichment parsing, retrieval filters, Per Scholas + Captivation + sponsorship cases
8. **Validate** — re-run `scripts/run_user_recommendations.py`; check Ram/Yatharth rankings;
   confirm Per Scholas jobs are tagged `educator` and excluded from engineer/researcher intents
9. **Change 4** — defense corpus review if clearance filter leaves residual noise

---

## Change summary

| # | Change | Side | Fixes |
|---|--------|------|-------|
| 1 | `requires_clearance` | Job | Cleared defense contractor pollution |
| 2 | `has_clearance` retrieval filter | User constraint | Default-hide clearance jobs; migrate from `exclude_security_clearance` |
| 3 | `role_intent` / `role_intents` | Job + User | Per Scholas, educator/sales misclassification |
| 4 | Defense corpus review | Company list | Residual contractor noise |
