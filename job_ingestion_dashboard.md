# Job Ingestion System — V2.2 Admin Dashboard Specification (Final)

---

## 1. Overview

V2.2 introduces an internal admin dashboard for the job ingestion system. The dashboard serves as **operations and review tooling** — combining operational visibility, reviewer workflows, and cost transparency in a single interface.

The primary users are non-technical reviewers and business stakeholders. The dashboard is internal-only and local during development. It will be deployed alongside the backend when the broader product goes live.

Future separation into a dedicated operations dashboard and a dedicated business/cost dashboard is intentionally deferred beyond V2.2.

---

## 2. Stack

| Concern | Choice |
|---|---|
| Framework | React |
| Language | JavaScript |
| Styling | Tailwind CSS |
| Charts | Recharts |
| HTTP client | fetch / axios |
| State management | React state + context |

The dashboard is a standalone React app communicating with the FastAPI backend via REST endpoints. No Redux for V2.2.

---

## 3. Navigation

Tab-based top-level navigation. Four tabs in fixed order:

```
[ Pipeline ]  [ Sources ]  [ Cost ]  [ Jobs ]
```

**Landing page:** Pipeline tab.

Order reflects reviewer priority — system health first, cost visibility second, job review last.

**Consistent layout pattern across all tabs:**
- **Summary strip** at the top: 3–4 key metric cards visible without scrolling.
- **Detailed content** below.

**Scalability constraint:** The dashboard is designed with the expectation that company counts, job counts, and event volumes will grow significantly. All tables use server-side pagination. No client-side full-dataset loading anywhere.

---

## 4. Pipeline Tab

### Purpose
Landing page. Shows the health and history of pipeline runs at a glance.

### Summary Strip

| Card | Value |
|---|---|
| Last Run Status | `Completed` / `Partial Success` / `Failed` — color-coded badge |
| Last Run Time | Relative timestamp (e.g. "2 hours ago") |
| Jobs Fetched (last run) | Total count |
| Failed Companies (last run) | Count — warning color if > 0 |

### Run History Table
Displays last 20 pipeline runs. Server-side paginated.

Columns:
- Timestamp (relative, absolute on hover)
- Status (color-coded badge)
- Total Companies
- Successful Companies
- Failed Companies
- Jobs Fetched
- Jobs New
- Jobs Updated
- Jobs Unchanged
- Duration

**Row interaction:** Clicking a run row expands an inline panel showing the per-company breakdown for that run.

Per-company breakdown columns:
- Company Name
- Platform
- Status
- Jobs Fetched
- Jobs New / Updated / Unchanged
- Error Message (if failed)

### Recent Events Panel
Located at the bottom of the Pipeline tab. Provides an operational activity feed — the dashboard's heartbeat.

Displays the most recent operational events with:
- Timestamp (relative)
- Severity badge (Info / Warning / Error / Critical)
- Event type (human-readable label)
- Related company / platform
- Short readable message

**Example visible events:**
- "Pipeline completed with partial success"
- "Ashby source failure threshold reached — OpenAI"
- "Reviewer corrected job metadata — Anthropic"
- "Malformed LLM response detected"
- "Token spike detected — Notion (12,400 input tokens)"

**Filters on the event feed:**
- Severity (multi-select)
- Platform (multi-select)
- Event Category (multi-select: Pipeline / Source / Enrichment / Review / System)

Server-side paginated. Loads incrementally as reviewer scrolls.

---

## 5. Sources Tab

### Purpose
Operational health view of all configured company sources. Allows reviewers to act on broken or problematic sources.

### Summary Strip

| Card | Value |
|---|---|
| Total Active Sources | Count |
| Sources with Failures | Count of companies with consecutive_fetch_failures > 0 |
| Paused Sources | Count of is_active = false |
| Flagged for Review | Count of companies marked requires_review |

### Sources Table
One row per company. Server-side paginated.

Columns:
- Company Name
- Platform (Greenhouse / Lever / Ashby — badge)
- Health (derived badge — see below)
- Active Jobs (total currently active normalized jobs)
- Last Successful Fetch (relative timestamp, absolute on hover)
- Last Failure (relative timestamp if applicable, absolute on hover)
- Consecutive Failures (shown as 0 or warning number if > 0)
- Status (Active / Paused / Flagged — badge)
- Actions

### Derived Health Badge

Each company displays a single derived health indicator to reduce cognitive load and surface unhealthy sources quickly.

| Badge | Color | Conditions |
|---|---|---|
| Healthy | Green | consecutive_failures = 0, no recent malformed source events |
| Warning | Yellow | consecutive_failures > 0, or intermittent extraction/enrichment issues |
| Critical | Red | repeated failures, source auto-disabled, repeated malformed payloads, or fetch threshold exceeded |

Health logic is heuristic-based and mutable over time — not hardcoded to exact thresholds.

### Actions Per Row

Two action buttons per company:
- **Pause / Resume** — toggles `is_active`. Label switches based on current state.
- **Flag for Review** — marks company `requires_review`, writes a source event. Disabled if already flagged.

### Row Interaction
Clicking a company row (not action buttons) expands an inline panel showing the last 10 ingestion events for that company, filtered from the event stream.

---

## 6. Cost Tab

### Purpose
Gives business stakeholders and operators visibility into LLM token usage and estimated cost across time, broken down by platform or company.

### Controls (above summary strip)

**Time period selector:**
- Per Run (dropdown of recent runs)
- Day (default)
- Month

**Split by filter:**
- By Platform
- By Company

### Summary Strip

| Card | Value |
|---|---|
| Total Input Tokens | Sum for selected period |
| Total Output Tokens | Sum for selected period |
| Estimated Cost | Approximate dollar cost for selected period (labeled as estimate) |
| Enrichment Failure Rate | % of failed enrichments for selected period |

### Cost Estimation Model

Estimated cost is computed dynamically using configurable pricing multipliers stored in environment variables:

```
LLM_INPUT_TOKEN_COST_PER_1K
LLM_OUTPUT_TOKEN_COST_PER_1K
```

Cost is always labeled as **"Estimated"** in the UI. This approach avoids hardcoding provider pricing and supports future LLM provider or model switching without schema changes.

### Breakdown View
Changes dynamically based on the Split By filter.

**When split by Platform:**
Bar chart + table showing input tokens, output tokens, estimated cost, and enrichment count per platform.

**When split by Company:**
Table showing input tokens, output tokens, estimated cost, enrichment count, average latency (ms), and failure count per company.

### Trend Chart
Line chart below the breakdown showing total token usage and estimated cost over time:
- Daily data points for Day and Month views
- Per-run data points for Run view

---

## 7. Jobs Tab

### Purpose
Primary reviewer work queue. Reviewers inspect, correct, and flag job records.

### Summary Strip

| Card | Value |
|---|---|
| Jobs Requiring Review | Count of jobs with `requires_review` |
| Enrichment Failures | Count of jobs with enrichment failure states |
| Manual Corrections Today | Count of reviewer edits today |
| Oldest Pending Review | Relative age of oldest unresolved review job |

### Default Filter State
On landing, the tab defaults to showing only jobs needing attention:
- `processing_state` in: `partial_success`, `extraction_failed`, `enrichment_failed`, `requires_review`

Reviewers can clear this filter to see all jobs.

### Filter Bar

| Filter | Type |
|---|---|
| Processing State | Multi-select dropdown |
| Platform | Multi-select dropdown |
| Company | Multi-select dropdown |
| Job Title | Text search |

Active filters shown as dismissible chips below the filter bar.

### Jobs Table
Server-side paginated with limit, offset, sorting, and filtering.

Columns:
- Job Title
- Company
- Platform (badge)
- Location
- Processing State (color-coded badge)
- Failure Reason (if present — shown as readable label via tooltip icon)
- Last Seen (relative, absolute on hover)
- Last Enrichment Attempt (relative, absolute on hover)
- Last Manual Review (relative if applicable)
- Actions

### Processing State Badge Colors

| State | Color |
|---|---|
| `success` | Green |
| `partial_success` | Yellow |
| `extraction_failed` / `enrichment_failed` | Orange |
| `requires_review` | Red |
| `manually_corrected` | Blue |
| `pending` | Grey |

### Job Detail Panel
Opens as a right-side slide-in panel on row click. Table remains visible behind it.

---

#### Panel Section 1 — Job Header
- Job title (prominent)
- Company name
- Platform badge
- "View Job Posting" button — opens posting URL in new tab

---

#### Panel Section 2 — Processing Status
- Current processing state (badge)
- Failure reason (human-readable label, not raw string)
- Last failure timestamp (relative, absolute on hover)
- Last enrichment attempt timestamp
- Last manual review timestamp

---

#### Panel Section 3 — Normalized Fields

Non-editable core fields (read-only):

| Field | Display |
|---|---|
| Title | Text |
| Company | Text |
| Location | Text |
| Department | Text |
| Employment Type | Text |
| Posted At | Relative timestamp |

Editable enrichment fields (form inputs):

| Field | Input Type |
|---|---|
| Seniority | Dropdown |
| Is Internship | Toggle |
| Is New Grad | Toggle |
| Sponsorship Status | Dropdown |
| Sponsorship Confidence | Dropdown |
| Remote Type | Dropdown |
| Tech Stack | Tag input |
| Skills | Tag input |

---

#### Panel Section 4 — Actions

Two buttons:
- **Save Changes** — enabled only when edits have been made. Requires comment before saving.
- **Flag for Engineering Review** — marks job `requires_review`. Requires comment before flagging.

**Comment Modal (triggered by either action):**
- Text area: "Add a comment (required)"
- Confirm button — disabled until comment is non-empty
- Cancel button

**On Save Changes confirm:**
- Normalized fields updated in DB
- `processing_state` set to `manually_corrected`
- `reviewer_edited_job` event written with comment in metadata

**On Flag confirm:**
- `processing_state` set to `requires_review`
- `job_marked_requires_review` event written with comment in metadata

---

#### Panel Section 5 — Raw Payload (collapsed by default)

Expandable section at the bottom of the panel. Reviewers can inspect but never modify.

- **"View Raw API Response"** toggle — expands formatted read-only JSON block
- **"View Raw HTML"** toggle below that — expands the raw job description HTML

---

## 8. Freshness Visibility

Relative timestamps are used throughout the dashboard. Absolute timestamps appear in tooltips on hover.

| Context | Freshness Fields Shown |
|---|---|
| Sources table | Last Successful Fetch, Last Failure |
| Jobs table | Last Seen, Last Enrichment Attempt, Last Manual Review |
| Pipeline table | Last Run Time, run timestamp per row |
| Events feed | Timestamp on every event |
| Summary strip cards | Last Run Time (Pipeline tab) |

Relative timestamp display conventions:
- Under 1 minute: "Just now"
- Under 1 hour: "X minutes ago"
- Under 24 hours: "X hours ago"
- Under 7 days: "Yesterday" / "X days ago"
- Beyond 7 days: absolute date

---

## 9. New API Endpoints Required

Endpoints required by the dashboard beyond what V2.1 delivers.

### Pipeline
```
GET /pipeline/runs?limit=20&offset=0
GET /pipeline/runs/{run_id}/companies
```

### Sources
```
GET /companies?include_job_counts=true&limit=50&offset=0
PATCH /companies/{id}                        # already exists — pause/resume
POST /companies/{id}/flag                    # flag for review + write event
```

### Events
```
GET /events?severity=&platform=&category=&limit=50&offset=0
GET /events/summary?period=day&date=
```

### Cost
```
GET /enrichments/usage?period=day&split_by=platform&date=
GET /enrichments/usage?period=month&split_by=company&month=
GET /enrichments/usage?period=run&run_id=&split_by=platform
GET /enrichments/usage/trend?period=day&days=30
```

### Jobs
```
GET /jobs?processing_state=&platform=&company=&title=&limit=50&offset=0&sort_by=&sort_dir=
GET /jobs/{job_id}
GET /jobs/{job_id}/raw
PATCH /jobs/{job_id}
POST /jobs/{job_id}/flag
```

---

## 10. Design Constraints

- **Non-technical readability.** Raw field names are never shown as labels. `processing_state: partial_success` displays as "Partial Success". `failure_reason: llm_timeout` displays as "LLM Timeout".
- **Status indicators over text.** Color-coded badges and health indicators preferred over plain text strings.
- **No raw JSON as primary view.** Raw payload always one click away, never the default visible state.
- **All reviewer actions require a comment.** Save and Flag both require a non-empty comment before executing. No accidental edits.
- **Raw layer is read-only.** Reviewers can view raw payloads but never modify them. No edit controls in raw sections.
- **Server-side pagination everywhere.** No client-side full-dataset loading. All tables support limit, offset, sorting, and filtering.
- **Estimated cost is always labeled as an estimate.** Never presented as exact billing.
- **Anonymous for V2.2.** No user identity attached to actions. Auth and reviewer identity deferred until product goes live.

---

## 11. Out of Scope for V2.2

- Authentication and user identity
- Reviewer name on audit events
- Email or push notifications
- Mobile responsiveness (desktop only)
- Dark mode
- Export / download functionality
- Separate operations vs. business dashboard split
- Public-facing job search UI