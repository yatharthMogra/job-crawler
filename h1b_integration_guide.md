# H-1B Dataset Integration — Implementation Guide

## Overview

This document specifies the full implementation of H-1B sponsorship data into the Career Match AI platform. The goal is to enrich job listings and recommendation scoring with real government sponsorship data from two sources: the **DOL Labor Condition Application (LCA) dataset** and the **USCIS H-1B Employer Data Hub**. The data surfaces on job cards for candidates who need sponsorship and feeds into the recommendation engine as a scoring signal.

---

## Data Sources

### Source 1: DOL LCA Dataset (Primary)
- **URL:** https://www.dol.gov/agencies/eta/foreign-labor/performance
- **Format:** Excel/CSV, published quarterly
- **Key fields:**
  - `EMPLOYER_NAME`
  - `SOC_CODE` (e.g. `15-1252`)
  - `SOC_TITLE`
  - `JOB_TITLE` (free text, not used for grouping)
  - `WAGE_RATE_OF_PAY_FROM`, `WAGE_UNIT_OF_PAY`
  - `WORKSITE_STATE`, `WORKSITE_CITY`
  - `CASE_STATUS` (`Certified` / `Denied` / `Withdrawn`)
  - `VISA_CLASS` (filter to `H-1B` only)
  - `RECEIVED_DATE`, `DECISION_DATE`
- **Use:** Intent signal — how many LCAs did this employer file per SOC code per year. Richer than USCIS because it has SOC codes and wage data.

### Source 2: USCIS H-1B Employer Data Hub (Outcome)
- **URL:** https://www.uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub
- **Format:** CSV download, fiscal year granularity
- **Key fields:**
  - `Employer`
  - `Initial Approvals`, `Initial Denials`
  - `Continuing Approvals`, `Continuing Denials`
  - `Fiscal Year`
  - `NAICS` (industry code — not used for role grouping)
- **Use:** Outcome signal — actual visa grant rate per employer. No role-level breakdown; used to compute employer-level approval rate only.

---

## SOC Code → Pool Family Mapping

This is the normalization anchor. SOC codes are standardized across the LCA dataset; map them once to your internal pool families. Store this as a static table — it changes rarely.

```sql
CREATE TABLE soc_to_pool_mapping (
    soc_code        VARCHAR(10) PRIMARY KEY,
    soc_title       TEXT NOT NULL,
    pool_family     VARCHAR(50) NOT NULL,  -- internal grouping, e.g. "SWE", "DATA_SCIENTIST"
    domain_hint     VARCHAR(50)            -- optional, matches your domain taxonomy
);
```

**Seed data (implement exactly as below):**

| SOC Code | SOC Title | pool_family | domain_hint |
|---|---|---|---|
| 15-1252 | Software Developers | SWE | Software |
| 15-1253 | Software Quality Assurance Analysts | SWE | Software |
| 15-1211 | Computer Systems Analysts | SWE | Software |
| 15-1299 | Computer Occupations, All Other | SWE | Software |
| 15-2051 | Data Scientists | DATA_SCIENTIST | Data_Analytics |
| 15-1243 | Database Architects | DATA_ENGINEER | Data_Analytics |
| 15-1245 | Database Administrators | DATA_ENGINEER | Data_Analytics |
| 15-2041 | Statisticians | DATA_ANALYST | Data_Analytics |
| 15-2031 | Operations Research Analysts | DATA_ANALYST | Data_Analytics |
| 15-1244 | Network and Computer Systems Administrators | DEVOPS_ENGINEER | Software |
| 15-1212 | Information Security Analysts | SECURITY_ENGINEER | Software |
| 15-1232 | Computer User Support Specialists | SUPPORT_ENGINEER | Software |
| 15-1241 | Computer Network Architects | DEVOPS_ENGINEER | Software |
| 11-3021 | Computer and Information Systems Managers | TECHNICAL_PROGRAM_MANAGER | Management |
| 11-9041 | Architectural and Engineering Managers | TECHNICAL_PROGRAM_MANAGER | Management |
| 17-2061 | Electrical Engineers | HARDWARE_ENGINEER | Hardware_Electrical |
| 17-2071 | Electrical and Electronics Engineers | HARDWARE_ENGINEER | Hardware_Electrical |
| 17-2141 | Mechanical Engineers | SYSTEMS_ENGINEER | Mechanical |
| 17-2051 | Civil Engineers | SYSTEMS_ENGINEER | Mechanical |
| 17-2112 | Industrial Engineers | SYSTEMS_ENGINEER | Industrial_Automation |
| 17-2011 | Aerospace Engineers | AEROSPACE_ENGINEER | Aerospace_Defense |
| 17-2199 | Engineers, All Other | SYSTEMS_ENGINEER | NULL |
| 19-1042 | Medical Scientists | RESEARCH_SCIENTIST | Research_Science |
| 19-2041 | Environmental Scientists | RESEARCH_SCIENTIST | Research_Science |
| 19-2099 | Physical Scientists, All Other | RESEARCH_SCIENTIST | Research_Science |
| 15-2099 | Mathematical Science Occupations, All Other | DATA_SCIENTIST | Data_Analytics |

> **Note:** Extend this table as you encounter SOC codes in the data that are not listed above. Do not delete existing rows — append only.

---

## Database Schema

### Raw storage tables (built from LCA/USCIS CSVs)

```sql
-- Raw LCA rows, one per certified/denied application
-- Load all H-1B rows here; normalize in a separate pass
CREATE TABLE lca_raw (
    id                  BIGSERIAL PRIMARY KEY,
    employer_name_raw   TEXT NOT NULL,
    soc_code            VARCHAR(10),
    soc_title           TEXT,
    job_title           TEXT,
    wage_from           NUMERIC,
    wage_unit           VARCHAR(20),       -- 'Year', 'Hour', etc.
    worksite_state      VARCHAR(2),
    worksite_city       TEXT,
    case_status         VARCHAR(30),       -- 'Certified', 'Denied', 'Withdrawn'
    visa_class          VARCHAR(10),       -- always 'H-1B' after filter
    received_date       DATE,
    decision_date       DATE,
    fiscal_year         INTEGER NOT NULL,
    source_file         TEXT               -- track which quarterly file this came from
);

-- Raw USCIS employer-level rows
CREATE TABLE uscis_raw (
    id                      BIGSERIAL PRIMARY KEY,
    employer_name_raw       TEXT NOT NULL,
    naics_code              VARCHAR(10),
    fiscal_year             INTEGER NOT NULL,
    initial_approvals       INTEGER DEFAULT 0,
    initial_denials         INTEGER DEFAULT 0,
    continuing_approvals    INTEGER DEFAULT 0,
    continuing_denials      INTEGER DEFAULT 0,
    source_file             TEXT
);
```

### Normalized employer name table

```sql
-- Canonical employer name registry
-- All matching goes through this table
CREATE TABLE h1b_employers (
    id                  SERIAL PRIMARY KEY,
    employer_name_norm  TEXT NOT NULL UNIQUE,   -- after normalization rules
    company_id          INTEGER REFERENCES companies(id),  -- NULL until matched
    match_method        VARCHAR(20),    -- 'exact', 'fuzzy_auto', 'manual', 'unmatched'
    match_confidence    NUMERIC(4,3),   -- 0.0–1.0 for fuzzy matches
    reviewed_at         TIMESTAMP,
    created_at          TIMESTAMP DEFAULT NOW()
);

-- Maps raw employer names to canonical normalized name
CREATE TABLE h1b_employer_aliases (
    employer_name_raw   TEXT PRIMARY KEY,
    employer_name_norm  TEXT NOT NULL REFERENCES h1b_employers(employer_name_norm),
    first_seen_year     INTEGER
);
```

### Aggregated stats tables

```sql
-- LCA stats per employer × SOC code × year
-- Built by aggregation job from lca_raw
CREATE TABLE h1b_lca_stats (
    id                  SERIAL PRIMARY KEY,
    employer_name_norm  TEXT NOT NULL REFERENCES h1b_employers(employer_name_norm),
    company_id          INTEGER REFERENCES companies(id),
    soc_code            VARCHAR(10) REFERENCES soc_to_pool_mapping(soc_code),
    pool_family         VARCHAR(50),        -- denormalized from soc_to_pool_mapping
    fiscal_year         INTEGER NOT NULL,
    lca_certified       INTEGER DEFAULT 0,
    lca_denied          INTEGER DEFAULT 0,
    lca_withdrawn       INTEGER DEFAULT 0,
    avg_wage_annual     NUMERIC,            -- normalized to annual
    primary_state       VARCHAR(2),         -- most common worksite state for this combo
    UNIQUE (employer_name_norm, soc_code, fiscal_year)
);

-- USCIS outcome stats per employer × year (no role breakdown available)
CREATE TABLE h1b_uscis_stats (
    id                          SERIAL PRIMARY KEY,
    employer_name_norm          TEXT NOT NULL REFERENCES h1b_employers(employer_name_norm),
    company_id                  INTEGER REFERENCES companies(id),
    fiscal_year                 INTEGER NOT NULL,
    initial_approvals           INTEGER DEFAULT 0,
    initial_denials             INTEGER DEFAULT 0,
    continuing_approvals        INTEGER DEFAULT 0,
    continuing_denials          INTEGER DEFAULT 0,
    approval_rate               NUMERIC(5,4),   -- computed: initial_approvals / (initial_approvals + initial_denials)
    UNIQUE (employer_name_norm, fiscal_year)
);

-- Final rollup — what the application actually reads
-- Rebuilt nightly after ingestion
CREATE TABLE h1b_company_pool_summary (
    company_id          INTEGER NOT NULL REFERENCES companies(id),
    pool_family         VARCHAR(50) NOT NULL,
    years_covered       INTEGER[],          -- e.g. [2021, 2022, 2023, 2024]
    latest_year         INTEGER,
    total_lca_3yr       INTEGER,            -- LCA certified over last 3 fiscal years
    total_h1b_3yr       INTEGER,            -- USCIS initial approvals over last 3 FY (company-level, prorated)
    approval_rate_3yr   NUMERIC(5,4),       -- USCIS approval rate averaged over 3yr
    is_top_sponsor      BOOLEAN,            -- true if top 500 sponsors for this pool_family
    last_updated        TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (company_id, pool_family)
);
```

---

## Employer Name Normalization Pipeline

Implement as a standalone Python script: `job_ingestion/scripts/normalize_h1b_employers.py`

### Normalization rules (apply in order)

```python
import re

LEGAL_SUFFIXES = [
    r'\bLLC\b', r'\bINC\b', r'\bINC\.\b', r'\bCORP\b', r'\bCORPORATION\b',
    r'\bLTD\b', r'\bL\.P\.\b', r'\bLP\b', r'\bLLP\b', r'\bPLC\b',
    r'\bCO\b', r'\bCO\.\b', r'\bGROUP\b', r'\bHOLDINGS\b', r'\bHOLDING\b',
    r'\bENTERPRISES\b', r'\bSOLUTIONS\b', r'\bSERVICES\b', r'\bTECHNOLOGIES\b',
    r'\bTECHNOLOGY\b'
]

GEO_SUFFIXES = [
    r'\bUSA\b', r'\bUS\b', r'\bU\.S\.\b', r'\bAMERICA\b', r'\bNORTH AMERICA\b',
    r'\bAMERICAS\b'
]

def normalize_employer_name(raw: str) -> str:
    name = raw.upper().strip()
    # Remove punctuation except spaces and hyphens
    name = re.sub(r"[^\w\s\-]", " ", name)
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    # Strip legal suffixes (repeat until stable — handles "LLC INC" chains)
    prev = None
    while prev != name:
        prev = name
        for suffix in LEGAL_SUFFIXES:
            name = re.sub(suffix, "", name).strip()
    # Strip geographic qualifiers
    for geo in GEO_SUFFIXES:
        name = re.sub(geo, "", name).strip()
    # Final collapse
    name = re.sub(r"\s+", " ", name).strip()
    return name
```

### Three-pass matching pipeline

**Pass 1 — Exact match** after normalization
- Normalize both the LCA employer name and your `companies.name`
- If normalized strings match exactly → `match_method = 'exact'`, `match_confidence = 1.0`
- Expected coverage: ~60-65% of volume

**Pass 2 — Fuzzy match**
- Use `rapidfuzz.fuzz.token_sort_ratio` against all normalized company names in your DB
- Threshold: score ≥ 88 → `match_method = 'fuzzy_auto'`, store confidence
- Score 75–87 → flag for manual review (insert to review queue with `match_method = 'fuzzy_candidate'`)
- Score < 75 → `match_method = 'unmatched'`
- Install: `pip install rapidfuzz`

**Pass 3 — Manual review queue**
- Query: unmatched or fuzzy_candidate employers with `lca_certified > 50` in any single year
- Low-volume unmatched employers stay unlinked — not worth operator time
- Build a simple admin endpoint `GET /admin/h1b-review-queue` returning these rows sorted by volume desc

```python
# Pass 2 implementation sketch
from rapidfuzz import fuzz, process

def fuzzy_match_employer(norm_name: str, company_lookup: dict[str, int]) -> tuple[str | None, float]:
    """
    company_lookup: {normalized_company_name: company_id}
    Returns (matched_norm_name, score) or (None, 0.0)
    """
    result = process.extractOne(
        norm_name,
        company_lookup.keys(),
        scorer=fuzz.token_sort_ratio,
        score_cutoff=75
    )
    if result is None:
        return None, 0.0
    match_name, score, _ = result
    return match_name, score / 100.0
```

---

## Ingestion Pipeline

Implement as an APScheduler job in `job_ingestion/app/schedulers/h1b_ingestion.py`. Run annually (fiscal year data is published once/year, quarterly updates are minor).

### Steps

1. **Download** — fetch latest LCA Performance Data file from DOL. Fiscal year runs Oct–Sep; latest full-year file is typically published Q1 of the following calendar year.

2. **Load raw** — parse CSV/Excel, filter `VISA_CLASS == 'H-1B'`, insert all rows to `lca_raw`. Track `source_file` so re-runs are idempotent (use `ON CONFLICT DO NOTHING` on a unique constraint over `employer_name_raw + soc_code + received_date`).

3. **Normalize employers** — run the three-pass normalization pipeline, upsert to `h1b_employers` and `h1b_employer_aliases`.

4. **Aggregate LCA stats** — group `lca_raw` by `(employer_name_norm, soc_code, fiscal_year)`, insert to `h1b_lca_stats`. Join `soc_to_pool_mapping` to populate `pool_family`. Normalize wages to annual (hourly × 2080).

5. **Download and load USCIS data** — same pattern, insert to `uscis_raw`, aggregate to `h1b_uscis_stats`, compute `approval_rate`.

6. **Rebuild summary** — truncate and rebuild `h1b_company_pool_summary` for all companies that have a `company_id` match. Use last 3 fiscal years. Flag `is_top_sponsor` as top 500 by `total_lca_3yr` per `pool_family`.

7. **Log and alert** — log count of matched vs unmatched employers above 50-LCA threshold. If match rate for high-volume employers < 80%, alert — something may have changed in normalization or your company list.

---

## Integration Points

### 1. Job listing display

Add to the job detail response in `recommendation_service` (or wherever job cards are assembled):

```python
# New field on job detail response
class H1BSponsorshipInfo(BaseModel):
    pool_family: str
    total_lca_3yr: int
    approval_rate_3yr: float | None  # None if USCIS data unavailable for this employer
    is_top_sponsor: bool
    years_covered: list[int]

# Add to job response only when candidate profile has sponsorship_needed = True
# or when the job detail endpoint is called directly (always show)
```

**Display copy guidance (for frontend, implement later):**
- `is_top_sponsor = True`: "Top H-1B sponsor · {total_lca_3yr} software engineering visas (last 3 years)"
- `approval_rate_3yr >= 0.90`: show approval rate
- `total_lca_3yr < 10`: show "Limited H-1B history in this role category"
- `company_id` not in summary table: show nothing (no data)

### 2. Candidate profile field

Add to `profile_service`:

```python
class CandidateProfile(BaseModel):
    # ... existing fields ...
    sponsorship_needed: bool = False   # True for F-1/OPT/H-4 candidates
```

When `sponsorship_needed = True`:
- H-1B data is shown on job cards
- Sponsorship signal feeds into scoring (see below)

### 3. Recommendation scoring

Add a `sponsorship_score` component to `personal_score`. Add it as a soft bonus, not a hard filter — a company with zero sponsorship history should still appear but rank lower, not disappear.

```python
def compute_sponsorship_score(
    company_id: int,
    pool_family: str,
    candidate_needs_sponsorship: bool,
    summary_lookup: dict  # preloaded from h1b_company_pool_summary
) -> float:
    """Returns 0.0–1.0 bonus weight"""
    if not candidate_needs_sponsorship:
        return 0.5  # neutral — don't penalize or boost when not relevant

    key = (company_id, pool_family)
    if key not in summary_lookup:
        return 0.1  # no data — slight penalty vs known sponsors

    row = summary_lookup[key]
    if row.is_top_sponsor:
        return 1.0
    if row.total_lca_3yr >= 20:
        return 0.8
    if row.total_lca_3yr >= 5:
        return 0.5
    return 0.2  # has data but very few filings
```

**Updated scoring formula:**

```
personal_score = 0.35×capability_overlap
               + 0.22×skill_overlap
               + 0.18×location_alignment
               + 0.13×comp_alignment
               + 0.12×sponsorship_score     ← new, only weighted when sponsorship_needed=True
               + seniority_soft_penalty
```

When `sponsorship_needed = False`, collapse `sponsorship_score` to 0 and redistribute its weight back proportionally to the original formula weights.

---

## Admin Dashboard — New Tab

Add an **H-1B** tab to the existing admin dashboard alongside Pipeline · Sources · Cost · Jobs · Taxonomy.

### Endpoints to build

```
GET /admin/h1b-stats
    → total matched employers, total LCA rows by year, match rate %

GET /admin/h1b-review-queue
    → unmatched/fuzzy_candidate employers with total_lca > 50, sorted by volume
    → allow operator to manually set company_id via PATCH /admin/h1b-employer/{id}

GET /admin/h1b-coverage
    → for each pool_family: how many of your tracked companies have h1b data
    → flags pool_families with < 50% coverage

PATCH /admin/h1b-employer/{id}
    → manually link h1b_employers.id to a company_id
    → triggers immediate recompute of summary for that company
```

---

## Implementation Order

Do these in sequence. Do not skip ahead.

1. **Schema migration** — create all tables above. Add `sponsorship_needed` to candidate profile schema.

2. **SOC mapping seed** — populate `soc_to_pool_mapping` with the table provided above.

3. **Normalization script** — implement `normalize_employer_name()` and the three-pass matching pipeline. Test against your existing `companies` table. Log match rate before moving on.

4. **LCA ingestion** — download latest full-year LCA file (FY2024 is the target), load `lca_raw`, run normalization, aggregate to `h1b_lca_stats`.

5. **USCIS ingestion** — download FY2024 USCIS employer hub data, load `uscis_raw`, aggregate to `h1b_uscis_stats`.

6. **Summary rebuild** — implement and run the `h1b_company_pool_summary` rebuild.

7. **Admin endpoints** — `/admin/h1b-stats` and `/admin/h1b-review-queue` first. Run manual review pass on high-volume unmatched employers.

8. **Profile field** — add `sponsorship_needed` to `CandidateProfile`. Wire to existing candidate data.

9. **Scoring integration** — add `sponsorship_score` to `build_personal_score()`. Keep old formula as fallback while testing.

10. **Job detail response** — add `H1BSponsorshipInfo` to job card output. Gate display on `sponsorship_needed`.

11. **APScheduler job** — wrap ingestion in a scheduled job. Annual cadence, triggered manually first run.

---

## Key Invariants to Preserve

- `lca_raw` and `uscis_raw` are append-only source-of-truth tables. Never delete rows — re-runs use `ON CONFLICT DO NOTHING`.
- `h1b_company_pool_summary` is a fully derived table — always safe to truncate and rebuild.
- `company_id` on any H-1B table is nullable. Unmatched employers are valid rows, not errors.
- `pool_family` grouping in the display layer must match the candidate's subscribed pools. Do not show "DATA_ENGINEER H-1B history" to a candidate subscribed only to SWE pools.
- Never hard-filter jobs by sponsorship history. It is always a soft scoring signal or display annotation, never a retrieval gate.

---

## Open Questions (resolve before Step 9)

1. **Weight of sponsorship signal** — 0.12 proposed above. Validate on a test run: compare Ram's and Yatharth's top-20 rankings with and without this signal before committing to the weight.

2. **Backfill years** — current proposal uses 3 fiscal years. For newer companies (founded post-2020), 1-year window may be more appropriate. Consider `MIN(3, years_of_data_available)` as denominator.

3. **Pool family granularity in display** — the summary table stores `pool_family` (e.g. "SWE"). At display time, all SWE-family pools (BACKEND_ENGINEER, FRONTEND_ENGINEER, etc.) should map to the same `pool_family = "SWE"` row. Confirm this mapping is consistent with `soc_to_pool_mapping`.

4. **Wage data use** — LCA contains `avg_wage_annual` per SOC/employer. This could supplement your existing `comp_alignment` scoring with more granular data than job postings provide. Defer to a future iteration but preserve the field.
