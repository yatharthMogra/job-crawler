# Job Recommendation System - Product Specification (V1)

## 1. Purpose

The recommendation system is designed to help students and early-career candidates discover and prioritize high-value opportunities quickly.

The system is optimized for:

* Early detection of newly posted jobs
* Efficient opportunity retrieval
* Lightweight personalization
* Scalable recommendation generation
* Minimal per-user compute cost

The system is NOT intended to be a fully AI-driven semantic recommendation engine in V1.

The architecture prioritizes:

* Shared computation
* Deterministic ranking
* Controlled infrastructure cost
* Fast retrieval
* Explainable recommendations

---

# 2. System Architecture

The recommendation platform consists of three independent systems:

```text
1. Job Ingestion Pipeline
2. Dashboard Service
3. Notification / Emailing Service
```

These systems communicate primarily through:

```text
Shared Jobs Database
```

Optional async communication:

```text
Publisher / Subscriber Queues
```

---

# 3. High-Level System Flow

```text
Crawler
↓
Job Enrichment
↓
Normalized Job Profile
↓
Retrieval Pool Assignment
↓
Shared Opportunity Ranking
↓
Jobs Database
↓
────────────────────────────
↓
Dashboard Service
↓
User Retrieval + SQL Filtering
↓
Dashboard Results
────────────────────────────
↓
Notification Service
↓
Personalized Ranking
↓
Top Opportunities
↓
Email / Push Notifications
```

---

# 4. Core Architectural Principles

## 4.1 Shared Computation First

Expensive computation must be shared across users whenever possible.

The system should avoid:

```text
user × all_jobs ranking
```

Instead:

```text
shared retrieval
+
lightweight personalization
```

---

## 4.2 Deterministic Recommendation Logic

V1 recommendation logic should be deterministic.

LLMs may be used for:

* Resume parsing
* Job enrichment
* Capability extraction
* Metadata normalization

LLMs should NOT be used for:

* Real-time recommendation
* Personalized ranking
* Dashboard retrieval
* Notification generation

---

## 4.3 Bounded Retrieval Space

Recommendation should occur only on a small candidate set.

The system should aggressively reduce retrieval space before personalization.

---

## 4.4 Controlled Taxonomy

Jobs and users must use a controlled normalized role taxonomy.

New normalized roles cannot be created dynamically during ingestion.

Unknown roles should map to:

```text
OTHER
```

---

# 5. System Components

# 5.1 Job Ingestion Pipeline

Repository:

```text
Independent Service
```

Purpose:

```text
Fetch jobs
→ enrich jobs
→ normalize jobs
→ assign retrieval pools
→ compute shared ranking signals
→ store final job profile
```

This pipeline executes once per job.

---

## 5.1.1 Inputs

Raw job data:

```yaml
title
description
company
location
salary
apply_url
posted_at
source_platform
```

Supported sources (V1):

```text
Greenhouse
Lever
Ashby
```

---

## 5.1.2 Job Enrichment

The enrichment layer generates structured metadata.

Example:

```yaml
normalized_roles:
  - SWE
  - BACKEND_ENGINEER

role_type:
  INTERNSHIP

capabilities:
  - BACKEND_ENGINEERING
  - DISTRIBUTED_SYSTEMS

skills:
  - Python
  - Java
  - AWS

application_effort:
  LOW
```

---

## 5.1.3 Retrieval Pool Assignment

Jobs are assigned to retrieval pools based on:

```text
normalized_role
+
role_type
```

Pools are intentionally limited and controlled.

Examples:

```text
SWE_INTERNSHIP
ML_ENGINEER_FULLTIME
DATA_ENGINEER_INTERNSHIP
```

Jobs may belong to multiple pools.

Example:

```text
ML_ENGINEER
+
BACKEND_ENGINEER
```

---

## 5.1.4 Shared Opportunity Ranking

Each job receives a shared opportunity score.

Initial V1 ranking signals:

```text
Freshness
Compensation
Application Effort
```

Future signals may include:

```text
Competition
Sponsorship Confidence
Application Velocity
Company Quality
```

---

## 5.1.5 Shared Opportunity Score

Example:

```text
opportunity_score =
  freshness_score
+ compensation_score
+ application_effort_score
```

This score is shared globally.

It is NOT personalized.

---

## 5.1.6 Persistence

Final enriched job profile is stored in the jobs database.

---

# 5.2 Dashboard Service

Repository:

```text
Independent Service
```

Purpose:

```text
Provide fast interactive retrieval of opportunities.
```

The dashboard is NOT deeply personalized.

The dashboard uses:

```text
retrieval pools
+
SQL filtering
```

---

## 5.2.1 User Onboarding

Users select:

* Interested normalized roles
* Internship/full-time preference
* Location preferences
* Compensation expectations

Example:

```yaml
interested_roles:
  - SWE
  - ML_ENGINEER

role_type:
  INTERNSHIP
```

---

## 5.2.2 Dashboard Retrieval Flow

### Step 1

Fetch jobs from subscribed retrieval pools.

Example:

```text
SWE_INTERNSHIP
ML_ENGINEER_INTERNSHIP
```

---

### Step 2

Apply SQL filters.

Examples:

```text
location
salary
remote
date_posted
```

---

### Step 3

Sort using shared opportunity score.

---

## 5.2.3 Dashboard Philosophy

The dashboard should provide:

```text
curated breadth
```

NOT:

```text
over-personalized suppression
```

Users should still discover opportunities outside narrow profile assumptions.

---

# 5.3 Notification / Emailing Service

Repository:

```text
Independent Service
```

Purpose:

```text
Actively prioritize opportunities worth immediate attention.
```

This is the primary personalization layer.

---

## 5.3.1 Trigger Model

Notifications are generated periodically.

Example:

```text
every 1 hour
every 3 hours
```

Notifications are batched.

---

## 5.3.2 Candidate Retrieval

The notification service retrieves jobs from:

```text
user subscribed retrieval pools
```

Then applies:

```text
SQL filters
```

---

## 5.3.3 Personalized Ranking

The candidate set is small.

Example:

```text
20-50 jobs
```

The system runs deterministic scoring.

Example signals:

```text
Capability overlap
Skill overlap
Experience alignment
Location preference
Compensation preference
```

---

## 5.3.4 Personalized Recommendation Score

Example:

```text
recommendation_score =
  capability_overlap
+ experience_overlap
+ location_alignment
+ compensation_alignment
```

---

## 5.3.5 Explainability

Recommendations must be explainable.

Example:

```text
Why this fits:
✓ Walmart backend experience
✓ AWS
✓ RAG systems
```

Explanation generation must be deterministic.

No LLM usage in notification generation.

---

## 5.3.6 Final Notification Output

The service selects:

```text
Top 4 opportunities
```

for:

* Email
* Push notifications
* Discord / Telegram
* Browser notifications

---

# 6. Controlled Taxonomy

# 6.1 Normalized Role Taxonomy (V1)

Initial controlled taxonomy:

```text
SWE
BACKEND_ENGINEER
FRONTEND_ENGINEER
FULLSTACK_ENGINEER
ML_ENGINEER
DATA_ENGINEER
DATA_SCIENTIST
DEVOPS_ENGINEER
SECURITY_ENGINEER
MOBILE_ENGINEER
PRODUCT_MANAGER
OTHER
```

This taxonomy is mutable but controlled.

---

# 6.2 Role Assignment Rules

Jobs may belong to multiple normalized roles.

Example:

```text
ML Infrastructure Engineer
→ ML_ENGINEER
→ BACKEND_ENGINEER
```

---

# 7. Database Philosophy

The jobs database acts as the shared source of truth between systems.

All systems remain independently deployable.

---

# 8. V1 Non-Goals

The following are intentionally excluded from V1:

* Deep semantic reranking
* Real-time LLM recommendation
* Behavior-adaptive recommendations
* Company prestige scoring
* Recruiter responsiveness modeling
* Social graph signals
* Collaborative filtering
* Vector retrieval infrastructure
* Real-time streaming personalization

---

# 9. V1 Success Criteria

The system succeeds if users consistently feel:

```text
These recommendations save me time
and help me focus on better opportunities faster.
```

Primary metrics:

```text
Email open rate
Click-through rate
Applications submitted
Notification retention
User retention
```

---

# 10. Future Extensions

Potential future additions:

* Sponsorship confidence
* Competition estimation
* Application velocity
* Company responsiveness
* Resume tailoring
* Auto-apply agents
* Behavioral personalization
* Conversion-aware ranking
* Opportunity outcome prediction
