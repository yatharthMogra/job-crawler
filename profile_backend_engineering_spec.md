# Candidate Profile Intelligence System — Backend + LLM Engineering Spec

---

## 1. What This Service Builds

A standalone FastAPI service responsible for:

- Ingesting candidate resume PDFs
- Extracting structured evidence via PyMuPDF + LLM
- Computing proposed profile patches
- Committing user-approved patches to a versioned canonical profile
- Deriving and storing capabilities from approved evidence

This service shares the same PostgreSQL instance as the job ingestion system but operates in its own table namespace.

---

## 2. Stack

| Concern | Choice |
|---|---|
| Framework | FastAPI (new service, separate process) |
| Language | Python 3.11+ |
| Database | PostgreSQL (shared instance, separate tables) |
| ORM | SQLAlchemy 2.x async + asyncpg |
| Migrations | Alembic |
| PDF text extraction | PyMuPDF (fitz) |
| Multimodal fallback | Claude API (direct PDF bytes) |
| LLM extraction | Claude API + Instructor |
| Structured output | Pydantic models |
| Logging | structlog |
| Config | pydantic-settings |

---

## 3. Core Design Rules

- **LLMs extract. Backend decides. Users approve.**
- **PyMuPDF runs first, always.** Claude multimodal is fallback only when text extraction fails or produces garbage (< 100 chars extracted, encoding errors).
- **No canonical profile mutation without an approved patch.** The backend never writes to the canonical profile layer directly from LLM output.
- **Evidence objects carry provenance.** Every evidence item references its source resume.
- **Capabilities are always recomputed.** Never manually written to the capabilities table.
- **Profile versions are immutable snapshots.** Every approved patch increments the version and writes a new snapshot.

---

## 4. Database Schema

### 4.1 `candidates`

Core identity record. System-controlled. Never touched by LLM.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| email | VARCHAR UNIQUE | Login identifier |
| name | VARCHAR | |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

### 4.2 `candidate_resumes`

Immutable. One row per uploaded resume. Never updated.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| file_path | VARCHAR | Local path or future S3 key |
| original_filename | VARCHAR | |
| file_size_bytes | INTEGER | |
| extraction_method | VARCHAR | "pymupdf" or "multimodal" |
| raw_text | TEXT | Extracted plain text — stored permanently |
| raw_text_char_count | INTEGER | Used to detect extraction failure |
| extraction_status | VARCHAR | "success" / "failed" / "fallback_used" |
| uploaded_at | TIMESTAMP | |
| parsed_at | TIMESTAMP | |

---

### 4.3 `candidate_evidence`

Append-heavy. One row per evidence item (experience, project, certification). Never silently deleted.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| source_resume_id | UUID FK → candidate_resumes | Provenance |
| evidence_type | VARCHAR | "experience" / "project" / "certification" |
| is_approved | BOOLEAN | False until user approves |
| is_active | BOOLEAN | Soft delete — rejected items marked inactive |
| raw_source_text | TEXT | The original text chunk this was extracted from |
| normalized_data | JSONB | Typed evidence payload (see below) |
| created_at | TIMESTAMP | |
| approved_at | TIMESTAMP | nullable |

**`normalized_data` structure by type:**

Experience:
```json
{
  "title": "Software Developer 2",
  "company": "Walmart",
  "duration_months": 24,
  "domains": ["Retail Tech"],
  "evidence_keywords": ["Backend APIs", "Distributed Systems", "Java", "Kafka"]
}
```

Project:
```json
{
  "name": "SpecterRossAI",
  "category": "AI Product",
  "domains": ["Legal Tech"],
  "evidence_keywords": ["Multi-Agent Systems", "RAG", "React", "Voice AI"]
}
```

Certification:
```json
{
  "name": "AWS Solutions Architect",
  "issuer": "AWS"
}
```

---

### 4.4 `candidate_profiles`

One row per profile version. Immutable snapshots. New row on every approved patch.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| version | INTEGER | Increments on every approved patch |
| is_current | BOOLEAN | Only one row per candidate is true |
| schema_version | VARCHAR | e.g. "v1" |
| constraints | JSONB | Full constraints snapshot |
| preferences | JSONB | Full preferences snapshot |
| skills | JSONB | Full skills snapshot |
| patch_id | UUID FK → candidate_patches | Patch that created this version |
| created_at | TIMESTAMP | |

**`constraints` JSONB structure:**
```json
{
  "sponsorship_required": true,
  "visa_type": "F1",
  "work_authorization": "CPT_OPT",
  "internship_only": false,
  "fulltime_only": false,
  "minimum_salary": null,
  "minimum_hourly_rate": 25
}
```

**`preferences` JSONB structure:**
```json
{
  "primary_roles": ["Software Engineer Intern", "AI Engineer Intern"],
  "secondary_roles": ["Data Scientist Intern"],
  "preferred_locations": ["NYC", "Remote"],
  "acceptable_locations": ["New Jersey"],
  "remote_preference": "Hybrid",
  "relocation_allowed": true,
  "preferred_company_stages": ["Startup", "Growth Stage"],
  "preferred_industries": ["AI", "FinTech"]
}
```

**`skills` JSONB structure:**
```json
{
  "languages": ["Python", "Java", "TypeScript"],
  "frameworks": ["React", "FastAPI"],
  "databases": ["PostgreSQL"],
  "cloud": ["AWS"],
  "ai_ml": ["RAG", "LLMs", "Multi-Agent Systems"],
  "infrastructure": ["Docker", "Kafka"],
  "product": ["Rapid Prototyping"]
}
```

---

### 4.5 `candidate_patches`

One row per proposed patch (approved or rejected). Full audit trail.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| source_resume_id | UUID FK → candidate_resumes | |
| profile_version_before | INTEGER | nullable on first profile creation |
| profile_version_after | INTEGER | nullable until committed |
| status | VARCHAR | "pending" / "committed" / "rejected" / "partial" |
| proposed_operations | JSONB | All operations proposed by backend |
| approved_operations | JSONB | Subset approved by user |
| rejected_operations | JSONB | Subset rejected by user |
| committed_at | TIMESTAMP | nullable |
| created_at | TIMESTAMP | |

**Operation structure inside JSONB arrays:**
```json
[
  {
    "op": "ADD_SKILL",
    "category": "languages",
    "value": "Python"
  },
  {
    "op": "ADD_EXPERIENCE",
    "evidence_id": "uuid"
  },
  {
    "op": "UPDATE_EXPERIENCE",
    "evidence_id": "uuid",
    "field": "duration_months",
    "from": 22,
    "to": 24
  },
  {
    "op": "ADD_CONSTRAINT_SUGGESTION",
    "field": "sponsorship_required",
    "suggested_value": true,
    "reason": "F1 visa indicators detected"
  }
]
```

---

### 4.6 `candidate_capabilities`

Derived. Fully replaced on every capability recomputation. One row per capability per candidate.

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| candidate_id | UUID FK → candidates | |
| profile_version | INTEGER | Version this was computed from |
| taxonomy_version | VARCHAR | e.g. "v1" |
| capability_name | VARCHAR | From frozen taxonomy |
| supporting_evidence | VARCHAR[] | References to evidence (company names, project names, keywords) |
| computed_at | TIMESTAMP | |

---

## 5. Project Structure

```
profile_service/
├── docker-compose.yml         # shared with job_ingestion or standalone
├── .env
├── .env.example
├── pyproject.toml
│
├── alembic/
│   └── versions/
│
└── app/
    ├── main.py                # FastAPI app, lifespan, router registration
    ├── config.py              # pydantic-settings
    ├── database.py            # async engine, session factory
    │
    ├── models/
    │   ├── candidate.py
    │   ├── resume.py
    │   ├── evidence.py
    │   ├── profile.py
    │   ├── patch.py
    │   └── capability.py
    │
    ├── schemas/               # Pydantic API schemas
    │   ├── candidate.py
    │   ├── resume.py
    │   ├── patch.py
    │   └── profile.py
    │
    ├── api/
    │   ├── candidates.py
    │   ├── resumes.py
    │   └── profiles.py
    │
    ├── pipeline/
    │   ├── extractor.py       # PyMuPDF + fallback orchestration
    │   ├── llm_parser.py      # LLM extraction call + Instructor
    │   ├── diff_engine.py     # proposed change computation
    │   ├── patch_engine.py    # patch commit + profile version write
    │   └── capability_engine.py  # capability recomputation
    │
    ├── llm/
    │   ├── base.py
    │   ├── claude.py
    │   └── factory.py
    │
    └── utils/
        ├── text_utils.py      # skill alias normalization, name normalization
        ├── logging.py
        └── seed.py            # hardcoded test profiles for V1 testing
```

---

## 6. Resume Parsing Pipeline

### Step 1: Upload

`POST /resumes/upload` — accepts multipart PDF upload.

- Store PDF to local filesystem under `data/resumes/{candidate_id}/{resume_id}.pdf`
- Create `candidate_resumes` row (status: pending)
- Return `resume_id`

---

### Step 2: Text Extraction

Called immediately after upload (synchronously in V1).

```python
# pipeline/extractor.py

import fitz  # PyMuPDF

def extract_text(pdf_path: str) -> tuple[str, str]:
    """
    Returns (extracted_text, method_used).
    method_used: "pymupdf" or "multimodal"
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # Fallback trigger conditions:
    # - Extracted text under 100 characters
    # - Text contains mostly encoding garbage
    if len(text.strip()) < 100:
        text = _multimodal_fallback(pdf_path)
        return text, "multimodal"

    return text.strip(), "pymupdf"
```

Text is stored permanently on the `candidate_resumes` row.

---

### Step 3: LLM Evidence Extraction

`pipeline/llm_parser.py`

The LLM receives the extracted plain text (never the PDF, never the canonical profile).

**Pydantic extraction schema (Instructor-enforced):**

```python
from typing import Literal
from pydantic import BaseModel

CapabilityName = Literal[
    "Backend Engineering", "Frontend Engineering", "Full Stack Development",
    "AI Systems", "Machine Learning", "Machine Learning Research",
    "Data Engineering", "Distributed Systems", "Cloud Infrastructure",
    "Platform Engineering", "DevOps", "Product Engineering",
    "Mobile Development", "Security Engineering", "Analytics Engineering",
    "Research",
]

class ExtractedExperience(BaseModel):
    title: str
    company: str
    duration_months: int
    domains: list[str]
    evidence_keywords: list[str]

class ExtractedProject(BaseModel):
    name: str
    category: str
    domains: list[str]
    evidence_keywords: list[str]

class ExtractedCertification(BaseModel):
    name: str
    issuer: str

class ExtractedSkills(BaseModel):
    languages: list[str]
    frameworks: list[str]
    databases: list[str]
    cloud: list[str]
    ai_ml: list[str]
    infrastructure: list[str]
    product: list[str]

class ConstraintSuggestions(BaseModel):
    sponsorship_required: bool | None
    visa_type: str | None
    work_authorization: str | None
    internship_only: bool | None
    fulltime_only: bool | None

class PreferenceSuggestions(BaseModel):
    primary_roles: list[str]
    secondary_roles: list[str]
    preferred_locations: list[str]
    remote_preference: str | None
    preferred_industries: list[str]

class LLMExtractionOutput(BaseModel):
    experiences: list[ExtractedExperience]
    projects: list[ExtractedProject]
    certifications: list[ExtractedCertification]
    skills: ExtractedSkills
    constraint_suggestions: ConstraintSuggestions
    preference_suggestions: PreferenceSuggestions
```

**System prompt (condensed):**

```
You are a precise resume parser. Extract structured professional information 
from the resume text provided.

Rules:
- Extract ONLY information explicitly present in the resume text.
- Do not infer, embellish, or hallucinate details.
- Normalize skill aliases: "js" → "JavaScript", "postgres" → "PostgreSQL".
- evidence_keywords must be normalized technical/architectural signals, 
  not raw bullet text.
- For constraint and preference suggestions: only suggest when there are 
  clear signals. Leave null if uncertain.
- duration_months: compute from date ranges if present. If only year given, 
  estimate conservatively.

Return a single JSON object matching the provided schema exactly.
```

**Two-step LLM flow:**

Step A — Extract evidence, skills, suggestions (above).
Step B — Capability inference (separate call after Step A):

```python
class InferredCapability(BaseModel):
    name: CapabilityName
    supporting_evidence: list[str]

class CapabilityInferenceOutput(BaseModel):
    capabilities: list[InferredCapability]
```

Step B system prompt:
```
Given the following extracted evidence and skills from a candidate's resume,
assign capabilities from the provided taxonomy only.

Rules:
- Only assign a capability if there is direct evidence supporting it.
- supporting_evidence must reference specific companies, project names, 
  or concrete technical signals from the evidence.
- Do not assign capabilities not present in the taxonomy.
- Do not invent new capability names.

Taxonomy (choose only from this list):
[Backend Engineering, Frontend Engineering, Full Stack Development, ...]
```

---

### Step 4: Proposed Change Computation

`pipeline/diff_engine.py`

The backend (not the LLM) computes what changes to propose.

**Input:** LLM extraction output + current canonical profile state

**Output:** List of typed operation objects

```python
def compute_proposed_operations(
    extracted: LLMExtractionOutput,
    current_profile: CandidateProfile | None,
    current_evidence: list[CandidateEvidence],
) -> list[dict]:
    operations = []

    # --- Skills diff ---
    for category, new_skills in extracted.skills:
        existing_skills = current_profile.skills.get(category, [])
        for skill in new_skills:
            normalized = normalize_skill(skill)
            if normalized not in existing_skills:
                operations.append({
                    "op": "ADD_SKILL",
                    "category": category,
                    "value": normalized,
                })

    # --- Experience diff ---
    for exp in extracted.experiences:
        merge_candidate = find_experience_merge_candidate(exp, current_evidence)
        if merge_candidate is None:
            operations.append({"op": "ADD_EXPERIENCE", "data": exp.dict()})
        else:
            field_diffs = compute_experience_diff(exp, merge_candidate)
            for diff in field_diffs:
                operations.append({"op": "UPDATE_EXPERIENCE", **diff})

    # --- Projects diff ---
    # same pattern as experiences

    # --- Constraint suggestions ---
    for field, suggested_value in extracted.constraint_suggestions:
        if suggested_value is not None:
            operations.append({
                "op": "ADD_CONSTRAINT_SUGGESTION",
                "field": field,
                "suggested_value": suggested_value,
            })

    return operations
```

---

### Merge Heuristics

```python
# utils/text_utils.py

def find_experience_merge_candidate(
    extracted_exp: ExtractedExperience,
    existing_evidence: list[CandidateEvidence],
) -> CandidateEvidence | None:
    """
    Merge if:
    - Normalized company name matches
    - Title similarity is high (fuzzy match > 0.8)
    Returns None if no strong merge candidate found.
    """

def normalize_skill(skill: str) -> str:
    """
    Normalize common aliases.
    js → JavaScript
    postgres / postgresql → PostgreSQL
    ts → TypeScript
    node / nodejs → Node.js
    etc.
    """
    ALIAS_MAP = {
        "js": "JavaScript",
        "ts": "TypeScript",
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "nodejs": "Node.js",
        "node": "Node.js",
        "mongo": "MongoDB",
        "k8s": "Kubernetes",
        "gcp": "Google Cloud",
    }
    return ALIAS_MAP.get(skill.lower().strip(), skill)
```

---

### Step 5: Patch Creation and User Review

After diff computation:

1. Store proposed operations in `candidate_patches` (status: pending)
2. Store proposed evidence objects in `candidate_evidence` (is_approved: false)
3. Return the proposed patch to the frontend for user review

`GET /profiles/{candidate_id}/pending-patch` — returns the pending patch in a frontend-friendly format (semantic diff, not raw operations).

---

### Step 6: Patch Commit

`POST /profiles/{candidate_id}/patches/{patch_id}/commit`

Request body: list of approved operation IDs.

**Backend commit flow:**

```python
async def commit_patch(patch_id, approved_op_ids, db):
    patch = await get_patch(patch_id, db)

    approved_ops = [op for op in patch.proposed_operations
                    if op["id"] in approved_op_ids]
    rejected_ops = [op for op in patch.proposed_operations
                    if op["id"] not in approved_op_ids]

    # Apply approved operations
    new_skills = apply_skill_ops(approved_ops, current_skills)
    new_constraints = apply_constraint_ops(approved_ops, current_constraints)
    new_preferences = apply_preference_ops(approved_ops, current_preferences)

    # Approve evidence items
    for op in approved_ops:
        if op["op"] in ("ADD_EXPERIENCE", "ADD_PROJECT", "ADD_CERTIFICATION"):
            await approve_evidence(op["evidence_id"], db)

    # Mark previous profile version as not current
    await mark_profile_not_current(candidate_id, db)

    # Write new profile version
    new_version = current_version + 1
    await write_profile_version(
        candidate_id=candidate_id,
        version=new_version,
        constraints=new_constraints,
        preferences=new_preferences,
        skills=new_skills,
        patch_id=patch_id,
        db=db,
    )

    # Update patch record
    await finalize_patch(patch_id, approved_ops, rejected_ops, new_version, db)

    # Trigger capability recomputation
    await recompute_capabilities(candidate_id, new_version, db)
```

---

### Step 7: Capability Recomputation

`pipeline/capability_engine.py`

Called automatically after every successful patch commit.

```python
async def recompute_capabilities(candidate_id, profile_version, db):
    # Load all approved evidence for candidate
    evidence = await get_approved_evidence(candidate_id, db)
    current_profile = await get_current_profile(candidate_id, db)

    # Build context for LLM
    evidence_summary = build_evidence_summary(evidence, current_profile.skills)

    # LLM inference (Step B from above)
    result = await llm_client.infer_capabilities(evidence_summary)

    # Delete current capabilities for this candidate
    await delete_capabilities(candidate_id, db)

    # Write new capabilities
    for cap in result.capabilities:
        await write_capability(
            candidate_id=candidate_id,
            profile_version=profile_version,
            capability_name=cap.name,
            supporting_evidence=cap.supporting_evidence,
            taxonomy_version="v1",
            db=db,
        )
```

---

## 7. API Endpoints

### Candidates
```
POST   /candidates                          # Create candidate (minimal identity)
GET    /candidates/{id}                     # Get candidate identity
```

### Resumes
```
POST   /candidates/{id}/resumes/upload      # Upload PDF, trigger parse pipeline
GET    /candidates/{id}/resumes             # List uploaded resumes
GET    /candidates/{id}/resumes/{resume_id} # Get resume metadata + extraction status
```

### Profile
```
GET    /candidates/{id}/profile             # Get current canonical profile
GET    /candidates/{id}/profile/versions    # List all profile versions
GET    /candidates/{id}/profile/versions/{v} # Get specific version snapshot
```

### Patches
```
GET    /candidates/{id}/patches/pending     # Get current pending patch (for review UI)
POST   /candidates/{id}/patches/{patch_id}/commit  # Commit with approved op IDs
DELETE /candidates/{id}/patches/{patch_id}  # Discard pending patch
```

### Capabilities
```
GET    /candidates/{id}/capabilities        # Get current capabilities with evidence
```

### Manual edits (direct profile mutation, no patch required)
```
PATCH  /candidates/{id}/profile/constraints  # User directly edits constraints
PATCH  /candidates/{id}/profile/preferences  # User directly edits preferences
```

---

## 8. Configuration

```
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/jobingestion

# LLM
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514

# Extraction
PYMUPDF_MIN_CHAR_THRESHOLD=100
EXTRACTION_VERSION=v1
CAPABILITY_TAXONOMY_VERSION=v1

# File storage
RESUME_STORAGE_PATH=./data/resumes

# Logging
LOG_LEVEL=INFO
```

---

## 9. Build Sequence

In order. Each step is independently testable.

**Step 1** — Project scaffold, models, Alembic migrations

**Step 2** — PyMuPDF extraction + multimodal fallback logic
- Validate with a set of sample PDFs including multi-column and creative layouts
- Confirm fallback triggers correctly on garbage extraction

**Step 3** — LLM extraction (Step A: evidence + skills)
- Pydantic models + Instructor binding
- Test against 2–3 real resume PDFs
- Validate taxonomy enforcement on capability names

**Step 4** — Diff engine (proposed change computation)
- Unit test merge heuristics against controlled evidence fixtures
- Test skill normalization alias map

**Step 5** — Patch creation + storage

**Step 6** — Patch commit + profile version write

**Step 7** — Capability recomputation (Step B)

**Step 8** — All API endpoints wired end-to-end

**Step 9** — Seed script for hardcoded test profiles
- `utils/seed.py` inserts 2–3 test candidates with pre-built profiles
- Bypasses the upload flow for early recommendation engine testing

---

## 10. Key Design Rules to Enforce

- **LLM output goes to evidence staging, never canonical profile directly.** The patch commit function is the only writer to `candidate_profiles`.
- **`candidate_resumes` and committed `candidate_profiles` are immutable.** No UPDATE on these rows, only INSERT.
- **Every evidence item carries `source_resume_id`.** Never insert evidence without provenance.
- **Skill normalization happens in `utils/text_utils.py`, not in the LLM prompt.** The LLM may suggest raw values; normalization is deterministic backend logic.
- **Capability table is fully replaced on recompute.** DELETE existing rows for candidate, INSERT new rows. No partial updates.
- **`is_current = true` is enforced as a single-row invariant per candidate.** When writing a new profile version, mark previous as `is_current = false` in the same transaction.
