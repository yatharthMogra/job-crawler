# Domain Taxonomy — Implementation Spec

## 1. What This Builds

A two-level hierarchy above the current flat pool structure. Every job and every candidate gets a
domain classification. The recommendation engine filters by domain first, then by pool
subscriptions within that domain. A candidate in the Software domain never sees Mechanical,
Hardware, or Aerospace jobs regardless of pool overlap.

```
Domain (top level — hard filter)
  └── Pool (second level — subscription-based filter)
        └── Job scoring (personal score)
```

---

## 2. Domain Taxonomy

Ten domains. Chosen to be mutually exclusive in the common case, with a small set of valid
cross-domain combinations for genuinely dual-discipline roles.

| Domain | What it covers |
|---|---|
| `Software` | All software engineering: backend, frontend, mobile, DevOps, ML engineering, data engineering, cloud, security, solutions engineering, TPM |
| `Data_Analytics` | Business-facing data: data science (statistical/analytical), BI, analytics engineering, data analysis. NOT ML engineering — that belongs to Software |
| `Management` | People and product leadership: product management, program management, supply chain management, operations leadership, project management |
| `Business` | Non-technical business: sales, marketing, finance, HR, customer success, legal, partnerships, recruiting, business operations |
| `Hardware_Electrical` | Electrical engineering, circuit design, FPGA, power systems, RF engineering, embedded hardware design |
| `Mechanical` | Mechanical engineering, structural analysis, CAD, materials, manufacturing design, wire/cable design |
| `Aerospace_Defense` | Avionics, satellite systems, missile systems, radar, defense systems, space systems. Assign this even when the role involves software if the context is aerospace or defense systems |
| `Industrial_Automation` | PLC programming, SCADA, manufacturing automation, process control, controls engineering |
| `Design` | UX design, product design, visual design, user research |
| `Research_Science` | Scientific research, laboratory work, academic research, computational science |

**Rule for ambiguous jobs:** When a job could plausibly belong to two domains, assign the domain
of the *output* of the work, not the tools used. A manufacturing controls engineer who writes
Python scripts → `Industrial_Automation` (the output is automated manufacturing, not software).
An ML engineer who builds production models → `Software` (the output is deployed software
systems). A Boeing software engineer building avionics software → `Aerospace_Defense` (the
context and output domain is aerospace even though the work is coding).

---

## 3. Multi-Domain Rules

Multiple domains are allowed but must be treated as the exception. The default is one domain.

### 3.1 Strictness threshold

**For jobs:** Assign a secondary domain only when the job description devotes substantial content
to two domains and explicitly requires non-trivial expertise in both. If in doubt, assign only
the primary domain.

Passing criteria for a secondary domain on a job:
- The secondary domain's work is explicitly described as a core responsibility (not a passing
  mention of tools)
- A candidate with zero background in the secondary domain would be materially disadvantaged

Failing criteria (do NOT assign secondary domain):
- The job mentions Python → this alone does not make it `Software` secondary
- The job is at a tech company but is a non-software role
- The secondary domain is the company's industry, not the role's work
- The employer is Boeing/RTX/Lockheed but the role is general enterprise software
- The role would be `Aerospace_Defense` if aerospace knowledge is required — assign that as
  **primary only**, not as secondary to `Software`

**For candidates:** Assign a secondary domain only when the candidate has demonstrated
professional-level work in both domains, evidenced by capabilities in each. The threshold:

```python
# Count capabilities per domain
# Primary domain: >= 3 capabilities
# Secondary domain: >= 3 capabilities (not 1-2 — that's just familiarity)
# If secondary has < 3 capabilities, assign primary only
```

### 3.2 Valid secondary domain combinations

Only these pairs are permitted. Any other combination is invalid and should be rejected in the
enrichment validation step.

```python
VALID_SECONDARY_PAIRS: set[frozenset] = {
    frozenset({"Software", "Data_Analytics"}),       # ML Engineer, Data Engineer building pipelines
    frozenset({"Software", "Management"}),            # Eng Manager who codes, Senior TPM
    frozenset({"Data_Analytics", "Research_Science"}),# Research Data Scientist, computational researcher
    frozenset({"Data_Analytics", "Management"}),      # Head of Data, Analytics Manager
    frozenset({"Hardware_Electrical", "Mechanical"}), # Mechatronics, electromechanical
    frozenset({"Hardware_Electrical", "Aerospace_Defense"}), # Defense electronics
    frozenset({"Mechanical", "Aerospace_Defense"}),   # Aerospace mechanical systems
    frozenset({"Industrial_Automation", "Hardware_Electrical"}), # Industrial electronics
    frozenset({"Management", "Business"}),            # GTM PM, business-facing program manager
    frozenset({"Design", "Software"}),                # Design engineer, design technologist
}
```

Any domain pair not in this set is invalid. If the LLM assigns an invalid secondary domain,
strip it and keep only primary.

### 3.4 Software vs Aerospace_Defense (binary — no dual-domain)

`Software` and `Aerospace_Defense` are **mutually exclusive**. There is no valid
`Software + Aerospace_Defense` secondary pair. Use this decision tree:

```
If the job requires domain-specific aerospace or defense knowledge to perform
(avionics standards, DO-178C, flight software safety, missile/radar/space systems,
classified systems context) →
    Aerospace_Defense primary, no secondary domain — regardless of tools used.

If the job is at an aerospace company but requires no aerospace expertise
(general backend, data engineering, enterprise software, internal tools) →
    Software primary, no secondary domain.
```

- Company industry alone does not make a role `Aerospace_Defense`.
- Never assign both `Software` and `Aerospace_Defense` on the same job.
- Residual case (general `Software` @ Boeing that still needs clearance) is handled by the
  candidate's `exclude_security_clearance` constraint — not by dual-domain tagging.

### 3.5 Domain hard filter logic

```python
def domains_match(job_domains: list[str], user_domains: list[str]) -> bool:
    """Returns True if job and user share at least one domain."""
    return bool(set(job_domains) & set(user_domains))
```

Jobs that share zero domains with the user are excluded before scoring. No exceptions.

---

## 4. Pool Taxonomy Update

### 4.1 `app/ingestion/taxonomy.py` (new file)

```python
from typing import Literal

DomainName = Literal[
    "Software",
    "Data_Analytics",
    "Management",
    "Business",
    "Hardware_Electrical",
    "Mechanical",
    "Aerospace_Defense",
    "Industrial_Automation",
    "Design",
    "Research_Science",
    "Other",
]

# Maps every pool to its domain.
# A job can only hold pools whose domain matches job.job_domain.
# Pool assignments that violate this mapping are stripped during enrichment write-back.
POOL_DOMAIN_MAP: dict[str, DomainName] = {

    # ── Software ──────────────────────────────────────────────────────────────
    "SWE_FULLTIME":                         "Software",
    "SWE_INTERNSHIP":                       "Software",
    "SWE_NEW_GRAD":                         "Software",
    "BACKEND_ENGINEER_FULLTIME":            "Software",
    "BACKEND_ENGINEER_INTERNSHIP":          "Software",
    "BACKEND_ENGINEER_NEW_GRAD":            "Software",
    "FRONTEND_ENGINEER_FULLTIME":           "Software",
    "FRONTEND_ENGINEER_INTERNSHIP":         "Software",
    "FRONTEND_ENGINEER_NEW_GRAD":           "Software",
    "FULLSTACK_ENGINEER_FULLTIME":          "Software",
    "FULLSTACK_ENGINEER_INTERNSHIP":        "Software",
    "MOBILE_ENGINEER_FULLTIME":             "Software",
    "MOBILE_ENGINEER_INTERNSHIP":           "Software",
    "DEVOPS_ENGINEER_FULLTIME":             "Software",
    "DEVOPS_ENGINEER_INTERNSHIP":           "Software",
    "ML_ENGINEER_FULLTIME":                 "Software",
    "ML_ENGINEER_INTERNSHIP":               "Software",
    "ML_ENGINEER_NEW_GRAD":                 "Software",
    "DATA_ENGINEER_FULLTIME":               "Software",
    "DATA_ENGINEER_INTERNSHIP":             "Software",
    "SECURITY_ENGINEER_FULLTIME":           "Software",
    "SOLUTIONS_ENGINEER_FULLTIME":          "Software",
    "SOLUTIONS_ENGINEER_INTERNSHIP":        "Software",
    "SUPPORT_ENGINEER_FULLTIME":            "Software",
    "TECHNICAL_PROGRAM_MANAGER_FULLTIME":   "Software",
    "TECHNICAL_PROGRAM_MANAGER_INTERNSHIP": "Software",

    # ── Data_Analytics ────────────────────────────────────────────────────────
    "DATA_SCIENTIST_FULLTIME":              "Data_Analytics",
    "DATA_SCIENTIST_INTERNSHIP":            "Data_Analytics",
    "DATA_SCIENTIST_NEW_GRAD":              "Data_Analytics",
    "DATA_ANALYST_FULLTIME":                "Data_Analytics",
    "DATA_ANALYST_INTERNSHIP":              "Data_Analytics",
    "DATA_ANALYST_NEW_GRAD":                "Data_Analytics",

    # ── Management ────────────────────────────────────────────────────────────
    "PRODUCT_MANAGER_FULLTIME":             "Management",
    "PRODUCT_MANAGER_INTERNSHIP":           "Management",

    # ── Business ──────────────────────────────────────────────────────────────
    "SALES_FULLTIME":                       "Business",
    "SALES_INTERNSHIP":                     "Business",
    "SALES_NEW_GRAD":                       "Business",
    "MARKETING_FULLTIME":                   "Business",
    "MARKETING_INTERNSHIP":                 "Business",
    "FINANCE_FULLTIME":                     "Business",
    "FINANCE_INTERNSHIP":                   "Business",
    "CUSTOMER_SUCCESS_FULLTIME":            "Business",
    "RECRUITING_FULLTIME":                  "Business",
    "PARTNERSHIPS_FULLTIME":                "Business",
    "LEGAL_FULLTIME":                       "Business",
    "OPERATIONS_FULLTIME":                  "Business",
    "OPERATIONS_NEW_GRAD":                  "Business",
    "SOLUTIONS_CONSULTANT_FULLTIME":        "Business",
    "SOLUTIONS_CONSULTANT_INTERNSHIP":      "Business",

    # ── Design ────────────────────────────────────────────────────────────────
    "PRODUCT_DESIGNER_FULLTIME":            "Design",
    "UX_RESEARCHER_FULLTIME":               "Design",       # new pool

    # ── Hardware_Electrical ───────────────────────────────────────────────────
    "ELECTRICAL_ENGINEER_FULLTIME":         "Hardware_Electrical",  # new pool
    "ELECTRICAL_ENGINEER_INTERNSHIP":       "Hardware_Electrical",  # new pool
    "HARDWARE_ENGINEER_FULLTIME":           "Hardware_Electrical",  # new pool

    # ── Mechanical ────────────────────────────────────────────────────────────
    "MECHANICAL_ENGINEER_FULLTIME":         "Mechanical",   # new pool
    "STRUCTURAL_ENGINEER_FULLTIME":         "Mechanical",   # new pool

    # ── Aerospace_Defense ─────────────────────────────────────────────────────
    "AEROSPACE_ENGINEER_FULLTIME":          "Aerospace_Defense",  # new pool
    "SYSTEMS_ENGINEER_FULLTIME":            "Aerospace_Defense",  # new pool (defense-context only)

    # ── Industrial_Automation ─────────────────────────────────────────────────
    "CONTROLS_ENGINEER_FULLTIME":           "Industrial_Automation",  # new pool
    "MANUFACTURING_ENGINEER_FULLTIME":      "Industrial_Automation",  # new pool

    # ── Research_Science ──────────────────────────────────────────────────────
    "RESEARCH_SCIENTIST_FULLTIME":          "Research_Science",  # new pool
    "RESEARCH_SCIENTIST_INTERNSHIP":        "Research_Science",  # new pool

    # ── Fallback ──────────────────────────────────────────────────────────────
    "OTHER_FULLTIME":                       "Other",
    "OTHER_INTERNSHIP":                     "Other",
}

# Reverse map: domain → pools in that domain
DOMAIN_POOLS: dict[str, list[str]] = {}
for pool, domain in POOL_DOMAIN_MAP.items():
    DOMAIN_POOLS.setdefault(domain, []).append(pool)

# Valid secondary domain pairings (bidirectional)
VALID_SECONDARY_PAIRS: set[frozenset] = {
    frozenset({"Software", "Data_Analytics"}),
    frozenset({"Software", "Management"}),
    frozenset({"Data_Analytics", "Research_Science"}),
    frozenset({"Data_Analytics", "Management"}),
    frozenset({"Hardware_Electrical", "Mechanical"}),
    frozenset({"Hardware_Electrical", "Aerospace_Defense"}),
    frozenset({"Mechanical", "Aerospace_Defense"}),
    frozenset({"Industrial_Automation", "Hardware_Electrical"}),
    frozenset({"Management", "Business"}),
    frozenset({"Design", "Software"}),
}

def is_valid_domain_pair(primary: str, secondary: str) -> bool:
    return frozenset({primary, secondary}) in VALID_SECONDARY_PAIRS
```

### 4.2 Pool validation in enrichment write-back

After the LLM assigns pools, strip any pool whose domain does not match the job's domain:

```python
from app.ingestion.taxonomy import POOL_DOMAIN_MAP

def validate_pools_against_domain(
    job_domain: str,
    assigned_pools: list[str],
    job_secondary_domain: str | None = None,
) -> list[str]:
    """
    Remove pools that don't belong to the job's domain(s).
    A pool is valid if its domain matches job_domain OR job_secondary_domain.
    """
    valid_domains = {job_domain}
    if job_secondary_domain:
        valid_domains.add(job_secondary_domain)

    return [
        pool for pool in assigned_pools
        if POOL_DOMAIN_MAP.get(pool) in valid_domains
    ]
```

---

## 5. Schema Additions

### 5.1 Migration

```sql
-- normalized_jobs
ALTER TABLE normalized_jobs
    ADD COLUMN job_domain        VARCHAR,
    ADD COLUMN job_secondary_domain VARCHAR;

CREATE INDEX idx_normalized_jobs_job_domain
    ON normalized_jobs(job_domain);

-- job_archive
ALTER TABLE job_archive
    ADD COLUMN job_domain        VARCHAR,
    ADD COLUMN job_secondary_domain VARCHAR;

-- candidate_profiles
ALTER TABLE candidate_profiles
    ADD COLUMN primary_domain   VARCHAR,
    ADD COLUMN secondary_domain VARCHAR;
```

All columns are nullable at migration time. New jobs get values from enrichment. Existing
normalized_jobs (7-day window, ~1,700 rows) get values from a lightweight reprocessing pass.

### 5.2 Migration file name

```
alembic/versions/YYYYMMDD_XXXX_domain_taxonomy.py
```

---

## 6. Enrichment Changes

### 6.1 Pydantic model additions (`app/ingestion/extractor/llm.py`)

```python
from app.ingestion.taxonomy import DomainName
from pydantic import BaseModel, field_validator
from typing import Optional

class JobEnrichmentOutput(BaseModel):
    # ... all existing fields unchanged ...

    # New fields
    job_domain: DomainName
    job_secondary_domain: Optional[DomainName] = None

    @field_validator("job_secondary_domain")
    @classmethod
    def validate_secondary_domain(cls, secondary, info):
        if secondary is None:
            return None
        primary = info.data.get("job_domain")
        if primary is None:
            return None
        if secondary == primary:
            return None  # same domain — just use primary
        from app.ingestion.taxonomy import is_valid_domain_pair
        if not is_valid_domain_pair(primary, secondary):
            # Invalid pair — strip secondary, keep only primary
            return None
        return secondary
```

### 6.2 Enrichment write-back update (`app/ingestion/enrichment_worker.py`)

After enrichment output is validated, apply pool validation before writing:

```python
from app.ingestion.taxonomy import validate_pools_against_domain

# After LLM output is parsed:
validated_pools = validate_pools_against_domain(
    job_domain=output.job_domain,
    assigned_pools=output.retrieval_pools,
    job_secondary_domain=output.job_secondary_domain,
)

# Write to normalized_jobs:
await db.execute(
    update(NormalizedJob)
    .where(NormalizedJob.id == normalized_job_id)
    .values(
        # ... existing enrichment fields ...
        job_domain=output.job_domain,
        job_secondary_domain=output.job_secondary_domain,
        retrieval_pools=validated_pools,    # overwrite with validated version
    )
)

# Write domain to job_archive too:
await db.execute(
    update(JobArchive)
    .where(JobArchive.id == job_archive_id)
    .values(
        job_domain=output.job_domain,
        job_secondary_domain=output.job_secondary_domain,
    )
)
```

### 6.3 LLM prompt addition

Add this block to the enrichment prompt, immediately before the output schema definition:

```
job_domain: The professional discipline this role belongs to. Choose exactly one value
from the list below. Assign based on what the role's PRIMARY OUTPUT is, not the tools
used or the company's industry.

- Software: Primary output is running software code, software systems, APIs, platforms.
  Includes: backend, frontend, mobile, DevOps, ML engineering, data engineering,
  cloud engineering, security engineering, solutions engineering, TPM roles.
  Key test: does the person spend most of their time writing and shipping code/systems?

- Data_Analytics: Business-facing data work. Primary output is insights, reports, models
  for business decisions. Includes: data science (statistical/analytical focus),
  BI development, analytics engineering, data analysis.
  NOT ML engineering — if the person is building production ML systems, use Software.

- Management: Primary output is decisions and coordination. Includes: product management,
  program management, project management, supply chain management, operations leadership.

- Business: Non-technical business roles. Includes: sales, marketing, finance, HR,
  customer success, legal, partnerships, recruiting, business operations.

- Hardware_Electrical: Primary output is hardware or electrical systems. Includes:
  electrical engineering, circuit design, PCB design, FPGA design, power systems,
  RF engineering, embedded hardware (not firmware — firmware is Software).

- Mechanical: Primary output is mechanical systems. Includes: mechanical engineering,
  structural analysis, CAD/design, materials engineering, manufacturing design,
  wire harness design, payload design.

- Aerospace_Defense: Primary output serves aerospace or defense systems. Assign this
  even if the role involves software (e.g., avionics software, mission systems software)
  if the context is aerospace or defense. Includes: avionics, satellite systems,
  missile/weapon systems, radar, space systems, defense software, flight simulation.

Software vs Aerospace_Defense (mutually exclusive — never assign both):
- If the job requires aerospace/defense domain knowledge (DO-178C, flight software safety,
  avionics, missile/radar/space systems, classified context) → Aerospace_Defense primary,
  no secondary — regardless of tools used.
- If the job is at an aerospace company but requires no aerospace expertise (internal HR
  systems, enterprise data pipelines, general backend) → Software primary, no secondary.
- Software + Aerospace_Defense is not a valid pair — never assign both.

- Industrial_Automation: Primary output is automated manufacturing or industrial
  control systems. Includes: PLC programming, SCADA, DCS, manufacturing automation,
  process control, controls engineering.

- Design: Primary output is user experience or visual design. Includes: UX design,
  product design, interaction design, visual design, user research.

- Research_Science: Primary output is scientific knowledge. Includes: scientific research,
  laboratory work, computational science, academic research.

- Other: Does not fit any category above.

job_secondary_domain: A second domain ONLY if the role genuinely requires substantial
expertise in two disciplines and both are explicitly described as core responsibilities.
If in doubt, leave null. Do not assign just because tools from another domain are mentioned.
Must be a different value from job_domain. Only valid pairs are accepted — all others
are stripped automatically.
```

---

## 7. User Domain Derivation

### 7.1 Capability-to-domain mapping (`app/ingestion/taxonomy.py` addition)

```python
# Maps each capability name to its domain(s).
# A capability can map to at most 2 domains (primary, optional secondary).
CAPABILITY_DOMAIN_MAP: dict[str, list[DomainName]] = {
    # Software capabilities
    "Backend Engineering":          ["Software"],
    "Frontend Engineering":         ["Software"],
    "Full Stack Development":       ["Software"],
    "Cloud Infrastructure":         ["Software"],
    "DevOps":                       ["Software"],
    "AI Systems":                   ["Software"],
    "Machine Learning Research":    ["Software", "Data_Analytics"],
    "Distributed Systems":          ["Software"],
    "Data Engineering":             ["Software", "Data_Analytics"],
    "Security Engineering":         ["Software"],
    "Research":                     ["Software", "Research_Science"],

    # Data_Analytics capabilities
    "Machine Learning":             ["Data_Analytics", "Software"],
    "Analytics Engineering":        ["Data_Analytics"],
    "Statistical Analysis":         ["Data_Analytics"],
    "Business Intelligence":        ["Data_Analytics"],

    # Management capabilities
    "Product Management":           ["Management"],
    "Program Management":           ["Management"],
    "Technical Leadership":         ["Management", "Software"],

    # Business capabilities
    "Sales":                        ["Business"],
    "Marketing":                    ["Business"],
    "Finance":                      ["Business"],
    "Customer Success":             ["Business"],
    "Business Development":         ["Business"],

    # Design capabilities
    "UX Design":                    ["Design"],
    "Product Design":               ["Design"],

    # Hardware/Mechanical capabilities
    "Electrical Engineering":       ["Hardware_Electrical"],
    "Hardware Design":              ["Hardware_Electrical"],
    "Mechanical Engineering":       ["Mechanical"],
    "Structural Analysis":          ["Mechanical"],

    # Aerospace capabilities
    "Avionics":                     ["Aerospace_Defense"],
    "Systems Engineering":          ["Aerospace_Defense"],

    # Research capabilities
    "Scientific Research":          ["Research_Science"],
    "Computational Science":        ["Research_Science", "Software"],
}
```

### 7.2 User domain derivation function

```python
from collections import Counter
from app.ingestion.taxonomy import (
    CAPABILITY_DOMAIN_MAP, VALID_SECONDARY_PAIRS, DomainName
)

MIN_CAPABILITIES_FOR_DOMAIN = 3  # must have at least 3 capabilities mapping to a domain

def derive_user_domains(capabilities: list[str]) -> tuple[str, str | None]:
    """
    Returns (primary_domain, secondary_domain | None) for a candidate.

    Rules:
    - Count how many capabilities map to each domain.
    - Primary = domain with highest count (must be >= 3 capabilities).
    - Secondary = domain with second-highest count (must be >= 3 capabilities AND
      form a valid pair with primary).
    - If no domain reaches the threshold, return ("Other", None).
    """
    domain_counts: Counter = Counter()

    for cap in capabilities:
        mapped_domains = CAPABILITY_DOMAIN_MAP.get(cap, [])
        for domain in mapped_domains:
            domain_counts[domain] += 1

    if not domain_counts:
        return ("Other", None)

    # Sort by count descending
    ranked = domain_counts.most_common()

    primary_domain, primary_count = ranked[0]
    if primary_count < MIN_CAPABILITIES_FOR_DOMAIN:
        return ("Other", None)

    secondary_domain = None
    if len(ranked) >= 2:
        candidate_secondary, secondary_count = ranked[1]
        if (
            secondary_count >= MIN_CAPABILITIES_FOR_DOMAIN
            and frozenset({primary_domain, candidate_secondary}) in VALID_SECONDARY_PAIRS
        ):
            secondary_domain = candidate_secondary

    return (primary_domain, secondary_domain)
```

**Current users derived:**

Yatharth capabilities: Backend Engineering, Full Stack Development, AI Systems,
Machine Learning Research, Data Engineering, Distributed Systems, Cloud Infrastructure,
DevOps, Research

Domain counts:
- Software: Backend(1) + FullStack(1) + AISystems(1) + MLResearch(1) + DataEng(1)
            + DistSys(1) + Cloud(1) + DevOps(1) + Research(1) = 9
- Data_Analytics: MLResearch(1) + DataEng(1) = 2
- Research_Science: Research(1) = 1

Result: `primary_domain: "Software"`, `secondary_domain: None`
(Data_Analytics only reaches 2, below threshold of 3)

Ram capabilities: Data Engineering, Analytics Engineering, Machine Learning,
Cloud Infrastructure

Domain counts:
- Software: DataEng(1) + Cloud(1) = 2
- Data_Analytics: DataEng(1) + Analytics(1) + ML(1) = 3
- Software (from ML secondary): ML(1) → adds 1 more to Software = 3 total

Actually: DataEng maps to [Software, Data_Analytics], so:
- Software: DataEng(1) + Cloud(1) + ML-secondary(1) = 3
- Data_Analytics: DataEng(1) + Analytics(1) + ML(1) = 3

Both reach threshold, pair (Software, Data_Analytics) is valid.

Result: `primary_domain: "Data_Analytics"` (highest or equal — Data_Analytics is primary
if user is primarily a data person), `secondary_domain: "Software"`

Note: When counts are equal, use the domain that aligns with the user's self-identified
primary role. Ram's subscribed pools are DATA_SCIENTIST, DATA_ENGINEER, ML_ENGINEER —
Data_Analytics is the right primary.

### 7.3 Trigger: when to derive

Run domain derivation:
1. At profile creation (after capabilities are extracted from resume)
2. After any capability update (patch applied to candidate profile)
3. Available as a manual recalculation endpoint: `POST /candidates/{id}/recalculate-domains`

Store in `candidate_profiles.primary_domain` and `candidate_profiles.secondary_domain`.
Display in the profile UI for user confirmation — domain is not immutable, user can override.

---

## 8. Recommendation Engine Changes

### 8.1 Domain filter in the recommendation query

Add to `app/recommendation/engine.py` (or wherever the pool subscription query lives):

```python
def get_candidate_domains(candidate: CandidateProfile) -> list[str]:
    """Returns all domains this candidate can see jobs in."""
    domains = [candidate.primary_domain]
    if candidate.secondary_domain:
        domains.append(candidate.secondary_domain)
    return [d for d in domains if d and d != "Other"]


async def get_eligible_jobs(
    candidate: CandidateProfile,
    db: AsyncSession,
) -> list[NormalizedJob]:
    candidate_domains = get_candidate_domains(candidate)
    subscribed_pools = await get_subscribed_pools(candidate.id, db)

    result = await db.execute(
        select(NormalizedJob)
        .where(
            # Gate 1: domain match (hard filter)
            or_(
                NormalizedJob.job_domain.in_(candidate_domains),
                NormalizedJob.job_secondary_domain.in_(candidate_domains),
            ),
            # Gate 2: pool subscription (existing filter)
            NormalizedJob.retrieval_pools.overlap(subscribed_pools),
            # Gate 3: active and fresh (existing filters)
            NormalizedJob.is_active == True,
            NormalizedJob.posted_at >= datetime.now(UTC) - timedelta(days=7),
        )
    )
    return result.scalars().all()
```

### 8.2 Scoring: no change needed for domain

Domain match is enforced as a hard filter in the query — no domain multiplier is needed in
scoring because mismatched domains never reach the scoring step. This is cleaner than a
multiplier approach. Jobs that pass both domain and pool gates are scored normally using
the existing formula.

This means the existing scoring weights (capabilities 40%, skills 25%, location 20%,
comp 15%) remain unchanged. Domain is handled structurally, not numerically.

### 8.3 Requires-clearance filter (separate, still needed)

Domain filtering handles aerospace/defense contamination for most roles:
- "Senior Software Engineer, Mission Systems @ RTX" → `Aerospace_Defense` primary (filtered
  out for Software-domain candidates)
- "Software Engineer @ Boeing" building internal enterprise tools → `Software` primary
  (visible to Software candidates). Among those, some still require clearance.

Keep `requires_clearance: bool` as a separate enrichment field and hard filter:

```python
# In get_eligible_jobs, add Gate 4:
NormalizedJob.requires_clearance == False,  # or candidate.clearance_eligible == True
```

---

## 9. Migration Plan

### Step 1 — Constants file (no risk, no DB)
Create `app/ingestion/taxonomy.py` with `POOL_DOMAIN_MAP`, `VALID_SECONDARY_PAIRS`,
`CAPABILITY_DOMAIN_MAP`. Unit test the validation functions.

### Step 2 — Schema migration
Add `job_domain`, `job_secondary_domain` to `normalized_jobs` and `job_archive`.
Add `primary_domain`, `secondary_domain` to `candidate_profiles`.
All nullable — no backfill required at migration time.

### Step 3 — Enrichment prompt + schema
Add `job_domain` and `job_secondary_domain` to the Pydantic output model.
Add domain block to LLM prompt.
Add pool validation in write-back.
New jobs from this point get domain tags automatically.

### Step 4 — Backfill active jobs
The active window is ~1,700 normalized_jobs rows. Run a lightweight enrichment reprocessing
pass that only re-extracts `job_domain` (not the full enrichment) using the new prompt.
Target: populate all active jobs before enabling the domain filter.

```python
# Minimal reprocessing — domain extraction only
# Can be done as a one-off script, not through the full enrichment queue
```

### Step 5 — User domain derivation
Run `derive_user_domains` for all existing candidates. Two candidates currently — trivial.
Write results to `candidate_profiles`.

### Step 6 — Enable domain filter
Toggle the domain filter on in the recommendation query. Validate results.

### Step 7 — Backfill job_archive
The archive has ~6,968 rows. Run domain extraction in batches overnight. Not urgent — archive
is only used for applied history display, not for recommendation scoring.

---

## 10. Expected Impact on Current Recommendations

After implementing Steps 1–6, running the same recommendation loop against the current
active pool (1,218 jobs):

**Jobs that would be FILTERED OUT for Yatharth and Ram (both Software domain):**
- All Boeing Structural/Mechanical/Wire/Payload engineering jobs → `Mechanical`
- All Boeing/RTX Electrical/Power/RF/FPGA jobs → `Hardware_Electrical`
- All RTX Radar/Missile/Avionics/Signal Processing jobs → `Aerospace_Defense`
- All Boeing aerospace systems jobs → `Aerospace_Defense`
- All RTX Manufacturing Controls/PLC/SCADA jobs → `Industrial_Automation`
- Per Scholas Instructional Assistant → `Management` or `Other`

**Jobs that PASS the filter (Software domain):**
- Boeing Data Engineer → `Software` ✅
- Boeing Software Engineer (enterprise, internal tools) → `Software` ✅
- Salesforce Data Engineering MTS → `Software` ✅
- Torc Robotics Software/ML roles → `Software` ✅
- RTX genuine SWE roles (enterprise, internal) → `Software` ✅
- All previously-working tech company jobs → `Software` ✅

**Estimated pool size after filter:** ~300–400 jobs from the current 1,218 active, all
genuinely relevant to a software engineering candidate. Quality over quantity.
