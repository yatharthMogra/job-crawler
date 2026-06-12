# Recommendation Engine Fixes — Directing Guide

Covers three implementation problems. Each section has context, exact changes required,
and a build sequence. Follow in order — location scoring first, then LLM prompt fixes.

---

## Problem 1 — Location Preferences

### What's broken

`preferred_locations` is currently a flat string array with no structure. When empty,
the scoring treats all locations neutrally — India, LatAm, Germany, and New York all
score identically. A US-based candidate with no explicit preference should default to
preferring US/remote, not globally neutral.

### 1.1 Schema changes

```sql
-- Add structured location columns to candidate_profiles.
-- Keep preferred_locations as a legacy column for now but stop reading from it.

ALTER TABLE candidate_profiles
    ADD COLUMN preferred_countries VARCHAR[]  DEFAULT '{}',
    ADD COLUMN preferred_states    VARCHAR[]  DEFAULT '{}',
    ADD COLUMN preferred_cities    VARCHAR[]  DEFAULT '{}';

-- Migrate existing preferred_locations data where parseable.
-- For current users (2 rows), do this manually — not worth an automated migration.
```

Store countries as ISO 3166-1 alpha-2 codes: `US`, `CA`, `GB`, `DE`, `AU`, etc.
Store states as abbreviations within US context: `NY`, `CA`, `WA`. For non-US, use
region names as-is (e.g., `Ontario`).
Store cities as display strings: `New York`, `San Francisco`, `Seattle`.

### 1.2 Job-side country field

Location scoring currently operates on free-text `normalized_jobs.location` strings.
Add a derived `job_country` column that the deterministic extractor populates at
ingestion time, so scoring doesn't do string parsing at query time.

```sql
ALTER TABLE normalized_jobs ADD COLUMN job_country VARCHAR(2);
CREATE INDEX idx_normalized_jobs_job_country ON normalized_jobs(job_country);
```

**Deterministic extractor addition** (`app/ingestion/extractor/deterministic.py`):

```python
# Simple country extraction — covers the majority of location strings
# in the current corpus without a geocoding dependency.

COUNTRY_SIGNALS: list[tuple[list[str], str]] = [
    # US signals
    (["united states", "usa", "u.s.a", " us ", "remote - us", "remote - united"],  "US"),
    (["new york", "san francisco", "seattle", "boston", "chicago",
      "los angeles", "austin", "denver", "atlanta", "washington, d.c",
      " ny", " ca", " wa", " tx", " ma", " co", " ga", " fl", " va",
      " dc", " nc", " il", " oh", " pa", " az", " mn"], "US"),
    # Canada
    (["canada", " on", " bc", " qc", "ontario", "british columbia",
      "toronto", "montreal", "vancouver"], "CA"),
    # UK
    (["united kingdom", " uk", "england", "london", "manchester",
      "edinburgh", "bristol"], "GB"),
    # Germany
    (["germany", "deutschland", "berlin", "munich", "hamburg", "frankfurt"], "DE"),
    # India
    (["india", "bengaluru", "hyderabad", "bangalore", "pune", "chennai",
      "mumbai", "new delhi", "gurgaon", "noida"], "IN"),
    # Australia
    (["australia", "sydney", "melbourne", "brisbane", "perth"], "AU"),
    # Remote (no country)
    (["remote", "anywhere", "worldwide", "global"], None),
]

def extract_job_country(location: str | None) -> str | None:
    """
    Returns ISO 3166-1 alpha-2 country code or None.
    None means remote/global/unknown — handled separately in scoring.
    """
    if not location:
        return None
    loc_lower = location.lower()

    # Remote check first
    if any(sig in loc_lower for sig in ["remote", "anywhere", "worldwide", "global"]):
        return None   # let remote_type field handle this

    for signals, code in COUNTRY_SIGNALS:
        if any(sig in loc_lower for sig in signals):
            return code

    return None   # unknown — score as neutral
```

Call `extract_job_country` in every platform's `_extract_*` function alongside the
other deterministic fields, and write the result to `job_country` in `normalized_jobs`.

Backfill active jobs with a one-off script:
```python
# scripts/backfill_job_country.py
# SELECT id, location FROM normalized_jobs WHERE job_country IS NULL AND is_active = TRUE
# For each row: update job_country = extract_job_country(location)
# Batch in groups of 500, commit each batch
```

### 1.3 Scoring changes

Replace the current location alignment function in `app/recommendation/scoring.py`:

```python
from app.ingestion.extractor.deterministic import extract_job_country


def get_effective_countries(candidate: CandidateProfile) -> list[str]:
    """
    Returns the candidate's effective country preferences.
    When preferred_countries is empty, derive a soft default from work_authorization
    so that US-based candidates don't get international jobs scored neutrally.
    """
    if candidate.preferred_countries:
        return [c.upper() for c in candidate.preferred_countries]

    # Derive from work authorization
    US_AUTH_TYPES = {
        "US_CITIZEN", "PERMANENT_RESIDENT", "GREEN_CARD",
        "OPT", "CPT", "H1B", "TN", "OTHER_US",
    }
    if candidate.work_authorization in US_AUTH_TYPES:
        return ["US"]   # soft default for US-authorized candidates

    return []   # truly no preference — keep neutral


def compute_location_score(job: NormalizedJob, candidate: CandidateProfile) -> float:
    """
    Hierarchical location scoring:
      1. Remote jobs bypass country check
      2. Country match is the primary gate
      3. State and city matches add bonus on top
    """
    # Remote: bypass country check
    if job.remote_type in ("REMOTE", "FULLY_REMOTE", "REMOTE_OK"):
        if candidate.remote_preference in ("REMOTE", "HYBRID_OR_REMOTE", "NO_PREFERENCE", None):
            return 1.0
        return 0.7   # job is remote but candidate prefers onsite

    effective_countries = get_effective_countries(candidate)

    if not effective_countries:
        return 0.5   # truly no country preference — neutral

    # Country gate
    job_country = job.job_country or extract_job_country(job.location)
    if job_country is None:
        # Unknown country — treat as partial match
        return 0.4

    if job_country not in effective_countries:
        return 0.15  # country mismatch — hard penalty

    # Country matches — check state bonus
    if candidate.preferred_states:
        job_state = _extract_state(job.location)
        if job_state and job_state.upper() in [s.upper() for s in candidate.preferred_states]:
            # State matches — check city bonus
            if candidate.preferred_cities:
                job_city = _extract_city(job.location)
                if job_city and job_city.lower() in [c.lower() for c in candidate.preferred_cities]:
                    return 1.0   # city match
                return 0.8       # state match, city miss
            return 0.9           # state match, no city preference
        return 0.55              # country match, state miss

    return 0.75   # country match, no state/city preference


def _extract_state(location: str | None) -> str | None:
    """Extract US state abbreviation from location string."""
    if not location:
        return None
    import re
    # Pattern: ", NY" or "New York, NY" or "New York, NY, USA"
    match = re.search(r",\s*([A-Z]{2})(?:\s*,|\s*$|\s+)", location)
    if match:
        return match.group(1)
    # Spelled-out state names
    STATE_MAP = {
        "new york": "NY", "california": "CA", "washington": "WA",
        "texas": "TX", "massachusetts": "MA", "colorado": "CO",
        "virginia": "VA", "illinois": "IL", "georgia": "GA",
        "florida": "FL", "pennsylvania": "PA", "north carolina": "NC",
        "arizona": "AZ", "minnesota": "MN", "ohio": "OH",
    }
    loc_lower = location.lower()
    for name, abbr in STATE_MAP.items():
        if name in loc_lower:
            return abbr
    return None


def _extract_city(location: str | None) -> str | None:
    """Return the first segment of the location string as a city name proxy."""
    if not location:
        return None
    return location.split(",")[0].strip()
```

### 1.4 Build sequence

1. Schema migration — add `preferred_countries/states/cities` to `candidate_profiles`,
   add `job_country` to `normalized_jobs`.
2. Add `extract_job_country` to deterministic extractor. Wire into all `_extract_*`
   functions (greenhouse, lever, ashby, workday, oracle_hcm, icims).
3. Run backfill script for active `job_country` values.
4. Replace `compute_location_score` with new version.
5. Update Yatharth profile: `preferred_countries: ["US"]`, `preferred_cities: ["New York"]`.
   Update Ram profile: `preferred_countries: ["US"]` (no city preference — he has none set).
6. Run recommendation loop, verify Ram no longer receives India/LatAm top-4 jobs.

---

## Problem 2a — LLM Domain Assignment Errors

### What's broken

The LLM is assigning `job_domain` based on the company's industry instead of the job's
content. Examples:
- `HARDWARE_ENGINEER` role at Amex → tagged `Business` (Amex is a financial company)
  → should be `Hardware_Electrical` (the job is hardware engineering)
- `OPERATIONS` role at a tech company → tagged `Software`
  → should be `Business` (the job is operations, not software)

### 2a.1 Prompt change

In the enrichment prompt, **replace the current `job_domain` block** with:

```
job_domain: The professional discipline this role belongs to.

CRITICAL RULE: Assign based on what THIS JOB requires the person to DO each day —
not what the company's industry is. The company's industry never determines the domain.

Correct examples:
  ✓ "Hardware Engineer" at American Express → Hardware_Electrical
    (the work is hardware engineering; Amex's finance industry is irrelevant)
  ✓ "Data Analyst" at RTX/Boeing → Data_Analytics
    (the work is data analysis; the defense industry is irrelevant)
  ✓ "Operations Manager, Supply Chain" at any company → Management
    (the work is managing operations; not Software, not Business)
  ✓ "Software Engineer, Enterprise Applications" at Boeing → Software
    (the job builds internal software tools; no aerospace expertise needed)
  ✓ "Software Engineer, Avionics Systems" at Boeing → Aerospace_Defense
    (the job requires avionics domain knowledge — DO-178C, flight software safety)
  ✓ "Finance Analyst" at a SaaS company → Business
    (the work is financial analysis; the tech industry context doesn't matter)

Wrong examples:
  ✗ "Hardware Engineer" at Amex → Business   (wrong: based on company industry)
  ✗ "Data Analyst" at RTX → Aerospace_Defense (wrong: based on company industry)
  ✗ "Software Engineer" at Boeing always → Aerospace_Defense (wrong: depends on job content)

Domain definitions:
[keep existing definitions unchanged — the rule above is the critical addition]
```

### 2a.2 Reprocessing scope

Target only the known mismatch cases. Run a re-enrichment pass filtered to:
```sql
-- Jobs to reprocess for domain fix
SELECT id FROM normalized_jobs
WHERE is_active = TRUE
  AND processing_state = 'success'
  AND (
    -- HARDWARE_ENGINEER role but not Hardware_Electrical domain
    (normalized_roles @> ARRAY['HARDWARE_ENGINEER']
     AND job_domain NOT IN ('Hardware_Electrical', 'Aerospace_Defense'))
    OR
    -- OPERATIONS role but Software domain
    (normalized_roles @> ARRAY['OPERATIONS']
     AND job_domain = 'Software')
  );
```

Estimated scope: ~400 jobs. Full re-enrichment (not domain-only) is fine since
the throughput is fast and the prompt fix improves overall quality.

---

## Problem 2b — Missing Pools in LLM Vocabulary

### What's broken

New pools from the domain taxonomy spec (taxonomy.py) were added to `POOL_DOMAIN_MAP`
but not to the LLM enrichment prompt's pool vocabulary list. The LLM cannot assign a
pool it doesn't know about.

Known missing pools with zero assignments in current data:
- `RESEARCH_SCIENTIST_FULLTIME` (Research_Science domain) — 120+ Research_Science jobs poolless
- `RESEARCH_SCIENTIST_INTERNSHIP` (Research_Science domain)

Pools that ARE working (confirmed by appearance in the pool table):
- `HARDWARE_ENGINEER_FULLTIME` ✅
- `SYSTEMS_ENGINEER_FULLTIME` ✅
- `AEROSPACE_ENGINEER_FULLTIME` — check if assigned anywhere; may be missing too

### 2b.1 Prompt addition

In the enrichment prompt's pool vocabulary section, add the following entries with
descriptions that tell the LLM when to use them:

```
RESEARCH_SCIENTIST_FULLTIME:
  Use for roles where the primary work is conducting scientific research,
  running laboratory experiments, or performing academic-style investigation.
  Typical titles: Research Scientist, Principal Scientist, Staff Scientist,
  Senior Scientist, Scientist I/II/III, Research Engineer (in a research lab
  context), Postdoctoral Researcher, Research Fellow.
  Domain: Research_Science.

RESEARCH_SCIENTIST_INTERNSHIP:
  Same as above for internship/co-op positions.
  Domain: Research_Science.

LIFE_SCIENTIST_FULLTIME:
  Use for roles focused on biological, chemical, or biomedical sciences where
  the primary work is laboratory or clinical research.
  Typical titles: Bioscientist, Biochemist, Biologist, Chemist, Biomedical
  Scientist, Lab Scientist, Research Associate (biosciences context).
  Domain: Research_Science.
  Note: Use RESEARCH_SCIENTIST for broader research roles; use LIFE_SCIENTIST
  specifically for biology/chemistry/biomedical roles.

AEROSPACE_ENGINEER_FULLTIME:
  Use for roles designing, testing, or developing aerospace vehicles, systems,
  or components — structural, propulsion, aerodynamics, flight dynamics.
  NOT for software engineers at aerospace companies (use SWE or BACKEND_ENGINEER
  if the work is general software, or SYSTEMS_ENGINEER if it's systems-level).
  Domain: Aerospace_Defense.
```

Also explicitly document `SYSTEMS_ENGINEER_FULLTIME` to reduce ambiguity:
```
SYSTEMS_ENGINEER_FULLTIME:
  Use for roles integrating complex hardware/software systems, especially in
  aerospace, defense, or industrial contexts requiring systems-level thinking.
  NOT for "platform engineer" or "distributed systems engineer" at tech companies —
  those should use DEVOPS_ENGINEER or BACKEND_ENGINEER.
  Domain: Aerospace_Defense.
```

### 2b.2 Add LIFE_SCIENTIST to taxonomy.py

```python
# In POOL_DOMAIN_MAP (app/ingestion/taxonomy.py):
"LIFE_SCIENTIST_FULLTIME":    "Research_Science",   # new pool
"LIFE_SCIENTIST_INTERNSHIP":  "Research_Science",   # new pool
```

### 2b.3 Reprocessing scope

Target Research_Science domain jobs with empty pools:
```sql
SELECT id FROM normalized_jobs
WHERE is_active = TRUE
  AND job_domain = 'Research_Science'
  AND (retrieval_pools IS NULL OR retrieval_pools = '{}')
  AND processing_state = 'success';
```

Estimated scope: ~120 jobs.

---

## Problem 2c — Aerospace vs Software Context at Defense Companies

### What's broken

The LLM frequently tags all software engineering roles at Boeing/RTX/Honeywell as
`Aerospace_Defense` domain, even when the job is general enterprise software with no
aerospace expertise required. This leaves software jobs at defense companies invisible
to software candidates.

The converse also happens: some genuinely aerospace software roles get tagged `Software`
because the LLM sees "Python" and "backend" without reading the aerospace-specific context.

### 2c.1 Prompt addition

Add a disambiguation block immediately after the `Aerospace_Defense` domain definition:

```
AEROSPACE_DEFENSE vs SOFTWARE — how to distinguish at defense/aerospace companies:

A software job at Boeing, RTX, Northrop, Honeywell, or similar should be tagged:

  → Software  if ALL of the following are true:
      • The job description is about general software development
        (web apps, APIs, internal tools, data platforms, enterprise systems)
      • The description makes no reference to aerospace/defense-specific
        knowledge requirements (avionics, flight software, missile systems,
        radar, DO-178C, MIL-STD, weapons, space systems)
      • A competent generalist software engineer could apply without
        aerospace domain background
      Examples: "Software Engineer, IT Systems @ Boeing"
                "Software Engineer, Data Platform @ RTX"
                "Full Stack Developer, Internal Tools @ Honeywell"

  → Aerospace_Defense  if ANY of the following are true:
      • The description explicitly mentions aerospace/defense domain work
        (avionics, flight software, mission systems, weapons, radar, satellites,
        space systems, guidance systems, C2 systems)
      • The description mentions domain-specific standards
        (DO-178C, DO-254, MIL-STD-461, ITAR, ICD, SIL, ARINC)
      • The title itself signals defense/aerospace context
        (Mission Systems, Avionics, Ground Systems, Flight Software,
         Space Systems, Electronic Warfare, Ballistic, Propulsion)
      • The job requires or prefers security clearance
      Examples: "Software Engineer, Mission Systems @ RTX"
                "Avionics Software Engineer @ Boeing"
                "Flight Software Engineer @ SpaceX"
```

### 2c.2 Reprocessing scope

Target the 136 SWE-role + Aerospace_Defense-domain no-pool jobs. Some will correctly
stay as Aerospace_Defense after re-enrichment (genuine aerospace software). Others
will flip to Software domain and gain `SWE_FULLTIME` or `BACKEND_ENGINEER_FULLTIME`
pool — these then become visible to software candidates.

```sql
-- Jobs to reprocess for aerospace/software disambiguation
SELECT id FROM normalized_jobs
WHERE is_active = TRUE
  AND job_domain = 'Aerospace_Defense'
  AND normalized_roles @> ARRAY['SWE']
  AND (retrieval_pools IS NULL OR retrieval_pools = '{}')
  AND processing_state = 'success'
  AND company_id IN (
      -- Only Boeing, RTX, Honeywell, similar dual-use companies
      -- where this ambiguity actually occurs
      SELECT id FROM companies
      WHERE platform IN ('workday', 'oracle_hcm')
  );
```

Estimated scope: ~100-136 jobs.

---

## Build Sequence (all problems combined)

| Step | Action | Scope | Risk |
|---|---|---|---|
| 1 | Schema migration (location fields + job_country) | DDL only | None |
| 2 | Add `extract_job_country` to deterministic extractor | Code | Low |
| 3 | Backfill `job_country` on active jobs | ~6,000 rows | Low |
| 4 | Replace `compute_location_score` | Scoring only | Medium — test after |
| 5 | Update user profiles (Yatharth NY, Ram US) | 2 rows | None |
| 6 | Update LLM enrichment prompt (2a + 2b + 2c) | Prompt text | Low |
| 7 | Add new pools to `taxonomy.py` (LIFE_SCIENTIST_*) | Constants | None |
| 8 | Run targeted re-enrichment for 2a (~400 jobs) | Enrichment queue | Low |
| 9 | Run targeted re-enrichment for 2b (~120 jobs) | Enrichment queue | Low |
| 10 | Run targeted re-enrichment for 2c (~136 jobs) | Enrichment queue | Low |
| 11 | Run recommendation loop, validate email top-4 | Validation | — |

Steps 1-5 are independent of the LLM prompt changes and can be done first. Steps 6-10
can be batched together since they all touch the enrichment prompt. Step 11 validates
everything.

---

## Validation Checklist

After all steps are complete, run `scripts/run_user_recommendations.py` and confirm:

**Location:**
- [ ] Ram's top-4 email contains no India or LatAm jobs
- [ ] Yatharth's top-4 email surface NYC / remote-US jobs in top slots
- [ ] A job in Germany scores 0.15× on location component for both users (check logs)

**Domain errors (2a):**
- [ ] No `HARDWARE_ENGINEER` role jobs remain tagged `Business` domain
- [ ] No `OPERATIONS` role jobs remain tagged `Software` domain

**Missing pools (2b):**
- [ ] Research_Science domain no-pool% drops from ~80% to <20%
- [ ] `RESEARCH_SCIENTIST_FULLTIME` appears in pool table with non-zero count

**Aerospace disambiguation (2c):**
- [ ] Some previously no-pool Boeing/RTX SWE jobs now have `SWE_FULLTIME` pool
- [ ] Boeing avionics / mission systems jobs retain `Aerospace_Defense` domain (not flipped)
- [ ] Taxonomy health dashboard shows Aerospace_Defense no-pool% decreased
