# User Recommendation Results

Generated 2026-06-12 14:23 UTC after v5 domain taxonomy enrichment (6,348 recommendation-eligible active jobs, 6,361 active normalized rows, 8,540 archived identities, 81 active companies; domain filter enabled, Tier 1+2 business pools, gemini-3.1-flash-lite).

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
| Ram Parekh | 672 | 0.105–0.5687 | 28 | `SWE_FULLTIME`, `DATA_SCIENTIST_FULLTIME`, `ML_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME` |
| Yatharth Mogra | 646 | 0.045–0.5664 | 103 | `DATA_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME` |

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

- **Total jobs matching subscribed pools (after filters):** 672
- **Notification-eligible jobs (≤60d, not yet emailed):** 500
- **Personal score range:** 0.105 – 0.5687 (28 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 540 |
| `BACKEND_ENGINEER_FULLTIME` | 340 |
| `ML_ENGINEER_FULLTIME` | 137 |
| `DATA_ENGINEER_FULLTIME` | 65 |
| `FULLSTACK_ENGINEER_FULLTIME` | 65 |
| `DEVOPS_ENGINEER_FULLTIME` | 63 |
| `FRONTEND_ENGINEER_FULLTIME` | 48 |
| `DATA_SCIENTIST_FULLTIME` | 35 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 27 |
| `SECURITY_ENGINEER_FULLTIME` | 14 |
| `MOBILE_ENGINEER_FULLTIME` | 12 |
| `DATA_ANALYST_FULLTIME` | 6 |
| `SUPPORT_ENGINEER_FULLTIME` | 4 |
| `PRODUCT_MANAGER_FULLTIME` | 3 |

### Email notification — top 4 (personalized)

#### #1 — Data Scientist @ Ramp

- **Location:** New York, NY (HQ) | San Francisco, CA | Remote (US) (unclear)
- **Posted:** —
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.52
- **Personal score:** 0.5687
- **Pools:** `DATA_SCIENTIST_FULLTIME`
- **Roles:** DATA_SCIENTIST
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering
- **Skills:** predictive modeling, statistical analysis
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering, Python, SQL
- **URL:** https://jobs.ashbyhq.com/ramp/e577622f-6657-4e53-8941-b3a774b04448

#### #2 — Software Engineer II @ American Express

- **Location:** Gurugram, HR, India (unclear)
- **Posted:** 2026-06-10T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5382
- **Personal score:** 0.5375
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, DATA_ENGINEER, ML_ENGINEER
- **Capabilities:** Backend Engineering, Data Engineering, Machine Learning, Distributed Systems, Cloud Infrastructure
- **Skills:** distributed systems, event-driven architecture, CI/CD, prompt engineering
- **Match reasons:** Data Engineering, Machine Learning, Cloud Infrastructure, Python, BigQuery
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26008666/details

#### #3 — Software Engineer, Machine Learning @ Figma

- **Location:** San Francisco, CA • New York, NY • United States (unclear)
- **Posted:** 2026-04-15T19:32:40+00:00
- **Salary:** 153000 – 376000
- **Effort:** MEDIUM
- **Opportunity score:** 0.52
- **Personal score:** 0.5062
- **Pools:** `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME`
- **Roles:** ML_ENGINEER, SWE
- **Capabilities:** Machine Learning, Data Engineering, Cloud Infrastructure
- **Skills:** applied machine learning, search relevance
- **Match reasons:** Machine Learning, Data Engineering, Cloud Infrastructure, Python
- **URL:** https://boards.greenhouse.io/figma/jobs/5551532004?gh_jid=5551532004

#### #4 — Credit Risk Expert (Experto/a en Riesgo de Credito)  @ Clara

- **Location:** Latin America  (unclear)
- **Posted:** 2026-05-28T20:38:08+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.3318
- **Personal score:** 0.4688
- **Pools:** `DATA_SCIENTIST_FULLTIME`
- **Roles:** DATA_SCIENTIST
- **Capabilities:** Machine Learning, Data Engineering
- **Skills:** Credit Risk, Statistical Modeling
- **Match reasons:** Machine Learning, Data Engineering, Python, SQL, R
- **URL:** https://job-boards.greenhouse.io/clara/jobs/4764183007

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Data Scientist | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.52 | 0.5687 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 2 | Software Engineer II | American Express | Gurugram, HR, India | 0.5382 | 0.5375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 3 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3952 | 0.5062 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 4 | Software Engineer, Machine Learning | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.5062 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 5 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.4688 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 6 | Data Scientist, Core Data -  PhD (2026) | Figma | San Francisco, CA • New York, NY | 0.4137 | 0.4688 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, SQL |
| 7 | Credit Risk Expert (Experto/a en Riesgo de Credito)  | Clara | Latin America  | 0.3318 | 0.4688 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 8 | Growth Intelligence Engineer (Ads & Revenue) | NewsBreak | Mountain View, California, United States | 0.3656 | 0.4688 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 9 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.326 | 0.4688 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 10 | Data Scientist II | Honeywell | Pune City, Maharashtra, India | 0.3247 | 0.4688 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 11 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.4688 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 12 |  Research Data Scientist 1 | iSpot | Bellevue, WA | 0.2365 | 0.4688 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 13 | Data Scientist   | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.4688 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 14 | Scientist - Ensemble Structural Informatics | Astera Institute | Emeryville HQ | 0.52 | 0.4688 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 15 | Cybersecurity Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.4375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 16 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4916 | 0.4375 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 17 | Associate-Digital Product Management (SQL, Hadoop, Hive) | American Express | Gurugram, HR, India | 0.4262 | 0.4375 | PRODUCT_MANAGER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 18 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.4375 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 19 | Chemical Engr II | Honeywell | Gurugram, Haryana, India | 0.3296 | 0.4375 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 20 | Junior Data Scientist | Clara | Latin America  | 0.3287 | 0.4375 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 21 | Technical Instructor (AWS Machine Learning) | Per Scholas | United States | 0.2942 | 0.4375 | ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 22 | Strategic Projects Lead - Coding | ScaleAI | India | 0.3204 | 0.4375 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 23 | Software Engineer, AI Platforms | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4375 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 24 | Machine Learning Scientist (Financial Scoring) | Lendbuzz | Boston, MA | 0.32 | 0.4375 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 25 | Data Engineering Instructor | Per Scholas | United States | 0.32 | 0.4375 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 26 | Data Scientist | Achievers | Toronto | 0.32 | 0.4375 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 27 | Data Engineer | Base Power Company | Austin, TX | 0.52 | 0.4375 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 28 | Market Operations Engineer | Base Power Company | Austin, TX | 0.52 | 0.4375 | SWE_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 29 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.755 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 30 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.6346 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 31 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.5384 | 0.4063 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 32 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 33 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4797 | 0.4063 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 34 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 35 | Software Engineer - Hosted Model Infrastructure | Palantir | Washington, D.C. | 0.3691 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 36 | Software Engineer - Hosted Model Infrastructure | Palantir | New York, NY | 0.3691 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 37 | Software Engineer - Hosted Model Infrastructure | Palantir | Palo Alto, CA | 0.3691 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 38 | Software Engineer, Robotics | ScaleAI | Mexico City, MX | 0.3274 | 0.4063 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 39 |  Machine Learning Research Engineer, Agent Data Foundation - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.4063 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 40 | Forward Deployed Engineer, GenAI  | ScaleAI | San Francisco, CA; New York, NY | 0.4357 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 41 | Full-Stack Engineer, AI Data Platform | Labelbox | San Francisco Bay Area | 0.3608 | 0.4063 | FULLSTACK_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 42 | Cloud Developer II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, SQL |
| 43 | Production Engineer - Database Operations | Palantir | London, United Kingdom | 0.3203 | 0.4063 | DEVOPS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 44 | Machine Learning Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.4063 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 45 | Intermediate Software Engineer (Backend Engineering) | Achievers | Toronto | 0.4 | 0.4063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 46 | ML Platform Engineer | Foxglove | San Francisco, CA | 0.52 | 0.4063 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 47 | Software Engineer, AI Forward Deployed | Ramp | San Francisco, CA / New York, NY (HQ) | 0.52 | 0.4063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 48 | Frontier Agents Engineer | ScaleAI | London, UK | 0.4003 | 0.3688 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Pandas |
| 49 | Data Scientist I | Honeywell | Bengaluru, Karnataka, India | 0.352 | 0.3688 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, R |
| 50 | Analyst - Data Science | American Express | Singapore, Singapore | 0.2418 | 0.3688 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 51 | Quantum Calibration Engineer, Quantum Computing Services | QuEra Computing | Boston, MA, USA | 0.3295 | 0.3688 | ML_ENGINEER_FULLTIME | Machine Learning, Python, NumPy |
| 52 | Data Scientist, Marketing | Figma | San Francisco, CA • New York, NY • United States | 0.8543 | 0.3412 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 53 | Support AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.7152 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 54 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.5382 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 55 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4775 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 56 | Workday Integrations & Data Architect | EarnIn | Remote, Mexico | 0.36 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 57 | Cybersecurity AI_ML Engineer | GM Financial | Irving, TX, United States / US - Arlington AOC I, TX | 0.3452 | 0.3375 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, pandas |
| 58 | Advanced Software Engineer -AI R&D | Honeywell | North Ryde, New South Wales, Australia | 0.3322 | 0.3375 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 59 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5141 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 60 | Infrastructure Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 61 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.3223 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 62 | Software Engineer II, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3318 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 63 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MySQL |
| 64 | Analytics Engineer | Podium | Lehi, Utah | 0.3202 | 0.3375 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, SQL, Python |
| 65 | Data Engineer | Lendbuzz | Tel Aviv | 0.3201 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 66 | AI Strategy Consultant, Frontier Tech | ScaleAI | San Francisco, CA | 0.3201 | 0.3375 | ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 67 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | New York, NY | 0.3201 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 68 | Forward Deployed Engineer | Labelbox | San Francisco Bay Area | 0.3676 | 0.3375 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, SQL |
| 69 | Instructional Assistant (Data Engineer) (3-6 month contract) | Per Scholas | Orlando, Florida, United States | 0.32 | 0.3375 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, SQL |
| 70 | Forward Deployed Software Engineer - US Government | Palantir | Fayetteville, NC | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 71 | Forward Deployed Enablement Engineer - Customer Success | Palantir | Washington, D.C. | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 72 | Forward Deployed Software Engineer - Japan Government | Palantir | Tokyo, Japan | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 73 | Forward Deployed Software Engineer - Warp Speed | Palantir | New York, NY | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 74 | Forward Deployed Software Engineer - Korea Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 75 | Forward Deployed Software Engineer - AUS Government | Palantir | Sydney, Australia | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 76 | Forward Deployed Software Engineer | Palantir | Dubai, United Arab Emirates | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 77 | Forward Deployed AI Engineer | Palantir | New York, NY | 0.32 | 0.3375 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, SQL |
| 78 | Backend Software Engineer - Infrastructure, Foundations | Palantir | New York, NY | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 79 | Forward Deployed Software Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.3375 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 80 | Forward Deployed Software Engineer | Palantir | Seoul, South Korea | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 81 | Forward Deployed Software Engineer | Palantir | Stockholm, Sweden | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 82 | Forward Deployed Software Engineer - US Government | Palantir | New York, NY | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 83 | Forward Deployed Software Engineer | Palantir | Amsterdam, Netherlands | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 84 | Forward Deployed Software Engineer | Palantir | Tel Aviv, Israel | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 85 | Forward Deployed Software Engineer | Palantir | London, United Kingdom | 0.32 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 86 | Software Engineer, Credit | Ramp | New York, NY (HQ) | 0.52 | 0.3375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 87 | Software Engineer, Data Infrastructure | Notion | Hyderabad, India | 0.52 | 0.3375 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 88 | Data Engineer, People Analytics  | Notion | San Francisco, California | 0.52 | 0.3375 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 89 | Software Engineer, Data Infrastructure | Notion | Hyderabad, India | 0.52 | 0.3375 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 90 | Advanced Data Engineer - GCP | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.3225 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 91 | Sr Advanced AI Platform Engineer | Honeywell | Atlanta, GA, United States | 0.3218 | 0.3225 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 92 | Senior, ML Engineer - Auto Tagger | Torc Robotics | Ann Arbor, MI, Remote - US | 0.417 | 0.3225 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 93 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.6725 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 94 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.6294 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 95 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5851 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 96 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5249 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 97 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.5413 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 98 | GTM Engineer | Greenhouse | British Columbia | 0.5275 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 99 | Software Engineer I, Service Network - Slack | Slack (Salesforce) | Washington - Seattle | 0.5446 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 100 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4916 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 101 | Application Engr II | Honeywell | Tianjin, China | 0.4915 | 0.3063 | ML_ENGINEER_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Machine Learning, Python |
| 102 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4981 | 0.3063 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 103 | Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 104 | AI Engineer III | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.3063 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 105 | Software Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 106 | Instructional Assistant (Cloud Systems Engineering) | Per Scholas | United States; United States | 0.3915 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 107 | Software Engineer II | Appian | Chennai, India | 0.3766 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 108 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.3717 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 109 | Software Engineer II, Full Stack - Global Servicing Technology | American Express | Sunrise, FL, United States | 0.3717 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 110 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.3063 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 111 | Consultant | Appian | Seville, Spain | 0.359 | 0.3063 | SWE_FULLTIME | Machine Learning, SQL |
| 112 | Software Engineer II | Appian | Chennai, India | 0.359 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 113 | Machine Learning Engineer, Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 114 | Machine Learning Engineer - LLM, AI & Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 115 | Software Engineer (Backend), Enterprise | ScaleAI | Budapest, Hungary | 0.3332 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 116 | AI Engineer III - Agentic AI | American Express | New York, NY, United States / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus | 0.3322 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 117 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2159 | 0.3063 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 118 | Machine Learning Systems Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 119 | Software Engineer, Robotics & Autonomous Systems | ScaleAI | San Francisco, CA | 0.437 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 120 | Machine Learning Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 121 | Software Engineer I - Metrics for Release Implementation | Torc Robotics | Remote, US | 0.2905 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 122 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.3063 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 123 | Advanced Software Engineer | Honeywell | Acton, MA, United States | 0.3428 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 124 | Machine Learning Engineer | True Anomaly | Denver, CO or Long Beach, CA | 0.2967 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python, Anomaly Detection |
| 125 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3204 | 0.3063 | SWE_FULLTIME | Cloud Infrastructure, SQL |
| 126 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2087 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 127 | Research Scientist I/II, AI for Process Engineering | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 128 | Machine Learning Scientist I/II, Scientific Reasoning | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 129 | Research Engineer, Frontier Capabilities | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4995 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 130 | Software Engr II | Honeywell | Shanghai, China | 0.3203 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 131 | Sales AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.4594 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, SQL, automation |
| 132 | HPC engineer | Honeywell | Bucuresti, Romania | 0.3203 | 0.3063 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 133 | Machine Learning Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.2401 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 134 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Honolulu, HI | 0.32 | 0.3063 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 135 | Software Engineer, Full Stack | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 136 | Platform Developer, AI Builder  | MaintainX | Canada/United States | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 137 | Développeur(se) Logiciel de Plateforme, Outils de développement IA | MaintainX | Montreal, Canada | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 138 | Measurement Software Engineer | Axiomatic AI | Toronto, Canada | 0.32 | 0.3063 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 139 | Forward Deployed Engineer, RL Environments | Labelbox | San Francisco Bay Area | 0.3676 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 140 | Forward Deployed Software Engineer - Tactical Edge | Palantir | Washington, D.C. | 0.32 | 0.3063 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 141 | Platform Intelligence Engineer | Palantir | New York, NY | 0.32 | 0.3063 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python |
| 142 | Forward Deployed Infrastructure Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.3063 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 143 | Forward Deployed Engineer - Mixed Reality | Palantir | Washington, D.C. | 0.32 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 144 | Forward Deployed AI Engineer | Palantir | London, United Kingdom | 0.32 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 145 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.3063 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 146 | Forward Deployed Infrastructure Engineer - US Government | Palantir | New York, NY | 0.32 | 0.3063 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 147 | Software Engineer - Developer Productivity | Palantir | New York, NY | 0.32 | 0.3063 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 148 | Data Science, Music & Audio | Melotech | Berlin / London / New York / Los Angeles / San Francisco | 0.52 | 0.3063 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 149 | AI/ML Engineer | Melotech | Berlin / New York / London | 0.52 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 150 | Applied ML Engineer | Foxglove | San Francisco, CA | 0.52 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 151 | Software Engineer, Web Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 152 | Intermediate AI/ML Engineer | Solink | Ottawa Office | 0.52 | 0.3063 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 153 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 154 | AI Applications Engineer | Notion | San Francisco, California | 0.52 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 155 | Infrastructure Engineer - Early Career | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.3063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, automation |
| 156 | Software Engineer, AI Workflows | Notion | San Francisco, California / New York, New York | 0.52 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 157 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.52 | 0.3063 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 158 | Applied AI Engineer | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 159 | Algorithms Engineer | Base Power Company | Austin, TX | 0.52 | 0.3063 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 160 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.3063 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 161 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5635 | 0.3037 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 162 | Sr Advanced Cloud Developer | Honeywell | Mason, OH, United States | 0.3204 | 0.3037 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 163 | Software Engineer, ML Infra | NewsBreak | Mountain View, California, United States | 0.4295 | 0.3037 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 164 | Data Platform Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3037 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 165 | Senior, ML Engineer - ML Ops Framework | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5181 | 0.3037 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 166 | Senior, ML Engineer - ML Ops Framework  | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5181 | 0.3037 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 167 | Senior IT Architect | Honeywell | Bucuresti, Romania | 0.3606 | 0.285 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Data Engineering |
| 168 | Sr. Data Analyst | EarnIn | Bengaluru, India | 0.3521 | 0.2812 | DATA_ANALYST_FULLTIME, DATA_SCIENTIST_FULLTIME | Analytics Engineering, Machine Learning, SQL |
| 169 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.2812 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 170 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.2812 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 171 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2812 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 172 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2812 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 173 | Senior Data Scientist, Growth  | Ramp | New York, NY (HQ) | 0.52 | 0.2812 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 174 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI | 0.6276 | 0.275 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning |
| 175 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 176 | Software Engineer, Platform | ScaleAI | San Francisco, CA; New York, NY | 0.7099 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 177 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.5118 | 0.275 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 178 | Experienced Software Configuration Management Specialist | Boeing | USA - Tukwila, WA | 0.3942 | 0.275 | SWE_FULLTIME | Cloud Infrastructure |
| 179 | Software Engineer II | Honeywell | Duluth, GA, United States | 0.3857 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 180 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3857 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 181 | Intermediate Software Engineer | Achievers | Canada | 0.3565 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 182 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.326 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 183 | Project Engr II | Honeywell | Pune, Maharashtra, India | 0.3247 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 184 | Advanced Software Engineer | Honeywell | Atlanta, GA, United States | 0.3223 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 185 | Software Engineer III - Java - Web Search Team | American Express | Phoenix, AZ, United States | 0.3211 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 186 | Développeur(se) Logiciel de Plateforme | MaintainX | Montreal, Quebec  | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 187 | DevOps Specialist | MaintainX | Montreal, Toronto | 0.32 | 0.275 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 188 | Software Engineer, AI Product (London, United Kingdom) | Figma | London, England | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 189 | Platform Engineer - Identity and Access Management (IAM) | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure |
| 190 | Cloud Engineer | Lendbuzz | Tel Aviv | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 191 | Software Engineer - Environment Platform | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 192 | High Performance Computing (HPC) Engineer | GenBio AI | Palo Alto, CA | 0.32 | 0.275 | SWE_FULLTIME | Cloud Infrastructure |
| 193 | Software Engineer - Apollo Platform | Palantir | London, United Kingdom | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 194 | Software Engineer - Apollo Platform | Palantir | New York, NY | 0.32 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 195 | Software Engineer - Apollo Platform | Palantir | Seattle, WA | 0.32 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 196 | Software Engineer, Infrastructure  | Notion | Hyderabad, India | 0.52 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 197 | Software Engineer, Production Engineering | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 198 | Software Engineer, Engineering Platform | Ramp | New York, NY (HQ) | 0.52 | 0.275 | SWE_FULLTIME | Cloud Infrastructure |
| 199 | Software Engineer, Developer Experience | Notion | Hyderabad, India | 0.52 | 0.275 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 200 | Software Engineer, Argentina | Ramp | Remote (Buenos Aires, Argentina) | 0.52 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 201 | Site Reliability Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.275 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 202 | Software Engineer, Data Platform  | Ramp | New York, NY (HQ) | 0.52 | 0.275 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering |
| 203 | Market Infrastructure Engineer | Base Power Company | Austin, TX | 0.52 | 0.275 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 204 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.659 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 205 | Advanced Data Scientist | Honeywell | Hyderabad, Telangana, India | 0.5971 | 0.2625 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 206 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.5385 | 0.2625 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Python |
| 207 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.5384 | 0.2625 | DATA_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, Machine Learning, SQL |
| 208 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.538 | 0.2625 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 209 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.5307 | 0.2625 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 210 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5827 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 211 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.4551 | 0.2625 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 212 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.2625 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Machine Learning, Python |
| 213 | Sr. Machine Learning Engineer | EarnIn | Bengaluru, India | 0.3978 | 0.2625 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 214 | Senior Software Developer - Data Engineering-2 | Boeing | USA - Seattle, WA | 0.4782 | 0.2625 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 215 | Senior Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.3717 | 0.2625 | DATA_ANALYST_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 216 | Senior Data Engineer | EarnIn | Bengaluru, India | 0.3577 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 217 | Senior Data Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 218 | Sr. AI Data Analyst-Agentic Systems & GenAI | GM Financial | Irving, TX, United States / US - Burnett, TX | 0.3452 | 0.2625 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 219 | Senior AI Engineer I | BillionToOne | Menlo Park, CA | 0.4123 | 0.2625 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 220 | Credit Policy Expert (Experto/a en política de Crédito) – LatAm | Clara | Latin America  | 0.3287 | 0.2625 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, SQL |
| 221 | Sr Advanced AI Data Engineer | Honeywell | Monterrey, NLE, Mexico | 0.3218 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 222 | Senior Software Engineer, Applied AI | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4385 | 0.2625 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 223 | Senior Data Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 224 | Software Engineer, Data Infrastructure | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2625 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 225 | Senior Data Engineer | Super.com | Canada / United States | 0.52 | 0.2625 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 226 | Senior Applied Scientist, Credit Risk | Ramp | New York, NY (HQ) | 0.52 | 0.2625 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 227 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7493 | 0.2438 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 228 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 229 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.5381 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 230 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 231 | Senior Product Data Scientist | MaintainX | Montreal, Toronto, Vancouver, SF (Remote) | 0.4453 | 0.2438 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 232 | Data Engineer, AI/ML III/IV | Zone 5 Technologies | United States | 0.5184 | 0.2438 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Analytics Engineering, Python |
| 233 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.5377 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 234 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4914 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 235 | Senior AI Engineer I - Agentic AI | American Express | New York, NY, United States / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus / Charlotte Hybrid-600 Tryon | 0.4035 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 236 | Senior AI Engineer II | American Express | LONDON, LONDON, United Kingdom / Sussex House | 0.3857 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 237 | Senior AI Engineer I | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.2438 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 238 | Senior AI Data Infrastructure/Pipeline Engineer | XPENG | Santa Clara, CA | 0.5536 | 0.2438 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 239 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5639 | 0.2438 | ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 240 | Senior Consultant | Appian | Tokyo, Japan | 0.359 | 0.2438 | SWE_FULLTIME | Machine Learning, Cloud Infrastructure, SQL |
| 241 | Software Engr II | Honeywell | India | 0.352 | 0.2438 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 242 | ML Systems Engineer, Robotics | ScaleAI | San Francisco, CA | 0.5275 | 0.2438 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 243 | Senior AI Infrastructure Engineer, Model Serving Platform | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 244 | Senior Software Engineer, Operations Research | Lila Sciences | Cambridge, MA USA | 0.4661 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 245 | Senior Software Engineer, Data | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4621 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 246 | Lead Data Engineer | Honeywell | Atlanta, GA, United States | 0.326 | 0.2438 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 247 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 248 | Advanced Chemical Engr (Digital Exec Tools Specialist’) | Honeywell | India | 0.3218 | 0.2438 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 249 | Lead Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 250 | Advanced AI Engineer | Honeywell | Charlotte, NC, United States | 0.3214 | 0.2438 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 251 | Machine Learning Engineer II / Senior Machine Learning Engineer I, Physical Sciences | Lila Sciences | Cambridge, MA USA | 0.3547 | 0.2438 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 252 | Software Development Engineer - Gen AI | GM Financial | Irving, TX, United States / US - Arlington, TX | 0.3203 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 253 | Sr IT Database Administrator | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2438 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, MySQL |
| 254 | Advanced Data Engineer | Honeywell | Pune, Maharashtra, India | 0.3202 | 0.2438 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 255 | Software Engineer, Robotics | ScaleAI | Argentina; Uruguay | 0.3201 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 256 | Senior Autonomy Software Systems Engineer (Python / C++ / Data) | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3351 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 257 | Senior Data Developer - Streaming | MaintainX | Montreal, Toronto | 0.32 | 0.2438 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 258 | Développeur de données senior | MaintainX | Montreal, Toronto | 0.32 | 0.2438 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 259 | Senior Machine Learning Engineer, Recommendation & AI Applications | NewsBreak | Mountain View, California, United States | 0.4486 | 0.2438 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 260 | Software Engineer, Code Platform | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 261 | Senior Research Engineer, Controls | PlusAI | Santa Clara, CA | 0.32 | 0.2438 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 262 | Senior Machine Learning Engineer, Simulation | PlusAI | Santa Clara, CA | 0.32 | 0.2438 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Data Engineering, Python |
| 263 | Senior Software Engineer, AI/ML (Infrastructure & Platform) | Wealth.com | New York, New York | 0.52 | 0.2438 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 264 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 265 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 266 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 267 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 268 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.538 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 269 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 270 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 271 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 272 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 273 | Associate Application Engineer | Appian | McLean, Virginia | 0.359 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Python, Data Modeling |
| 274 | Application Engr II | Honeywell | Chennai, Tamil Nadu, India | 0.3247 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 275 | Business Systems Applications Developer | CesiumAstro | Austin, TX | 0.32 | 0.2375 | SWE_FULLTIME | SQL, Python |
| 276 | Forward Deployed Software Engineer - US Government | Palantir | San Diego, CA | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 277 | Forward Deployed Software Engineer - Japan Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 278 | Forward Deployed Software Engineer - AUS Government | Palantir | Canberra, Australia | 0.32 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 279 | Forward Deployed Software Engineer | Palantir | Abu Dhabi, United Arab Emirates | 0.32 | 0.2375 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Python, SQL |
| 280 | Forward Deployed Software Engineer | Palantir | Vilnius, Lithuania | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 281 | Forward Deployed Software Engineer - Intel | Palantir | Washington, D.C. | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 282 | Forward Deployed Software Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 283 | Forward Deployed Software Engineer | Palantir | New York, NY | 0.32 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 284 | Software Engineer, Backend | Base Power Company | Austin, TX | 0.52 | 0.2375 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 285 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.52 | 0.2375 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 286 | Forward Deployed Engineer, GTM, France | Notion | Paris, France | 0.52 | 0.2375 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 287 | Forward Deployed Engineer, GTM | Notion | San Francisco, California / New York, New York | 0.52 | 0.2375 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 288 | Forward Deployed Engineer, GTM - Japan | Notion | Tokyo, Japan  | 0.52 | 0.2375 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 289 | Forward Deployed Engineer - MTS | Context | San Francisco Office | 0.52 | 0.2375 | SWE_FULLTIME | Python, SQL |
| 290 | Backend Engineer, Ops | Ramp | New York, NY (HQ) | 0.52 | 0.2375 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 291 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.52 | 0.2375 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 292 | Senior Technical Product Management Specialist | Boeing | USA - Seattle, WA | 0.5556 | 0.225 | PRODUCT_MANAGER_FULLTIME, DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering |
| 293 | Data Engineer | Clarity Innovations | Herndon, VA and/or Columbia, MD | 0.4038 | 0.225 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure |
| 294 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure |
| 295 | Senior Machine Learning Infrastructure Engineer | PlusAI | Santa Clara, CA | 0.32 | 0.225 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 296 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5969 | 0.2213 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, R |
| 297 | Data Scientist (Data Science) | Boeing | USA - Everett, WA | 0.4501 | 0.2213 | ML_ENGINEER_FULLTIME | Machine Learning, Python, R |
| 298 | Senior Applied Scientist, Parts Intelligence & Inventory Optimization | MaintainX | Canada (Remote) | 0.3599 | 0.2213 | ML_ENGINEER_FULLTIME | Machine Learning, Python, NumPy |
| 299 | Sr Data Scientist | GM Financial | Fort Worth, TX, United States | 0.3452 | 0.2213 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 300 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.697 | 0.2062 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 301 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.2062 | SWE_FULLTIME | Python |
| 302 | Appian Product Engineer  | Appian | McLean, Virginia | 0.584 | 0.2062 | SWE_FULLTIME | SQL |
| 303 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.2062 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | SQL |
| 304 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5381 | 0.2062 | SWE_FULLTIME | Python |
| 305 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.2062 | SWE_FULLTIME | Python |
| 306 | Advanced SW Test Engineer (m/f/d) | Honeywell | Ratingen, Nordrhein-Westfalen, Germany | 0.5381 | 0.2062 | SWE_FULLTIME | Python |
| 307 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5379 | 0.2062 | SWE_FULLTIME | Python |
| 308 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.2062 | SWE_FULLTIME | Python |
| 309 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5377 | 0.2062 | SWE_FULLTIME | SQL |
| 310 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.4203 | 0.2062 | SWE_FULLTIME | Python |
| 311 | GTM Engineer | Greenhouse | Ontario | 0.5276 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 312 | Computing Architect (Manhattan Warehouse M.S.) | Boeing | USA - Hialeah, FL | 0.4881 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 313 | Manufacturing Applications and Controls Engineer (Onsite) | RTX | US-ME-NORTH BERWICK-113 ~ 113 Wells St ~ WELLS, Rte 9 | 0.476 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 314 | Software Control Engr I (C++, SQL, Automation) | Honeywell | Mexico | 0.4549 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, automation |
| 315 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.3857 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 316 | Application Engineer | Appian | McLean, Virginia | 0.3784 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 317 | Consultant (Software Implementation, Public Sector) | Appian | McLean, Virginia | 0.359 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, data modeling |
| 318 | Consultant (Top Secret Clearance, Software Implementation) | Appian | McLean, Virginia | 0.359 | 0.2062 | SWE_FULLTIME | SQL, data modeling |
| 319 | Consultant (Technical, Public Sector) | Appian | Atlanta, Georgia | 0.2733 | 0.2062 | SWE_FULLTIME | SQL, data modeling |
| 320 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.2496 | 0.2062 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 321 | Growth Marketing Developer (Desenvolvedor de Growth Marketing) -  São Paulo  (Hybrid | Clara | Latin America  | 0.3287 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 322 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Mexico City (Hybrid) | Clara | Latin America  | 0.3287 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 323 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Bogotá (Hybrid) | Clara | Latin America  | 0.3287 | 0.2062 | SWE_FULLTIME | SQL |
| 324 | Software Engineer, Simulation | PlusAI | Santa Clara, CA | 0.3273 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 325 | Application Engr I | Honeywell | Chennai, Tamil Nadu, India | 0.3223 | 0.2062 | SWE_FULLTIME | Python |
| 326 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 327 | Software Engineer I, Instrument Software  | Lila Sciences | Cambridge, MA USA | 0.2804 | 0.2062 | SWE_FULLTIME | Python |
| 328 | Software Engineer, Tools & Services | Basis | United States | 0.3204 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 329 | Software Engr II - C++ Development, QT | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 330 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 331 | Software Engineer (Gen AI) | EarnIn | Mountain View, US | 0.4277 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 332 | SWE Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.2062 | SWE_FULLTIME | Python |
| 333 | Integration Developer  | MaintainX | Miami, Florida | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 334 | Integrations Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 335 | Développeuse / Développeur d'intégration | MaintainX | Montreal, Toronto | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 336 | Intermediate Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 337 | Développeur(se) Full-Stack intermédiaire  | MaintainX | Montréal | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 338 | Scientific Software Engineer - Shuttle Compilation  | QuEra Computing | Tsukuba, Japan | 0.32 | 0.2062 | SWE_FULLTIME | Python |
| 339 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Tsukuba, Japan | 0.32 | 0.2062 | SWE_FULLTIME | Python |
| 340 | Scientific Software Engineer - Compiler | QuEra Computing | Tsukuba, Japan | 0.32 | 0.2062 | SWE_FULLTIME | Python |
| 341 | QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.3295 | 0.2062 | SWE_FULLTIME | Python |
| 342 | Software Engineer I - Device Drivers | Torc Robotics | Ann Arbor, MI | 0.2833 | 0.2062 | SWE_FULLTIME | Python |
| 343 | Scientific Software Engineer  | QuEra Computing | Toronto, Ontario, Canada | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 344 | Scientific Software Engineer- Shuttle Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2062 | SWE_FULLTIME | Python |
| 345 | Scientific Software Engineer - Compiler | QuEra Computing | Harwell, England, UK | 0.2998 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 346 | Scientific Software Engineer - Virtual Machine & Emulation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2062 | SWE_FULLTIME | Python |
| 347 | Scientific Software Engineer - Compiler | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2062 | SWE_FULLTIME | Python |
| 348 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 349 | Full-Stack Software Engineer (Backend Oriented) | Lendbuzz | Boston, MA | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 350 | Neurodivergent Fellowship | Palantir | Washington, D.C. | 0.32 | 0.2062 | SWE_FULLTIME | Python |
| 351 | Neurodivergent Fellowship | Palantir | New York, NY | 0.32 | 0.2062 | SWE_FULLTIME | Python |
| 352 | Software Engineer, C++ Middleware and Runtime Infrastructure | PlusAI | Santa Clara, CA | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 353 | Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 354 | Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 355 | Application Security Engineer | Palantir | London, United Kingdom | 0.32 | 0.2062 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 356 | Application Security Engineer | Palantir | Washington, D.C. | 0.32 | 0.2062 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 357 | Software Engineer, Developer and Qualification Tools | d-Matrix | Santa Clara | 0.52 | 0.2062 | SWE_FULLTIME | Python, Automation |
| 358 | Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 359 | Software Engineer, Security | Notion | San Francisco, California | 0.52 | 0.2062 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 360 | Software Engineer, Trust | Notion | San Francisco, California / New York, New York | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 361 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 362 | Software Engineer - Distributed Simulation Systems | Astera Institute | Emeryville HQ | 0.52 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 363 | Software Engineer, Core Product | Ramp | New York, NY (HQ) | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 364 | Software Engineer, Guest Travel | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Denver, CO | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 365 | Software Engineer, Agent Developer Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 366 | Software Engineer, Growth Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 367 | Software Engineer - Fleet | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 368 | Software Engineer, AI DevX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2062 | SWE_FULLTIME | Python |
| 369 | Application Security Engineer, AI Security | Notion | San Francisco, California | 0.52 | 0.2062 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 370 | Software Engineer - Fleet | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 371 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6285 | 0.2025 | ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 372 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.7386 | 0.2025 | ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 373 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.5385 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 374 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 375 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5719 | 0.2025 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 376 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3717 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 377 | Equipment & Tooling Software Engineer (Associate, Experienced and/or Senior) | Boeing | USA - North Charleston, SC | 0.3555 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 378 | Senior Consultant (Public Sector) | Appian | McLean, Virginia | 0.359 | 0.2025 | SWE_FULLTIME | Machine Learning, SQL, Python |
| 379 | Senior Consultant (Public Sector) | Appian | Denver, Colorado | 0.3209 | 0.2025 | SWE_FULLTIME | Machine Learning, SQL, Python |
| 380 | Senior Technical Consultant | Appian | Madison, Wisconsin | 0.3209 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 381 | Senior Technical Consultant | Appian | Boston, Massachusetts | 0.3209 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 382 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3398 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 383 | Senior Data Engineers | American Express | New York, NY, United States | 0.3276 | 0.2025 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 384 |  Senior Software Engineer,  Full-Stack – Scale GP | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 385 | Senior Software Engineer, App | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4165 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 386 | Senior Software Engineer, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3879 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 387 | Advanced Software Engineer | Honeywell | Pittsburgh, PA, United States | 0.3223 | 0.2025 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 388 | Pricing Data Scientist | iHerb | United States of America - Irvine, California; United States of America - Remote / Home Office | 0.4008 | 0.2025 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 389 | Senior Data Infrastructure Engineer | Voltus | Remote | 0.3213 | 0.2025 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 390 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MySQL |
| 391 | Lead Software Development Engineer | iSpot | Bellevue, WA | 0.3647 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 392 | Senior Data Developer, Governance  | MaintainX | Montreal, Toronto | 0.32 | 0.2025 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 393 | Data Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.2025 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 394 | Senior Software Engineer - AI/ML | Wealth.com | New York, New York | 0.52 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 395 | Senior Software Developer, Core Applications | Solink | Ottawa Office | 0.52 | 0.2025 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 396 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.52 | 0.2025 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 397 | Senior Full Stack Developer, Data Integrations | Solink | Ottawa Office | 0.52 | 0.2025 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 398 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.1837 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 399 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.6658 | 0.1837 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 400 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5695 | 0.1837 | BACKEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 401 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.638 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 402 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5382 | 0.1837 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 403 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5381 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 404 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1837 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 405 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 406 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.1837 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 407 | Lead Software Engineer (Kubernetes) | Appian | McLean, Virginia | 0.514 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 408 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4917 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 409 | Software Engineer III - MFT Business Enablement - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 410 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4913 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 411 | Senior Consultant | Appian | Chennai, India | 0.3905 | 0.1837 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, SQL |
| 412 | Senior Software Engineer, Digital Banking & Payments | American Express | Phoenix, AZ, United States | 0.3857 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 413 | Senior AI Engineer II - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.3857 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 414 | Data Engineer-ETL Tools & Python/ Python frameworks | American Express | Phoenix, AZ, United States | 0.3857 | 0.1837 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, ETL |
| 415 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1837 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 416 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 417 | Senior Software Engineer | Appian | Chennai, India | 0.3769 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 418 | Senior Software Engineer  | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.3685 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 419 | Senior Software Engineer, Scientific System of Record | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4561 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 420 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 421 | Senior Software Engineer | Appian | McLean, Virginia | 0.359 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 422 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 423 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 424 | Senior Technical Consultant | Appian | Toronto, Canada | 0.359 | 0.1837 | SWE_FULLTIME | Machine Learning, SQL, data modeling |
| 425 | Senior Consultant (Public Sector) | Appian | Atlanta, Georgia | 0.3209 | 0.1837 | SWE_FULLTIME | Machine Learning, SQL |
| 426 | Senior Consultant (Public Sector) | Appian | Raleigh, North Carolina | 0.3209 | 0.1837 | SWE_FULLTIME | Machine Learning, SQL |
| 427 | Senior Applied Machine Learning Engineer, Asset Intelligence | MaintainX | San Francisco (Remote) | 0.3581 | 0.1837 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, anomaly detection |
| 428 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Remote - US, Ann Arbor, MI | 0.4657 | 0.1837 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 429 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Montreal, Canada, Remote - Canada | 0.4293 | 0.1837 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 430 | Senior Machine Learning Engineer - Foundation Model | XPENG | Santa Clara, CA | 0.5216 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 431 | Senior Machine Learning Engineer - AI Foundation | XPENG | Santa Clara, CA | 0.5216 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 432 | Senior Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.3452 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 433 | Senior Compliance Automation Engineer | True Anomaly | Denver, CO or Long Beach, CA or SF Bay area, CA or Washington, DC | 0.3729 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 434 | Sr Software Engineer II - Global Commercial Services | American Express | FL, United States / Sunrise Campus / New York-Amex Tower WFC-35 Hr / AEDR Desert Ridge OB2-McDowell | 0.3322 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 435 | Sr Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3322 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 436 | Senior Software Engineer, Prenatal | BillionToOne | Menlo Park, CA | 0.4432 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 437 | Senior Software Engineer - Live Pay | EarnIn | Vancouver, Canada | 0.4769 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 438 | Sr Advanced Software Engr | Honeywell | Singapore, Singapore, Singapore | 0.3296 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 439 | AI Engineer, Agent Platform | NewsBreak | Mountain View, California, United States | 0.3771 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 440 | Senior Software Engineer - Internal Tools & Productivity | ScaleAI | San Francisco, CA | 0.5141 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 441 | Applied AI Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.1837 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 442 | Senior, Software Engineer - Cloud Automation | Torc Robotics | Ann Arbor, MI, Remote - US | 0.3216 | 0.1837 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 443 | Senior Simulation Engineer I/II, Robotics | Lila Sciences | Cambridge, MA USA | 0.4105 | 0.1837 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 444 | Scientist/Sr. Scientist, AI Safety | Lila Sciences | Cambridge, MA USA; London, UK; San Francisco, CA USA | 0.5204 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 445 | Senior Software Engineer, ML Research | Lila Sciences | Cambridge, MA USA | 0.3852 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 446 | Sr Oracle Application Developer | GM Financial | Irving, TX, United States | 0.3203 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 447 | Lead AI Engineer | Honeywell | Atlanta, GA, United States | 0.3203 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 448 | ML Research Engineer, ML Systems | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.4502 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 449 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3201 | 0.1837 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 450 | Senior, Software Engineer - Release Pipelines | Torc Robotics | Ann Arbor, MI ;Remote - US | 0.3808 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 451 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1837 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 452 | Sr Software Engineer - Core Backend & Platform Engineering | Basis | United States | 0.32 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 453 | Senior Software Engineer (Backend Engineering) ⭐ | Achievers | Toronto | 0.32 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 454 | Développeur(euse) de données sénior, gouvernance des données | MaintainX | Montréal, Toronto | 0.32 | 0.1837 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL |
| 455 | Développeur(se) de logiciel senior spécialisé en moteurs de recherche | MaintainX | Montréal, Toronto | 0.32 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 456 | Senior AI Engineer - Agentic | Podium | Lehi, Utah, Open to Remote | 0.32 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 457 | Software Engineer, Developer Experience | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 458 | Software Engineer, Distributed Systems | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 459 | Sr. QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.4105 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 460 | Senior Computer Vision/AI  Engineer | BrightAI | Palo Alto, CA | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 461 | Senior Machine Learning Engineer II | CesiumAstro | Austin, TX | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 462 | Senior Software Engineer, Planning | PlusAI | Santa Clara, CA | 0.32 | 0.1837 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 463 | Senior AI Engineer | Reply | Seattle, Washington | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 464 | Senior AI Engineer, Time-Series Signal Processing | BrightAI | Palo Alto, CA | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 465 | Senior AI Engineer – LLM, RAG | BrightAI | Palo Alto, CA | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 466 | Senior AI Engineer | Reply | Chicago, Illinois | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 467 | Senior AI Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 468 | Senior Machine Learning Engineer, Perception | PlusAI | Santa Clara, CA | 0.32 | 0.1837 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 469 | Senior Software Engineer, Mapping & Localization | PlusAI | Santa Clara, CA | 0.32 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 470 | Senior Software Engineer | Wealth.com | Hybrid, New York, Tempe, San Francisco | 0.52 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 471 | Senior Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.1837 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 472 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 473 | Senior AI Developer (Coming Soon!) | Nuclear Promise X | Canada | 0.52 | 0.1837 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 474 | Senior Infrastructure Engineer | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 475 | Senior Software Engineer, AI Enablement | Wealth.com | New York, New York | 0.52 | 0.1837 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 476 | Senior QA Engineer | Super.com | Canada / United States | 0.52 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 477 | Sr. Site Development Engineer | Mariana Minerals | San Francisco HQ | 0.52 | 0.1837 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 478 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.175 | SWE_FULLTIME | — |
| 479 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 480 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5383 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 481 | Experienced Java Software Engineer | Boeing | POL - Gdansk, Poland | 0.5382 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 482 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.175 | SWE_FULLTIME | — |
| 483 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.175 | SWE_FULLTIME | — |
| 484 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 485 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.5238 | 0.175 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 486 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4917 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 487 | Software Engineer I | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.455 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 488 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.175 | SWE_FULLTIME | — |
| 489 | Experienced Software Engineer | Boeing | USA - Hazelwood, MO | 0.3829 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 490 | Intermediate Quality Assurance Engineer | Honeywell | Salem, OR, United States | 0.3619 | 0.175 | SWE_FULLTIME | — |
| 491 | Software Engineer I, QA | True Anomaly | Denver, CO or Long Beach, CA | 0.2857 | 0.175 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | — |
| 492 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 493 | Mid-Level Programmer Analyst | Boeing | USA - Saint Charles, MO | 0.2575 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 494 | AI Prompt Engineer | Appian | McLean, Virginia | 0.359 | 0.175 | SWE_FULLTIME | — |
| 495 | Software Engineer In Test - Android | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.175 | SWE_FULLTIME | — |
| 496 | Software Engineer In Test - iOS | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.175 | SWE_FULLTIME | — |
| 497 | Application Programmer | EarnIn | Remote, US | 0.2601 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 498 | Forward-deployed Engineer - LatAm (Remote) | Clara | Latin America  | 0.3287 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 499 | Forward-deployed Engineer - LatAm (Remote) | Clara | São Paulo, São Paulo, Brazil | 0.3287 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 500 | Application Engr II | Honeywell | Chongqing, China | 0.3247 | 0.175 | SWE_FULLTIME | — |
| 501 | Software Engineer II - MCU Applications (C++/Linux) | Torc Robotics | Ann Arbor, MI | 0.3371 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 502 | Application Engr II | Honeywell | Pune, Maharashtra, India | 0.3218 | 0.175 | SWE_FULLTIME | — |
| 503 | Project Engr I | Honeywell | Tianjin, China | 0.3214 | 0.175 | SWE_FULLTIME | — |
| 504 | Software Engr I | Honeywell | Pune City, Maharashtra, India | 0.3211 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 505 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.175 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | — |
| 506 | Software Engr II | Honeywell | Atlanta, GA, United States | 0.2402 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 507 | Full-Stack Developer - IAM | MaintainX | Toronto | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 508 | Scientific Software Engineer — Emulation & Application | QuEra Computing | Boston, MA, USA | 0.3505 | 0.175 | SWE_FULLTIME | — |
| 509 | Software Engineer, Growth & Monetization | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.175 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 510 | Developer Advocate (Tokyo, Japan) | Figma | Tokyo, Japan | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 511 | Software Engineering Instructor (Continuous)  | Per Scholas | Columbus, Ohio, United States | 0.1771 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 512 | Software Engineer - Core Interfaces | Palantir | Palo Alto, CA | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 513 | Software Engineer (C#/React) | Reply | Chicago, Illinois | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 514 | Software Engineer - Edge | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 515 | Software Engineer - Frontend Developer Productivity | Palantir | New York, NY | 0.32 | 0.175 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 516 | Mixed Reality Developer | Palantir | Washington, D.C. | 0.32 | 0.175 | SWE_FULLTIME | — |
| 517 | Software Engineer, Fraud & Identity | Ramp | New York, NY (HQ) | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 518 | Software Engineer, Stablecoin | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.175 | SWE_FULLTIME | — |
| 519 | Software Engineer, Accounting | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.175 | SWE_FULLTIME | — |
| 520 | Software Engineer, Product Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 521 | Software Engineer, Banking | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 522 | Embedded Software Engineer | Base Power Company | Austin, TX | 0.52 | 0.175 | SWE_FULLTIME | — |
| 523 | Software Engineer, Bill Pay & Procurement | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.175 | SWE_FULLTIME | — |
| 524 | Mobile Engineer, Android | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.175 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 525 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 526 | Software Engineer, Product | Base Power Company | Austin, TX | 0.52 | 0.175 | SWE_FULLTIME | — |
| 527 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.6542 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 528 | Senior Platform Engineer  | Clarity Innovations | Required  | 0.6497 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 529 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.6418 | 0.165 | DATA_ENGINEER_FULLTIME | Data Engineering, data modeling |
| 530 | Senior SAP FIORI Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 531 | Senior IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 532 | Sr Software Eng Supervisor | Honeywell | India | 0.5381 | 0.165 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 533 | Cloud Application Deployment and Migration Specialist (Mid-Level, Senior or Lead) **Sign on Bonus Potential** | Boeing | USA - Berkeley, MO | 0.5431 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 534 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 535 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 536 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 537 | Sr IT Architect | Honeywell | Pune City, Maharashtra, India | 0.4915 | 0.165 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure |
| 538 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4915 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 539 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.5219 | 0.165 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, data modeling |
| 540 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.516 | 0.165 | SWE_FULLTIME | Cloud Infrastructure |
| 541 | Service Now Sys Administrator | RTX | US-TX-REMOTE | 0.4761 | 0.165 | SWE_FULLTIME | Cloud Infrastructure |
| 542 | Lead Software Application – Architect | Boeing | IND - Bangalore, India | 0.4553 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 543 | Experienced Software Engineer- FSD | Boeing | IND - Bangalore, India | 0.4551 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 544 | Senior Backend Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.455 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 545 | Java Software Engineer (Associate, Experienced or Senior) - Bixby | Boeing | USA - Seal Beach, CA | 0.4178 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 546 | Cloud Architect | RTX | Warminster, Wiltshire | 0.3858 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 547 | Sr Advanced SW Architect | Honeywell | India | 0.3856 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 548 | Lead Architect, S4 Integration | Honeywell | Charlotte, NC, United States | 0.3716 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 549 | Advanced Software Engineer | Honeywell | Gdansk, Pomorskie, Poland | 0.3606 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 550 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.165 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 551 | Senior Software Engineer - Java / AWS Services | Appian | McLean, Virginia | 0.359 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 552 | Senior Software Engineer - Database Platform | Appian | McLean, Virginia | 0.359 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 553 | Senior Software Engineer II - Amex Ads | American Express | New York, NY, United States | 0.3322 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 554 | Lead Software Architect - EPMS Systems | Honeywell | Atlanta, GA, United States | 0.3276 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 555 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3276 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 556 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.165 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure |
| 557 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 558 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.165 | SWE_FULLTIME | Cloud Infrastructure |
| 559 | Advanced Software Engineer - Cybersecurity | Honeywell | Duluth, GA, United States | 0.3204 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 560 | Lead IT Architect ORACLE HCM (Integration Cloud) | Honeywell | Charlotte, NC, United States | 0.3204 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 561 | Salesforce Sr IT Architect – Customer and Commercial Experience (CCEX) | Honeywell | Charlotte, NC, United States | 0.3203 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 562 | Lead Software Engineer | Reply | Atlanta, Georgia | 0.3201 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 563 | Développeur logiciel senior, facturation | MaintainX | Montréal | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 564 | Edge Infrastructure Engineer | Palantir | Warsaw, Poland | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 565 | Senior Software Developer, Search  | MaintainX | Montreal, Toronto | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 566 | Senior Software Developer, Compliance and Multi-Region | MaintainX | Montreal, Toronto  | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 567 | Full-Stack Developer, Connected Data  | MaintainX | Montréal, Toronto | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 568 |  Senior SDET - Tooling Engineer | EarnIn | Mountain View, US | 0.4086 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 569 | Software Engineer, Production Engineering  (London, United Kingdom) | Figma | London, England | 0.32 | 0.165 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 570 | Azure Cloud Architect | Reply | Detroit Area, Michigan | 0.32 | 0.165 | SWE_FULLTIME | Cloud Infrastructure |
| 571 | Azure Cloud Architect | Reply | Chicago, Illinois | 0.32 | 0.165 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 572 | Azure Cloud Architect | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.165 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 573 | Senior Software Engineer, Substrate | Palantir | Washington, D.C. | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 574 | Senior Software Engineer, Network Infrastructure | Palantir | Washington, D.C. | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 575 | Senior Data Engineer | Reply | Kochi, Kerala | 0.32 | 0.165 | DATA_ENGINEER_FULLTIME | Data Engineering, data modeling |
| 576 | Senior Software Engineer, Substrate | Palantir | London, United Kingdom | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 577 | Senior Software Engineer, Substrate | Palantir | New York, NY | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 578 | Senior Software Engineer, Substrate | Palantir | Seattle, WA | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 579 | Senior Software Engineer, Network Infrastructure | Palantir | New York, NY | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 580 | Senior Software Engineer, Network Infrastructure | Palantir | Seattle, WA | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 581 | Senior Software Engineer - Observability | Palantir | New York, NY | 0.32 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 582 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | San Francisco | 0.52 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 583 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | New York | 0.52 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 584 | Senior Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.1425 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python, SQL |
| 585 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.7039 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 586 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.5382 | 0.1237 | SWE_FULLTIME | Python |
| 587 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.508 | 0.1237 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 588 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4918 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 589 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4913 | 0.1237 | SWE_FULLTIME | Python |
| 590 | Senior Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.1237 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Python |
| 591 | Senior Software Engineer - Operating System | Torc Robotics | Ann Arbor, MI | 0.5232 | 0.1237 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Python |
| 592 | Lead Software Engineer - Firmware | Honeywell | Pittsford, NY, United States | 0.4921 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 593 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4553 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL |
| 594 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4552 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 595 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 596 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 597 | Senior Associate - Oracle Technical Developer | American Express | Gurugram, HR, India | 0.3717 | 0.1237 | SWE_FULLTIME | SQL |
| 598 | Advanced Software Engineer | Honeywell | Raleigh, NC, United States | 0.3716 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 599 | Senior Software Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.368 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 600 | Senior Consultant (Top Secret Clearance) | Appian | McLean, Virginia | 0.359 | 0.1237 | SWE_FULLTIME | SQL, data modeling |
| 601 | Senior Technical Consultant | Appian | McLean, Virginia | 0.359 | 0.1237 | SWE_FULLTIME | SQL, data modeling |
| 602 | Senior Test Automation Engineer | Appian | Chennai, India | 0.359 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 603 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 604 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.1237 | SWE_FULLTIME | SQL |
| 605 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3519 | 0.1237 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | SQL |
| 606 | Senior Identity Security Engineer | Palantir | Palo Alto, CA | 0.3318 | 0.1237 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 607 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 608 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 609 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 610 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 611 | Engineer II /Senior Software Engineer, Simulation | Lila Sciences | Cambridge, MA USA | 0.3486 | 0.1237 | SWE_FULLTIME | Python |
| 612 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.3276 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 613 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.3276 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 614 | Senior Software Engineer, GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 615 | Senior Software Engineer, Calibration | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3853 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 616 | Senior Software Engineer, Calibration | Torc Robotics | Remote - Canada, Montreal, Canada | 0.3253 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 617 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.1237 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL |
| 618 | Senior Full Stack Engineer | EarnIn | Mountain View, US | 0.4891 | 0.1237 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Python |
| 619 | Senior Software Engineers | American Express | New York, NY, United States | 0.3202 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 620 | Senior Applied Scientist, Scheduling and Optimization | MaintainX | Canada (Remote) | 0.32 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 621 | Sr Software Engineer - Basis Platform / DSP | Basis | United States | 0.32 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 622 | Senior or Lead Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 623 | Software Engineer, C++ | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1237 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Python |
| 624 | Senior Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 625 | Senior Mobile Security Engineer (Forensics) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.1237 | MOBILE_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 626 | Senior Software Engineer / GTM Platform, Backend | Ramp | New York, NY (HQ) | 0.52 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 627 | Founding Engineer | Icon | New York / Remote | 0.52 | 0.1237 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 628 | Senior Integration Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 629 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.5381 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 630 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.105 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 631 | Senior Mobile Engineer (Android) | EarnIn | Mountain View, US | 0.727 | 0.105 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 632 | Senior UX Design Engineer, Design Systems | Greenhouse | Ontario | 0.4975 | 0.105 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 633 | Lead Software Engineer | Appian | McLean, Virginia | 0.514 | 0.105 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 634 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.5066 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 635 | Senior Quality Engineer I | American Express | Chennai, TN, India | 0.4917 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 636 | Developpeur SAP ABAP  /  SAP ABAP Developer | RTX | CA-QC-LONGUEUIL-J01 ~ 1000 Blvd Marie-Victorin ~ J01 BLDG | 0.3858 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 637 | Advanced Embedded Engineer | Honeywell | United Kingdom | 0.3717 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 638 | Sr IT Engineer | Honeywell | Hyderabad, Telangana, India | 0.3716 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 639 | Senior Software Engineer - Java /  Hibernate | Appian | McLean, Virginia | 0.359 | 0.105 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 640 | Sr Software Engineer - Global Commercial Services | American Express | New York, NY, United States / AEDR Desert Ridge CSB - Sierra | 0.352 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 641 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 642 | Senior Software Engineer, Front End | True Anomaly | Denver, CO or Long Beach, CA | 0.4886 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 643 | Senior Backend Engineer — ClarOps (Ingeniero Backend Senior de ClarOps) - Remote | Clara | Latin America  | 0.3364 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 644 | Senior Embedded Software Engineer II | CesiumAstro | Westminster, CO | 0.3313 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 645 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3237 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 646 | Senior Front End Engineer | EarnIn | Mountain View, US | 0.4891 | 0.105 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 647 | Software Engineers | American Express | Phoenix, AZ, United States | 0.3202 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 648 | Senior Software Engineer | EarnIn | Bengaluru, India | 0.3201 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 649 | Lead Software Engineer | Reply | Chicago, Illinois | 0.3201 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 650 | Senior Software Developer, Billing  | MaintainX | Montreal, Toronto | 0.32 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 651 | Sr. Software Engineer, React/ React Native | Prosper | San Francisco, CA | 0.32 | 0.105 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 652 | Développeur(se) Full-Stack sénior ou en chef  | MaintainX | Montréal | 0.32 | 0.105 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 653 | Senior Software Engineer, iOS | NewsBreak | Mountain View, California, United States | 0.439 | 0.105 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 654 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.105 | SWE_FULLTIME | — |
| 655 | Senior Software Engineer I, Client Connections | EnergyHub | Remote - United States | 0.3295 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 656 | Senior Software Engineer - Vehicle Diagnostics | Torc Robotics | Ann Arbor, MI, Remote, US | 0.3808 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 657 | Senior iOS Engineer | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.105 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 658 | Senior Software Engineer (PHP/ Golang) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.105 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 659 | Senior Software Engineers | Achievers | Toronto | 0.32 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 660 | Senior Embedded Software Integration Engineer | PlusAI | Chicago, IL | 0.32 | 0.105 | SWE_FULLTIME | — |
| 661 | Senior Front End Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 662 | Senior Backend Engineer | Nash | San Francisco | 0.52 | 0.105 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 663 | Senior Software Engineer—Kernels | d-Matrix | Bangalore | 0.52 | 0.105 | SWE_FULLTIME | — |
| 664 |  Senior Software Engineer, Visualization | Foxglove | San Francisco, CA | 0.52 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 665 | Senior Software Engineer (Frontend Focus) | Kira | New York | 0.52 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 666 | Senior Software Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.105 | SWE_FULLTIME | — |
| 667 | Senior .NET Developer | Nuclear Promise X | Chalk River | 0.52 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 668 | Senior Software Engineer / GTM Platform, Frontend | Ramp | New York, NY (HQ) | 0.52 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 669 | Senior .NET Developer (Coming Soon!) | Nuclear Promise X | Ontario / Remote | 0.52 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 670 | Senior Software Engineer - API Experience | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 671 | Senior Software Engineer / Web + Design | Ramp | New York, NY (HQ) | 0.52 | 0.105 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 672 | Senior React Native Engineer — Driver App  | Nash | Remote HQ / San Francisco | 0.52 | 0.105 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |

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

- **Total jobs matching subscribed pools (after filters):** 646
- **Notification-eligible jobs (≤60d, not yet emailed):** 500
- **Personal score range:** 0.045 – 0.5664 (103 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 540 |
| `BACKEND_ENGINEER_FULLTIME` | 340 |
| `ML_ENGINEER_FULLTIME` | 137 |
| `FULLSTACK_ENGINEER_FULLTIME` | 65 |
| `DATA_ENGINEER_FULLTIME` | 65 |
| `DEVOPS_ENGINEER_FULLTIME` | 63 |
| `FRONTEND_ENGINEER_FULLTIME` | 48 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 27 |
| `SECURITY_ENGINEER_FULLTIME` | 14 |
| `MOBILE_ENGINEER_FULLTIME` | 12 |
| `DATA_SCIENTIST_FULLTIME` | 9 |
| `SUPPORT_ENGINEER_FULLTIME` | 4 |
| `DATA_ANALYST_FULLTIME` | 4 |
| `PRODUCT_MANAGER_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Software Engineer II, Lab Software @ Lila Sciences

- **Location:** Cambridge, MA USA (unclear)
- **Posted:** 2026-05-21T22:35:47+00:00
- **Salary:** 120000 – 180000
- **Effort:** MEDIUM
- **Opportunity score:** 0.3318
- **Personal score:** 0.5664
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, FULLSTACK_ENGINEER
- **Capabilities:** Backend Engineering, Full Stack Development, Cloud Infrastructure, DevOps
- **Skills:** Data pipeline architecture, System performance optimization, Orchestration, Infrastructure-as-Code
- **Match reasons:** Backend Engineering, Full Stack Development, Cloud Infrastructure, DevOps, Python
- **URL:** https://job-boards.greenhouse.io/lilasciences/jobs/4250045009

#### #2 — Software Engineer II, Full Stack - Global Servicing Technology @ American Express

- **Location:** Sunrise, FL, United States (unclear)
- **Posted:** 2026-06-04T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.3717
- **Personal score:** 0.5437
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `FRONTEND_ENGINEER_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, FRONTEND_ENGINEER, FULLSTACK_ENGINEER
- **Capabilities:** Full Stack Development, Cloud Infrastructure, DevOps, Distributed Systems
- **Skills:** microservices architecture, CI/CD, API development, Infrastructure as Code
- **Match reasons:** Full Stack Development, Cloud Infrastructure, DevOps, Distributed Systems, Java
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26007438/details

#### #3 — Forward Deployed Software Engineer - US Government - Federal Health and Civilian @ Palantir

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

#### #4 — Software Engineer, Credit @ Ramp

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

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Software Engineer II, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3318 | 0.5664 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 2 | Software Engineer II, Full Stack - Global Servicing Technology | American Express | Sunrise, FL, United States | 0.3717 | 0.5437 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 3 | Software Engineer III - Java - Web Search Team | American Express | Phoenix, AZ, United States | 0.3211 | 0.521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 4 | Forward Deployed Software Engineer - US Government - Federal Health and Civilian | Palantir | New York, NY | 0.3201 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, AI Systems |
| 5 | Backend Software Engineer - Infrastructure, Foundations | Palantir | New York, NY | 0.32 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 6 | Forward Deployed Software Engineer | Palantir | New York, NY | 0.32 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 7 | Software Engineer, Credit | Ramp | New York, NY (HQ) | 0.52 | 0.4992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 8 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2159 | 0.4982 | SWE_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 9 | Software Engineer, Full Stack | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4775 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, React |
| 10 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.5413 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 11 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4916 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 12 | Instructional Assistant (Cloud Systems Engineering) | Per Scholas | United States; United States | 0.3915 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 13 | Infrastructure Software Engineer, Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 14 | Forward Deployed Software Engineer - US Government | Palantir | New York, NY | 0.32 | 0.4765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 15 | Software Engineer, Growth & Monetization | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4548 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 16 | Cybersecurity Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Data Engineering |
| 17 | Software Engineer - Hosted Model Infrastructure | Palantir | New York, NY | 0.3691 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 18 | Platform Developer, AI Builder  | MaintainX | Canada/United States | 0.32 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 19 | Data Engineering Instructor | Per Scholas | United States | 0.32 | 0.4538 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, AI Systems |
| 20 | Software Engineer - Apollo Platform | Palantir | New York, NY | 0.32 | 0.4538 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 21 | Software Engineer, Agent Developer Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.4538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 22 | Advanced Software Engineer | Honeywell | Atlanta, GA, United States | 0.3223 | 0.4528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 23 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 24 | AI Engineer III - Agentic AI | American Express | New York, NY, United States / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus | 0.3322 | 0.4321 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 25 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5141 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 26 | Software Engineer, Enterprise AI | ScaleAI | New York, NY; San Francisco, CA | 0.5141 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 27 | Software Engineer I | Honeywell | Hamilton, NJ, United States | 0.2087 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 28 | Software Engineer, AI Platforms | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.4321 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, TypeScript |
| 29 | Neurodivergent Fellowship | Palantir | New York, NY | 0.32 | 0.4321 | SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 30 | Forward Deployed Software Engineer - Warp Speed | Palantir | New York, NY | 0.32 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 31 | Software Engineer, Banking | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) | 0.52 | 0.4321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 32 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.755 | 0.4311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 33 | Software Engineer, Platform | ScaleAI | San Francisco, CA; New York, NY | 0.7099 | 0.4311 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, DevOps |
| 34 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.3717 | 0.4311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 35 | Growth Intelligence Engineer (Ads & Revenue) | NewsBreak | Mountain View, California, United States | 0.3656 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, SQL |
| 36 | Technical Instructor (AWS Machine Learning) | Per Scholas | United States | 0.2942 | 0.4093 | ML_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 37 | Instructional Assistant (Data Engineer) (3-6 month contract) | Per Scholas | Orlando, Florida, United States | 0.32 | 0.4093 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Backend Engineering, Python |
| 38 | Forward Deployed AI Engineer | Palantir | New York, NY | 0.32 | 0.4093 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Backend Engineering, Python |
| 39 | Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 40 | Forward Deployed Infrastructure Engineer - US Government | Palantir | New York, NY | 0.32 | 0.4093 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 41 | Software Engineer - Developer Productivity | Palantir | New York, NY | 0.32 | 0.4093 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 42 | Software Engineer, Web Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Go |
| 43 | Software Engineer II | Honeywell | Duluth, GA, United States | 0.3857 | 0.4083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 44 | Software Engineer, Product Infrastructure | Notion | San Francisco, California / New York, New York | 0.52 | 0.3876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Go |
| 45 | Forward Deployed Engineer, GTM | Notion | San Francisco, California / New York, New York | 0.52 | 0.3876 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, SQL |
| 46 | Backend Engineer, Ops | Ramp | New York, NY (HQ) | 0.52 | 0.3876 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Java, Python |
| 47 | Software Engineer, Trust | Notion | San Francisco, California / New York, New York | 0.52 | 0.3876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 48 | Software Engineer, Growth Platform | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3876 | SWE_FULLTIME | Backend Engineering, Python, Go |
| 49 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.6346 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, Python |
| 50 | Cybersecurity AI_ML Engineer | GM Financial | Irving, TX, United States / US - Arlington AOC I, TX | 0.3452 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 51 |  Machine Learning Research Engineer, Agent Data Foundation - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.3866 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 52 | Forward Deployed Engineer, GenAI  | ScaleAI | San Francisco, CA; New York, NY | 0.4357 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Python |
| 53 | Software Engineer I - Metrics for Release Implementation | Torc Robotics | Remote, US | 0.2905 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 54 | Advanced Software Engineer | Honeywell | Acton, MA, United States | 0.3428 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 55 | Research Scientist I/II, AI for Process Engineering | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.3866 | ML_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Python |
| 56 | Research Engineer, Frontier Capabilities | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4995 | 0.3866 | ML_ENGINEER_FULLTIME | Distributed Systems, AI Systems, Python |
| 57 | Software Engineer, Tools & Services | Basis | United States | 0.3204 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 58 | Sales AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.4594 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, SQL |
| 59 | Software Engineer (Gen AI) | EarnIn | Mountain View, US | 0.4277 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 60 | Software Engineer, Machine Learning | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3866 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 61 | QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.3295 | 0.3866 | SWE_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 62 | Software Engineering Instructor (Continuous)  | Per Scholas | Columbus, Ohio, United States | 0.1771 | 0.3866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, PostgreSQL |
| 63 | Platform Intelligence Engineer | Palantir | New York, NY | 0.32 | 0.3866 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Backend Engineering, Python |
| 64 | Software Engineer, AI Forward Deployed | Ramp | San Francisco, CA / New York, NY (HQ) | 0.52 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 65 | Applied AI Engineer | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 66 | Support AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.7152 | 0.3649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 67 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.5382 | 0.3649 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 68 | Manufacturing Applications and Controls Engineer (Onsite) | RTX | US-ME-NORTH BERWICK-113 ~ 113 Wells St ~ WELLS, Rte 9 | 0.476 | 0.3649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 69 | Data Scientist, Core Data -  PhD (2026) | Figma | San Francisco, CA • New York, NY | 0.4137 | 0.3649 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 70 | Advanced Software Engineer -AI R&D | Honeywell | North Ryde, New South Wales, Australia | 0.3322 | 0.3649 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 71 | Software Engineer, Collections Experience | Notion | San Francisco, California / New York, New York | 0.52 | 0.3649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, PostgreSQL |
| 72 | Experienced Software Configuration Management Specialist | Boeing | USA - Tukwila, WA | 0.3942 | 0.3639 | SWE_FULLTIME | Cloud Infrastructure, DevOps |
| 73 | Experienced Software Engineer | Boeing | USA - Hazelwood, MO | 0.3829 | 0.3639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering |
| 74 | Software Engineer, Production Engineering | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.3639 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 75 | Senior Software Engineer, Data | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4621 | 0.3529 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 76 | Software Engineer, Core Product | Ramp | New York, NY (HQ) | 0.52 | 0.3432 | SWE_FULLTIME | Python, Go, Java |
| 77 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.6294 | 0.3422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 78 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5851 | 0.3422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 79 | Computing Architect (Manhattan Warehouse M.S.) | Boeing | USA - Hialeah, FL | 0.4881 | 0.3422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 80 | Mid-Level Programmer Analyst | Boeing | USA - Saint Charles, MO | 0.2575 | 0.3422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 81 | Machine Learning Systems Research Engineer, Agent Post-training - Enterprise GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5275 | 0.3422 | ML_ENGINEER_FULLTIME | Distributed Systems, Python |
| 82 | Machine Learning Scientist I/II, Scientific Reasoning | Lila Sciences | Cambridge, MA USA | 0.5014 | 0.3422 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 83 | Scientific Software Engineer - Compiler | QuEra Computing | Boston, MA  USA | 0.2998 | 0.3422 | SWE_FULLTIME | Backend Engineering, Python |
| 84 | Scientific Software Engineer - Virtual Machine & Emulation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.3422 | SWE_FULLTIME | Distributed Systems, Python |
| 85 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.3422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 86 | Scientific Software Engineer- Shuttle Compilation | QuEra Computing | Boston, MA  USA | 0.2998 | 0.3422 | SWE_FULLTIME | Backend Engineering, Python |
| 87 | Software Engineer, AI Workflows | Notion | San Francisco, California / New York, New York | 0.52 | 0.3422 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Python |
| 88 | AI/ML Engineer | Melotech | Berlin / New York / London | 0.52 | 0.3422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 89 | Senior Software Engineer, Lab Software | Lila Sciences | Cambridge, MA USA | 0.3879 | 0.3398 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 90 | Sr Advanced Cloud Developer | Honeywell | Mason, OH, United States | 0.3204 | 0.3392 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Data Engineering |
| 91 |  Senior Software Engineer,  Full-Stack – Scale GP | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.3262 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 92 | Software Engineer (Backend), Enterprise | ScaleAI | Budapest, Hungary | 0.3332 | 0.322 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 93 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5249 | 0.321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 94 | Software Engineer II | Appian | Chennai, India | 0.359 | 0.321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 95 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.4203 | 0.3205 | SWE_FULLTIME | Java, Python |
| 96 | Software Engineer - Frontend Developer Productivity | Palantir | New York, NY | 0.32 | 0.3205 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 97 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.52 | 0.3205 | SWE_FULLTIME | Java, Python |
| 98 | Software Engineer, Guest Travel | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Denver, CO | 0.52 | 0.3205 | SWE_FULLTIME | Java, Python |
| 99 | Application Programmer | EarnIn | Remote, US | 0.2601 | 0.3194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 100 | Scientific Software Engineer — Emulation & Application | QuEra Computing | Boston, MA, USA | 0.3505 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 101 | Software Engineer, Accounting | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 102 | Software Engineer, Stablecoin | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 103 | Software Engineer, Fraud & Identity | Ramp | New York, NY (HQ) | 0.52 | 0.3194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 104 | Software Engineer, Engineering Platform | Ramp | New York, NY (HQ) | 0.52 | 0.3194 | SWE_FULLTIME | Cloud Infrastructure |
| 105 | Software Engineer, Data Platform  | Ramp | New York, NY (HQ) | 0.52 | 0.3194 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering |
| 106 | Software Engineer, Bill Pay & Procurement | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.3194 | SWE_FULLTIME | Backend Engineering |
| 107 | Senior Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.3452 | 0.3132 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Distributed Systems |
| 108 | Senior Software Engineer, App | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4165 | 0.3132 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 109 | Senior Software Engineer, Applied AI | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4385 | 0.3132 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 110 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.5377 | 0.3126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 111 | Senior AI Engineer I - Agentic AI | American Express | New York, NY, United States / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley / Sunrise Campus / Charlotte Hybrid-600 Tryon | 0.4035 | 0.3126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 112 | Senior Software Engineer, Operations Research | Lila Sciences | Cambridge, MA USA | 0.4661 | 0.3126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 113 | Software Engineer, Developer Experience | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.3126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 114 | Equipment & Tooling Software Engineer (Associate, Experienced and/or Senior) | Boeing | USA - North Charleston, SC | 0.3555 | 0.2995 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 115 | Software Engineer, Distributed Systems | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2995 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, Backend Engineering |
| 116 | Sr. QPU Software Engineer | QuEra Computing | Boston, MA, USA | 0.4105 | 0.2995 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 117 | Software Engineer, Robotics | ScaleAI | Mexico City, MX | 0.3274 | 0.2992 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, Cloud Infrastructure |
| 118 | Software Engineer, Robotics & Autonomous Systems | ScaleAI | San Francisco, CA | 0.437 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 119 | Forward Deployed Software Engineer - Japan Government | Palantir | Tokyo, Japan | 0.32 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 120 | Forward Deployed Software Engineer - AUS Government | Palantir | Sydney, Australia | 0.32 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 121 | Forward Deployed Software Engineer | Palantir | Dubai, United Arab Emirates | 0.32 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Data Engineering |
| 122 | Forward Deployed Software Engineer | Palantir | Stockholm, Sweden | 0.32 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Data Engineering |
| 123 | Forward Deployed Software Engineer | Palantir | Amsterdam, Netherlands | 0.32 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 124 | Forward Deployed Software Engineer | Palantir | Tel Aviv, Israel | 0.32 | 0.2992 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 125 | Senior Software Developer - Data Engineering-2 | Boeing | USA - Seattle, WA | 0.4782 | 0.2989 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 126 | Lead Software Architect - EPMS Systems | Honeywell | Atlanta, GA, United States | 0.3276 | 0.2989 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 127 | Sr Software Engineer - Core Backend & Platform Engineering | Basis | United States | 0.32 | 0.2989 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 128 | Software Engineer, Data Infrastructure | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2989 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 129 | Software Engineer II | American Express | Gurugram, HR, India | 0.5382 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 130 | Software Engineer I, Service Network - Slack | Slack (Salesforce) | Washington - Seattle | 0.5446 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 131 | Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 132 | Software Engineer II | Appian | Chennai, India | 0.3766 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 133 | Forward Deployed Engineer, RL Environments | Labelbox | San Francisco Bay Area | 0.3676 | 0.2982 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 134 | Software Engineer I, Instrument Software  | Lila Sciences | Cambridge, MA USA | 0.2804 | 0.2977 | SWE_FULLTIME | Python |
| 135 | Software Engr II | Honeywell | Atlanta, GA, United States | 0.2402 | 0.2977 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | React |
| 136 | Quantum Calibration Engineer, Quantum Computing Services | QuEra Computing | Boston, MA, USA | 0.3295 | 0.2977 | ML_ENGINEER_FULLTIME | Python |
| 137 | Mobile Engineer, Android | Ramp | New York, NY (HQ) / San Francisco, CA / Remote (US) / Remote (Canada) | 0.52 | 0.2977 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | Java |
| 138 | Software Engineer, AI DevX | Ramp | New York, NY (HQ) / San Francisco, CA | 0.52 | 0.2977 | SWE_FULLTIME | Python |
| 139 | Sr Software Engineer II - Global Commercial Services | American Express | FL, United States / Sunrise Campus / New York-Amex Tower WFC-35 Hr / AEDR Desert Ridge OB2-McDowell | 0.3322 | 0.2865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, TypeScript |
| 140 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5381 | 0.2859 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 141 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5381 | 0.2859 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 142 | Senior Software Engineer, Scientific System of Record | Lila Sciences | Cambridge, MA USA; San Francisco, CA USA | 0.4561 | 0.2859 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 143 | Software Development Engineer - Gen AI | GM Financial | Irving, TX, United States / US - Arlington, TX | 0.3203 | 0.2859 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 144 | Senior Software Engineer | Wealth.com | Hybrid, New York, Tempe, San Francisco | 0.52 | 0.2859 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 145 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.6542 | 0.2853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 146 | Senior Software Engineer, Substrate | Palantir | New York, NY | 0.32 | 0.2853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 147 | GTM Engineer | Greenhouse | British Columbia | 0.5275 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Data Engineering |
| 148 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.3857 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, AI Systems |
| 149 | AI Engineer III | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.2765 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 150 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.2765 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, AI Systems |
| 151 | Full-Stack Software Engineer (Backend Oriented) | Lendbuzz | Boston, MA | 0.32 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 152 | Forward Deployed Software Engineer - US Government | Palantir | Fayetteville, NC | 0.32 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 153 | Market Infrastructure Engineer | Base Power Company | Austin, TX | 0.52 | 0.2765 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 154 | Software Engineer, Argentina | Ramp | Remote (Buenos Aires, Argentina) | 0.52 | 0.2765 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 155 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.2755 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 156 | Intermediate Quality Assurance Engineer | Honeywell | Salem, OR, United States | 0.3619 | 0.275 | SWE_FULLTIME | — |
| 157 | AI Engineer, Agent Platform | NewsBreak | Mountain View, California, United States | 0.3771 | 0.2729 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 158 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.659 | 0.2723 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 159 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.638 | 0.2723 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 160 | Java Software Engineer (Associate, Experienced or Senior) - Bixby | Boeing | USA - Seal Beach, CA | 0.4178 | 0.2723 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 161 | Sr Advanced AI Platform Engineer | Honeywell | Atlanta, GA, United States | 0.3218 | 0.2723 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, Cloud Infrastructure |
| 162 | Senior Software Engineer, ML Research | Lila Sciences | Cambridge, MA USA | 0.3852 | 0.2723 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 163 | Software Engineer, ML Infra | NewsBreak | Mountain View, California, United States | 0.4295 | 0.2723 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 164 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.5382 | 0.2592 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 165 | Software Engineers | American Express | Phoenix, AZ, United States | 0.5382 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 166 | Senior Data Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.2592 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, PostgreSQL |
| 167 | Senior Software Engineer, GenAI | ScaleAI | San Francisco, CA; New York, NY | 0.5141 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, TypeScript |
| 168 | Sr Software Engineer - Basis Platform / DSP | Basis | United States | 0.32 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 169 | Software Engineer, Code Platform | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 170 | Founding Engineer | Icon | New York / Remote | 0.52 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 171 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 172 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4917 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 173 | Software Engineer III - MFT Business Enablement - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 174 | Senior Backend Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.455 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 175 | Senior Software Engineer, Digital Banking & Payments | American Express | Phoenix, AZ, United States | 0.3857 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 176 | Senior Software Engineer II - Amex Ads | American Express | New York, NY, United States | 0.3322 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 177 | Advanced AI Engineer | Honeywell | Charlotte, NC, United States | 0.3214 | 0.2586 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Cloud Infrastructure, DevOps |
| 178 | Senior, ML Engineer - ML Ops Framework | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5181 | 0.2586 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 179 | Full-Stack Engineer, AI Data Platform | Labelbox | San Francisco Bay Area | 0.3608 | 0.2548 | FULLSTACK_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, React |
| 180 | Backend Software Engineer - Infrastructure | Palantir | London, United Kingdom | 0.32 | 0.2548 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 181 | Forward Deployed Software Engineer | Palantir | London, United Kingdom | 0.32 | 0.2548 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 182 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2538 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 183 | Software Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 184 | Data Engineer II | American Express | Bengaluru, KA, India | 0.3857 | 0.2538 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, AI Systems |
| 185 | Software Engineer - Hosted Model Infrastructure | Palantir | Palo Alto, CA | 0.3691 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 186 | Production Engineer - Database Operations | Palantir | London, United Kingdom | 0.3203 | 0.2538 | DEVOPS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 187 | Développeur(se) Logiciel de Plateforme, Outils de développement IA | MaintainX | Montreal, Canada | 0.32 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 188 | Intermediate Software Engineer (Backend Engineering) | Achievers | Toronto | 0.4 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 189 | Software Engineer - Environment Platform | Palantir | Seattle, WA | 0.32 | 0.2538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 190 | Senior Full Stack Engineer | EarnIn | Mountain View, US | 0.4891 | 0.2462 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, React, TypeScript |
| 191 | Senior Backend Software Engineer - Application Development | Palantir | New York, NY | 0.32 | 0.2462 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Java, Python |
| 192 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5827 | 0.2456 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 193 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5719 | 0.2456 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, SQL |
| 194 | Data Engineer-ETL Tools & Python/ Python frameworks | American Express | Phoenix, AZ, United States | 0.3857 | 0.2456 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 195 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.2456 | SWE_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 196 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.3276 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 197 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.3276 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 198 | Senior Data Engineers | American Express | New York, NY, United States | 0.3276 | 0.2456 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 199 | Senior, ML Engineer - Auto Tagger | Torc Robotics | Ann Arbor, MI, Remote - US | 0.417 | 0.2456 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 200 | Machine Learning Engineer II / Senior Machine Learning Engineer I, Physical Sciences | Lila Sciences | Cambridge, MA USA | 0.3547 | 0.2456 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 201 | Sr Oracle Application Developer | GM Financial | Irving, TX, United States | 0.3203 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 202 | Senior Software Engineers | American Express | New York, NY, United States | 0.3202 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 203 | Senior Software Engineer I, Client Connections | EnergyHub | Remote - United States | 0.3295 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 204 | Senior Software Engineer - Observability | Palantir | New York, NY | 0.32 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, Java |
| 205 | Senior Data Engineer | Super.com | Canada / United States | 0.52 | 0.2456 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 206 | Senior Software Engineer - AI/ML | Wealth.com | New York, New York | 0.52 | 0.2456 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 207 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.2456 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 208 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4916 | 0.245 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 209 | Lead Architect, S4 Integration | Honeywell | Charlotte, NC, United States | 0.3716 | 0.245 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 210 | Lead IT Architect ORACLE HCM (Integration Cloud) | Honeywell | Charlotte, NC, United States | 0.3204 | 0.245 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 211 | Salesforce Sr IT Architect – Customer and Commercial Experience (CCEX) | Honeywell | Charlotte, NC, United States | 0.3203 | 0.245 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 212 |  Senior SDET - Tooling Engineer | EarnIn | Mountain View, US | 0.4086 | 0.245 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 213 | Software Engineer, Production Engineering | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.245 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 214 | Forward Deployed Software Engineer - Japan Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.2331 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 215 | Forward Deployed Software Engineer - Intel | Palantir | Washington, D.C. | 0.32 | 0.2331 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 216 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.7386 | 0.2326 | ML_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 217 | Data Engineer, AI/ML III/IV | Zone 5 Technologies | United States | 0.5184 | 0.2326 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, TypeScript, React |
| 218 | Advanced Software Engineer | Honeywell | Pittsburgh, PA, United States | 0.3223 | 0.2326 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 219 | Senior Software Engineer / GTM Platform, Backend | Ramp | New York, NY (HQ) | 0.52 | 0.2326 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, PostgreSQL, Python |
| 220 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 221 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 222 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 223 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4775 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 224 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.3223 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 225 | Software Engr I | Honeywell | Pune City, Maharashtra, India | 0.3211 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 226 | Neurodivergent Fellowship | Palantir | Washington, D.C. | 0.32 | 0.2321 | SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 227 | Forward Deployed Enablement Engineer - Customer Success | Palantir | Washington, D.C. | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 228 | Forward Deployed Software Engineer - US Government | Palantir | San Diego, CA | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Java |
| 229 | Forward Deployed Software Engineer - Korea Forward Deployed | Palantir | Washington, D.C. | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 230 | Forward Deployed Software Engineer | Palantir | Seoul, South Korea | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Java |
| 231 | Forward Deployed Software Engineer | Palantir | Vilnius, Lithuania | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 232 | Forward Deployed Software Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2321 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 233 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7493 | 0.232 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Data Engineering, Python |
| 234 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.5382 | 0.232 | SWE_FULLTIME | AI Systems, Machine Learning Research, Python |
| 235 | Lead Software Engineer - Firmware | Honeywell | Pittsford, NY, United States | 0.4921 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 236 | Sr Software Engineer - Global Commercial Services | American Express | New York, NY, United States / AEDR Desert Ridge CSB - Sierra | 0.352 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 237 | Senior Software Engineers | American Express | Sunrise, FL, United States | 0.352 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 238 | Lead Data Engineer | Honeywell | Atlanta, GA, United States | 0.326 | 0.232 | DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Python |
| 239 | Senior, Software Engineer - Cloud Automation | Torc Robotics | Ann Arbor, MI, Remote - US | 0.3216 | 0.232 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 240 | Senior Simulation Engineer I/II, Robotics | Lila Sciences | Cambridge, MA USA | 0.4105 | 0.232 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 241 | Advanced Software Engineer - Cybersecurity | Honeywell | Duluth, GA, United States | 0.3204 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 242 | Software Engineers | American Express | Phoenix, AZ, United States | 0.3202 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 243 | ML Research Engineer, ML Systems | ScaleAI | San Francisco, CA; Seattle, WA; New York, NY | 0.4502 | 0.232 | ML_ENGINEER_FULLTIME | Distributed Systems, AI Systems, Python |
| 244 | Senior, Software Engineer - Release Pipelines | Torc Robotics | Ann Arbor, MI ;Remote - US | 0.3808 | 0.232 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 245 | Data Platform Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.232 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 246 | Senior Software Engineer, AI Enablement | Wealth.com | New York, New York | 0.52 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 247 | Senior QA Engineer | Super.com | Canada / United States | 0.52 | 0.232 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 248 | Senior Software Engineer, AI/ML (Infrastructure & Platform) | Wealth.com | New York, New York | 0.52 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 249 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | New York | 0.52 | 0.232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, PostgreSQL |
| 250 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.6725 | 0.2311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 251 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3952 | 0.2311 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 252 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.2311 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 253 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3204 | 0.2311 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 254 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.2311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, DevOps |
| 255 | HPC engineer | Honeywell | Bucuresti, Romania | 0.3203 | 0.2311 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 256 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Honolulu, HI | 0.32 | 0.2311 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 257 | DevOps Specialist | MaintainX | Montreal, Toronto | 0.32 | 0.2311 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 258 | Forward Deployed Software Engineer - Tactical Edge | Palantir | Washington, D.C. | 0.32 | 0.2311 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Backend Engineering |
| 259 | Forward Deployed Infrastructure Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2311 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 260 | Forward Deployed Infrastructure Engineer - US Government | Palantir | Washington, D.C. | 0.32 | 0.2311 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 261 | Software Engineer - Apollo Platform | Palantir | Seattle, WA | 0.32 | 0.2311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 262 | Site Reliability Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.2311 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 263 | Infrastructure Engineer - Early Career | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.2311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 264 | Software Engineer, Developer Experience | Notion | Hyderabad, India | 0.52 | 0.2311 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 265 | Experienced Software Engineer- FSD | Boeing | IND - Bangalore, India | 0.4551 | 0.2198 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 266 | Software Engineer, C++ | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2195 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React, Go |
| 267 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6285 | 0.2189 | ML_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 268 | Data Scientist (Data Science) | Boeing | USA - Everett, WA | 0.4501 | 0.2189 | ML_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 269 | Sr. AI Data Analyst-Agentic Systems & GenAI | GM Financial | Irving, TX, United States / US - Burnett, TX | 0.3452 | 0.2189 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 270 | Senior Machine Learning Engineer, Recommendation & AI Applications | NewsBreak | Mountain View, California, United States | 0.4486 | 0.2189 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, Java |
| 271 | Data Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.5086 | 0.2189 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 272 | Senior SAP FIORI Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 273 | Cloud Application Deployment and Migration Specialist (Mid-Level, Senior or Lead) **Sign on Bonus Potential** | Boeing | USA - Berkeley, MO | 0.5431 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 274 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.5219 | 0.2183 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 275 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.516 | 0.2183 | SWE_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 276 | Service Now Sys Administrator | RTX | US-TX-REMOTE | 0.4761 | 0.2183 | SWE_FULLTIME | Cloud Infrastructure, DevOps |
| 277 | Senior Software Engineer, Network Infrastructure | Palantir | New York, NY | 0.32 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 278 | Forward Deployed Software Engineer - AUS Government | Palantir | Canberra, Australia | 0.32 | 0.2104 | SWE_FULLTIME | Full Stack Development, Java, Python |
| 279 | Forward Deployed Software Engineer | Palantir | Abu Dhabi, United Arab Emirates | 0.32 | 0.2104 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 280 | Software Engineer I | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.455 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 281 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3857 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 282 | Chemical Engr II | Honeywell | Gurugram, Haryana, India | 0.3296 | 0.2093 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, AI Systems, SQL |
| 283 | Software Engr II | Honeywell | Guangzhou, Guangdong, China | 0.326 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 284 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.326 | 0.2093 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, DevOps, Python |
| 285 | Développeuse / Développeur d'intégration | MaintainX | Montreal, Toronto | 0.32 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 286 | Full-Stack Developer - IAM | MaintainX | Toronto | 0.32 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 287 | Software Engineer, AI Product (London, United Kingdom) | Figma | London, England | 0.32 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, React |
| 288 | Platform Engineer - Identity and Access Management (IAM) | Palantir | London, United Kingdom | 0.32 | 0.2093 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 289 | Machine Learning Scientist (Financial Scoring) | Lendbuzz | Boston, MA | 0.32 | 0.2093 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | AI Systems, Data Engineering, Python |
| 290 | Forward Deployed Software Engineer - UK Government | Palantir | London, United Kingdom | 0.32 | 0.2093 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 291 | Software Engineer - Fleet | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 292 | Software Engineer, Data Infrastructure | Notion | Hyderabad, India | 0.52 | 0.2093 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 293 | Software Engineer, Infrastructure  | Notion | Hyderabad, India | 0.52 | 0.2093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Go |
| 294 | Market Operations Engineer | Base Power Company | Austin, TX | 0.52 | 0.2093 | SWE_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 295 | Data Engineer | Base Power Company | Austin, TX | 0.52 | 0.2093 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 296 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.5378 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, Distributed Systems |
| 297 | Intermediate Software Engineer | Achievers | Canada | 0.3565 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 298 | Software Engr II | Honeywell | Shanghai, China | 0.3203 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 299 | Cloud Engineer | Lendbuzz | Tel Aviv | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 300 | Software Engineer - Apollo Platform | Palantir | London, United Kingdom | 0.32 | 0.2083 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 301 | Software Engineer, Robotics | ScaleAI | Argentina; Uruguay | 0.3201 | 0.2062 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 302 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.7039 | 0.2053 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Python |
| 303 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.6658 | 0.2053 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python |
| 304 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4917 | 0.2053 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 305 | Senior AI Engineer II - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.3857 | 0.2053 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 306 | Advanced Software Engineer | Honeywell | Raleigh, NC, United States | 0.3716 | 0.2053 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 307 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - US, Ann Arbor, MI | 0.5639 | 0.2053 | ML_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 308 | Senior Software Engineers | American Express | Phoenix, AZ, United States | 0.352 | 0.2053 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 309 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Remote - US, Ann Arbor, MI | 0.4657 | 0.2053 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 310 | Lead AI Engineer | Honeywell | Atlanta, GA, United States | 0.3203 | 0.2053 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 311 | Software Engineer, AI Product | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.2053 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python |
| 312 | Senior IT Architect | Honeywell | Bucuresti, Romania | 0.3606 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 313 | Senior Software Engineer, Prenatal | BillionToOne | Menlo Park, CA | 0.4432 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 314 | Senior Software Engineer - Internal Tools & Productivity | ScaleAI | San Francisco, CA | 0.5141 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 315 | Lead Software Engineer (Kubernetes) | Appian | McLean, Virginia | 0.514 | 0.1926 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 316 | Lead Software Application – Architect | Boeing | IND - Bangalore, India | 0.4553 | 0.1926 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 317 | Senior AI Engineer I | American Express | LONDON, United Kingdom / Sussex House | 0.3857 | 0.1926 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 318 | Senior Software Engineer | Appian | Chennai, India | 0.3769 | 0.1926 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 319 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1926 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 320 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.1926 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 321 | Senior Front End Engineer | EarnIn | Mountain View, US | 0.4891 | 0.1923 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript |
| 322 | Senior Software Engineer / GTM Platform, Frontend | Ramp | New York, NY (HQ) | 0.52 | 0.1923 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 323 | Senior Software Engineer / Web + Design | Ramp | New York, NY (HQ) | 0.52 | 0.1923 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 324 | Senior Software Engineer (Frontend Focus) | Kira | New York | 0.52 | 0.1923 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 325 | Senior Integration Developer | Monster Energy | USA - Corona, CA | 0.5373 | 0.1917 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 326 | Senior Software Engineer - Vehicle Diagnostics | Torc Robotics | Ann Arbor, MI, Remote, US | 0.3808 | 0.1917 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 327 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.1876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 328 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5968 | 0.1876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 329 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.1876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 330 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.538 | 0.1876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 331 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.1876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 332 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.1876 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 333 | Associate Application Engineer | Appian | McLean, Virginia | 0.359 | 0.1876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL, Java |
| 334 | Application Engr II | Honeywell | Chennai, Tamil Nadu, India | 0.3247 | 0.1876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 335 | Analyst - Data Science | American Express | Singapore, Singapore | 0.2418 | 0.1876 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 336 | Développeur(se) Full-Stack intermédiaire  | MaintainX | Montréal | 0.32 | 0.1876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, React |
| 337 | Intermediate Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, React |
| 338 | Forward Deployed Engineer, GTM, DACH | Notion | Munich, Germany | 0.52 | 0.1876 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, SQL |
| 339 | Forward Deployed Engineer, GTM, France | Notion | Paris, France | 0.52 | 0.1876 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, SQL |
| 340 | Software Engineer, Backend | Base Power Company | Austin, TX | 0.52 | 0.1876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 341 | Forward Deployed Engineer, GTM - Japan | Notion | Tokyo, Japan  | 0.52 | 0.1876 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, TypeScript |
| 342 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.697 | 0.1866 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, DevOps, Python |
| 343 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 344 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4797 | 0.1866 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 345 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4917 | 0.1866 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 346 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4981 | 0.1866 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 347 | Software Control Engr I (C++, SQL, Automation) | Honeywell | Mexico | 0.4549 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 348 | Software Engineer - Hosted Model Infrastructure | Palantir | Washington, D.C. | 0.3691 | 0.1866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 349 | Consultant (Software Implementation, Public Sector) | Appian | McLean, Virginia | 0.359 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, SQL |
| 350 | Consultant (Top Secret Clearance, Software Implementation) | Appian | McLean, Virginia | 0.359 | 0.1866 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 351 | Consultant | Appian | Seville, Spain | 0.359 | 0.1866 | SWE_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 352 | Consultant (Technical, Public Sector) | Appian | Atlanta, Georgia | 0.2733 | 0.1866 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 353 | Software Engineer, Simulation | PlusAI | Santa Clara, CA | 0.3273 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 354 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 355 | Cloud Developer II | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 356 | Software Engr II - C++ Development, QT | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, SQL |
| 357 | Développeur(se) Logiciel de Plateforme | MaintainX | Montreal, Quebec  | 0.32 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, TypeScript |
| 358 | Software Engineer I - Device Drivers | Torc Robotics | Ann Arbor, MI | 0.2833 | 0.1866 | SWE_FULLTIME | Backend Engineering, DevOps, Python |
| 359 | Software Engineer (C#/React) | Reply | Chicago, Illinois | 0.32 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, React |
| 360 | Software Engineer, C++ Middleware and Runtime Infrastructure | PlusAI | Santa Clara, CA | 0.32 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 361 | Forward Deployed Engineer - Mixed Reality | Palantir | Washington, D.C. | 0.32 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 362 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.52 | 0.1866 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 363 | AI Applications Engineer | Notion | San Francisco, California | 0.52 | 0.1866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 364 | Software Engineer - Distributed Simulation Systems | Astera Institute | Emeryville HQ | 0.52 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Backend Engineering, Python |
| 365 | Senior AI Data Infrastructure/Pipeline Engineer | XPENG | Santa Clara, CA | 0.5536 | 0.1795 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 366 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | London, UK | 0.3201 | 0.1795 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, AI Systems |
| 367 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4914 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 368 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3717 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 369 | Senior Software Engineer - Java / AWS Services | Appian | McLean, Virginia | 0.359 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 370 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3398 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 371 | Sr Advanced Software Engr | Honeywell | Singapore, Singapore, Singapore | 0.3296 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 372 | Full-Stack Developer, Connected Data  | MaintainX | Montréal, Toronto | 0.32 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 373 | Senior, ML Engineer - ML Ops Framework  | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5181 | 0.1789 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 374 | Senior Infrastructure Engineer | Northwood Space | Torrance, CA / Washington D.C. | 0.52 | 0.1789 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 375 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.508 | 0.1786 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 376 | Engineer II /Senior Software Engineer, Simulation | Lila Sciences | Cambridge, MA USA | 0.3486 | 0.1786 | SWE_FULLTIME | Python |
| 377 | Scientist/Sr. Scientist, AI Safety | Lila Sciences | Cambridge, MA USA; London, UK; San Francisco, CA USA | 0.5204 | 0.1786 | ML_ENGINEER_FULLTIME | Python |
| 378 | Software Engineer, Graphics & Media | Figma | San Francisco, CA • New York, NY • United States | 0.52 | 0.1786 | SWE_FULLTIME | TypeScript |
| 379 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4553 | 0.1665 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 380 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.1665 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Python |
| 381 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.1665 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Python |
| 382 | Senior Software Engineer | BillionToOne | Menlo Park, CA | 0.4374 | 0.1665 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Python |
| 383 | Lead Software Development Engineer | iSpot | Bellevue, WA | 0.3647 | 0.1665 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 384 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, AI Systems |
| 385 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5695 | 0.1659 | BACKEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 386 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.5385 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 387 | Senior AI Engineer II | American Express | LONDON, LONDON, United Kingdom / Sussex House | 0.3857 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 388 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1659 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 389 | Senior Software Engineer | Appian | Chennai, India | 0.359 | 0.1659 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 390 | Senior Compliance Automation Engineer | True Anomaly | Denver, CO or Long Beach, CA or SF Bay area, CA or Washington, DC | 0.3729 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 391 | Senior Software Engineer - Live Pay | EarnIn | Vancouver, Canada | 0.4769 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 392 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3276 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 393 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 394 | Senior Software Engineer (Backend, Infrastructure Focus) | Kira | San Francisco | 0.52 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 395 | Senior Software Developer, Core Applications | Solink | Ottawa Office | 0.52 | 0.1659 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 396 | Lead Software Engineer | Appian | Chennai, India | 0.359 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 397 | Lead Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 398 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3211 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 399 | Senior Software Engineer, Substrate | Palantir | Washington, D.C. | 0.32 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 400 | Senior Software Engineer, Network Infrastructure | Palantir | Washington, D.C. | 0.32 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 401 | Senior Software Engineer, Substrate | Palantir | Seattle, WA | 0.32 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 402 | Senior Software Engineer, Network Infrastructure | Palantir | Seattle, WA | 0.32 | 0.1653 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 403 | Senior Mobile Engineer (Android) | EarnIn | Mountain View, US | 0.727 | 0.165 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 404 | Senior Software Engineer, iOS | NewsBreak | Mountain View, California, United States | 0.439 | 0.165 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 405 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5377 | 0.1649 | SWE_FULLTIME | Backend Engineering, Java, SQL |
| 406 | GTM Engineer | Greenhouse | Ontario | 0.5276 | 0.1649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript, Python |
| 407 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4916 | 0.1649 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 408 | Application Engineer | Appian | McLean, Virginia | 0.3784 | 0.1649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL, PostgreSQL |
| 409 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.1649 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python, Java |
| 410 | Workday Integrations & Data Architect | EarnIn | Remote, Mexico | 0.36 | 0.1649 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 411 | AI Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1649 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 412 | Strategic Projects Lead - Coding | ScaleAI | India | 0.3204 | 0.1649 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 413 | Analytics Engineer | Podium | Lehi, Utah | 0.3202 | 0.1649 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, SQL, Python |
| 414 | Data Engineer | Lendbuzz | Tel Aviv | 0.3201 | 0.1649 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 415 | SWE Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.1649 | SWE_FULLTIME | AI Systems, Python, Java |
| 416 | Integration Developer  | MaintainX | Miami, Florida | 0.32 | 0.1649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript, React |
| 417 | Integrations Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1649 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript, React |
| 418 | Business Systems Applications Developer | CesiumAstro | Austin, TX | 0.32 | 0.1649 | SWE_FULLTIME | Backend Engineering, SQL, Python |
| 419 | Forward Deployed Engineer | Labelbox | San Francisco Bay Area | 0.3676 | 0.1649 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, SQL |
| 420 | Application Security Engineer | Palantir | London, United Kingdom | 0.32 | 0.1649 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, Java |
| 421 | Application Security Engineer | Palantir | Washington, D.C. | 0.32 | 0.1649 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, Java |
| 422 | Forward Deployed Engineer | Nash | Australia | 0.52 | 0.1649 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python, SQL |
| 423 | Software Engineer, Security | Notion | San Francisco, California | 0.52 | 0.1649 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Python, Go |
| 424 | Application Security Engineer, AI Security | Notion | San Francisco, California | 0.52 | 0.1649 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Python, Go |
| 425 | Data Engineer, People Analytics  | Notion | San Francisco, California | 0.52 | 0.1649 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 426 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5383 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems |
| 427 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1639 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems |
| 428 | Project Engr II | Honeywell | Pune, Maharashtra, India | 0.3247 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 429 | Software Engineer II - MCU Applications (C++/Linux) | Torc Robotics | Ann Arbor, MI | 0.3371 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 430 | Software Engineer - Edge | Palantir | Washington, D.C. | 0.32 | 0.1639 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 431 | High Performance Computing (HPC) Engineer | GenBio AI | Palo Alto, CA | 0.32 | 0.1639 | SWE_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 432 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4552 | 0.1529 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 433 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.1529 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Backend Engineering, Java |
| 434 | Senior Backend Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.1529 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 435 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.5381 | 0.1523 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 436 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.5307 | 0.1523 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Distributed Systems |
| 437 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4913 | 0.1523 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 438 | Senior Software Engineer | Appian | McLean, Virginia | 0.359 | 0.1523 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 439 | Senior Data Engineer | EarnIn | Bengaluru, India | 0.3577 | 0.1523 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 440 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.1523 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 441 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3214 | 0.1523 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 442 | Développeur logiciel senior, facturation | MaintainX | Montréal | 0.32 | 0.1523 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 443 | Senior Software Engineer (Backend Engineering) ⭐ | Achievers | Toronto | 0.32 | 0.1523 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 444 | Senior Data Developer - Streaming | MaintainX | Montreal, Toronto | 0.32 | 0.1523 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 445 | Senior Data Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1523 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 446 | Senior Platform Engineer  | Clarity Innovations | Required  | 0.6497 | 0.1517 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 447 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4915 | 0.1517 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 448 | Data Engineer | Clarity Innovations | Herndon, VA and/or Columbia, MD | 0.4038 | 0.1517 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 449 | Lead Software Engineer | Reply | Atlanta, Georgia | 0.3201 | 0.1517 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 450 | Senior Software Engineer, Substrate | Palantir | London, United Kingdom | 0.32 | 0.1517 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 451 | Forward Deployed Engineer - MTS | Context | San Francisco Office | 0.52 | 0.1432 | SWE_FULLTIME | Python, SQL, Java |
| 452 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.5384 | 0.1422 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, SQL |
| 453 | Experienced Java Software Engineer | Boeing | POL - Gdansk, Poland | 0.5382 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 454 | Application Engr II | Honeywell | Tianjin, China | 0.4915 | 0.1422 | ML_ENGINEER_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | AI Systems, Python |
| 455 | Frontier Agents Engineer | ScaleAI | London, UK | 0.4003 | 0.1422 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 456 | Machine Learning Engineer - LLM, AI & Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.1422 | ML_ENGINEER_FULLTIME | AI Systems, Python, LLM |
| 457 | Machine Learning Engineer, Robotics | XPENG | Santa Clara, CA | 0.4554 | 0.1422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 458 | Forward-deployed Engineer - LatAm (Remote) | Clara | Latin America  | 0.3287 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 459 | Growth Marketing Developer (Desenvolvedor de Growth Marketing) -  São Paulo  (Hybrid | Clara | Latin America  | 0.3287 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 460 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Bogotá (Hybrid) | Clara | Latin America  | 0.3287 | 0.1422 | SWE_FULLTIME | Full Stack Development, SQL |
| 461 | Forward-deployed Engineer - LatAm (Remote) | Clara | São Paulo, São Paulo, Brazil | 0.3287 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 462 | Growth Marketing Developer (Desarrollador de Growth Marketing) - Mexico City (Hybrid) | Clara | Latin America  | 0.3287 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 463 | Machine Learning Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.1422 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 464 | Machine Learning Engineer | True Anomaly | Denver, CO or Long Beach, CA | 0.2967 | 0.1422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 465 | Machine Learning Fellow - Human Frontier Collective (Canada) | ScaleAI | Canada | 0.3201 | 0.1422 | ML_ENGINEER_FULLTIME | Data Engineering, Python |
| 466 | Measurement Software Engineer | Axiomatic AI | Toronto, Canada | 0.32 | 0.1422 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 467 | Scientific Software Engineer - Shuttle Compilation  | QuEra Computing | Tsukuba, Japan | 0.32 | 0.1422 | SWE_FULLTIME | Backend Engineering, Python |
| 468 | Scientific Software Engineer - Hardware Compilation | QuEra Computing | Tsukuba, Japan | 0.32 | 0.1422 | SWE_FULLTIME | Backend Engineering, Python |
| 469 | Scientific Software Engineer - Compiler | QuEra Computing | Tsukuba, Japan | 0.32 | 0.1422 | SWE_FULLTIME | Backend Engineering, Python |
| 470 | Scientific Software Engineer  | QuEra Computing | Toronto, Ontario, Canada | 0.32 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 471 | Scientific Software Engineer - Compiler | QuEra Computing | Harwell, England, UK | 0.2998 | 0.1422 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 472 | Software Engineer - Core Interfaces | Palantir | Palo Alto, CA | 0.32 | 0.1422 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript |
| 473 | Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.1422 | SWE_FULLTIME | Distributed Systems, Python |
| 474 | ML Platform Engineer | Foxglove | San Francisco, CA | 0.52 | 0.1422 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 475 | Algorithms Engineer | Base Power Company | Austin, TX | 0.52 | 0.1422 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 476 | Intermediate AI/ML Engineer | Solink | Ottawa Office | 0.52 | 0.1422 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 477 | Senior Software Engineer, Digital Experiences | BillionToOne | Menlo Park, CA | 0.4374 | 0.1398 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, Django |
| 478 | Lead Software Engineer | Appian | McLean, Virginia | 0.514 | 0.1392 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Java |
| 479 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.5066 | 0.1392 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Go |
| 480 | Senior Quality Engineer I | American Express | Chennai, TN, India | 0.4917 | 0.1392 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 481 | Senior Software Engineer - Java /  Hibernate | Appian | McLean, Virginia | 0.359 | 0.1392 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Java |
| 482 | Senior or Lead Full-Stack Developer  | MaintainX | Montreal, Toronto | 0.32 | 0.1392 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 483 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3856 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 484 | Sr Advanced SW Architect | Honeywell | India | 0.3856 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 485 | Advanced Software Engineer | Honeywell | Gdansk, Pomorskie, Poland | 0.3606 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 486 | Senior Software Engineer - Database Platform | Appian | McLean, Virginia | 0.359 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 487 | Senior Autonomy Software Systems Engineer (Python / C++ / Data) | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3351 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 488 | Edge Infrastructure Engineer | Palantir | Warsaw, Poland | 0.32 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 489 | Senior Software Developer, Compliance and Multi-Region | MaintainX | Montreal, Toronto  | 0.32 | 0.1386 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 490 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.538 | 0.1256 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 491 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4913 | 0.1256 | SWE_FULLTIME | Backend Engineering, AI Systems, Java |
| 492 | Senior Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4796 | 0.1256 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Distributed Systems, Python |
| 493 | Sr. Machine Learning Engineer | EarnIn | Bengaluru, India | 0.3978 | 0.1256 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Python |
| 494 | Senior Software Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.368 | 0.1256 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 495 | Senior Software Engineer  | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.3685 | 0.1256 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 496 | Senior Test Automation Engineer | Appian | Chennai, India | 0.359 | 0.1256 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 497 | Senior Consultant (Public Sector) | Appian | McLean, Virginia | 0.359 | 0.1256 | SWE_FULLTIME | Backend Engineering, Full Stack Development, SQL |
| 498 | Senior Consultant (Public Sector) | Appian | Denver, Colorado | 0.3209 | 0.1256 | SWE_FULLTIME | Backend Engineering, Full Stack Development, SQL |
| 499 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3519 | 0.1256 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 500 | Senior Backend Engineer — ClarOps (Ingeniero Backend Senior de ClarOps) - Remote | Clara | Latin America  | 0.3364 | 0.1256 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 501 | Senior AI Engineer I | BillionToOne | Menlo Park, CA | 0.4123 | 0.1256 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 502 | ML Systems Engineer, Robotics | ScaleAI | San Francisco, CA | 0.5275 | 0.1256 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 503 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1256 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, DevOps, Python |
| 504 | Advanced Data Engineer - GCP | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1256 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 505 | Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3223 | 0.1256 | ML_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, AI Systems, Python |
| 506 | Senior Software Developer, Billing  | MaintainX | Montreal, Toronto | 0.32 | 0.1256 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, TypeScript |
| 507 | Senior AI Engineer - Agentic | Podium | Lehi, Utah, Open to Remote | 0.32 | 0.1256 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Go |
| 508 | Senior Runtime Software Engineer   | d-Matrix | Sydney | 0.52 | 0.1256 | SWE_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 509 | Senior Platform Engineer | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.1256 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Go |
| 510 | Senior Backend Engineer | Nash | San Francisco | 0.52 | 0.1256 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 511 | Senior Full Stack Developer, Data Integrations | Solink | Ottawa Office | 0.52 | 0.1256 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, Python |
| 512 | Sr Software Eng Supervisor | Honeywell | India | 0.5381 | 0.125 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 513 | Cloud Architect | RTX | Warminster, Wiltshire | 0.3858 | 0.125 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems, DevOps |
| 514 | Sr IT Database Administrator | Honeywell | Bengaluru, Karnataka, India | 0.3203 | 0.125 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 515 | Lead Software Engineer | Reply | Chicago, Illinois | 0.3201 | 0.125 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, DevOps |
| 516 | Software Engineer, Production Engineering  (London, United Kingdom) | Figma | London, England | 0.32 | 0.125 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Distributed Systems, Cloud Infrastructure |
| 517 | Senior Machine Learning Infrastructure Engineer | PlusAI | Santa Clara, CA | 0.32 | 0.125 | ML_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 518 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5973 | 0.1205 | SWE_FULLTIME | Python, Java |
| 519 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.1205 | SWE_FULLTIME | Python, Java |
| 520 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.1205 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Java, SQL |
| 521 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5381 | 0.1205 | SWE_FULLTIME | Python, Java |
| 522 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.5379 | 0.1205 | SWE_FULLTIME | Java, Python |
| 523 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.1205 | SWE_FULLTIME | Python, Java |
| 524 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.2496 | 0.1205 | SECURITY_ENGINEER_FULLTIME, SWE_FULLTIME | Python, Java |
| 525 | Application Engr II | Honeywell | Chongqing, China | 0.3247 | 0.1205 | SWE_FULLTIME | Java, TypeScript |
| 526 | Application Engr II | Honeywell | Pune, Maharashtra, India | 0.3218 | 0.1205 | SWE_FULLTIME | Java, TypeScript |
| 527 | AI Strategy Consultant, Frontier Tech | ScaleAI | San Francisco, CA | 0.3201 | 0.1205 | ML_ENGINEER_FULLTIME | Python, SQL |
| 528 | Developer Advocate (Tokyo, Japan) | Figma | Tokyo, Japan | 0.32 | 0.1205 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 529 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI | 0.6276 | 0.1194 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems |
| 530 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.1194 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 531 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.5238 | 0.1194 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | DevOps |
| 532 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.5118 | 0.1194 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering |
| 533 | Software Engineer I, QA | True Anomaly | Denver, CO or Long Beach, CA | 0.2857 | 0.1194 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | DevOps |
| 534 | AI Prompt Engineer | Appian | McLean, Virginia | 0.359 | 0.1194 | SWE_FULLTIME | AI Systems |
| 535 | Software Engineer In Test - Android | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.1194 | SWE_FULLTIME | Backend Engineering |
| 536 | Project Engr I | Honeywell | Tianjin, China | 0.3214 | 0.1194 | SWE_FULLTIME | Backend Engineering |
| 537 | Embedded Software Engineer | Base Power Company | Austin, TX | 0.52 | 0.1194 | SWE_FULLTIME | Backend Engineering |
| 538 | Senior Technical Consultant | Appian | Boston, Massachusetts | 0.3209 | 0.1126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 539 | Senior Technical Consultant | Appian | Madison, Wisconsin | 0.3209 | 0.1126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 540 | Senior Identity Security Engineer | Palantir | Palo Alto, CA | 0.3318 | 0.1126 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Java, Go |
| 541 | Applied AI Engineer, Global Public Sector | ScaleAI | Doha, Qatar; London, UK | 0.3274 | 0.1126 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python, TypeScript |
| 542 | Senior Software Engineer | Astera Institute | Emeryville HQ | 0.52 | 0.1126 | SWE_FULLTIME | Backend Engineering, Java, PostgreSQL |
| 543 | Senior Software Engineer - API Experience | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / Bellevue, WA | 0.52 | 0.1126 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Go |
| 544 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.5385 | 0.112 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Data Engineering, Python |
| 545 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.5381 | 0.112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 546 | Senior Software Engineer - Operating System | Torc Robotics | Ann Arbor, MI | 0.5232 | 0.112 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps, Python |
| 547 | Senior Consultant | Appian | Chennai, India | 0.3905 | 0.112 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Data Engineering, SQL |
| 548 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 549 | Senior Application Integration Engineer | EarnIn | Bengaluru, India | 0.3806 | 0.112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 550 | Senior, ML Engineer - Offline Perception | Torc Robotics | Remote - Canada, Montreal, Canada | 0.5635 | 0.112 | ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 551 | Senior Technical Consultant | Appian | McLean, Virginia | 0.359 | 0.112 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 552 | Senior Consultant | Appian | Tokyo, Japan | 0.359 | 0.112 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 553 | Senior Consultant (Top Secret Clearance) | Appian | McLean, Virginia | 0.359 | 0.112 | SWE_FULLTIME | Full Stack Development, AI Systems, SQL |
| 554 | Senior Consultant (Public Sector) | Appian | Raleigh, North Carolina | 0.3209 | 0.112 | SWE_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 555 | Senior Consultant (Public Sector) | Appian | Atlanta, Georgia | 0.3209 | 0.112 | SWE_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 556 | Software Engr II | Honeywell | India | 0.352 | 0.112 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 557 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.3218 | 0.112 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 558 | Advanced Chemical Engr (Digital Exec Tools Specialist’) | Honeywell | India | 0.3218 | 0.112 | ML_ENGINEER_FULLTIME | DevOps, Data Engineering, Python |
| 559 | Advanced Data Engineer | Honeywell | Pune, Maharashtra, India | 0.3202 | 0.112 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 560 | Senior Applied Scientist, Scheduling and Optimization | MaintainX | Canada (Remote) | 0.32 | 0.112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 561 | Développeur(se) de logiciel senior spécialisé en moteurs de recherche | MaintainX | Montréal, Toronto | 0.32 | 0.112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 562 | Senior Software Engineer, Mapping & Localization | PlusAI | Santa Clara, CA | 0.32 | 0.112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 563 | Sr. Site Development Engineer | Mariana Minerals | San Francisco HQ | 0.52 | 0.112 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 564 | Senior Simulation Engineer | Northwood Space | Torrance, CA | 0.52 | 0.112 | SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 565 | Senior AI Developer (Coming Soon!) | Nuclear Promise X | Canada | 0.52 | 0.112 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 566 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.5384 | 0.0989 | DATA_ENGINEER_FULLTIME, DATA_SCIENTIST_FULLTIME | Data Engineering, SQL, Python |
| 567 | Sr Advanced AI Data Engineer | Honeywell | Monterrey, NLE, Mexico | 0.3218 | 0.0989 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 568 | Senior Data Infrastructure Engineer | Voltus | Remote | 0.3213 | 0.0989 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 569 | Développeur(se) Full-Stack sénior ou en chef  | MaintainX | Montréal | 0.32 | 0.0989 | FULLSTACK_ENGINEER_FULLTIME, SWE_FULLTIME | Full Stack Development, TypeScript, React |
| 570 | Senior Data Developer, Governance  | MaintainX | Montreal, Toronto | 0.32 | 0.0989 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 571 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.52 | 0.0989 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 572 | Senior IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.5384 | 0.0983 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 573 | Sr IT Architect | Honeywell | Pune City, Maharashtra, India | 0.4915 | 0.0983 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 574 | Advanced Embedded Engineer | Honeywell | United Kingdom | 0.3717 | 0.0983 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 575 | Sr IT Engineer | Honeywell | Hyderabad, Telangana, India | 0.3716 | 0.0983 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps |
| 576 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3606 | 0.0983 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 577 | Sr Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3237 | 0.0983 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering |
| 578 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.0983 | SWE_FULLTIME | DevOps, Cloud Infrastructure |
| 579 | Azure Cloud Architect | Reply | Detroit Area, Michigan | 0.32 | 0.0983 | SWE_FULLTIME | Cloud Infrastructure, Backend Engineering |
| 580 | Azure Cloud Architect | Reply | Chicago, Illinois | 0.32 | 0.0983 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 581 | Azure Cloud Architect | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.0983 | SWE_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, Distributed Systems |
| 582 | Senior .NET Developer | Nuclear Promise X | Chalk River | 0.52 | 0.0983 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 583 | Appian Product Engineer  | Appian | McLean, Virginia | 0.584 | 0.0977 | SWE_FULLTIME | SQL |
| 584 | Advanced SW Test Engineer (m/f/d) | Honeywell | Ratingen, Nordrhein-Westfalen, Germany | 0.5381 | 0.0977 | SWE_FULLTIME | Python |
| 585 | Application Engr I | Honeywell | Chennai, Tamil Nadu, India | 0.3223 | 0.0977 | SWE_FULLTIME | Python |
| 586 | Machine Learning Fellow - Human Frontier Collective (UK) | ScaleAI | United Kingdom | 0.2401 | 0.0977 | ML_ENGINEER_FULLTIME | Python |
| 587 | Forward Deployed AI Engineer | Palantir | London, United Kingdom | 0.32 | 0.0977 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 588 | Software Engineer, Developer and Qualification Tools | d-Matrix | Santa Clara | 0.52 | 0.0977 | SWE_FULLTIME | Python |
| 589 | Applied ML Engineer | Foxglove | San Francisco, CA | 0.52 | 0.0977 | ML_ENGINEER_FULLTIME | Python |
| 590 | Software Engineer, AI Capture | Notion | San Francisco, California | 0.52 | 0.0977 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Python |
| 591 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.0853 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 592 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5377 | 0.0853 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 593 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 594 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.71 | 0.0853 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 595 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4918 | 0.0853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 596 | Developpeur SAP ABAP  /  SAP ABAP Developer | RTX | CA-QC-LONGUEUIL-J01 ~ 1000 Blvd Marie-Victorin ~ J01 BLDG | 0.3858 | 0.0853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 597 | Senior Associate - Oracle Technical Developer | American Express | Gurugram, HR, India | 0.3717 | 0.0853 | SWE_FULLTIME | Backend Engineering, SQL |
| 598 | Senior Applied Scientist, Parts Intelligence & Inventory Optimization | MaintainX | Canada (Remote) | 0.3599 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 599 | Senior Technical Consultant | Appian | Toronto, Canada | 0.359 | 0.0853 | SWE_FULLTIME | Backend Engineering, SQL |
| 600 | Senior Applied Machine Learning Engineer, Asset Intelligence | MaintainX | San Francisco (Remote) | 0.3581 | 0.0853 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 601 | Senior, ML Engineer - Neural Rendering | Torc Robotics | Montreal, Canada, Remote - Canada | 0.4293 | 0.0853 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 602 | Senior Machine Learning Engineer - Foundation Model | XPENG | Santa Clara, CA | 0.5216 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 603 | Senior Machine Learning Engineer - AI Foundation | XPENG | Santa Clara, CA | 0.5216 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 604 | Sr Advanced AI Engr | Honeywell | Bengaluru, Karnataka, India | 0.3322 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 605 | Senior Software Engineer, Calibration | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.3853 | 0.0853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 606 | Senior Software Engineer, Calibration | Torc Robotics | Remote - Canada, Montreal, Canada | 0.3253 | 0.0853 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 607 | Senior Software Engineer | EarnIn | Bengaluru, India | 0.3201 | 0.0853 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, TypeScript |
| 608 | Développeur de données senior | MaintainX | Montreal, Toronto | 0.32 | 0.0853 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, SQL, data pipelines |
| 609 | Développeur(euse) de données sénior, gouvernance des données | MaintainX | Montréal, Toronto | 0.32 | 0.0853 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL |
| 610 | Senior Computer Vision/AI  Engineer | BrightAI | Palo Alto, CA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 611 | Senior Machine Learning Engineer II | CesiumAstro | Austin, TX | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Python |
| 612 | Senior Research Engineer, Controls | PlusAI | Santa Clara, CA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 613 | Senior Software Engineer, Planning | PlusAI | Santa Clara, CA | 0.32 | 0.0853 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Distributed Systems, Python |
| 614 | Senior AI Engineer | Reply | Seattle, Washington | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 615 | Senior AI Engineer, Time-Series Signal Processing | BrightAI | Palo Alto, CA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 616 | Senior AI Engineer – LLM, RAG | BrightAI | Palo Alto, CA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python, LLM |
| 617 | Senior AI Engineer | Reply | Chicago, Illinois | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 618 | Senior AI Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 619 | Senior Software Engineer (PHP/ Golang) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.0853 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Go |
| 620 | Senior Machine Learning Engineer, Perception | PlusAI | Santa Clara, CA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 621 | Senior Machine Learning Engineer, Simulation | PlusAI | Santa Clara, CA | 0.32 | 0.0853 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Python, data pipelines |
| 622 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5971 | 0.075 | SWE_FULLTIME | — |
| 623 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5381 | 0.075 | SWE_FULLTIME | — |
| 624 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.075 | SWE_FULLTIME | — |
| 625 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4548 | 0.075 | SWE_FULLTIME | — |
| 626 | Software Engineer In Test - iOS | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.3452 | 0.075 | SWE_FULLTIME | — |
| 627 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.3209 | 0.075 | PRODUCT_MANAGER_FULLTIME, SWE_FULLTIME | — |
| 628 | Mixed Reality Developer | Palantir | Washington, D.C. | 0.32 | 0.075 | SWE_FULLTIME | — |
| 629 | Software Engineer, Product | Base Power Company | Austin, TX | 0.52 | 0.075 | SWE_FULLTIME | — |
| 630 | Senior UX Design Engineer, Design Systems | Greenhouse | Ontario | 0.4975 | 0.0723 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript |
| 631 | Senior Software Engineer, Front End | True Anomaly | Denver, CO or Long Beach, CA | 0.4886 | 0.0723 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 632 | Sr. Software Engineer, React/ React Native | Prosper | San Francisco, CA | 0.32 | 0.0723 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | React, TypeScript |
| 633 |  Senior Software Engineer, Visualization | Foxglove | San Francisco, CA | 0.52 | 0.0723 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript, React |
| 634 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.6418 | 0.0717 | DATA_ENGINEER_FULLTIME | Data Engineering |
| 635 | Senior Embedded Software Engineer II | CesiumAstro | Westminster, CO | 0.3313 | 0.0717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 636 | Senior Software Developer, Search  | MaintainX | Montreal, Toronto | 0.32 | 0.0717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems |
| 637 | Senior Software Engineers | Achievers | Toronto | 0.32 | 0.0717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 638 | Senior Data Engineer | Reply | Kochi, Kerala | 0.32 | 0.0717 | DATA_ENGINEER_FULLTIME | Data Engineering |
| 639 | Senior Embedded Software Integration Engineer | PlusAI | Chicago, IL | 0.32 | 0.0717 | SWE_FULLTIME | Backend Engineering |
| 640 | Senior Software Engineer—Kernels | d-Matrix | Bangalore | 0.52 | 0.0717 | SWE_FULLTIME | Backend Engineering |
| 641 | Senior .NET Developer (Coming Soon!) | Nuclear Promise X | Ontario / Remote | 0.52 | 0.0717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 642 | Senior Mobile Security Engineer (Forensics) | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.0586 | MOBILE_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python |
| 643 | Senior Front End Software Engineer - Application Development | Palantir | London, United Kingdom | 0.32 | 0.0586 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | TypeScript |
| 644 | Senior React Native Engineer — Driver App  | Nash | Remote HQ / San Francisco | 0.52 | 0.0586 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | TypeScript |
| 645 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.538 | 0.045 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 646 | Senior iOS Engineer | GeoComply | Ho Chi Minh, Vietnam | 0.32 | 0.045 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |

---

## iCIMS connector validation (2026-06-12)

**Company:** SRI International (`platform=icims`, `board_token=sri`, `https://careers-sri.icims.com`)

### Unit tests

```
cd job_ingestion && pytest tests/test_icims_connector.py tests/test_extractors.py -q
# 32 passed
```

### Live fetch (curl_cffi Chrome impersonation)

Plain `httpx`/curl requests returned HTTP 405 from iCIMS bot protection. Connector updated to use `curl_cffi` with `impersonate=chrome120`.

| Check | Result |
|-------|--------|
| Jobs fetched | 36 |
| Missing title | 0 |
| Missing raw_html | 0 |
| Fetch runtime | ~82s (2s delay per detail) |
| Sample `id=6414` | Finance Project Analyst, US-CA-Menlo Park, Accounting/Finance, Full-time, 6221-char description |

### Pipeline ingestion

Ran `run_pipeline` with only SRI active:

| Metric | Value |
|--------|-------|
| jobs_fetched | 36 |
| jobs_new | 36 |
| jobs_updated | 0 |
| pipeline status | completed |

### Enrichment (4 parallel Gemini workers)

`python scripts/parallel_gemini_drain_today.py --launch-all --reset-stuck --worker-count 4`

| Metric | Value |
|--------|-------|
| queued | 36 |
| completed | 36 |
| processing_state=success | 36 |
| opportunity_score set | 36 |
| failed | 0 |
| worker runtime | ~71s |

Sample enriched jobs: Analog IC Design Engineer (Hardware_Electrical, MID), Data Solutions and Data Integration Lead (Business, SENIOR), Bioscience Research Associate I (Research_Science, ENTRY).
