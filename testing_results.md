# User Recommendation Results

Generated 2026-06-12 17:01 UTC after v5 domain taxonomy enrichment (6,378 recommendation-eligible active jobs, 6,397 active normalized rows, 8,576 archived identities, 96 active companies; domain filter enabled, Tier 1+2 business pools, gemini-3.1-flash-lite).

Active layer (`normalized_jobs`) retains jobs ≤7 days; long-lived history lives in `job_archive`.

Pools synced via `PATCH /subscriptions` from profile preferences or existing subscriptions.

**Ranking modes:**
- **Dashboard** — sorted by global `opportunity_score` (freshness + comp + effort)
- **Personalized / Email** — sorted by profile match score (capabilities 40%, skills 25%, location 20%, comp 15%, seniority soft penalty); ties broken by `posted_at` then `opportunity_score`
- **Email retrieval** — only jobs posted within 60 days, not previously emailed; skips send when fewer than 3 eligible jobs (daily cadence default)

Full machine-readable export: [`exports/user_recommendations.json`](exports/user_recommendations.json)

## Run summary

| User | Matching jobs | Personal score range | Unique score tiers | Subscribed pools |
|------|---------------|----------------------|--------------------|------------------|
| Ram Parekh | 690 | 0.063–0.5488 | 68 | `SWE_FULLTIME`, `DATA_SCIENTIST_FULLTIME`, `ML_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME` |
| Yatharth Mogra | 662 | 0.063–0.4992 | 166 | `DATA_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME` |

---

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
| Hard constraints | sponsorship=False, min_salary=None, target_seniority=— |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 690
- **Notification-eligible jobs (≤60d, not yet emailed):** 500
- **Personal score range:** 0.063 – 0.5488 (68 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 549 |
| `BACKEND_ENGINEER_FULLTIME` | 346 |
| `ML_ENGINEER_FULLTIME` | 144 |
| `DATA_ENGINEER_FULLTIME` | 66 |
| `FULLSTACK_ENGINEER_FULLTIME` | 66 |
| `DEVOPS_ENGINEER_FULLTIME` | 63 |
| `FRONTEND_ENGINEER_FULLTIME` | 48 |
| `DATA_SCIENTIST_FULLTIME` | 37 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 27 |
| `SECURITY_ENGINEER_FULLTIME` | 15 |
| `MOBILE_ENGINEER_FULLTIME` | 12 |
| `DATA_ANALYST_FULLTIME` | 6 |
| `SUPPORT_ENGINEER_FULLTIME` | 4 |
| `PRODUCT_MANAGER_FULLTIME` | 3 |
| `RESEARCH_SCIENTIST_FULLTIME` | 2 |

### Email notification — top 4 (personalized)

#### #1 — Software Engineer, Machine Learning @ Figma

- **Location:** San Francisco, CA • New York, NY • United States (unclear)
- **Posted:** 2026-04-15T19:32:40+00:00
- **Salary:** 153000 – 376000
- **Effort:** MEDIUM
- **Opportunity score:** 0.52
- **Personal score:** 0.5563
- **Pools:** `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME`
- **Roles:** ML_ENGINEER, SWE
- **Capabilities:** Machine Learning, Data Engineering, Cloud Infrastructure
- **Skills:** applied machine learning, search relevance
- **Match reasons:** Machine Learning, Data Engineering, Cloud Infrastructure, Python
- **URL:** https://boards.greenhouse.io/figma/jobs/5551532004?gh_jid=5551532004

#### #2 — Data Scientist @ Ramp

- **Location:** New York, NY (HQ) | San Francisco, CA | Remote (US) (unclear)
- **Posted:** —
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.52
- **Personal score:** 0.5488
- **Pools:** `DATA_SCIENTIST_FULLTIME`
- **Roles:** DATA_SCIENTIST
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering
- **Skills:** predictive modeling, statistical analysis
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering, Python, SQL
- **URL:** https://jobs.ashbyhq.com/ramp/e577622f-6657-4e53-8941-b3a774b04448

#### #3 — Growth Intelligence Engineer (Ads & Revenue) @ NewsBreak

- **Location:** Mountain View, California, United States (unclear)
- **Posted:** 2026-05-26T23:23:17+00:00
- **Salary:** 145000 – 185000
- **Effort:** MEDIUM
- **Opportunity score:** 0.3656
- **Personal score:** 0.5188
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME`, `DATA_SCIENTIST_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, DATA_ENGINEER, DATA_SCIENTIST
- **Capabilities:** Backend Engineering, Data Engineering, Machine Learning
- **Skills:** A/B testing, experimental design, recommendation systems, ad-tech
- **Match reasons:** Data Engineering, Machine Learning, SQL, Python, BigQuery
- **URL:** https://job-boards.greenhouse.io/newsbreak/jobs/4684499006

#### #4 — Cybersecurity Engineers @ American Express

- **Location:** Phoenix, AZ, United States (unclear)
- **Posted:** 2026-06-10T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5382
- **Personal score:** 0.4875
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `SECURITY_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, SECURITY_ENGINEER
- **Capabilities:** Security Engineering, Backend Engineering, Cloud Infrastructure, Data Engineering
- **Skills:** Cybersecurity, Data Profiling
- **Match reasons:** Cloud Infrastructure, Data Engineering, Python, SQL
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26009230/details

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Data Scientist | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.52 | 0.5488 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 2 | Data Scientist, Core Data -  PhD (2026) | Figma | San Francisco, CA • New York, NY | 0.4137 | 0.5188 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, SQL |
| 3 | Growth Intelligence Engineer (Ads & Revenue) | NewsBreak | Mountain View, California, United States | 0.3656 | 0.5188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 4 |  Research Data Scientist 1 | iSpot | Bellevue, WA | 0.2365 | 0.5188 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 5 | Data Scientist   | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.5188 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 6 | Cybersecurity Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.4875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 7 | Technical Instructor (AWS Machine Learning) | Per Scholas | United States | 0.2942 | 0.4875 | ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 8 | Software Engineer, AI Platforms | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4875 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 9 | Machine Learning Scientist (Financial Scoring) | Lendbuzz | Boston, MA | 0.32 | 0.4875 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 10 | Data Engineering Instructor | Per Scholas | United States | 0.32 | 0.4875 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 11 | Data Engineer | Base Power Company | Austin, TX | 0.52 | 0.4875 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 12 | Software Engineer II | American Express | Gurugram, HR, India | 0.5382 | 0.4675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 13 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.755 | 0.4563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 14 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.6346 | 0.4563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 15 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.4563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 16 | Software Engineer - Hosted Model Infrastructure | Palantir | Washington, D.C. | 0.3691 | 0.4563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 17 | Software Engineer - Hosted Model Infrastructure | Palantir | New York, NY | 0.3691 | 0.4563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 18 | Software Engineer - Hosted Model Infrastructure | Palantir | Palo Alto, CA | 0.3691 | 0.4563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 19 |  Machine Learning Research Engineer, Agent Data Foundation - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.4563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 20 | Forward Deployed Engineer, GenAI  | ScaleAI | San Francisco, CA; New York, NY | 0.4357 | 0.4563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 21 | Full-Stack Engineer, AI Data Platform | Labelbox | San Francisco Bay Area | 0.3608 | 0.4563 | FULLSTACK_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 22 | Machine Learning Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3201 | 0.4563 | ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 23 | Software Engineer, AI Forward Deployed | Ramp | San Francisco, CA / New York, NY (HQ) | 0.52 | 0.4563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 24 | ML Platform Engineer | Foxglove | San Francisco, CA | 0.52 | 0.4563 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 25 | Credit Risk Expert (Experto/a en Riesgo de Credito)  | Clara | Latin America  | 0.3318 | 0.4488 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 26 | Scientist - Ensemble Structural Informatics | Astera Institute | Emeryville HQ | 0.52 | 0.4488 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 27 | Scientist - Ensemble Structural Informatics | Astera Institute | Emeryville HQ | 0.52 | 0.4488 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 28 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3952 | 0.4363 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 29 | Quantum Calibration Engineer, Quantum Computing Services | QuEra Computing | Boston, MA, USA | 0.3295 | 0.4188 | ML_ENGINEER_FULLTIME | Machine Learning, Python, NumPy |
| 30 | Junior Data Scientist | Clara | Latin America  | 0.3287 | 0.4175 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 31 | Bioinformatics Data Engineer | GenBio AI | Abu Dhabi | 0.32 | 0.4175 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 32 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.3987 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 33 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.326 | 0.3987 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 34 | Data Scientist II | Honeywell | Pune City, Maharashtra, India | 0.3247 | 0.3987 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 35 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.3987 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 36 | Support AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.7152 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 37 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.5382 | 0.3875 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 38 | Cybersecurity AI_ML Engineer | GM Financial | Irving, TX, United States / US - Arlington AOC I, TX | 0.3452 | 0.3875 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, pandas |
| 39 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5141 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 40 | Infrastructure Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 41 | Software Engineer II, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3318 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 42 | AI Strategy Consultant, Frontier Tech | ScaleAI | San Francisco, CA | 0.3201 | 0.3875 | ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 43 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | New York, NY | 0.3201 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 44 | Forward Deployed Engineer | Labelbox | San Francisco Bay Area | 0.3676 | 0.3875 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, SQL |
| 45 | Instructional Assistant (Data Engineer) (3-6 month contract) | Per Scholas | Orlando, Florida, United States | 0.32 | 0.3875 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, SQL |
| 46 | Forward Deployed Software Engineer - US Government | Palantir | Fayetteville, NC | 0.32 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 47 | Forward Deployed Enablement Engineer - Customer Success | Palantir | Washington, D.C. | 0.32 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 48 | Forward Deployed Software Engineer - Warp Speed | Palantir | New York, NY | 0.32 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 49 | Forward Deployed Software Engineer - Korea Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 50 | Forward Deployed AI Engineer | Palantir | New York, NY | 0.32 | 0.3875 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, SQL |
| 51 | Backend Software Engineer - Infrastructure, Foundations | Palantir | New York, NY | 0.32 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 52 | Forward Deployed Software Engineer - US Government | Palantir | New York, NY | 0.32 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 53 | Software Engineer, Credit | Ramp | New York, NY (HQ) | 0.52 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 54 | Data Engineer, People Analytics  | Notion | San Francisco, California | 0.52 | 0.3875 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 55 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4797 | 0.3863 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 56 | Software Engineer, Robotics | ScaleAI | Mexico City, MX | 0.3274 | 0.3863 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 57 | Data Scientist, Marketing | Figma | San Francisco, CA • New York, NY • United States | 0.8543 | 0.3713 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 58 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4916 | 0.3675 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 59 | Associate-Digital Product Management (SQL, Hadoop, Hive) | American Express | Gurugram, HR, India | 0.4262 | 0.3675 | PRODUCT_MANAGER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 60 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.3675 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 61 | Chemical Engr II | Honeywell | Gurugram, Haryana, India | 0.3296 | 0.3675 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 62 | Strategic Projects Lead - Coding | ScaleAI | India | 0.3204 | 0.3675 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 63 | Data Scientist | Achievers | Toronto | 0.32 | 0.3675 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 64 | Software Engineer I, Service Network - Slack | Slack (Salesforce) | Washington - Seattle | 0.5446 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 65 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4916 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 66 | Instructional Assistant (Cloud Systems Engineering) | Per Scholas | United States; United States | 0.3915 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 67 | Software Engineer II, Full Stack - Global Servicing Technology | American Express | Sunrise, FL, United States | 0.3717 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 68 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.3717 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 69 | Machine Learning Engineer - LLM, AI & Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 70 | Machine Learning Engineer, Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 71 | AI Engineer III - Agentic AI | American Express | New York, NY, United States / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus | 0.3322 | 0.3563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 72 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2159 | 0.3563 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 73 | Machine Learning Systems Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 74 | Machine Learning Research Engineer, Agents - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5272 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 75 | Software Engineer, Robotics & Autonomous Systems | ScaleAI | San Francisco, CA | 0.437 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 76 | Advanced Software Engineer | Honeywell | Acton, MA, United States | 0.3428 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 77 | Machine Learning Engineer | True Anomaly | Denver, CO or Long Beach, CA | 0.2967 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python, Anomaly Detection |
| 78 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2087 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 79 | Research Scientist I/II, AI for Process Engineering | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 80 | Machine Learning Scientist I/II, Scientific Reasoning | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.3563 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 81 | Research Engineer, Frontier Capabilities | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4995 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 82 | Sales AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.4594 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, SQL, automation |
| 83 | Software Engineer, Full Stack | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 84 | Forward Deployed Engineer, RL Environments | Labelbox | San Francisco Bay Area | 0.3676 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 85 | Forward Deployed Software Engineer - Tactical Edge | Palantir | Washington, D.C. | 0.32 | 0.3563 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 86 | Platform Intelligence Engineer | Palantir | New York, NY | 0.32 | 0.3563 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python |
| 87 | Forward Deployed Engineer - Mixed Reality | Palantir | Washington, D.C. | 0.32 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 88 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.3563 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 89 | Forward Deployed Infrastructure Engineer - US Government | Palantir | New York, NY | 0.32 | 0.3563 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 90 | Software Engineer - Developer Productivity | Palantir | New York, NY | 0.32 | 0.3563 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 91 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.3563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 92 | Algorithms Engineer | Base Power Company | Austin, TX | 0.52 | 0.3563 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 93 | Model Behavior Engineer | Notion | New York, New York / San Francisco, California | 0.52 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 94 | Applied AI Engineer | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 95 | AI Applications Engineer | Notion | San Francisco, California | 0.52 | 0.3563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 96 | Software Engineer, AI Workflows | Notion | San Francisco, California / New York, New York | 0.52 | 0.3563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 97 | Applied ML Engineer | Foxglove | San Francisco, CA | 0.52 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 98 | Infrastructure Engineer - Early Career | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, automation |
| 99 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.52 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 100 | Software Engineer, Web Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 101 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.52 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 102 | Sr Advanced AI Platform Engineer | Honeywell | Atlanta, GA, United States | 0.3218 | 0.3525 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 103 | Analyst - Data Science | American Express | Singapore, Singapore | 0.2418 | 0.3488 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 104 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.5384 | 0.3362 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 105 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.3362 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 106 | Cloud Developer II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.3362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, SQL |
| 107 | Production Engineer - Database Operations | Palantir | London, United Kingdom | 0.3203 | 0.3362 | DEVOPS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 108 | Machine Learning Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.3362 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 109 | Intermediate Software Engineer (Backend Engineering) | Achievers | Toronto | 0.4 | 0.3362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 110 | Sr Advanced Cloud Developer | Honeywell | Mason, OH, United States | 0.3204 | 0.3337 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 111 | Software Engineer, ML Infra | NewsBreak | Mountain View, California, United States | 0.4295 | 0.3337 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 112 | Data Platform Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3337 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 113 | Software Engineer, Platform | ScaleAI | San Francisco, CA; New York, NY | 0.7099 | 0.325 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 114 | Experienced Software Configuration Management Specialist | Boeing | USA - Tukwila, WA | 0.3942 | 0.325 | SWE_FULLTIME | Cloud Infrastructure |
| 115 | Software Engineer II | Honeywell | Duluth, GA, United States | 0.3857 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 116 | Advanced Software Engineer | Honeywell | Atlanta, GA, United States | 0.3223 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 117 | Software Engineer III - Java - Web Search Team | American Express | Phoenix, AZ, United States | 0.3211 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 118 | Software Engineer - Environment Platform | Palantir | Seattle, WA | 0.32 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 119 | High Performance Computing (HPC) Engineer | GenBio AI | Palo Alto, CA | 0.32 | 0.325 | SWE_FULLTIME | Cloud Infrastructure |
| 120 | Software Engineer - Apollo Platform | Palantir | New York, NY | 0.32 | 0.325 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 121 | Software Engineer - Apollo Platform | Palantir | Seattle, WA | 0.32 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 122 | Software Engineer, Engineering Platform | Ramp | New York, NY (HQ) | 0.52 | 0.325 | SWE_FULLTIME | Cloud Infrastructure |
| 123 | Software Engineer, Data Platform  | Ramp | New York, NY (HQ) | 0.52 | 0.325 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering |
| 124 | Market Infrastructure Engineer | Base Power Company | Austin, TX | 0.52 | 0.325 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 125 | Workday Integrations & Data Architect | EarnIn | Remote, Mexico | 0.36 | 0.3175 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 126 | Analytics Engineer | Podium | Lehi, Utah | 0.3202 | 0.3175 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, SQL, Python |
| 127 | Data Engineer | Lendbuzz | Tel Aviv | 0.3201 | 0.3175 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 128 | Forward Deployed Software Engineer - Japan Government | Palantir | Tokyo, Japan | 0.32 | 0.3175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 129 | Forward Deployed Software Engineer | Palantir | Dubai, United Arab Emirates | 0.32 | 0.3175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 130 | Forward Deployed Software Engineer | Palantir | Seoul, South Korea | 0.32 | 0.3175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 131 | Forward Deployed Software Engineer | Palantir | Stockholm, Sweden | 0.32 | 0.3175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 132 | Forward Deployed Software Engineer | Palantir | Amsterdam, Netherlands | 0.32 | 0.3175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 133 | Forward Deployed Software Engineer | Palantir | Tel Aviv, Israel | 0.32 | 0.3175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 134 | Senior Data Scientist, Growth  | Ramp | New York, NY (HQ) | 0.52 | 0.3113 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 135 | Senior, ML Engineer - Auto Tagger | Torc Robotics | Ann Arbor, MI, Remote - US | 0.417 | 0.3105 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 136 | Frontier Agents Engineer | ScaleAI | London, UK | 0.4003 | 0.2988 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Pandas |
| 137 | Data Scientist I | Honeywell | Bengaluru, Karnataka, India | 0.352 | 0.2988 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, R |
| 138 | Senior Software Developer - Data Engineering-2 | Boeing | USA - Seattle, WA | 0.4782 | 0.2925 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 139 | Senior Data Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.2925 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 140 | Sr. AI Data Analyst-Agentic Systems & GenAI | GM Financial | Irving, TX, United States / US - Burnett, TX | 0.3452 | 0.2925 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 141 | Senior AI Engineer I | BillionToOne | Menlo Park, CA | 0.4123 | 0.2925 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 142 | Senior Software Engineer, Applied AI | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4385 | 0.2925 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 143 | Software Engineer, Data Infrastructure | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2925 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 144 | Senior Applied Scientist, Credit Risk | Ramp | New York, NY (HQ) | 0.52 | 0.2925 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 145 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5635 | 0.2918 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 146 | Senior, ML Engineer - ML Ops Framework  | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5181 | 0.2918 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 147 | Senior, ML Engineer - ML Ops Framework | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5181 | 0.2918 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 148 | Business Systems Applications Developer | CesiumAstro | Austin, TX | 0.32 | 0.2875 | SWE_FULLTIME | SQL, Python |
| 149 | Forward Deployed Software Engineer - US Government | Palantir | San Diego, CA | 0.32 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 150 | Forward Deployed Software Engineer - Japan Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 151 | Forward Deployed Software Engineer - Intel | Palantir | Washington, D.C. | 0.32 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 152 | Forward Deployed Software Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 153 | Forward Deployed Software Engineer | Palantir | New York, NY | 0.32 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 154 | Forward Deployed Engineer, GTM | Notion | San Francisco, California / New York, New York | 0.52 | 0.2875 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 155 | Software Engineer, Backend | Base Power Company | Austin, TX | 0.52 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 156 | Backend Engineer, Ops | Ramp | New York, NY (HQ) | 0.52 | 0.2875 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 157 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.6725 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 158 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.6294 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 159 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5851 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 160 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5249 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 161 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.5413 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 162 | Application Engr II | Honeywell | Tianjin, China | 0.4915 | 0.2863 | ML_ENGINEER_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Machine Learning, Python |
| 163 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4981 | 0.2863 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 164 | Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 165 | Consultant | Appian | Seville, Spain | 0.359 | 0.2863 | SWE_FULLTIME | Machine Learning, SQL |
| 166 | Software Engineer (Backend), Enterprise | ScaleAI | Budapest, Hungary | 0.3332 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 167 | Software Engineer I - Metrics for Release Implementation | Torc Robotics | Remote, US | 0.2905 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 168 | Software Engr II | Honeywell | Shanghai, China | 0.3203 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 169 | HPC engineer | Honeywell | Bucuresti, Romania | 0.3203 | 0.2863 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 170 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Honolulu, HI | 0.32 | 0.2863 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 171 | Intermediate AI/ML Engineer | Solink | Ottawa Office | 0.52 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 172 | Machine Learning Researcher - Springtail | Astera Institute | Emeryville HQ | 0.52 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 173 | Advanced Data Engineer - GCP | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.2805 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 174 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7493 | 0.2737 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 175 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 176 | Data Engineer, AI/ML III/IV | Zone 5 Technologies | United States | 0.5184 | 0.2737 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Analytics Engineering, Python |
| 177 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.5377 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 178 | Senior AI Engineer I - Agentic AI | American Express | New York, NY, United States / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus / Charlotte Hybrid-600 Tryon | 0.4035 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 179 | Senior AI Data Infrastructure/Pipeline Engineer | XPENG | Santa Clara, CA | 0.5536 | 0.2737 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 180 | ML Systems Engineer, Robotics | ScaleAI | San Francisco, CA | 0.5275 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 181 | Senior AI Infrastructure Engineer, Model Serving Platform | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 182 | Senior Software Engineer, Operations Research | Lila Sciences | Cambridge, MA USA | 0.4661 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 183 | Senior Software Engineer, Data | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4621 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 184 | Lead Data Engineer | Honeywell | Atlanta, GA, United States | 0.326 | 0.2737 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 185 | Advanced AI Engineer | Honeywell | Charlotte, NC, United States | 0.3214 | 0.2737 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 186 | Machine Learning Engineer II / Senior Machine Learning Engineer I, Physical Sciences | Lila Sciences | Cambridge, MA USA | 0.3547 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 187 | Software Development Engineer - Gen AI | GM Financial | Irving, TX, United States / US - Arlington, TX | 0.3203 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 188 | Senior Machine Learning Engineer, Recommendation & AI Applications | NewsBreak | Mountain View, California, United States | 0.4486 | 0.2737 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 189 | Software Engineer, Code Platform | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 190 | Senior Research Engineer, Controls | PlusAI | Santa Clara, CA | 0.32 | 0.2737 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 191 | Senior Machine Learning Engineer, Simulation | PlusAI | Santa Clara, CA | 0.32 | 0.2737 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Python |
| 192 | Senior Software Engineer, AI/ML (Infrastructure & Platform) | Wealth.com | New York, New York | 0.52 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 193 | Senior IT Architect | Honeywell | Bucuresti, Romania | 0.3606 | 0.273 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Data Engineering |
| 194 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4775 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 195 | Advanced Software Engineer -AI R&D | Honeywell | North Ryde, New South Wales, Australia | 0.3322 | 0.2675 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 196 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.3223 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 197 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MySQL |
| 198 | Forward Deployed Software Engineer - AUS Government | Palantir | Sydney, Australia | 0.32 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 199 | Forward Deployed Software Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2675 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 200 | Forward Deployed Software Engineer | Palantir | London, United Kingdom | 0.32 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 201 | Software Engineer, Data Infrastructure | Notion | Hyderabad, India | 0.52 | 0.2675 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 202 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.4203 | 0.2563 | SWE_FULLTIME | Python |
| 203 | Computing Architect (Manhattan Warehouse M.S.) | Boeing | USA - Hialeah, FL | 0.4881 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 204 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3663 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 205 | Manufacturing Applications and Controls Engineer (Onsite) | RTX | US-ME-NORTH BERWICK-113 ~ 113 Wells St ~ WELLS, Rte 9 | 0.476 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 206 | 2026 Raytheon Full Time - Software Engineer I - Andover, MA (Onsite) | RTX | US-MA-ANDOVER-AN0 ~ 366 Lowell St ~ BLDG AN0 | 0.3312 | 0.2563 | SWE_FULLTIME | Python, Automation |
| 207 | Consultant (Technical, Public Sector) | Appian | Atlanta, Georgia | 0.2733 | 0.2563 | SWE_FULLTIME | SQL, data modeling |
| 208 | Software Engineer, Simulation | PlusAI | Santa Clara, CA | 0.3273 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 209 | Software Engineer I, Instrument Software  | Lila Sciences | Cambridge, MA USA | 0.2804 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 210 | Software Engineer, Tools & Services | Basis | United States | 0.3204 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 211 | Software Engineer (Gen AI) | EarnIn | Mountain View, US | 0.4277 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 212 | SWE Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3201 | 0.2563 | SWE_FULLTIME | Python |
| 213 | Integration Developer  | MaintainX | Miami, Florida | 0.32 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 214 | QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.3295 | 0.2563 | SWE_FULLTIME | Python |
| 215 | Scientific Software Engineer- Shuttle Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2563 | SWE_FULLTIME | Python |
| 216 | Scientific Software Engineer - Virtual Machine & Emulation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2563 | SWE_FULLTIME | Python |
| 217 | Scientific Software Engineer - Compiler | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2563 | SWE_FULLTIME | Python |
| 218 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 219 | Full-Stack Software Engineer (Backend Oriented) | Lendbuzz | Boston, MA | 0.32 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 220 | Neurodivergent Fellowship | Palantir | Washington, D.C. | 0.32 | 0.2563 | SWE_FULLTIME | Python |
| 221 | Neurodivergent Fellowship | Palantir | New York, NY | 0.32 | 0.2563 | SWE_FULLTIME | Python |
| 222 | Software Engineer, C++ Middleware and Runtime Infrastructure | PlusAI | Santa Clara, CA | 0.32 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 223 | Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 224 | Application Security Engineer | Palantir | Washington, D.C. | 0.32 | 0.2563 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 225 | Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.2563 | SWE_FULLTIME | Python |
| 226 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.52 | 0.2563 | SWE_FULLTIME | Python |
| 227 | Embedded Software Engineer | Base Power Company | Austin, TX | 0.52 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 228 | Software Engineer, Core Product | Ramp | New York, NY (HQ) | 0.52 | 0.2563 | SWE_FULLTIME | Python |
| 229 | Software Engineer - Fleet | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 230 | Application Security Engineer, AI Security | Notion | San Francisco, California | 0.52 | 0.2563 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 231 | Software Engineer, Trust | Notion | San Francisco, California / New York, New York | 0.52 | 0.2563 | SWE_FULLTIME | Python |
| 232 | Software Engineer, Security | Notion | San Francisco, California | 0.52 | 0.2563 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 233 | Software Engineer, Growth Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2563 | SWE_FULLTIME | Python |
| 234 | Software Engineer, Agent Developer Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 235 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI | 0.6276 | 0.255 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning |
| 236 | Senior Technical Product Management Specialist | Boeing | USA - Seattle, WA | 0.5556 | 0.255 | PRODUCT_MANAGER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering |
| 237 | Data Engineer | Clarity Innovations | Herndon, VA and/or Columbia, MD | 0.4038 | 0.255 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure |
| 238 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.326 | 0.255 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 239 | Cloud Engineer | Lendbuzz | Tel Aviv | 0.32 | 0.255 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 240 | Senior Machine Learning Infrastructure Engineer | PlusAI | Santa Clara, CA | 0.32 | 0.255 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 241 | Site Reliability Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.255 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 242 | Software Engineer, Argentina | Ramp | Remote (Buenos Aires, Argentina) | 0.52 | 0.255 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 243 | Software Engineer, Production Engineering | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.255 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 244 | Data Scientist (Data Science) | Boeing | USA - Everett, WA | 0.4501 | 0.2512 | ML_ENGINEER_FULLTIME | Machine Learning, Python, R |
| 245 | Sr Data Scientist | GM Financial | Fort Worth, TX, United States | 0.3452 | 0.2512 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 246 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.659 | 0.2505 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 247 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.538 | 0.2505 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 248 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5827 | 0.2505 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 249 | Credit Policy Expert (Experto/a en política de Crédito) – LatAm | Clara | Latin America  | 0.3287 | 0.2505 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 250 | Sr Advanced AI Data Engineer | Honeywell | Monterrey, NLE, Mexico | 0.3218 | 0.2505 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 251 | Sr. Data Analyst | EarnIn | Bengaluru, India | 0.3521 | 0.2392 | DATA_ANALYST_FULLTIME, DATA_SCIENTIST_FULLTIME | Analytics Engineering, Machine Learning, SQL |
| 252 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.2392 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 253 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.2392 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 254 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2392 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 255 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2392 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 256 | GTM Engineer | Greenhouse | British Columbia | 0.5275 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 257 | Software Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 258 | AI Engineer III | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.2363 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 259 | Software Engineer II | Appian | Chennai, India | 0.3766 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 260 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.2363 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 261 | Software Engineer II | Appian | Chennai, India | 0.359 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 262 | Machine Learning Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.2363 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 263 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2363 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 264 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3204 | 0.2363 | SWE_FULLTIME | Cloud Infrastructure, SQL |
| 265 | Machine Learning Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.2401 | 0.2363 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 266 | Platform Developer, AI Builder  | MaintainX | Canada/United States | 0.32 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 267 | Développeur(se) Logiciel de Plateforme, Outils de développement IA | MaintainX | Montreal, Canada | 0.32 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 268 | Measurement Software Engineer | Axiomatic AI | Toronto, Canada | 0.32 | 0.2363 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 269 | Forward Deployed Infrastructure Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2363 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 270 | Forward Deployed AI Engineer | Palantir | London, United Kingdom | 0.32 | 0.2363 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 271 | Data Science, Music & Audio | Melotech | Berlin / London / New York / Los Angeles / San Francisco | 0.52 | 0.2363 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 272 | AI/ML Engineer | Melotech | Berlin / New York / London | 0.52 | 0.2363 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 273 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.7386 | 0.2325 | ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 274 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 275 | Equipment & Tooling Software Engineer (Associate, Experienced and/or Senior) | Boeing | USA - North Charleston, SC | 0.3555 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 276 | Senior Technical Consultant | Appian | Boston, Massachusetts | 0.3209 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 277 | Senior Consultant (Public Sector) | Appian | Denver, Colorado | 0.3209 | 0.2325 | SWE_FULLTIME | Machine Learning, SQL, Python |
| 278 | Senior Data Engineers | American Express | New York, NY, United States | 0.3276 | 0.2325 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 279 |  Senior Software Engineer,  Full-Stack – Scale GP | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 280 | Senior Software Engineer, App | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4165 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 281 | Senior Software Engineer, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3879 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 282 | Advanced Software Engineer | Honeywell | Pittsburgh, PA, United States | 0.3223 | 0.2325 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 283 | Lead Software Development Engineer | iSpot | Bellevue, WA | 0.3647 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 284 | AI Applied Scientist | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2325 | ML_ENGINEER_FULLTIME | Machine Learning, Python, R |
| 285 | Data Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.2325 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 286 | Senior Software Engineer - AI/ML | Wealth.com | New York, New York | 0.52 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 287 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.52 | 0.2325 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 288 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.52 | 0.2325 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 289 | Senior Product Data Scientist | MaintainX | Montreal, Toronto, Vancouver, SF (Remote) | 0.4453 | 0.2318 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 290 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5639 | 0.2318 | ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 291 | Senior Consultant | Appian | Tokyo, Japan | 0.359 | 0.2318 | SWE_FULLTIME | Machine Learning, Cloud Infrastructure, SQL |
| 292 | Software Engineer, Robotics | ScaleAI | Argentina; Uruguay | 0.3201 | 0.2318 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 293 | Senior Autonomy Software Systems Engineer (Python / C++ / Data) | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3351 | 0.2318 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 294 | Experienced Software Engineer | Boeing | USA - Hazelwood, MO | 0.3829 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 295 | Software Engineer II - Test | RTX | US-AZ-TUCSON-805 ~ 1151 E Hermans Rd ~ BLDG 805 | 0.3636 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 296 | Intermediate Quality Assurance Engineer | Honeywell | Salem, OR, United States | 0.3619 | 0.225 | SWE_FULLTIME | — |
| 297 | Software Engineer I, QA | True Anomaly | Denver, CO or Long Beach, CA | 0.2857 | 0.225 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | — |
| 298 | Software Engineer | Boeing | USA - Maryland Heights, MO | 0.3153 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 299 | Associate Software Engineer | Boeing | USA - Maryland Heights, MO | 0.2611 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 300 | Mid-Level Programmer Analyst | Boeing | USA - Saint Charles, MO | 0.2575 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 301 | Software Engr II | Honeywell | Atlanta, GA, United States | 0.2402 | 0.225 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 302 | Scientific Software Engineer — Emulation & Application | QuEra Computing | Boston, MA, USA | 0.3505 | 0.225 | SWE_FULLTIME | — |
| 303 | Software Engineer, Growth & Monetization | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.225 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 304 | Software Engineering Instructor (Continuous)  | Per Scholas | Columbus, Ohio, United States | 0.1771 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 305 | Software Engineer - Core Interfaces | Palantir | Palo Alto, CA | 0.32 | 0.225 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 306 | Software Engineer (C#/React) | Reply | Chicago, Illinois | 0.32 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 307 | Software Engineer - Edge | Palantir | Washington, D.C. | 0.32 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 308 | Software Engineer - Frontend Developer Productivity | Palantir | New York, NY | 0.32 | 0.225 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 309 | Mixed Reality Developer | Palantir | Washington, D.C. | 0.32 | 0.225 | SWE_FULLTIME | — |
| 310 | Software Engineer, Fraud & Identity | Ramp | New York, NY (HQ) | 0.52 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 311 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 312 | Software Engineer, Accounting | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.225 | SWE_FULLTIME | — |
| 313 | Software Engineer, Product Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 314 | Software Engineer, Product | Base Power Company | Austin, TX | 0.52 | 0.225 | SWE_FULLTIME | — |
| 315 | Software Engineer, Bill Pay & Procurement | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.225 | SWE_FULLTIME | — |
| 316 | Software Engineer, Bill Pay & Procurement | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.225 | SWE_FULLTIME | — |
| 317 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 318 | Advanced Data Scientist | Honeywell | Hyderabad, Telangana, India | 0.5971 | 0.2205 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 319 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.5385 | 0.2205 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Python |
| 320 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.5384 | 0.2205 | DATA_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, Machine Learning, SQL |
| 321 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.5307 | 0.2205 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 322 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.4551 | 0.2205 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 323 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.2205 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Machine Learning, Python |
| 324 | Sr. Machine Learning Engineer | EarnIn | Bengaluru, India | 0.3978 | 0.2205 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 325 | Senior Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.3717 | 0.2205 | DATA_ANALYST_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 326 | Senior Data Engineer | EarnIn | Bengaluru, India | 0.3577 | 0.2205 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 327 | Senior Data Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.2205 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 328 | Senior Data Engineer | Super.com | Canada / United States | 0.52 | 0.2205 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 329 | Associate Application Engineer | Appian | McLean, Virginia | 0.359 | 0.2175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Python, Data Modeling |
| 330 | Forward Deployed Software Engineer | Palantir | Abu Dhabi, United Arab Emirates | 0.32 | 0.2175 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Python, SQL |
| 331 | Forward Deployed Software Engineer | Palantir | Vilnius, Lithuania | 0.32 | 0.2175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 332 | Forward Deployed Engineer, GTM - Japan | Notion | Tokyo, Japan  | 0.52 | 0.2175 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 333 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.6658 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 334 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.638 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 335 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5382 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 336 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5381 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 337 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4917 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 338 | Software Engineer III - MFT Business Enablement - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 339 | Senior AI Engineer II - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.3857 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 340 | Senior Software Engineer, Digital Banking & Payments | American Express | Phoenix, AZ, United States | 0.3857 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 341 | Data Engineer-ETL Tools & Python/ Python frameworks | American Express | Phoenix, AZ, United States | 0.3857 | 0.2137 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, ETL |
| 342 | Experienced Software Engineer, Developer | Boeing | USA - Seal Beach, CA | 0.3296 | 0.2137 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 343 | Senior Software Engineer, Scientific System of Record | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4561 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 344 | Senior Consultant (Public Sector) | Appian | Atlanta, Georgia | 0.3209 | 0.2137 | SWE_FULLTIME | Machine Learning, SQL |
| 345 | Senior Machine Learning Engineer - AI Foundation | XPENG | Santa Clara, CA | 0.5216 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 346 | Senior Machine Learning Engineer - Foundation Model | XPENG | Santa Clara, CA | 0.5216 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 347 | Senior Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.3452 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 348 | Senior Compliance Automation Engineer | True Anomaly | Denver, CO or Long Beach, CA or SF Bay area, CA or Washington, DC | 0.3729 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 349 | Sr Software Engineer II - Global Commercial Services | American Express | FL, United States / Sunrise Campus / New York-Amex Tower WFC-35 Hr / AEDR Desert Ridge OB2-McDowell | 0.3322 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 350 | Senior Software Engineer, Prenatal | BillionToOne | Menlo Park, CA | 0.4432 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 351 | Senior Scientist, Oncology | BillionToOne | Menlo Park, CA | 0.3406 | 0.2137 | RESEARCH_SCIENTIST_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 352 | Senior Scientist | BillionToOne | Menlo Park, CA | 0.3406 | 0.2137 | RESEARCH_SCIENTIST_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 353 | AI Engineer, Agent Platform | NewsBreak | Mountain View, California, United States | 0.3771 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 354 | Senior Software Engineer - Internal Tools & Productivity | ScaleAI | San Francisco, CA | 0.5141 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 355 | Senior Simulation Engineer I/II, Robotics | Lila Sciences | Cambridge, MA USA | 0.4105 | 0.2137 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 356 | Scientist/Sr. Scientist, AI Safety | Lila Sciences | Cambridge, MA USA; London, UK; San Francisco, CA USA | 0.5204 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 357 | Senior Software Engineer, ML Research | Lila Sciences | Cambridge, MA USA | 0.3852 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 358 | Sr Oracle Application Developer | GM Financial | Irving, TX, United States | 0.3203 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 359 | Lead AI Engineer | Honeywell | Atlanta, GA, United States | 0.3203 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 360 | ML Research Engineer, ML Systems | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.4502 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 361 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 362 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 363 | Sr Software Engineer - Core Backend & Platform Engineering | Basis | United States | 0.32 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 364 | Software Engineer, Developer Experience | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 365 | Software Engineer, Distributed Systems | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 366 | Sr. QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.4105 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 367 | Senior Computer Vision/AI  Engineer | BrightAI | Palo Alto, CA | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 368 | Senior Machine Learning Engineer II | CesiumAstro | Austin, TX | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 369 | Senior Software Engineer, Planning | PlusAI | Santa Clara, CA | 0.32 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 370 | Senior AI Engineer | Reply | Seattle, Washington | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 371 | Senior AI Engineer, Time-Series Signal Processing | BrightAI | Palo Alto, CA | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 372 | Senior AI Engineer – LLM, RAG | BrightAI | Palo Alto, CA | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 373 | Senior AI Engineer | Reply | Chicago, Illinois | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 374 | Senior AI Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 375 | Applied Research Engineer, Agents | Labelbox | San Francisco Bay Area | 0.52 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 376 | Senior Machine Learning Engineer, Perception | PlusAI | Santa Clara, CA | 0.32 | 0.2137 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 377 | Senior Software Engineer, Mapping & Localization | PlusAI | Santa Clara, CA | 0.32 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 378 | Senior Software Engineer, AI Enablement | Wealth.com | New York, New York | 0.52 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 379 | Sr. Site Development Engineer | Mariana Minerals | San Francisco HQ | 0.52 | 0.2137 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 380 | Senior Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.2137 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 381 | Senior Software Engineer | Wealth.com | Hybrid, New York, Tempe, San Francisco | 0.52 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 382 | Senior Infrastructure Engineer | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 383 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.2137 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 384 | Senior Applied Scientist, Parts Intelligence & Inventory Optimization | MaintainX | Canada (Remote) | 0.3599 | 0.2093 | ML_ENGINEER_FULLTIME | Machine Learning, Python, NumPy |
| 385 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 386 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.5118 | 0.205 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 387 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3857 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 388 | Intermediate Software Engineer | Achievers | Canada | 0.3565 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 389 | Project Engr II | Honeywell | Pune, Maharashtra, India | 0.3247 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 390 | DevOps Specialist | MaintainX | Montreal, Toronto | 0.32 | 0.205 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 391 | Développeur(se) Logiciel de Plateforme | MaintainX | Montreal, Quebec  | 0.32 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 392 | Software Engineer, AI Product (London, United Kingdom) | Figma | London, England | 0.32 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 393 | Platform Engineer - Identity and Access Management (IAM) | Palantir | London, United Kingdom | 0.32 | 0.205 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure |
| 394 | Software Engineer - Apollo Platform | Palantir | London, United Kingdom | 0.32 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 395 | Software Engineer, Infrastructure  | Notion | Hyderabad, India | 0.52 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 396 | Software Engineer, Developer Experience | Notion | Hyderabad, India | 0.52 | 0.205 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 397 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 398 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.5381 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 399 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4914 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 400 | Senior AI Engineer II | American Express | LONDON, LONDON, United Kingdom / Sussex House | 0.3857 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 401 | Senior AI Engineer I | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.2017 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 402 | Software Engr II | Honeywell | India | 0.352 | 0.2017 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 403 | Advanced Chemical Engr (Digital Exec Tools Specialist’) | Honeywell | India | 0.3218 | 0.2017 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 404 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 405 | Lead Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 406 | Sr IT Database Administrator | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2017 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, MySQL |
| 407 | Advanced Data Engineer | Honeywell | Pune, Maharashtra, India | 0.3202 | 0.2017 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 408 | Développeur de données senior | MaintainX | Montreal, Toronto | 0.32 | 0.2017 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 409 | Senior Data Developer - Streaming | MaintainX | Montreal, Toronto | 0.32 | 0.2017 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 410 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.6418 | 0.195 | DATA_ENGINEER_FULLTIME | Data Engineering, data modeling |
| 411 | Senior SAP FIORI Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 412 | Senior Software Security Engineer | Boeing | USA - Seattle, WA | 0.6548 | 0.195 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure |
| 413 | Cloud Application Deployment and Migration Specialist (Mid-Level, Senior or Lead) **Sign on Bonus Potential** | Boeing | USA - Berkeley, MO | 0.5431 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 414 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 415 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 416 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 417 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.5219 | 0.195 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, data modeling |
| 418 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.516 | 0.195 | SWE_FULLTIME | Cloud Infrastructure |
| 419 | Service Now Sys Administrator | RTX | US-TX-REMOTE | 0.4761 | 0.195 | SWE_FULLTIME | Cloud Infrastructure |
| 420 | Senior Backend Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.455 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 421 | Java Software Engineer (Associate, Experienced or Senior) - Bixby | Boeing | USA - Seal Beach, CA | 0.4178 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 422 | Lead Architect, S4 Integration | Honeywell | Charlotte, NC, United States | 0.3716 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 423 | Senior Software Engineer II - Amex Ads | American Express | New York, NY, United States | 0.3322 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 424 | Lead Software Architect - EPMS Systems | Honeywell | Atlanta, GA, United States | 0.3276 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 425 | Advanced Software Engineer - Cybersecurity | Honeywell | Duluth, GA, United States | 0.3204 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 426 | Lead IT Architect ORACLE HCM (Integration Cloud) | Honeywell | Charlotte, NC, United States | 0.3204 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 427 | Salesforce Sr IT Architect – Customer and Commercial Experience (CCEX) | Honeywell | Charlotte, NC, United States | 0.3203 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 428 | Lead Software Engineer | Reply | Atlanta, Georgia | 0.3201 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 429 |  Senior SDET - Tooling Engineer | EarnIn | Mountain View, US | 0.4086 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 430 | Software Engineer, Production Engineering | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.195 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 431 | Azure Cloud Architect | Reply | Chicago, Illinois | 0.32 | 0.195 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 432 | Azure Cloud Architect | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.195 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 433 | Senior Software Engineer, Substrate | Palantir | Washington, D.C. | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 434 | Senior Software Engineer, Network Infrastructure | Palantir | Washington, D.C. | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 435 | Senior Software Engineer, Substrate | Palantir | New York, NY | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 436 | Senior Software Engineer, Substrate | Palantir | Seattle, WA | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 437 | Senior Software Engineer, Network Infrastructure | Palantir | New York, NY | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 438 | Senior Software Engineer, Network Infrastructure | Palantir | Seattle, WA | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 439 | Senior Software Engineer - Observability | Palantir | New York, NY | 0.32 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 440 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | New York | 0.52 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 441 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | San Francisco | 0.52 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 442 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6285 | 0.1905 | ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 443 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5719 | 0.1905 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 444 | Senior Consultant (Public Sector) | Appian | McLean, Virginia | 0.359 | 0.1905 | SWE_FULLTIME | Machine Learning, SQL, Python |
| 445 | Senior Technical Consultant | Appian | Madison, Wisconsin | 0.3209 | 0.1905 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 446 | Pricing Data Scientist | iHerb | United States of America - Irvine, California; United States of America - Remote / Home Office | 0.4008 | 0.1905 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 447 | Senior Data Infrastructure Engineer | Voltus | Remote | 0.3213 | 0.1905 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 448 | Senior Full Stack Developer, Data Integrations | Solink | Ottawa Office | 0.52 | 0.1905 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 449 | Senior Software Developer, Core Applications | Solink | Ottawa Office | 0.52 | 0.1905 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 450 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.697 | 0.1863 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 451 | Appian Product Engineer  | Appian | McLean, Virginia | 0.584 | 0.1863 | SWE_FULLTIME | SQL |
| 452 | Software Control Engr I (C++, SQL, Automation) | Honeywell | Mexico | 0.4549 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, automation |
| 453 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.3857 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 454 | Application Engineer | Appian | McLean, Virginia | 0.3784 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 455 | Consultant (Software Implementation, Public Sector) | Appian | McLean, Virginia | 0.359 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, data modeling |
| 456 | Consultant (Top Secret Clearance, Software Implementation) | Appian | McLean, Virginia | 0.359 | 0.1863 | SWE_FULLTIME | SQL, data modeling |
| 457 | Growth Marketing Developer (Desenvolvedor de Growth Marketing) -  São Paulo  (Hybrid | Clara | Latin America  | 0.3287 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 458 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Bogotá (Hybrid) | Clara | Latin America  | 0.3287 | 0.1863 | SWE_FULLTIME | SQL |
| 459 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Mexico City (Hybrid) | Clara | Latin America  | 0.3287 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 460 | Développeur(se) Full-Stack intermédiaire  | MaintainX | Montréal | 0.32 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 461 | Scientific Software Engineer - Shuttle Compilation  | QuEra Computing | Tsukuba, Japan | 0.32 | 0.1863 | SWE_FULLTIME | Python |
| 462 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Tsukuba, Japan | 0.32 | 0.1863 | SWE_FULLTIME | Python |
| 463 | Scientific Software Engineer - Compiler | QuEra Computing | Tsukuba, Japan | 0.32 | 0.1863 | SWE_FULLTIME | Python |
| 464 | Software Engineer I - Device Drivers | Torc Robotics | Ann Arbor, MI | 0.2833 | 0.1863 | SWE_FULLTIME | Python |
| 465 | Software Engineer, Guest Travel | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Denver, CO | 0.52 | 0.1863 | SWE_FULLTIME | Python |
| 466 | Software Engineer - Distributed Simulation Systems | Astera Institute | Emeryville HQ | 0.52 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 467 | Software Engineer, Developer and Qualification Tools | d-Matrix | Santa Clara | 0.52 | 0.1863 | SWE_FULLTIME | Python, Automation |
| 468 | Software Engineer - Distributed Simulation Systems | Astera Institute | Emeryville HQ | 0.52 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 469 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure |
| 470 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5969 | 0.1792 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, R |
| 471 | Senior Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.1725 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 472 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5695 | 0.1717 | BACKEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 473 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.1717 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 474 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.1717 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 475 | Lead Software Engineer (Kubernetes) | Appian | McLean, Virginia | 0.514 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 476 | Senior Software Engineer  | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.3685 | 0.1717 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 477 | Senior Software Engineer | Appian | McLean, Virginia | 0.359 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 478 | Senior Consultant (Public Sector) | Appian | Raleigh, North Carolina | 0.3209 | 0.1717 | SWE_FULLTIME | Machine Learning, SQL |
| 479 | Senior Applied Machine Learning Engineer, Asset Intelligence | MaintainX | San Francisco (Remote) | 0.3581 | 0.1717 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, anomaly detection |
| 480 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Remote - US, Ann Arbor, MI | 0.4657 | 0.1717 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 481 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Montreal, Canada, Remote - Canada | 0.4293 | 0.1717 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 482 | Sr Advanced Software Engr | Honeywell | Singapore, Singapore, Singapore | 0.3296 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 483 | Senior, Software Engineer - Cloud Automation | Torc Robotics | Ann Arbor, MI, Remote - US | 0.3216 | 0.1717 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 484 | Senior, Software Engineer - Release Pipelines | Torc Robotics | Ann Arbor, MI ;Remote - US | 0.3808 | 0.1717 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 485 | Senior AI Engineer - Agentic | Podium | Lehi, Utah, Open to Remote | 0.32 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 486 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 487 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 488 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.1675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 489 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.538 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 490 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 491 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 492 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.1675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 493 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.1675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 494 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 495 | Application Engr II | Honeywell | Chennai, Tamil Nadu, India | 0.3247 | 0.1675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 496 | Forward Deployed Software Engineer - AUS Government | Palantir | Canberra, Australia | 0.32 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 497 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.52 | 0.1675 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 498 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.5385 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 499 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3717 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 500 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3398 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 501 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MySQL |
| 502 | Senior Data Developer, Governance  | MaintainX | Montreal, Toronto | 0.32 | 0.1605 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 503 | Experienced Java Software Engineer | Boeing | POL - Gdansk, Poland | 0.5382 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 504 | AI Prompt Engineer | Appian | McLean, Virginia | 0.359 | 0.155 | SWE_FULLTIME | — |
| 505 | Application Programmer | EarnIn | Remote, US | 0.2601 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 506 | Forward-deployed Engineer - LatAm (Remote) | Clara | Latin America  | 0.3287 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 507 | Forward-deployed Engineer - LatAm (Remote) | Clara | São Paulo, São Paulo, Brazil | 0.3287 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 508 | Application Engr II | Honeywell | Chongqing, China | 0.3247 | 0.155 | SWE_FULLTIME | — |
| 509 | Software Engineer II - MCU Applications (C++/Linux) | Torc Robotics | Ann Arbor, MI | 0.3371 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 510 | Project Engr I | Honeywell | Tianjin, China | 0.3214 | 0.155 | SWE_FULLTIME | — |
| 511 | Developer Advocate (Tokyo, Japan) | Figma | Tokyo, Japan | 0.32 | 0.155 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 512 | Software Engineer, Banking | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.52 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 513 | Mobile Engineer, Android | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.155 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 514 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.5382 | 0.1538 | SWE_FULLTIME | Python |
| 515 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.508 | 0.1538 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 516 | Lead Software Engineer - Firmware | Honeywell | Pittsford, NY, United States | 0.4921 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 517 | Advanced Software Engineer | Honeywell | Raleigh, NC, United States | 0.3716 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 518 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 519 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.1538 | SWE_FULLTIME | SQL |
| 520 | Senior Identity Security Engineer | Palantir | Palo Alto, CA | 0.3318 | 0.1538 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 521 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 522 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 523 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 524 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 525 | Engineer II /Senior Software Engineer, Simulation | Lila Sciences | Cambridge, MA USA | 0.3486 | 0.1538 | SWE_FULLTIME | Python |
| 526 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.3276 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 527 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.3276 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 528 | Senior Software Engineer, GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 529 | Senior Full Stack Engineer | EarnIn | Mountain View, US | 0.4891 | 0.1538 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Python |
| 530 | Senior Software Engineers | American Express | New York, NY, United States | 0.3202 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 531 | Sr Software Engineer - Basis Platform / DSP | Basis | United States | 0.32 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 532 | Senior Software Engineer / GTM Platform, Backend | Ramp | New York, NY (HQ) | 0.52 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 533 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.6542 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 534 | Senior Platform Engineer  | Clarity Innovations | Required  | 0.6497 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 535 | Cloud Architect | RTX | Warminster, Wiltshire | 0.3858 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 536 | Advanced Software Engineer | Honeywell | Gdansk, Pomorskie, Poland | 0.3606 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 537 | Senior Software Engineer - Java / AWS Services | Appian | McLean, Virginia | 0.359 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 538 | Senior Software Engineer - Database Platform | Appian | McLean, Virginia | 0.359 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 539 | Développeur logiciel senior, facturation | MaintainX | Montréal | 0.32 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 540 | Edge Infrastructure Engineer | Palantir | Warsaw, Poland | 0.32 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 541 | Azure Cloud Architect | Reply | Detroit Area, Michigan | 0.32 | 0.153 | SWE_FULLTIME | Cloud Infrastructure |
| 542 | Senior Data Engineer | Reply | Kochi, Kerala | 0.32 | 0.153 | DATA_ENGINEER_FULLTIME | Data Engineering, data modeling |
| 543 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.1418 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 544 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1418 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 545 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4913 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 546 | Senior Consultant | Appian | Chennai, India | 0.3905 | 0.1418 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, SQL |
| 547 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1418 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 548 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 549 | Senior Software Engineer | Appian | Chennai, India | 0.3769 | 0.1418 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 550 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1418 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 551 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 552 | Senior Technical Consultant | Appian | Toronto, Canada | 0.359 | 0.1418 | SWE_FULLTIME | Machine Learning, SQL, data modeling |
| 553 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 554 | Sr Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3322 | 0.1418 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 555 | Senior Software Engineer - Live Pay | EarnIn | Vancouver, Canada | 0.4769 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 556 | Applied AI Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.1418 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 557 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3201 | 0.1418 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 558 | SWE Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.3201 | 0.1418 | SWE_FULLTIME | Machine Learning, Python |
| 559 | Senior Software Engineer (Backend Engineering) ⭐ | Achievers | Toronto | 0.32 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 560 | Développeur(euse) de données sénior, gouvernance des données | MaintainX | Montréal, Toronto | 0.32 | 0.1418 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL |
| 561 | Développeur(se) de logiciel senior spécialisé en moteurs de recherche | MaintainX | Montréal, Toronto | 0.32 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 562 | Senior AI Developer (Coming Soon!) | Nuclear Promise X | Canada | 0.52 | 0.1418 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 563 | Software Machine Learning Test Engineer - Sr Engineer | d-Matrix | Bangalore | 0.52 | 0.1418 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 564 | Senior QA Engineer | Super.com | Canada / United States | 0.52 | 0.1418 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 565 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.1362 | SWE_FULLTIME | Python |
| 566 | Advanced SW Test Engineer (m/f/d) | Honeywell | Ratingen, Nordrhein-Westfalen, Germany | 0.5381 | 0.1362 | SWE_FULLTIME | Python |
| 567 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.1362 | SWE_FULLTIME | Python |
| 568 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.1362 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | SQL |
| 569 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5381 | 0.1362 | SWE_FULLTIME | Python |
| 570 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5379 | 0.1362 | SWE_FULLTIME | Python |
| 571 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1362 | SWE_FULLTIME | Python |
| 572 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5377 | 0.1362 | SWE_FULLTIME | SQL |
| 573 | GTM Engineer | Greenhouse | Ontario | 0.5276 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 574 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.2496 | 0.1362 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 575 | Application Engr I | Honeywell | Chennai, Tamil Nadu, India | 0.3223 | 0.1362 | SWE_FULLTIME | Python |
| 576 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 577 | Software Engr II - C++ Development, QT | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 578 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 579 | SWE Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.1362 | SWE_FULLTIME | Python |
| 580 | Integrations Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 581 | Développeuse / Développeur d'intégration | MaintainX | Montreal, Toronto | 0.32 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 582 | Intermediate Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 583 | Scientific Software Engineer  | QuEra Computing | Toronto, Ontario, Canada | 0.32 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 584 | Scientific Software Engineer - Compiler | QuEra Computing | Harwell, England, UK | 0.2998 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 585 | Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 586 | Application Security Engineer | Palantir | London, United Kingdom | 0.32 | 0.1362 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 587 | Senior Integration Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 588 | Senior Mobile Engineer (Android) | EarnIn | Mountain View, US | 0.727 | 0.135 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 589 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 590 | Sr Software Engineer - Global Commercial Services | American Express | New York, NY, United States / AEDR Desert Ridge CSB - Sierra | 0.352 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 591 | Senior Software Engineer, Front End | True Anomaly | Denver, CO or Long Beach, CA | 0.4886 | 0.135 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 592 | Senior Embedded Software Engineer II | CesiumAstro | Westminster, CO | 0.3313 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 593 | Senior Front End Engineer | EarnIn | Mountain View, US | 0.4891 | 0.135 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 594 | Software Engineers | American Express | Phoenix, AZ, United States | 0.3202 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 595 | Lead Software Engineer | Reply | Chicago, Illinois | 0.3201 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 596 | Sr. Software Engineer, React/ React Native | Prosper | San Francisco, CA | 0.32 | 0.135 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 597 | Senior Software Engineer, iOS | NewsBreak | Mountain View, California, United States | 0.439 | 0.135 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 598 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.135 | SWE_FULLTIME | — |
| 599 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.135 | SWE_FULLTIME | — |
| 600 | Senior Embedded Software Integration Engineer | PlusAI | Chicago, IL | 0.32 | 0.135 | SWE_FULLTIME | — |
| 601 | Senior Backend Engineer | Nash | San Francisco | 0.52 | 0.135 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 602 | Senior Software Engineer / Web + Design | Ramp | New York, NY (HQ) | 0.52 | 0.135 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 603 | Senior Software Engineer (Frontend Focus) | Kira | New York | 0.52 | 0.135 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 604 | Senior Software Engineer / GTM Platform, Frontend | Ramp | New York, NY (HQ) | 0.52 | 0.135 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 605 |  Senior Software Engineer, Visualization | Foxglove | San Francisco, CA | 0.52 | 0.135 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 606 | Senior Software Engineer - API Experience | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 607 | Senior IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 608 | Sr Software Eng Supervisor | Honeywell | India | 0.5381 | 0.123 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 609 | Sr IT Architect | Honeywell | Pune City, Maharashtra, India | 0.4915 | 0.123 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure |
| 610 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4915 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 611 | Lead Software Application – Architect | Boeing | IND - Bangalore, India | 0.4553 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 612 | Experienced Software Engineer- FSD | Boeing | IND - Bangalore, India | 0.4551 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 613 | Sr Advanced SW Architect | Honeywell | India | 0.3856 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 614 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.123 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 615 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3276 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 616 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 617 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.123 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure |
| 618 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.123 | SWE_FULLTIME | Cloud Infrastructure |
| 619 | Senior Software Developer, Compliance and Multi-Region | MaintainX | Montreal, Toronto  | 0.32 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 620 | Senior Software Developer, Search  | MaintainX | Montreal, Toronto | 0.32 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 621 | Full-Stack Developer, Connected Data  | MaintainX | Montréal, Toronto | 0.32 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 622 | Software Engineer, Production Engineering  (London, United Kingdom) | Figma | London, England | 0.32 | 0.123 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 623 | Senior Software Engineer, Substrate | Palantir | London, United Kingdom | 0.32 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 624 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.7039 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 625 | Senior Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.1118 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Python |
| 626 | Senior Software Engineer - Operating System | Torc Robotics | Ann Arbor, MI | 0.5232 | 0.1118 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Python |
| 627 | Senior Software Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.368 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 628 | Senior Technical Consultant | Appian | McLean, Virginia | 0.359 | 0.1118 | SWE_FULLTIME | SQL, data modeling |
| 629 | Senior Consultant (Top Secret Clearance) | Appian | McLean, Virginia | 0.359 | 0.1118 | SWE_FULLTIME | SQL, data modeling |
| 630 | Senior Software Engineer, Calibration | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3853 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 631 | Senior Software Engineer, Calibration | Torc Robotics | Remote - Canada, Montreal, Canada | 0.3253 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 632 | Senior Applied Scientist, Scheduling and Optimization | MaintainX | Canada (Remote) | 0.32 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 633 | Senior Mobile Security Engineer (Forensics) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.1118 | MOBILE_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 634 | Founding Engineer | Icon | New York / Remote | 0.52 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 635 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.105 | SWE_FULLTIME | — |
| 636 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 637 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5383 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 638 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.105 | SWE_FULLTIME | — |
| 639 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.105 | SWE_FULLTIME | — |
| 640 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 641 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.5238 | 0.105 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 642 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4917 | 0.105 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 643 | Software Engineer I | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.455 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 644 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.105 | SWE_FULLTIME | — |
| 645 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.105 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 646 | Software Engineer In Test - Android | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.105 | SWE_FULLTIME | — |
| 647 | Software Engineer In Test - iOS | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.105 | SWE_FULLTIME | — |
| 648 | Application Engr II | Honeywell | Pune, Maharashtra, India | 0.3218 | 0.105 | SWE_FULLTIME | — |
| 649 | Software Engr I | Honeywell | Pune City, Maharashtra, India | 0.3211 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 650 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.105 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | — |
| 651 | Full-Stack Developer - IAM | MaintainX | Toronto | 0.32 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 652 | Lead Software Engineer | Appian | McLean, Virginia | 0.514 | 0.093 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 653 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.5066 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 654 | Developpeur SAP ABAP  /  SAP ABAP Developer | RTX | CA-QC-LONGUEUIL-J01 ~ 1000 Blvd Marie-Victorin ~ J01 BLDG | 0.3858 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 655 | Senior Software Engineer - Java /  Hibernate | Appian | McLean, Virginia | 0.359 | 0.093 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 656 | Senior Backend Engineer — ClarOps (Ingeniero Backend Senior de ClarOps) - Remote | Clara | Latin America  | 0.3364 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 657 | Développeur(se) Full-Stack sénior ou en chef  | MaintainX | Montréal | 0.32 | 0.093 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 658 | Senior Software Engineer I, Client Connections | EnergyHub | Remote - United States | 0.3295 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 659 | Senior Software Engineer - Vehicle Diagnostics | Torc Robotics | Ann Arbor, MI, Remote, US | 0.3808 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 660 | Senior iOS Engineer | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.093 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 661 | Senior Software Engineer (PHP/ Golang) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.093 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 662 | Senior Software Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.093 | SWE_FULLTIME | — |
| 663 | Senior React Native Engineer — Driver App  | Nash | Remote HQ / San Francisco | 0.52 | 0.093 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 664 | Senior .NET Developer (Coming Soon!) | Nuclear Promise X | Ontario / Remote | 0.52 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 665 | Senior .NET Developer | Nuclear Promise X | Chalk River | 0.52 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 666 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4918 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 667 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4913 | 0.0817 | SWE_FULLTIME | Python |
| 668 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4553 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 669 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4552 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 670 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 671 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 672 | Senior Associate - Oracle Technical Developer | American Express | Gurugram, HR, India | 0.3717 | 0.0817 | SWE_FULLTIME | SQL |
| 673 | Senior Test Automation Engineer | Appian | Chennai, India | 0.359 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 674 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3519 | 0.0817 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | SQL |
| 675 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.0817 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL |
| 676 | Senior or Lead Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 677 | Senior Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 678 | Senior Runtime Software Engineer   | d-Matrix | Sydney | 0.52 | 0.0817 | SWE_FULLTIME | Python |
| 679 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.5381 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 680 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.063 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 681 | Senior UX Design Engineer, Design Systems | Greenhouse | Ontario | 0.4975 | 0.063 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 682 | Senior Quality Engineer I | American Express | Chennai, TN, India | 0.4917 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 683 | Advanced Embedded Engineer | Honeywell | United Kingdom | 0.3717 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 684 | Sr IT Engineer | Honeywell | Hyderabad, Telangana, India | 0.3716 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 685 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3237 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 686 | Senior Software Engineer | EarnIn | Bengaluru, India | 0.3201 | 0.063 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 687 | Senior Software Developer, Billing  | MaintainX | Montreal, Toronto | 0.32 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 688 | Senior Software Engineers | Achievers | Toronto | 0.32 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 689 | Senior Front End Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.063 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 690 | Senior Software Engineer—Kernels | d-Matrix | Bangalore | 0.52 | 0.063 | SWE_FULLTIME | — |

## Yatharth Mogra (`yatharthmogra@gmail.com`)

**Candidate ID:** `6230dd88-b346-4e96-94fd-4a51c4500f34`

### Subscribed pools
- `DATA_ENGINEER_FULLTIME`
- `ML_ENGINEER_FULLTIME`
- `SWE_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Backend Engineering, Full Stack Development, AI Systems, Machine Learning Research, Data Engineering, Distributed Systems, Cloud Infrastructure, DevOps, Research |
| Preferred locations | NY, USA, New York, USA |
| Primary roles | Software Developer, AI Engineer, Data Engineer, Software Engineer |
| Hard constraints | sponsorship=False, min_salary=None, target_seniority=— |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 662
- **Notification-eligible jobs (≤60d, not yet emailed):** 500
- **Personal score range:** 0.063 – 0.4992 (166 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 549 |
| `BACKEND_ENGINEER_FULLTIME` | 346 |
| `ML_ENGINEER_FULLTIME` | 144 |
| `FULLSTACK_ENGINEER_FULLTIME` | 66 |
| `DATA_ENGINEER_FULLTIME` | 66 |
| `DEVOPS_ENGINEER_FULLTIME` | 63 |
| `FRONTEND_ENGINEER_FULLTIME` | 48 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 27 |
| `SECURITY_ENGINEER_FULLTIME` | 15 |
| `MOBILE_ENGINEER_FULLTIME` | 12 |
| `DATA_SCIENTIST_FULLTIME` | 9 |
| `SUPPORT_ENGINEER_FULLTIME` | 4 |
| `DATA_ANALYST_FULLTIME` | 4 |
| `PRODUCT_MANAGER_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Forward Deployed Software Engineer - US Government - Federal Health and Civilian @ Palantir

- **Location:** New York, NY (unclear)
- **Posted:** 2026-05-07T17:41:25.599000+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.3201
- **Personal score:** 0.4992
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, ML_ENGINEER
- **Capabilities:** Backend Engineering, Data Engineering, AI Systems
- **Skills:** data pipelines, AI orchestration
- **Match reasons:** Backend Engineering, Data Engineering, AI Systems, Java, Python
- **URL:** https://jobs.lever.co/palantir/be4ab5cb-9caa-4c2a-97b9-c73805fca4fc

#### #2 — Software Engineer, Credit @ Ramp

- **Location:** New York, NY (HQ) (unclear)
- **Posted:** —
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.52
- **Personal score:** 0.4992
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER
- **Capabilities:** Backend Engineering, Data Engineering, Distributed Systems
- **Skills:** data consistency, financial systems
- **Match reasons:** Backend Engineering, Data Engineering, Distributed Systems, Java, Python
- **URL:** https://jobs.ashbyhq.com/ramp/5598f7b8-4ae2-4105-a2b4-2d0f55c54c40

#### #3 — AI Engineer III - Global Servicing Technology @ American Express

- **Location:** New York, NY, United States | Sunrise Campus | AEDR Desert Ridge CSB - Sierra (unclear)
- **Posted:** 2026-06-09T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.4916
- **Personal score:** 0.4765
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, ML_ENGINEER
- **Capabilities:** Backend Engineering, AI Systems, Machine Learning, Distributed Systems
- **Skills:** LLMs, Agentic AI, RAG, Distributed Systems
- **Match reasons:** Backend Engineering, AI Systems, Distributed Systems, Python, Go
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26008627/details

#### #4 — Software Engineer II, Lab Software @ Lila Sciences

- **Location:** Cambridge, MA USA (unclear)
- **Posted:** 2026-05-21T22:35:47+00:00
- **Salary:** 120000 – 180000
- **Effort:** MEDIUM
- **Opportunity score:** 0.3318
- **Personal score:** 0.4764
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, FULLSTACK_ENGINEER
- **Capabilities:** Backend Engineering, Full Stack Development, Cloud Infrastructure, DevOps
- **Skills:** Data pipeline architecture, System performance optimization, Orchestration, Infrastructure-as-Code
- **Match reasons:** Backend Engineering, Full Stack Development, Cloud Infrastructure, DevOps, Python
- **URL:** https://job-boards.greenhouse.io/lilasciences/jobs/4250045009

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | New York, NY | 0.3201 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, AI Systems |
| 2 | Backend Software Engineer - Infrastructure, Foundations | Palantir | New York, NY | 0.32 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 3 | Forward Deployed Software Engineer | Palantir | New York, NY | 0.32 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 4 | Software Engineer, Credit | Ramp | New York, NY (HQ) | 0.52 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 5 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4916 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 6 | Forward Deployed Software Engineer - US Government | Palantir | New York, NY | 0.32 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 7 | Software Engineer II, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3318 | 0.4764 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 8 | Software Engineer - Hosted Model Infrastructure | Palantir | New York, NY | 0.3691 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 9 | Software Engineer - Apollo Platform | Palantir | New York, NY | 0.32 | 0.4538 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 10 | Software Engineer, Agent Developer Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 11 | Software Engineer II, Full Stack - Global Servicing Technology | American Express | Sunrise, FL, United States | 0.3717 | 0.4537 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 12 | Infrastructure Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.4365 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 13 | AI Engineer III - Agentic AI | American Express | New York, NY, United States / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus | 0.3322 | 0.4321 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 14 | Neurodivergent Fellowship | Palantir | New York, NY | 0.32 | 0.4321 | SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 15 | Forward Deployed Software Engineer - Warp Speed | Palantir | New York, NY | 0.32 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 16 | Software Engineer III - Java - Web Search Team | American Express | Phoenix, AZ, United States | 0.3211 | 0.431 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 17 | Forward Deployed AI Engineer | Palantir | New York, NY | 0.32 | 0.4093 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Backend Engineering, Python |
| 18 | Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 19 | Forward Deployed Infrastructure Engineer - US Government | Palantir | New York, NY | 0.32 | 0.4093 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 20 | Software Engineer - Developer Productivity | Palantir | New York, NY | 0.32 | 0.4093 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 21 | Software Engineer, Robotics & Autonomous Systems | ScaleAI | San Francisco, CA | 0.437 | 0.4092 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 22 | Software Engineer I, Service Network - Slack | Slack (Salesforce) | Washington - Seattle | 0.5446 | 0.4082 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 23 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2159 | 0.4082 | SWE_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 24 | Forward Deployed Engineer, RL Environments | Labelbox | San Francisco Bay Area | 0.3676 | 0.4082 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 25 | Software Engineer (Backend), Enterprise | ScaleAI | Budapest, Hungary | 0.3332 | 0.402 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 26 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5249 | 0.401 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 27 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.755 | 0.3911 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 28 | Software Engineer, Platform | ScaleAI | San Francisco, CA; New York, NY | 0.7099 | 0.3911 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, DevOps |
| 29 | Backend Engineer, Ops | Ramp | New York, NY (HQ) | 0.52 | 0.3876 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Java, Python |
| 30 | Software Engineer, Growth Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3876 | SWE_FULLTIME | Backend Engineering, Python, Go |
| 31 | Software Engineer, Full Stack | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, React |
| 32 | Platform Intelligence Engineer | Palantir | New York, NY | 0.32 | 0.3866 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Backend Engineering, Python |
| 33 | Applied AI Engineer | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 34 | Instructional Assistant (Cloud Systems Engineering) | Per Scholas | United States; United States | 0.3915 | 0.3865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 35 | Full-Stack Software Engineer (Backend Oriented) | Lendbuzz | Boston, MA | 0.32 | 0.3865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 36 | Forward Deployed Software Engineer - US Government | Palantir | Fayetteville, NC | 0.32 | 0.3865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 37 | Market Infrastructure Engineer | Base Power Company | Austin, TX | 0.52 | 0.3865 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 38 | Software Engineer, Robotics | ScaleAI | Mexico City, MX | 0.3274 | 0.3792 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, Cloud Infrastructure |
| 39 | Forward Deployed Software Engineer - Japan Government | Palantir | Tokyo, Japan | 0.32 | 0.3792 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 40 | Forward Deployed Software Engineer | Palantir | Dubai, United Arab Emirates | 0.32 | 0.3792 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Data Engineering |
| 41 | Forward Deployed Software Engineer | Palantir | Stockholm, Sweden | 0.32 | 0.3792 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Data Engineering |
| 42 | Forward Deployed Software Engineer | Palantir | Amsterdam, Netherlands | 0.32 | 0.3792 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 43 | Forward Deployed Software Engineer | Palantir | Tel Aviv, Israel | 0.32 | 0.3792 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 44 | Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.3782 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 45 | Software Engineer, Web Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.3693 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Go |
| 46 | Full-Stack Engineer, AI Data Platform | Labelbox | San Francisco Bay Area | 0.3608 | 0.3648 | FULLSTACK_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, React |
| 47 | Software Engineer, Growth & Monetization | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3648 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 48 | Cybersecurity Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.3638 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Data Engineering |
| 49 | Software Engineer - Hosted Model Infrastructure | Palantir | Palo Alto, CA | 0.3691 | 0.3638 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 50 | Data Engineering Instructor | Per Scholas | United States | 0.32 | 0.3638 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, AI Systems |
| 51 | Software Engineer - Environment Platform | Palantir | Seattle, WA | 0.32 | 0.3638 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 52 | Advanced Software Engineer | Honeywell | Atlanta, GA, United States | 0.3223 | 0.3628 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 53 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.5413 | 0.3565 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 54 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.3857 | 0.3565 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 55 | Software Engineer, Argentina | Ramp | Remote (Buenos Aires, Argentina) | 0.52 | 0.3565 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 56 | Software Engineer II | Appian | Chennai, India | 0.359 | 0.351 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 57 | Forward Deployed Engineer, GTM | Notion | San Francisco, California / New York, New York | 0.52 | 0.3476 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, SQL |
| 58 | Software Engineer, Trust | Notion | San Francisco, California / New York, New York | 0.52 | 0.3476 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 59 | Software Engineer, Product Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.3476 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Go |
| 60 |  Machine Learning Research Engineer, Agent Data Foundation - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.3466 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 61 | Machine Learning Research Engineer, Agents - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5272 | 0.3466 | ML_ENGINEER_FULLTIME | Machine Learning Research, Backend Engineering, Python |
| 62 | Forward Deployed Engineer, GenAI  | ScaleAI | San Francisco, CA; New York, NY | 0.4357 | 0.3466 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Python |
| 63 | Software Engineer, Core Product | Ramp | New York, NY (HQ) | 0.52 | 0.3432 | SWE_FULLTIME | Python, Go, Java |
| 64 | Forward Deployed Software Engineer - Japan Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.3431 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 65 | Forward Deployed Software Engineer - Intel | Palantir | Washington, D.C. | 0.32 | 0.3431 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 66 | Model Behavior Engineer | Notion | New York, New York / San Francisco, California | 0.52 | 0.3422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 67 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 68 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5141 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 69 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2087 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 70 | Software Engineer, AI Platforms | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3421 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, TypeScript |
| 71 | Neurodivergent Fellowship | Palantir | Washington, D.C. | 0.32 | 0.3421 | SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 72 | Forward Deployed Enablement Engineer - Customer Success | Palantir | Washington, D.C. | 0.32 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 73 | Forward Deployed Software Engineer - US Government | Palantir | San Diego, CA | 0.32 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Java |
| 74 | Forward Deployed Software Engineer - Korea Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 75 | Forward Deployed Software Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 76 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.3717 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 77 | Forward Deployed Software Engineer - Tactical Edge | Palantir | Washington, D.C. | 0.32 | 0.3411 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Backend Engineering |
| 78 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.3411 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 79 | Software Engineer - Apollo Platform | Palantir | Seattle, WA | 0.32 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 80 | Infrastructure Engineer - Early Career | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 81 | Forward Deployed Software Engineer - AUS Government | Palantir | Sydney, Australia | 0.32 | 0.3292 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 82 | Software Engineer II | American Express | Gurugram, HR, India | 0.5382 | 0.3282 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 83 | Software Engineer II | Appian | Chennai, India | 0.3766 | 0.3282 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 84 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.3249 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, PostgreSQL |
| 85 | Software Engineer - Frontend Developer Productivity | Palantir | New York, NY | 0.32 | 0.3205 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 86 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.52 | 0.3205 | SWE_FULLTIME | Java, Python |
| 87 | Software Engineer, Bill Pay & Procurement | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 88 | Software Engineer, Data Platform  | Ramp | New York, NY (HQ) | 0.52 | 0.3194 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering |
| 89 | Software Engineer, Engineering Platform | Ramp | New York, NY (HQ) | 0.52 | 0.3194 | SWE_FULLTIME | Cloud Infrastructure |
| 90 | Software Engineer, Stablecoin | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 91 | Software Engineer, Accounting | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 92 | Software Engineer, Fraud & Identity | Ramp | New York, NY (HQ) | 0.52 | 0.3194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 93 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3663 | 0.3193 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 94 | 2026 Raytheon Full Time - Software Engineer I - Andover, MA (Onsite) | RTX | US-MA-ANDOVER-AN0 ~ 366 Lowell St ~ BLDG AN0 | 0.3312 | 0.3193 | SWE_FULLTIME | Backend Engineering, DevOps, Java |
| 95 | Growth Intelligence Engineer (Ads & Revenue) | NewsBreak | Mountain View, California, United States | 0.3656 | 0.3193 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, SQL |
| 96 | Technical Instructor (AWS Machine Learning) | Per Scholas | United States | 0.2942 | 0.3193 | ML_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 97 | Machine Learning Scientist (Financial Scoring) | Lendbuzz | Boston, MA | 0.32 | 0.3193 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Data Engineering, Python |
| 98 | Instructional Assistant (Data Engineer) (3-6 month contract) | Per Scholas | Orlando, Florida, United States | 0.32 | 0.3193 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Backend Engineering, Python |
| 99 | Data Engineer | Base Power Company | Austin, TX | 0.52 | 0.3193 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 100 | Software Engineer - Fleet | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.3193 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 101 | Software Engineer II | Honeywell | Duluth, GA, United States | 0.3857 | 0.3183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 102 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.5377 | 0.3126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 103 | Senior AI Engineer I - Agentic AI | American Express | New York, NY, United States / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus / Charlotte Hybrid-600 Tryon | 0.4035 | 0.3126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 104 | Forward Deployed Software Engineer | Palantir | Seoul, South Korea | 0.32 | 0.3121 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Java |
| 105 | Forward Deployed Software Engineer | Palantir | Vilnius, Lithuania | 0.32 | 0.3121 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 106 | Software Engineer, Banking | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.52 | 0.3121 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 107 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.6725 | 0.3111 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 108 | HPC engineer | Honeywell | Bucuresti, Romania | 0.3203 | 0.3111 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 109 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Honolulu, HI | 0.32 | 0.3111 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 110 | Site Reliability Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.3111 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 111 | GTM Engineer | Greenhouse | British Columbia | 0.5275 | 0.3065 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 112 | AI Engineer III | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.3065 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 113 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.3065 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, AI Systems |
| 114 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.3055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 115 |  Senior Software Engineer,  Full-Stack – Scale GP | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.3022 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 116 | Machine Learning Systems Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.3022 | ML_ENGINEER_FULLTIME | Distributed Systems, Python |
| 117 | Software Engineer, AI Workflows | Notion | San Francisco, California / New York, New York | 0.52 | 0.3022 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Python |
| 118 | Senior Software Engineer, Data | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4621 | 0.2989 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 119 | Software Engineer, AI DevX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2977 | SWE_FULLTIME | Python |
| 120 | Software Engineer, Backend | Base Power Company | Austin, TX | 0.52 | 0.2976 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 121 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.6346 | 0.2966 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, Python |
| 122 | Software Engineer - Hosted Model Infrastructure | Palantir | Washington, D.C. | 0.3691 | 0.2966 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 123 | Consultant (Technical, Public Sector) | Appian | Atlanta, Georgia | 0.2733 | 0.2966 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 124 | Cybersecurity AI_ML Engineer | GM Financial | Irving, TX, United States / US - Arlington AOC I, TX | 0.3452 | 0.2966 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 125 | Software Engineer, Simulation | PlusAI | Santa Clara, CA | 0.3273 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 126 | Advanced Software Engineer | Honeywell | Acton, MA, United States | 0.3428 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 127 | Research Scientist I/II, AI for Process Engineering | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.2966 | ML_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Python |
| 128 | Research Engineer, Frontier Capabilities | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4995 | 0.2966 | ML_ENGINEER_FULLTIME | Distributed Systems, AI Systems, Python |
| 129 | Software Engineer, Tools & Services | Basis | United States | 0.3204 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 130 | Sales AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.4594 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, SQL |
| 131 | Software Engineer (Gen AI) | EarnIn | Mountain View, US | 0.4277 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 132 | Machine Learning Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3201 | 0.2966 | ML_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 133 | Software Engineer, Machine Learning | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2966 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 134 | QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.3295 | 0.2966 | SWE_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 135 | Software Engineering Instructor (Continuous)  | Per Scholas | Columbus, Ohio, United States | 0.1771 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, PostgreSQL |
| 136 | Software Engineer (C#/React) | Reply | Chicago, Illinois | 0.32 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, React |
| 137 | Software Engineer, C++ Middleware and Runtime Infrastructure | PlusAI | Santa Clara, CA | 0.32 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 138 | Forward Deployed Engineer - Mixed Reality | Palantir | Washington, D.C. | 0.32 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 139 | Embedded Software Engineer | Base Power Company | Austin, TX | 0.52 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 140 | Software Engineer, AI Forward Deployed | Ramp | San Francisco, CA / New York, NY (HQ) | 0.52 | 0.2966 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 141 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.52 | 0.2966 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 142 | AI Applications Engineer | Notion | San Francisco, California | 0.52 | 0.2966 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 143 | Forward Deployed Software Engineer | Palantir | Abu Dhabi, United Arab Emirates | 0.32 | 0.2904 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 144 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.326 | 0.2893 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 145 | Software Engr II | Honeywell | Shanghai, China | 0.3203 | 0.2883 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 146 | Cloud Engineer | Lendbuzz | Tel Aviv | 0.32 | 0.2883 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 147 | Senior Software Engineer, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3879 | 0.2858 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 148 | Senior Software Engineer, Substrate | Palantir | New York, NY | 0.32 | 0.2853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 149 | Sr Advanced Cloud Developer | Honeywell | Mason, OH, United States | 0.3204 | 0.2852 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 150 | Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.2848 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 151 | Forward Deployed Software Engineer | Palantir | London, United Kingdom | 0.32 | 0.2848 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 152 | Software Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2838 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 153 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2838 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 154 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2838 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, AI Systems |
| 155 | Production Engineer - Database Operations | Palantir | London, United Kingdom | 0.3203 | 0.2838 | DEVOPS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 156 | Développeur(se) Logiciel de Plateforme, Outils de développement IA | MaintainX | Montreal, Canada | 0.32 | 0.2838 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 157 | Platform Developer, AI Builder  | MaintainX | Canada/United States | 0.32 | 0.2838 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 158 | Intermediate Software Engineer (Backend Engineering) | Achievers | Toronto | 0.4 | 0.2838 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 159 | Support AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.7152 | 0.2749 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 160 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.5382 | 0.2749 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 161 | Manufacturing Applications and Controls Engineer (Onsite) | RTX | US-ME-NORTH BERWICK-113 ~ 113 Wells St ~ WELLS, Rte 9 | 0.476 | 0.2749 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 162 | Data Scientist, Core Data -  PhD (2026) | Figma | San Francisco, CA • New York, NY | 0.4137 | 0.2749 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 163 | SWE Fellow - Human Frontier Collective (US) | ScaleAI | United States | 0.3201 | 0.2749 | SWE_FULLTIME | Research, Python, Java |
| 164 | Integration Developer  | MaintainX | Miami, Florida | 0.32 | 0.2749 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript, React |
| 165 | Business Systems Applications Developer | CesiumAstro | Austin, TX | 0.32 | 0.2749 | SWE_FULLTIME | Backend Engineering, SQL, Python |
| 166 | Forward Deployed Engineer | Labelbox | San Francisco Bay Area | 0.3676 | 0.2749 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, SQL |
| 167 | Application Security Engineer | Palantir | Washington, D.C. | 0.32 | 0.2749 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, Java |
| 168 | Application Security Engineer, AI Security | Notion | San Francisco, California | 0.52 | 0.2749 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, Go |
| 169 | Software Engineer, Security | Notion | San Francisco, California | 0.52 | 0.2749 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Python, Go |
| 170 | Data Engineer, People Analytics  | Notion | San Francisco, California | 0.52 | 0.2749 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 171 | Experienced Software Configuration Management Specialist | Boeing | USA - Tukwila, WA | 0.3942 | 0.2739 | SWE_FULLTIME | Cloud Infrastructure, DevOps |
| 172 | Experienced Software Engineer | Boeing | USA - Hazelwood, MO | 0.3829 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering |
| 173 | Software Engineer - Edge | Palantir | Washington, D.C. | 0.32 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 174 | High Performance Computing (HPC) Engineer | GenBio AI | Palo Alto, CA | 0.32 | 0.2739 | SWE_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 175 | Associate Application Engineer | Appian | McLean, Virginia | 0.359 | 0.2676 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL, Java |
| 176 | Analyst - Data Science | American Express | Singapore, Singapore | 0.2418 | 0.2676 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 177 | Développeur(se) Full-Stack intermédiaire  | MaintainX | Montréal | 0.32 | 0.2676 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, React |
| 178 | Forward Deployed Engineer, GTM, France | Notion | Paris, France | 0.52 | 0.2676 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, SQL |
| 179 | Forward Deployed Engineer, GTM - Japan | Notion | Tokyo, Japan  | 0.52 | 0.2676 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, TypeScript |
| 180 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.697 | 0.2666 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, DevOps, Python |
| 181 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4797 | 0.2666 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 182 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4981 | 0.2666 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 183 | Software Control Engr I (C++, SQL, Automation) | Honeywell | Mexico | 0.4549 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 184 | Consultant | Appian | Seville, Spain | 0.359 | 0.2666 | SWE_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 185 | Consultant (Top Secret Clearance, Software Implementation) | Appian | McLean, Virginia | 0.359 | 0.2666 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 186 | Consultant (Software Implementation, Public Sector) | Appian | McLean, Virginia | 0.359 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, SQL |
| 187 | Software Engineer I - Metrics for Release Implementation | Torc Robotics | Remote, US | 0.2905 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 188 | Software Engineer I - Device Drivers | Torc Robotics | Ann Arbor, MI | 0.2833 | 0.2666 | SWE_FULLTIME | Backend Engineering, DevOps, Python |
| 189 | Software Engineer - Distributed Simulation Systems | Astera Institute | Emeryville HQ | 0.52 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Backend Engineering, Python |
| 190 | Sr Software Engineer II - Global Commercial Services | American Express | FL, United States / Sunrise Campus / New York-Amex Tower WFC-35 Hr / AEDR Desert Ridge OB2-McDowell | 0.3322 | 0.2625 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, TypeScript |
| 191 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 192 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 193 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 194 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4775 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 195 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.3223 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 196 | Software Engr I | Honeywell | Pune City, Maharashtra, India | 0.3211 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 197 | Senior Software Engineer | Wealth.com | Hybrid, New York, Tempe, San Francisco | 0.52 | 0.2619 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 198 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3952 | 0.2611 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 199 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2611 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 200 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3204 | 0.2611 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 201 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2611 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, DevOps |
| 202 | DevOps Specialist | MaintainX | Montreal, Toronto | 0.32 | 0.2611 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 203 | Forward Deployed Infrastructure Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2611 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 204 | Software Engineer, Developer Experience | Notion | Hyderabad, India | 0.52 | 0.2611 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 205 | Senior Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.3452 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Distributed Systems |
| 206 | Senior Software Engineer, Prenatal | BillionToOne | Menlo Park, CA | 0.4432 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 207 | Senior Software Engineer - Internal Tools & Productivity | ScaleAI | San Francisco, CA | 0.5141 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 208 | Senior Software Engineer, App | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4165 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 209 | Senior Software Engineer, Applied AI | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4385 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 210 | Senior Software Engineer II - Amex Ads | American Express | New York, NY, United States | 0.3322 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 211 | Senior Software Engineer, Operations Research | Lila Sciences | Cambridge, MA USA | 0.4661 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 212 | Software Engineer, Developer Experience | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 213 | Software Engineer, Robotics | ScaleAI | Argentina; Uruguay | 0.3201 | 0.2542 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 214 | Forward Deployed Engineer - MTS | Context | San Francisco Office | 0.52 | 0.2532 | SWE_FULLTIME | Python, SQL, Java |
| 215 | Senior IT Architect | Honeywell | Bucuresti, Romania | 0.3606 | 0.253 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 216 | Computing Architect (Manhattan Warehouse M.S.) | Boeing | USA - Hialeah, FL | 0.4881 | 0.2522 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 217 | Mid-Level Programmer Analyst | Boeing | USA - Saint Charles, MO | 0.2575 | 0.2522 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 218 | Machine Learning Engineer, Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.2522 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 219 | Machine Learning Engineer - LLM, AI & Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.2522 | ML_ENGINEER_FULLTIME | AI Systems, Python, LLM |
| 220 | Machine Learning Engineer | True Anomaly | Denver, CO or Long Beach, CA | 0.2967 | 0.2522 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 221 | Software Engineer I, Instrument Software  | Lila Sciences | Cambridge, MA USA | 0.2804 | 0.2522 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 222 | Machine Learning Scientist I/II, Scientific Reasoning | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.2522 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 223 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2522 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 224 | Scientific Software Engineer- Shuttle Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2522 | SWE_FULLTIME | Backend Engineering, Python |
| 225 | Scientific Software Engineer - Compiler | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2522 | SWE_FULLTIME | Backend Engineering, Python |
| 226 | Scientific Software Engineer - Virtual Machine & Emulation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2522 | SWE_FULLTIME | Distributed Systems, Python |
| 227 | Software Engineer - Core Interfaces | Palantir | Palo Alto, CA | 0.32 | 0.2522 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript |
| 228 | ML Platform Engineer | Foxglove | San Francisco, CA | 0.52 | 0.2522 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 229 | Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.2522 | SWE_FULLTIME | Distributed Systems, Python |
| 230 | Algorithms Engineer | Base Power Company | Austin, TX | 0.52 | 0.2522 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 231 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.638 | 0.2483 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 232 | Senior AI Infrastructure Engineer, Model Serving Platform | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2483 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 233 | Senior Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.2462 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Java, Python |
| 234 | Senior Data Engineers | American Express | New York, NY, United States | 0.3276 | 0.2456 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 235 | Senior Software Engineers | American Express | New York, NY, United States | 0.3202 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 236 | Senior Software Engineer - Observability | Palantir | New York, NY | 0.32 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, Java |
| 237 | Senior Software Engineer - AI/ML | Wealth.com | New York, New York | 0.52 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 238 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.2456 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 239 | Senior AI Data Infrastructure/Pipeline Engineer | XPENG | Santa Clara, CA | 0.5536 | 0.2455 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 240 | Equipment & Tooling Software Engineer (Associate, Experienced and/or Senior) | Boeing | USA - North Charleston, SC | 0.3555 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 241 | Software Engineer, Distributed Systems | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, Backend Engineering |
| 242 | Sr. QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.4105 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 243 | Senior Software Developer - Data Engineering-2 | Boeing | USA - Seattle, WA | 0.4782 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 244 | Lead Software Architect - EPMS Systems | Honeywell | Atlanta, GA, United States | 0.3276 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 245 | Sr Software Engineer - Core Backend & Platform Engineering | Basis | United States | 0.32 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 246 | Software Engineer, Data Infrastructure | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 247 | Senior Infrastructure Engineer | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 248 | Application Engineer | Appian | McLean, Virginia | 0.3784 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL, PostgreSQL |
| 249 | Workday Integrations & Data Architect | EarnIn | Remote, Mexico | 0.36 | 0.2449 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 250 | Analytics Engineer | Podium | Lehi, Utah | 0.3202 | 0.2449 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, SQL, Python |
| 251 | Data Engineer | Lendbuzz | Tel Aviv | 0.3201 | 0.2449 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 252 | Bioinformatics Data Engineer | GenBio AI | Abu Dhabi | 0.32 | 0.2449 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 253 | Software Engineer II - MCU Applications (C++/Linux) | Torc Robotics | Ann Arbor, MI | 0.3371 | 0.2439 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 254 | Software Engineer, Production Engineering | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.2439 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 255 | Lead Software Engineer (Kubernetes) | Appian | McLean, Virginia | 0.514 | 0.2406 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 256 | Forward Deployed Software Engineer - AUS Government | Palantir | Canberra, Australia | 0.32 | 0.2404 | SWE_FULLTIME | Full Stack Development, Java, Python |
| 257 | Software Engineer I | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.455 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 258 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3857 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 259 | Chemical Engr II | Honeywell | Gurugram, Haryana, India | 0.3296 | 0.2393 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, AI Systems, SQL |
| 260 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.326 | 0.2393 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, DevOps, Python |
| 261 | Développeuse / Développeur d'intégration | MaintainX | Montreal, Toronto | 0.32 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 262 | Full-Stack Developer - IAM | MaintainX | Toronto | 0.32 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 263 | Software Engineer, AI Product (London, United Kingdom) | Figma | London, England | 0.32 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, React |
| 264 | Platform Engineer - Identity and Access Management (IAM) | Palantir | London, United Kingdom | 0.32 | 0.2393 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 265 | Forward Deployed Software Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2393 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 266 | Software Engineer, Infrastructure  | Notion | Hyderabad, India | 0.52 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Go |
| 267 | Software Engineer, Data Infrastructure | Notion | Hyderabad, India | 0.52 | 0.2393 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 268 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2383 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, Distributed Systems |
| 269 | Intermediate Software Engineer | Achievers | Canada | 0.3565 | 0.2383 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 270 | Software Engineer - Apollo Platform | Palantir | London, United Kingdom | 0.32 | 0.2383 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 271 | Experienced Software Engineer- FSD | Boeing | IND - Bangalore, India | 0.4551 | 0.2378 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 272 | Senior Software Engineer, GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2352 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, TypeScript |
| 273 | Senior Software Engineer / GTM Platform, Backend | Ramp | New York, NY (HQ) | 0.52 | 0.2326 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, PostgreSQL, Python |
| 274 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Python |
| 275 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Python |
| 276 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Python |
| 277 | Lead Software Development Engineer | iSpot | Bellevue, WA | 0.3647 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 278 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.5382 | 0.232 | SWE_FULLTIME | AI Systems, Machine Learning Research, Python |
| 279 | Sr Software Engineer - Global Commercial Services | American Express | New York, NY, United States / AEDR Desert Ridge CSB - Sierra | 0.352 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 280 | Senior Software Engineer, AI/ML (Infrastructure & Platform) | Wealth.com | New York, New York | 0.52 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 281 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | New York | 0.52 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, PostgreSQL |
| 282 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 283 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5381 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 284 | Experienced Software Engineer, Developer | Boeing | USA - Seal Beach, CA | 0.3296 | 0.2319 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 285 | Senior Software Engineer, Scientific System of Record | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4561 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 286 | Senior Compliance Automation Engineer | True Anomaly | Denver, CO or Long Beach, CA or SF Bay area, CA or Washington, DC | 0.3729 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 287 | Software Development Engineer - Gen AI | GM Financial | Irving, TX, United States / US - Arlington, TX | 0.3203 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 288 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | San Francisco | 0.52 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 289 | Senior Software Engineer, Substrate | Palantir | Washington, D.C. | 0.32 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 290 | Senior Software Engineer, Network Infrastructure | Palantir | Washington, D.C. | 0.32 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 291 | Senior Software Engineer, Substrate | Palantir | Seattle, WA | 0.32 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 292 | Senior Software Engineer, Network Infrastructure | Palantir | Seattle, WA | 0.32 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 293 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.4203 | 0.2305 | SWE_FULLTIME | Java, Python |
| 294 | AI Strategy Consultant, Frontier Tech | ScaleAI | San Francisco, CA | 0.3201 | 0.2305 | ML_ENGINEER_FULLTIME | Python, SQL |
| 295 | Software Engineer II - Test | RTX | US-AZ-TUCSON-805 ~ 1151 E Hermans Rd ~ BLDG 805 | 0.3636 | 0.2294 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 296 | Software Engineer I, QA | True Anomaly | Denver, CO or Long Beach, CA | 0.2857 | 0.2294 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | DevOps |
| 297 | Software Engineer | Boeing | USA - Maryland Heights, MO | 0.3153 | 0.2294 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 298 | Associate Software Engineer | Boeing | USA - Maryland Heights, MO | 0.2611 | 0.2294 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 299 | Scientific Software Engineer — Emulation & Application | QuEra Computing | Boston, MA, USA | 0.3505 | 0.2294 | SWE_FULLTIME | Backend Engineering |
| 300 | Senior Software Engineer - Java / AWS Services | Appian | McLean, Virginia | 0.359 | 0.2269 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 301 | Sr Advanced Software Engr | Honeywell | Singapore, Singapore, Singapore | 0.3296 | 0.2269 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 302 | Senior, ML Engineer - ML Ops Framework  | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5181 | 0.2269 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 303 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.6294 | 0.2222 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 304 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5851 | 0.2222 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 305 | Experienced Java Software Engineer | Boeing | POL - Gdansk, Poland | 0.5382 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 306 | Application Engr II | Honeywell | Tianjin, China | 0.4915 | 0.2222 | ML_ENGINEER_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | AI Systems, Python |
| 307 | Growth Marketing Developer (Desenvolvedor de Growth Marketing) -  São Paulo  (Hybrid | Clara | Latin America  | 0.3287 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 308 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Mexico City (Hybrid) | Clara | Latin America  | 0.3287 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 309 | Forward-deployed Engineer - LatAm (Remote) | Clara | Latin America  | 0.3287 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 310 | Forward-deployed Engineer - LatAm (Remote) | Clara | São Paulo, São Paulo, Brazil | 0.3287 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 311 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Bogotá (Hybrid) | Clara | Latin America  | 0.3287 | 0.2222 | SWE_FULLTIME | Full Stack Development, SQL |
| 312 | Scientific Software Engineer - Shuttle Compilation  | QuEra Computing | Tsukuba, Japan | 0.32 | 0.2222 | SWE_FULLTIME | Backend Engineering, Python |
| 313 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Tsukuba, Japan | 0.32 | 0.2222 | SWE_FULLTIME | Backend Engineering, Python |
| 314 | Scientific Software Engineer - Compiler | QuEra Computing | Tsukuba, Japan | 0.32 | 0.2222 | SWE_FULLTIME | Backend Engineering, Python |
| 315 | Intermediate AI/ML Engineer | Solink | Ottawa Office | 0.52 | 0.2222 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 316 | Machine Learning Researcher - Springtail | Astera Institute | Emeryville HQ | 0.52 | 0.2222 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 317 | AI Engineer, Agent Platform | NewsBreak | Mountain View, California, United States | 0.3771 | 0.2189 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 318 | Senior Software Engineer, Network Infrastructure | Palantir | New York, NY | 0.32 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 319 | Java Software Engineer (Associate, Experienced or Senior) - Bixby | Boeing | USA - Seal Beach, CA | 0.4178 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 320 | Sr Advanced AI Platform Engineer | Honeywell | Atlanta, GA, United States | 0.3218 | 0.2183 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, Cloud Infrastructure |
| 321 | Senior Software Engineer, ML Research | Lila Sciences | Cambridge, MA USA | 0.3852 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 322 | Software Engineer, ML Infra | NewsBreak | Mountain View, California, United States | 0.4295 | 0.2183 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 323 | Data Engineer | Clarity Innovations | Herndon, VA and/or Columbia, MD | 0.4038 | 0.2177 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 324 | Lead Software Engineer | Reply | Atlanta, Georgia | 0.3201 | 0.2177 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 325 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 326 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 327 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 328 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 329 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.538 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 330 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 331 | Application Engr II | Honeywell | Chennai, Tamil Nadu, India | 0.3247 | 0.2176 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 332 | Intermediate Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.2176 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, React |
| 333 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.52 | 0.2176 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, SQL |
| 334 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.2166 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 335 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4917 | 0.2166 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 336 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.2166 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 337 | Cloud Developer II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.2166 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 338 | Software Engr II - C++ Development, QT | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2166 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 339 | Développeur(se) Logiciel de Plateforme | MaintainX | Montreal, Quebec  | 0.32 | 0.2166 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, TypeScript |
| 340 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5695 | 0.2139 | BACKEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 341 | Senior Software Developer, Core Applications | Solink | Ottawa Office | 0.52 | 0.2139 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 342 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.6542 | 0.2133 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 343 | Lead Software Application – Architect | Boeing | IND - Bangalore, India | 0.4553 | 0.2106 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 344 | Senior AI Engineer I | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.2106 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 345 | Senior Software Engineer | Appian | Chennai, India | 0.3769 | 0.2106 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 346 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.2106 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 347 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.2106 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 348 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7493 | 0.208 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Data Engineering, Python |
| 349 | Lead Software Engineer - Firmware | Honeywell | Pittsford, NY, United States | 0.4921 | 0.208 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 350 | ML Research Engineer, ML Systems | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.4502 | 0.208 | ML_ENGINEER_FULLTIME | Distributed Systems, AI Systems, Python |
| 351 | Software Engr II | Honeywell | Atlanta, GA, United States | 0.2402 | 0.2077 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | React |
| 352 | Quantum Calibration Engineer, Quantum Computing Services | QuEra Computing | Boston, MA, USA | 0.3295 | 0.2077 | ML_ENGINEER_FULLTIME | Python |
| 353 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.2077 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Python |
| 354 | Applied ML Engineer | Foxglove | San Francisco, CA | 0.52 | 0.2077 | ML_ENGINEER_FULLTIME | Python |
| 355 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.2058 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, Django |
| 356 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5382 | 0.2052 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 357 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.2052 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 358 | Senior Data Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.2052 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, PostgreSQL |
| 359 | Sr Software Engineer - Basis Platform / DSP | Basis | United States | 0.32 | 0.2052 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 360 | Software Engineer, Code Platform | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2052 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 361 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 362 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 363 | Software Engineer III - MFT Business Enablement - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 364 | Senior Backend Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.455 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 365 | Senior Software Engineer, Digital Banking & Payments | American Express | Phoenix, AZ, United States | 0.3857 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 366 | Advanced AI Engineer | Honeywell | Charlotte, NC, United States | 0.3214 | 0.2046 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Cloud Infrastructure, DevOps |
| 367 | Application Engr II | Honeywell | Chongqing, China | 0.3247 | 0.2005 | SWE_FULLTIME | Java, TypeScript |
| 368 | Developer Advocate (Tokyo, Japan) | Figma | Tokyo, Japan | 0.32 | 0.2005 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 369 | Software Engineer, Guest Travel | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Denver, CO | 0.52 | 0.2005 | SWE_FULLTIME | Java, Python |
| 370 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.659 | 0.2003 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 371 | Senior Software Engineer | Appian | McLean, Virginia | 0.359 | 0.2003 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 372 | Développeur logiciel senior, facturation | MaintainX | Montréal | 0.32 | 0.2003 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 373 | Senior Platform Engineer  | Clarity Innovations | Required  | 0.6497 | 0.1997 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 374 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI | 0.6276 | 0.1994 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems |
| 375 | AI Prompt Engineer | Appian | McLean, Virginia | 0.359 | 0.1994 | SWE_FULLTIME | AI Systems |
| 376 | Application Programmer | EarnIn | Remote, US | 0.2601 | 0.1994 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 377 | Project Engr I | Honeywell | Tianjin, China | 0.3214 | 0.1994 | SWE_FULLTIME | Backend Engineering |
| 378 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3201 | 0.1975 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, AI Systems |
| 379 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4914 | 0.1969 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 380 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3717 | 0.1969 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 381 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3398 | 0.1969 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 382 | Full-Stack Developer, Connected Data  | MaintainX | Montréal, Toronto | 0.32 | 0.1969 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 383 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5377 | 0.1949 | SWE_FULLTIME | Backend Engineering, Java, SQL |
| 384 | GTM Engineer | Greenhouse | Ontario | 0.5276 | 0.1949 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript, Python |
| 385 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4916 | 0.1949 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 386 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.1949 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python, Java |
| 387 | Advanced Software Engineer -AI R&D | Honeywell | North Ryde, New South Wales, Australia | 0.3322 | 0.1949 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 388 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1949 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 389 | Strategic Projects Lead - Coding | ScaleAI | India | 0.3204 | 0.1949 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 390 | SWE Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.1949 | SWE_FULLTIME | AI Systems, Python, Java |
| 391 | Integrations Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1949 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript, React |
| 392 | Application Security Engineer | Palantir | London, United Kingdom | 0.32 | 0.1949 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, Java |
| 393 | Forward Deployed Engineer | Nash | Australia | 0.52 | 0.1949 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python, SQL |
| 394 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5383 | 0.1939 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems |
| 395 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1939 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems |
| 396 | Project Engr II | Honeywell | Pune, Maharashtra, India | 0.3247 | 0.1939 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 397 | Senior Software Engineer / GTM Platform, Frontend | Ramp | New York, NY (HQ) | 0.52 | 0.1923 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 398 | Senior Software Engineer (Frontend Focus) | Kira | New York | 0.52 | 0.1923 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 399 | Senior Software Engineer / Web + Design | Ramp | New York, NY (HQ) | 0.52 | 0.1923 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 400 | Senior Full Stack Engineer | EarnIn | Mountain View, US | 0.4891 | 0.1922 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, React, TypeScript |
| 401 | Data Engineer-ETL Tools & Python/ Python frameworks | American Express | Phoenix, AZ, United States | 0.3857 | 0.1916 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 402 | Senior Consultant (Public Sector) | Appian | Denver, Colorado | 0.3209 | 0.1916 | SWE_FULLTIME | Backend Engineering, Full Stack Development, SQL |
| 403 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.1916 | SWE_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 404 | Senior AI Engineer I | BillionToOne | Menlo Park, CA | 0.4123 | 0.1916 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 405 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.3276 | 0.1916 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 406 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.3276 | 0.1916 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 407 | ML Systems Engineer, Robotics | ScaleAI | San Francisco, CA | 0.5275 | 0.1916 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 408 | Machine Learning Engineer II / Senior Machine Learning Engineer I, Physical Sciences | Lila Sciences | Cambridge, MA USA | 0.3547 | 0.1916 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 409 | Sr Oracle Application Developer | GM Financial | Irving, TX, United States | 0.3203 | 0.1916 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 410 | AI Applied Scientist | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1916 | ML_ENGINEER_FULLTIME | AI Systems, Machine Learning Research, Python |
| 411 | Senior Backend Engineer | Nash | San Francisco | 0.52 | 0.1916 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 412 | Senior Platform Engineer | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.1916 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Go |
| 413 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 414 | Lead Architect, S4 Integration | Honeywell | Charlotte, NC, United States | 0.3716 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 415 | Lead IT Architect ORACLE HCM (Integration Cloud) | Honeywell | Charlotte, NC, United States | 0.3204 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 416 | Salesforce Sr IT Architect – Customer and Commercial Experience (CCEX) | Honeywell | Charlotte, NC, United States | 0.3203 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 417 | Lead Software Engineer | Reply | Chicago, Illinois | 0.3201 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, DevOps |
| 418 |  Senior SDET - Tooling Engineer | EarnIn | Mountain View, US | 0.4086 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 419 | Software Engineer, Production Engineering | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.191 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 420 | Senior Machine Learning Infrastructure Engineer | PlusAI | Santa Clara, CA | 0.32 | 0.191 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 421 | Lead Software Engineer | Appian | McLean, Virginia | 0.514 | 0.1872 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Java |
| 422 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.5066 | 0.1872 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Go |
| 423 | Senior Software Engineer - Java /  Hibernate | Appian | McLean, Virginia | 0.359 | 0.1872 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Java |
| 424 | Founding Engineer | Icon | New York / Remote | 0.52 | 0.1872 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 425 | Advanced Software Engineer | Honeywell | Gdansk, Pomorskie, Poland | 0.3606 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 426 | Senior Software Engineer - Database Platform | Appian | McLean, Virginia | 0.359 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 427 | Senior Autonomy Software Systems Engineer (Python / C++ / Data) | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3351 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 428 | Edge Infrastructure Engineer | Palantir | Warsaw, Poland | 0.32 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 429 | Senior, ML Engineer - ML Ops Framework | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5181 | 0.1866 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 430 | Intermediate Quality Assurance Engineer | Honeywell | Salem, OR, United States | 0.3619 | 0.185 | SWE_FULLTIME | — |
| 431 | Mixed Reality Developer | Palantir | Washington, D.C. | 0.32 | 0.185 | SWE_FULLTIME | — |
| 432 | Software Engineer, Product | Base Power Company | Austin, TX | 0.52 | 0.185 | SWE_FULLTIME | — |
| 433 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4553 | 0.1845 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 434 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.1839 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, AI Systems |
| 435 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.5385 | 0.1839 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 436 | Senior AI Engineer II | American Express | LONDON, LONDON, United Kingdom / Sussex House | 0.3857 | 0.1839 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 437 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1839 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 438 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1839 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 439 | Senior Software Engineer - Live Pay | EarnIn | Vancouver, Canada | 0.4769 | 0.1839 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 440 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3276 | 0.1839 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 441 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.1839 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 442 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.1833 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 443 | Lead Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.1833 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 444 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.1833 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 445 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.7386 | 0.1786 | ML_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 446 | Data Engineer, AI/ML III/IV | Zone 5 Technologies | United States | 0.5184 | 0.1786 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, TypeScript, React |
| 447 | Senior Technical Consultant | Appian | Boston, Massachusetts | 0.3209 | 0.1786 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 448 | Senior Identity Security Engineer | Palantir | Palo Alto, CA | 0.3318 | 0.1786 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Java, Go |
| 449 | Advanced Software Engineer | Honeywell | Pittsburgh, PA, United States | 0.3223 | 0.1786 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 450 | Senior Software Engineer - API Experience | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.1786 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Go |
| 451 | Senior Consultant (Public Sector) | Appian | Atlanta, Georgia | 0.3209 | 0.178 | SWE_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 452 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 453 | Lead Data Engineer | Honeywell | Atlanta, GA, United States | 0.326 | 0.178 | DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Python |
| 454 | Senior Simulation Engineer I/II, Robotics | Lila Sciences | Cambridge, MA USA | 0.4105 | 0.178 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 455 | Advanced Software Engineer - Cybersecurity | Honeywell | Duluth, GA, United States | 0.3204 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 456 | Software Engineers | American Express | Phoenix, AZ, United States | 0.3202 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 457 | Data Platform Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.178 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 458 | Applied Research Engineer, Agents | Labelbox | San Francisco Bay Area | 0.52 | 0.178 | ML_ENGINEER_FULLTIME | AI Systems, Research, Python |
| 459 | Senior Software Engineer, Mapping & Localization | PlusAI | Santa Clara, CA | 0.32 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 460 | Sr. Site Development Engineer | Mariana Minerals | San Francisco HQ | 0.52 | 0.178 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 461 | Senior Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.178 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 462 | Appian Product Engineer  | Appian | McLean, Virginia | 0.584 | 0.1777 | SWE_FULLTIME | SQL |
| 463 | Mobile Engineer, Android | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.1777 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | Java |
| 464 | Software Engineer, Developer and Qualification Tools | d-Matrix | Santa Clara | 0.52 | 0.1777 | SWE_FULLTIME | Python |
| 465 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.538 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 466 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5827 | 0.1736 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 467 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5719 | 0.1736 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, SQL |
| 468 | Senior Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.1736 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Distributed Systems, Python |
| 469 | Senior Software Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.368 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 470 | Senior Software Engineer  | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.3685 | 0.1736 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 471 | Senior Consultant (Public Sector) | Appian | McLean, Virginia | 0.359 | 0.1736 | SWE_FULLTIME | Backend Engineering, Full Stack Development, SQL |
| 472 | Senior Backend Engineer — ClarOps (Ingeniero Backend Senior de ClarOps) - Remote | Clara | Latin America  | 0.3364 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 473 | Senior, ML Engineer - Auto Tagger | Torc Robotics | Ann Arbor, MI, Remote - US | 0.417 | 0.1736 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 474 | Senior AI Engineer - Agentic | Podium | Lehi, Utah, Open to Remote | 0.32 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Go |
| 475 | Senior Software Engineer I, Client Connections | EnergyHub | Remote - United States | 0.3295 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 476 | Senior Full Stack Developer, Data Integrations | Solink | Ottawa Office | 0.52 | 0.1736 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, Python |
| 477 | Cloud Architect | RTX | Warminster, Wiltshire | 0.3858 | 0.173 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, DevOps |
| 478 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.5384 | 0.1722 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, SQL |
| 479 | Frontier Agents Engineer | ScaleAI | London, UK | 0.4003 | 0.1722 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 480 | Machine Learning Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.1722 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 481 | Machine Learning Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.1722 | ML_ENGINEER_FULLTIME | Data Engineering, Python |
| 482 | Measurement Software Engineer | Axiomatic AI | Toronto, Canada | 0.32 | 0.1722 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 483 | Scientific Software Engineer  | QuEra Computing | Toronto, Ontario, Canada | 0.32 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 484 | Scientific Software Engineer - Compiler | QuEra Computing | Harwell, England, UK | 0.2998 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 485 | AI/ML Engineer | Melotech | Berlin / New York / London | 0.52 | 0.1722 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 486 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4552 | 0.1709 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 487 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.1709 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Backend Engineering, Java |
| 488 | Senior Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1709 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 489 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.5381 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 490 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.5307 | 0.1703 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Distributed Systems |
| 491 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4913 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 492 | Senior Data Engineer | EarnIn | Bengaluru, India | 0.3577 | 0.1703 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 493 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 494 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.1703 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 495 | Senior Software Engineer (Backend Engineering) ⭐ | Achievers | Toronto | 0.32 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 496 | Senior Data Developer - Streaming | MaintainX | Montreal, Toronto | 0.32 | 0.1703 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 497 | Senior Data Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1703 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 498 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4915 | 0.1697 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 499 | Senior Software Engineer, Substrate | Palantir | London, United Kingdom | 0.32 | 0.1697 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 500 | Software Engineer, C++ | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1655 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React, Go |
| 501 | Data Scientist (Data Science) | Boeing | USA - Everett, WA | 0.4501 | 0.1649 | ML_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 502 | Sr. AI Data Analyst-Agentic Systems & GenAI | GM Financial | Irving, TX, United States / US - Burnett, TX | 0.3452 | 0.1649 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 503 | Senior Machine Learning Engineer, Recommendation & AI Applications | NewsBreak | Mountain View, California, United States | 0.4486 | 0.1649 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, Java |
| 504 | Data Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.1649 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 505 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.52 | 0.1649 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 506 | Senior SAP FIORI Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.1643 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 507 | Senior Software Security Engineer | Boeing | USA - Seattle, WA | 0.6548 | 0.1643 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 508 | Cloud Application Deployment and Migration Specialist (Mid-Level, Senior or Lead) **Sign on Bonus Potential** | Boeing | USA - Berkeley, MO | 0.5431 | 0.1643 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 509 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.5219 | 0.1643 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 510 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.516 | 0.1643 | SWE_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 511 | Service Now Sys Administrator | RTX | US-TX-REMOTE | 0.4761 | 0.1643 | SWE_FULLTIME | Cloud Infrastructure, DevOps |
| 512 | Azure Cloud Architect | Reply | Chicago, Illinois | 0.32 | 0.1643 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 513 | Azure Cloud Architect | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.1643 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 514 | Senior Technical Consultant | Appian | Madison, Wisconsin | 0.3209 | 0.1606 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 515 | Senior Software Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.1606 | SWE_FULLTIME | Backend Engineering, Java, PostgreSQL |
| 516 | Senior Software Engineer - Operating System | Torc Robotics | Ann Arbor, MI | 0.5232 | 0.16 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Python |
| 517 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5635 | 0.16 | ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 518 | Senior Consultant (Top Secret Clearance) | Appian | McLean, Virginia | 0.359 | 0.16 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 519 | Senior Technical Consultant | Appian | McLean, Virginia | 0.359 | 0.16 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 520 | Senior Consultant | Appian | Tokyo, Japan | 0.359 | 0.16 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 521 | Senior Consultant (Public Sector) | Appian | Raleigh, North Carolina | 0.3209 | 0.16 | SWE_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 522 | Senior, Software Engineer - Cloud Automation | Torc Robotics | Ann Arbor, MI, Remote - US | 0.3216 | 0.16 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 523 | Senior, Software Engineer - Release Pipelines | Torc Robotics | Ann Arbor, MI ;Remote - US | 0.3808 | 0.16 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 524 | Senior Applied Scientist, Scheduling and Optimization | MaintainX | Canada (Remote) | 0.32 | 0.16 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 525 | Senior Quality Engineer I | American Express | Chennai, TN, India | 0.4917 | 0.1572 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 526 | Senior or Lead Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1572 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 527 | Sr Advanced SW Architect | Honeywell | India | 0.3856 | 0.1566 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 528 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1566 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 529 | Senior Software Developer, Compliance and Multi-Region | MaintainX | Montreal, Toronto  | 0.32 | 0.1566 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 530 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.6658 | 0.1513 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python |
| 531 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4917 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 532 | Senior AI Engineer II - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.3857 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 533 | Advanced Software Engineer | Honeywell | Raleigh, NC, United States | 0.3716 | 0.1513 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 534 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.1513 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 535 | Senior Machine Learning Engineer - Foundation Model | XPENG | Santa Clara, CA | 0.5216 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 536 | Senior Machine Learning Engineer - AI Foundation | XPENG | Santa Clara, CA | 0.5216 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 537 | Lead AI Engineer | Honeywell | Atlanta, GA, United States | 0.3203 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 538 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1513 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python |
| 539 | Senior Computer Vision/AI  Engineer | BrightAI | Palo Alto, CA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 540 | Senior Machine Learning Engineer II | CesiumAstro | Austin, TX | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Python |
| 541 | Senior Research Engineer, Controls | PlusAI | Santa Clara, CA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 542 | Senior Software Engineer, Planning | PlusAI | Santa Clara, CA | 0.32 | 0.1513 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Distributed Systems, Python |
| 543 | Senior AI Engineer | Reply | Seattle, Washington | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 544 | Senior AI Engineer, Time-Series Signal Processing | BrightAI | Palo Alto, CA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 545 | Senior AI Engineer – LLM, RAG | BrightAI | Palo Alto, CA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python, LLM |
| 546 | Senior AI Engineer | Reply | Chicago, Illinois | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 547 | Senior AI Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 548 | Senior Machine Learning Engineer, Perception | PlusAI | Santa Clara, CA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 549 | Senior Machine Learning Engineer, Simulation | PlusAI | Santa Clara, CA | 0.32 | 0.1513 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, data pipelines |
| 550 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.1505 | SWE_FULLTIME | Python, Java |
| 551 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.1505 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Java, SQL |
| 552 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.1505 | SWE_FULLTIME | Python, Java |
| 553 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5381 | 0.1505 | SWE_FULLTIME | Python, Java |
| 554 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5379 | 0.1505 | SWE_FULLTIME | Java, Python |
| 555 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1505 | SWE_FULLTIME | Python, Java |
| 556 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.2496 | 0.1505 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python, Java |
| 557 | Application Engr II | Honeywell | Pune, Maharashtra, India | 0.3218 | 0.1505 | SWE_FULLTIME | Java, TypeScript |
| 558 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.1494 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 559 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.5238 | 0.1494 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | DevOps |
| 560 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.5118 | 0.1494 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering |
| 561 | Software Engineer In Test - Android | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 562 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6285 | 0.1469 | ML_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 563 | Sr Advanced AI Data Engineer | Honeywell | Monterrey, NLE, Mexico | 0.3218 | 0.1469 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 564 | Senior Data Infrastructure Engineer | Voltus | Remote | 0.3213 | 0.1469 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 565 | Développeur(se) Full-Stack sénior ou en chef  | MaintainX | Montréal | 0.32 | 0.1469 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | Full Stack Development, TypeScript, React |
| 566 | Azure Cloud Architect | Reply | Detroit Area, Michigan | 0.32 | 0.1463 | SWE_FULLTIME | Cloud Infrastructure, Backend Engineering |
| 567 | Senior .NET Developer | Nuclear Promise X | Chalk River | 0.52 | 0.1463 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 568 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4913 | 0.1436 | SWE_FULLTIME | Backend Engineering, AI Systems, Java |
| 569 | Sr. Machine Learning Engineer | EarnIn | Bengaluru, India | 0.3978 | 0.1436 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Python |
| 570 | Senior Test Automation Engineer | Appian | Chennai, India | 0.359 | 0.1436 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 571 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3519 | 0.1436 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 572 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1436 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, DevOps, Python |
| 573 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1436 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, AI Systems, Python |
| 574 | Advanced Data Engineer - GCP | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1436 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 575 | Senior Software Developer, Billing  | MaintainX | Montreal, Toronto | 0.32 | 0.1436 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 576 | Senior Runtime Software Engineer   | d-Matrix | Sydney | 0.52 | 0.1436 | SWE_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 577 | Senior Data Engineer | Super.com | Canada / United States | 0.52 | 0.1436 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 578 | Sr Software Eng Supervisor | Honeywell | India | 0.5381 | 0.143 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 579 | Sr IT Database Administrator | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.143 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 580 | Software Engineer, Production Engineering  (London, United Kingdom) | Figma | London, England | 0.32 | 0.143 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Distributed Systems, Cloud Infrastructure |
| 581 | Senior Software Engineer, Front End | True Anomaly | Denver, CO or Long Beach, CA | 0.4886 | 0.1383 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 582 | Senior Front End Engineer | EarnIn | Mountain View, US | 0.4891 | 0.1383 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript |
| 583 | Sr. Software Engineer, React/ React Native | Prosper | San Francisco, CA | 0.32 | 0.1383 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript |
| 584 |  Senior Software Engineer, Visualization | Foxglove | San Francisco, CA | 0.52 | 0.1383 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 585 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.6418 | 0.1377 | DATA_ENGINEER_FULLTIME | Data Engineering |
| 586 | Senior Integration Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.1377 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 587 | Senior Embedded Software Engineer II | CesiumAstro | Westminster, CO | 0.3313 | 0.1377 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 588 | Senior Embedded Software Integration Engineer | PlusAI | Chicago, IL | 0.32 | 0.1377 | SWE_FULLTIME | Backend Engineering |
| 589 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.7039 | 0.1333 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Python |
| 590 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.1333 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 591 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.1333 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 592 | Developpeur SAP ABAP  /  SAP ABAP Developer | RTX | CA-QC-LONGUEUIL-J01 ~ 1000 Blvd Marie-Victorin ~ J01 BLDG | 0.3858 | 0.1333 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 593 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5639 | 0.1333 | ML_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 594 | Senior Applied Scientist, Parts Intelligence & Inventory Optimization | MaintainX | Canada (Remote) | 0.3599 | 0.1333 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 595 | Senior Applied Machine Learning Engineer, Asset Intelligence | MaintainX | San Francisco (Remote) | 0.3581 | 0.1333 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 596 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Remote - US, Ann Arbor, MI | 0.4657 | 0.1333 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 597 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Montreal, Canada, Remote - Canada | 0.4293 | 0.1333 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 598 | Senior Software Engineer, Calibration | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3853 | 0.1333 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 599 | Senior Software Engineer, Calibration | Torc Robotics | Remote - Canada, Montreal, Canada | 0.3253 | 0.1333 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 600 | Senior Software Engineer (PHP/ Golang) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.1333 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Go |
| 601 | Applied AI Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.1306 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python, TypeScript |
| 602 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.5385 | 0.13 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Data Engineering, Python |
| 603 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.5381 | 0.13 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 604 | Senior Consultant | Appian | Chennai, India | 0.3905 | 0.13 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Data Engineering, SQL |
| 605 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.13 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 606 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.13 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 607 | Software Engr II | Honeywell | India | 0.352 | 0.13 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 608 | Advanced Chemical Engr (Digital Exec Tools Specialist’) | Honeywell | India | 0.3218 | 0.13 | ML_ENGINEER_FULLTIME | DevOps, Data Engineering, Python |
| 609 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.13 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 610 | Advanced Data Engineer | Honeywell | Pune, Maharashtra, India | 0.3202 | 0.13 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 611 | Développeur(se) de logiciel senior spécialisé en moteurs de recherche | MaintainX | Montréal, Toronto | 0.32 | 0.13 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 612 | Senior AI Developer (Coming Soon!) | Nuclear Promise X | Canada | 0.52 | 0.13 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 613 | Senior QA Engineer | Super.com | Canada / United States | 0.52 | 0.13 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 614 | Advanced SW Test Engineer (m/f/d) | Honeywell | Ratingen, Nordrhein-Westfalen, Germany | 0.5381 | 0.1277 | SWE_FULLTIME | Python |
| 615 | Application Engr I | Honeywell | Chennai, Tamil Nadu, India | 0.3223 | 0.1277 | SWE_FULLTIME | Python |
| 616 | Machine Learning Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.2401 | 0.1277 | ML_ENGINEER_FULLTIME | Python |
| 617 | Forward Deployed AI Engineer | Palantir | London, United Kingdom | 0.32 | 0.1277 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 618 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.508 | 0.1246 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 619 | Engineer II /Senior Software Engineer, Simulation | Lila Sciences | Cambridge, MA USA | 0.3486 | 0.1246 | SWE_FULLTIME | Python |
| 620 | Scientist/Sr. Scientist, AI Safety | Lila Sciences | Cambridge, MA USA; London, UK; San Francisco, CA USA | 0.5204 | 0.1246 | ML_ENGINEER_FULLTIME | Python |
| 621 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1246 | SWE_FULLTIME | TypeScript |
| 622 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1246 | SWE_FULLTIME | TypeScript |
| 623 | Senior Software Engineer - Vehicle Diagnostics | Torc Robotics | Ann Arbor, MI, Remote, US | 0.3808 | 0.1197 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 624 | Senior Data Engineer | Reply | Kochi, Kerala | 0.32 | 0.1197 | DATA_ENGINEER_FULLTIME | Data Engineering |
| 625 | Senior .NET Developer (Coming Soon!) | Nuclear Promise X | Ontario / Remote | 0.52 | 0.1197 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 626 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.5384 | 0.1169 | DATA_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, SQL, Python |
| 627 | SWE Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.3201 | 0.1169 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 628 | Senior Data Developer, Governance  | MaintainX | Montreal, Toronto | 0.32 | 0.1169 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 629 | Senior IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 630 | Sr IT Architect | Honeywell | Pune City, Maharashtra, India | 0.4915 | 0.1163 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 631 | Advanced Embedded Engineer | Honeywell | United Kingdom | 0.3717 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 632 | Sr IT Engineer | Honeywell | Hyderabad, Telangana, India | 0.3716 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps |
| 633 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.1163 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 634 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3237 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering |
| 635 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.1163 | SWE_FULLTIME | DevOps, Cloud Infrastructure |
| 636 | Senior Mobile Engineer (Android) | EarnIn | Mountain View, US | 0.727 | 0.111 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 637 | Senior Software Engineer, iOS | NewsBreak | Mountain View, California, United States | 0.439 | 0.111 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 638 | Senior Mobile Security Engineer (Forensics) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.1066 | MOBILE_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 639 | Senior React Native Engineer — Driver App  | Nash | Remote HQ / San Francisco | 0.52 | 0.1066 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | TypeScript |
| 640 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.105 | SWE_FULLTIME | — |
| 641 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.105 | SWE_FULLTIME | — |
| 642 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.105 | SWE_FULLTIME | — |
| 643 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.105 | SWE_FULLTIME | — |
| 644 | Software Engineer In Test - iOS | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.105 | SWE_FULLTIME | — |
| 645 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.105 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | — |
| 646 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.1033 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 647 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1033 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 648 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4918 | 0.1033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 649 | Senior Associate - Oracle Technical Developer | American Express | Gurugram, HR, India | 0.3717 | 0.1033 | SWE_FULLTIME | Backend Engineering, SQL |
| 650 | Senior Technical Consultant | Appian | Toronto, Canada | 0.359 | 0.1033 | SWE_FULLTIME | Backend Engineering, SQL |
| 651 | Sr Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3322 | 0.1033 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 652 | Senior Software Engineer | EarnIn | Bengaluru, India | 0.3201 | 0.1033 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript |
| 653 | Développeur(euse) de données sénior, gouvernance des données | MaintainX | Montréal, Toronto | 0.32 | 0.1033 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL |
| 654 | Développeur de données senior | MaintainX | Montreal, Toronto | 0.32 | 0.1033 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, SQL, data pipelines |
| 655 | Senior iOS Engineer | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.093 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 656 | Senior UX Design Engineer, Design Systems | Greenhouse | Ontario | 0.4975 | 0.0903 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript |
| 657 | Software Machine Learning Test Engineer - Sr Engineer | d-Matrix | Bangalore | 0.52 | 0.0903 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Python, Java |
| 658 | Senior Software Developer, Search  | MaintainX | Montreal, Toronto | 0.32 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems |
| 659 | Senior Software Engineers | Achievers | Toronto | 0.32 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 660 | Senior Software Engineer—Kernels | d-Matrix | Bangalore | 0.52 | 0.0897 | SWE_FULLTIME | Backend Engineering |
| 661 | Senior Front End Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.0766 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript |
| 662 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.063 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
