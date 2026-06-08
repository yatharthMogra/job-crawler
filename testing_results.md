# User Recommendation Results

Generated 2026-06-08 04:41 UTC after location scoring fix + notification dedup (889/889 enriched jobs).

Pools synced via `PATCH /subscriptions`. Same subscription buckets as prior run.

**Ranking modes:**
- **Dashboard** — sorted by global `opportunity_score` (freshness + comp + effort)
- **Personalized / Email** — sorted by profile match score (capabilities 40%, skills 25%, location 20%, comp 15%)

Full machine-readable export: [`exports/user_recommendations.json`](exports/user_recommendations.json)

## Changes vs prior run (pre-Ashby fix)

| Metric | Yatharth (before → now) | Ram (before → now) |
|--------|--------------------------|---------------------|
| Matching jobs | 260 → **317** | 263 → **321** |
| Unique personal scores | ~6 flat tiers → **57** | ~5 flat tiers → **15** |
| Personal score range | 0.075–0.3417 → **0.0750–0.5654** | 0.075–0.375 → **0.1750–0.5687** |
| Skills in top-4 | empty on most | **populated** |
| Ashby jobs in pool | 0 | **281 enriched** |
| Ramp/Notion/Linear visible | 0 → **65** | 0 → **62** |

**Observations:**
- Segment-aware location matcher now boosts NY-listed jobs when prefs are `NY, USA` / `New York, USA`.
- Notification top-4 dedupes same company+title across cities (keeps highest personal score).
- Yatharth top-4 is NY/SF-multi-city heavy (ScaleAI, Figma, Ramp) — no Doha/London/Mexico outliers.
- Ram top-4 includes Figma data science (#1) and Ramp data platform (#2).
- Personal score spread: Yatharth 57 unique tiers, Ram 15 unique tiers.

---

## Yatharth Mogra (`yatharthmogra@gmail.com`)

**Candidate ID:** `6230dd88-b346-4e96-94fd-4a51c4500f34`

### Subscribed pools
- `SWE_FULLTIME`
- `BACKEND_ENGINEER_FULLTIME`
- `ML_ENGINEER_FULLTIME`
- `FULLSTACK_ENGINEER_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Backend Engineering, Full Stack Development, AI Systems, Machine Learning Research, Data Engineering, Distributed Systems, Cloud Infrastructure, DevOps, Research |
| Preferred locations | NY, USA, New York, USA |
| Primary roles | Software Developer, AI Engineer, Data Engineer, Software Engineer |
| Hard constraints | sponsorship=False, min_salary=None |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 317
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 272 |
| `BACKEND_ENGINEER_FULLTIME` | 182 |
| `ML_ENGINEER_FULLTIME` | 81 |
| `FULLSTACK_ENGINEER_FULLTIME` | 73 |
| `DEVOPS_ENGINEER_FULLTIME` | 45 |
| `FRONTEND_ENGINEER_FULLTIME` | 36 |
| `DATA_ENGINEER_FULLTIME` | 27 |
| `DATA_SCIENTIST_FULLTIME` | 19 |
| `SECURITY_ENGINEER_FULLTIME` | 18 |
| `PRODUCT_MANAGER_FULLTIME` | 6 |
| `OTHER_FULLTIME` | 6 |
| `MOBILE_ENGINEER_FULLTIME` | 3 |

### Email notification — top 4 (personalized)

#### #1 — Infrastructure Software Engineer, Enterprise GenAI @ ScaleAI

- **Location:** San Francisco, CA; New York, NY (unclear)
- **Posted:** 2026-05-26T23:28:58+00:00
- **Salary:** 216000 – 270000
- **Effort:** MEDIUM
- **Opportunity score:** 0.529
- **Personal score:** 0.5654
- **Pools:** `BACKEND_ENGINEER_FULLTIME`, `DEVOPS_ENGINEER_FULLTIME`
- **Roles:** BACKEND_ENGINEER, DEVOPS_ENGINEER
- **Capabilities:** Backend Engineering, Distributed Systems, Cloud Infrastructure, DevOps, AI Systems
- **Skills:** distributed systems, large-scale systems, LLMs, vector databases, cloud architecture
- **Match reasons:** Backend Engineering, Distributed Systems, Cloud Infrastructure, DevOps, AI Systems
- **URL:** https://job-boards.greenhouse.io/scaleai/jobs/4665557005

#### #2 —  Senior Software Engineer,  Full-Stack – Scale GP @ ScaleAI

- **Location:** San Francisco, CA; New York, NY (unclear)
- **Posted:** 2026-05-26T23:28:59+00:00
- **Salary:** 216000 – 270000
- **Effort:** MEDIUM
- **Opportunity score:** 0.529
- **Personal score:** 0.5437
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `FRONTEND_ENGINEER_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, FRONTEND_ENGINEER, FULLSTACK_ENGINEER
- **Capabilities:** Backend Engineering, Frontend Engineering, Full Stack Development, AI Systems, Machine Learning, Distributed Systems
- **Skills:** LLMs, vector databases, data pipelines, microservice architectures, API development
- **Match reasons:** Backend Engineering, Full Stack Development, AI Systems, Distributed Systems, React
- **URL:** https://job-boards.greenhouse.io/scaleai/jobs/4637484005

#### #3 — Software Engineer, Distributed Systems @ Figma

- **Location:** San Francisco, CA • New York, NY • United States (unclear)
- **Posted:** 2026-04-15T19:32:40+00:00
- **Salary:** 153000 – 376000
- **Effort:** MEDIUM
- **Opportunity score:** 0.52
- **Personal score:** 0.5437
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER
- **Capabilities:** Backend Engineering, Distributed Systems, Cloud Infrastructure, Platform Engineering, DevOps
- **Skills:** Distributed systems, Compute orchestration, CI/CD, Networking, Traffic management, DDoS mitigation
- **Match reasons:** Backend Engineering, Distributed Systems, Cloud Infrastructure, DevOps, Go
- **URL:** https://boards.greenhouse.io/figma/jobs/5552549004?gh_jid=5552549004

#### #4 — Backend Engineer, Ops @ Ramp

- **Location:** New York, NY (HQ) (unclear)
- **Posted:** 2026-03-04T05:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.32
- **Personal score:** 0.5437
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `FRONTEND_ENGINEER_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, FRONTEND_ENGINEER, FULLSTACK_ENGINEER
- **Capabilities:** Backend Engineering, Frontend Engineering, Full Stack Development, Platform Engineering, DevOps, AI Systems
- **Skills:** Full-stack development, API design, Database systems, AI integration, Internal tooling
- **Match reasons:** Backend Engineering, Full Stack Development, DevOps, AI Systems, Python
- **URL:** https://jobs.ashbyhq.com/ramp/7bfa613e-151c-469b-9973-c89ee3d14838

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Infrastructure Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.5654 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 2 |  Senior Software Engineer,  Full-Stack – Scale GP | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.5437 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 3 | Software Engineer, Distributed Systems | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.5437 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 4 | Backend Engineer, Ops | Ramp | New York, NY (HQ) | 0.32 | 0.5437 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, DevOps |
| 5 | Senior Software Engineer, Public Sector | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.517 | 0.5417 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Data Engineering |
| 6 | Staff Infrastructure Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5423 | 0.521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 7 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.529 | 0.521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 8 | Staff Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5203 | 0.521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 9 | Software Engineer, Developer Experience | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 10 | Software Engineer, Production Engineering | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.32 | 0.521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 11 | Staff Software Engineer, Data Platform | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.5199 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 12 | Frontier Agent Engineering Manager, Enterprise | ScaleAI | San Francisco, CA; New York, NY | 0.513 | 0.5199 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 13 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.4519 | 0.5199 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 14 | Software Engineer, Banking | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.3425 | 0.4992 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 15 | Senior AI Infrastructure Engineer, Model Serving Platform | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.4982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 16 | Senior AI Infrastructure Engineer - Training Platform | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.529 | 0.4982 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 17 | Software Engineer, Data Infrastructure | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 18 | Software Engineer, AI Platforms | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 19 | Applied AI Engineer | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4982 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 20 | Manager, Software Engineering - DevEx AI Tools | Figma | San Francisco, CA • New York, NY • United States | 0.6673 | 0.4972 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 21 | Technical Program Manager, AI Performance | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4972 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 22 | Forward Deployed Infrastructure Engineer - US Government | Palantir | New York, NY | 0.32 | 0.4972 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 23 | Software Engineer, Full Stack | Figma | San Francisco, CA • New York, NY • United States | 0.5201 | 0.4775 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, React |
| 24 | Marketing Engineer, AI Deployment | Figma | San Francisco, CA • New York, NY • United States | 0.6871 | 0.4765 | SWE_FULLTIME, OTHER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 25 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.5747 | 0.4765 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 26 | Senior Software Engineer, GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.4765 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 27 | Forward Deployed Engineer, GTM | Notion | San Francisco, California / New York, New York | 0.439 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 28 | Software Engineer, Fraud & Identity | Ramp | New York, NY (HQ) | 0.32 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, DevOps |
| 29 | Software Engineer, Guest Travel | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Denver, CO | 0.32 | 0.4765 | FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 30 | Senior Staff Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.5424 | 0.4755 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Data Engineering, Cloud Infrastructure |
| 31 | Staff Frontier Agents Engineer  | ScaleAI | San Francisco, CA; New York, NY | 0.5424 | 0.4755 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Data Engineering, Cloud Infrastructure |
| 32 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.4755 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Data Engineering, Cloud Infrastructure |
| 33 | Staff Software Engineer, Full-Stack - Enterprise Gen AI | ScaleAI | New York, NY; San Francisco, CA | 0.5424 | 0.4548 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, React |
| 34 | Software Engineer, Growth & Monetization | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4548 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 35 | Software Engineer, C++ | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4548 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 36 | Software Engineer, Core Product | Ramp | New York, NY (HQ) | 0.32 | 0.4548 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 37 | Software Engineer, Machine Learning | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4538 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Data Engineering |
| 38 | Software Engineer, Code Platform | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 39 | Software Engineer, Data Platform  | Ramp | New York, NY (HQ) | 0.32 | 0.4538 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, AI Systems, Cloud Infrastructure |
| 40 | Staff Software Engineer, Public Sector | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.5423 | 0.4528 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Data Engineering |
| 41 | Manager, Software Engineering - Observability | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4528 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 42 | Software Engineer - Hosted Model Infrastructure | Palantir | New York, NY | 0.4665 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 43 | Software Engineer - Apollo Platform | Palantir | New York, NY | 0.32 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 44 | Software Engineer - Apollo Systems | Palantir | New York, NY | 0.32 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 45 | DevOps Engineer | Palantir | New York, NY | 0.32 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 46 | Senior Software Engineer, Substrate | Palantir | New York, NY | 0.32 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 47 | Senior Software Engineer, Network Infrastructure | Palantir | New York, NY | 0.32 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 48 | Software Engineer, Robotics & Autonomous Systems | ScaleAI | San Francisco, CA | 0.4519 | 0.4326 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 49 | Software Engineer, Trust | Notion | San Francisco, California / New York, New York | 0.5011 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, React |
| 50 | Software Engineer, Product Infrastructure | Notion | San Francisco, California / New York, New York | 0.4714 | 0.4321 | FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, PostgreSQL |
| 51 | Software Engineer, Stablecoin | Ramp | New York, NY (HQ) / San Francisco, CA | 0.3208 | 0.4321 | SWE_FULLTIME | Distributed Systems, AI Systems, Python |
| 52 | Security Engineer, Privacy | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.32 | 0.4321 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 53 | AI Operations Specialist / Agentic Workflows | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4321 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 54 | Enterprise Technical Support Specialist - NYC | Notion | New York, New York | 0.3076 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 55 | Research Scientist, Frontier Risk Evaluations | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.4311 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning Research, AI Systems, Data Engineering |
| 56 | Software Engineer, Credit | Ramp | New York, NY (HQ) | 0.3208 | 0.4311 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, AI Systems |
| 57 | Machine Learning Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3203 | 0.4311 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research, Cloud Infrastructure |
| 58 | Software Engineer, AI DevX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, AI Systems |
| 59 | Software Engineer, Accounting | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4311 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, AI Systems |
| 60 | Software Engineer, Agent Developer Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4311 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, AI Systems |
| 61 | AI Applied Scientist | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4093 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Machine Learning Research, Python |
| 62 | Software Engineer, AI Workflows | Notion | San Francisco, California / New York, New York | 0.5025 | 0.4093 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Distributed Systems, React |
| 63 | AI Builder Intern | ScaleAI | San Francisco, CA; New York, NY | 0.4826 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Python |
| 64 | Strategic Projects Lead - Coding  | ScaleAI | San Francisco, CA; New York, NY | 0.3317 | 0.4093 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, SQL |
| 65 | Senior Software Engineer / GTM Platform, Backend | Ramp | New York, NY (HQ) | 0.3208 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 66 | SWE Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3203 | 0.4093 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning Research, AI Systems, Python |
| 67 |  Security Engineer, Cloud | Ramp | New York, NY (HQ) / Miami, FL / Remote (US) / Remote (Canada) | 0.32 | 0.4093 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 68 | Software Engineer, Bill Pay & Procurement | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4093 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 69 | Engineering Manager, AgentOps | ScaleAI | San Francisco, CA; New York, NY | 0.6626 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 70 | Distinguished Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.4083 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Cloud Infrastructure |
| 71 |  Machine Learning Research Engineer, Agent Data Foundation - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.4083 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research, Data Engineering |
| 72 | Machine Learning Systems Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.4083 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Machine Learning Research, Distributed Systems |
| 73 | Tech Lead Manager- MLRE, ML Systems | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.4083 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 74 | Software Engineer, Production Engineering | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4083 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, DevOps |
| 75 | Machine Learning Research Engineer, GenAI Applied ML | ScaleAI | San Francisco, CA; New York, NY | 0.4724 | 0.4083 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, AI Systems |
| 76 | ML Research Engineer, ML Systems | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.4504 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 77 | Software Engineer, Frontier AI Infrastructure | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.4447 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 78 | Software Engineer, ARC Team | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.4447 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 79 | Technical Consultant / Strategic | Ramp | New York, NY (HQ) / Miami, FL / San Francisco, CA / Remote (US) / Remote (Canada) | 0.3829 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 80 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | New York, NY | 0.3202 | 0.4083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, AI Systems |
| 81 | Sr Software Engineer - Core Backend & Platform Engineering | Basis | United States | 0.3201 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 82 | Forward Deployed Software Engineer | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, AI Systems |
| 83 | Full Stack Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 84 | Software Engineer - Mission Manager | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 85 | Backend Software Engineer - Infrastructure | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Full Stack Development |
| 86 | Forward Deployed Software Engineer, Internship - Poland | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 87 | Forward Deployed Software Engineer - US Government | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 88 | Forward Deployed Software Engineer - Warp Speed | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Data Engineering |
| 89 | Senior Backend Software Engineer - Infrastructure | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 90 | Backend Software Engineer - Infrastructure, Foundations | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Data Engineering |
| 91 | Product Reliability Engineer - Defense | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 92 | Software Engineer - Environment Platform | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, DevOps |
| 93 | Systems Engineer - Business Systems | Palantir | New York, NY | 0.32 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 94 | Mobile Engineer, iOS | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (Canada) / Remote (US) | 0.32 | 0.3886 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript, Python |
| 95 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | Doha, Qatar  | 0.6907 | 0.3881 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 96 | Software Engineer, Robotics | ScaleAI | Mexico City, MX | 0.3423 | 0.3881 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 97 | Product Operations Manager | Notion | San Francisco, California / New York, New York | 0.3867 | 0.3876 | SWE_FULLTIME | AI Systems, Python, Go |
| 98 | Senior Machine Learning Engineer, Public Sector | ScaleAI | San Francisco, CA; New York, NY; Washington, DC | 0.6662 | 0.3866 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 99 | Senior Machine Learning Engineer - Model Evaluations, Public Sector | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.6662 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 100 | Research Scientist, Safety Post Training | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.3866 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning Research, AI Systems, Python |
| 101 | Senior/Staff Machine Learning Engineer, General Agents, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5203 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 102 | Data Platform Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3866 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 103 | Sales AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.46 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Backend Engineering, SQL |
| 104 | Product Manager / Agentic CX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.3208 | 0.3866 | PRODUCT_MANAGER_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Data Engineering, Python |
| 105 | Software Engineer, Growth Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.3866 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 106 | Software Engineer, Enterprise | ScaleAI | London, UK | 0.3597 | 0.3664 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 107 | Software Engineer (Backend), Enterprise | ScaleAI | Budapest, Hungary | 0.3597 | 0.3664 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 108 | Director, Forward Deployed Engineering | ScaleAI | London, UK | 0.3423 | 0.3654 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 109 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.3649 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript, React |
| 110 | Solutions Engineer, Enterprise | ScaleAI | San Francisco, CA; New York, NY | 0.4519 | 0.3649 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 111 | Technical Program Manager | Ramp | New York, NY (HQ) | 0.3268 | 0.3649 | OTHER_FULLTIME, SWE_FULLTIME | DevOps, Python, Go |
| 112 | Senior Applied Scientist, Credit Risk | Ramp | New York, NY (HQ) | 0.3205 | 0.3649 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, Python, SQL |
| 113 | Software Engineer, Mobile AI, iOS | Notion | New York, New York | 0.3201 | 0.3649 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, TypeScript, React |
| 114 | Security Engineer, Product | Ramp | New York, NY (HQ) | 0.32 | 0.3649 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Python, Flask |
| 115 | Model Behavior Engineer | Notion | New York, New York / San Francisco, California | 0.2705 | 0.3649 | ML_ENGINEER_FULLTIME, PRODUCT_MANAGER_FULLTIME | AI Systems, SQL, Python |
| 116 | Manager, Software Engineering - Growth Platform  | Figma | San Francisco, CA • New York, NY • United States | 0.6674 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems |
| 117 | Director, Enterprise Machine Learning & Research | ScaleAI | San Francisco, CA; New York, NY | 0.5633 | 0.3639 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning Research |
| 118 | Machine Learning Research Engineer, Agents - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.3639 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning Research, AI Systems |
| 119 | Staff Machine Learning Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.3639 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research |
| 120 | Research Scientist, AI Controls and Monitoring | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.3639 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning Research, AI Systems |
| 121 | Research Scientist, Agent Robustness | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.3639 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning Research, AI Systems |
| 122 | Security Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.521 | 0.3639 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, AI Systems |
| 123 | Manager, Machine Learning Research Scientist, GenAI | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.3639 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning Research, AI Systems |
| 124 | Machine Learning Research Scientist, Reasoning | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.3639 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning Research, AI Systems |
| 125 | Senior / Staff Machine Learning Research Scientist, Agents | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.3639 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning Research |
| 126 | Machine Learning Research Scientist, Post-Training | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.3639 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research |
| 127 | Manager, Software Engineering - Search & Recommendations | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3639 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering |
| 128 | Manager, Software Engineering - Billing | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering |
| 129 | Manager, Software Engineering - Interaction Design | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 130 | Forward Deployed Engineer, GenAI  | ScaleAI | San Francisco, CA; New York, NY | 0.4506 | 0.3639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering |
| 131 | Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 132 | Sr Software Engineer - Basis Platform / DSP | Basis | United States | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 133 | Forward Deployed Software Engineer, Internship - France | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering |
| 134 | Neurodivergent Fellowship | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems |
| 135 | Senior Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 136 | Software Engineer - Developer Productivity | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 137 | Forward Deployed Reliability Engineer | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 138 | Senior Software Engineer - Observability | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 139 | Backend Software Engineer - Defense | Palantir | New York, NY | 0.32 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 140 | Software Engineer, Robotics | ScaleAI | Argentina; Uruguay | 0.3203 | 0.3437 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 141 | Staff FullStack Software Engineer, (Forward Deployed), GPS | ScaleAI | Doha, Qatar  | 0.3203 | 0.3427 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 142 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, TypeScript |
| 143 | Senior Software Engineer / GTM Platform, Frontend | Ramp | New York, NY (HQ) | 0.32 | 0.3422 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, React |
| 144 | Software Engineer, AI Forward Deployed | Ramp | San Francisco, CA / New York, NY (HQ) | 0.32 | 0.3422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 145 | Software Engineer, Engineering Platform | Ramp | New York, NY (HQ) | 0.32 | 0.3422 | SWE_FULLTIME | DevOps, Python |
| 146 | Platform Intelligence Engineer | Palantir | New York, NY | 0.32 | 0.3422 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, data pipelines |
| 147 | AI Applications Ops Lead, GPS | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.3417 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 148 | Senior Software Engineer - Internal Tools & Productivity | ScaleAI | San Francisco, CA | 0.529 | 0.322 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 149 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5535 | 0.321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 150 | DevOps Engineer, GPS | ScaleAI | Doha, Qatar  | 0.3423 | 0.321 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 151 | Senior / Staff Product Engineer | Linear | Europe | 0.32 | 0.321 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 152 | Senior / Staff Product Engineer | Linear | North America | 0.32 | 0.321 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 153 | Software Engineer, Web Infrastructure | Notion | San Francisco, California / New York, New York | 0.5486 | 0.3205 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | React, TypeScript |
| 154 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.5201 | 0.3194 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems |
| 155 | Manager, Software Engineering - AI Product  | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3194 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems |
| 156 | Partner Solutions Engineer | Notion | New York, New York / San Francisco, California | 0.501 | 0.3194 | SWE_FULLTIME | AI Systems |
| 157 | Engineering Manager, Mobile AI | Notion | New York, New York | 0.4967 | 0.3194 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems |
| 158 | Product Designer, AI Models | Figma | San Francisco, CA • New York, NY • United States | 0.4933 | 0.3194 | ML_ENGINEER_FULLTIME | AI Systems |
| 159 | Manager, Web Experience | ScaleAI | San Francisco, CA; New York, NY | 0.4056 | 0.3194 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 160 | Senior Identity Security Engineer | Palantir | New York, NY | 0.3553 | 0.3194 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering |
| 161 | Staff Technical Product Manager | ScaleAI | London, UK; New York, NY; San Francisco, CA | 0.3423 | 0.3194 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | AI Systems |
| 162 | Year at Palantir - Software Engineer, Internship | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems |
| 163 | Senior Front End Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering |
| 164 | Software Engineer - Frontend Developer Productivity | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Full Stack Development |
| 165 | Forward Deployed Enablement Engineer - Customer Success | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 166 | Partner Development Representative / Financial Institutions | Ramp | New York, NY (HQ) / Remote (US) / San Francisco, CA / Miami, FL | 0.32 | 0.3194 | PRODUCT_MANAGER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 167 | Forward Deployed AI Engineer | Palantir | New York, NY | 0.32 | 0.3194 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems |
| 168 | Incident Management Engineer | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 169 | Year at Palantir - Forward Deployed Software Engineer, Internship - USG | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems |
| 170 | Year at Palantir - Forward Deployed Software Engineer, Internship - Commercial | Palantir | New York, NY | 0.32 | 0.3194 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems |
| 171 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5536 | 0.2992 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 172 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3203 | 0.2992 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Cloud Infrastructure |
| 173 | Principal Architect | ScaleAI | Washington, DC | 0.5423 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Cloud Infrastructure |
| 174 | Staff Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3203 | 0.2982 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 175 | Intermediate Software Engineer (Backend Engineering) | Achievers | Toronto | 0.32 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 176 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Honolulu, HI | 0.3201 | 0.2972 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 177 | Forward Deployed Infrastructure Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2972 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 178 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.3381 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 179 | Senior / Staff Product Engineer, AI | Linear | North America | 0.32 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 180 | Senior / Staff Fullstack Engineer | Linear | Europe | 0.32 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 181 | Forward Deployed Engineer, GTM, France | Notion | Paris, France | 0.319 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 182 | Forward Deployed Software Engineer, Internship | Palantir | Paris, France | 0.2402 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 183 | Field Engineer, Public Sector | ScaleAI | Colorado Springs, CO; St. Louis, MO; Washington, DC | 0.5656 | 0.2755 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 184 | Edge Infrastructure Engineer | Palantir | Paris, France | 0.32 | 0.2755 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 185 | Edge Infrastructure Engineer | Palantir | Warsaw, Poland | 0.32 | 0.2755 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 186 | Solutions Consultant | Figma | San Francisco, CA • New York, NY • United States | 0.4712 | 0.275 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 187 | Software Engineer, Product Growth | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.275 | SWE_FULLTIME | ETL |
| 188 | Application Security Engineer | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 189 | Compliance Engineer | Palantir | New York, NY | 0.32 | 0.275 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 190 | Software Engineer, Argentina | Ramp | Remote (Buenos Aires, Argentina) | 0.32 | 0.2548 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 191 | Software Engineer, New Grad (AI) | Notion | San Francisco, California | 0.3029 | 0.2548 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, TypeScript |
| 192 | Software Engineer, New Grad | Notion | San Francisco, California | 0.3029 | 0.2548 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 193 | ML Systems Engineer, Robotics | ScaleAI | San Francisco, CA | 0.5423 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 194 | Mission Software Engineer, Public Sector | ScaleAI | Colorado Springs, CO; Honolulu, HI; St. Louis, MO; Washington, DC | 0.4762 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 195 | Head of Finance Systems & Automation | ScaleAI | San Francisco, CA | 0.4692 | 0.2538 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 196 | SWE Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3203 | 0.2538 | SWE_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research, Research |
| 197 | Software Engineer, Developer Experience | Notion | Hyderabad, India | 0.32 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, DevOps |
| 198 | Software Engineer - Hosted Model Infrastructure | Palantir | Washington, D.C. | 0.4665 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 199 | Software Engineer - Hosted Model Infrastructure | Palantir | Palo Alto, CA | 0.4664 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 200 | Principal AI Ops Architect, GPS | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.2528 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 201 | Frontier Agent Engineering Manager | ScaleAI | Berlin, Germany; London, UK | 0.3283 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 202 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 203 | Software Engineer - Apollo Platform | Palantir | London, United Kingdom | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 204 | Software Engineer - Apollo Systems | Palantir | Seattle, WA | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 205 | Senior Software Engineer, Substrate | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 206 | Senior Software Engineer, Substrate | Palantir | London, United Kingdom | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 207 | Senior Software Engineer, Substrate | Palantir | Seattle, WA | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 208 | DevOps Engineer | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 209 | Software Engineer - Environment Platform | Palantir | Seattle, WA | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 210 | Software Engineer - Mission Manager | Palantir | Seattle, WA | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 211 | Software Engineer - Apollo Platform | Palantir | Seattle, WA | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 212 | Product Reliability Engineer - Defense | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 213 | Software Engineer - Mission Manager | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 214 | Site Reliability Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 215 | Senior Software Engineer, Network Infrastructure | Palantir | Washington, D.C. | 0.32 | 0.2528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 216 | Senior / Staff Fullstack Engineer | Linear | North America | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 217 | Software Engineer Intern (Fall 2026) | Notion | San Francisco, California | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, TypeScript |
| 218 | Forward Deployed Engineer, GTM - Korea | Notion | Seoul, South Korea | 0.32 | 0.2321 | SWE_FULLTIME | Backend Engineering, AI Systems, Java |
| 219 | Frontier Agents Engineer | ScaleAI | London, UK | 0.5598 | 0.2311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 220 | Technical Lead Manager, Physical AI | ScaleAI | San Francisco, CA | 0.5423 | 0.2311 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning Research, Distributed Systems |
| 221 | Machine Learning Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.2311 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Backend Engineering, Distributed Systems |
| 222 | Machine Learning Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3203 | 0.2311 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research, Cloud Infrastructure |
| 223 | Machine Learning Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.3203 | 0.2311 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning Research, Cloud Infrastructure |
| 224 | Solutions Engineer (Clearance Required) | ScaleAI | Washington, DC | 0.4656 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 225 | Solutions Engineer, Enterprise | ScaleAI | London, UK | 0.3423 | 0.2093 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 226 | Strategic Projects Lead - Coding | ScaleAI | Mexico City, MX | 0.3203 | 0.2093 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, AI Systems, SQL |
| 227 | SWE Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.3203 | 0.2093 | SWE_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Research, Python |
| 228 | Senior Software Engineer (Backend Engineering) ⭐ | Achievers | Toronto | 0.32 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 229 | Software Engineer, AI Product (London, United Kingdom) | Figma | London, England | 0.32 | 0.2093 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, React |
| 230 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Distributed Systems |
| 231 | Software Engineer, Infrastructure  | Notion | Hyderabad, India | 0.4732 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 232 | Intermediate Software Engineer | Achievers | Canada | 0.429 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 233 | AI Applications Engineer | Notion | San Francisco, California | 0.4267 | 0.2083 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | AI Systems, Data Engineering, Cloud Infrastructure |
| 234 | GTM Systems Analyst | ScaleAI | San Francisco, CA | 0.4017 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 235 | Finance Systems & Automations Manager | ScaleAI | San Francisco, CA | 0.3994 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 236 | Staff Software Engineer | Achievers | Canada | 0.3618 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 237 | Forward Deployed Software Engineer, Internship - AUS Government | Palantir | Sydney, Australia | 0.3612 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 238 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | Washington, D.C. | 0.3202 | 0.2083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, AI Systems |
| 239 | Forward Deployed Software Engineer | Palantir | Vilnius, Lithuania | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 240 | Forward Deployed Software Engineer | Palantir | Stockholm, Sweden | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 241 | Edge Infrastructure Engineer | Palantir | London, United Kingdom | 0.32 | 0.2083 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, DevOps |
| 242 | Forward Deployed Software Engineer - Tactical Edge | Palantir | Washington, D.C. | 0.32 | 0.2083 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 243 | Systems Engineer - Business Systems | Palantir | London, United Kingdom | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 244 | Forward Deployed Software Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 245 | Forward Deployed Software Engineer | Palantir | London, United Kingdom | 0.32 | 0.2083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, AI Systems |
| 246 | Forward Deployed Software Engineer | Palantir | Tel Aviv, Israel | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 247 | Forward Deployed Software Engineer - US Government | Palantir | San Diego, CA | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 248 | Forward Deployed Software Engineer - AUS Government | Palantir | Canberra, Australia | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 249 | Forward Deployed Software Engineer, Internship - US Government | Palantir | Honolulu, HI | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 250 | Forward Deployed Software Engineer - AUS Government | Palantir | Sydney, Australia | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 251 | Forward Deployed Software Engineer - US Government | Palantir | Fayetteville, NC | 0.32 | 0.2083 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 252 | Forward Deployed Software Engineer | Palantir | Amsterdam, Netherlands | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 253 | Forward Deployed Software Engineer | Palantir | Seoul, South Korea | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 254 | Senior Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Data Engineering |
| 255 | Forward Deployed Software Engineer | Palantir | Dubai, United Arab Emirates | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 256 | Forward Deployed Software Engineer | Palantir | Abu Dhabi, United Arab Emirates | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 257 | Senior Software Engineer, Network Infrastructure | Palantir | Seattle, WA | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 258 | Systems Engineer - Business Systems | Palantir | Denver, CO | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 259 | Forward Deployed Software Engineer - Japan Government | Palantir | Tokyo, Japan | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 260 | Forward Deployed Software Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 261 | Applied AI Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.1876 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python, TypeScript |
| 262 | Enterprise Technical Support Specialist, Korea | Notion | Seoul, South Korea | 0.32 | 0.1876 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 263 | Production Engineer - Database Operations | Palantir | Singapore, Singapore | 0.32 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 264 | Strategic Projects Lead - Coding | ScaleAI | India | 0.3212 | 0.1649 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 265 | AI Strategy Consultant, Frontier Tech | ScaleAI | San Francisco, CA | 0.3203 | 0.1649 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning Research, Python, SQL |
| 266 | Solutions Engineer, EMEA | Notion | Dublin, Ireland | 0.32 | 0.1649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL, Python |
| 267 | Director of Technology & Systems | ScaleAI | San Francisco, CA | 0.5423 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering |
| 268 | Engineering Manager, Context (Agentic Search) | Notion | San Francisco, California | 0.52 | 0.1639 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Distributed Systems |
| 269 | Senior Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 270 | Year at Palantir - Forward Deployed Software Engineer, Internship - Commercial | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems |
| 271 | Platform Engineer - Identity and Access Management (IAM) | Palantir | London, United Kingdom | 0.32 | 0.1639 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 272 | Systems Engineer - Business Systems | Palantir | Palo Alto, CA | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering |
| 273 | Data Scientist | Achievers | Toronto | 0.32 | 0.1639 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Data Engineering |
| 274 | Systems Engineer - Business Systems | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering |
| 275 | Forward Deployed Software Engineer - Autonomous Systems C2 | Palantir | Palo Alto, CA | 0.32 | 0.1639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems |
| 276 | Forward Deployed Software Engineer - Korea Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering |
| 277 | Forward Deployed Software Engineer - Intel | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering |
| 278 | Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 279 | Forward Deployed Software Engineer - US Government | Palantir | Honolulu, HI | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering |
| 280 | Forward Deployed Software Engineer - Japan Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering |
| 281 | Forward Deployed Reliability Engineer | Palantir | London, United Kingdom | 0.32 | 0.1639 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Distributed Systems |
| 282 | Year at Palantir - Forward Deployed Software Engineer, Internship - USG | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems |
| 283 | Full Stack Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering |
| 284 | Forward Deployed Software Engineer  - Edge Autonomous Systems | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems |
| 285 | Software Engineer - Edge | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 286 | Forward Deployed Software Engineer - Autonomous Systems C2 | Palantir | Seattle, WA | 0.32 | 0.1639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems |
| 287 | Forward Deployed Enablement Engineer - Customer Success | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 288 | Forward Deployed Enablement Engineer - Customer Success | Palantir | London, United Kingdom | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 289 | Security Engineer, Detection and Response | Notion | Dublin, Ireland | 0.3 | 0.1639 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 290 | Solutions Engineer, Enterprise, France | Notion | Paris, France | 0.32 | 0.1422 | SWE_FULLTIME | Backend Engineering, TypeScript |
| 291 | Data Migrations Engineer I | Greenhouse | Ontario | 0.2003 | 0.1422 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, ETL |
| 292 | Data Migrations Engineer I | Greenhouse | British Columbia | 0.2003 | 0.1422 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, ETL |
| 293 | Solutions Engineer, Robotics | ScaleAI | San Francisco, CA | 0.4519 | 0.1205 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Python, Java |
| 294 | Strategic Projects Lead, Generative AI | ScaleAI | India | 0.3212 | 0.1205 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | SQL, Python |
| 295 | Senior UX Design Engineer, Design Systems | Greenhouse | Ontario | 0.2967 | 0.1205 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | React, TypeScript |
| 296 | Senior Identity Security Engineer | Palantir | Washington, D.C. | 0.3553 | 0.1194 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering |
| 297 | Senior Identity Security Engineer | Palantir | Palo Alto, CA | 0.3553 | 0.1194 | BACKEND_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering |
| 298 | Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1194 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering |
| 299 | Forward Deployed Engineer - Mixed Reality | Palantir | Washington, D.C. | 0.32 | 0.1194 | SWE_FULLTIME, OTHER_FULLTIME | AI Systems |
| 300 | Forward Deployed AI Engineer | Palantir | London, United Kingdom | 0.32 | 0.1194 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems |
| 301 | Senior Software Engineers | Achievers | Toronto | 0.32 | 0.1194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 302 | Incident Management Engineer | Palantir | London, United Kingdom | 0.32 | 0.1194 | SWE_FULLTIME, OTHER_FULLTIME | Distributed Systems |
| 303 | Senior Front End Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1194 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering |
| 304 | Mixed Reality Developer | Palantir | Washington, D.C. | 0.32 | 0.1194 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 305 | Neurodivergent Fellowship | Palantir | Washington, D.C. | 0.32 | 0.1194 | SWE_FULLTIME | AI Systems |
| 306 | Backend Software Engineer - Defense | Palantir | Washington, D.C. | 0.32 | 0.1194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 307 | Backend Software Engineer - Defense | Palantir | Palo Alto, CA | 0.32 | 0.1194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 308 | Principal Product Designer | Linear | Europe | 0.24 | 0.1194 | FRONTEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 309 | Senior / Staff Product Designer | Linear | North America | 0.24 | 0.1194 | FRONTEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 310 | Software Engineer - Defense Applications | Palantir | Washington, D.C. | 0.32 | 0.0977 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React |
| 311 | Application Security Engineer | Palantir | London, United Kingdom | 0.32 | 0.075 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 312 | Software Engineer - Core Interfaces | Palantir | Palo Alto, CA | 0.32 | 0.075 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 313 | Compliance Engineer | Palantir | Washington, D.C. | 0.32 | 0.075 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 314 | Technical Account Manager, Spanish & Portuguese Speaking (São Paulo, Brazil) | Figma | São Paulo, Brazil | 0.32 | 0.075 | SWE_FULLTIME | — |
| 315 | Developer Advocate (Tokyo, Japan) | Figma | Tokyo, Japan | 0.32 | 0.075 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 316 | Compliance Engineer | Palantir | Palo Alto, CA | 0.32 | 0.075 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 317 | Application Security Engineer | Palantir | Washington, D.C. | 0.32 | 0.075 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |

## Ram Parekh (`ramparekh208@gmail.com`)

**Candidate ID:** `9502535f-33c7-452e-8fb4-bf3467eb8394`

### Subscribed pools
- `SWE_FULLTIME`
- `DATA_SCIENTIST_FULLTIME`
- `ML_ENGINEER_FULLTIME`
- `DATA_ENGINEER_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Data Engineering, Analytics Engineering, Machine Learning, Cloud Infrastructure |
| Preferred locations | — |
| Primary roles | — |
| Hard constraints | sponsorship=False, min_salary=None |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 321
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 272 |
| `BACKEND_ENGINEER_FULLTIME` | 170 |
| `ML_ENGINEER_FULLTIME` | 81 |
| `FULLSTACK_ENGINEER_FULLTIME` | 67 |
| `DEVOPS_ENGINEER_FULLTIME` | 43 |
| `DATA_ENGINEER_FULLTIME` | 39 |
| `FRONTEND_ENGINEER_FULLTIME` | 34 |
| `DATA_SCIENTIST_FULLTIME` | 31 |
| `SECURITY_ENGINEER_FULLTIME` | 16 |
| `OTHER_FULLTIME` | 11 |
| `PRODUCT_MANAGER_FULLTIME` | 5 |
| `MOBILE_ENGINEER_FULLTIME` | 3 |

### Email notification — top 4 (personalized)

#### #1 — Data Scientist, Core Data -  PhD (2026) @ Figma

- **Location:** San Francisco, CA • New York, NY (unclear)
- **Posted:** 2026-06-02T19:03:57+00:00
- **Salary:** 170000 – 178000
- **Effort:** MEDIUM
- **Opportunity score:** 0.49
- **Personal score:** 0.5687
- **Pools:** `DATA_SCIENTIST_FULLTIME`, `DATA_ENGINEER_FULLTIME`
- **Roles:** DATA_SCIENTIST, DATA_ENGINEER
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering, Research
- **Skills:** experimentation, causal inference, statistical modeling, distributed data systems
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering, SQL, Python
- **URL:** https://boards.greenhouse.io/figma/jobs/5976930004?gh_jid=5976930004

#### #2 — Software Engineer, Data Platform  @ Ramp

- **Location:** New York, NY (HQ) (unclear)
- **Posted:** 2026-03-11T04:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.32
- **Personal score:** 0.5687
- **Pools:** `DATA_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME`
- **Roles:** DATA_ENGINEER, ML_ENGINEER, SWE
- **Capabilities:** Data Engineering, Machine Learning, AI Systems, Cloud Infrastructure, Platform Engineering
- **Skills:** data platform, machine learning infrastructure, data science workflows, workflow orchestration, cloud infrastructure, sql databases
- **Match reasons:** Data Engineering, Machine Learning, Cloud Infrastructure, Python, SQL
- **URL:** https://jobs.ashbyhq.com/ramp/bca0346c-b843-4795-96df-6091f51e421b

#### #3 — Senior Applied Scientist, Credit Risk @ Ramp

- **Location:** New York, NY (HQ) (unclear)
- **Posted:** 2026-05-11T04:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.3205
- **Personal score:** 0.5375
- **Pools:** `ML_ENGINEER_FULLTIME`, `DATA_SCIENTIST_FULLTIME`, `DATA_ENGINEER_FULLTIME`
- **Roles:** ML_ENGINEER, DATA_SCIENTIST, DATA_ENGINEER
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering
- **Skills:** Machine Learning, Statistics, Causal Inference
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering, Python, SQL
- **URL:** https://jobs.ashbyhq.com/ramp/2888b101-b1da-4e53-a02e-1bb9b1b5a951

#### #4 — Staff Frontier Agents Engineer  @ ScaleAI

- **Location:** San Francisco, CA; New York, NY (unclear)
- **Posted:** 2026-05-26T23:29:02+00:00
- **Salary:** 252000 – 315000
- **Effort:** MEDIUM
- **Opportunity score:** 0.5424
- **Personal score:** 0.5062
- **Pools:** `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME`
- **Roles:** ML_ENGINEER, SWE
- **Capabilities:** AI Systems, Machine Learning, Data Engineering, Cloud Infrastructure, DevOps
- **Skills:** LLMs, RAG, Prompt Engineering, CI/CD, Vector Databases, Infrastructure as Code
- **Match reasons:** Machine Learning, Data Engineering, Cloud Infrastructure, Python
- **URL:** https://job-boards.greenhouse.io/scaleai/jobs/4694865005

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Data Scientist, Core Data -  PhD (2026) | Figma | San Francisco, CA • New York, NY | 0.49 | 0.5687 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 2 | Software Engineer, Data Platform  | Ramp | New York, NY (HQ) | 0.32 | 0.5687 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 3 | Senior Applied Scientist, Credit Risk | Ramp | New York, NY (HQ) | 0.3205 | 0.5375 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 4 | Staff Frontier Agents Engineer  | ScaleAI | San Francisco, CA; New York, NY | 0.5424 | 0.5062 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 5 | Senior Staff Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.5424 | 0.5062 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 6 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.5062 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 7 | Data Platform Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.5062 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 8 | Frontier Agent Engineering Manager, Enterprise | ScaleAI | San Francisco, CA; New York, NY | 0.513 | 0.5062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 9 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.4519 | 0.5062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 10 | Software Engineer, Robotics & Autonomous Systems | ScaleAI | San Francisco, CA | 0.4519 | 0.5062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 11 | Director, Forward Deployed Engineering | ScaleAI | London, UK | 0.3423 | 0.5062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 12 | AI Applications Engineer | Notion | San Francisco, California | 0.4267 | 0.475 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 13 | Frontier Agents Engineer | ScaleAI | London, UK | 0.5598 | 0.4688 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 14 | Software Engineer, Data Infrastructure | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 15 | Head of Finance Systems & Automation | ScaleAI | San Francisco, CA | 0.4692 | 0.4375 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 16 | Forward Deployed Engineer, GTM | Notion | San Francisco, California / New York, New York | 0.439 | 0.4375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 17 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.3381 | 0.4375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 18 | Strategic Projects Lead - Coding  | ScaleAI | San Francisco, CA; New York, NY | 0.3317 | 0.4375 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, SQL |
| 19 | Strategic Projects Lead - Coding | ScaleAI | India | 0.3212 | 0.4375 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, SQL |
| 20 | Strategic Projects Lead - Coding | ScaleAI | Mexico City, MX | 0.3203 | 0.4375 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 21 | Senior Data Scientist, Growth  | Ramp | New York, NY (HQ) | 0.32 | 0.4375 | DATA_SCIENTIST_FULLTIME | Data Engineering, Analytics Engineering, Python |
| 22 | Software Engineer, Data Infrastructure | Notion | Hyderabad, India | 0.32 | 0.4375 | DATA_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 23 | Forward Deployed Engineer, GTM, France | Notion | Paris, France | 0.319 | 0.4375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 24 | Senior Machine Learning Engineer - Model Evaluations, Public Sector | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.6662 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 25 | Field Engineer, Public Sector | ScaleAI | Colorado Springs, CO; St. Louis, MO; Washington, DC | 0.5656 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 26 | ML Systems Engineer, Robotics | ScaleAI | San Francisco, CA | 0.5423 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 27 | Research Scientist, Frontier Risk Evaluations | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.4063 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 28 | Senior AI Infrastructure Engineer, Model Serving Platform | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 29 | Senior/Staff Machine Learning Engineer, General Agents, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5203 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 30 | Software Engineer, AI Platforms | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 31 | Software Engineer, Machine Learning | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4063 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 32 | People Analytics & Operations, University Hire (Rotational Program) | Notion | San Francisco, California | 0.5151 | 0.4063 | DATA_ENGINEER_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 33 | Mission Software Engineer, Public Sector | ScaleAI | Colorado Springs, CO; Honolulu, HI; St. Louis, MO; Washington, DC | 0.4762 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 34 | Data Scientist | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.4409 | 0.4063 | DATA_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 35 | Software Engineer (Backend), Enterprise | ScaleAI | Budapest, Hungary | 0.3597 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 36 | Software Engineer, Robotics | ScaleAI | Mexico City, MX | 0.3423 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 37 | Solutions Engineer, Enterprise | ScaleAI | London, UK | 0.3423 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 38 | Product Manager / Agentic CX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.3208 | 0.4063 | PRODUCT_MANAGER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 39 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3203 | 0.4063 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 40 | Machine Learning Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3203 | 0.4063 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 41 | Machine Learning Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3203 | 0.4063 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 42 | Machine Learning Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.3203 | 0.4063 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 43 | Intermediate Software Engineer (Backend Engineering) | Achievers | Toronto | 0.32 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 44 | Software Engineer, Growth Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.4063 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 45 | Principal Marketing Analytics Manager | Greenhouse | British Columbia | 0.3087 | 0.4063 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Analytics Engineering, Data Engineering, SQL |
| 46 | Staff Software Engineer, Public Sector | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.5423 | 0.375 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, ETL |
| 47 | Staff Software Engineer, Data Platform | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.375 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure |
| 48 | Distinguished Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.375 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 49 |  Machine Learning Research Engineer, Agent Data Foundation - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.375 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering |
| 50 | Manager, Data Science - AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.375 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering |
| 51 | Senior Software Engineer, Public Sector | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.517 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, ETL |
| 52 | Software Engineer - Hosted Model Infrastructure | Palantir | New York, NY | 0.4665 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 53 | Software Engineer - Hosted Model Infrastructure | Palantir | Washington, D.C. | 0.4665 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 54 | Software Engineer - Hosted Model Infrastructure | Palantir | Palo Alto, CA | 0.4664 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 55 | Forward Deployed Engineer, GenAI  | ScaleAI | San Francisco, CA; New York, NY | 0.4506 | 0.375 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, Machine Learning |
| 56 | GenAI Strategic Projects Lead, Public Sector | ScaleAI | Washington, DC | 0.4075 | 0.375 | DATA_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering |
| 57 | Frontier Agent Engineering Manager | ScaleAI | Berlin, Germany; London, UK | 0.3283 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 58 | Production Engineer - Database Operations | Palantir | London, United Kingdom | 0.3208 | 0.375 | DATA_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, automation |
| 59 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Honolulu, HI | 0.3201 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, automation |
| 60 | Data Scientist | Achievers | Toronto | 0.32 | 0.375 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering |
| 61 | Forward Deployed Software Engineer | Palantir | Seoul, South Korea | 0.32 | 0.375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering |
| 62 | Marketing Engineer, AI Deployment | Figma | San Francisco, CA • New York, NY • United States | 0.6871 | 0.3688 | SWE_FULLTIME, OTHER_FULLTIME | Data Engineering, SQL, BigQuery |
| 63 | Data Scientist   | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.3688 | DATA_SCIENTIST_FULLTIME | Data Engineering, SQL, Python |
| 64 | Staff Infrastructure Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5423 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 65 |  Senior Software Engineer,  Full-Stack – Scale GP | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 66 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.529 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 67 | Staff Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5203 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 68 | AI Applied Scientist | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3375 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, R |
| 69 | Data Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 70 | Data Engineer, People Analytics  | Notion | San Francisco, California | 0.4848 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 71 | Data Engineer, Go-To-Market | Notion | San Francisco, California | 0.3552 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 72 | AI Strategy Consultant, Frontier Tech | ScaleAI | San Francisco, CA | 0.3203 | 0.3375 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 73 | Software Engineer, New Grad (AI) | Notion | San Francisco, California | 0.3029 | 0.3375 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, MySQL |
| 74 | Model Behavior Engineer | Notion | New York, New York / San Francisco, California | 0.2705 | 0.3375 | ML_ENGINEER_FULLTIME, PRODUCT_MANAGER_FULLTIME | Machine Learning, SQL, Python |
| 75 | Data Migrations Engineer I | Greenhouse | British Columbia | 0.2003 | 0.3375 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, Pandas |
| 76 | Data Migrations Engineer I | Greenhouse | Ontario | 0.2003 | 0.3375 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, Pandas |
| 77 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | Doha, Qatar  | 0.6907 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 78 | Senior Machine Learning Engineer, Public Sector | ScaleAI | San Francisco, CA; New York, NY; Washington, DC | 0.6662 | 0.3063 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 79 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.5747 | 0.3063 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Python |
| 80 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5535 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 81 | Technical Lead Manager, Physical AI | ScaleAI | San Francisco, CA | 0.5423 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 82 | Principal Architect | ScaleAI | Washington, DC | 0.5423 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 83 | Senior AI Infrastructure Engineer - Training Platform | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.529 | 0.3063 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 84 | Research Scientist, Safety Post Training | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.3063 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 85 | Senior Software Engineer - Internal Tools & Productivity | ScaleAI | San Francisco, CA | 0.529 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 86 | Software Engineer, Developer Experience | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 87 | Software Engineer, Distributed Systems | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 88 | Software Engineer, AI Workflows | Notion | San Francisco, California / New York, New York | 0.5025 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, MySQL, Data Modeling |
| 89 | AI Builder Intern | ScaleAI | San Francisco, CA; New York, NY | 0.4826 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, automation |
| 90 | Solutions Engineer (Clearance Required) | ScaleAI | Washington, DC | 0.4656 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 91 | Sales AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.46 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, SQL, Automation |
| 92 | Solutions Engineer, Robotics | ScaleAI | San Francisco, CA | 0.4519 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 93 | Solutions Engineer, Enterprise | ScaleAI | San Francisco, CA; New York, NY | 0.4519 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 94 | Principal Marketing Analytics Manager | Greenhouse | Anywhere in the United States | 0.394 | 0.3063 | DATA_SCIENTIST_FULLTIME | Analytics Engineering, SQL |
| 95 | Software Engineer, Enterprise | ScaleAI | London, UK | 0.3597 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 96 | Principal Marketing Analytics Manager | Greenhouse | Ontario | 0.3546 | 0.3063 | DATA_SCIENTIST_FULLTIME | Analytics Engineering, SQL |
| 97 | Applied AI Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 98 | Machine Learning Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 99 | SWE Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.3203 | 0.3063 | SWE_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 100 | SWE Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3203 | 0.3063 | SWE_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 101 | Software Engineer, Robotics | ScaleAI | Argentina; Uruguay | 0.3203 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 102 | Staff FullStack Software Engineer, (Forward Deployed), GPS | ScaleAI | Doha, Qatar  | 0.3203 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 103 | Software Engineer, Production Engineering | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 104 | Production Engineer - Database Operations | Palantir | Singapore, Singapore | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, automation |
| 105 | Security Engineer, Privacy | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.32 | 0.3063 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 106 |  Security Engineer, Cloud | Ramp | New York, NY (HQ) / Miami, FL / Remote (US) / Remote (Canada) | 0.32 | 0.3063 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 107 | Software Engineer Intern (Fall 2026) | Notion | San Francisco, California | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 108 | Senior Software Engineer (Backend Engineering) ⭐ | Achievers | Toronto | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 109 | Platform Intelligence Engineer | Palantir | New York, NY | 0.32 | 0.3063 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, data cleaning |
| 110 | Forward Deployed Software Engineer, Internship | Palantir | Paris, France | 0.2402 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 111 | Manager, Software Engineering - DevEx AI Tools | Figma | San Francisco, CA • New York, NY • United States | 0.6673 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 112 | Technical Program Manager, Data Science | Figma | San Francisco, CA • New York, NY • United States | 0.6138 | 0.275 | DATA_ENGINEER_FULLTIME, OTHER_FULLTIME | Data Engineering |
| 113 | Director, Enterprise Machine Learning & Research | ScaleAI | San Francisco, CA; New York, NY | 0.5633 | 0.275 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning |
| 114 | Staff Machine Learning Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.275 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning |
| 115 | Machine Learning Research Engineer, Agents - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.275 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning |
| 116 | Tech Lead Manager- MLRE, ML Systems | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 117 | Machine Learning Systems Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5423 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 118 | Research Scientist, AI Controls and Monitoring | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.275 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Anomaly Detection |
| 119 | Research Scientist, Agent Robustness | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.275 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 120 | Security Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.521 | 0.275 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 121 | Machine Learning Research Scientist, Post-Training | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.275 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning |
| 122 | Manager, Machine Learning Research Scientist, GenAI | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.275 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 123 | Senior / Staff Machine Learning Research Scientist, Agents | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.275 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning |
| 124 | Machine Learning Research Scientist, Reasoning | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.5203 | 0.275 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 125 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.5201 | 0.275 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning |
| 126 | Manager, Software Engineering - Observability | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Anomaly detection |
| 127 | Manager, Software Engineering - Search & Recommendations | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, recommendation systems |
| 128 | Software Engineer, Production Engineering | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 129 | Engineering Manager, Context (Agentic Search) | Notion | San Francisco, California | 0.52 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 130 | Manager, Software Engineering - AI Product  | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 131 | Technical Program Manager, AI Performance | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 132 | Product Designer, AI Models | Figma | San Francisco, CA • New York, NY • United States | 0.4933 | 0.275 | ML_ENGINEER_FULLTIME | Machine Learning |
| 133 | Software Engineer, Infrastructure  | Notion | Hyderabad, India | 0.4732 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 134 | Machine Learning Research Engineer, GenAI Applied ML | ScaleAI | San Francisco, CA; New York, NY | 0.4724 | 0.275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 135 | ML Research Engineer, ML Systems | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.4504 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 136 | Software Engineer, ARC Team | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.4447 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 137 | Software Engineer, Frontier AI Infrastructure | ScaleAI | San Francisco, CA; St. Louis, MO; New York, NY; Washington, DC | 0.4447 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 138 | Intermediate Software Engineer | Achievers | Canada | 0.429 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 139 | GTM Systems Analyst | ScaleAI | San Francisco, CA | 0.4017 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 140 | Finance Systems & Automations Manager | ScaleAI | San Francisco, CA | 0.3994 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 141 | Technical Consultant / Strategic | Ramp | New York, NY (HQ) / Miami, FL / San Francisco, CA / Remote (US) / Remote (Canada) | 0.3829 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 142 | Staff Software Engineer | Achievers | Canada | 0.3618 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 143 | Forward Deployed Software Engineer, Internship - AUS Government | Palantir | Sydney, Australia | 0.3612 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 144 | AI Applications Ops Lead, GPS | ScaleAI | Doha, Qatar; London, UK | 0.3423 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 145 | Staff Technical Product Manager | ScaleAI | London, UK; New York, NY; San Francisco, CA | 0.3423 | 0.275 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | Machine Learning |
| 146 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | Washington, D.C. | 0.3202 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 147 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | New York, NY | 0.3202 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 148 | Sr Software Engineer - Core Backend & Platform Engineering | Basis | United States | 0.3201 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 149 | Forward Deployed Software Engineer - AUS Government | Palantir | Canberra, Australia | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 150 | Senior / Staff Product Engineer, AI | Linear | North America | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 151 | Forward Deployed Engineer - Mixed Reality | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, OTHER_FULLTIME | Machine Learning |
| 152 | Software Engineer - Apollo Systems | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 153 | Year at Palantir - Software Engineer, Internship | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 154 | Software Engineer - Apollo Systems | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 155 | Software Engineer - Apollo Platform | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 156 | Software Engineer - Apollo Platform | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 157 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Automation |
| 158 | Senior Software Engineer, Substrate | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 159 | Senior Software Engineer, Substrate | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 160 | Edge Infrastructure Engineer | Palantir | Warsaw, Poland | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 161 | Edge Infrastructure Engineer | Palantir | Paris, France | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 162 | Senior Software Engineer, Substrate | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 163 | Software Engineer - Mission Manager | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 164 | Forward Deployed Software Engineer - Intel | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 165 | Forward Deployed Software Engineer - Korea Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 166 | Forward Deployed Software Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 167 | Systems Engineer - Business Systems | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 168 | Forward Deployed Software Engineer - Tactical Edge | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 169 | Forward Deployed Software Engineer | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 170 | Forward Deployed Software Engineer, Internship - France | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 171 | Edge Infrastructure Engineer | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 172 | Systems Engineer - Business Systems | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 173 | Forward Deployed Software Engineer | Palantir | Stockholm, Sweden | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 174 | Forward Deployed Software Engineer | Palantir | Vilnius, Lithuania | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 175 | Forward Deployed AI Engineer | Palantir | London, United Kingdom | 0.32 | 0.275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 176 | Systems Engineer - Business Systems | Palantir | Palo Alto, CA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 177 | DevOps Engineer | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 178 | DevOps Engineer | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 179 | Senior / Staff Product Engineer | Linear | Europe | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure |
| 180 | Senior / Staff Product Engineer | Linear | North America | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure |
| 181 | Integrations Expert / Customer Experience | Ramp | New York, NY (HQ) / Denver, CO / Remote (US) / San Francisco, CA / Miami, FL | 0.32 | 0.275 | DATA_ENGINEER_FULLTIME, OTHER_FULLTIME | Data Engineering |
| 182 | Software Engineer, AI Product (London, United Kingdom) | Figma | London, England | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning |
| 183 | Senior Software Engineer, Network Infrastructure | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 184 | Senior Software Engineer, Network Infrastructure | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 185 | Forward Deployed Infrastructure Engineer - US Government | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Automation |
| 186 | Forward Deployed AI Engineer | Palantir | New York, NY | 0.32 | 0.275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 187 | Forward Deployed Infrastructure Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Automation |
| 188 | Forward Deployed Software Engineer | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 189 | Forward Deployed Software Engineer - US Government | Palantir | Honolulu, HI | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 190 | Neurodivergent Fellowship | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 191 | Forward Deployed Software Engineer - Japan Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 192 | Forward Deployed Software Engineer, Internship - Poland | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 193 | Forward Deployed Software Engineer | Palantir | Tel Aviv, Israel | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 194 | Forward Deployed Software Engineer - US Government | Palantir | San Diego, CA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 195 | Forward Deployed Software Engineer - US Government | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 196 | Forward Deployed Software Engineer, Internship - US Government | Palantir | Honolulu, HI | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 197 | Forward Deployed Software Engineer - AUS Government | Palantir | Sydney, Australia | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 198 | Forward Deployed Software Engineer - Warp Speed | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 199 | Forward Deployed Software Engineer - US Government | Palantir | Fayetteville, NC | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering |
| 200 | Forward Deployed Software Engineer | Palantir | Amsterdam, Netherlands | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 201 | Software Engineer - Developer Productivity | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 202 | Senior Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 203 | Senior Backend Software Engineer - Infrastructure | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 204 | Forward Deployed Reliability Engineer | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 205 | Backend Software Engineer - Infrastructure, Foundations | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 206 | Forward Deployed Software Engineer | Palantir | Dubai, United Arab Emirates | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 207 | Forward Deployed Software Engineer | Palantir | Abu Dhabi, United Arab Emirates | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 208 | Product Reliability Engineer - Defense | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 209 | Software Engineer - Environment Platform | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 210 | Senior Software Engineer, Network Infrastructure | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 211 | Forward Deployed Software Engineer  - Edge Autonomous Systems | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 212 | Software Engineer - Environment Platform | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 213 | Software Engineer - Mission Manager | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 214 | Systems Engineer - Business Systems | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 215 | Systems Engineer - Business Systems | Palantir | Denver, CO | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 216 | Year at Palantir - Forward Deployed Software Engineer, Internship - USG | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 217 | Year at Palantir - Forward Deployed Software Engineer, Internship - Commercial | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 218 | Software Engineer - Apollo Platform | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 219 | Forward Deployed Software Engineer - Autonomous Systems C2 | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning |
| 220 | Forward Deployed Software Engineer - Japan Government | Palantir | Tokyo, Japan | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 221 | Forward Deployed Software Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering |
| 222 | Product Reliability Engineer - Defense | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 223 | Software Engineer - Mission Manager | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 224 | Senior Software Engineer, Substrate | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 225 | Site Reliability Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, automation |
| 226 | Security Engineer, Detection and Response | Notion | Dublin, Ireland | 0.3 | 0.275 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure |
| 227 | STEM Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.2403 | 0.275 | DATA_SCIENTIST_FULLTIME, OTHER_FULLTIME | Machine Learning |
| 228 | Finance Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.2403 | 0.275 | DATA_SCIENTIST_FULLTIME, OTHER_FULLTIME | Machine Learning |
| 229 | STEM Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.2403 | 0.275 | DATA_SCIENTIST_FULLTIME, OTHER_FULLTIME | Machine Learning |
| 230 | Product Operations Manager | Notion | San Francisco, California / New York, New York | 0.3867 | 0.2375 | SWE_FULLTIME | Python, MySQL |
| 231 | Strategic Projects Lead, Generative AI | ScaleAI | India | 0.3212 | 0.2375 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | SQL, Python |
| 232 | Solutions Engineer, EMEA | Notion | Dublin, Ireland | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Python, Data Modeling |
| 233 | Enterprise Technical Support Specialist, Korea | Notion | Seoul, South Korea | 0.32 | 0.2375 | SWE_FULLTIME | Python, MySQL |
| 234 | Mobile Engineer, iOS | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (Canada) / Remote (US) | 0.32 | 0.2375 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 235 | AI Operations Specialist / Agentic Workflows | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.2375 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | Python, SQL, automation |
| 236 | Forward Deployed Engineer, GTM - Korea | Notion | Seoul, South Korea | 0.32 | 0.2375 | SWE_FULLTIME | SQL, Python |
| 237 | Enterprise Technical Support Specialist - NYC | Notion | New York, New York | 0.3076 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, MySQL |
| 238 | Software Engineer, New Grad | Notion | San Francisco, California | 0.3029 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, MySQL |
| 239 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5536 | 0.2062 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Python, Data Modeling |
| 240 | Senior Software Engineer, GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.529 | 0.2062 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 241 | Software Engineer, Full Stack | Figma | San Francisco, CA • New York, NY • United States | 0.5201 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 242 | Software Engineer, C++ | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 243 | Technical Program Manager | Ramp | New York, NY (HQ) | 0.3268 | 0.2062 | OTHER_FULLTIME, SWE_FULLTIME | Python |
| 244 | Software Engineer, Stablecoin | Ramp | New York, NY (HQ) / San Francisco, CA | 0.3208 | 0.2062 | SWE_FULLTIME | Python |
| 245 | Senior Software Engineer / GTM Platform, Backend | Ramp | New York, NY (HQ) | 0.3208 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 246 | SWE Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3203 | 0.2062 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Python |
| 247 | Software Engineer, Fraud & Identity | Ramp | New York, NY (HQ) | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 248 | Software Engineer, Argentina | Ramp | Remote (Buenos Aires, Argentina) | 0.32 | 0.2062 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 249 | Software Engineer, AI DevX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, automation |
| 250 | Software Engineer, AI Forward Deployed | Ramp | San Francisco, CA / New York, NY (HQ) | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 251 | Software Engineer, Core Product | Ramp | New York, NY (HQ) | 0.32 | 0.2062 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 252 | Security Engineer, Product | Ramp | New York, NY (HQ) | 0.32 | 0.2062 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 253 | Backend Engineer, Ops | Ramp | New York, NY (HQ) | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 254 | Software Engineer, Accounting | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.2062 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 255 | Software Engineer, Engineering Platform | Ramp | New York, NY (HQ) | 0.32 | 0.2062 | SWE_FULLTIME | Python |
| 256 | Manager, Software Engineering - Growth Platform  | Figma | San Francisco, CA • New York, NY • United States | 0.6674 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 257 | Engineering Manager, AgentOps | ScaleAI | San Francisco, CA; New York, NY | 0.6626 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 258 | Software Engineer, Web Infrastructure | Notion | San Francisco, California / New York, New York | 0.5486 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 259 | Staff Software Engineer, Full-Stack - Enterprise Gen AI | ScaleAI | New York, NY; San Francisco, CA | 0.5424 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 260 | Director of Technology & Systems | ScaleAI | San Francisco, CA | 0.5423 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 261 | Manager, Software Engineering - Interaction Design | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 262 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 263 | Manager, Software Engineering - Billing | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 264 | Software Engineer, Code Platform | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 265 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 266 | Software Engineer, Growth & Monetization | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.175 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 267 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 268 | Software Engineer, Trust | Notion | San Francisco, California / New York, New York | 0.5011 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 269 | Partner Solutions Engineer | Notion | New York, New York / San Francisco, California | 0.501 | 0.175 | SWE_FULLTIME | — |
| 270 | Engineering Manager, Mobile AI | Notion | New York, New York | 0.4967 | 0.175 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 271 | Solutions Consultant | Figma | San Francisco, CA • New York, NY • United States | 0.4712 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 272 | Manager, Web Experience | ScaleAI | San Francisco, CA; New York, NY | 0.4056 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 273 | Senior Identity Security Engineer | Palantir | Washington, D.C. | 0.3553 | 0.175 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 274 | Senior Identity Security Engineer | Palantir | New York, NY | 0.3553 | 0.175 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 275 | Software Engineer, Mobile AI, iOS | Notion | New York, New York | 0.3201 | 0.175 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 276 | Software Engineer - Core Interfaces | Palantir | Palo Alto, CA | 0.32 | 0.175 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 277 | Software Engineer - Defense Applications | Palantir | Washington, D.C. | 0.32 | 0.175 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 278 | Application Security Engineer | Palantir | London, United Kingdom | 0.32 | 0.175 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 279 | Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.175 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 280 | Forward Deployed Enablement Engineer - Customer Success | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME | — |
| 281 | Software Engineer - Frontend Developer Productivity | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 282 | Year at Palantir - Forward Deployed Software Engineer, Internship - Commercial | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 283 | Senior Front End Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 284 | Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 285 | Senior Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 286 | Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 287 | Backend Software Engineer - Infrastructure | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 288 | Full Stack Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 289 | Forward Deployed Software Engineer - Autonomous Systems C2 | Palantir | Palo Alto, CA | 0.32 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 290 | Compliance Engineer | Palantir | Washington, D.C. | 0.32 | 0.175 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 291 | Senior Software Engineer / GTM Platform, Frontend | Ramp | New York, NY (HQ) | 0.32 | 0.175 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 292 | Senior / Staff Fullstack Engineer | Linear | North America | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 293 | Senior / Staff Fullstack Engineer | Linear | Europe | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 294 | Software Engineer, Product Growth | Ramp | New York, NY (HQ) / San Francisco, CA | 0.32 | 0.175 | SWE_FULLTIME | ETL |
| 295 | Solutions Engineer, Enterprise, France | Notion | Paris, France | 0.32 | 0.175 | SWE_FULLTIME | — |
| 296 | Sr Software Engineer - Basis Platform / DSP | Basis | United States | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 297 | Senior Software Engineers | Achievers | Toronto | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 298 | Software Engineer, Developer Experience | Notion | Hyderabad, India | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 299 | Technical Account Manager, Spanish & Portuguese Speaking (São Paulo, Brazil) | Figma | São Paulo, Brazil | 0.32 | 0.175 | SWE_FULLTIME | — |
| 300 | Developer Advocate (Tokyo, Japan) | Figma | Tokyo, Japan | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 301 | Compliance Engineer | Palantir | New York, NY | 0.32 | 0.175 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 302 | Compliance Engineer | Palantir | Palo Alto, CA | 0.32 | 0.175 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 303 | Forward Deployed Reliability Engineer | Palantir | London, United Kingdom | 0.32 | 0.175 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 304 | Incident Management Engineer | Palantir | London, United Kingdom | 0.32 | 0.175 | SWE_FULLTIME, OTHER_FULLTIME | — |
| 305 | Senior Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 306 | Incident Management Engineer | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 307 | Year at Palantir - Forward Deployed Software Engineer, Internship - USG | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 308 | Full Stack Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 309 | Senior Front End Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 310 | Mixed Reality Developer | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 311 | Neurodivergent Fellowship | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME | — |
| 312 | Backend Software Engineer - Defense | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 313 | Senior Software Engineer - Observability | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 314 | Software Engineer - Edge | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 315 | Application Security Engineer | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 316 | Backend Software Engineer - Defense | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 317 | Application Security Engineer | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 318 | Backend Software Engineer - Defense | Palantir | Palo Alto, CA | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 319 | Forward Deployed Enablement Engineer - Customer Success | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 320 | Forward Deployed Enablement Engineer - Customer Success | Palantir | London, United Kingdom | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 321 | Senior UX Design Engineer, Design Systems | Greenhouse | Ontario | 0.2967 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
