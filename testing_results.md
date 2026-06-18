# User Recommendation Results

Generated 2026-06-14 17:11 UTC (7,395 recommendation-eligible active jobs, 7,434 active normalized rows, 24,499 archived identities, 194 active companies; domain_filter=True, role_intent_filter=True, clearance_filter=True, sponsorship_score=False).

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
| Naman Kothari | 497 | 0.066–0.4906 | 166 | `BACKEND_ENGINEER_FULLTIME`, `SWE_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME` (+1) |
| Ram Parekh | 401 | 0.063–0.5875 | 59 | `SWE_FULLTIME`, `DATA_SCIENTIST_FULLTIME`, `ML_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME` |
| Nishant Jethwa | 488 | 0.036–0.4195 | 144 | `BACKEND_ENGINEER_FULLTIME`, `SWE_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`, `DEVOPS_ENGINEER_FULLTIME` |
| Ishan Bhutada | 131 | 0.06–0.58 | 29 | `DATA_ANALYST_FULLTIME`, `DATA_SCIENTIST_FULLTIME`, `SWE_FULLTIME` |
| Soham Navandar | 418 | 0.018–0.495 | 92 | `DATA_SCIENTIST_FULLTIME`, `SWE_FULLTIME`, `DATA_ANALYST_FULLTIME`, `SOLUTIONS_CONSULTANT_FULLTIME` |
| Yatharth Mogra | 370 | 0.0766–0.4321 | 120 | `DATA_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`, `SWE_FULLTIME` |

---

## Naman Kothari (`naman@example.com`)

**Candidate ID:** `e4262e5b-a8e4-4b18-8912-23604b3fbdef`

### Subscribed pools
- `BACKEND_ENGINEER_FULLTIME`
- `SWE_FULLTIME`
- `FULLSTACK_ENGINEER_FULLTIME`
- `DATA_ENGINEER_FULLTIME`
- `ML_ENGINEER_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Backend Engineering, Frontend Engineering, Full Stack Development, AI Systems, Machine Learning, Cloud Infrastructure, Security Engineering |
| Preferred locations | USA, California |
| Primary roles | Backend Engineer, Full Stack Engineer, Software Engineer, Data Engineer, Machine Learning Engineer, AI Engineer |
| Hard constraints | sponsorship=True, min_salary=None, target_seniority=INTERN, NEW_GRAD, ENTRY, JUNIOR, MID |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 497
- **Notification-eligible jobs (≤60d, not yet emailed):** 497
- **Personal score range:** 0.066 – 0.4906 (166 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `BACKEND_ENGINEER_FULLTIME` | 321 |
| `SWE_FULLTIME` | 282 |
| `FULLSTACK_ENGINEER_FULLTIME` | 89 |
| `ML_ENGINEER_FULLTIME` | 79 |
| `DEVOPS_ENGINEER_FULLTIME` | 55 |
| `DATA_ENGINEER_FULLTIME` | 51 |
| `FRONTEND_ENGINEER_FULLTIME` | 29 |
| `SECURITY_ENGINEER_FULLTIME` | 10 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 7 |
| `SUPPORT_ENGINEER_FULLTIME` | 4 |
| `MOBILE_ENGINEER_FULLTIME` | 4 |
| `RESEARCH_SCIENTIST_FULLTIME` | 2 |
| `DATA_SCIENTIST_FULLTIME` | 2 |
| `DATA_ANALYST_FULLTIME` | 2 |
| `SYSTEMS_ENGINEER_FULLTIME` | 1 |
| `MARKETING_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Software Engineer, Full-Stack @ Loop

- **Location:** San Francisco, CA (unclear)
- **Posted:** 2026-06-08T17:04:05+00:00
- **Salary:** 150000 – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.4343
- **Personal score:** 0.4906
- **Pools:** `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** FULLSTACK_ENGINEER
- **Capabilities:** Full Stack Development, Backend Engineering, Frontend Engineering, Cloud Infrastructure
- **Skills:** distributed systems, logistics software
- **Match reasons:** Full Stack Development, Backend Engineering, Frontend Engineering, Cloud Infrastructure, TypeScript
- **URL:** https://job-boards.greenhouse.io/loop/jobs/4102236004

#### #2 — Software Engineer II @ Cox

- **Location:** Atlanta GA (unclear)
- **Posted:** 2026-06-10T00:00:00+00:00
- **Salary:** 89400 – 134000
- **Effort:** MEDIUM
- **Opportunity score:** 0.3996
- **Personal score:** 0.4456
- **Pools:** `SWE_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, FULLSTACK_ENGINEER
- **Capabilities:** Full Stack Development, Cloud Infrastructure, Backend Engineering, Frontend Engineering
- **Skills:** system integration, secure coding
- **Match reasons:** Full Stack Development, Cloud Infrastructure, Backend Engineering, Frontend Engineering, TypeScript
- **URL:** https://cox.wd1.myworkdayjobs.com/Cox_External_Career_Site_1/job/Atlanta-GA/Software-Engineer-II_R202678357

#### #3 — Software Engineer, Machine Learning @ Whoop

- **Location:** Boston, MA (unclear)
- **Posted:** 2026-06-11T18:40:49.846000+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5388
- **Personal score:** 0.4335
- **Pools:** `ML_ENGINEER_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** ML_ENGINEER, BACKEND_ENGINEER
- **Capabilities:** Machine Learning, Backend Engineering, Full Stack Development
- **Skills:** machine learning models, production services, API design, observability
- **Match reasons:** Machine Learning, Backend Engineering, Full Stack Development, Java, PostgreSQL
- **URL:** https://jobs.lever.co/whoop/d8b1c557-bf1a-40ca-850a-74d4e91728fe

#### #4 — AI Engineer III - Agentic AI @ American Express

- **Location:** Phoenix, AZ, United States (unclear)
- **Posted:** 2026-06-12T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5497
- **Personal score:** 0.4242
- **Pools:** `ML_ENGINEER_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** ML_ENGINEER, BACKEND_ENGINEER
- **Capabilities:** Machine Learning, AI Systems, Backend Engineering, Distributed Systems
- **Skills:** LLM, agentic AI, RAG
- **Match reasons:** Machine Learning, AI Systems, Backend Engineering, Python, Go
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26007444/details

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Software Engineer, Full-Stack | Loop | San Francisco, CA | 0.4343 | 0.4906 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 2 | Software Engineer II | Cox | Atlanta GA | 0.3996 | 0.4456 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Backend Engineering |
| 3 | Software Engineer II | Cox | Atlanta GA | 0.3987 | 0.4456 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 4 | Software Engineer, Machine Learning | Whoop | Boston, MA | 0.5388 | 0.4335 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Full Stack Development |
| 5 | AI Engineer III - Agentic AI | American Express | Phoenix, AZ, United States | 0.5497 | 0.4242 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Backend Engineering |
| 6 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.4242 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 7 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4469 | 0.4242 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Backend Engineering |
| 8 | ML Engineer, Generative Video | Mirage | Union Square, New York City | 0.5091 | 0.4057 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Cloud Infrastructure |
| 9 | Software Engineer (Front End) | CACI | Aurora, CO, US | 0.3868 | 0.3977 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Frontend Engineering, Backend Engineering, Cloud Infrastructure |
| 10 | Software Engineer 2 | Berkshire Hathaway Energy | Des Moines, IA, United States | 0.4628 | 0.3964 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 11 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.3885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 12 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.3885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 13 | Software Engineer, Full-Stack | Loop | New York, NY, USA | 0.4357 | 0.3885 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 14 | Software Engineer, Full-Stack | Loop | Chicago, IL | 0.4356 | 0.3885 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 15 | AI Builder Partner Solutions | Salesforce | California - San Francisco | 0.6822 | 0.3792 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 16 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5344 | 0.3792 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 17 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.3792 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 18 | Cloud Developer | Freedom Technology Solutions Group | Chantilly, VA | 0.5985 | 0.3763 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, Java |
| 19 | Software Engineer II | Cox | Atlanta GA | 0.4239 | 0.3699 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Security Engineering |
| 20 | Factory Software Engineer (Starlink) | SpaceX | Bastrop, TX | 0.4246 | 0.3671 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 21 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.3607 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 22 | Software Engineering I | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.3607 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 23 | Software Engineer - Defense Applications | Palantir | New York, NY | 0.5474 | 0.3578 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | Frontend Engineering, AI Systems, React |
| 24 | Software Development Engineer I - General Motors Insurance | GM Financial | United States | 0.5005 | 0.3578 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 25 | Software Development Engineer II - General Motors Insurance | GM Financial | United States | 0.5005 | 0.3578 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 26 | Network Engineer 1/Network Engineer 2/Network Engineer 3 | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4318 | 0.3578 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 27 | Software Engineer, Network Monitoring (Starlink) | SpaceX | Hawthorne, CA | 0.4365 | 0.3498 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Python |
| 28 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.5272 | 0.3485 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, Python |
| 29 | ML Engineer, Agentic Systems | Mirage | Union Square, New York City | 0.5075 | 0.3485 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Python |
| 30 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.4877 | 0.3485 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 31 | Software Engineer | Intel | US, Arizona, Phoenix | 0.6671 | 0.3406 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C# |
| 32 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.3406 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Java |
| 33 | Software Engineer, Test Infrastructure (Application Software) | SpaceX | Hawthorne, CA | 0.4754 | 0.3406 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C++ |
| 34 | Software Engineer II - 20202 | Cox | Atlanta GA | 0.3445 | 0.3406 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 35 | Marketing Productivity Engineer | Sigma Computing | San Francisco, CA | 0.626 | 0.3313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, TypeScript |
| 36 | Software Engineer I (AI Driven) | Travelers | GA - Atlanta | 0.5232 | 0.3221 | SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 37 | Software Engineer I | Cox | Austin TX | 0.4688 | 0.3221 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 38 | Support AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.6949 | 0.3221 | BACKEND_ENGINEER_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 39 | Software Engineer II | Cox | Austin TX | 0.4597 | 0.3221 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C# |
| 40 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, Aliso Viejo, CA | 0.5298 | 0.3221 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 41 | Software Engineer, Hardware-in-the-Loop (Starlink) | SpaceX | Redmond, WA | 0.4987 | 0.3221 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 42 | Software Engineer for Data at Rest (DAR) Crypto & Cross Domain Solutions | General Dynamics Mission Systems | US-MA-Dedham | 0.4222 | 0.3221 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Security Engineering, Rust |
| 43 | Software Engineer | Aquatic Capital Management | New York | 0.608 | 0.3221 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, Python |
| 44 | Software Engineer, Developer Productivity  | Glean | Mountain View, CA | 0.4989 | 0.3221 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, Java |
| 45 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.549 | 0.3192 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C#, Python |
| 46 | Software Engineer II, EV | EnergyHub | Remote - United States | 0.4311 | 0.3185 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 47 | Software Engineer II (Java) | Sony Interactive Entertainment | United States, Madison, WI | 0.5699 | 0.3128 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 48 | Software Engineer, Platform | ScaleAI | San Francisco, CA; New York, NY | 0.6413 | 0.3128 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, PostgreSQL |
| 49 | Data Engineer | Base Power Company | Austin, TX | 0.4691 | 0.3099 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 50 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4755 | 0.3099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, SQL |
| 51 | Experienced Fullstack Software Engineer | Boeing | POL - Gdansk, Poland | 0.5002 | 0.3042 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 52 | AI-Enabled Full Stack Developer - Experienced | Micron Technology | Taichung - AATT, Taiwan | 0.4617 | 0.3042 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Cloud Infrastructure |
| 53 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.3035 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, SQL |
| 54 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.6717 | 0.3035 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 55 | Software Engineer | General Dynamics Mission Systems | US-MA-Pittsfield | 0.4726 | 0.3035 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C++ |
| 56 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.3035 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, C++ |
| 57 | Computing Architect (Manhattan Warehouse M.S.) | Boeing | USA - Hialeah, FL | 0.4289 | 0.3035 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 58 | Software Engineer | General Dynamics Mission Systems | US-MA-Pittsfield | 0.3431 | 0.3035 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C++ |
| 59 | Applied Researcher II (AI Foundations) | Capital One | New York, NY | 0.5285 | 0.3035 | RESEARCH_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 60 | Full Stack Developer (Remote) | RTX | US-CT-REMOTE | 0.4136 | 0.3035 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Python |
| 61 | Embedded Software Engineer - Electrification | General Motors | Milford, Michigan, United States of America | 0.5495 | 0.3007 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 62 | Data Engineer I | University of Texas at Austin | AUSTIN, TX | 0.2797 | 0.3007 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 63 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.4115 | 0.3007 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 64 | Java API Back End Developer | RELX | Pennsylvania | 0.5053 | 0.2999 | BACKEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 65 | Software Engineer ll - Java 8 Reactjs Web Search Team | American Express | Phoenix, AZ, United States | 0.5327 | 0.2999 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 66 | Full‑Stack Machine Learning Engineer | LexisNexis Risk Solutions | UK - London (London Wall) | 0.5016 | 0.2949 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Full Stack Development |
| 67 | Software Engineer II | American Express | Gurugram, HR, India | 0.4632 | 0.2949 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 68 | DevSecOps Software Engineer (Associate or Experienced), Phantom Works | Boeing | USA - Saint Charles, MO | 0.3778 | 0.2943 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 69 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.599 | 0.2943 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems |
| 70 | Software Engineer, Compute Infrastructure | Glean | Mountain View, CA | 0.5245 | 0.2943 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 71 | Associate and Experienced Software Engineers - Secure Network & Protocols | Boeing | USA - Oklahoma City, OK | 0.2598 | 0.2943 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 72 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3632 | 0.2927 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 73 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5797 | 0.2914 | SWE_FULLTIME | Backend Engineering, Python |
| 74 | Software Engineer - Core Interfaces | Palantir | New York, NY | 0.5451 | 0.2914 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Frontend Engineering, JavaScript |
| 75 | Embedded Software Engineer II | CesiumAstro | El Segundo, CA | 0.4757 | 0.2914 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 76 | Embedded Software Engineer II | CesiumAstro | Austin, TX | 0.4757 | 0.2914 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 77 | Embedded Software Engineer II | CesiumAstro | Westminster, CO | 0.4757 | 0.2914 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 78 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4755 | 0.2888 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 79 | Software Engineer II - AI Focused | Cadence Design Systems | BELO HORIZONTE | 0.549 | 0.2878 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, C++ |
| 80 | Software Engineer I | LexisNexis Risk Solutions | Cardiff | 0.5806 | 0.2878 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Go |
| 81 | Sr Lead Software Engineer (Full Stack) | Capital One | McLean, VA | 0.6252 | 0.284 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Backend Engineering |
| 82 | Lead Software Engineer, Full Stack (Golang, Angular, AWS) | Capital One | Richmond, VA | 0.5221 | 0.284 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 83 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.2834 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 84 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.2834 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 85 | Information & Application Developer (Entry Level and Associate) | Boeing | USA - North Charleston, SC | 0.4034 | 0.2834 | SWE_FULLTIME, DATA_ANALYST_FULLTIME | Backend Engineering, Python, SQL |
| 86 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3242 | 0.2834 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 87 | Site Reliability Engineer II | PROS Holdings, Inc. | USA TX Houston Virtual | 0.5814 | 0.2821 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 88 | Embedded SW Development Engineer | GE Vernova | Zamudio | 0.4314 | 0.2785 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C++ |
| 89 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2785 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 90 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5771 | 0.2785 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 91 | Lead Software Engineer, Full Stack | Capital One | Richmond, VA | 0.53 | 0.2785 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 92 | Software Engineer - SDET | Sigma Computing | San francisco, CA | 0.5848 | 0.2742 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Rust, Go |
| 93 | Entry Level Software Engineer - Austin, TX | Cox | Austin TX | 0.3807 | 0.2742 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C#, Java |
| 94 | Infrastructure Engineer | RTX | Gloucester, South Gloucestershire | 0.4198 | 0.2693 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering |
| 95 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2674 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 96 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2674 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 97 | Lead AI Engineer (MLX) | Capital One | New York, NY | 0.5535 | 0.2674 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 98 | Senior Software Engineer  | Axiomatic AI | Boston, US | 0.5196 | 0.2656 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 99 | Solutions Architect | Centerfield | Los Angeles, California | 0.4688 | 0.2656 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Full Stack Development |
| 100 | Associate Engineer - Fullstack (Hybrid) | RTX | IN-TS-HYDERABAD-B3F7 ~ DLF Cybercity Gachibowli ~ DLF CYBERCITY GACHIBOWLI-B3F7, 7th Fl in Block 3 | 0.5015 | 0.2656 | FULLSTACK_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Full Stack Development, Frontend Engineering, JavaScript |
| 101 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, San Diego, CA | 0.5283 | 0.2649 | SWE_FULLTIME | Full Stack Development, Python, JavaScript |
| 102 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.4929 | 0.2618 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Backend Engineering |
| 103 | IT Engineer | Micron Technology | Fab 10W, Singapore | 0.4874 | 0.2563 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C# |
| 104 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4251 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 105 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI, Fort Worth, TX | 0.6387 | 0.2557 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, C++, Python |
| 106 | Data Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.2557 | DATA_ENGINEER_FULLTIME | Machine Learning, SQL, Python |
| 107 | Quality Engineer II | RELX | Philadelphia, PA | 0.4851 | 0.2557 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, JavaScript, TypeScript |
| 108 | Software Engineer I | LivaNova | Houston, Texas, United States | 0.4256 | 0.2557 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | Backend Engineering, C#, C++ |
| 109 | Software Engineer, CDN  (Starlink) | SpaceX | Redmond, WA | 0.4769 | 0.2557 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Rust |
| 110 | Software Infrastructure Engineer (Starlink) | SpaceX | Palo Alto, CA | 0.4885 | 0.2557 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, C++ |
| 111 | Software Infrastructure Engineer (Starlink) | SpaceX | Redmond, WA | 0.4691 | 0.2557 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, C++ |
| 112 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Palo Alto, CA | 0.4864 | 0.2557 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 113 | Software Engineer I, Service Network - Slack | Slack (Salesforce) | Washington - Seattle | 0.4673 | 0.2557 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Go, Python |
| 114 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.2545 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 115 | CAD Engineer | Micron Technology | Richardson, TX | 0.5796 | 0.2528 | SWE_FULLTIME | Python, C++, Java |
| 116 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.6624 | 0.2521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, TypeScript |
| 117 | (Remote) System Analyst/Software Developer | Harris Computer | Office - Blair | 0.3286 | 0.2521 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, C# |
| 118 | AI Prompt Engineer | CACI | Remote (Any State) | 0.322 | 0.2521 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 119 | Software Engineer - Frontend/Full Stack | Sony Interactive Entertainment | Ireland, Dublin | 0.3649 | 0.2499 | BACKEND_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 120 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5015 | 0.2471 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 121 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.2471 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 122 | Continuous Integration/Continuous Development Engineer | Monster Energy | USA - Corona, CA | 0.5845 | 0.2464 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, C# |
| 123 | 2026 Raytheon Full Time-Software Engineer I – EOIR Advanced Products and Solutions (Onsite) | RTX | US-TX-MCKINNEY-513WC ~ 2501 W University Dr ~ WING C BLDG | 0.3632 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 124 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 125 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 126 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Redmond, WA | 0.4574 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 127 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Palo Alto, CA | 0.4864 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 128 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 129 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.2464 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 130 | RAN Validation Engineer (Starlink Mobile)  | SpaceX | Sunnyvale, CA | 0.4866 | 0.2464 | SWE_FULLTIME | Backend Engineering, Python |
| 131 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6359 | 0.2442 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 132 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6358 | 0.2442 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 133 | Lead Software Engineer, Fullstack (React, Java, Python) | Capital One | New York, NY | 0.6247 | 0.2442 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 134 | Senior Lead Software Engineer, Full Stack (Global Payment Network) | Capital One | Riverwoods, IL | 0.6053 | 0.2442 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 135 | Lead Software Engineer | Cox | Austin TX | 0.499 | 0.2442 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 136 | Senior Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.6085 | 0.2442 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 137 | Forward Deployed Engineer I/II | Giga AI | San Francisco | 0.5602 | 0.2435 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | React, Python |
| 138 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.4632 | 0.2435 | DATA_ENGINEER_FULLTIME | SQL, Python |
| 139 | Forward Deployed Engineer  | Loop | San Francisco, CA | 0.4398 | 0.2435 | SWE_FULLTIME | Python, SQL |
| 140 | Software Engineer, Agents  | Mirage | Union Square, New York City | 0.5078 | 0.2434 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, AI Systems |
| 141 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.5603 | 0.2428 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C++ |
| 142 | Software Engineer II, AI Platform | Cadence Design Systems | SAN JOSE | 0.4236 | 0.2428 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 143 | Roku Engineer | TribalScale | Remote Office | 0.5331 | 0.2399 | MOBILE_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Kotlin, Java |
| 144 | Product Engineer | Linear | North America | 0.4519 | 0.2399 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript, React |
| 145 | Machine Learning Engineer, Asia | Manulife Financial | Manulife Tower, Manulife (Singapore) Pte Ltd | 0.5328 | 0.2378 | ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 146 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5004 | 0.2378 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Security Engineering, Java |
| 147 | Développeur de logiciel | Harris Computer | Quebec, Canada | 0.3817 | 0.2378 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Node.js |
| 148 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5114 | 0.2371 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering |
| 149 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5109 | 0.2371 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 150 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6284 | 0.2335 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 151 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5616 | 0.2335 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 152 | Senior Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.4619 | 0.2335 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 153 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4198 | 0.2335 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 154 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2331 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 155 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2331 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 156 | Senior Lead AI Engineer,(MLX, Agentic AI, Gen AI platform Services) | Capital One | San Jose, CA | 0.6325 | 0.2331 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Cloud Infrastructure |
| 157 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2331 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Cloud Infrastructure |
| 158 | Senior Lead AI Engineer (Gen AI Platform Services) | Capital One | San Jose, CA | 0.6085 | 0.2331 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Cloud Infrastructure |
| 159 | Appian Product Engineer  | Appian | McLean, Virginia | 0.4941 | 0.2307 | SWE_FULLTIME | Full Stack Development, SQL, Java |
| 160 | Associate Software Engineer - Analytics | Boeing | IND - Bangalore, India | 0.5019 | 0.2285 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Python |
| 161 | Forward Deployed Engineer | Nash | Australia | 0.5319 | 0.2285 | BACKEND_ENGINEER_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 162 | Application Engr II | Honeywell | Tianjin, China | 0.4316 | 0.2285 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Python |
| 163 | Senior Lead AI Engineer (GenAI Platform Services) | Capital One | San Jose, CA | 0.7497 | 0.2275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Cloud Infrastructure |
| 164 | Senior Software Engineer | Cox | Atlanta GA | 0.4445 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Cloud Infrastructure |
| 165 | Lead AI Engineer (AI Foundations, LLM Customization and Finetuning) | Capital One | Cambridge, MA | 0.5782 | 0.2275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Backend Engineering |
| 166 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5781 | 0.2275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Cloud Infrastructure |
| 167 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5652 | 0.2275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Backend Engineering |
| 168 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5541 | 0.2275 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Cloud Infrastructure |
| 169 | Sr. Lead Software Engineer | Capital One | Bangalore, In | 0.5497 | 0.227 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 170 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4632 | 0.2258 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 171 | R&D AI Platform Engineer / Administrator | Ciena | Ottawa | 0.4191 | 0.2243 | BACKEND_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 172 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | Doha, Qatar  | 0.4019 | 0.2236 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Cloud Infrastructure |
| 173 | SMTS, Software Engineering (Salesforce Expert) | Salesforce | India - Hyderabad | 0.5494 | 0.2224 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Backend Engineering |
| 174 | Senior Inference Engineer, AIConfigurator for Dynamo | NVIDIA | US, CA, Santa Clara | 0.7794 | 0.222 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, Cloud Infrastructure |
| 175 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7513 | 0.222 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Cloud Infrastructure |
| 176 | Senior ML Ops Engineer | RELX | Philadelphia, PA | 0.5653 | 0.222 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Cloud Infrastructure |
| 177 | Senior Machine Learning Engineer (AI Foundations) | Capital One | McLean, VA | 0.5022 | 0.222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, Cloud Infrastructure |
| 178 | Machine Learning Engineer I | PROS Holdings, Inc. | BGR Sofia Hybrid | 0.5256 | 0.2214 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 179 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.4953 | 0.2214 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 180 | Associate Linux/Window Engineer / Platform Services / Experienced Hire | Susquehanna International Group (SIG) | Associate Linux/Window Engineer / Platform Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.2214 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 181 | Senior Cyber Security Engineer – Security Services | General Motors | Warren, Michigan, United States of America | 0.5495 | 0.2202 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Security Engineering, Python |
| 182 | Internal Channel Systems Engineer | Fortinet | LONDON, United Kingdom | 0.4079 | 0.2193 | SOLUTIONS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Security Engineering |
| 183 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5111 | 0.2181 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 184 | Senior Software Engineer, Full-Stack — Content Tools | Epic Kids | Bangalore, India (remote within India) | 0.4626 | 0.2181 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 185 | Senior Software Developer / HR Technology & Shared Services / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Developer / HR Technology & Shared Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.2181 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 186 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.2168 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 187 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7489 | 0.2164 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 188 | Sr Software Engineer - 20197 | Cox | Atlanta GA | 0.3892 | 0.2164 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 189 | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire in New York, New York / Careers at SIG | 0.6962 | 0.2164 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Machine Learning |
| 190 | Senior Signal Processing Engineer | Whoop | Boston, MA | 0.5929 | 0.2147 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, C++ |
| 191 | Advanced Software Engineer | Honeywell | Charlotte, NC, United States | 0.5798 | 0.2147 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, C# |
| 192 | Sr Software Engineer I - Java - International Card Risk Services Technology | American Express | Phoenix, AZ, United States | 0.5514 | 0.2147 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 193 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.4752 | 0.2125 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 194 | Lead Software Engineer | Appian | McLean, Virginia | 0.448 | 0.2125 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 195 | Data Architect | RTX | Warminster, Wiltshire | 0.4805 | 0.2121 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure |
| 196 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.4865 | 0.2109 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, Security Engineering |
| 197 | Lead Software Engineer | Capital One | McLean, VA | 0.628 | 0.2099 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 198 | Lead Software Engineer | Capital One | McLean, VA | 0.6279 | 0.2099 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 199 | Lead Software Engineer | Capital One | McLean, VA | 0.5711 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 200 | Lead Software Engineer (Java, Golang, AWS) | Capital One | Plano, TX | 0.5413 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 201 | Senior Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.6194 | 0.2099 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 202 | Lead Software Engineer, Full Stack (Risk Tech, Intelligent Foundations & Experiences) | Capital One | New York, NY | 0.5944 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 203 | Lead Software Engineer, Full Stack (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.5497 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 204 | Lead Software Engineer, Full Stack | Capital One | Riverwoods, IL | 0.5221 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 205 | Lead Software Engineer , Backend | Capital One | Plano, TX | 0.5214 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, JavaScript |
| 206 | Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.5712 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 207 | Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.5175 | 0.2099 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 208 | Lead Software Engineer, Back End | Capital One | Plano, TX | 0.4981 | 0.2099 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, JavaScript |
| 209 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5005 | 0.2091 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 210 | Software Engineer III - MFT Business Enablement - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4422 | 0.2091 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 211 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4327 | 0.2091 | ML_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 212 | Senior Backend Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.4086 | 0.2091 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, PostgreSQL |
| 213 | AI Security Architect | Cadence Design Systems | SAN JOSE | 0.696 | 0.2087 | SECURITY_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Security Engineering, Machine Learning, AI Systems |
| 214 | Sr Software Engineer - 20198 | Cox | Atlanta GA | 0.4833 | 0.2043 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 215 | Lead Software Engineer | Capital One | McLean, VA | 0.607 | 0.2043 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 216 | Lead Software Engineer, DevOps - Card Tech | Capital One | McLean, VA | 0.572 | 0.2043 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, Java |
| 217 | Lead Software Engineer, DevOps - Card Tech | Capital One | McLean, VA | 0.572 | 0.2043 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, Java |
| 218 | Lead Software Engineer (Scala, JavaScript) | Capital One | New York, NY | 0.5951 | 0.2043 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 219 | Lead Software Engineer | Capital One | McLean, VA | 0.5586 | 0.2043 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 220 | Lead Software Engineer (Python, Kubernetes) | Capital One | McLean, VA | 0.5497 | 0.2043 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 221 | Software Engineer I | LexisNexis Risk Solutions | Colorado | 0.4234 | 0.2042 | SWE_FULLTIME | Backend Engineering, Java, JavaScript |
| 222 | Senior Cybersecurity Vulnerability Management Engineer | General Motors | Warren, Michigan, United States of America | 0.5511 | 0.2036 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Cloud Infrastructure |
| 223 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4469 | 0.2036 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 224 | GTM Engineer | Greenhouse | Ontario | 0.4752 | 0.2021 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 225 | Senior Software Engineer, DGXC Data Services | NVIDIA | US, CA, Santa Clara | 0.7239 | 0.1988 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Go |
| 226 | Senior Fullstack/Frontend Engineer | General Motors | Sunnyvale, California, United States of America | 0.66 | 0.1988 | FULLSTACK_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Full Stack Development, Frontend Engineering, JavaScript |
| 227 | Senior Software Engineer - Backend | Sigma Computing | San Francisco, CA | 0.5736 | 0.1988 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Rust |
| 228 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.6813 | 0.1988 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 229 | Senior Lead AI Engineer, Gen AI Platform | Capital One | New York, NY | 0.6809 | 0.1988 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 230 | Lead Software Engineer, Back End (Cloud Operations Resilience Engineering) | Capital One | Plano, TX | 0.5711 | 0.1988 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 231 | Systems Engineer - US Remote | Motorola Solutions | Illinois Remote Work | 0.429 | 0.1949 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C#, Python |
| 232 | DevOps Engineer, GPS | ScaleAI | Dubai, UAE; Riyadh, Saudi Arabia | 0.5333 | 0.1949 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 233 | AI Automation Engineer, Security | NVIDIA | US, CA, Santa Clara | 0.7611 | 0.1932 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 234 | Senior Software Engineer - Storage | NVIDIA | US, CA, Santa Clara | 0.7218 | 0.1932 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C++ |
| 235 | Senior Failure Analysis Engineer | NVIDIA | US, CA, Santa Clara | 0.6616 | 0.1932 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 236 | Lead AI Engineer (Vision model customization, VML) | Capital One | New York, NY | 0.6718 | 0.1932 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 237 | Senior Software Engineer - Fullstack | Sigma Computing | San Francisco, CA | 0.5665 | 0.1932 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Rust |
| 238 | Lead AI Engineer (Vision model customization, VLM) | Capital One | New York, NY | 0.5932 | 0.1932 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 239 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5922 | 0.1932 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 240 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.1932 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 241 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.406 | 0.1928 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 242 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.525 | 0.1899 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 243 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1899 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 244 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5176 | 0.1899 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 245 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 246 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.5005 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 247 | Software Development Engineer | Micron Technology | Taoyuan - Fab 11, Taiwan | 0.5003 | 0.1899 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 248 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 249 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 250 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 251 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 252 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4812 | 0.1899 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 253 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 254 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 255 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4633 | 0.1899 | SWE_FULLTIME | Backend Engineering, C++, Java |
| 256 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4632 | 0.1899 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 257 | Software Engineer I | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.4086 | 0.1899 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Kotlin |
| 258 | C# Full-Stack Developer - Experienced Hire | Susquehanna International Group (SIG) | C# Full-Stack Developer - Experienced Hire in Dublin / Careers at SIG | 0.52 | 0.1899 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, C#, Python |
| 259 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.4587 | 0.1881 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 260 | Experienced Software Engineer- FSD | Boeing | IND - Bangalore, India | 0.4198 | 0.1881 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 261 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7801 | 0.1877 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 262 | Senior Software Engineer | Cox | Atlanta GA | 0.5311 | 0.1877 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 263 | Sr. Software Engineer, Telemetry (Starlink) | SpaceX | Hawthorne, CA | 0.6232 | 0.1877 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, C# |
| 264 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6548 | 0.1877 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 265 | Sr. Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6548 | 0.1877 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 266 | Sr Software Engineer | Cox | Atlanta GA | 0.4437 | 0.1877 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, C# |
| 267 | Senior AI/ML Engineer | Sigma Computing | San Francisco, CA | 0.6783 | 0.1877 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, AI Systems, Python |
| 268 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6252 | 0.1877 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 269 | Lead Machine Learning Engineer | Capital One | McLean, VA | 0.5586 | 0.1877 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 270 | Sr. Automation Engineer (Starlink Customer Success) | SpaceX | Bastrop, TX | 0.4731 | 0.186 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 271 | Software Engineer II, Mission Interface | Torc Robotics | Ann Arbor, MI | 0.6096 | 0.1857 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 272 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.5825 | 0.1857 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 273 | Print, Mail & Data System Engineer | Travelers | GA - Norcross | 0.4636 | 0.1857 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 274 | Data Engineer | Bonterra | Remote, United States | 0.4054 | 0.1857 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 275 | Firmware Engineer Data Center Solid State Drives | Micron Technology | Arzano (NA), Italy | 0.3054 | 0.1857 | SWE_FULLTIME | Backend Engineering, Python, C++ |
| 276 | Networking/Security Software Engineer - SMTS | Salesforce | India - Hyderabad | 0.5792 | 0.1825 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Backend Engineering, Cloud Infrastructure |
| 277 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.4632 | 0.1825 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, Full Stack Development |
| 278 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4327 | 0.1825 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 279 | Senior SAP FIORI Developer | Monster Energy | USA - Corona, CA | 0.5994 | 0.1821 | BACKEND_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, Frontend Engineering, JavaScript |
| 280 | Senior Security Engineer - Proxy & Cloud Security Platform | Truist Bank | Atlanta, GA | 0.5304 | 0.1821 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Cloud Infrastructure, Python |
| 281 | Senior Software Engineer NAVAIR Product Line | CACI | Austin, TX, US | 0.5443 | 0.1821 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 282 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | San Francisco, CA | 0.5856 | 0.1821 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Go |
| 283 | Senior AI/ML Engineer | Sigma Computing | New York City, NY | 0.6784 | 0.1821 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 284 | Associate-Digital Product Management | American Express | Gurugram, HR, India | 0.5514 | 0.1807 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 285 | Audio Programmer | Sony Interactive Entertainment | United Kingdom, London | 0.5209 | 0.1807 | SWE_FULLTIME | Backend Engineering, C++, C# |
| 286 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1807 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 287 | SNOW Developer | Dexcom | Manila, Philippines | 0.463 | 0.1807 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, JavaScript, SQL |
| 288 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.448 | 0.1807 | ML_ENGINEER_FULLTIME | Machine Learning, C++, Python |
| 289 | Analytics Engineer | Pebl | Toronto, Ontario | 0.4525 | 0.1807 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 290 | Associate ATE Software Engineer | Boeing | IND - Bangalore, India | 0.4469 | 0.1807 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, C# |
| 291 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.4691 | 0.1804 | DATA_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 292 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.1804 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 293 | Senior Software Developer, Tooling Team | MaintainX | Toronto, Ontario, Canada | 0.5295 | 0.177 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 294 | Senior Network Engineer | NOV | Kochi, Kerala, India | 0.4802 | 0.177 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Security Engineering |
| 295 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.4631 | 0.177 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, AI Systems |
| 296 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.4696 | 0.1766 | SWE_FULLTIME | Cloud Infrastructure, Backend Engineering |
| 297 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4145 | 0.1764 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 298 | Engineer Software T1/T2 | Northrop Grumman | GAWR03GC | 0.3461 | 0.1764 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 299 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4439 | 0.1764 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 300 | Software Engineer II | Cadence Design Systems | SAN JOSE | 0.4196 | 0.1764 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 301 | Quality Assurance Engineer PON / DCOM | Ciena | Ottawa | 0.286 | 0.1764 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 302 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.4754 | 0.1748 | SWE_FULLTIME, RESEARCH_SCIENTIST_FULLTIME | AI Systems, Python |
| 303 | Cloud Network Engineer III (Anchorage, Alaska) | GCI | Anchorage, AK, United States | 0.4469 | 0.1748 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 304 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4327 | 0.1748 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 305 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4318 | 0.1748 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 306 | Senior IT Systems Engineer | Brain Co. | San Francisco Bay Area | 0.4236 | 0.1748 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 307 | Senior Gen AI Developer | KBR | El Segundo, California | 0.6387 | 0.1744 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Machine Learning, Cloud Infrastructure |
| 308 | Senior Data Engineer, Underwriting Technical Lead | Travelers | CT - Hartford | 0.508 | 0.1744 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, AI Systems, Machine Learning |
| 309 | Senior Full Stack Engineer | Podium | Lehi, Utah | 0.4679 | 0.1727 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, AI Systems, React |
| 310 | Lead Software Engineer (Kubernetes) | Appian | McLean, Virginia | 0.448 | 0.1727 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 311 | Sr Full Stack Developer, TD Securities | TD Bank | Toronto, Ontario | 0.5025 | 0.1722 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Frontend Engineering |
| 312 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5021 | 0.1714 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Cloud Infrastructure |
| 313 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.1714 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 314 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4813 | 0.1714 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 315 | Experienced Java Software Engineer | Boeing | POL - Gdansk, Poland | 0.4632 | 0.1714 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 316 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4327 | 0.1714 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, React |
| 317 | IT SOFTWARE ENGINEER | Micron Technology | Fab 10W, Singapore | 0.4194 | 0.1714 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 318 | Lead Software Engineer, DevOps | Capital One | Riverwoods, IL | 0.5721 | 0.1701 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Java, Python |
| 319 | Senior Sub-System Lead Engineer - High Voltage Battery Management | General Motors | Milford, Michigan, United States of America | 0.5798 | 0.1693 | BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 320 | Engineer I/Engineer II/Sr. Engineer/Sr Engineer II | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4631 | 0.1693 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 321 | Sales Engineer, Enterprise  Named | Fortinet | Atlanta, GA, United States | 0.4517 | 0.1693 | SOLUTIONS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 322 | M365 Developer | CACI | Remote (Any State) | 0.4972 | 0.1671 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 323 | Software Engineering Architect | Salesforce | Norway - Remote | 0.5793 | 0.1671 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 324 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.4754 | 0.1671 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, Python |
| 325 | Lead Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.463 | 0.1649 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 326 | Software Engineer - Compiler  | Sigma Computing | New York City, NY | 0.58 | 0.1645 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Rust, TypeScript |
| 327 | Software Engineer - Compiler  | Sigma Computing | San Francisco, CA | 0.5799 | 0.1645 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Rust, TypeScript |
| 328 | Lead Software Engineer, DevOps | Capital One | Richmond, VA | 0.5362 | 0.1645 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 329 | Lead Data Engineer - Nexus Data Products | Capital One | McLean, VA | 0.534 | 0.1645 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 330 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1621 | SWE_FULLTIME | Backend Engineering |
| 331 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1621 | SWE_FULLTIME | Backend Engineering |
| 332 | Systems Engr II | Honeywell | Delhi, India | 0.4812 | 0.1621 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 333 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4755 | 0.1621 | BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 334 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1621 | SWE_FULLTIME | Backend Engineering |
| 335 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4633 | 0.1621 | SWE_FULLTIME | Backend Engineering |
| 336 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.4516 | 0.1621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 337 | IT STORAGE ENGINEER | Micron Technology | Taichung - Fab 16, Taiwan | 0.4194 | 0.1621 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 338 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4086 | 0.1621 | SWE_FULLTIME | Backend Engineering |
| 339 | Senior Engineer, Advanced Modeling & AI Solutions | Micron Technology | Boise, ID - Main Site | 0.4079 | 0.1616 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, agentic AI |
| 340 | Senior Full Stack Software Engineer | Micron Technology | Taichung - AATT, Taiwan | 0.5244 | 0.1593 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Machine Learning, C# |
| 341 | Senior Solutions Architect, IPP | NVIDIA | US, CA, Santa Clara | 0.7816 | 0.159 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 342 | Senior Lead Data Engineer (Enterprise Platform Technology) (Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7512 | 0.159 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Java, Python |
| 343 | Lead Data Engineer (Enterprise Platforms Technology) ( Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7257 | 0.159 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 344 | Lead Data Engineer (Python, AWS, SQL, GenAI) (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.6947 | 0.159 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 345 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6645 | 0.159 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Java, Python |
| 346 | Senior Software Engineer - Fullstack | Sigma Computing | New York City, NY | 0.5856 | 0.159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Rust, Go |
| 347 | Senior Software Engineer - Backend | Sigma Computing | New York City, NY | 0.6041 | 0.159 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Rust, Go |
| 348 | Sr Lead Site Reliability & Systems Engineer | Cox | Austin TX | 0.5713 | 0.159 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Go |
| 349 | Lead Platform Engineer - Palo Alto (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4773 | 0.159 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 350 | Senior Platform Engineer | Capital One | Richmond, VA | 0.4258 | 0.159 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 351 | Sr. Hardware / Infrastructure Site Reliability Engineer (Starlink) | SpaceX | Redmond, WA | 0.5232 | 0.159 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Go |
| 352 | Sr. Kubernetes Platform Site Reliability Engineer (Starlink)  | SpaceX | Redmond, WA | 0.5232 | 0.159 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Go |
| 353 | Lead Data Engineer - Payment Networks | Capital One | McLean, VA | 0.5346 | 0.159 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 354 | GTM Engineer | Greenhouse | British Columbia | 0.4751 | 0.1542 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Python |
| 355 | Senior UI Software Engineer II | LexisNexis Risk Solutions | UK - London (London Wall) | 0.4874 | 0.1538 | FRONTEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Frontend Engineering, Full Stack Development, React |
| 356 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4198 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 357 | Data Migration Architect (Senior or Lead) | Boeing | USA - Hazelwood, MO | 0.6256 | 0.1534 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 358 | Senior Embedded Software Engineer | Micron Technology | San Jose, CA | 0.7214 | 0.1534 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 359 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6873 | 0.1534 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 360 | Senior DevOps Developer | Boeing | USA - Hazelwood, MO | 0.5671 | 0.1534 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, JavaScript |
| 361 | Senior Firmware Engineer | Motorola Solutions | Fresno, CA (CA180) | 0.4814 | 0.1534 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 362 | Sr. Data Engineer (Starlink Network Analytics, Wi-Fi)  | SpaceX | Redmond, WA | 0.5885 | 0.1534 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, C++, Python |
| 363 | Sr. Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6544 | 0.1534 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 364 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.5809 | 0.1534 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Go |
| 365 | Lead Software/Controls Engineer | GE Vernova | Wilmington NC USA | 0.4187 | 0.1534 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Node.js, Python |
| 366 | Sr. Software Infrastructure Engineer (Starlink) | SpaceX | Redmond, WA | 0.5226 | 0.1534 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, C++ |
| 367 | Lead Machine Learning Engineer | Capital One | Cambridge, MA | 0.5286 | 0.1534 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 368 | Partner Operations Senior Engineer  | Sigma Computing | San Francisco, CA | 0.4897 | 0.1517 | DATA_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL, React, Python |
| 369 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.5378 | 0.1512 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C# |
| 370 | Full Stack Software Engineer | Manulife Financial | Hong Kong | 0.549 | 0.1482 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Angular |
| 371 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.4632 | 0.1482 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 372 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4327 | 0.1482 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, JavaScript |
| 373 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4323 | 0.1482 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 374 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.1482 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, C# |
| 375 | Product Architect | Monster Energy | USA - Corona, CA | 0.5401 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, JavaScript |
| 376 | Senior Software Engineer - C++/UI | General Motors | Mountain View, California, United States of America | 0.5715 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 377 | Lead Software Engineer (Cloud) | Northwood Space | Torrance, CA | 0.6467 | 0.1478 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Rust |
| 378 | Advanced Software Engr | Honeywell | Hamilton Township, NJ, United States | 0.462 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 379 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | New York City, NY | 0.5857 | 0.1478 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Go |
| 380 | Lead DevOps Developer | Boeing | USA - Long Beach, CA | 0.5052 | 0.1478 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Angular |
| 381 | Sr. Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.1478 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 382 | Sr. Software Engineer, High Performance Computing (Starlink)    | SpaceX | Redmond, WA | 0.5578 | 0.1478 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 383 | Sr. Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 384 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.5769 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 385 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.5758 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 386 | Expert Site Reliability Engineer | Harris Computer | Kentucky, United States | 0.3655 | 0.1478 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 387 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in New York, New York / Careers at SIG | 0.72 | 0.1478 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 388 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.5426 | 0.1457 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 389 | Senior Software Engineer | Cadence Design Systems | SAN JOSE | 0.6448 | 0.1457 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 390 | Architect - Personal Insurance Cross-Domain Architecture | Travelers | CT - Hartford | 0.5447 | 0.1457 | SWE_FULLTIME | Cloud Infrastructure, AI Systems, Python |
| 391 | Software Engineer II-Team Lead (AWS, Typescript) | Travelers | CT - Hartford | 0.5281 | 0.1457 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 392 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5155 | 0.1457 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 393 | Success Architect (Agentforce / Data Cloud) | Salesforce | Indiana - Indianapolis | 0.5675 | 0.1449 | SOLUTIONS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 394 | .NET/C# Engineer, TD Securities | TD Bank | Toronto, Ontario | 0.3795 | 0.1444 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 395 | Senior Software Engineer | GE Vernova | Bucharest | 0.5514 | 0.144 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Kotlin |
| 396 | Software Engineering MTS - Compliance Automation & Tooling (Apex, Python) | Salesforce | India - Hyderabad | 0.5792 | 0.1427 | SWE_FULLTIME | Backend Engineering, Security Engineering, Python |
| 397 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.4591 | 0.1427 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Backend Engineering, Python |
| 398 | Sr. Batch Operations Technician - Run My Job and SAP BW (Remote) | RTX | US-TX-REMOTE | 0.5433 | 0.1423 | BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 399 | Senior Cloud Solution Architect | Boeing | USA - Hazelwood, MO | 0.5577 | 0.1423 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 400 | Senior Integration Developer | Monster Energy | USA - Corona, CA | 0.447 | 0.1423 | BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 401 | Engineering Technical Lead - I&C Embedded Software | GE Vernova | Wilmington NC USA | 0.3946 | 0.1423 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 402 | Software Engineer, Security | Notion | San Francisco, California | 0.7173 | 0.1423 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Security Engineering |
| 403 | Senior Network Engineer | CACI | Chantilly, VA, US | 0.437 | 0.1423 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 404 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6489 | 0.1401 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 405 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6359 | 0.1401 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, AI Systems, Python |
| 406 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6622 | 0.1401 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 407 | Senior Business Systems Analyst | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.6073 | 0.1384 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 408 | Senior Software Engineer | Podium | Lehi, Utah, Open to Remote | 0.5313 | 0.1384 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, React, PostgreSQL |
| 409 | Senior Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4254 | 0.1384 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Go |
| 410 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.4813 | 0.1371 | ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 411 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4316 | 0.1371 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 412 | Senior Software Engineer II | LexisNexis Risk Solutions | Mumbai | 0.4195 | 0.1371 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Java |
| 413 | AWS Data Engineer | Bank of Montreal | Toronto, ON, CAN | 0.4809 | 0.1357 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 414 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3562 | 0.1357 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python, SQL |
| 415 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.5327 | 0.135 | DATA_ENGINEER_FULLTIME | — |
| 416 | Senior OT Cybersecurity Engineer | GE Vernova | Findlay Township | 0.5628 | 0.1346 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Backend Engineering |
| 417 | Lead Protection and Control Engineer | GE Vernova | Remote | 0.4757 | 0.1346 | SWE_FULLTIME, SYSTEMS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 418 | Azure IaaS Engineer | CACI | Remote (Any State) | 0.4776 | 0.1346 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 419 | Senior Momentum Technical Specialist | CACI | Remote (Any State) | 0.5056 | 0.1346 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering |
| 420 | Firewall Engineering Architect | Leidos | Huntsville, AL | 0.3785 | 0.1346 | BACKEND_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Security Engineering |
| 421 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.1328 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 422 | Data Engineer (12 month Fixed term Contract) | Sony Interactive Entertainment | United Kingdom, London | 0.5128 | 0.1328 | DATA_ENGINEER_FULLTIME | SQL, Python, Java |
| 423 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4632 | 0.1328 | SWE_FULLTIME | Java, Python, SQL |
| 424 | QE PCT Engineer | Micron Technology | Miaoli - Tongluo, Taiwan | 0.4235 | 0.1328 | SWE_FULLTIME | Python, C++, SQL |
| 425 | Sr Advanced Cyb Sec Archt/Engr | Honeywell | Rio de Janeiro, RJ, Brazil | 0.4813 | 0.1316 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Backend Engineering |
| 426 | Senior IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4632 | 0.1316 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 427 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.5494 | 0.1306 | SWE_FULLTIME | Backend Engineering, C++, Java |
| 428 | Senior Platform Engineer  | Clarity Innovations | Required  | 0.5354 | 0.1273 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 429 | Senior Process Engineer (Oil and Gas, EPC, Midstream) | NOV | Dubai, Dubai, United Arab Emirates | 0.4463 | 0.1273 | SWE_FULLTIME | Backend Engineering |
| 430 | Senior Software Developer – Virtualization, SIL, and AI‑Enablement | General Motors | Markham, Ontario, Canada | 0.5397 | 0.1268 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Machine Learning, Python |
| 431 | ML Engineer, II - App Engine | Torc Robotics | Ann Arbor, MI, Montreal, Canada | 0.4928 | 0.1264 | SWE_FULLTIME | Backend Engineering, C++ |
| 432 | Lead Engineer 1 - Customer Application Engineering | GE Vernova | Schenectady | 0.4052 | 0.1225 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, SQL, Python |
| 433 | Senior Software Cloud Engineer - PCS - IoT | Medtronic | Galway, County Galway, Ireland | 0.4597 | 0.1212 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, C# |
| 434 | Senior Software Cloud Engineer - PCS - IoT | Medtronic | Galway, County Galway, Ireland | 0.4422 | 0.1212 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Backend Engineering, C# |
| 435 | ENGINEER, FW & PRODUCT TEST ENGINEERING | Micron Technology | Arzano (NA), Italy | 0.3292 | 0.1193 | SWE_FULLTIME | Python |
| 436 | EA-Data Engineer 1, Data Services | Bonterra | Remote, United States | 0.3216 | 0.1193 | DATA_ENGINEER_FULLTIME | SQL |
| 437 | Aeroderivative Performance Engineer - Field | GE Vernova | Greenville | 0.3469 | 0.1193 | SWE_FULLTIME | Python |
| 438 | Automation Data Information Administrator | CACI | Washington, DC, US | 0.5686 | 0.1191 | DATA_ENGINEER_FULLTIME | Python, SQL |
| 439 | Lead Software Engineer, Android (Kotlin & Jetpack Compose) | Capital One | McLean, VA | 0.5778 | 0.1191 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | Kotlin, Swift |
| 440 | Digital Transformation Manufacturing Engineer 2/3 | Northrop Grumman | United States-California-Northridge | 0.4318 | 0.1191 | SWE_FULLTIME | Python, SQL |
| 441 | Senior Technical Designer | Sony Interactive Entertainment | United States, Santa Monica, CA | 0.4603 | 0.1191 | SWE_FULLTIME | C++, C# |
| 442 | Software Developer (Mid Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.117 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, C++, Python |
| 443 | Software Engineer Developer ( Mid-Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.117 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 444 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4466 | 0.117 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 445 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4278 | 0.117 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 446 | Sr. Product Solution Analyst, TD Securities | TD Bank | Toronto, Ontario | 0.4116 | 0.1157 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 447 | Package Device Product Engineer (PDPE) Engineer | Micron Technology | Sanand - 303A - AT/SSD/MOD, India | 0.5796 | 0.1143 | SWE_FULLTIME | Python |
| 448 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.114 | SWE_FULLTIME | Backend Engineering, C++, Python |
| 449 | Software Engineering, SMTS (Salesforce Developer) | Salesforce | India - Hyderabad | 0.4755 | 0.114 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 450 | Sr Engineer, Data Science | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.114 | DATA_SCIENTIST_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Python, Angular |
| 451 | Senior Software Engineer | LexisNexis Risk Solutions | Australia - (Sydney) | 0.4317 | 0.114 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 452 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4192 | 0.114 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Java, Python |
| 453 | Senior Software Engineer II | LexisNexis Risk Solutions | Australia - (Sydney) | 0.4079 | 0.114 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 454 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.4509 | 0.1136 | SWE_FULLTIME | Python |
| 455 | Lead Data Engineer | Capital One | Wilmington, DE | 0.7087 | 0.1114 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 456 | Senior Firmware Engineer | Ciena | New Providence - NJ | 0.5076 | 0.1114 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 457 | Sr. Backend Engineer | dv01 | Remote - USA  | 0.6155 | 0.1114 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Kotlin, SQL |
| 458 | C++ Software Engineer | Cadence Design Systems | SAN JOSE | 0.5967 | 0.1114 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 459 | Senior SAP PI/PO Developer | CACI | Remote (Any State) | 0.4713 | 0.1114 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, SQL |
| 460 | Senior Data Engineer (AWS, Databricks) | Travelers | CT - Hartford | 0.508 | 0.1114 | DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 461 | Oracle EPM Integration Lead | CACI | Remote (Any State) | 0.4128 | 0.1114 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL, Python |
| 462 | Senior Software Engineer - Operating System | Torc Robotics | Ann Arbor, MI | 0.4758 | 0.1114 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, C++, Python |
| 463 | Sr. Electricity Market Optimization Software Engineer | GE Vernova | Bellevue | 0.448 | 0.1114 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Python |
| 464 | Senior ABAP Developer | CACI | Remote (Any State) | 0.3919 | 0.1114 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, SQL |
| 465 | Senior Software Engineer | EarnIn | Mexico City, Mexico | 0.643 | 0.1084 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, Go |
| 466 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5744 | 0.1084 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, C# |
| 467 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, Liverpool | 0.5759 | 0.1084 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, C# |
| 468 | Senior Quality Engineer I | American Express | Chennai, TN, India | 0.502 | 0.1084 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, PostgreSQL |
| 469 | Experienced Software Application Development – QA and Test Automation Engineer | Boeing | IND - Bangalore, India | 0.5019 | 0.1084 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, JavaScript |
| 470 | Sr Embedded Software Engineer | Dexcom | San Diego, California | 0.5218 | 0.1058 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 471 | Sr. QA Engineer - IP Routing | Ciena | Remote-Canada | 0.4707 | 0.1058 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 472 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.4543 | 0.105 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 473 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4197 | 0.105 | SWE_FULLTIME | — |
| 474 | Senior Commercial Data & Insights Engineer | Dexcom | Remote - Spain | 0.5496 | 0.1041 | DATA_ENGINEER_FULLTIME | SQL, Python |
| 475 | Senior Discipline Engineer - Software Requirements | Valeo | Chennai | 0.5507 | 0.1028 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 476 | Simulation Software Engineer (Experienced or Senior level) | Boeing | GBR - Crawley, UK | 0.5019 | 0.1028 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 477 | Senior Advanced Embedded Engineer | Honeywell | Givisiez, Sarine, Switzerland | 0.4874 | 0.1028 | BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++ |
| 478 | Senior Linux Platform Development Engineer | Susquehanna International Group (SIG) | Senior Linux Platform Development Engineer in Dublin / Careers at SIG | 0.52 | 0.1028 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 479 | Momentum Technical Specialist | CACI | Remote (Any State) | 0.4128 | 0.1003 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 480 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.4294 | 0.0981 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, C++, Java |
| 481 | Lead AC Control Automation Engineer | GE Vernova | Noida | 0.5513 | 0.0973 | BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 482 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.0973 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 483 | Sr IT Analyst | Honeywell | Bengaluru, Karnataka, India | 0.4619 | 0.0973 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 484 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4327 | 0.0973 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 485 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5223 | 0.0882 | DATA_ENGINEER_FULLTIME | MySQL, PostgreSQL, JavaScript |
| 486 | Senior Software Developer – DevOps | General Motors | Markham, Ontario, Canada | 0.5412 | 0.0814 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, C++, Python |
| 487 | IT Developer (Java), TD Securities | TD Bank | Toronto, Ontario | 0.3363 | 0.0814 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, MongoDB |
| 488 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.0797 | SWE_FULLTIME | Java, JavaScript, SQL |
| 489 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.4039 | 0.0785 | BACKEND_ENGINEER_FULLTIME | Python, C++ |
| 490 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.4035 | 0.0785 | BACKEND_ENGINEER_FULLTIME | Python, C++ |
| 491 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.3895 | 0.0785 | BACKEND_ENGINEER_FULLTIME | Python, C++ |
| 492 | Software Development Engineer in Test | Medtronic | London, London, United Kingdom | 0.3251 | 0.0785 | SWE_FULLTIME | Python, Java |
| 493 | Quality Engineer Lead | LexisNexis Risk Solutions | Mumbai | 0.5798 | 0.0741 | SWE_FULLTIME | TypeScript, JavaScript |
| 494 | Senior Discipline Engineer | Valeo | Chennai | 0.5507 | 0.0741 | SWE_FULLTIME | C++, Python |
| 495 | Advanced Data Analyst -MDM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4874 | 0.0741 | DATA_ENGINEER_FULLTIME | SQL, Java |
| 496 | Senior Workday Platform Engineer - Absence (Workday) | Sony Interactive Entertainment | Ireland, Dublin | 0.4838 | 0.0703 | BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 497 | SAP IBP Analyst | iHerb | United States of America - Remote / Home Office | 0.5662 | 0.066 | BACKEND_ENGINEER_FULLTIME | — |

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

- **Total jobs matching subscribed pools (after filters):** 401
- **Notification-eligible jobs (≤60d, not yet emailed):** 401
- **Personal score range:** 0.063 – 0.5875 (59 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 284 |
| `BACKEND_ENGINEER_FULLTIME` | 214 |
| `ML_ENGINEER_FULLTIME` | 81 |
| `FULLSTACK_ENGINEER_FULLTIME` | 65 |
| `DATA_ENGINEER_FULLTIME` | 64 |
| `FRONTEND_ENGINEER_FULLTIME` | 22 |
| `DATA_SCIENTIST_FULLTIME` | 19 |
| `DEVOPS_ENGINEER_FULLTIME` | 16 |
| `DATA_ANALYST_FULLTIME` | 9 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 4 |
| `SECURITY_ENGINEER_FULLTIME` | 4 |
| `SUPPORT_ENGINEER_FULLTIME` | 3 |
| `MOBILE_ENGINEER_FULLTIME` | 3 |
| `RESEARCH_SCIENTIST_FULLTIME` | 2 |
| `SYSTEMS_ENGINEER_FULLTIME` | 1 |
| `TECHNICAL_PROGRAM_MANAGER_FULLTIME` | 1 |
| `MARKETING_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Data Scientist, Finance @ Figma

- **Location:** San Francisco, CA • New York, NY • United States (unclear)
- **Posted:** 2026-06-12T19:20:07+00:00
- **Salary:** 140000 – 348000
- **Effort:** MEDIUM
- **Opportunity score:** 0.7884
- **Personal score:** 0.5875
- **Pools:** `DATA_SCIENTIST_FULLTIME`, `DATA_ENGINEER_FULLTIME`
- **Roles:** DATA_SCIENTIST, DATA_ENGINEER
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering
- **Skills:** financial modeling, data architecture, forecasting, statistical analysis
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering, SQL, Python
- **URL:** https://boards.greenhouse.io/figma/jobs/6013304004?gh_jid=6013304004

#### #2 — Data Engineer I @ University of Texas at Austin

- **Location:** AUSTIN, TX (unclear)
- **Posted:** 2026-06-11T00:00:00+00:00
- **Salary:** 71060 – —
- **Effort:** HIGH
- **Opportunity score:** 0.2797
- **Personal score:** 0.5188
- **Pools:** `DATA_ENGINEER_FULLTIME`
- **Roles:** DATA_ENGINEER
- **Capabilities:** Data Engineering, Cloud Infrastructure
- **Skills:** data pipelines, ETL development, data governance, cloud infrastructure
- **Match reasons:** Data Engineering, Cloud Infrastructure, SQL, Python, BigQuery
- **URL:** https://utaustin.wd1.myworkdayjobs.com/UTstaff/job/AUSTIN-TX/Data-Engineer-I_R_00045134

#### #3 — Data Engineer @ The Coca-Cola Company

- **Location:** US - GA - Atlanta (unclear)
- **Posted:** 2026-06-12T00:00:00+00:00
- **Salary:** 124600 – 148200
- **Effort:** MEDIUM
- **Opportunity score:** 0.5331
- **Personal score:** 0.4875
- **Pools:** `DATA_ENGINEER_FULLTIME`
- **Roles:** DATA_ENGINEER
- **Capabilities:** Data Engineering, Machine Learning
- **Skills:** data modeling, data pipelines, ETL
- **Match reasons:** Data Engineering, Machine Learning, SQL, Python
- **URL:** https://coke.wd1.myworkdayjobs.com/coca-cola-careers/job/US---GA---Atlanta/Software-Engineer-I_R-140135

#### #4 — Machine Learning Engineer, Asia @ Manulife Financial

- **Location:** Manulife Tower, Manulife (Singapore) Pte Ltd (unclear)
- **Posted:** 2026-06-12T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5328
- **Personal score:** 0.4675
- **Pools:** `ML_ENGINEER_FULLTIME`
- **Roles:** ML_ENGINEER
- **Capabilities:** Machine Learning, Data Engineering, Cloud Infrastructure
- **Skills:** GenAI, Model Deployment
- **Match reasons:** Machine Learning, Data Engineering, Cloud Infrastructure, Python, SQL
- **URL:** https://manulife.wd3.myworkdayjobs.com/en-US/MFCJH_Jobs/job/Manulife-Tower-Manulife-Singapore-Pte-Ltd/Machine-Learning-Engineer--Asia--Global-Marketing-AI-_JR26040655-2

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Data Scientist, Finance | Figma | San Francisco, CA • New York, NY • United States | 0.7884 | 0.5875 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 2 | Data Engineer I | University of Texas at Austin | AUSTIN, TX | 0.2797 | 0.5188 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 3 | Data Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.4875 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, SQL |
| 4 | Machine Learning Engineer, Asia | Manulife Financial | Manulife Tower, Manulife (Singapore) Pte Ltd | 0.5328 | 0.4675 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 5 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.6717 | 0.4563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 6 | ML Engineer, Generative Video | Mirage | Union Square, New York City | 0.5091 | 0.4563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 7 | Machine Learning Engineer I | PROS Holdings, Inc. | BGR Sofia Hybrid | 0.5256 | 0.4488 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 8 | Data Engineer | Base Power Company | Austin, TX | 0.4691 | 0.4188 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 9 | Postgraduate Associate for Academic Integrity | University of Texas at Austin | UT MAIN CAMPUS | 0.3074 | 0.4175 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 10 | Data Engineer | Bonterra | Remote, United States | 0.4054 | 0.4175 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 11 | Data Scientist | Micron Technology | Boise, ID - Main Site | 0.4194 | 0.4175 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 12 | Performance Engineer II | Berkshire Hathaway Energy | Calipatria, CA, United States | 0.5015 | 0.3875 | DATA_ANALYST_FULLTIME, SWE_FULLTIME | Analytics Engineering, SQL, Python |
| 13 | Information & Application Developer (Entry Level and Associate) | Boeing | USA - North Charleston, SC | 0.4034 | 0.3875 | SWE_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Python, SQL |
| 14 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.4632 | 0.3875 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 15 | Software Engineer | Aquatic Capital Management | New York | 0.608 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 16 | Analytics Engineer | Loop | Chicago | 0.4398 | 0.3875 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 17 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6284 | 0.3863 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 18 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4145 | 0.3863 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 19 | Analyst-Data Science (SQL, Python, GenAI) | American Express | Gurugram, HR, India | 0.5496 | 0.3675 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 20 | Analyst-Risk Management | American Express | Gurugram, HR, India | 0.5493 | 0.3675 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 21 | AWS Data Engineer | Bank of Montreal | Toronto, ON, CAN | 0.4809 | 0.3675 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 22 | DATA SCIENTIST, SMAI | Micron Technology | MSB, Singapore | 0.5005 | 0.3675 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 23 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.406 | 0.3675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 24 | Analytics Engineer | Pebl | Toronto, Ontario | 0.4525 | 0.3675 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 25 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4469 | 0.3675 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 26 | Global Facilities Engineer | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4463 | 0.3675 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, Python |
| 27 | Data Scientist | Micron Technology | Fab 10A, Singapore | 0.4203 | 0.3675 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 28 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3562 | 0.3675 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 29 | DATA SCIENTIST | Micron Technology | Fab 10A, Singapore | 0.3982 | 0.3675 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 30 | Cloud Developer | Freedom Technology Solutions Group | Chantilly, VA | 0.5985 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 31 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI, Fort Worth, TX | 0.6387 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 32 | AI Builder Partner Solutions | Salesforce | California - San Francisco | 0.6822 | 0.3563 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 33 | Software Engineer | Intel | US, Arizona, Phoenix | 0.6671 | 0.3563 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 34 | AI Engineer III - Agentic AI | American Express | Phoenix, AZ, United States | 0.5497 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 35 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.3563 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 36 | Software Engineer I | Cox | Austin TX | 0.4688 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 37 | Data Solutions and Data Integration Lead | SRI International | US-VA-Arlington | 0.5692 | 0.3563 | DATA_ENGINEER_FULLTIME, TECHNICAL_PROGRAM_MANAGER_FULLTIME | Data Engineering, Python |
| 38 | Software Engineer, Machine Learning | Whoop | Boston, MA | 0.5388 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 39 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.5272 | 0.3563 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 40 | ML Engineer, Agentic Systems | Mirage | Union Square, New York City | 0.5075 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 41 | Software Engineer II | Cox | Atlanta GA | 0.4239 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 42 | Software Engineer (Front End) | CACI | Aurora, CO, US | 0.3868 | 0.3563 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 43 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, Aliso Viejo, CA | 0.5298 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 44 | Software Engineer, Hardware-in-the-Loop (Starlink) | SpaceX | Redmond, WA | 0.4987 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 45 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.4877 | 0.3563 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 46 | Software Engineer, Test Infrastructure (Application Software) | SpaceX | Hawthorne, CA | 0.4754 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 47 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 48 | Software Engineer, Developer Productivity  | Glean | Mountain View, CA | 0.4989 | 0.3563 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 49 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4469 | 0.3563 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 50 | Software Engineer, Network Monitoring (Starlink) | SpaceX | Hawthorne, CA | 0.4365 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 51 | Factory Software Engineer (Starlink) | SpaceX | Bastrop, TX | 0.4246 | 0.3563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 52 | Applied Researcher II (AI Foundations) | Capital One | New York, NY | 0.5285 | 0.3563 | RESEARCH_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 53 | Data Architect | RTX | Warminster, Wiltshire | 0.4805 | 0.355 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, data modeling |
| 54 | R&D AI Platform Engineer / Administrator | Ciena | Ottawa | 0.4191 | 0.355 | BACKEND_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure |
| 55 | Sr. Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6548 | 0.3525 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 56 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6548 | 0.3525 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 57 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.4813 | 0.3362 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 58 | Software Engineer II | American Express | Gurugram, HR, India | 0.4632 | 0.3362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 59 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7801 | 0.3337 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Data Engineering |
| 60 | Lead Machine Learning Engineer | Capital One | McLean, VA | 0.5586 | 0.3337 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 61 | Senior Machine Learning Engineer (AI Foundations) | Capital One | McLean, VA | 0.5022 | 0.3337 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Cloud Infrastructure |
| 62 | Software Development Engineer I - General Motors Insurance | GM Financial | United States | 0.5005 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 63 | Software Engineer II | Cox | Austin TX | 0.4597 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 64 | DevSecOps Software Engineer (Associate or Experienced), Phantom Works | Boeing | USA - Saint Charles, MO | 0.3778 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 65 | Software Engineer II (Java) | Sony Interactive Entertainment | United States, Madison, WI | 0.5699 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 66 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.599 | 0.325 | ML_ENGINEER_FULLTIME | Machine Learning |
| 67 | Software Engineer II | Cox | Atlanta GA | 0.3996 | 0.325 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure |
| 68 | Software Engineer II | Cox | Atlanta GA | 0.3987 | 0.325 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure |
| 69 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning |
| 70 | Software Engineer II - 20202 | Cox | Atlanta GA | 0.3445 | 0.325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 71 | Data Scientist, Marketing | Figma | San Francisco, CA • New York, NY • United States | 0.7654 | 0.3113 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 72 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.5426 | 0.3105 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Cloud Infrastructure |
| 73 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5155 | 0.3105 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Machine Learning |
| 74 | Senior Lead Data Engineer (Enterprise Platform Technology) (Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7512 | 0.2925 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 75 | Lead Data Engineer (Enterprise Platforms Technology) ( Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7257 | 0.2925 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 76 | Lead Data Engineer (Python, AWS, SQL, GenAI) (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.6947 | 0.2925 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 77 | Data Migration Architect (Senior or Lead) | Boeing | USA - Hazelwood, MO | 0.6256 | 0.2925 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 78 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6645 | 0.2925 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 79 | Sr. Automation Engineer (Starlink Customer Success) | SpaceX | Bastrop, TX | 0.4731 | 0.2925 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 80 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.4691 | 0.2925 | DATA_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 81 | Solutions Architect | Centerfield | Los Angeles, California | 0.4688 | 0.2925 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Python |
| 82 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2925 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 83 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5771 | 0.2925 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 84 | Lead Data Engineer - Payment Networks | Capital One | McLean, VA | 0.5346 | 0.2925 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 85 | Lead Data Engineer - Nexus Data Products | Capital One | McLean, VA | 0.534 | 0.2925 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 86 | Senior Data Engineer, Underwriting Technical Lead | Travelers | CT - Hartford | 0.508 | 0.2918 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Machine Learning |
| 87 | Marketing Productivity Engineer | Sigma Computing | San Francisco, CA | 0.626 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 88 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.549 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL, data modeling |
| 89 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5344 | 0.2875 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL, Python |
| 90 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 91 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 92 | Software Engineer I (AI Driven) | Travelers | GA - Atlanta | 0.5232 | 0.2875 | SWE_FULLTIME | Python, SQL |
| 93 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3632 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 94 | Forward Deployed Engineer  | Loop | San Francisco, CA | 0.4398 | 0.2875 | SWE_FULLTIME | Python, SQL |
| 95 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.4115 | 0.2875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 96 | Software Engineer II - AI Focused | Cadence Design Systems | BELO HORIZONTE | 0.549 | 0.2863 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 97 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.5603 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 98 | Software Engineer I | LexisNexis Risk Solutions | Cardiff | 0.5806 | 0.2863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 99 | EA-Data Engineer 1, Data Services | Bonterra | Remote, United States | 0.3216 | 0.2863 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL |
| 100 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5616 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 101 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.4953 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 102 | Software Engineer II, AI Platform | Cadence Design Systems | SAN JOSE | 0.4236 | 0.2863 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 103 | Aeroderivative Performance Engineer - Field | GE Vernova | Greenville | 0.3469 | 0.2863 | SWE_FULLTIME | Data Engineering, Python |
| 104 | AI Prompt Engineer | CACI | Remote (Any State) | 0.322 | 0.2863 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 105 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4439 | 0.2863 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 106 | Senior Inference Engineer, AIConfigurator for Dynamo | NVIDIA | US, CA, Santa Clara | 0.7794 | 0.2737 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 107 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7513 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 108 | Senior Lead AI Engineer (GenAI Platform Services) | Capital One | San Jose, CA | 0.7497 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 109 | Senior ML Ops Engineer | RELX | Philadelphia, PA | 0.5653 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 110 | Sr. Data Engineer (Starlink Network Analytics, Wi-Fi)  | SpaceX | Redmond, WA | 0.5885 | 0.2737 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 111 | Sr. Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6544 | 0.2737 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 112 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4755 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 113 | Senior Lead AI Engineer,(MLX, Agentic AI, Gen AI platform Services) | Capital One | San Jose, CA | 0.6325 | 0.2737 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 114 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6252 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 115 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5781 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 116 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 117 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 118 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.4929 | 0.2737 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 119 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2737 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 120 | Senior Lead AI Engineer (Gen AI Platform Services) | Capital One | San Jose, CA | 0.6085 | 0.2737 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 121 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5541 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 122 | Lead AI Engineer (MLX) | Capital One | New York, NY | 0.5535 | 0.2737 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 123 | Lead Machine Learning Engineer | Capital One | Cambridge, MA | 0.5286 | 0.2737 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 124 | Success Architect (Agentforce / Data Cloud) | Salesforce | Indiana - Indianapolis | 0.5675 | 0.2675 | SOLUTIONS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 125 | Associate-Digital Product Management | American Express | Gurugram, HR, India | 0.5514 | 0.2675 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 126 | Data Engineer (12 month Fixed term Contract) | Sony Interactive Entertainment | United Kingdom, London | 0.5128 | 0.2675 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 127 | Data Engineer | Manulife Financial | Toronto, Ontario | 0.4359 | 0.2675 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 128 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4251 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 129 | DATA SCIENTIST | Micron Technology | Fab 10A, Singapore | 0.4079 | 0.2675 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 130 | Forward Deployed Engineer I/II | Giga AI | San Francisco | 0.5602 | 0.2563 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 131 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5797 | 0.2563 | SWE_FULLTIME | Python |
| 132 | CAD Engineer | Micron Technology | Richardson, TX | 0.5796 | 0.2563 | SWE_FULLTIME | Python |
| 133 | Embedded Software Engineer - Electrification | General Motors | Milford, Michigan, United States of America | 0.5495 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 134 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.2563 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 135 | Software Engineering I | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 136 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 137 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 138 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.2563 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 139 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.2563 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python |
| 140 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, San Diego, CA | 0.5283 | 0.2563 | SWE_FULLTIME | Python |
| 141 | Software Engineer for Data at Rest (DAR) Crypto & Cross Domain Solutions | General Dynamics Mission Systems | US-MA-Dedham | 0.4222 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 142 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4755 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 143 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Palo Alto, CA | 0.4864 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 144 | RAN Validation Engineer (Starlink Mobile)  | SpaceX | Sunnyvale, CA | 0.4866 | 0.2563 | SWE_FULLTIME | Python |
| 145 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3242 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 146 | Full Stack Developer (Remote) | RTX | US-CT-REMOTE | 0.4136 | 0.2563 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 147 | Senior Associate, Data Scientist - NLP | Capital One | McLean, VA | 0.4651 | 0.2512 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 148 | Senior Data Engineer (AWS, Databricks) | Travelers | CT - Hartford | 0.508 | 0.2505 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 149 | Senior Data Analyst/Developer | CACI | Remote (Any State) | 0.437 | 0.2505 | DATA_ANALYST_FULLTIME, SWE_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 150 | Associate Software Engineer - Analytics | Boeing | IND - Bangalore, India | 0.5019 | 0.2363 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 151 | Full‑Stack Machine Learning Engineer | LexisNexis Risk Solutions | UK - London (London Wall) | 0.5016 | 0.2363 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 152 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5015 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 153 | AI-Enabled Full Stack Developer - Experienced | Micron Technology | Taichung - AATT, Taiwan | 0.4617 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 154 | GTM Engineer | Greenhouse | British Columbia | 0.4751 | 0.2363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 155 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.448 | 0.2363 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 156 | Application Engr II | Honeywell | Tianjin, China | 0.4316 | 0.2363 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 157 | Senior Failure Analysis Engineer | NVIDIA | US, CA, Santa Clara | 0.6616 | 0.2325 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 158 | Lead Software Engineer | Capital One | McLean, VA | 0.628 | 0.2325 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 159 | Lead Software Engineer | Capital One | McLean, VA | 0.6279 | 0.2325 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 160 | Automation Data Information Administrator | CACI | Washington, DC, US | 0.5686 | 0.2325 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 161 | Partner Operations Senior Engineer  | Sigma Computing | San Francisco, CA | 0.4897 | 0.2325 | DATA_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 162 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.6813 | 0.2325 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 163 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6359 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 164 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6358 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 165 | Lead Software Engineer, Fullstack (React, Java, Python) | Capital One | New York, NY | 0.6247 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 166 | Lead Software Engineer, DevOps | Capital One | Riverwoods, IL | 0.5721 | 0.2325 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python, SQL |
| 167 | Lead Software Engineer, Back End (Cloud Operations Resilience Engineering) | Capital One | Plano, TX | 0.5711 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 168 | Lead Software Engineer | Capital One | McLean, VA | 0.5711 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 169 | Lead Software Engineer (Java, Golang, AWS) | Capital One | Plano, TX | 0.5413 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 170 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 171 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 172 | Digital Transformation Manufacturing Engineer 2/3 | Northrop Grumman | United States-California-Northridge | 0.4318 | 0.2325 | SWE_FULLTIME | Data Engineering, Python, SQL |
| 173 | Senior AI/ML Engineer | Sigma Computing | San Francisco, CA | 0.6783 | 0.2325 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, SQL |
| 174 | Senior Lead Software Engineer, Full Stack (Global Payment Network) | Capital One | Riverwoods, IL | 0.6053 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 175 | Lead Software Engineer (Scala, JavaScript) | Capital One | New York, NY | 0.5951 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 176 | Lead Software Engineer, Full Stack (Risk Tech, Intelligent Foundations & Experiences) | Capital One | New York, NY | 0.5944 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 177 | Lead Software Engineer | Capital One | McLean, VA | 0.5586 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 178 | Lead Software Engineer, Full Stack (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.5497 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 179 | Lead Software Engineer (Python, Kubernetes) | Capital One | McLean, VA | 0.5497 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 180 | Lead Software Engineer, Full Stack | Capital One | Riverwoods, IL | 0.5221 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 181 | Lead Software Engineer, Full Stack (Golang, Angular, AWS) | Capital One | Richmond, VA | 0.5221 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 182 | Senior Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.6085 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 183 | Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.5712 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 184 | Lead Software Engineer, Full Stack | Capital One | Richmond, VA | 0.53 | 0.2325 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 185 | Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.5175 | 0.2325 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 186 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6489 | 0.2318 | ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 187 | AI Security Architect | Cadence Design Systems | SAN JOSE | 0.696 | 0.2318 | SECURITY_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 188 | Senior Gen AI Developer | KBR | El Segundo, California | 0.6387 | 0.2318 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 189 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5223 | 0.2318 | DATA_ENGINEER_FULLTIME | Data Engineering, Analytics Engineering, MySQL |
| 190 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5114 | 0.225 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | — |
| 191 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5109 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 192 | Quality Engineer II | RELX | Philadelphia, PA | 0.4851 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 193 | Software Engineer I | LivaNova | Houston, Texas, United States | 0.4256 | 0.225 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 194 | Software Engineer - Defense Applications | Palantir | New York, NY | 0.5474 | 0.225 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 195 | Software Engineer - Core Interfaces | Palantir | New York, NY | 0.5451 | 0.225 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 196 | Software Engineer 2 | Berkshire Hathaway Energy | Des Moines, IA, United States | 0.4628 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 197 | Entry Level Software Engineer - Austin, TX | Cox | Austin TX | 0.3807 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 198 | 2026 Raytheon Full Time-Software Engineer I – EOIR Advanced Products and Solutions (Onsite) | RTX | US-TX-MCKINNEY-513WC ~ 2501 W University Dr ~ WING C BLDG | 0.3632 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 199 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 200 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 201 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Redmond, WA | 0.4574 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 202 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Palo Alto, CA | 0.4864 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 203 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 204 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 205 | Senior Analytics Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5553 | 0.2205 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 206 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5243 | 0.2205 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 207 | Advanced Data Scientist | Honeywell | Hyderabad, Telangana, India | 0.5004 | 0.2205 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 208 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.4813 | 0.2205 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 209 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.4591 | 0.2205 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 210 | Sr Engineer, Data Science | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.2205 | DATA_SCIENTIST_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 211 | Lead Data Architect | Boeing | IND - Bangalore, India | 0.4327 | 0.2205 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 212 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4192 | 0.2205 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Machine Learning, Python |
| 213 | Systems Engineer - US Remote | Motorola Solutions | Illinois Remote Work | 0.429 | 0.2175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 214 | Senior Signal Processing Engineer | Whoop | Boston, MA | 0.5929 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 215 | AI Automation Engineer, Security | NVIDIA | US, CA, Santa Clara | 0.7611 | 0.2137 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python |
| 216 | Software Engineer ll - Java 8 Reactjs Web Search Team | American Express | Phoenix, AZ, United States | 0.5327 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 217 | Senior Software Engineer | Cox | Atlanta GA | 0.5311 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 218 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7489 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 219 | Software Engineer, Agents  | Mirage | Union Square, New York City | 0.5078 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 220 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6873 | 0.2137 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 221 | Lead AI Engineer (Vision model customization, VML) | Capital One | New York, NY | 0.6718 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 222 | Senior Lead AI Engineer, Gen AI Platform | Capital One | New York, NY | 0.6809 | 0.2137 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 223 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.5809 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 224 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 225 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4632 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 226 | Senior AI/ML Engineer | Sigma Computing | New York City, NY | 0.6784 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 227 | Lead AI Engineer (Vision model customization, VLM) | Capital One | New York, NY | 0.5932 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 228 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5922 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 229 | Lead AI Engineer (AI Foundations, LLM Customization and Finetuning) | Capital One | Cambridge, MA | 0.5782 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 230 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4327 | 0.2137 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 231 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 232 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5652 | 0.2137 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 233 | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire in New York, New York / Careers at SIG | 0.6962 | 0.2137 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 234 | Software Engineering Architect | Salesforce | Norway - Remote | 0.5793 | 0.213 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure |
| 235 | Lead Engineer 1 - Customer Application Engineering | GE Vernova | Schenectady | 0.4052 | 0.2093 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 236 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.4516 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 237 | Développeur de logiciel | Harris Computer | Quebec, Canada | 0.3817 | 0.205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 238 | Senior Data Scientist I | RELX | Gurgaon | 0.5814 | 0.2017 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 239 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5021 | 0.2017 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 240 | Sr. Product Solution Analyst, TD Securities | TD Bank | Toronto, Ontario | 0.4116 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 241 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.4631 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 242 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4323 | 0.2017 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 243 | Sr Software Engineer I - Java - International Card Risk Services Technology | American Express | Phoenix, AZ, United States | 0.5514 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 244 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.5327 | 0.195 | DATA_ENGINEER_FULLTIME | Data Engineering |
| 245 | Senior Software Engineer NAVAIR Product Line | CACI | Austin, TX, US | 0.5443 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 246 | Sr Software Engineer - 20198 | Cox | Atlanta GA | 0.4833 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 247 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | San Francisco, CA | 0.5856 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 248 | Senior Software Engineer - Fullstack | Sigma Computing | San Francisco, CA | 0.5665 | 0.195 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, data modeling |
| 249 | Lead DevOps Developer | Boeing | USA - Long Beach, CA | 0.5052 | 0.195 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 250 | Senior Software Engineer | Cox | Atlanta GA | 0.4445 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 251 | Sr Software Engineer | Cox | Atlanta GA | 0.4437 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 252 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4469 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 253 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.4865 | 0.195 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure |
| 254 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.4696 | 0.195 | SWE_FULLTIME | Cloud Infrastructure |
| 255 | Sr Software Engineer - 20197 | Cox | Atlanta GA | 0.3892 | 0.195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 256 | Senior Business Systems Analyst | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.6073 | 0.1905 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 257 | Senior Commercial Data & Insights Engineer | Dexcom | Remote - Spain | 0.5496 | 0.1905 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 258 | HR Data & Analytics Architect | CACI | 999 REMOTE | 0.4906 | 0.1905 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 259 | Oracle EPM Integration Lead | CACI | Remote (Any State) | 0.4128 | 0.1905 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 260 | Senior Software Developer / HR Technology & Shared Services / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Developer / HR Technology & Shared Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.1905 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, SQL, Python |
| 261 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.6624 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 262 | Software Engineer II, Mission Interface | Torc Robotics | Ann Arbor, MI | 0.6096 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 263 | Software Engineer I | LexisNexis Risk Solutions | Colorado | 0.4234 | 0.1863 | SWE_FULLTIME | SQL, data modeling |
| 264 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.5825 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 265 | ENGINEER, FW & PRODUCT TEST ENGINEERING | Micron Technology | Arzano (NA), Italy | 0.3292 | 0.1863 | SWE_FULLTIME | Python |
| 266 | Firmware Engineer Data Center Solid State Drives | Micron Technology | Arzano (NA), Italy | 0.3054 | 0.1863 | SWE_FULLTIME | Python |
| 267 | Appian Product Engineer  | Appian | McLean, Virginia | 0.4941 | 0.1863 | SWE_FULLTIME | SQL |
| 268 | Quality Assurance Engineer PON / DCOM | Ciena | Ottawa | 0.286 | 0.1863 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 269 | Lead Software Engineer , Backend | Capital One | Plano, TX | 0.5214 | 0.1725 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Python |
| 270 | Lead Software Engineer, Back End | Capital One | Plano, TX | 0.4981 | 0.1725 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Python |
| 271 | Lead Data Engineer | Capital One | Wilmington, DE | 0.7087 | 0.1717 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python |
| 272 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.5378 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 273 | Senior Software Engineer | Cadence Design Systems | SAN JOSE | 0.6448 | 0.1717 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 274 | Architect - Personal Insurance Cross-Domain Architecture | Travelers | CT - Hartford | 0.5447 | 0.1717 | SWE_FULLTIME | Cloud Infrastructure, Python |
| 275 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.4754 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 276 | Senior Software Engineer, Full-Stack — Content Tools | Epic Kids | Bangalore, India (remote within India) | 0.4626 | 0.1717 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL, data modeling |
| 277 | Senior Product Data Scientist | MaintainX | Montreal, Toronto, Vancouver, SF (Remote) | 0.457 | 0.1717 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python |
| 278 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.4752 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, data modeling |
| 279 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6359 | 0.1717 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 280 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6622 | 0.1717 | ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 281 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.525 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 282 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 283 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 284 | Software Development Engineer | Micron Technology | Taoyuan - Fab 11, Taiwan | 0.5003 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 285 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 286 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 287 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 288 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 289 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4812 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 290 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 291 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 292 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4632 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 293 | QE PCT Engineer | Micron Technology | Miaoli - Tongluo, Taiwan | 0.4235 | 0.1675 | SWE_FULLTIME | Python, SQL |
| 294 | Sr. Lead Software Engineer | Capital One | Bangalore, In | 0.5497 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MySQL |
| 295 | Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5014 | 0.1605 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, R |
| 296 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.1605 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, R |
| 297 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.4813 | 0.1605 | ML_ENGINEER_FULLTIME | Machine Learning, Python, R |
| 298 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.4632 | 0.1605 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 299 | Senior Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.4619 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 300 | Senior Data Engineer- Customer Data Platform | LexisNexis Risk Solutions | UK - Sutton (Carshalton) | 0.4317 | 0.1605 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 301 | M365 Developer | CACI | Remote (Any State) | 0.4972 | 0.155 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 302 | (Remote) System Analyst/Software Developer | Harris Computer | Office - Blair | 0.3286 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 303 | Product Engineer | Linear | North America | 0.4519 | 0.155 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 304 | Engineer Software T1/T2 | Northrop Grumman | GAWR03GC | 0.3461 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 305 | Software Engineer II | Cadence Design Systems | SAN JOSE | 0.4196 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 306 | Senior Cyber Security Engineer – Security Services | General Motors | Warren, Michigan, United States of America | 0.5495 | 0.1538 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python, automation |
| 307 | Senior Embedded Software Engineer | Micron Technology | San Jose, CA | 0.7214 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 308 | Software Engineer - Compiler  | Sigma Computing | San Francisco, CA | 0.5799 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 309 | Senior Software Engineer - Fullstack | Sigma Computing | New York City, NY | 0.5856 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 310 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.4754 | 0.1538 | SWE_FULLTIME, RESEARCH_SCIENTIST_FULLTIME | Python |
| 311 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.4509 | 0.1538 | SWE_FULLTIME | Python |
| 312 | Lead Software/Controls Engineer | GE Vernova | Wilmington NC USA | 0.4187 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 313 | Lead Software Engineer | Cox | Austin TX | 0.499 | 0.1538 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 314 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.1538 | SWE_FULLTIME | Python |
| 315 | Software Engineer II-Team Lead (AWS, Typescript) | Travelers | CT - Hartford | 0.5281 | 0.153 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 316 | Lead Protection and Control Engineer | GE Vernova | Remote | 0.4757 | 0.153 | SWE_FULLTIME, SYSTEMS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 317 | Senior Engineer, Advanced Modeling & AI Solutions | Micron Technology | Boise, ID - Main Site | 0.4079 | 0.153 | ML_ENGINEER_FULLTIME | Machine Learning |
| 318 | SMTS, Software Engineering (Salesforce Expert) | Salesforce | India - Hyderabad | 0.5494 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 319 | Senior Software Developer – DevOps | General Motors | Markham, Ontario, Canada | 0.5412 | 0.1418 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Python |
| 320 | Senior Software Developer – Virtualization, SIL, and AI‑Enablement | General Motors | Markham, Ontario, Canada | 0.5397 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, automation |
| 321 | Advanced Data Analyst -MDM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4874 | 0.1418 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, ETL |
| 322 | Senior Network Engineer | NOV | Kochi, Kerala, India | 0.4802 | 0.1418 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 323 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4327 | 0.1418 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 324 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4198 | 0.1418 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Cloud Infrastructure, MySQL |
| 325 | Package Device Product Engineer (PDPE) Engineer | Micron Technology | Sanand - 303A - AT/SSD/MOD, India | 0.5796 | 0.1362 | SWE_FULLTIME | Python |
| 326 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1362 | SWE_FULLTIME | Python |
| 327 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5176 | 0.1362 | SWE_FULLTIME | Python |
| 328 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.5005 | 0.1362 | SWE_FULLTIME | Python |
| 329 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4813 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 330 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4633 | 0.1362 | SWE_FULLTIME | Python |
| 331 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4632 | 0.1362 | SWE_FULLTIME | Python |
| 332 | Software Development Engineer in Test | Medtronic | London, London, United Kingdom | 0.3251 | 0.1362 | SWE_FULLTIME | Python |
| 333 | GTM Engineer | Greenhouse | Ontario | 0.4752 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 334 | Associate ATE Software Engineer | Boeing | IND - Bangalore, India | 0.4469 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 335 | IT SOFTWARE ENGINEER | Micron Technology | Fab 10W, Singapore | 0.4194 | 0.1362 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 336 | Product Architect | Monster Energy | USA - Corona, CA | 0.5401 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 337 | Senior Software Engineer - C++/UI | General Motors | Mountain View, California, United States of America | 0.5715 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 338 | Sr. Software Engineer, Telemetry (Starlink) | SpaceX | Hawthorne, CA | 0.6232 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 339 | Advanced Software Engr | Honeywell | Hamilton Township, NJ, United States | 0.462 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 340 | Software Engineer - Compiler  | Sigma Computing | New York City, NY | 0.58 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 341 | Lead Software Engineer, Android (Kotlin & Jetpack Compose) | Capital One | McLean, VA | 0.5778 | 0.135 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 342 | Engineer I/Engineer II/Sr. Engineer/Sr Engineer II | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4631 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 343 | Engineering Technical Lead - I&C Embedded Software | GE Vernova | Wilmington NC USA | 0.3946 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 344 | Sr. Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 345 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.5769 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 346 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.5758 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 347 | Software Engineer, Security | Notion | San Francisco, California | 0.7173 | 0.135 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 348 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4327 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 349 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4318 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 350 | Senior Technical Designer | Sony Interactive Entertainment | United States, Santa Monica, CA | 0.4603 | 0.135 | SWE_FULLTIME | — |
| 351 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in New York, New York / Careers at SIG | 0.72 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 352 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4327 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 353 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4316 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 354 | .NET/C# Engineer, TD Securities | TD Bank | Toronto, Ontario | 0.3795 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 355 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.123 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 356 | Software Engineer Developer ( Mid-Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 357 | Software Developer (Mid Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.1118 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 358 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5111 | 0.1118 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Python, data modeling |
| 359 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4278 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, data modeling |
| 360 | Sr. QA Engineer - IP Routing | Ciena | Remote-Canada | 0.4707 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 361 | Sr. Electricity Market Optimization Software Engineer | GE Vernova | Bellevue | 0.448 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 362 | Senior ABAP Developer | CACI | Remote (Any State) | 0.3919 | 0.1118 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 363 | Audio Programmer | Sony Interactive Entertainment | United Kingdom, London | 0.5209 | 0.105 | SWE_FULLTIME | — |
| 364 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.105 | SWE_FULLTIME | — |
| 365 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.105 | SWE_FULLTIME | — |
| 366 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5004 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 367 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.105 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 368 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.105 | SWE_FULLTIME | — |
| 369 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4633 | 0.105 | SWE_FULLTIME | — |
| 370 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.4543 | 0.105 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | — |
| 371 | ML Engineer, II - App Engine | Torc Robotics | Ann Arbor, MI, Montreal, Canada | 0.4928 | 0.105 | SWE_FULLTIME | — |
| 372 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4327 | 0.105 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 373 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4197 | 0.105 | SWE_FULLTIME | — |
| 374 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4086 | 0.105 | SWE_FULLTIME | — |
| 375 | Software Engineering MTS - Compliance Automation & Tooling (Apex, Python) | Salesforce | India - Hyderabad | 0.5792 | 0.1005 | SWE_FULLTIME | Python, SQL |
| 376 | Senior Software Engineer | GE Vernova | Bucharest | 0.5514 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 377 | Sr Embedded Software Engineer | Dexcom | San Diego, California | 0.5218 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 378 | Senior Process Engineer (Oil and Gas, EPC, Midstream) | NOV | Dubai, Dubai, United Arab Emirates | 0.4463 | 0.093 | SWE_FULLTIME | — |
| 379 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 380 | Senior Software Engineer | EarnIn | Mexico City, Mexico | 0.643 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 381 | Senior Discipline Engineer | Valeo | Chennai | 0.5507 | 0.0817 | SWE_FULLTIME | Python |
| 382 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.5494 | 0.0817 | SWE_FULLTIME | Python |
| 383 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.4294 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 384 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.0817 | SWE_FULLTIME | Python |
| 385 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.0817 | SWE_FULLTIME | SQL |
| 386 | Software Engineering, SMTS (Salesforce Developer) | Salesforce | India - Hyderabad | 0.4755 | 0.0817 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 387 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5744 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 388 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, Liverpool | 0.5759 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 389 | Quality Engineer Lead | LexisNexis Risk Solutions | Mumbai | 0.5798 | 0.063 | SWE_FULLTIME | — |
| 390 | Senior Discipline Engineer - Software Requirements | Valeo | Chennai | 0.5507 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 391 | Sr Full Stack Developer, TD Securities | TD Bank | Toronto, Ontario | 0.5025 | 0.063 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 392 | Experienced Software Application Development – QA and Test Automation Engineer | Boeing | IND - Bangalore, India | 0.5019 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 393 | Experienced Software Application Development – QA and Test Automation Engineer | Boeing | IND - Bangalore, India | 0.5019 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 394 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 395 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.4632 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 396 | Sr IT Analyst | Honeywell | Bengaluru, Karnataka, India | 0.4619 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 397 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.4587 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 398 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4327 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 399 | IT Developer (Java), TD Securities | TD Bank | Toronto, Ontario | 0.3363 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 400 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4198 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 401 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.063 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |

## Nishant Jethwa (`user1@example.com`)

**Candidate ID:** `aa79f43d-3122-480a-88ab-2a1be7138529`

### Subscribed pools
- `BACKEND_ENGINEER_FULLTIME`
- `SWE_FULLTIME`
- `FULLSTACK_ENGINEER_FULLTIME`
- `DEVOPS_ENGINEER_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Full Stack Development, Machine Learning, Research, Cloud Infrastructure, DevOps, Security Engineering |
| Preferred locations | United Sates, California, Seattle |
| Primary roles | Backend Engineer, Full Stack Engineer, Java Engineer, DevOps Engineer, Software Engineer |
| Hard constraints | sponsorship=True, min_salary=None, target_seniority=INTERN, NEW_GRAD, ENTRY, MID, JUNIOR |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 488
- **Notification-eligible jobs (≤60d, not yet emailed):** 488
- **Personal score range:** 0.036 – 0.4195 (144 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `BACKEND_ENGINEER_FULLTIME` | 321 |
| `SWE_FULLTIME` | 282 |
| `DEVOPS_ENGINEER_FULLTIME` | 95 |
| `FULLSTACK_ENGINEER_FULLTIME` | 89 |
| `ML_ENGINEER_FULLTIME` | 52 |
| `FRONTEND_ENGINEER_FULLTIME` | 29 |
| `DATA_ENGINEER_FULLTIME` | 23 |
| `SECURITY_ENGINEER_FULLTIME` | 14 |
| `SUPPORT_ENGINEER_FULLTIME` | 6 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 6 |
| `MOBILE_ENGINEER_FULLTIME` | 5 |
| `SYSTEMS_ENGINEER_FULLTIME` | 2 |
| `RESEARCH_SCIENTIST_FULLTIME` | 1 |
| `MARKETING_FULLTIME` | 1 |
| `DATA_ANALYST_FULLTIME` | 1 |
| `DATA_SCIENTIST_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Software Engineer II @ Cox

- **Location:** Atlanta GA (unclear)
- **Posted:** 2026-06-10T00:00:00+00:00
- **Salary:** 89400 – 134000
- **Effort:** MEDIUM
- **Opportunity score:** 0.3987
- **Personal score:** 0.4195
- **Pools:** `SWE_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, FULLSTACK_ENGINEER
- **Capabilities:** Full Stack Development, Backend Engineering, Frontend Engineering, Cloud Infrastructure, DevOps
- **Skills:** secure coding, system integration
- **Match reasons:** Full Stack Development, Cloud Infrastructure, DevOps, TypeScript, Angular
- **URL:** https://cox.wd1.myworkdayjobs.com/Cox_External_Career_Site_1/job/Atlanta-GA/Software-Engineer-II---20200_R202678358

#### #2 — Cloud Developer @ Freedom Technology Solutions Group

- **Location:** Chantilly, VA (unclear)
- **Posted:** 2026-06-12T18:40:32+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5985
- **Personal score:** 0.3846
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER
- **Capabilities:** Cloud Infrastructure, DevOps, Backend Engineering
- **Skills:** infrastructure as code, CI/CD pipelines, cloud architecture
- **Match reasons:** Cloud Infrastructure, DevOps, Java, Python
- **URL:** https://job-boards.greenhouse.io/freedomconsulting/jobs/4831214007

#### #3 — Software Engineer, Machine Learning @ Whoop

- **Location:** Boston, MA (unclear)
- **Posted:** 2026-06-11T18:40:49.846000+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5388
- **Personal score:** 0.3846
- **Pools:** `ML_ENGINEER_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** ML_ENGINEER, BACKEND_ENGINEER
- **Capabilities:** Machine Learning, Backend Engineering, Full Stack Development
- **Skills:** machine learning models, production services, API design, observability
- **Match reasons:** Machine Learning, Full Stack Development, Java, Python
- **URL:** https://jobs.lever.co/whoop/d8b1c557-bf1a-40ca-850a-74d4e91728fe

#### #4 — Software Engineer, Full-Stack @ Loop

- **Location:** San Francisco, CA (unclear)
- **Posted:** 2026-06-08T17:04:05+00:00
- **Salary:** 150000 – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.4343
- **Personal score:** 0.3846
- **Pools:** `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** FULLSTACK_ENGINEER
- **Capabilities:** Full Stack Development, Backend Engineering, Frontend Engineering, Cloud Infrastructure
- **Skills:** distributed systems, logistics software
- **Match reasons:** Full Stack Development, Cloud Infrastructure, TypeScript, Node.js
- **URL:** https://job-boards.greenhouse.io/loop/jobs/4102236004

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Software Engineer II | Cox | Atlanta GA | 0.3987 | 0.4195 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 2 | Cloud Developer | Freedom Technology Solutions Group | Chantilly, VA | 0.5985 | 0.3846 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 3 | Software Engineer, Machine Learning | Whoop | Boston, MA | 0.5388 | 0.3846 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Full Stack Development, Java |
| 4 | Software Engineer, Full-Stack | Loop | San Francisco, CA | 0.4343 | 0.3846 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, TypeScript |
| 5 | DevSecOps Engineer | General Dynamics Mission Systems | US-Telework-Telework | 0.5097 | 0.38 | DEVOPS_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Security Engineering |
| 6 | Mid-level Vulnerability Assessments & Infrastructure Specialist - Vulnerability & Attack Surface Management (VASM) | Boeing | USA - Kent, WA | 0.4136 | 0.38 | SECURITY_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Security Engineering, DevOps, Cloud Infrastructure |
| 7 | IT Systems Administrator | LG Ad Solutions | New York, NY | 0.5583 | 0.3715 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 8 | ML Engineer, Generative Video | Mirage | Union Square, New York City | 0.5091 | 0.3715 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 9 | Software Development Engineer II - General Motors Insurance | GM Financial | United States | 0.5005 | 0.3715 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 10 | Software Development Engineer I - General Motors Insurance | GM Financial | United States | 0.5005 | 0.3715 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 11 | Software Engineer I | LexisNexis Risk Solutions | Cardiff | 0.5806 | 0.3682 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 12 | Site Reliability Engineer II | PROS Holdings, Inc. | USA TX Houston Virtual | 0.5814 | 0.3583 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 13 | Digital Identity Services Life Cycle Specialist (Puerto Rico) | RTX | US-PR-SANTA ISABEL-B1 ~ Felicia Industrial Park - St B1 ~ BLDG 1 | 0.4324 | 0.3583 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 14 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, Aliso Viejo, CA | 0.5298 | 0.3528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 15 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, San Diego, CA | 0.5283 | 0.3528 | SWE_FULLTIME | Full Stack Development, DevOps, Python |
| 16 | Software Engineer II | Cox | Atlanta GA | 0.3996 | 0.3528 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, TypeScript |
| 17 | Software Engineer, Network Monitoring (Starlink) | SpaceX | Hawthorne, CA | 0.4365 | 0.3528 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Python |
| 18 | Software Engineer | Intel | US, Arizona, Phoenix | 0.6671 | 0.3396 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 19 | Mid-Level DevOps Developer | Boeing | USA - Hazelwood, MO | 0.487 | 0.3396 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 20 | Software Engineer II | Cox | Atlanta GA | 0.4239 | 0.3396 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Security Engineering, SQL |
| 21 | Software Engineer II (Java) | Sony Interactive Entertainment | United States, Madison, WI | 0.5699 | 0.3396 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 22 | Software Engineer, Hardware-in-the-Loop (Starlink) | SpaceX | Redmond, WA | 0.4987 | 0.3396 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 23 | Software Engineer for Data at Rest (DAR) Crypto & Cross Domain Solutions | General Dynamics Mission Systems | US-MA-Dedham | 0.4222 | 0.3396 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, DevOps, Python |
| 24 | Software Engineer, Test Infrastructure (Application Software) | SpaceX | Hawthorne, CA | 0.4754 | 0.3396 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 25 | Software Engineer, Developer Productivity  | Glean | Mountain View, CA | 0.4989 | 0.3396 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 26 | Associate Systems Administrator | Boeing | USA - Sylmar, CA | 0.3267 | 0.3396 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 27 | Full‑Stack Machine Learning Engineer | LexisNexis Risk Solutions | UK - London (London Wall) | 0.5016 | 0.3313 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Full Stack Development, DevOps |
| 28 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.549 | 0.3311 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, SQL |
| 29 | Continuous Integration/Continuous Development Engineer | Monster Energy | USA - Corona, CA | 0.5845 | 0.3265 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, .NET |
| 30 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.3265 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, SQL |
| 31 | Software Engineer II | Cox | Austin TX | 0.4597 | 0.3265 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, JavaScript |
| 32 | Software Infrastructure Engineer (Starlink) | SpaceX | Palo Alto, CA | 0.4885 | 0.3265 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 33 | Kubernetes Platform Infrastructure Engineer (Starlink) | SpaceX | Redmond, WA | 0.4863 | 0.3265 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 34 | Software Infrastructure Engineer (Starlink) | SpaceX | Redmond, WA | 0.4691 | 0.3265 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 35 | Software Engineer, Platform | ScaleAI | San Francisco, CA; New York, NY | 0.6413 | 0.3265 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, MongoDB |
| 36 | Software Engineer I, Service Network - Slack | Slack (Salesforce) | Washington - Seattle | 0.4673 | 0.3265 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 37 | Linux System Administrator | CACI | National Harbor, MD, US | 0.4619 | 0.3265 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Security Engineering, Python |
| 38 | Oracle HCM Cloud Platform & DevOps Engineer | CACI | Ashburn, VA, US | 0.4777 | 0.3265 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 39 | AI Engineer III - Agentic AI | American Express | Phoenix, AZ, United States | 0.5497 | 0.318 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, TypeScript |
| 40 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.318 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, TypeScript |
| 41 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4469 | 0.318 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, TypeScript |
| 42 | Network Engineer 1/Network Engineer 2/Network Engineer 3 | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4318 | 0.318 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 43 | Network Engineer | Northrop Grumman | United States-California-San Diego | 0.4719 | 0.3133 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 44 | Engineering Technical Specialist (Associate + Mid-Level) | Boeing | USA - Hazelwood, MO | 0.4032 | 0.3133 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 45 | DevSecOps Software Engineer (Associate or Experienced), Phantom Works | Boeing | USA - Saint Charles, MO | 0.3778 | 0.3133 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 46 | Associate Computer Systems Architect/Computer Systems Architect (Level 1/2) | Northrop Grumman | United States-California-Manhattan Beach | 0.4079 | 0.3133 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 47 | Software Engineer, Compute Infrastructure | Glean | Mountain View, CA | 0.5245 | 0.3133 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 48 | Network Communications | Northrop Grumman | United States-Virginia-McLean | 0.3239 | 0.3133 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 49 | R&D AI Platform Engineer / Administrator | Ciena | Ottawa | 0.4191 | 0.31 | BACKEND_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, DevOps |
| 50 | Mid Level DevOps Engineer  | Freedom Technology Solutions Group | Annapolis Junction, MD | 0.4501 | 0.31 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Security Engineering |
| 51 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.5272 | 0.3048 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 52 | ML Engineer, Agentic Systems | Mirage | Union Square, New York City | 0.5075 | 0.3048 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 53 | Software Engineer 2 | Berkshire Hathaway Energy | Des Moines, IA, United States | 0.4628 | 0.3048 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, .NET |
| 54 | Factory Software Engineer (Starlink) | SpaceX | Bastrop, TX | 0.4246 | 0.3048 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 55 | Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4386 | 0.3015 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 56 | Associate Linux/Window Engineer / Platform Services / Experienced Hire | Susquehanna International Group (SIG) | Associate Linux/Window Engineer / Platform Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.3015 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 57 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.2993 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Java, Python |
| 58 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.2993 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Java, Python |
| 59 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.2993 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | DevOps, Java, JavaScript |
| 60 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.2993 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | DevOps, Java, JavaScript |
| 61 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4251 | 0.291 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 62 | Data Center Deployment Specialist | NVIDIA | Germany, Remote | 0.5509 | 0.2883 | SUPPORT_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 63 | Systems Engineer I | Stewart | USA TX - Remote | 0.5016 | 0.2883 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 64 | Embedded SW Development Engineer | GE Vernova | Zamudio | 0.4314 | 0.2883 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 65 | Infrastructure Engineer | RTX | Gloucester, South Gloucestershire | 0.4198 | 0.2883 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 66 | Solutions Architect | Centerfield | Los Angeles, California | 0.4688 | 0.2866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Machine Learning, Full Stack Development |
| 67 | Marketing Productivity Engineer | Sigma Computing | San Francisco, CA | 0.626 | 0.2861 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Python |
| 68 | AI Builder Partner Solutions | Salesforce | California - San Francisco | 0.6822 | 0.2861 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, TypeScript |
| 69 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5344 | 0.2861 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, SQL, JavaScript |
| 70 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.2861 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Java, Python |
| 71 | Software Engineer I | Cox | Austin TX | 0.4688 | 0.2861 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, TypeScript |
| 72 | Software Engineer (Front End) | CACI | Aurora, CO, US | 0.3868 | 0.2861 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Flask |
| 73 | Software Engineer II - 20202 | Cox | Atlanta GA | 0.3445 | 0.2861 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, TypeScript, Java |
| 74 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6359 | 0.2833 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 75 | Software Engineer ll - Java 8 Reactjs Web Search Team | American Express | Phoenix, AZ, United States | 0.5327 | 0.2787 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 76 | Quality Engineer II | RELX | Philadelphia, PA | 0.4851 | 0.273 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, JavaScript, TypeScript |
| 77 | Software Engineer - SDET | Sigma Computing | San francisco, CA | 0.5848 | 0.273 | BACKEND_ENGINEER_FULLTIME | DevOps, Python, SQL |
| 78 | Software Engineer | Aquatic Capital Management | New York | 0.608 | 0.273 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 79 | Software Engineer, Full-Stack | Loop | New York, NY, USA | 0.4357 | 0.273 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Node.js |
| 80 | Software Engineer, Full-Stack | Loop | Chicago, IL | 0.4356 | 0.273 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Node.js |
| 81 | Print, Mail & Data System Engineer | Travelers | GA - Norcross | 0.4636 | 0.2696 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 82 | Site Reliability Engineer II | American Express | LONDON, United Kingdom | 0.502 | 0.2646 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 83 | IT Engineer | Micron Technology | Fab 10W, Singapore | 0.4874 | 0.2646 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Angular |
| 84 | AI-Enabled Full Stack Developer - Experienced | Micron Technology | Taichung - AATT, Taiwan | 0.4617 | 0.2646 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Angular |
| 85 | Développeur de logiciel | Harris Computer | Quebec, Canada | 0.3817 | 0.2646 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, .NET |
| 86 | CAD Engineer | Micron Technology | Richardson, TX | 0.5796 | 0.2645 | SWE_FULLTIME | Python, C, Java |
| 87 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4755 | 0.2645 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, JavaScript |
| 88 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.4115 | 0.2645 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, Flask, SQL |
| 89 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI, Fort Worth, TX | 0.6387 | 0.2598 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 90 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2598 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, SQL |
| 91 | Software Engineering I | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2598 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, SQL |
| 92 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.6717 | 0.2598 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 93 | Software Engineer | General Dynamics Mission Systems | US-MA-Pittsfield | 0.4726 | 0.2598 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, C |
| 94 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.2598 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, C |
| 95 | RAN Validation Engineer (Starlink Mobile)  | SpaceX | Sunnyvale, CA | 0.4866 | 0.2598 | SWE_FULLTIME | DevOps, Python |
| 96 | Computing Architect (Manhattan Warehouse M.S.) | Boeing | USA - Hialeah, FL | 0.4289 | 0.2598 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 97 | Software Engineer | General Dynamics Mission Systems | US-MA-Pittsfield | 0.3431 | 0.2598 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, C |
| 98 | Full Stack Developer (Remote) | RTX | US-CT-REMOTE | 0.4136 | 0.2598 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Python |
| 99 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2596 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 100 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2596 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 101 | Cloud Support Engineer - Managed Cloud Services | Cadence Design Systems | SAN JOSE | 0.5971 | 0.2565 | SUPPORT_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 102 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4145 | 0.2565 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 103 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4439 | 0.2565 | SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 104 | Senior Cybersecurity Vulnerability Management Engineer | General Motors | Warren, Michigan, United States of America | 0.5511 | 0.255 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Cloud Infrastructure, DevOps |
| 105 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.2515 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 106 | Site Reliability Engineer | EarnIn | Bengaluru, India | 0.4765 | 0.2515 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 107 | Embedded Software Engineer - Electrification | General Motors | Milford, Michigan, United States of America | 0.5495 | 0.2513 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, Python |
| 108 | Data Engineer | Base Power Company | Austin, TX | 0.4691 | 0.2513 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 109 | Forward Deployed Engineer  | Loop | San Francisco, CA | 0.4398 | 0.2513 | SWE_FULLTIME | Python, SQL |
| 110 | Appian Product Engineer  | Appian | McLean, Virginia | 0.4941 | 0.248 | SWE_FULLTIME | Full Stack Development, SQL, Java |
| 111 | Data Center Operations Engineer II  | Sony Interactive Entertainment | United States, Manassas, VA | 0.5969 | 0.2467 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 112 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5114 | 0.2467 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps |
| 113 | Associate and Experienced Software Engineers - Secure Network & Protocols | Boeing | USA - Oklahoma City, OK | 0.2598 | 0.2467 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 114 | Sr. Lead Software Engineer | Capital One | Bangalore, In | 0.5497 | 0.2462 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 115 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6252 | 0.2438 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, DevOps |
| 116 | Lead Machine Learning Engineer | Capital One | McLean, VA | 0.5586 | 0.2438 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, DevOps |
| 117 | Experienced ServiceNow Operations Specialist | Boeing | IND - Bangalore, India | 0.5512 | 0.2383 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 118 | Systems Engr II | Honeywell | Delhi, India | 0.4812 | 0.2383 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 119 | Développeur(se) mobile logiciel | MaintainX | Montreal, Quebec  | 0.4715 | 0.2383 | MOBILE_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 120 | DevOps Engineer  | Remodel Health | Indianapolis, IN | 0.4423 | 0.2383 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 121 | IT STORAGE ENGINEER | Micron Technology | Taichung - Fab 16, Taiwan | 0.4194 | 0.2383 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 122 | Internal Channel Systems Engineer | Fortinet | LONDON, United Kingdom | 0.4079 | 0.2383 | SOLUTIONS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Security Engineering |
| 123 | Forward Deployed Engineer I/II | Giga AI | San Francisco | 0.5602 | 0.2382 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 124 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5797 | 0.2382 | SWE_FULLTIME | Python |
| 125 | Software Engineer - Defense Applications | Palantir | New York, NY | 0.5474 | 0.2382 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | TypeScript |
| 126 | Software Engineer - Core Interfaces | Palantir | New York, NY | 0.5451 | 0.2382 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | JavaScript |
| 127 | Embedded Software Engineer II | CesiumAstro | El Segundo, CA | 0.4757 | 0.2382 | BACKEND_ENGINEER_FULLTIME | C |
| 128 | Embedded Software Engineer II | CesiumAstro | Austin, TX | 0.4757 | 0.2382 | BACKEND_ENGINEER_FULLTIME | C |
| 129 | Embedded Software Engineer II | CesiumAstro | Westminster, CO | 0.4757 | 0.2382 | BACKEND_ENGINEER_FULLTIME | C |
| 130 | Senior Full-Stack Software Engineer, (Forward Deployed), GPS | ScaleAI | Doha, Qatar  | 0.4019 | 0.2367 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 131 | Senior Security Engineer - Proxy & Cloud Security Platform | Truist Bank | Atlanta, GA | 0.5304 | 0.2359 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Cloud Infrastructure, DevOps |
| 132 | Sr Lead Software Engineer (Full Stack) | Capital One | McLean, VA | 0.6252 | 0.2354 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 133 | Lead Software Engineer, Full Stack (Golang, Angular, AWS) | Capital One | Richmond, VA | 0.5221 | 0.2354 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 134 | Software Engineer II - AI Focused | Cadence Design Systems | BELO HORIZONTE | 0.549 | 0.2348 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 135 | Product Engineer | Linear | North America | 0.4519 | 0.2348 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript |
| 136 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.2326 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Java, JavaScript, TypeScript |
| 137 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3632 | 0.2326 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, JavaScript, Python |
| 138 | Sr Software Engineer I - Java - International Card Risk Services Technology | American Express | Phoenix, AZ, United States | 0.5514 | 0.2308 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 139 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4755 | 0.2308 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 140 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4632 | 0.2308 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 141 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.4865 | 0.228 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Security Engineering |
| 142 | Lead Software Engineer | Capital One | McLean, VA | 0.628 | 0.2275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 143 | Lead Software Engineer | Capital One | McLean, VA | 0.6279 | 0.2275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 144 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6358 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 145 | Lead Software Engineer, Fullstack (React, Java, Python) | Capital One | New York, NY | 0.6247 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 146 | Lead Software Engineer | Capital One | McLean, VA | 0.5711 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 147 | Lead Software Engineer (Java, Golang, AWS) | Capital One | Plano, TX | 0.5413 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 148 | Senior Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.6194 | 0.2275 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 149 | Senior Lead Software Engineer, Full Stack (Global Payment Network) | Capital One | Riverwoods, IL | 0.6053 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 150 | Lead Software Engineer, Full Stack (Risk Tech, Intelligent Foundations & Experiences) | Capital One | New York, NY | 0.5944 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 151 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Java |
| 152 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5771 | 0.2275 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Java |
| 153 | Lead Software Engineer, Full Stack (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.5497 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 154 | Lead Software Engineer, Full Stack | Capital One | Riverwoods, IL | 0.5221 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 155 | Senior Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.6085 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 156 | Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.5712 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 157 | Lead Software Engineer, Full Stack | Capital One | Richmond, VA | 0.53 | 0.2275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 158 | Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.5175 | 0.2275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 159 | Sr. Network Engineer | Lambda | San Francisco Office (Fremont St) / San Jose Office (Zanker) / San Jose Office (First St) / Bellevue, WA | 0.591 | 0.2229 | DEVOPS_ENGINEER_FULLTIME, SYSTEMS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 160 | Cloud Network Engineer III (Anchorage, Alaska) | GCI | Anchorage, AK, United States | 0.4469 | 0.2229 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 161 | Software Engineer III - MFT Business Enablement - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4422 | 0.2229 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 162 | Senior IT Systems Engineer | Brain Co. | San Francisco Bay Area | 0.4236 | 0.2229 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 163 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3562 | 0.2196 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 164 | Software Engineer I (AI Driven) | Travelers | GA - Atlanta | 0.5232 | 0.2195 | SWE_FULLTIME | Python, Java, SQL |
| 165 | Information & Application Developer (Entry Level and Associate) | Boeing | USA - North Charleston, SC | 0.4034 | 0.2195 | SWE_FULLTIME, DATA_ANALYST_FULLTIME | Python, SQL, JavaScript |
| 166 | Entry Level Software Engineer - Austin, TX | Cox | Austin TX | 0.3807 | 0.2195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, JavaScript, HTML |
| 167 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3242 | 0.2195 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, JavaScript, Python |
| 168 | Advanced Software Engineer | Honeywell | Charlotte, NC, United States | 0.5798 | 0.215 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure |
| 169 | Sr IT Engineer | Honeywell | Phoenix, AZ, United States | 0.4086 | 0.215 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 170 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.4632 | 0.2146 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 171 | Senior Solutions Architect, IPP | NVIDIA | US, CA, Santa Clara | 0.7816 | 0.2117 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 172 | Senior Software Engineer | Cox | Atlanta GA | 0.5311 | 0.2117 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 173 | Sr Software Engineer - 20198 | Cox | Atlanta GA | 0.4833 | 0.2117 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, TypeScript |
| 174 | Lead Software Engineer, DevOps | Capital One | Riverwoods, IL | 0.5721 | 0.2117 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 175 | Lead Software Engineer, DevOps - Card Tech | Capital One | McLean, VA | 0.572 | 0.2117 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 176 | Lead Software Engineer, DevOps - Card Tech | Capital One | McLean, VA | 0.572 | 0.2117 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 177 | Senior Lead Software Engineer, DevOps | Capital One | McLean, VA | 0.6393 | 0.2117 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 178 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2117 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Java |
| 179 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2117 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Java |
| 180 | Lead Software Engineer, DevOps | Capital One | Richmond, VA | 0.5362 | 0.2117 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Java |
| 181 | Associate Engineer - Fullstack (Hybrid) | RTX | IN-TS-HYDERABAD-B3F7 ~ DLF Cybercity Gachibowli ~ DLF CYBERCITY GACHIBOWLI-B3F7, 7th Fl in Block 3 | 0.5015 | 0.2111 | FULLSTACK_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Full Stack Development, JavaScript, TypeScript |
| 182 | C# Full-Stack Developer - Experienced Hire | Susquehanna International Group (SIG) | C# Full-Stack Developer - Experienced Hire in Dublin / Careers at SIG | 0.52 | 0.2111 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, .NET, Python |
| 183 | Senior Network Engineer | NOV | Kochi, Kerala, India | 0.4802 | 0.2067 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Security Engineering |
| 184 | Support AI Engineer | Figma | San Francisco, CA • New York, NY • United States | 0.6949 | 0.2063 | BACKEND_ENGINEER_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Python, TypeScript |
| 185 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Palo Alto, CA | 0.4864 | 0.2063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, Python |
| 186 | DevOps Engineer, GPS | ScaleAI | Dubai, UAE; Riyadh, Saudi Arabia | 0.5333 | 0.2046 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 187 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7801 | 0.2038 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 188 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7513 | 0.2038 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 189 | Senior Lead AI Engineer (GenAI Platform Services) | Capital One | San Jose, CA | 0.7497 | 0.2038 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 190 | Senior Failure Analysis Engineer | NVIDIA | US, CA, Santa Clara | 0.6616 | 0.2038 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 191 | Senior ML Ops Engineer | RELX | Philadelphia, PA | 0.5653 | 0.2038 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 192 | Senior DevOps Developer | Boeing | USA - Hazelwood, MO | 0.5671 | 0.2038 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 193 | Senior Software Engineer | Cox | Atlanta GA | 0.4445 | 0.2038 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, TypeScript |
| 194 | Senior Lead AI Engineer,(MLX, Agentic AI, Gen AI platform Services) | Capital One | San Jose, CA | 0.6325 | 0.2038 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 195 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5781 | 0.2038 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 196 | Sr Lead Site Reliability & Systems Engineer | Cox | Austin TX | 0.5713 | 0.2038 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 197 | Senior Machine Learning Engineer (AI Foundations) | Capital One | McLean, VA | 0.5022 | 0.2038 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 198 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.4929 | 0.2038 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 199 | Lead Platform Engineer - Palo Alto (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4773 | 0.2038 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 200 | ​Senior Site Reliability Engineer  | Cox | Austin TX | 0.439 | 0.2038 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 201 | Senior Platform Engineer | Capital One | Richmond, VA | 0.4258 | 0.2038 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 202 | Senior Lead AI Engineer (Gen AI Platform Services) | Capital One | San Jose, CA | 0.6085 | 0.2038 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 203 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2038 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 204 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5541 | 0.2038 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 205 | Lead AI Engineer (MLX) | Capital One | New York, NY | 0.5535 | 0.2038 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 206 | Software Engineer II, EV | EnergyHub | Remote - United States | 0.4311 | 0.203 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Java, TypeScript |
| 207 | (Remote) System Analyst/Software Developer | Harris Computer | Office - Blair | 0.3286 | 0.203 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Angular, TypeScript |
| 208 | DevSecOps AWS Engineer | CACI | Remote (Any State) | 0.5643 | 0.2018 | DEVOPS_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Security Engineering |
| 209 | Full Stack Software Engineer | Manulife Financial | Hong Kong | 0.549 | 0.1988 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 210 | Senior Cyber Security Engineer – Security Services | General Motors | Warren, Michigan, United States of America | 0.5495 | 0.1987 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Security Engineering, Python, JavaScript |
| 211 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5004 | 0.198 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Java, JavaScript |
| 212 | Experienced Fullstack Software Engineer | Boeing | POL - Gdansk, Poland | 0.5002 | 0.198 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, JavaScript, TypeScript |
| 213 | Software Engineer II | American Express | Gurugram, HR, India | 0.4632 | 0.198 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Java |
| 214 | Senior Software Engineer, Full-Stack — Content Tools | Epic Kids | Bangalore, India (remote within India) | 0.4626 | 0.1967 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Angular |
| 215 | Senior Software Developer / HR Technology & Shared Services / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Developer / HR Technology & Shared Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.1967 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 216 | Senior Inference Engineer, AIConfigurator for Dynamo | NVIDIA | US, CA, Santa Clara | 0.7794 | 0.1959 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, Python |
| 217 | Senior Site Reliability Engineer | RELX | Philadelphia, PA | 0.5916 | 0.1959 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 218 | Sr. Software Engineer, Telemetry (Starlink) | SpaceX | Hawthorne, CA | 0.6232 | 0.1959 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, DevOps, Java |
| 219 | Senior Software Engineer - Fullstack | Sigma Computing | San Francisco, CA | 0.5665 | 0.1959 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, TypeScript |
| 220 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.5809 | 0.1959 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 221 | Lead DevOps Developer | Boeing | USA - Long Beach, CA | 0.5052 | 0.1959 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Angular |
| 222 | Expert Site Reliability Engineer | Harris Computer | Kentucky, United States | 0.3655 | 0.1959 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 223 | Advanced DevOps Specialist with Linux/RedHat | General Dynamics Mission Systems | US-MA-Dedham | 0.3921 | 0.1959 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 224 | Sr. Hardware / Infrastructure Site Reliability Engineer (Starlink) | SpaceX | Redmond, WA | 0.5232 | 0.1959 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 225 | Sr. Kubernetes Platform Site Reliability Engineer (Starlink)  | SpaceX | Redmond, WA | 0.5232 | 0.1959 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 226 | Sr. Software Infrastructure Engineer (Starlink) | SpaceX | Redmond, WA | 0.5226 | 0.1959 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 227 | Sr Software Engineer - 20197 | Cox | Atlanta GA | 0.3892 | 0.1959 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Java |
| 228 | Senior Gen AI Developer | KBR | El Segundo, California | 0.6387 | 0.1939 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, DevOps |
| 229 | Software Security Architect | Cadence Design Systems | SAN JOSE | 0.5956 | 0.1939 | SECURITY_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Security Engineering, DevOps, Cloud Infrastructure |
| 230 | Sr. Security Engineer II | iHerb | United States of America - Remote / Home Office | 0.5735 | 0.1939 | SECURITY_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Security Engineering |
| 231 | Software Engineer I | LivaNova | Houston, Texas, United States | 0.4256 | 0.1932 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | .NET |
| 232 | Software Engineer, CDN  (Starlink) | SpaceX | Redmond, WA | 0.4769 | 0.1932 | BACKEND_ENGINEER_FULLTIME | C |
| 233 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 234 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 235 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Redmond, WA | 0.4574 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 236 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Palo Alto, CA | 0.4864 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 237 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 238 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.1932 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 239 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5021 | 0.1909 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Cloud Infrastructure, DevOps |
| 240 | Senior Software Engineer  | Axiomatic AI | Boston, US | 0.5196 | 0.1908 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Python, TypeScript |
| 241 | Sr. Automation Engineer (Starlink Customer Success) | SpaceX | Bastrop, TX | 0.4731 | 0.1908 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 242 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.1908 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, TypeScript |
| 243 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.1908 | SWE_FULLTIME | DevOps, Python, Java |
| 244 | Java API Back End Developer | RELX | Pennsylvania | 0.5053 | 0.1898 | BACKEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Java |
| 245 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.5603 | 0.1898 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 246 | Software Engineer II, AI Platform | Cadence Design Systems | SAN JOSE | 0.4236 | 0.1898 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 247 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.4752 | 0.1888 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 248 | Lead Software Engineer (Kubernetes) | Appian | McLean, Virginia | 0.448 | 0.1888 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 249 | Power Platform and Dynamics 365 Administrator | CACI | Arlington, VA, US | 0.6093 | 0.188 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 250 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | New York City, NY | 0.5857 | 0.188 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 251 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | San Francisco, CA | 0.5856 | 0.188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 252 | Sr Software Engineer | Cox | Atlanta GA | 0.4437 | 0.188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure |
| 253 | Window System Administrator | CACI | National Harbor, MD, US | 0.4622 | 0.188 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 254 | Senior Network Engineer | CACI | Chantilly, VA, US | 0.437 | 0.188 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 255 | Service Now Sys Administrator | RTX | US-TX-REMOTE | 0.4371 | 0.188 | DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure |
| 256 | Lead Software Engineer , Backend | Capital One | Plano, TX | 0.5214 | 0.1875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, JavaScript, Java |
| 257 | Lead Software Engineer, Back End | Capital One | Plano, TX | 0.4981 | 0.1875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, JavaScript, Java |
| 258 | Associate Software Engineer - Analytics | Boeing | IND - Bangalore, India | 0.5019 | 0.1848 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Deep Learning |
| 259 | Forward Deployed Engineer | Nash | Australia | 0.5319 | 0.1848 | BACKEND_ENGINEER_FULLTIME, SOLUTIONS_ENGINEER_FULLTIME | Cloud Infrastructure, SQL |
| 260 | Application Engr II | Honeywell | Tianjin, China | 0.4316 | 0.1848 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 261 | Software Engineer, Agents  | Mirage | Union Square, New York City | 0.5078 | 0.1829 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 262 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5005 | 0.1829 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 263 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.4754 | 0.1829 | SWE_FULLTIME, RESEARCH_SCIENTIST_FULLTIME | Research, Python |
| 264 | Lead Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.463 | 0.1825 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 265 | Senior Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.4619 | 0.1825 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, JavaScript |
| 266 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4198 | 0.1825 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Java |
| 267 | Senior IT Analyst m/f/d | Honeywell | Bucuresti, Bucuresti, Romania | 0.4327 | 0.1809 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 268 | Senior Site Reliability Engineer | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.4254 | 0.1809 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 269 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5109 | 0.18 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 270 | 2026 Raytheon Full Time-Software Engineer I – EOIR Advanced Products and Solutions (Onsite) | RTX | US-TX-MCKINNEY-513WC ~ 2501 W University Dr ~ WING C BLDG | 0.3632 | 0.18 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 271 | Lead Software Engineer | Capital One | McLean, VA | 0.607 | 0.1796 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 272 | Lead Software/Controls Engineer | GE Vernova | Wilmington NC USA | 0.4187 | 0.1796 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, C, .NET |
| 273 | Lead Software Engineer (Scala, JavaScript) | Capital One | New York, NY | 0.5951 | 0.1796 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 274 | Lead Software Engineer | Capital One | McLean, VA | 0.5586 | 0.1796 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 275 | Lead Software Engineer (Python, Kubernetes) | Capital One | McLean, VA | 0.5497 | 0.1796 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Java |
| 276 | M365 Developer | CACI | Remote (Any State) | 0.4972 | 0.1767 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 277 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4469 | 0.175 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 278 | Senior Backend Software Engineer  - Global Commercial Services Technology | American Express | Seattle, WA, United States | 0.4086 | 0.175 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 279 | Senior Platform Engineer  | Clarity Innovations | Required  | 0.5354 | 0.173 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 280 | Senior Lead Data Engineer (Enterprise Platform Technology) (Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7512 | 0.1717 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Java, Python |
| 281 | Lead Data Engineer (Python, AWS, SQL, GenAI) (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.6947 | 0.1717 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 282 | Senior Fullstack/Frontend Engineer | General Motors | Sunnyvale, California, United States of America | 0.66 | 0.1717 | FULLSTACK_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Full Stack Development, JavaScript, TypeScript |
| 283 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6645 | 0.1717 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Cloud Infrastructure, Java, Python |
| 284 | Lead Software Engineer, Back End (Cloud Operations Resilience Engineering) | Capital One | Plano, TX | 0.5711 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 285 | Lead Software Engineer | Cox | Austin TX | 0.499 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Python |
| 286 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.4516 | 0.1717 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 287 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.4543 | 0.1717 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | DevOps |
| 288 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4327 | 0.1717 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 289 | Roku Engineer | TribalScale | Remote Office | 0.5331 | 0.1682 | MOBILE_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 290 | Senior Full Stack Software Engineer | Micron Technology | Taichung - AATT, Taiwan | 0.5244 | 0.1667 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Machine Learning, Python |
| 291 | GTM Engineer | Greenhouse | Ontario | 0.4752 | 0.1661 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Python |
| 292 | GTM Engineer | Greenhouse | British Columbia | 0.4751 | 0.1661 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Python |
| 293 | Senior Software Engineer, DGXC Data Services | NVIDIA | US, CA, Santa Clara | 0.7239 | 0.1638 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, Java |
| 294 | Lead AI Engineer (Vision model customization, VML) | Capital One | New York, NY | 0.6718 | 0.1638 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 295 | Senior Software Engineer - Backend | Sigma Computing | San Francisco, CA | 0.5736 | 0.1638 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Node.js, SQL |
| 296 | Senior Lead AI Engineer, Gen AI Platform | Capital One | New York, NY | 0.6809 | 0.1638 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 297 | Digital Transformation Manufacturing Engineer 2/3 | Northrop Grumman | United States-California-Northridge | 0.4318 | 0.1638 | SWE_FULLTIME | DevOps, Python, SQL |
| 298 | Senior AI/ML Engineer | Sigma Computing | San Francisco, CA | 0.6783 | 0.1638 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python, SQL |
| 299 | Lead AI Engineer (Vision model customization, VLM) | Capital One | New York, NY | 0.5932 | 0.1638 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 300 | Lead AI Engineer (AI Foundations, LLM Customization and Finetuning) | Capital One | Cambridge, MA | 0.5782 | 0.1638 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 301 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.1638 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 302 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5652 | 0.1638 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 303 | Lead Machine Learning Engineer | Capital One | Cambridge, MA | 0.5286 | 0.1638 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 304 | Software Engineer I | LexisNexis Risk Solutions | Colorado | 0.4234 | 0.1626 | SWE_FULLTIME | Java, JavaScript, SQL |
| 305 | Networking/Security Software Engineer - SMTS | Salesforce | India - Hyderabad | 0.5792 | 0.1588 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering, Cloud Infrastructure, Java |
| 306 | SMTS, Software Engineering (Salesforce Expert) | Salesforce | India - Hyderabad | 0.5494 | 0.1588 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Node.js |
| 307 | Senior Software Developer, Tooling Team | MaintainX | Toronto, Ontario, Canada | 0.5295 | 0.1588 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Node.js |
| 308 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.4591 | 0.1588 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, DevOps, Python |
| 309 | AI Automation Engineer, Security | NVIDIA | US, CA, Santa Clara | 0.7611 | 0.1559 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | DevOps, Python |
| 310 | Senior Software Engineer - Storage | NVIDIA | US, CA, Santa Clara | 0.7218 | 0.1559 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 311 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7489 | 0.1559 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 312 | Senior Software Engineer NAVAIR Product Line | CACI | Austin, TX, US | 0.5443 | 0.1559 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java |
| 313 | Senior Software Engineer - Fullstack | Sigma Computing | New York City, NY | 0.5856 | 0.1559 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, SQL |
| 314 | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire in New York, New York / Careers at SIG | 0.6962 | 0.1559 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 315 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.5378 | 0.1539 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, SQL |
| 316 | Senior Software Engineer - Operating System | Torc Robotics | Ann Arbor, MI | 0.4758 | 0.1539 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 317 | AWS Data Engineer | Bank of Montreal | Toronto, ON, CAN | 0.4809 | 0.153 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, SQL |
| 318 | Software Engineer - Frontend/Full Stack | Sony Interactive Entertainment | Ireland, Dublin | 0.3649 | 0.153 | BACKEND_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Full Stack Development, Java, Spring Boot |
| 319 | Software Development Engineer in Test | Medtronic | London, London, United Kingdom | 0.3251 | 0.153 | SWE_FULLTIME | DevOps, Python, Java |
| 320 | Senior Linux Platform Development Engineer | Susquehanna International Group (SIG) | Senior Linux Platform Development Engineer in Dublin / Careers at SIG | 0.52 | 0.1509 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Python |
| 321 | Partner Operations Senior Engineer  | Sigma Computing | San Francisco, CA | 0.4897 | 0.1508 | DATA_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL, Python |
| 322 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.6624 | 0.1495 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | TypeScript, Python, Node.js |
| 323 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5111 | 0.1488 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Python, TypeScript |
| 324 | Lead Software Engineer | Appian | McLean, Virginia | 0.448 | 0.1488 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Java, TypeScript |
| 325 | Lead Software Engineer (Cloud) | Northwood Space | Torrance, CA | 0.6467 | 0.148 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 326 | Senior Cloud Solution Architect | Boeing | USA - Hazelwood, MO | 0.5577 | 0.148 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 327 | Senior Integration Developer | Monster Energy | USA - Corona, CA | 0.447 | 0.148 | BACKEND_ENGINEER_FULLTIME | DevOps |
| 328 | Software Engineer, Security | Notion | San Francisco, California | 0.7173 | 0.148 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Security Engineering |
| 329 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.4696 | 0.148 | SWE_FULLTIME | Cloud Infrastructure |
| 330 | Lead Network Engineer | Cadence Design Systems | SAN JOSE | 0.5153 | 0.146 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 331 | Senior Site Reliability Engineer II | LexisNexis Risk Solutions | Remote - USA - Nationwide | 0.4906 | 0.146 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 332 | Azure IaaS Engineer | CACI | Remote (Any State) | 0.4776 | 0.146 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 333 | Senior Momentum Technical Specialist | CACI | Remote (Any State) | 0.5056 | 0.146 | DEVOPS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 334 | Momentum Technical Specialist | CACI | Remote (Any State) | 0.4128 | 0.146 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 335 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.525 | 0.1445 | SWE_FULLTIME | Python, Java, SQL |
| 336 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1445 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 337 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 338 | Software Development Engineer | Micron Technology | Taoyuan - Fab 11, Taiwan | 0.5003 | 0.1445 | SWE_FULLTIME | Python, Java, SQL |
| 339 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 340 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 341 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 342 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 343 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4812 | 0.1445 | SWE_FULLTIME | Python, Java, SQL |
| 344 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 345 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 346 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4632 | 0.1445 | SWE_FULLTIME | Java, Python, SQL |
| 347 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4632 | 0.1445 | SWE_FULLTIME | Java, Python, JavaScript |
| 348 | Senior IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4632 | 0.143 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 349 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4628 | 0.143 | DEVOPS_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 350 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.143 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure |
| 351 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4327 | 0.1429 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 352 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4318 | 0.1429 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 353 | Software Engineering Architect | Salesforce | Norway - Remote | 0.5793 | 0.1409 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java |
| 354 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.4754 | 0.1409 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 355 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.406 | 0.1398 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python |
| 356 | Systems Engineer - US Remote | Motorola Solutions | Illinois Remote Work | 0.429 | 0.1363 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 357 | ENGINEER, FW & PRODUCT TEST ENGINEERING | Micron Technology | Arzano (NA), Italy | 0.3292 | 0.1363 | SWE_FULLTIME | C, Python |
| 358 | Firmware Engineer Data Center Solid State Drives | Micron Technology | Arzano (NA), Italy | 0.3054 | 0.1363 | SWE_FULLTIME | Python, C |
| 359 | Senior Sub-System Lead Engineer - High Voltage Battery Management | General Motors | Milford, Michigan, United States of America | 0.5798 | 0.135 | BACKEND_ENGINEER_FULLTIME | — |
| 360 | Engineer I/Engineer II/Sr. Engineer/Sr Engineer II | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4631 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 361 | Sales Engineer, Enterprise  Named | Fortinet | Atlanta, GA, United States | 0.4517 | 0.135 | SOLUTIONS_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 362 | Sr Engineer, Data Science | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.1346 | DATA_SCIENTIST_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Python, Angular |
| 363 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4327 | 0.1346 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 364 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4198 | 0.1346 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Java, Spring Boot |
| 365 | Senior Software Engineer | Podium | Lehi, Utah, Open to Remote | 0.5313 | 0.133 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 366 | Senior Full Stack Engineer | Podium | Lehi, Utah | 0.4679 | 0.133 | FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 367 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1313 | SWE_FULLTIME | Java, Python |
| 368 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5176 | 0.1313 | SWE_FULLTIME | Python, Java |
| 369 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5015 | 0.1313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, MongoDB |
| 370 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.5005 | 0.1313 | SWE_FULLTIME | Java, Python |
| 371 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4633 | 0.1313 | SWE_FULLTIME | Java, Python |
| 372 | SNOW Developer | Dexcom | Manila, Philippines | 0.463 | 0.1313 | BACKEND_ENGINEER_FULLTIME | JavaScript, SQL |
| 373 | Associate ATE Software Engineer | Boeing | IND - Bangalore, India | 0.4469 | 0.1313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, C |
| 374 | QE PCT Engineer | Micron Technology | Miaoli - Tongluo, Taiwan | 0.4235 | 0.1313 | SWE_FULLTIME | Python, SQL |
| 375 | Senior UI Software Engineer II | LexisNexis Risk Solutions | UK - London (London Wall) | 0.4874 | 0.1267 | FRONTEND_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Python |
| 376 | Experienced Software Engineer- FSD | Boeing | IND - Bangalore, India | 0.4198 | 0.1267 | FULLSTACK_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Java, Spring Boot |
| 377 | Senior Software Developer – DevOps | General Motors | Markham, Ontario, Canada | 0.5412 | 0.1239 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 378 | .NET/C# Engineer, TD Securities | TD Bank | Toronto, Ontario | 0.3795 | 0.1239 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, .NET |
| 379 | Senior Embedded Software Engineer | Micron Technology | San Jose, CA | 0.7214 | 0.1238 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, Python |
| 380 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6873 | 0.1238 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python |
| 381 | Senior Firmware Engineer | Motorola Solutions | Fresno, CA (CA180) | 0.4814 | 0.1238 | BACKEND_ENGINEER_FULLTIME | C, Python |
| 382 | Software Engineer - Compiler  | Sigma Computing | New York City, NY | 0.58 | 0.1238 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | TypeScript, Node.js |
| 383 | Software Engineer - Compiler  | Sigma Computing | San Francisco, CA | 0.5799 | 0.1238 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | TypeScript, SQL |
| 384 | Software Engineer II, Mission Interface | Torc Robotics | Ann Arbor, MI | 0.6096 | 0.1232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 385 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.5825 | 0.1232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 386 | Aeroderivative Performance Engineer - Field | GE Vernova | Greenville | 0.3469 | 0.1232 | SWE_FULLTIME | Python |
| 387 | Engineer Software T1/T2 | Northrop Grumman | GAWR03GC | 0.3461 | 0.1232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 388 | Software Engineer II | Cadence Design Systems | SAN JOSE | 0.4196 | 0.1232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 389 | Quality Assurance Engineer PON / DCOM | Ciena | Ottawa | 0.286 | 0.1232 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 390 | Architect - Personal Insurance Cross-Domain Architecture | Travelers | CT - Hartford | 0.5447 | 0.1218 | SWE_FULLTIME | Cloud Infrastructure, Python, Java |
| 391 | Software Engineer II-Team Lead (AWS, Typescript) | Travelers | CT - Hartford | 0.5281 | 0.1218 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, TypeScript, JavaScript |
| 392 | Quality Engineer Lead | LexisNexis Risk Solutions | Mumbai | 0.5798 | 0.1188 | SWE_FULLTIME | DevOps, TypeScript, JavaScript |
| 393 | Software Engineering MTS - Compliance Automation & Tooling (Apex, Python) | Salesforce | India - Hyderabad | 0.5792 | 0.1188 | SWE_FULLTIME | Security Engineering, Python, SQL |
| 394 | Experienced Software Application Development – QA and Test Automation Engineer | Boeing | IND - Bangalore, India | 0.5019 | 0.1188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, JavaScript |
| 395 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.4632 | 0.1188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, JavaScript, Express |
| 396 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.4631 | 0.1188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Python |
| 397 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4327 | 0.1188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, JavaScript, MongoDB |
| 398 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4323 | 0.1188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MongoDB |
| 399 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4316 | 0.1188 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Spring Boot |
| 400 | Senior Software Engineer II | LexisNexis Risk Solutions | Mumbai | 0.4195 | 0.1188 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, Spring Boot |
| 401 | Package Device Product Engineer (PDPE) Engineer | Micron Technology | Sanand - 303A - AT/SSD/MOD, India | 0.5796 | 0.1182 | SWE_FULLTIME | Python |
| 402 | Audio Programmer | Sony Interactive Entertainment | United Kingdom, London | 0.5209 | 0.1182 | SWE_FULLTIME | .NET |
| 403 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.1182 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 404 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4813 | 0.1182 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 405 | Experienced Java Software Engineer | Boeing | POL - Gdansk, Poland | 0.4632 | 0.1182 | BACKEND_ENGINEER_FULLTIME | Java |
| 406 | IT SOFTWARE ENGINEER | Micron Technology | Fab 10W, Singapore | 0.4194 | 0.1182 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 407 | Software Engineer I | American Express | BURGESS HILL, WEST SUSSEX, United Kingdom / 123 Buckingham Palace Road | 0.4086 | 0.1182 | BACKEND_ENGINEER_FULLTIME | Java |
| 408 | Senior SAP FIORI Developer | Monster Energy | USA - Corona, CA | 0.5994 | 0.1159 | BACKEND_ENGINEER_FULLTIME, FRONTEND_ENGINEER_FULLTIME | JavaScript |
| 409 | Product Architect | Monster Energy | USA - Corona, CA | 0.5401 | 0.1159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | JavaScript |
| 410 | Advanced Software Engr | Honeywell | Hamilton Township, NJ, United States | 0.462 | 0.1159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 411 | Senior Software Engineer - Backend | Sigma Computing | New York City, NY | 0.6041 | 0.1159 | BACKEND_ENGINEER_FULLTIME | Node.js |
| 412 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.4509 | 0.1159 | SWE_FULLTIME | Python |
| 413 | Engineering Technical Lead - I&C Embedded Software | GE Vernova | Wilmington NC USA | 0.3946 | 0.1159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 414 | Sr. Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.1159 | BACKEND_ENGINEER_FULLTIME | C |
| 415 | Sr. Software Engineer, High Performance Computing (Starlink)    | SpaceX | Redmond, WA | 0.5578 | 0.1159 | BACKEND_ENGINEER_FULLTIME | C |
| 416 | Sr. Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.1159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 417 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.5769 | 0.1159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 418 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.5758 | 0.1159 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 419 | Sr Full Stack Developer, TD Securities | TD Bank | Toronto, Ontario | 0.5025 | 0.1155 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, TypeScript, Node.js |
| 420 | Senior Software Engineer | Cadence Design Systems | SAN JOSE | 0.6448 | 0.1139 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, NLP |
| 421 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6359 | 0.1139 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, Python |
| 422 | Sr. QA Engineer - IP Routing | Ciena | Remote-Canada | 0.4707 | 0.1139 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python |
| 423 | Senior Software Engineer | EarnIn | Mexico City, Mexico | 0.643 | 0.1109 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python |
| 424 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.4587 | 0.1109 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, TypeScript |
| 425 | Senior Business Systems Analyst | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.6073 | 0.1088 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Python, SQL |
| 426 | Senior Software Engineer - C++/UI | General Motors | Mountain View, California, United States of America | 0.5715 | 0.108 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 427 | Sr. Batch Operations Technician - Run My Job and SAP BW (Remote) | RTX | US-TX-REMOTE | 0.5433 | 0.108 | BACKEND_ENGINEER_FULLTIME | — |
| 428 | Lead Software Engineer, Android (Kotlin & Jetpack Compose) | Capital One | McLean, VA | 0.5778 | 0.108 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 429 | Senior Technical Designer | Sony Interactive Entertainment | United States, Santa Monica, CA | 0.4603 | 0.108 | SWE_FULLTIME | — |
| 430 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in New York, New York / Careers at SIG | 0.72 | 0.108 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 431 | Senior OT Cybersecurity Engineer | GE Vernova | Findlay Township | 0.5628 | 0.106 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering |
| 432 | Lead Protection and Control Engineer | GE Vernova | Remote | 0.4757 | 0.106 | SWE_FULLTIME, SYSTEMS_ENGINEER_FULLTIME | Cloud Infrastructure |
| 433 | Firewall Engineering Architect | Leidos | Huntsville, AL | 0.3785 | 0.106 | BACKEND_ENGINEER_FULLTIME, SECURITY_ENGINEER_FULLTIME | Security Engineering |
| 434 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.105 | SWE_FULLTIME | — |
| 435 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.105 | SWE_FULLTIME | — |
| 436 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4755 | 0.105 | BACKEND_ENGINEER_FULLTIME | — |
| 437 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.105 | SWE_FULLTIME | — |
| 438 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4633 | 0.105 | SWE_FULLTIME | — |
| 439 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4197 | 0.105 | SWE_FULLTIME | — |
| 440 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4086 | 0.105 | SWE_FULLTIME | — |
| 441 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5744 | 0.103 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps |
| 442 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, Liverpool | 0.5759 | 0.103 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps |
| 443 | Sr Advanced Cyb Sec Archt/Engr | Honeywell | Rio de Janeiro, RJ, Brazil | 0.4813 | 0.103 | SECURITY_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Security Engineering |
| 444 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.103 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 445 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.5494 | 0.1025 | SWE_FULLTIME | Java, JavaScript, .NET |
| 446 | Senior Software Engineer | GE Vernova | Bucharest | 0.5514 | 0.1009 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 447 | Senior Software Cloud Engineer - PCS - IoT | Medtronic | Galway, County Galway, Ireland | 0.4422 | 0.0997 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, .NET, Java |
| 448 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4466 | 0.0976 | BACKEND_ENGINEER_FULLTIME | Java, Spring Boot, JavaScript |
| 449 | Software Engineering, SMTS (Salesforce Developer) | Salesforce | India - Hyderabad | 0.4755 | 0.0946 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, JavaScript, CSS |
| 450 | Senior Process Engineer (Oil and Gas, EPC, Midstream) | NOV | Dubai, Dubai, United Arab Emirates | 0.4463 | 0.093 | SWE_FULLTIME | — |
| 451 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 452 | Senior Software Developer – Virtualization, SIL, and AI‑Enablement | General Motors | Markham, Ontario, Canada | 0.5397 | 0.0918 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, Java |
| 453 | Senior Software Cloud Engineer - PCS - IoT | Medtronic | Galway, County Galway, Ireland | 0.4597 | 0.0918 | BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Java, SQL |
| 454 | Sr. Product Solution Analyst, TD Securities | TD Bank | Toronto, Ontario | 0.4116 | 0.0918 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Python, MongoDB |
| 455 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4278 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, JavaScript, SQL |
| 456 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.0867 | SWE_FULLTIME | Java, JavaScript, SQL |
| 457 | Lead Data Engineer | Capital One | Wilmington, DE | 0.7087 | 0.0818 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python |
| 458 | Senior Firmware Engineer | Ciena | New Providence - NJ | 0.5076 | 0.0818 | BACKEND_ENGINEER_FULLTIME | C, Python |
| 459 | Sr. Backend Engineer | dv01 | Remote - USA  | 0.6155 | 0.0818 | BACKEND_ENGINEER_FULLTIME | Spring Boot, SQL |
| 460 | C++ Software Engineer | Cadence Design Systems | SAN JOSE | 0.5967 | 0.0818 | BACKEND_ENGINEER_FULLTIME | C, Python |
| 461 | Software Developer (Mid Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.0818 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | C, Python |
| 462 | Software Engineer Developer ( Mid-Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.0818 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, Python |
| 463 | Senior SAP PI/PO Developer | CACI | Remote (Any State) | 0.4713 | 0.0818 | BACKEND_ENGINEER_FULLTIME | Java, SQL |
| 464 | Oracle EPM Integration Lead | CACI | Remote (Any State) | 0.4128 | 0.0818 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Python |
| 465 | Lead Engineer 1 - Customer Application Engineering | GE Vernova | Schenectady | 0.4052 | 0.0818 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | SQL, Python |
| 466 | Senior ABAP Developer | CACI | Remote (Any State) | 0.3919 | 0.0818 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL |
| 467 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.0788 | SWE_FULLTIME | Python, Java |
| 468 | Sr Embedded Software Engineer | Dexcom | San Diego, California | 0.5218 | 0.0739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 469 | Sr. Electricity Market Optimization Software Engineer | GE Vernova | Bellevue | 0.448 | 0.0739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 470 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.4039 | 0.0732 | BACKEND_ENGINEER_FULLTIME | Python |
| 471 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.4035 | 0.0732 | BACKEND_ENGINEER_FULLTIME | Python |
| 472 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.3895 | 0.0732 | BACKEND_ENGINEER_FULLTIME | Python |
| 473 | Senior Discipline Engineer | Valeo | Chennai | 0.5507 | 0.0709 | SWE_FULLTIME | Python |
| 474 | Senior Quality Engineer I | American Express | Chennai, TN, India | 0.502 | 0.0709 | BACKEND_ENGINEER_FULLTIME | Java |
| 475 | Senior Advanced Embedded Engineer | Honeywell | Givisiez, Sarine, Switzerland | 0.4874 | 0.0709 | BACKEND_ENGINEER_FULLTIME | C |
| 476 | Senior Software Engineer | LexisNexis Risk Solutions | Australia - (Sydney) | 0.4317 | 0.0709 | BACKEND_ENGINEER_FULLTIME | Python |
| 477 | Senior Software Engineer II | LexisNexis Risk Solutions | Australia - (Sydney) | 0.4079 | 0.0709 | BACKEND_ENGINEER_FULLTIME | Python |
| 478 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.4294 | 0.0676 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, JavaScript, Python |
| 479 | SAP IBP Analyst | iHerb | United States of America - Remote / Home Office | 0.5662 | 0.066 | BACKEND_ENGINEER_FULLTIME | — |
| 480 | Lead AC Control Automation Engineer | GE Vernova | Noida | 0.5513 | 0.063 | BACKEND_ENGINEER_FULLTIME | — |
| 481 | Senior Discipline Engineer - Software Requirements | Valeo | Chennai | 0.5507 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 482 | Simulation Software Engineer (Experienced or Senior level) | Boeing | GBR - Crawley, UK | 0.5019 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 483 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 484 | Sr IT Analyst | Honeywell | Bengaluru, Karnataka, India | 0.4619 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 485 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4327 | 0.063 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 486 | ML Engineer, II - App Engine | Torc Robotics | Ann Arbor, MI, Montreal, Canada | 0.4928 | 0.06 | SWE_FULLTIME | — |
| 487 | IT Developer (Java), TD Securities | TD Bank | Toronto, Ontario | 0.3363 | 0.0597 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Spring Boot, MongoDB |
| 488 | Senior Workday Platform Engineer - Absence (Workday) | Sony Interactive Entertainment | Ireland, Dublin | 0.4838 | 0.036 | BACKEND_ENGINEER_FULLTIME | — |

## Ishan Bhutada (`user2@example.com`)

**Candidate ID:** `3df95ff2-9785-43fc-89a7-c9ec92415eb3`

### Subscribed pools
- `DATA_ANALYST_FULLTIME`
- `DATA_SCIENTIST_FULLTIME`
- `SWE_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Data Engineering, Machine Learning, Analytics Engineering |
| Preferred locations | United States |
| Primary roles | Data Analyst, Data Scientist |
| Hard constraints | sponsorship=True, min_salary=None, target_seniority=INTERN, NEW_GRAD, ENTRY, MID, JUNIOR |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 131
- **Notification-eligible jobs (≤60d, not yet emailed):** 131
- **Personal score range:** 0.06 – 0.58 (29 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `DATA_ANALYST_FULLTIME` | 116 |
| `DATA_SCIENTIST_FULLTIME` | 15 |
| `DATA_ENGINEER_FULLTIME` | 7 |
| `ML_ENGINEER_FULLTIME` | 3 |
| `SWE_FULLTIME` | 2 |
| `OPERATIONS_FULLTIME` | 2 |
| `FRONTEND_ENGINEER_FULLTIME` | 1 |
| `FINANCE_FULLTIME` | 1 |
| `FULLSTACK_ENGINEER_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Data Scientist, Finance @ Figma

- **Location:** San Francisco, CA • New York, NY • United States (unclear)
- **Posted:** 2026-06-12T19:20:07+00:00
- **Salary:** 140000 – 348000
- **Effort:** MEDIUM
- **Opportunity score:** 0.7884
- **Personal score:** 0.58
- **Pools:** `DATA_SCIENTIST_FULLTIME`, `DATA_ENGINEER_FULLTIME`
- **Roles:** DATA_SCIENTIST, DATA_ENGINEER
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering
- **Skills:** financial modeling, data architecture, forecasting, statistical analysis
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering
- **URL:** https://boards.greenhouse.io/figma/jobs/6013304004?gh_jid=6013304004

#### #2 — Postgraduate Associate for Academic Integrity @ University of Texas at Austin

- **Location:** UT MAIN CAMPUS (unclear)
- **Posted:** 2026-06-12T00:00:00+00:00
- **Salary:** 60000 – —
- **Effort:** HIGH
- **Opportunity score:** 0.3074
- **Personal score:** 0.4217
- **Pools:** `DATA_SCIENTIST_FULLTIME`
- **Roles:** DATA_SCIENTIST
- **Capabilities:** Machine Learning, Data Engineering
- **Skills:** anomaly detection, statistical modeling, data mining
- **Match reasons:** Machine Learning, Data Engineering
- **URL:** https://utaustin.wd1.myworkdayjobs.com/UTstaff/job/UT-MAIN-CAMPUS/Postgraduate-Associate-for-Academic-Integrity_R_00046165

#### #3 — Data Scientist @ Micron Technology

- **Location:** Boise, ID - Main Site (unclear)
- **Posted:** 2026-06-08T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.4194
- **Personal score:** 0.4217
- **Pools:** `DATA_SCIENTIST_FULLTIME`
- **Roles:** DATA_SCIENTIST
- **Capabilities:** Machine Learning, Analytics Engineering
- **Skills:** time series forecasting, statistical modeling
- **Match reasons:** Machine Learning, Analytics Engineering
- **URL:** https://micron.wd1.myworkdayjobs.com/External/job/Boise-ID---Main-Site/Data-Scientist_JR103250

#### #4 — Analyst-Data Science @ American Express

- **Location:** Gurugram, HR, India (unclear)
- **Posted:** 2026-06-12T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5496
- **Personal score:** 0.3717
- **Pools:** `DATA_ANALYST_FULLTIME`
- **Roles:** DATA_ANALYST
- **Capabilities:** Machine Learning, Analytics Engineering
- **Skills:** model validation, risk assessment
- **Match reasons:** Machine Learning, Analytics Engineering
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26008698/details

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Data Scientist, Finance | Figma | San Francisco, CA • New York, NY • United States | 0.7884 | 0.58 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 2 | Postgraduate Associate for Academic Integrity | University of Texas at Austin | UT MAIN CAMPUS | 0.3074 | 0.4217 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering |
| 3 | Data Scientist | Micron Technology | Boise, ID - Main Site | 0.4194 | 0.4217 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering |
| 4 | Analyst-Data Science | American Express | Gurugram, HR, India | 0.5496 | 0.3717 | DATA_ANALYST_FULLTIME | Machine Learning, Analytics Engineering |
| 5 | Analyst-Data Science (SQL, Python, GenAI) | American Express | Gurugram, HR, India | 0.5496 | 0.3717 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering |
| 6 | Analyst-Risk Management | American Express | Gurugram, HR, India | 0.5493 | 0.3717 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering |
| 7 | DATA SCIENTIST, SMAI | Micron Technology | MSB, Singapore | 0.5005 | 0.3717 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering |
| 8 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.4813 | 0.3717 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering |
| 9 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4469 | 0.3717 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering |
| 10 | Global Facilities Engineer | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4463 | 0.3717 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering |
| 11 | DATA SCIENTIST | Micron Technology | Fab 10A, Singapore | 0.3982 | 0.3717 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering |
| 12 | Data Analytics Associate (Marketing Science) | LG Ad Solutions | New York, NY | 0.6703 | 0.3583 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 13 | Performance Engineer II | Berkshire Hathaway Energy | Calipatria, CA, United States | 0.5015 | 0.3583 | DATA_ANALYST_FULLTIME, SWE_FULLTIME | Analytics Engineering |
| 14 | Risk Analyst - Portfolio Analytics | GM Financial | Fort Worth, TX, United States | 0.4086 | 0.3583 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 15 | Sales Systems Analyst - Temp | Monster Energy | USA - Corona, CA | 0.4079 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 16 | Inventory Buy Signal Analyst (Associate, Experienced, and Subject Matter Expert) | Boeing | USA - Dallas, TX | 0.4731 | 0.3133 | DATA_ANALYST_FULLTIME, OPERATIONS_FULLTIME | Analytics Engineering |
| 17 | Advanced Analytics Analyst | Medtronic | Minneapolis, Minnesota, United States of America | 0.4558 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 18 | Advanced Analytics Analyst | Medtronic | Minneapolis, Minnesota, United States of America | 0.4543 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 19 | Business Analyst | Boeing | USA - Everett, WA | 0.4283 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 20 | Aviation Training Analyst | CACI | Pensacola, FL, US | 0.3611 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 21 | Equity Research Associate - Clean Energy | TD Bank | New York, New York | 0.4857 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 22 | Decision Support Analyst II | LexisNexis Risk Solutions | Alpharetta, GA | 0.3857 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 23 | Materials Management Analyst (Associate or Experienced) | Boeing | USA - Seattle, WA | 0.361 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 24 | Advanced Business Systems Specialist | General Dynamics Mission Systems | US-AZ-Scottsdale | 0.3631 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering, agile |
| 25 | Operations Analyst – Service Management Operations | RTX | US-NY-REMOTE | 0.3017 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 26 | Sell Side Research Associate, Travel and Leisure | Susquehanna International Group (SIG) | Sell Side Research Associate, Travel and Leisure in New York, New York / Careers at SIG | 0.4724 | 0.3133 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 27 | Senior Financial Analyst | American Express | New York, NY, United States | 0.4198 | 0.295 | DATA_ANALYST_FULLTIME | Machine Learning, Analytics Engineering |
| 28 | Operations Analyst | Manulife Financial | Quezon City | 0.5492 | 0.2883 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 29 | Workforce Insights Consultant | Ciena | Belfast | 0.5246 | 0.2883 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 30 | Energy Markets Analyst (NYISO) | Voltus | Remote | 0.4378 | 0.2883 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 31 | Sales Business Planning Analyst | Micron Technology | Boise, ID - Main Site | 0.4195 | 0.2883 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 32 | Quality Data Analytics Engineer | GE Vernova | Vadodara | 0.4079 | 0.2883 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 33 | Data Scientist, Marketing | Figma | San Francisco, CA • New York, NY • United States | 0.7654 | 0.268 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering |
| 34 | Clinical Analytics Specialist – MD | RELX | Texas | 0.5053 | 0.2433 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 35 | Process & Data Integration Specialist H/F | GE Vernova | Greenville | 0.4816 | 0.2433 | DATA_ANALYST_FULLTIME | Data Engineering |
| 36 | Associate-Digital Product Management | American Express | Gurugram, HR, India | 0.5514 | 0.2383 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 37 | Analyst-Risk Management | American Express | Singapore | 0.5513 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 38 | Analyst, Competitive Intelligence - Bangalore | Danaher Corporation | Bangalore, Karnataka, India | 0.5495 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 39 | ビジネスアナリスト | Manulife Financial | Tokyo | 0.5492 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 40 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.5492 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 41 | Financial Svcs Analyst | Honeywell | Bengaluru, Karnataka, India | 0.5014 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 42 | CX OM BUSINESS SYSTEMS ANALYST | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 43 | Data Analyst | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4315 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 44 | Business Analyst | American Express | Gurugram, HR, India | 0.4162 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 45 | Analyst-Risk Management | American Express | Gurugram, HR, India | 0.4086 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 46 | Analyst-Business Development | American Express | Gurugram, HR, India | 0.4086 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 47 | Analyst - Operational Risk Management | American Express | Taguig City, Manila, Philippines | 0.4086 | 0.2383 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 48 | DATA SCIENTIST | Micron Technology | Fab 10A, Singapore | 0.4079 | 0.2383 | DATA_SCIENTIST_FULLTIME | Machine Learning |
| 49 | Senior BI Engineer, CRM | General Motors | Remote - United States | 0.5429 | 0.226 | DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering |
| 50 | Senior Data Analyst/Developer | CACI | Remote (Any State) | 0.437 | 0.226 | DATA_ANALYST_FULLTIME, SWE_FULLTIME | Data Engineering, Analytics Engineering |
| 51 | Analyst-Risk Management | American Express | Phoenix, AZ, United States | 0.5019 | 0.225 | DATA_ANALYST_FULLTIME | — |
| 52 | Analyst-Risk Management | American Express | New York, NY, United States | 0.5019 | 0.225 | DATA_ANALYST_FULLTIME | — |
| 53 | Analyst-Compliance Global Sanctions Governance | American Express | Phoenix, AZ, United States / Charlotte Hybrid-600 Tryon / Sunrise Campus / Towne Ridge Center III | 0.4423 | 0.225 | DATA_ANALYST_FULLTIME | — |
| 54 | Analyst of Issues, Events & Remediation | American Express | New York, NY, United States | 0.4162 | 0.225 | DATA_ANALYST_FULLTIME | — |
| 55 | Senior Analytics Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5553 | 0.223 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering |
| 56 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5243 | 0.223 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering |
| 57 | Advanced Data Scientist | Honeywell | Hyderabad, Telangana, India | 0.5004 | 0.223 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering |
| 58 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.4813 | 0.223 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering |
| 59 | Sr Engineer, Data Science | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.223 | DATA_SCIENTIST_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Data Engineering |
| 60 | Sr. Process Transformation Business Intelligence Data Analyst | General Motors | Warren, Michigan, United States of America | 0.5798 | 0.215 | DATA_ANALYST_FULLTIME | Data Engineering, ETL |
| 61 | Procurement Business Solutions Senior Analyst | Truist Bank | Atlanta, GA | 0.549 | 0.215 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 62 | Senior Auditor | American Express | New York, NY, United States / AEDR Desert Ridge CSB - Sierra / AEDR Desert Ridge OB1-Camelback / AEDR Desert Ridge OB2-McDowell / AEDR Desert Ridge OB4 - Canyon / Towne Ridge Center III / Charlotte Hybrid-600 Tryon | 0.4813 | 0.215 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 63 | Senior Business Analyst (Platform) | Whoop | Boston, MA | 0.4478 | 0.215 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 64 | GMF Sr Credit Analyst I | GM Financial | Raleigh, NC, United States | 0.4469 | 0.215 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 65 | Senior Strategy & Analytics Analyst | VITAS Healthcare | Miami, FL, United States | 0.4015 | 0.215 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 66 | FinOps Technical Analyst | Bank of Montreal | Toronto, ON, CAN | 0.3494 | 0.1933 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 67 | Lead Data Analyst - Product Growth | Constant Contact | Waltham or Boston, MA | 0.5579 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 68 | Senior Revenue Analyst, Customer Success | Constant Contact | Waltham or Boston, MA | 0.4871 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 69 | Senior Business Planning Analyst | Micron Technology | San Jose, CA | 0.6972 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 70 | Analyst/Senior Analyst, Product Growth & GTM Strategy | Salesforce | California - San Francisco | 0.5721 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 71 | Senior Analyst, Strategy & Data | Salesforce | California - San Francisco | 0.5534 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 72 | Senior Data Analyst | Capital One | McLean, VA | 0.4906 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 73 | Senior Associate; Brand Creative Researcher | Capital One | Richmond, VA | 0.4728 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 74 | People Analytics Lead - Recruiting | Notion | San Francisco, California / New York, New York | 0.6795 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 75 | Facilities Analyst (Senior or Lead) | Boeing | USA - Mesa, AZ | 0.5384 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 76 | Senior Financial Analyst | Boeing | USA - San Antonio, TX | 0.4828 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 77 | Senior Data Analyst-Tech Analytics | Capital One | McLean, VA | 0.4429 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 78 | Decision Support Sr Finance Analyst | LexisNexis Risk Solutions | Alpharetta, GA | 0.4062 | 0.188 | DATA_ANALYST_FULLTIME, FINANCE_FULLTIME | Analytics Engineering |
| 79 | Senior Category Analyst | Monster Energy | USA - Corona, CA | 0.3902 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 80 | Senior Analyst, Strategic Operations & Insights | Salesforce | New York - New York | 0.4555 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 81 | Senior Associate, Capital Markets and Risk (Stress Test Forecasting Team) (Hybrid) | Capital One | McLean, VA | 0.403 | 0.188 | DATA_ANALYST_FULLTIME | Data Engineering |
| 82 | Senior Financial Analyst - Cox Fleet, Sales | Cox | Atlanta GA | 0.3805 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 83 | Data Engineer, AI/ML III/IV | Zone 5 Technologies | United States | 0.4732 | 0.188 | DATA_ANALYST_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Analytics Engineering |
| 84 | Senior Business Intelligence Analyst | Boeing | USA - Everett, WA | 0.4456 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 85 | Sr. Business Analyst, Commercial Treasury Management Product Analytics | Capital One | New York, NY | 0.4081 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 86 | Sr. Fraud Data Analyst (Remote USA) | LexisNexis Risk Solutions | Alpharetta, GA | 0.3556 | 0.188 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 87 | Logistics TMS Analyst | Monster Energy | USA - Corona, CA; USA - Rogers, AR | 0.4079 | 0.18 | DATA_ANALYST_FULLTIME | — |
| 88 | Pricing Representative Temp to Hire | Monster Energy | USA - Corona, CA | 0.4078 | 0.18 | DATA_ANALYST_FULLTIME | — |
| 89 | Training Analyst | Boeing | USA - Huntsville, AL | 0.4459 | 0.18 | DATA_ANALYST_FULLTIME | — |
| 90 | Lead Demand Planner | GlobalFoundries | USA - Texas - Austin | 0.4164 | 0.18 | DATA_ANALYST_FULLTIME | — |
| 91 | Analyst, Enterprise Agentic Search | American Express | New York, NY, United States | 0.3 | 0.18 | DATA_ANALYST_FULLTIME | — |
| 92 | Analyst - Enterprise Agentic Search Content | American Express | New York, NY, United States | 0.3 | 0.18 | DATA_ANALYST_FULLTIME | — |
| 93 | Senior Business Intelligence Analyst- SMAI | Micron Technology | Boise, ID - ID1 | 0.5243 | 0.173 | DATA_ANALYST_FULLTIME | Machine Learning |
| 94 | Senior Product Data Scientist | MaintainX | Montreal, Toronto, Vancouver, SF (Remote) | 0.457 | 0.173 | DATA_SCIENTIST_FULLTIME | Machine Learning |
| 95 | Senior Analyst - IT-applications - Oracle EBS | Ciena | Remote- India- Gurugram | 0.4079 | 0.173 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 96 | Senior Data Analyst | University of Arkansas | Little Rock | 0.3278 | 0.173 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 97 | Revenue Operations Business Analyst – Strategic Revenue Intelligence | Micron Technology | Boise, ID - Main Site | 0.5016 | 0.155 | DATA_ANALYST_FULLTIME | — |
| 98 | Business Analyst - Oracle EBS Budget to Report (B2R) | CACI | Remote (Any State) | 0.4706 | 0.146 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 99 | Sr Project Management Analyst | Motorola Solutions | Washington DC Remote Work | 0.4624 | 0.146 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 100 | Senior BI Analyst | Torc Robotics | Ann Arbor, MI, Remote - US | 0.427 | 0.146 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 101 | Senior Analyst - Workday Testing | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.5812 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 102 | Senior Financial Analyst | American Express | Toronto, ON, Canada | 0.5513 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 103 | Experienced Global Security Intelligence Analyst | Boeing | IND - Bangalore, India | 0.5512 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 104 | Senior Analyst - Control Management | American Express | Gurugram, HR, India | 0.549 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 105 | Financial Svcs Analyst | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 106 | Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5014 | 0.143 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning |
| 107 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.143 | DATA_SCIENTIST_FULLTIME | Machine Learning |
| 108 | Senior Analyst - Sales Strategy & Operations | Salesforce | United Kingdom - London | 0.4813 | 0.143 | DATA_ANALYST_FULLTIME, OPERATIONS_FULLTIME | Analytics Engineering |
| 109 | Senior Engineer, Assembly & Test Central QA | Micron Technology | Fab 10A, Singapore | 0.4806 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 110 | Senior AI Solutions Analyst | Micron Technology | Jalisco, Mexico | 0.4464 | 0.143 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 111 | Sr Financial Analyst | American Express | New York, NY, United States | 0.5513 | 0.135 | DATA_ANALYST_FULLTIME | — |
| 112 | Senior Analyst - Paid Search Banking & Non-Card | American Express | New York, NY, United States | 0.502 | 0.135 | DATA_ANALYST_FULLTIME | — |
| 113 | Associate LNG Commercial Analyst/LNG Commercial Analyst/Sr LNG Commercial Analyst | Berkshire Hathaway Energy | Glen Allen, VA, United States | 0.4619 | 0.135 | DATA_ANALYST_FULLTIME | — |
| 114 | Lead Data Analyst - Product Growth | Constant Contact | Toronto, Ontario, Canada | 0.618 | 0.116 | DATA_ANALYST_FULLTIME | Analytics Engineering, A/B testing |
| 115 | Competition Analyst | Manulife Financial | USA, Massachusetts - Full Time Remote | 0.4899 | 0.11 | DATA_ANALYST_FULLTIME | — |
| 116 | Quality Assurance Analyst I, Manheim Mobile Inspections | Cox | Remote - Michigan | 0.4206 | 0.11 | DATA_ANALYST_FULLTIME | — |
| 117 | Construction Surety Underwriter / Financial Analyst (Associate Account Executive) | Travelers | UT - Salt Lake City | 0.3532 | 0.11 | DATA_ANALYST_FULLTIME | — |
| 118 | SAP Business Analyst | CACI | Remote (Any State) | 0.3387 | 0.11 | DATA_ANALYST_FULLTIME | — |
| 119 | SAP Business Analyst | CACI | Remote (Any State) | 0.3273 | 0.11 | DATA_ANALYST_FULLTIME | — |
| 120 | Senior Financial Analyst - Coronary Sales Finance | Medtronic | Minneapolis, Minnesota, United States of America | 0.4844 | 0.108 | DATA_ANALYST_FULLTIME | — |
| 121 | Senior Product Analyst-Agile | Truist Bank | Richmond, VA | 0.4158 | 0.108 | DATA_ANALYST_FULLTIME | — |
| 122 | Senior Business Analyst | Boeing | USA - Seattle, WA | 0.4797 | 0.108 | DATA_ANALYST_FULLTIME | — |
| 123 | Sr. Business Analyst | Capital One | McLean, VA | 0.4427 | 0.108 | DATA_ANALYST_FULLTIME | — |
| 124 | GMF Sr Credit Analyst I - Zone C | GM Financial | Seattle, WA, United States | 0.3928 | 0.108 | DATA_ANALYST_FULLTIME | — |
| 125 | RDA Process Owner｜データ分析で歩留まり・品質を改善（広島） | Micron Technology | Hiroshima - Fab 15, Japan | 0.4806 | 0.105 | DATA_ANALYST_FULLTIME | — |
| 126 | Lead Analyst | American Express | Gurugram, HR, India | 0.4086 | 0.105 | DATA_ANALYST_FULLTIME | — |
| 127 | Global Master Data Sr. Analyst H/F | GE Vernova | Greenville | 0.4432 | 0.066 | DATA_ANALYST_FULLTIME | — |
| 128 | Systems Integration Specialist (Experienced/Senior) | Boeing | POL - Swidnik, Poland | 0.4327 | 0.063 | DATA_ANALYST_FULLTIME | — |
| 129 | Sr Business Analyst - Informatica MDM | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4078 | 0.063 | DATA_ANALYST_FULLTIME | — |
| 130 | Jr. Investment Analyst | Manulife Financial | Toronto, Ontario | 0.4345 | 0.06 | DATA_ANALYST_FULLTIME | — |
| 131 | Field Supervision Analyst | Manulife Financial | Toronto, Ontario | 0.4115 | 0.06 | DATA_ANALYST_FULLTIME | — |

## Soham Navandar (`user3@example.com`)

**Candidate ID:** `c661dc97-5b60-4987-8b52-1507d6562b76`

### Subscribed pools
- `DATA_SCIENTIST_FULLTIME`
- `SWE_FULLTIME`
- `DATA_ANALYST_FULLTIME`
- `SOLUTIONS_CONSULTANT_FULLTIME`

### Profile snapshot

| Field | Value |
|-------|-------|
| Capabilities | Data Engineering, Machine Learning, AI Systems, Analytics Engineering, DevOps |
| Preferred locations | United States, New York |
| Primary roles | Data Scientist, Data Analyst, Solutions Consultant |
| Hard constraints | sponsorship=True, min_salary=None, target_seniority=INTERN, NEW_GRAD, ENTRY, MID, JUNIOR |

### Match summary

- **Total jobs matching subscribed pools (after filters):** 418
- **Notification-eligible jobs (≤60d, not yet emailed):** 418
- **Personal score range:** 0.018 – 0.495 (92 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 284 |
| `BACKEND_ENGINEER_FULLTIME` | 176 |
| `DATA_ANALYST_FULLTIME` | 118 |
| `FULLSTACK_ENGINEER_FULLTIME` | 63 |
| `ML_ENGINEER_FULLTIME` | 28 |
| `FRONTEND_ENGINEER_FULLTIME` | 23 |
| `DATA_SCIENTIST_FULLTIME` | 19 |
| `DATA_ENGINEER_FULLTIME` | 19 |
| `DEVOPS_ENGINEER_FULLTIME` | 14 |
| `SECURITY_ENGINEER_FULLTIME` | 4 |
| `MOBILE_ENGINEER_FULLTIME` | 3 |
| `SUPPORT_ENGINEER_FULLTIME` | 3 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 3 |
| `OPERATIONS_FULLTIME` | 2 |
| `SYSTEMS_ENGINEER_FULLTIME` | 1 |
| `MARKETING_FULLTIME` | 1 |
| `RESEARCH_SCIENTIST_FULLTIME` | 1 |
| `FINANCE_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — Data Scientist, Finance @ Figma

- **Location:** San Francisco, CA • New York, NY • United States (unclear)
- **Posted:** 2026-06-12T19:20:07+00:00
- **Salary:** 140000 – 348000
- **Effort:** MEDIUM
- **Opportunity score:** 0.7884
- **Personal score:** 0.495
- **Pools:** `DATA_SCIENTIST_FULLTIME`, `DATA_ENGINEER_FULLTIME`
- **Roles:** DATA_SCIENTIST, DATA_ENGINEER
- **Capabilities:** Machine Learning, Data Engineering, Analytics Engineering
- **Skills:** financial modeling, data architecture, forecasting, statistical analysis
- **Match reasons:** Machine Learning, Data Engineering, Analytics Engineering, SQL, Python
- **URL:** https://boards.greenhouse.io/figma/jobs/6013304004?gh_jid=6013304004

#### #2 — AI Engineer III @ American Express

- **Location:** Phoenix, AZ, United States | New York-Amex Tower WFC-35 Hr (unclear)
- **Posted:** 2026-06-10T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.4632
- **Personal score:** 0.4475
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`, `ML_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER, ML_ENGINEER
- **Capabilities:** Backend Engineering, AI Systems, Machine Learning
- **Skills:** LLMs, agentic AI, RAG, distributed systems
- **Match reasons:** AI Systems, Machine Learning, Python
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26009446/details

#### #3 — Data Analytics Associate (Marketing Science) @ LG Ad Solutions

- **Location:** New York, NY (unclear)
- **Posted:** 2026-06-12T04:00:00+00:00
- **Salary:** — – —
- **Effort:** LOW
- **Opportunity score:** 0.6703
- **Personal score:** 0.38
- **Pools:** `DATA_ANALYST_FULLTIME`
- **Roles:** DATA_ANALYST
- **Capabilities:** Analytics Engineering
- **Skills:** data quality, workflow automation
- **Match reasons:** Analytics Engineering, SQL, Python
- **URL:** https://jobs.ashbyhq.com/lgads/c049db92-3ae6-4022-84fa-821e4fed3253

#### #4 — Performance Engineer II @ Berkshire Hathaway Energy

- **Location:** Calipatria, CA, United States (unclear)
- **Posted:** 2026-06-11T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5015
- **Personal score:** 0.38
- **Pools:** `DATA_ANALYST_FULLTIME`, `SWE_FULLTIME`
- **Roles:** DATA_ANALYST, SWE
- **Capabilities:** Analytics Engineering
- **Skills:** data analysis, performance modeling
- **Match reasons:** Analytics Engineering, SQL, Python
- **URL:** https://fa-essf-saasfaprod1.fa.ocs.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/10005208/details

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | Data Scientist, Finance | Figma | San Francisco, CA • New York, NY • United States | 0.7884 | 0.495 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Analytics Engineering |
| 2 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.4475 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 3 | Data Analytics Associate (Marketing Science) | LG Ad Solutions | New York, NY | 0.6703 | 0.38 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 4 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.549 | 0.38 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, SQL |
| 5 | Performance Engineer II | Berkshire Hathaway Energy | Calipatria, CA, United States | 0.5015 | 0.38 | DATA_ANALYST_FULLTIME, SWE_FULLTIME | Analytics Engineering, SQL, Python |
| 6 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.5272 | 0.3675 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 7 | Software Development Engineer I - General Motors Insurance | GM Financial | United States | 0.5005 | 0.3675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java |
| 8 | Risk Analyst - Portfolio Analytics | GM Financial | Fort Worth, TX, United States | 0.4086 | 0.3675 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 9 | Software Engineer - Defense Applications | Palantir | New York, NY | 0.5474 | 0.355 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, API integration |
| 10 | Software Engineer | Intel | US, Arizona, Phoenix | 0.6671 | 0.3475 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Java, C++ |
| 11 | Software Engineer for Data at Rest (DAR) Crypto & Cross Domain Solutions | General Dynamics Mission Systems | US-MA-Dedham | 0.4222 | 0.3475 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, C |
| 12 | Software Engineer | Aquatic Capital Management | New York | 0.608 | 0.3475 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, C++ |
| 13 | DATA SCIENTIST, SMAI | Micron Technology | MSB, Singapore | 0.5005 | 0.34 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, AI Systems, Data Engineering |
| 14 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.335 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | DevOps, Java, Python |
| 15 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.335 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | DevOps, Java, Python |
| 16 | Advanced Analytics Analyst | Medtronic | Minneapolis, Minnesota, United States of America | 0.4558 | 0.335 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 17 | Advanced Analytics Analyst | Medtronic | Minneapolis, Minnesota, United States of America | 0.4543 | 0.335 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 18 | Information & Application Developer (Entry Level and Associate) | Boeing | USA - North Charleston, SC | 0.4034 | 0.335 | SWE_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Python, SQL |
| 19 | Software Development Engineer in Test | Medtronic | London, London, United Kingdom | 0.3251 | 0.335 | SWE_FULLTIME | DevOps, Python, Java |
| 20 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.6624 | 0.3225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 21 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, Aliso Viejo, CA | 0.5298 | 0.3225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, CI/CD |
| 22 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, San Diego, CA | 0.5283 | 0.3225 | SWE_FULLTIME | DevOps, Python, CI/CD |
| 23 | Embedded Software Engineer - Electrification | General Motors | Milford, Michigan, United States of America | 0.5495 | 0.3125 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++, Python |
| 24 | Sales Systems Analyst - Temp | Monster Energy | USA - Corona, CA | 0.4079 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 25 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5114 | 0.31 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps |
| 26 | Inventory Buy Signal Analyst (Associate, Experienced, and Subject Matter Expert) | Boeing | USA - Dallas, TX | 0.4731 | 0.31 | DATA_ANALYST_FULLTIME, OPERATIONS_FULLTIME | Analytics Engineering |
| 27 | Business Analyst | Boeing | USA - Everett, WA | 0.4283 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 28 | DevSecOps Software Engineer (Associate or Experienced), Phantom Works | Boeing | USA - Saint Charles, MO | 0.3778 | 0.31 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, CI/CD |
| 29 | Aviation Training Analyst | CACI | Pensacola, FL, US | 0.3611 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 30 | Equity Research Associate - Clean Energy | TD Bank | New York, New York | 0.4857 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 31 | Materials Management Analyst (Associate or Experienced) | Boeing | USA - Seattle, WA | 0.361 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 32 | Advanced Business Systems Specialist | General Dynamics Mission Systems | US-AZ-Scottsdale | 0.3631 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 33 | Operations Analyst – Service Management Operations | RTX | US-NY-REMOTE | 0.3017 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 34 | Sell Side Research Associate, Travel and Leisure | Susquehanna International Group (SIG) | Sell Side Research Associate, Travel and Leisure in New York, New York / Careers at SIG | 0.4724 | 0.31 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 35 | Analyst-Risk Management | American Express | New York, NY, United States | 0.5019 | 0.3 | DATA_ANALYST_FULLTIME | Python, SQL |
| 36 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4755 | 0.3 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL |
| 37 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.4115 | 0.3 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 38 | Senior Analytics Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5553 | 0.291 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 39 | Audio Programmer | Sony Interactive Entertainment | United Kingdom, London | 0.5209 | 0.2875 | SWE_FULLTIME | C++ |
| 40 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3632 | 0.28 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, C++ |
| 41 | Senior Financial Analyst | American Express | New York, NY, United States | 0.4198 | 0.276 | DATA_ANALYST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 42 | Software Engineer - Core Interfaces | Palantir | New York, NY | 0.5451 | 0.275 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 43 | Analyst-Risk Management | American Express | Phoenix, AZ, United States | 0.5019 | 0.275 | DATA_ANALYST_FULLTIME | — |
| 44 | Software Engineer 2 | Berkshire Hathaway Energy | Des Moines, IA, United States | 0.4628 | 0.275 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 45 | Analyst-Compliance Global Sanctions Governance | American Express | Phoenix, AZ, United States / Charlotte Hybrid-600 Tryon / Sunrise Campus / Towne Ridge Center III | 0.4423 | 0.275 | DATA_ANALYST_FULLTIME | — |
| 46 | Analyst of Issues, Events & Remediation | American Express | New York, NY, United States | 0.4162 | 0.275 | DATA_ANALYST_FULLTIME | — |
| 47 | Analyst-Data Science | American Express | Gurugram, HR, India | 0.5496 | 0.2725 | DATA_ANALYST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 48 | Software Engineer II | American Express | Gurugram, HR, India | 0.4632 | 0.2725 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 49 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.4469 | 0.2725 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 50 | Data Scientist | Micron Technology | Fab 10A, Singapore | 0.4203 | 0.2725 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 51 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.6813 | 0.2715 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 52 | Senior Lead AI Engineer, Gen AI Platform | Capital One | New York, NY | 0.6809 | 0.2715 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 53 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2715 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Python |
| 54 | Lead AI Engineer (MLX) | Capital One | New York, NY | 0.5535 | 0.2715 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 55 | Software Engineer, Agents  | Mirage | Union Square, New York City | 0.5078 | 0.2685 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 56 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.2685 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 57 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 58 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 59 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3242 | 0.2675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, C++ |
| 60 | Analyst-Data Science (SQL, Python, GenAI) | American Express | Gurugram, HR, India | 0.5496 | 0.26 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 61 | Analyst-Risk Management | American Express | Gurugram, HR, India | 0.5493 | 0.26 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 62 | Postgraduate Associate for Academic Integrity | University of Texas at Austin | UT MAIN CAMPUS | 0.3074 | 0.26 | DATA_SCIENTIST_FULLTIME | Machine Learning, Data Engineering, Python |
| 63 | Global Facilities Engineer | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4463 | 0.26 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, Python |
| 64 | Data Scientist | Micron Technology | Boise, ID - Main Site | 0.4194 | 0.26 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 65 | DATA SCIENTIST | Micron Technology | Fab 10A, Singapore | 0.3982 | 0.26 | DATA_SCIENTIST_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 66 | Data Scientist, Marketing | Figma | San Francisco, CA • New York, NY • United States | 0.7654 | 0.2565 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, SQL |
| 67 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.255 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Java, Python |
| 68 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5344 | 0.255 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL, Python |
| 69 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.255 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python |
| 70 | Software Engineer (Front End) | CACI | Aurora, CO, US | 0.3868 | 0.255 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Python, DynamoDB, API integration |
| 71 | Software Engineer II, AI Platform | Cadence Design Systems | SAN JOSE | 0.4236 | 0.2525 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 72 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7489 | 0.249 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 73 | Digital Transformation Manufacturing Engineer 2/3 | Northrop Grumman | United States-California-Northridge | 0.4318 | 0.249 | SWE_FULLTIME | DevOps, Data Engineering, Python |
| 74 | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire in New York, New York / Careers at SIG | 0.6962 | 0.249 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Python |
| 75 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5015 | 0.2475 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 76 | Data Engineering & Analytics, Software Engineering MTS | Salesforce | India - Hyderabad | 0.4813 | 0.2475 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 77 | Logistics TMS Analyst | Monster Energy | USA - Corona, CA; USA - Rogers, AR | 0.4079 | 0.2425 | DATA_ANALYST_FULLTIME | SQL |
| 78 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.2425 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | SQL |
| 79 | Software Engineering I | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 80 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 81 | Software Engineer I | LivaNova | Houston, Texas, United States | 0.4256 | 0.2425 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | C++ |
| 82 | Software Engineer II (Java) | Sony Interactive Entertainment | United States, Madison, WI | 0.5699 | 0.2425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, CI/CD |
| 83 | Lead Demand Planner | GlobalFoundries | USA - Texas - Austin | 0.4164 | 0.2425 | DATA_ANALYST_FULLTIME | SQL |
| 84 | 2026 Raytheon Full Time-Software Engineer I – EOIR Advanced Products and Solutions (Onsite) | RTX | US-TX-MCKINNEY-513WC ~ 2501 W University Dr ~ WING C BLDG | 0.3632 | 0.2425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++ |
| 85 | Full Stack Developer (Remote) | RTX | US-CT-REMOTE | 0.4136 | 0.2425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 86 | Senior BI Engineer, CRM | General Motors | Remote - United States | 0.5429 | 0.2415 | DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 87 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.4929 | 0.2415 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 88 | Pricing Representative Temp to Hire | Monster Energy | USA - Corona, CA | 0.4078 | 0.23 | DATA_ANALYST_FULLTIME | — |
| 89 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5109 | 0.23 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 90 | Competition Analyst | Manulife Financial | USA, Massachusetts - Full Time Remote | 0.4899 | 0.23 | DATA_ANALYST_FULLTIME | — |
| 91 | Training Analyst | Boeing | USA - Huntsville, AL | 0.4459 | 0.23 | DATA_ANALYST_FULLTIME | — |
| 92 | Cybersecurity Asset and Observability Analyst | CACI | National Harbor, MD, US | 0.3436 | 0.23 | DATA_ANALYST_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 93 | Analyst, Enterprise Agentic Search | American Express | New York, NY, United States | 0.3 | 0.23 | DATA_ANALYST_FULLTIME | — |
| 94 | Analyst - Enterprise Agentic Search Content | American Express | New York, NY, United States | 0.3 | 0.23 | DATA_ANALYST_FULLTIME | — |
| 95 | Sr. Process Transformation Business Intelligence Data Analyst | General Motors | Warren, Michigan, United States of America | 0.5798 | 0.228 | DATA_ANALYST_FULLTIME | Data Engineering, SQL, Python |
| 96 | Software Engineer ll - Java 8 Reactjs Web Search Team | American Express | Phoenix, AZ, United States | 0.5327 | 0.228 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, Python |
| 97 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.228 | SWE_FULLTIME | DevOps, Python, Java |
| 98 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5744 | 0.2205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, C++ |
| 99 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, Liverpool | 0.5759 | 0.2205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, C++ |
| 100 | Sr Software Engineer I - Java - International Card Risk Services Technology | American Express | Phoenix, AZ, United States | 0.5514 | 0.2205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, CI/CD |
| 101 | Senior Analyst - Sales Strategy & Operations | Salesforce | United Kingdom - London | 0.4813 | 0.2205 | DATA_ANALYST_FULLTIME, OPERATIONS_FULLTIME | Analytics Engineering, SQL |
| 102 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.4754 | 0.2205 | SWE_FULLTIME, RESEARCH_SCIENTIST_FULLTIME | AI Systems, Python |
| 103 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4632 | 0.2205 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, CI/CD |
| 104 | GMF Sr Credit Analyst I | GM Financial | Raleigh, NC, United States | 0.4469 | 0.2205 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 105 | Senior Strategy & Analytics Analyst | VITAS Healthcare | Miami, FL, United States | 0.4015 | 0.2205 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 106 | AI Builder Partner Solutions | Salesforce | California - San Francisco | 0.6822 | 0.215 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Python |
| 107 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3562 | 0.215 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, DevOps, Python |
| 108 | Senior Auditor | American Express | New York, NY, United States / AEDR Desert Ridge CSB - Sierra / AEDR Desert Ridge OB1-Camelback / AEDR Desert Ridge OB2-McDowell / AEDR Desert Ridge OB4 - Canyon / Towne Ridge Center III / Charlotte Hybrid-600 Tryon | 0.4813 | 0.213 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 109 | Senior Data Scientist I | RELX | Gurgaon | 0.5814 | 0.2115 | DATA_SCIENTIST_FULLTIME | AI Systems, Machine Learning, Data Engineering |
| 110 | Senior Category Analyst | Monster Energy | USA - Corona, CA | 0.3902 | 0.2085 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, R |
| 111 | Analyst-Data Analytics | American Express | Gurugram, HR, India | 0.5492 | 0.205 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Hive |
| 112 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4145 | 0.2025 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Python |
| 113 | Lead Software/Controls Engineer | GE Vernova | Wilmington NC USA | 0.4187 | 0.201 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, C, Python |
| 114 | Senior Business Intelligence Analyst | Boeing | USA - Everett, WA | 0.4456 | 0.201 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 115 | Senior BI Analyst | Torc Robotics | Ann Arbor, MI, Remote - US | 0.427 | 0.201 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 116 | Lead Machine Learning Engineer | Capital One | McLean, VA | 0.5586 | 0.1995 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Machine Learning, Data Engineering, DevOps |
| 117 | Senior Inference Engineer, AIConfigurator for Dynamo | NVIDIA | US, CA, Santa Clara | 0.7794 | 0.1935 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python |
| 118 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.5378 | 0.1935 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, SQL, CI/CD |
| 119 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.5809 | 0.1935 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, CI/CD |
| 120 | Senior Analyst, Strategic Operations & Insights | Salesforce | New York - New York | 0.4555 | 0.1935 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 121 | Data Engineer, AI/ML III/IV | Zone 5 Technologies | United States | 0.4732 | 0.1935 | DATA_ANALYST_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Analytics Engineering, Python |
| 122 | Sr. Business Analyst, Commercial Treasury Management Product Analytics | Capital One | New York, NY | 0.4081 | 0.1935 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 123 | Cloud Developer | Freedom Technology Solutions Group | Chantilly, VA | 0.5985 | 0.1925 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, Python |
| 124 | People Analytics Lead - Recruiting | Notion | San Francisco, California / New York, New York | 0.6795 | 0.186 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 125 | Facilities Analyst (Senior or Lead) | Boeing | USA - Mesa, AZ | 0.5384 | 0.186 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 126 | Senior Financial Analyst | Boeing | USA - San Antonio, TX | 0.4828 | 0.186 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 127 | Lead DevOps Developer | Boeing | USA - Long Beach, CA | 0.5052 | 0.186 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, CI/CD |
| 128 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.4865 | 0.186 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps |
| 129 | Associate-Digital Product Management | American Express | Gurugram, HR, India | 0.5514 | 0.18 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, Python, SQL |
| 130 | Analyst-Risk Management | American Express | Singapore | 0.5513 | 0.18 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 131 | Senior Cyber Security Engineer – Security Services | General Motors | Warren, Michigan, United States of America | 0.5495 | 0.18 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Python, Java |
| 132 | Software Engineer II - AI Focused | Cadence Design Systems | BELO HORIZONTE | 0.549 | 0.18 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, C++, Python |
| 133 | Workforce Insights Consultant | Ciena | Belfast | 0.5246 | 0.18 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 134 | AI-Enabled Full Stack Developer - Experienced | Micron Technology | Taichung - AATT, Taiwan | 0.4617 | 0.18 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, SQL, NoSQL |
| 135 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4251 | 0.18 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, SQL |
| 136 | Business Analyst | American Express | Gurugram, HR, India | 0.4162 | 0.18 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 137 | Analyst-Risk Management | American Express | Gurugram, HR, India | 0.4086 | 0.18 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 138 | DATA SCIENTIST | Micron Technology | Fab 10A, Singapore | 0.4079 | 0.18 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, SQL |
| 139 | Senior Gen AI Developer | KBR | El Segundo, California | 0.6387 | 0.177 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Machine Learning, DevOps |
| 140 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4327 | 0.1725 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 141 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4318 | 0.1725 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 142 | Lead Software Engineer (Scala, JavaScript) | Capital One | New York, NY | 0.5951 | 0.168 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Scala, Python |
| 143 | Software Engineer I | LexisNexis Risk Solutions | Cardiff | 0.5806 | 0.1675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, CI/CD |
| 144 | CX OM BUSINESS SYSTEMS ANALYST | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.1675 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 145 | Analyst-Business Development | American Express | Gurugram, HR, India | 0.4086 | 0.1675 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 146 | Sr Financial Analyst | American Express | New York, NY, United States | 0.5513 | 0.165 | DATA_ANALYST_FULLTIME | — |
| 147 | Senior Analyst - Paid Search Banking & Non-Card | American Express | New York, NY, United States | 0.502 | 0.165 | DATA_ANALYST_FULLTIME | — |
| 148 | Engineer I/Engineer II/Sr. Engineer/Sr Engineer II | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4631 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 149 | Associate LNG Commercial Analyst/LNG Commercial Analyst/Sr LNG Commercial Analyst | Berkshire Hathaway Energy | Glen Allen, VA, United States | 0.4619 | 0.165 | DATA_ANALYST_FULLTIME | — |
| 150 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4469 | 0.165 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | CI/CD |
| 151 | Senior Process Engineer (Oil and Gas, EPC, Midstream) | NOV | Dubai, Dubai, United Arab Emirates | 0.4463 | 0.165 | SWE_FULLTIME | — |
| 152 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.4631 | 0.1635 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, AI Systems, Java |
| 153 | Sr Engineer, Data Science | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4464 | 0.1635 | DATA_SCIENTIST_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 154 | Software Engineer Developer ( Mid-Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++, Python |
| 155 | Software Developer (Mid Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.1605 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | C, C++, Python |
| 156 | Lead Software Engineer, Fullstack (React, Java, Python) | Capital One | New York, NY | 0.6247 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 157 | Lead Software Engineer, Full Stack (Risk Tech, Intelligent Foundations & Experiences) | Capital One | New York, NY | 0.5944 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 158 | Senior Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.6085 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 159 | Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.5712 | 0.1605 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 160 | Sr Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5243 | 0.156 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 161 | Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5014 | 0.156 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | Machine Learning, AI Systems, Python |
| 162 | Advanced Data Scientist | Honeywell | Hyderabad, Telangana, India | 0.5004 | 0.156 | DATA_SCIENTIST_FULLTIME | Machine Learning, Analytics Engineering, Python |
| 163 | Senior Analytics Engineer | Salesforce | India - Bangalore | 0.4813 | 0.156 | DATA_ENGINEER_FULLTIME, DATA_ANALYST_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 164 | Analyst, Competitive Intelligence - Bangalore | Danaher Corporation | Bangalore, Karnataka, India | 0.5495 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 165 | ビジネスアナリスト | Manulife Financial | Tokyo | 0.5492 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 166 | Operations Analyst | Manulife Financial | Quezon City | 0.5492 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 167 | Financial Svcs Analyst | Honeywell | Bengaluru, Karnataka, India | 0.5014 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 168 | Développeur de logiciel | Harris Computer | Quebec, Canada | 0.3817 | 0.155 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, CI/CD |
| 169 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.4543 | 0.155 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | DevOps |
| 170 | Data Analyst | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4315 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 171 | Energy Markets Analyst (NYISO) | Voltus | Remote | 0.4378 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 172 | Sales Business Planning Analyst | Micron Technology | Boise, ID - Main Site | 0.4195 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 173 | Analyst - Operational Risk Management | American Express | Taguig City, Manila, Philippines | 0.4086 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 174 | Quality Data Analytics Engineer | GE Vernova | Vadodara | 0.4079 | 0.155 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 175 | Senior Lead AI Engineer,(MLX, Agentic AI, Gen AI platform Services) | Capital One | San Jose, CA | 0.6325 | 0.1515 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Python |
| 176 | Senior Machine Learning Engineer (AI Foundations) | Capital One | McLean, VA | 0.5022 | 0.1515 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Data Engineering, Python |
| 177 | Senior Lead AI Engineer (Gen AI Platform Services) | Capital One | San Jose, CA | 0.6085 | 0.1515 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Python |
| 178 | Senior Product Data Scientist | MaintainX | Montreal, Toronto, Vancouver, SF (Remote) | 0.457 | 0.1485 | DATA_SCIENTIST_FULLTIME | Machine Learning, AI Systems, Python |
| 179 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.4752 | 0.1485 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, AI Systems, Python |
| 180 | Software Engineer I (AI Driven) | Travelers | GA - Atlanta | 0.5232 | 0.1475 | SWE_FULLTIME | AI Systems, Python, Java |
| 181 | Software Engineer, Hardware-in-the-Loop (Starlink) | SpaceX | Redmond, WA | 0.4987 | 0.1475 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python, C |
| 182 | Senior Software Engineer - C++/UI | General Motors | Mountain View, California, United States of America | 0.5715 | 0.1455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++ |
| 183 | Senior Software Engineer NAVAIR Product Line | CACI | Austin, TX, US | 0.5443 | 0.1455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 184 | Advanced Software Engr | Honeywell | Hamilton Township, NJ, United States | 0.462 | 0.1455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 185 | Senior Software Engineer - Fullstack | Sigma Computing | New York City, NY | 0.5856 | 0.1455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 186 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.4509 | 0.1455 | SWE_FULLTIME | Python |
| 187 | Engineering Technical Lead - I&C Embedded Software | GE Vernova | Wilmington NC USA | 0.3946 | 0.1455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C |
| 188 | Senior Technical Designer | Sony Interactive Entertainment | United States, Santa Monica, CA | 0.4603 | 0.1455 | SWE_FULLTIME | C++ |
| 189 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in New York, New York / Careers at SIG | 0.72 | 0.1455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++ |
| 190 | Product Architect | Monster Energy | USA - Corona, CA | 0.5401 | 0.138 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 191 | Senior Financial Analyst - Coronary Sales Finance | Medtronic | Minneapolis, Minnesota, United States of America | 0.4844 | 0.138 | DATA_ANALYST_FULLTIME | — |
| 192 | Senior Business Analyst | Boeing | USA - Seattle, WA | 0.4797 | 0.138 | DATA_ANALYST_FULLTIME | — |
| 193 | GMF Sr Credit Analyst I - Zone C | GM Financial | Seattle, WA, United States | 0.3928 | 0.138 | DATA_ANALYST_FULLTIME | — |
| 194 | Software Engineer - Compiler  | Sigma Computing | New York City, NY | 0.58 | 0.138 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 195 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.4696 | 0.138 | SWE_FULLTIME | — |
| 196 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.1365 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Java |
| 197 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5771 | 0.1365 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Machine Learning, Java |
| 198 | Marketing Productivity Engineer | Sigma Computing | San Francisco, CA | 0.626 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python, SQL |
| 199 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.406 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, C++ |
| 200 | FinOps Technical Analyst | Bank of Montreal | Toronto, ON, CAN | 0.3494 | 0.135 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 201 | Software Engineer, Test Infrastructure (Application Software) | SpaceX | Hawthorne, CA | 0.4754 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, C++, Python |
| 202 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.135 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, C, C++ |
| 203 | Software Engineer, Developer Productivity  | Glean | Mountain View, CA | 0.4989 | 0.135 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Java, Python |
| 204 | Sr. Lead Software Engineer | Capital One | Bangalore, In | 0.5497 | 0.1305 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, Python |
| 205 | Senior AI/ML Engineer | Sigma Computing | San Francisco, CA | 0.6783 | 0.129 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, AI Systems, Python |
| 206 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6359 | 0.129 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | Machine Learning, AI Systems, Python |
| 207 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.129 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Java |
| 208 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.129 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Machine Learning, Java |
| 209 | Senior Data Analyst/Developer | CACI | Remote (Any State) | 0.437 | 0.129 | DATA_ANALYST_FULLTIME, SWE_FULLTIME | Data Engineering, Analytics Engineering, SQL |
| 210 | CAD Engineer | Micron Technology | Richardson, TX | 0.5796 | 0.125 | SWE_FULLTIME | Python, C, C++ |
| 211 | Software Engineer II | Cox | Austin TX | 0.4597 | 0.1225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, DynamoDB |
| 212 | Software Engineer II | Cox | Atlanta GA | 0.3987 | 0.1225 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | DevOps, Java |
| 213 | RAN Validation Engineer (Starlink Mobile)  | SpaceX | Sunnyvale, CA | 0.4866 | 0.1225 | SWE_FULLTIME | DevOps, Python |
| 214 | GTM Engineer | Greenhouse | British Columbia | 0.4751 | 0.1225 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, API integration |
| 215 | Aeroderivative Performance Engineer - Field | GE Vernova | Greenville | 0.3469 | 0.1225 | SWE_FULLTIME | Data Engineering, Python |
| 216 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4439 | 0.1225 | SWE_FULLTIME | DevOps, Python |
| 217 | Sr Software Engineer - 20197 | Cox | Atlanta GA | 0.3892 | 0.1215 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, AI Systems, Java |
| 218 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.4632 | 0.1155 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | DevOps, Java, Python |
| 219 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.525 | 0.1125 | SWE_FULLTIME | Python, Java, SQL |
| 220 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1125 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 221 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5176 | 0.1125 | SWE_FULLTIME | Python, Java, C++ |
| 222 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 223 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.5005 | 0.1125 | SWE_FULLTIME | Java, Python, C++ |
| 224 | Software Development Engineer | Micron Technology | Taoyuan - Fab 11, Taiwan | 0.5003 | 0.1125 | SWE_FULLTIME | Python, Java, SQL |
| 225 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 226 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 227 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 228 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 229 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4812 | 0.1125 | SWE_FULLTIME | Python, Java, SQL |
| 230 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 231 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 232 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4633 | 0.1125 | SWE_FULLTIME | C++, Java, Python |
| 233 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4632 | 0.1125 | SWE_FULLTIME | Java, Python, SQL |
| 234 | QE PCT Engineer | Micron Technology | Miaoli - Tongluo, Taiwan | 0.4235 | 0.1125 | SWE_FULLTIME | Python, C++, SQL |
| 235 | Clinical Analytics Specialist – MD | RELX | Texas | 0.5053 | 0.11 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 236 | Quality Engineer II | RELX | Philadelphia, PA | 0.4851 | 0.11 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps |
| 237 | Process & Data Integration Specialist H/F | GE Vernova | Greenville | 0.4816 | 0.11 | DATA_ANALYST_FULLTIME | Data Engineering |
| 238 | Decision Support Analyst II | LexisNexis Risk Solutions | Alpharetta, GA | 0.3857 | 0.11 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 239 | Advanced Data Scientist | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.108 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, R |
| 240 | Solutions Architect | Centerfield | Los Angeles, California | 0.4688 | 0.108 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, MySQL |
| 241 | Senior Network Engineer | NOV | Kochi, Kerala, India | 0.4802 | 0.108 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Python, C |
| 242 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4327 | 0.108 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Java, Python |
| 243 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4323 | 0.108 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Scala, Python |
| 244 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6645 | 0.1035 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Java, Scala |
| 245 | Senior Associate, Data Scientist - NLP | Capital One | McLean, VA | 0.4651 | 0.1035 | DATA_SCIENTIST_FULLTIME | Machine Learning, Python, PyTorch |
| 246 | Senior Software Engineer | EarnIn | Mexico City, Mexico | 0.643 | 0.1005 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python |
| 247 | Software Engineering Architect | Salesforce | Norway - Remote | 0.5793 | 0.1005 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Java |
| 248 | Senior Analyst - Control Management | American Express | Gurugram, HR, India | 0.549 | 0.1005 | DATA_ANALYST_FULLTIME | Analytics Engineering, Python |
| 249 | Experienced Software Application Development – QA and Test Automation Engineer | Boeing | IND - Bangalore, India | 0.5019 | 0.1005 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, CI/CD |
| 250 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5111 | 0.1005 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | AI Systems, Python |
| 251 | Senior Engineer, Assembly & Test Central QA | Micron Technology | Fab 10A, Singapore | 0.4806 | 0.1005 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 252 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.4754 | 0.1005 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python |
| 253 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1 | SWE_FULLTIME | Java, Python |
| 254 | Appian Product Engineer  | Appian | McLean, Virginia | 0.4941 | 0.1 | SWE_FULLTIME | SQL, Java |
| 255 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4632 | 0.1 | SWE_FULLTIME | Java, Python |
| 256 | Associate ATE Software Engineer | Boeing | IND - Bangalore, India | 0.4469 | 0.1 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, C |
| 257 | Forward Deployed Engineer  | Loop | San Francisco, CA | 0.4398 | 0.1 | SWE_FULLTIME | Python, SQL |
| 258 | Factory Software Engineer (Starlink) | SpaceX | Bastrop, TX | 0.4246 | 0.1 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, C++ |
| 259 | Senior Lead Data Engineer (Enterprise Platform Technology) (Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7512 | 0.096 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Java, Python |
| 260 | Lead Engineer 1 - Customer Application Engineering | GE Vernova | Schenectady | 0.4052 | 0.096 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 261 | Senior Analyst - Workday Testing | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.5812 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 262 | Quality Engineer Lead | LexisNexis Risk Solutions | Mumbai | 0.5798 | 0.093 | SWE_FULLTIME | DevOps |
| 263 | Senior Financial Analyst | American Express | Toronto, ON, Canada | 0.5513 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 264 | Experienced Global Security Intelligence Analyst | Boeing | IND - Bangalore, India | 0.5512 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 265 | Procurement Business Solutions Senior Analyst | Truist Bank | Atlanta, GA | 0.549 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 266 | Financial Svcs Analyst | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 267 | Senior Business Intelligence Analyst- SMAI | Micron Technology | Boise, ID - ID1 | 0.5243 | 0.093 | DATA_ANALYST_FULLTIME | Machine Learning |
| 268 | Senior Business Analyst (Platform) | Whoop | Boston, MA | 0.4478 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 269 | Senior AI Solutions Analyst | Micron Technology | Jalisco, Mexico | 0.4464 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 270 | Senior Analyst - IT-applications - Oracle EBS | Ciena | Remote- India- Gurugram | 0.4079 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 271 | Senior Data Analyst | University of Arkansas | Little Rock | 0.3278 | 0.093 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 272 | Senior Software Developer – Virtualization, SIL, and AI‑Enablement | General Motors | Markham, Ontario, Canada | 0.5397 | 0.0885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Machine Learning, Python, C++ |
| 273 | Senior Data Analyst | Capital One | McLean, VA | 0.4906 | 0.0885 | DATA_ANALYST_FULLTIME | Analytics Engineering, Python, R |
| 274 | Senior Data Analyst-Tech Analytics | Capital One | McLean, VA | 0.4429 | 0.0885 | DATA_ANALYST_FULLTIME | Analytics Engineering, Python, R |
| 275 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6359 | 0.0885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, SQL |
| 276 | Lead Software Engineer, DevOps | Capital One | Riverwoods, IL | 0.5721 | 0.0885 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Java, Python |
| 277 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.0885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, Python |
| 278 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.0885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, Python |
| 279 | Sr. Fraud Data Analyst (Remote USA) | LexisNexis Risk Solutions | Alpharetta, GA | 0.3556 | 0.0885 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 280 | Lead Software Engineer, Full Stack | Capital One | Richmond, VA | 0.53 | 0.0885 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Java, SQL |
| 281 | Forward Deployed Engineer I/II | Giga AI | San Francisco | 0.5602 | 0.0875 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Python |
| 282 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5797 | 0.0875 | SWE_FULLTIME | Python |
| 283 | Package Device Product Engineer (PDPE) Engineer | Micron Technology | Sanand - 303A - AT/SSD/MOD, India | 0.5796 | 0.0875 | SWE_FULLTIME | Python |
| 284 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5004 | 0.0875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, CI/CD |
| 285 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.0875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 286 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4813 | 0.0875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, API integration |
| 287 | RDA Process Owner｜データ分析で歩留まり・品質を改善（広島） | Micron Technology | Hiroshima - Fab 15, Japan | 0.4806 | 0.0875 | DATA_ANALYST_FULLTIME | Python |
| 288 | IT SOFTWARE ENGINEER | Micron Technology | Fab 10W, Singapore | 0.4194 | 0.0875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 289 | Lead Data Analyst - Product Growth | Constant Contact | Toronto, Ontario, Canada | 0.618 | 0.081 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 290 | Lead Data Analyst - Product Growth | Constant Contact | Waltham or Boston, MA | 0.5579 | 0.081 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 291 | Analyst/Senior Analyst, Product Growth & GTM Strategy | Salesforce | California - San Francisco | 0.5721 | 0.081 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL, Python |
| 292 | Senior Software Developer – DevOps | General Motors | Markham, Ontario, Canada | 0.5412 | 0.081 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, C++, Python |
| 293 | Senior Software Engineer | Cox | Atlanta GA | 0.5311 | 0.081 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, Python |
| 294 | Architect - Personal Insurance Cross-Domain Architecture | Travelers | CT - Hartford | 0.5447 | 0.081 | SWE_FULLTIME | AI Systems, Python, Java |
| 295 | Senior Associate, Capital Markets and Risk (Stress Test Forecasting Team) (Hybrid) | Capital One | McLean, VA | 0.403 | 0.081 | DATA_ANALYST_FULLTIME | Data Engineering, Python, SQL |
| 296 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.075 | SWE_FULLTIME | — |
| 297 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.075 | SWE_FULLTIME | — |
| 298 | Revenue Operations Business Analyst – Strategic Revenue Intelligence | Micron Technology | Boise, ID - Main Site | 0.5016 | 0.075 | DATA_ANALYST_FULLTIME | — |
| 299 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.075 | SWE_FULLTIME | — |
| 300 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4633 | 0.075 | SWE_FULLTIME | — |
| 301 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.4516 | 0.075 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 302 | Product Engineer | Linear | North America | 0.4519 | 0.075 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 303 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4327 | 0.075 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 304 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4197 | 0.075 | SWE_FULLTIME | — |
| 305 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4086 | 0.075 | SWE_FULLTIME | — |
| 306 | Lead Analyst | American Express | Gurugram, HR, India | 0.4086 | 0.075 | DATA_ANALYST_FULLTIME | — |
| 307 | Senior Analyst, Strategy & Data | Salesforce | California - San Francisco | 0.5534 | 0.0735 | DATA_ANALYST_FULLTIME | Analytics Engineering, SQL |
| 308 | Sr. Software Engineer, Telemetry (Starlink) | SpaceX | Hawthorne, CA | 0.6232 | 0.0735 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java, CI/CD |
| 309 | Sr Software Engineer - 20198 | Cox | Atlanta GA | 0.4833 | 0.0735 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Java |
| 310 | Sr. Product Solution Analyst, TD Securities | TD Bank | Toronto, Ontario | 0.4116 | 0.0735 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Python, CI/CD |
| 311 | Sr. QA Engineer - IP Routing | Ciena | Remote-Canada | 0.4707 | 0.0735 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps, Python |
| 312 | Software Engineer I | LexisNexis Risk Solutions | Colorado | 0.4234 | 0.0675 | SWE_FULLTIME | Java, C++, SQL |
| 313 | Firmware Engineer Data Center Solid State Drives | Micron Technology | Arzano (NA), Italy | 0.3054 | 0.0675 | SWE_FULLTIME | Python, C, C++ |
| 314 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Palo Alto, CA | 0.4864 | 0.0675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++, Python |
| 315 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.5494 | 0.0675 | SWE_FULLTIME | C++, Java, Python |
| 316 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.0675 | SWE_FULLTIME | C++, Python, Java |
| 317 | Senior Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.4619 | 0.0675 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 318 | Senior Software Developer / HR Technology & Shared Services / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Developer / HR Technology & Shared Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.0675 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java, SQL, Python |
| 319 | Senior Revenue Analyst, Customer Success | Constant Contact | Waltham or Boston, MA | 0.4871 | 0.066 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 320 | Senior Business Planning Analyst | Micron Technology | San Jose, CA | 0.6972 | 0.066 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 321 | Senior Associate; Brand Creative Researcher | Capital One | Richmond, VA | 0.4728 | 0.066 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 322 | Business Analyst - Oracle EBS Budget to Report (B2R) | CACI | Remote (Any State) | 0.4706 | 0.066 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 323 | Sr Project Management Analyst | Motorola Solutions | Washington DC Remote Work | 0.4624 | 0.066 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 324 | Decision Support Sr Finance Analyst | LexisNexis Risk Solutions | Alpharetta, GA | 0.4062 | 0.066 | DATA_ANALYST_FULLTIME, FINANCE_FULLTIME | Analytics Engineering |
| 325 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | San Francisco, CA | 0.5856 | 0.066 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps |
| 326 | Senior Software Engineer | Cox | Atlanta GA | 0.4445 | 0.066 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | DevOps |
| 327 | Senior Financial Analyst - Cox Fleet, Sales | Cox | Atlanta GA | 0.3805 | 0.066 | DATA_ANALYST_FULLTIME | Analytics Engineering |
| 328 | Software Engineering MTS - Compliance Automation & Tooling (Apex, Python) | Salesforce | India - Hyderabad | 0.5792 | 0.06 | SWE_FULLTIME | Python, SQL |
| 329 | Senior Discipline Engineer | Valeo | Chennai | 0.5507 | 0.06 | SWE_FULLTIME | C++, Python |
| 330 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.06 | SWE_FULLTIME | Java, SQL |
| 331 | Software Engineering, SMTS (Salesforce Developer) | Salesforce | India - Hyderabad | 0.4755 | 0.06 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python |
| 332 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4198 | 0.06 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java, MySQL |
| 333 | Software Engineer II, Mission Interface | Torc Robotics | Ann Arbor, MI | 0.6096 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, Python |
| 334 | Software Engineer I | Cox | Austin TX | 0.4688 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python |
| 335 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.5825 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, Python |
| 336 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.5603 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, Python |
| 337 | Systems Engineer - US Remote | Motorola Solutions | Illinois Remote Work | 0.429 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, SQL |
| 338 | Software Engineer II | Cox | Atlanta GA | 0.4239 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL, Java |
| 339 | ENGINEER, FW & PRODUCT TEST ENGINEERING | Micron Technology | Arzano (NA), Italy | 0.3292 | 0.055 | SWE_FULLTIME | C, Python |
| 340 | Entry Level Software Engineer - Austin, TX | Cox | Austin TX | 0.3807 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, C++ |
| 341 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 342 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 343 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Redmond, WA | 0.4574 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 344 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Palo Alto, CA | 0.4864 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 345 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 346 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 347 | ML Engineer, II - App Engine | Torc Robotics | Ann Arbor, MI, Montreal, Canada | 0.4928 | 0.055 | SWE_FULLTIME | C++, PyTorch |
| 348 | Engineer Software T1/T2 | Northrop Grumman | GAWR03GC | 0.3461 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 349 | Software Engineer, Network Monitoring (Starlink) | SpaceX | Hawthorne, CA | 0.4365 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, Java |
| 350 | Software Engineer II | Cadence Design Systems | SAN JOSE | 0.4196 | 0.055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, C |
| 351 | Senior Software Engineer | GE Vernova | Bucharest | 0.5514 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 352 | Senior Discipline Engineer - Software Requirements | Valeo | Chennai | 0.5507 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++ |
| 353 | SMTS, Software Engineering (Salesforce Expert) | Salesforce | India - Hyderabad | 0.5494 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | MySQL, CI/CD |
| 354 | Simulation Software Engineer (Experienced or Senior level) | Boeing | GBR - Crawley, UK | 0.5019 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, CI/CD |
| 355 | Senior Software Engineer, Full-Stack — Content Tools | Epic Kids | Bangalore, India (remote within India) | 0.4626 | 0.0525 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | MySQL |
| 356 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4316 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 357 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4198 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 358 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.0525 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++ |
| 359 | Lead Software Engineer, Back End (Cloud Operations Resilience Engineering) | Capital One | Plano, TX | 0.5711 | 0.048 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, Scala |
| 360 | Lead Software Engineer | Capital One | McLean, VA | 0.5586 | 0.048 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 361 | Lead Software Engineer (Python, Kubernetes) | Capital One | McLean, VA | 0.5497 | 0.048 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, Java, SQL |
| 362 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 363 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.4632 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 364 | Sr IT Analyst | Honeywell | Bengaluru, Karnataka, India | 0.4619 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 365 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.4587 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 366 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4327 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 367 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4327 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 368 | Systems Integration Specialist (Experienced/Senior) | Boeing | POL - Swidnik, Poland | 0.4327 | 0.045 | DATA_ANALYST_FULLTIME | — |
| 369 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.045 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 370 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.045 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 371 | Sr Business Analyst - Informatica MDM | Micron Technology | Hyderabad - Phoenix Aquila, India | 0.4078 | 0.045 | DATA_ANALYST_FULLTIME | — |
| 372 | Software Engineer II | Cox | Atlanta GA | 0.3996 | 0.0425 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java |
| 373 | GTM Engineer | Greenhouse | Ontario | 0.4752 | 0.0425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, API Integration |
| 374 | Software Engineer II - 20202 | Cox | Atlanta GA | 0.3445 | 0.0425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 375 | Quality Assurance Engineer PON / DCOM | Ciena | Ottawa | 0.286 | 0.0425 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python |
| 376 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.4294 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, Java, Python |
| 377 | Senior Embedded Software Engineer | Micron Technology | San Jose, CA | 0.7214 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++, Python |
| 378 | Lead Software Engineer | Capital One | McLean, VA | 0.628 | 0.0405 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java, SQL, Python |
| 379 | Lead Software Engineer | Capital One | McLean, VA | 0.6279 | 0.0405 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java, SQL, Python |
| 380 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6358 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 381 | Lead Software Engineer | Capital One | McLean, VA | 0.5711 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 382 | Lead Software Engineer (Java, Golang, AWS) | Capital One | Plano, TX | 0.5413 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, Python, SQL |
| 383 | Senior Lead Software Engineer, Full Stack (Global Payment Network) | Capital One | Riverwoods, IL | 0.6053 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 384 | Lead Software Engineer, Full Stack (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.5497 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 385 | Lead Software Engineer, Full Stack (Golang, Angular, AWS) | Capital One | Richmond, VA | 0.5221 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 386 | Lead Software Engineer, Full Stack | Capital One | Riverwoods, IL | 0.5221 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 387 | Lead Software Engineer , Backend | Capital One | Plano, TX | 0.5214 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 388 | Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.5175 | 0.0405 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java, SQL, Python |
| 389 | Lead Software Engineer, Back End | Capital One | Plano, TX | 0.4981 | 0.0405 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL, Python |
| 390 | Sr Embedded Software Engineer | Dexcom | San Diego, California | 0.5218 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 391 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4278 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL |
| 392 | Sr. Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 393 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.5769 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 394 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.5758 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C, C++ |
| 395 | Lead Software Engineer | Cox | Austin TX | 0.499 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Python, Java, CI/CD |
| 396 | Sr. Electricity Market Optimization Software Engineer | GE Vernova | Bellevue | 0.448 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | C++, Python |
| 397 | Senior ABAP Developer | CACI | Remote (Any State) | 0.3919 | 0.033 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java, SQL |
| 398 | M365 Developer | CACI | Remote (Any State) | 0.4972 | 0.03 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 399 | Jr. Investment Analyst | Manulife Financial | Toronto, Ontario | 0.4345 | 0.03 | DATA_ANALYST_FULLTIME | — |
| 400 | Quality Assurance Analyst I, Manheim Mobile Inspections | Cox | Remote - Michigan | 0.4206 | 0.03 | DATA_ANALYST_FULLTIME | — |
| 401 | Field Supervision Analyst | Manulife Financial | Toronto, Ontario | 0.4115 | 0.03 | DATA_ANALYST_FULLTIME | — |
| 402 | Construction Surety Underwriter / Financial Analyst (Associate Account Executive) | Travelers | UT - Salt Lake City | 0.3532 | 0.03 | DATA_ANALYST_FULLTIME | — |
| 403 | SAP Business Analyst | CACI | Remote (Any State) | 0.3387 | 0.03 | DATA_ANALYST_FULLTIME | — |
| 404 | (Remote) System Analyst/Software Developer | Harris Computer | Office - Blair | 0.3286 | 0.03 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 405 | SAP Business Analyst | CACI | Remote (Any State) | 0.3273 | 0.03 | DATA_ANALYST_FULLTIME | — |
| 406 | Senior Product Analyst-Agile | Truist Bank | Richmond, VA | 0.4158 | 0.0255 | DATA_ANALYST_FULLTIME | SQL |
| 407 | Sr Full Stack Developer, TD Securities | TD Bank | Toronto, Ontario | 0.5025 | 0.0255 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Java, CI/CD |
| 408 | Software Engineer - Compiler  | Sigma Computing | San Francisco, CA | 0.5799 | 0.0255 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | SQL |
| 409 | IT Developer (Java), TD Securities | TD Bank | Toronto, Ontario | 0.3363 | 0.0255 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Java |
| 410 | Software Engineer II-Team Lead (AWS, Typescript) | Travelers | CT - Hartford | 0.5281 | 0.018 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 411 | Lead Protection and Control Engineer | GE Vernova | Remote | 0.4757 | 0.018 | SWE_FULLTIME, SYSTEMS_ENGINEER_FULLTIME | — |
| 412 | Sr. Business Analyst | Capital One | McLean, VA | 0.4427 | 0.018 | DATA_ANALYST_FULLTIME | — |
| 413 | Senior Software Engineer - Fullstack | Sigma Computing | San Francisco, CA | 0.5665 | 0.018 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | — |
| 414 | Lead Software Engineer, Android (Kotlin & Jetpack Compose) | Capital One | McLean, VA | 0.5778 | 0.018 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 415 | Sr Software Engineer | Cox | Atlanta GA | 0.4437 | 0.018 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | — |
| 416 | Software Engineer, Security | Notion | San Francisco, California | 0.7173 | 0.018 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 417 | .NET/C# Engineer, TD Securities | TD Bank | Toronto, Ontario | 0.3795 | 0.018 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | CI/CD |
| 418 | Global Master Data Sr. Analyst H/F | GE Vernova | Greenville | 0.4432 | 0.018 | DATA_ANALYST_FULLTIME | — |

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

- **Total jobs matching subscribed pools (after filters):** 370
- **Notification-eligible jobs (≤60d, not yet emailed):** 370
- **Personal score range:** 0.0766 – 0.4321 (120 unique tiers)
- Pool tag counts (jobs can appear in multiple pools):

| Pool | Job tag count |
|------|---------------|
| `SWE_FULLTIME` | 282 |
| `BACKEND_ENGINEER_FULLTIME` | 214 |
| `ML_ENGINEER_FULLTIME` | 79 |
| `FULLSTACK_ENGINEER_FULLTIME` | 64 |
| `DATA_ENGINEER_FULLTIME` | 51 |
| `FRONTEND_ENGINEER_FULLTIME` | 22 |
| `DEVOPS_ENGINEER_FULLTIME` | 16 |
| `SOLUTIONS_ENGINEER_FULLTIME` | 4 |
| `SECURITY_ENGINEER_FULLTIME` | 4 |
| `MOBILE_ENGINEER_FULLTIME` | 3 |
| `SUPPORT_ENGINEER_FULLTIME` | 3 |
| `RESEARCH_SCIENTIST_FULLTIME` | 2 |
| `DATA_ANALYST_FULLTIME` | 2 |
| `SYSTEMS_ENGINEER_FULLTIME` | 1 |
| `MARKETING_FULLTIME` | 1 |
| `DATA_SCIENTIST_FULLTIME` | 1 |

### Email notification — top 4 (personalized)

#### #1 — AI Engineer III - Global Servicing Technology @ American Express

- **Location:** New York, NY, United States | Sunrise Campus | AEDR Desert Ridge CSB - Sierra (unclear)
- **Posted:** 2026-06-09T00:00:00+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.4469
- **Personal score:** 0.4321
- **Pools:** `ML_ENGINEER_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** ML_ENGINEER, BACKEND_ENGINEER
- **Capabilities:** Machine Learning, AI Systems, Backend Engineering
- **Skills:** LLM agentic systems, RAG pipelines
- **Match reasons:** AI Systems, Backend Engineering, Python, Go, TypeScript
- **URL:** https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions/26008627/details

#### #2 — Software Engineer II @ Cox

- **Location:** Atlanta GA (unclear)
- **Posted:** 2026-06-10T00:00:00+00:00
- **Salary:** 89400 – 134000
- **Effort:** MEDIUM
- **Opportunity score:** 0.3987
- **Personal score:** 0.431
- **Pools:** `SWE_FULLTIME`, `FULLSTACK_ENGINEER_FULLTIME`
- **Roles:** SWE, FULLSTACK_ENGINEER
- **Capabilities:** Full Stack Development, Backend Engineering, Frontend Engineering, Cloud Infrastructure, DevOps
- **Skills:** secure coding, system integration
- **Match reasons:** Full Stack Development, Backend Engineering, Cloud Infrastructure, DevOps, TypeScript
- **URL:** https://cox.wd1.myworkdayjobs.com/Cox_External_Career_Site_1/job/Atlanta-GA/Software-Engineer-II---20200_R202678358

#### #3 — Software Engineer @ Aquatic Capital Management

- **Location:** New York (unclear)
- **Posted:** 2026-06-09T19:26:04+00:00
- **Salary:** 220000 – 230000
- **Effort:** MEDIUM
- **Opportunity score:** 0.608
- **Personal score:** 0.4093
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER
- **Capabilities:** Backend Engineering, Distributed Systems, Machine Learning
- **Skills:** low-latency infrastructure, quantitative strategies, time series analysis
- **Match reasons:** Backend Engineering, Distributed Systems, Python, SQL
- **URL:** https://job-boards.greenhouse.io/aquaticcapitalmanagement/jobs/8584171002

#### #4 — Cloud Developer @ Freedom Technology Solutions Group

- **Location:** Chantilly, VA (unclear)
- **Posted:** 2026-06-12T18:40:32+00:00
- **Salary:** — – —
- **Effort:** MEDIUM
- **Opportunity score:** 0.5985
- **Personal score:** 0.4092
- **Pools:** `SWE_FULLTIME`, `BACKEND_ENGINEER_FULLTIME`
- **Roles:** SWE, BACKEND_ENGINEER
- **Capabilities:** Cloud Infrastructure, DevOps, Backend Engineering
- **Skills:** infrastructure as code, CI/CD pipelines, cloud architecture
- **Match reasons:** Cloud Infrastructure, DevOps, Backend Engineering, Java, Python
- **URL:** https://job-boards.greenhouse.io/freedomconsulting/jobs/4831214007

### Full personalized ranking (all jobs)

| Rank | Title | Company | Location | Opp | Personal | Pools | Match reasons |
|------|-------|---------|----------|-----|----------|-------|---------------|
| 1 | AI Engineer III - Global Servicing Technology | American Express | New York, NY, United States / Sunrise Campus / AEDR Desert Ridge CSB - Sierra | 0.4469 | 0.4321 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 2 | Software Engineer II | Cox | Atlanta GA | 0.3987 | 0.431 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 3 | Software Engineer | Aquatic Capital Management | New York | 0.608 | 0.4093 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 4 | Cloud Developer | Freedom Technology Solutions Group | Chantilly, VA | 0.5985 | 0.4092 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Backend Engineering |
| 5 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.4092 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 6 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.533 | 0.4092 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 7 | ML Engineer, Generative Video | Mirage | Union Square, New York City | 0.5091 | 0.3911 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Cloud Infrastructure |
| 8 | Software Engineer, Onboarding | Ramp | New York, NY (HQ) | 0.4115 | 0.3876 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, Flask |
| 9 | Software Engineer (Front End) | CACI | Aurora, CO, US | 0.3868 | 0.3875 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, React |
| 10 | Software Engineer, Network Monitoring (Starlink) | SpaceX | Hawthorne, CA | 0.4365 | 0.3875 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Python |
| 11 | Software Engineer | Intel | US, Arizona, Phoenix | 0.6671 | 0.3865 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 12 | AI Engineer III - Agentic AI | American Express | Phoenix, AZ, United States | 0.5497 | 0.3865 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Distributed Systems |
| 13 | Software Engineer I | Cox | Austin TX | 0.4688 | 0.3865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 14 | Software Engineer II (Java) | Sony Interactive Entertainment | United States, Madison, WI | 0.5699 | 0.3865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 15 | Software Engineer, Test Infrastructure (Application Software) | SpaceX | Hawthorne, CA | 0.4754 | 0.3865 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 16 | Software Engineer II | Cox | Atlanta GA | 0.3996 | 0.3865 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Backend Engineering |
| 17 | Software Engineer, Developer Productivity  | Glean | Mountain View, CA | 0.4989 | 0.3865 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | DevOps, Cloud Infrastructure, Backend Engineering |
| 18 | Software Engineer - Defense Applications | Palantir | New York, NY | 0.5474 | 0.3649 | FRONTEND_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, React, TypeScript |
| 19 | Marketing Productivity Engineer | Sigma Computing | San Francisco, CA | 0.626 | 0.3648 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, TypeScript |
| 20 | Information & Application Developer (Entry Level and Associate) | Boeing | USA - North Charleston, SC | 0.4034 | 0.3648 | SWE_FULLTIME, DATA_ANALYST_FULLTIME | Backend Engineering, Data Engineering, Python |
| 21 | Software Engineer II - 20202 | Cox | Atlanta GA | 0.3445 | 0.3648 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 22 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, Aliso Viejo, CA | 0.5298 | 0.3638 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 23 | Software Engineer, Platform  | ScaleAI | London, UK | 0.4251 | 0.351 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 24 | Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.6717 | 0.3466 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Data Engineering, Python |
| 25 | Applied Researcher II (AI Foundations) | Capital One | New York, NY | 0.5285 | 0.3422 | RESEARCH_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python |
| 26 | AI Builder Partner Solutions | Salesforce | California - San Francisco | 0.6822 | 0.3421 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 27 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.3421 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 28 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5326 | 0.3421 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 29 | Software Engineer I (AI Driven) | Travelers | GA - Atlanta | 0.5232 | 0.3421 | SWE_FULLTIME | Backend Engineering, AI Systems, Python |
| 30 | Software Engineer, Machine Learning | Whoop | Boston, MA | 0.5388 | 0.3421 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 31 | Data Engineer | Base Power Company | Austin, TX | 0.4691 | 0.3421 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Python |
| 32 | AI Engineer III | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.3421 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 33 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.3411 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Distributed Systems |
| 34 | Software Development Engineer I - General Motors Insurance | GM Financial | United States | 0.5005 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 35 | Software Engineer II | Cox | Austin TX | 0.4597 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 36 | Software Engineer, Hardware-in-the-Loop (Starlink) | SpaceX | Redmond, WA | 0.4987 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 37 | Factory Software Engineer (Starlink) | SpaceX | Bastrop, TX | 0.4246 | 0.3411 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 38 | Lead Software Engineer, Fullstack (React, Java, Python) | Capital One | New York, NY | 0.6247 | 0.3398 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 39 | Software Engineer I | LexisNexis Risk Solutions | Cardiff | 0.5806 | 0.3338 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 40 | Software Engineer II | American Express | Gurugram, HR, India | 0.4632 | 0.3282 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 41 | Software Engineer I | American Express | Phoenix, AZ, United States | 0.549 | 0.3193 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Python |
| 42 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5344 | 0.3193 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, SQL |
| 43 | Software Engineer I | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.3193 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 44 | Software Engineer II | Cox | Atlanta GA | 0.4239 | 0.3193 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, SQL |
| 45 | Data Engineer I | University of Texas at Austin | AUSTIN, TX | 0.2797 | 0.3193 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 46 | Software Development Engineer in Test II | Sony Interactive Entertainment | United States, San Diego, CA | 0.5283 | 0.3193 | SWE_FULLTIME | Full Stack Development, DevOps, Python |
| 47 | DevSecOps Software Engineer (Associate or Experienced), Phantom Works | Boeing | USA - Saint Charles, MO | 0.3778 | 0.3183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Cloud Infrastructure |
| 48 | Lead Software Engineer, Full Stack (Risk Tech, Intelligent Foundations & Experiences) | Capital One | New York, NY | 0.5944 | 0.3132 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 49 | Senior Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.6085 | 0.3132 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 50 | Lead Software Engineer, Full Stack | Capital One | New York, NY | 0.5712 | 0.3132 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 51 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6359 | 0.3125 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 52 | Product Engineer | Linear | North America | 0.4519 | 0.3121 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, TypeScript |
| 53 | Software Engineer, I - Data Engineering | Torc Robotics | Ann Arbor, MI | 0.4145 | 0.3111 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 54 | Distributed Systems Engineer | Cadence Design Systems | PORT MOODY 01 (VANCOUVER) | 0.406 | 0.3055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Backend Engineering, Data Engineering |
| 55 | AI-Enabled Full Stack Developer - Experienced | Micron Technology | Taichung - AATT, Taiwan | 0.4617 | 0.3055 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, AI Systems, Cloud Infrastructure |
| 56 | ML Engineer, Agentic Systems | Mirage | Union Square, New York City | 0.5075 | 0.3022 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 57 | Lead Software Engineer (Scala, JavaScript) | Capital One | New York, NY | 0.5951 | 0.2995 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 58 | Quality Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5345 | 0.2976 | SWE_FULLTIME, SUPPORT_ENGINEER_FULLTIME | Backend Engineering, Java, TypeScript |
| 59 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3632 | 0.2976 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 60 | Software Engineering I | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, SQL |
| 61 | Software Engineer I - CRM | The Coca-Cola Company | US - GA - Atlanta | 0.5343 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, SQL |
| 62 | Quality Engineer II | RELX | Philadelphia, PA | 0.4851 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, TypeScript |
| 63 | Research Software Engineer — Differentiable Scientific Computing  (JAX/Julia) | Axiomatic AI | Boston, US / Barcelona, Spain | 0.5272 | 0.2966 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 64 | Software Engineer for Data at Rest (DAR) Crypto & Cross Domain Solutions | General Dynamics Mission Systems | US-MA-Dedham | 0.4222 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Python |
| 65 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Palo Alto, CA | 0.4864 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 66 | RAN Validation Engineer (Starlink Mobile)  | SpaceX | Sunnyvale, CA | 0.4866 | 0.2966 | SWE_FULLTIME | Backend Engineering, DevOps, Python |
| 67 | Full Stack Developer (Remote) | RTX | US-CT-REMOTE | 0.4136 | 0.2966 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Python |
| 68 | Sr. Lead Software Engineer | Capital One | Bangalore, In | 0.5497 | 0.2918 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 69 | Revenue Intelligence Engineer | Greenhouse | Anywhere in the United States | 0.6624 | 0.2893 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, TypeScript |
| 70 | Data Engineer | Bonterra | Remote, United States | 0.4054 | 0.2893 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 71 | Data Architect | RTX | Warminster, Wiltshire | 0.4805 | 0.2883 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 72 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5781 | 0.2859 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Cloud Infrastructure |
| 73 | Senior AI Engineer II - Agentic AI | American Express | New York, NY, United States / Sunrise Campus / Charlotte Hybrid-600 Tryon / AEDR Desert Ridge OB4 - Canyon / Palo Alto -Waverley | 0.4929 | 0.2859 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Cloud Infrastructure |
| 74 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5541 | 0.2859 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Cloud Infrastructure |
| 75 | Lead AI Engineer (MLX) | Capital One | New York, NY | 0.5535 | 0.2859 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 76 | Senior Lead Software Engineer | Capital One | McLean, VA | 0.6358 | 0.2858 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 77 | Senior Lead Software Engineer, Full Stack (Global Payment Network) | Capital One | Riverwoods, IL | 0.6053 | 0.2858 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 78 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2858 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 79 | Lead Software Engineer, Full Stack | Capital One | Richmond, VA | 0.53 | 0.2858 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 80 | AWS Data Engineer | Bank of Montreal | Toronto, ON, CAN | 0.4809 | 0.2838 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 81 | Full‑Stack Machine Learning Engineer | LexisNexis Risk Solutions | UK - London (London Wall) | 0.5016 | 0.2838 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, DevOps |
| 82 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5015 | 0.2838 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, AI Systems |
| 83 | Data Engineer | Boeing | CAN - Richmond, Canada | 0.3562 | 0.2838 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 84 | Software Engineer - Core Interfaces | Palantir | New York, NY | 0.5451 | 0.275 | SWE_FULLTIME, FRONTEND_ENGINEER_FULLTIME | — |
| 85 | Data Engineer | The Coca-Cola Company | US - GA - Atlanta | 0.5331 | 0.2749 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 86 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4755 | 0.2749 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, SQL |
| 87 | Data Engineer II | American Express | Phoenix, AZ, United States | 0.4632 | 0.2749 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 88 | 2026 Raytheon Full Time - Software Engineer I - Tucson, AZ (Hybrid) | RTX | US-AZ-TUCSON-M10 ~ 3360 E Hemisphere Loop ~ BLDG M10 | 0.3242 | 0.2749 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 89 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5114 | 0.2739 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, DevOps |
| 90 | Software Engineer 2 | Berkshire Hathaway Energy | Des Moines, IA, United States | 0.4628 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development |
| 91 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Backend Engineering |
| 92 | Software Engineer, Low Latency Computing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 93 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Redmond, WA | 0.4574 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 94 | Software Engineer, High Performance Computing (Starlink) | SpaceX | Palo Alto, CA | 0.4864 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 95 | Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 96 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.4853 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 97 | Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.4764 | 0.2739 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 98 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7513 | 0.2723 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 99 | Software Engineer ll - Java 8 Reactjs Web Search Team | American Express | Phoenix, AZ, United States | 0.5327 | 0.2722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 100 | Software Engineer II, Mission Interface | Torc Robotics | Ann Arbor, MI | 0.6096 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 101 | Machine Learning Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6284 | 0.2666 | ML_ENGINEER_FULLTIME | AI Systems, Data Engineering, Python |
| 102 | Software Engineer, II - Operating System | Torc Robotics | Ann Arbor, MI | 0.5603 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 103 | (Remote) System Analyst/Software Developer | Harris Computer | Office - Blair | 0.3286 | 0.2666 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 104 | Software Engineer II, AI Platform | Cadence Design Systems | SAN JOSE | 0.4236 | 0.2666 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Python |
| 105 | Software Engineer, II - Release Pipelines | Torc Robotics | Ann Arbor, MI | 0.4439 | 0.2666 | SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 106 | Success Architect (Agentforce / Data Cloud) | Salesforce | Indiana - Indianapolis | 0.5675 | 0.2621 | SOLUTIONS_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, AI Systems, Python |
| 107 | GTM Engineer | Greenhouse | British Columbia | 0.4751 | 0.2621 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Data Engineering, TypeScript |
| 108 | Développeur de logiciel | Harris Computer | Quebec, Canada | 0.3817 | 0.2611 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 109 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2592 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 110 | Senior Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.6085 | 0.2592 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Python |
| 111 | Lead AI Engineer (AI Foundations, LLM Core and Agentic AI) | Capital One | New York, NY | 0.5652 | 0.2592 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 112 | Lead Software Engineer | Capital One | McLean, VA | 0.628 | 0.2592 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Distributed Systems |
| 113 | Lead Software Engineer | Capital One | McLean, VA | 0.6279 | 0.2592 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 114 | Lead Software Engineer | Capital One | McLean, VA | 0.5711 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 115 | Lead Software Engineer (Java, Golang, AWS) | Capital One | Plano, TX | 0.5413 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 116 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5771 | 0.2592 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 117 | Lead Software Engineer, Full Stack (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.5497 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 118 | Lead Software Engineer, Full Stack | Capital One | Riverwoods, IL | 0.5221 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 119 | Lead Software Engineer, Full Stack (Golang, Angular, AWS) | Capital One | Richmond, VA | 0.5221 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 120 | Lead Software Engineer , Backend | Capital One | Plano, TX | 0.5214 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 121 | Lead Software Engineer, Full Stack | Capital One | McLean, VA | 0.5175 | 0.2592 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 122 | Lead Software Engineer, Back End | Capital One | Plano, TX | 0.4981 | 0.2592 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 123 | Sr Software Engineer I - Java - International Card Risk Services Technology | American Express | Phoenix, AZ, United States | 0.5514 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 124 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 125 | Senior Software Engineer, Full Stack (API Gateway) (Cloud Operations Resilience Engineering) | Capital One | Riverwoods, IL | 0.4859 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 126 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4755 | 0.2586 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Distributed Systems |
| 127 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, AI Systems |
| 128 | Lead Software Engineer, Messaging Dispatch | Capital One | McLean, VA | 0.5774 | 0.2586 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, AI Systems |
| 129 | ML Engineer, I - App Engine | Torc Robotics | Ann Arbor, MI, Fort Worth, TX | 0.6387 | 0.2522 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Python |
| 130 | Foundry PDK / Collateral Integration Engineer (CAD/EDA) | Micron Technology | Richardson, TX | 0.5797 | 0.2522 | SWE_FULLTIME | Backend Engineering, Python |
| 131 | Embedded Software Engineer - Electrification | General Motors | Milford, Michigan, United States of America | 0.5495 | 0.2522 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 132 | Machine Learning Engineer  | Mariana Minerals | Ann Arbor, MI / San Francisco HQ / Houston, TX | 0.4877 | 0.2522 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 133 | Entry Level Software Engineer - Austin, TX | Cox | Austin TX | 0.3807 | 0.2522 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 134 | Software Engineering SMTS - Cloud Reliability | Salesforce | New York - New York | 0.5809 | 0.2483 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps, Distributed Systems |
| 135 | Lead Software Engineer | Cox | Austin TX | 0.499 | 0.2462 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, React |
| 136 | Sr. Lead Machine Learning Engineer | Capital One | New York, NY | 0.7801 | 0.2456 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 137 | Senior Quality & Automation Engineer  | Kira | New York | 0.52 | 0.2456 | SWE_FULLTIME | Backend Engineering, DevOps, Python |
| 138 | Sr Software Engineer - 20198 | Cox | Atlanta GA | 0.4833 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 139 | Lead Software Engineer, DevOps | Capital One | Riverwoods, IL | 0.5721 | 0.2455 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Distributed Systems |
| 140 | Lead Software Engineer, Back End (Cloud Operations Resilience Engineering) | Capital One | Plano, TX | 0.5711 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 141 | Lead Software Engineer | Capital One | McLean, VA | 0.5586 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 142 | Lead Software Engineer (Python, Kubernetes) | Capital One | McLean, VA | 0.5497 | 0.2455 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 143 | AI Automation Engineer, Security | NVIDIA | US, CA, Santa Clara | 0.7611 | 0.2449 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, DevOps |
| 144 | Senior Software Engineer | Cox | Atlanta GA | 0.5311 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 145 | Software Engineer I | LexisNexis Risk Solutions | Colorado | 0.4234 | 0.2449 | SWE_FULLTIME | Backend Engineering, Java, SQL |
| 146 | Systems Engineer - US Remote | Motorola Solutions | Illinois Remote Work | 0.429 | 0.2449 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python, SQL |
| 147 | Appian Product Engineer  | Appian | McLean, Virginia | 0.4941 | 0.2449 | SWE_FULLTIME | Full Stack Development, SQL, Java |
| 148 | AI Prompt Engineer | CACI | Remote (Any State) | 0.322 | 0.2449 | ML_ENGINEER_FULLTIME | AI Systems, Python, TypeScript |
| 149 | R&D AI Platform Engineer / Administrator | Ciena | Ottawa | 0.4191 | 0.2439 | BACKEND_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Cloud Infrastructure, DevOps |
| 150 | Platform Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.4752 | 0.2406 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 151 | Machine Learning Engineer, Asia | Manulife Financial | Manulife Tower, Manulife (Singapore) Pte Ltd | 0.5328 | 0.2393 | ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 152 | GTM Engineer | Greenhouse | Ontario | 0.4752 | 0.2393 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, TypeScript |
| 153 | Analytics Engineer | Pebl | Toronto, Ontario | 0.4525 | 0.2393 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, SQL |
| 154 | Lead AI Engineer (Vision model customization, VML) | Capital One | New York, NY | 0.6718 | 0.2326 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python, Go |
| 155 | Senior Lead AI Engineer, Gen AI Platform | Capital One | New York, NY | 0.6809 | 0.2326 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, Go |
| 156 | Lead AI Engineer (Vision model customization, VLM) | Capital One | New York, NY | 0.5932 | 0.2326 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python, Go |
| 157 | Lead AI Engineer (MLX, Agentic AI, Gen AI platform Services) | Capital One | New York, NY | 0.5922 | 0.2326 | ML_ENGINEER_FULLTIME | AI Systems, Python, Go |
| 158 | Sr Software Engineer II - Technology Research and Development | American Express | New York, NY, United States / AEDR Desert Ridge OB2-McDowell | 0.4754 | 0.232 | SWE_FULLTIME, RESEARCH_SCIENTIST_FULLTIME | AI Systems, Research, Python |
| 159 | Senior Lead Data Engineer (Enterprise Platform Technology) (Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7512 | 0.2319 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 160 | Senior Lead AI Engineer (GenAI Platform Services) | Capital One | San Jose, CA | 0.7497 | 0.2319 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Distributed Systems, Cloud Infrastructure |
| 161 | Lead Data Engineer (Enterprise Platforms Technology) ( Java, Python, Scala, AWS) | Capital One | McLean, VA | 0.7257 | 0.2319 | DATA_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 162 | Lead Data Engineer (Python, AWS, SQL, GenAI) (Enterprise Platforms Technology) | Capital One | McLean, VA | 0.6947 | 0.2319 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 163 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6645 | 0.2319 | DATA_ENGINEER_FULLTIME, SWE_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 164 | Software Engineers | American Express | Phoenix, AZ, United States | 0.4632 | 0.2319 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 165 | Lead Data Engineer - Payment Networks | Capital One | McLean, VA | 0.5346 | 0.2319 | DATA_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 166 | Lead Data Engineer - Nexus Data Products | Capital One | McLean, VA | 0.534 | 0.2319 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 167 | Sr. Software Engineer, Telemetry (Starlink) | SpaceX | Hawthorne, CA | 0.6232 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Distributed Systems |
| 168 | Senior Software Engineer  - Observability and Reliability | Sigma Computing | San Francisco, CA | 0.5856 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 169 | Sr Software Engineer - 20197 | Cox | Atlanta GA | 0.3892 | 0.2313 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 170 | Forward Deployed Engineer I/II | Giga AI | San Francisco | 0.5602 | 0.2305 | SOLUTIONS_ENGINEER_FULLTIME, SWE_FULLTIME | React, Python |
| 171 | CAD Engineer | Micron Technology | Richardson, TX | 0.5796 | 0.2305 | SWE_FULLTIME | Python, Java |
| 172 | Forward Deployed Engineer  | Loop | San Francisco, CA | 0.4398 | 0.2305 | SWE_FULLTIME | Python, SQL |
| 173 | Test System Automation Software Engineer II - LabVIEW/TestStand | Medtronic | Tempe, Arizona, United States of America | 0.5109 | 0.2294 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 174 | Software Engineer I | LivaNova | Houston, Texas, United States | 0.4256 | 0.2294 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | Backend Engineering |
| 175 | Machine Learning Engineer, LLM Post-Training | NewsBreak | Mountain View, California, United States | 0.599 | 0.2294 | ML_ENGINEER_FULLTIME | AI Systems |
| 176 | 2026 Raytheon Full Time-Software Engineer I – EOIR Advanced Products and Solutions (Onsite) | RTX | US-TX-MCKINNEY-513WC ~ 2501 W University Dr ~ WING C BLDG | 0.3632 | 0.2294 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 177 | Software Engineer (Contract, Argentina) | Greenhouse | Argentina | 0.5111 | 0.2275 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, AI Systems |
| 178 | Sr. Software Development Engineer | iHerb | United States of America - Remote / Home Office | 0.5378 | 0.2269 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 179 | Senior Software Engineer I | American Express | Gurugram, HR, India | 0.4631 | 0.2236 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Distributed Systems |
| 180 | Software Engineer II - AI Focused | Cadence Design Systems | BELO HORIZONTE | 0.549 | 0.2222 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Python |
| 181 | Software Engineer II | Torc Robotics | Ann Arbor, MI | 0.5825 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 182 | Machine Learning Engineer I | PROS Holdings, Inc. | BGR Sofia Hybrid | 0.5256 | 0.2222 | ML_ENGINEER_FULLTIME | Data Engineering, Python |
| 183 | EA-Data Engineer 1, Data Services | Bonterra | Remote, United States | 0.3216 | 0.2222 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL |
| 184 | Firmware Engineer Data Center Solid State Drives | Micron Technology | Arzano (NA), Italy | 0.3054 | 0.2222 | SWE_FULLTIME | Backend Engineering, Python |
| 185 | ML Engineer, II - Learned Behaviors | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.5616 | 0.2222 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 186 | Aeroderivative Performance Engineer - Field | GE Vernova | Greenville | 0.3469 | 0.2222 | SWE_FULLTIME | Data Engineering, Python |
| 187 | Quality Assurance Engineer PON / DCOM | Ciena | Ottawa | 0.286 | 0.2222 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 188 | Software Engineer - Compiler  | Sigma Computing | New York City, NY | 0.58 | 0.2216 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, TypeScript |
| 189 | Senior Software Engineer - Fullstack | Sigma Computing | New York City, NY | 0.5856 | 0.2216 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Go |
| 190 | Senior Failure Analysis Engineer | NVIDIA | US, CA, Santa Clara | 0.6616 | 0.2183 | BACKEND_ENGINEER_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 191 | Data Migration Architect (Senior or Lead) | Boeing | USA - Hazelwood, MO | 0.6256 | 0.2183 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 192 | Lead Data Engineer | Capital One | San Francisco,  CA | 0.6873 | 0.2183 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Distributed Systems |
| 193 | Senior Software Engineer - Fullstack | Sigma Computing | San Francisco, CA | 0.5665 | 0.2183 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Distributed Systems, Cloud Infrastructure |
| 194 | Solutions Architect | Centerfield | Los Angeles, California | 0.4688 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, Full Stack Development |
| 195 | Sr. Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6548 | 0.2183 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Cloud Infrastructure |
| 196 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6548 | 0.2183 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Distributed Systems |
| 197 | Senior Software Engineer | Cox | Atlanta GA | 0.4445 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 198 | Sr Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6252 | 0.2183 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Cloud Infrastructure, DevOps |
| 199 | Lead Machine Learning Engineer | Capital One | McLean, VA | 0.5586 | 0.2183 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 200 | Senior Machine Learning Engineer (AI Foundations) | Capital One | McLean, VA | 0.5022 | 0.2183 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 201 | Data Engineer (12 month Fixed term Contract) | Sony Interactive Entertainment | United Kingdom, London | 0.5128 | 0.2176 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 202 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.525 | 0.2176 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 203 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.2176 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 204 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 205 | Software Development Engineer | Micron Technology | Taoyuan - Fab 11, Taiwan | 0.5003 | 0.2176 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 206 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 207 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 208 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 209 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4813 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 210 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4812 | 0.2176 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 211 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 212 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.2176 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 213 | Senior Software Developer / HR Technology & Shared Services / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Developer / HR Technology & Shared Services / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.2139 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 214 | Software Engineering Architect | Salesforce | Norway - Remote | 0.5793 | 0.2133 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Data Engineering |
| 215 | Senior Software Engineer - Full Stack | Capital One | Mexico City, Mexico | 0.4619 | 0.2112 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 216 | Lead Software Developer - Java FullStack | Boeing | IND - Bangalore, India | 0.4198 | 0.2112 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 217 | Senior Frontier Agents Engineer | ScaleAI | San Francisco, CA; New York, NY | 0.7489 | 0.208 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 218 | Software Engineer, Agents  | Mirage | Union Square, New York City | 0.5078 | 0.208 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 219 | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire | Susquehanna International Group (SIG) | Senior Software Engineer – AI Tools / Data Engineering / Experienced Hire in New York, New York / Careers at SIG | 0.6962 | 0.208 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 220 | Software Engineer - Compiler  | Sigma Computing | San Francisco, CA | 0.5799 | 0.2052 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, TypeScript |
| 221 | Senior AI Engineer I | American Express | Phoenix, AZ, United States / New York-Amex Tower WFC-35 Hr | 0.4632 | 0.2052 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Python |
| 222 | Senior Lead AI Engineer,(MLX, Agentic AI, Gen AI platform Services) | Capital One | San Jose, CA | 0.6325 | 0.2052 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 223 | Lead AI Engineer (AI Foundations, LLM Customization and Finetuning) | Capital One | Cambridge, MA | 0.5782 | 0.2052 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Backend Engineering, Python |
| 224 | Senior Lead AI Engineer (Gen AI Platform Services) | Capital One | San Jose, CA | 0.6085 | 0.2052 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 225 | Senior Inference Engineer, AIConfigurator for Dynamo | NVIDIA | US, CA, Santa Clara | 0.7794 | 0.2046 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 226 | Senior Software Engineer NAVAIR Product Line | CACI | Austin, TX, US | 0.5443 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 227 | Sr Software Engineer | Cox | Atlanta GA | 0.4437 | 0.2046 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Distributed Systems |
| 228 | Lead Data Engineer | Capital One | Wilmington, DE | 0.7087 | 0.2003 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, Distributed Systems |
| 229 | Sr. Data Engineer I | iHerb | United States of America - Remote / Home Office | 0.5426 | 0.2003 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 230 | Senior Software Engineer, Full-Stack — Content Tools | Epic Kids | Bangalore, India (remote within India) | 0.4626 | 0.2003 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Cloud Infrastructure |
| 231 | Senior Data Engineer (AWS, Databricks) | Travelers | CT - Hartford | 0.508 | 0.2003 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, DevOps |
| 232 | M365 Developer | CACI | Remote (Any State) | 0.4972 | 0.1994 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development |
| 233 | Engineer Software T1/T2 | Northrop Grumman | GAWR03GC | 0.3461 | 0.1994 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 234 | Software Engineer II | Cadence Design Systems | SAN JOSE | 0.4196 | 0.1994 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 235 | Sr Advanced Software Engineer | Honeywell | Bengaluru, Karnataka, India | 0.4323 | 0.1969 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 236 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.1969 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 237 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5244 | 0.1949 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 238 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5176 | 0.1949 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 239 | Software Engr I | Honeywell | Pune, Maharashtra, India | 0.5005 | 0.1949 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 240 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4633 | 0.1949 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 241 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4632 | 0.1949 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 242 | Software Development Engineer in Test | Medtronic | London, London, United Kingdom | 0.3251 | 0.1949 | SWE_FULLTIME | DevOps, Python, Java |
| 243 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in New York, New York / Careers at SIG | 0.72 | 0.1943 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 244 | ML Engineer, II - App Engine | Torc Robotics | Ann Arbor, MI, Montreal, Canada | 0.4928 | 0.1939 | SWE_FULLTIME | Backend Engineering, Distributed Systems |
| 245 | Senior ML Ops Engineer | RELX | Philadelphia, PA | 0.5653 | 0.1916 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Python |
| 246 | Automation Data Information Administrator | CACI | Washington, DC, US | 0.5686 | 0.1916 | DATA_ENGINEER_FULLTIME | Data Engineering, DevOps, Python |
| 247 | Sr. Automation Engineer (Starlink Customer Success) | SpaceX | Bastrop, TX | 0.4731 | 0.1916 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Cloud Infrastructure, Data Engineering, Python |
| 248 | Sr. Lead Machine Learning Engineer | Capital One | McLean, VA | 0.6544 | 0.1916 | ML_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Python |
| 249 | Digital Transformation Manufacturing Engineer 2/3 | Northrop Grumman | United States-California-Northridge | 0.4318 | 0.1916 | SWE_FULLTIME | DevOps, Data Engineering, Python |
| 250 | Lead Machine Learning Engineer | Capital One | Cambridge, MA | 0.5286 | 0.1916 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Distributed Systems, Python |
| 251 | Software Engineer III - Managed File Transfer - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4469 | 0.191 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Cloud Infrastructure |
| 252 | Senior Salesforce Solution Architect | Boeing | USA - Renton, WA | 0.4865 | 0.191 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 253 | Senior Gen AI Developer | KBR | El Segundo, California | 0.6387 | 0.1866 | SWE_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, DevOps |
| 254 | Senior Data Engineer, Underwriting Technical Lead | Travelers | CT - Hartford | 0.508 | 0.1866 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, AI Systems |
| 255 | Sr. QA Engineer - IP Routing | Ciena | Remote-Canada | 0.4707 | 0.1866 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, DevOps |
| 256 | Sr Full Stack Developer, TD Securities | TD Bank | Toronto, Ontario | 0.5025 | 0.1845 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, React |
| 257 | Experienced Software Engineer | Boeing | IND - Bangalore, India | 0.4632 | 0.1839 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, DevOps |
| 258 | Senior AI/ML Engineer | Sigma Computing | New York City, NY | 0.6784 | 0.1813 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 259 | Partner Operations Senior Engineer  | Sigma Computing | San Francisco, CA | 0.4897 | 0.1786 | DATA_ENGINEER_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Data Engineering, SQL, React |
| 260 | Lead Artificial Intelligence /Machine Learning Data Scientist (Data Science) | Boeing | USA - Seattle, WA | 0.6813 | 0.1786 | DATA_SCIENTIST_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Python, Java |
| 261 | Lead Software/Controls Engineer | GE Vernova | Wilmington NC USA | 0.4187 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Python |
| 262 | Senior Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4327 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 263 | Sr Solutions Architect II - Enterprise Architecture | American Express | Phoenix, AZ, United States | 0.4318 | 0.178 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 264 | ENGINEER, FW & PRODUCT TEST ENGINEERING | Micron Technology | Arzano (NA), Italy | 0.3292 | 0.1777 | SWE_FULLTIME | Python |
| 265 | Ingénieur·e en apprentissage automatique, II | Torc Robotics | Remote - US, Ann Arbor, MI,  Montreal, Canada, Remote - Canada | 0.4953 | 0.1777 | ML_ENGINEER_FULLTIME | Python |
| 266 | Senior Business Systems Analyst | EarnIn | Mexico City, Mexico; Remote, Mexico | 0.6073 | 0.1736 | BACKEND_ENGINEER_FULLTIME, DATA_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Python |
| 267 | Senior Software Engineer | GE Vernova | Bucharest | 0.5514 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 268 | Architect - Personal Insurance Cross-Domain Architecture | Travelers | CT - Hartford | 0.5447 | 0.1736 | SWE_FULLTIME | Cloud Infrastructure, AI Systems, Python |
| 269 | Senior Software Engineer II | LexisNexis Risk Solutions | Texas | 0.4278 | 0.1736 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 270 | Senior Autonomy Data Engineer | Torc Robotics | Remote - US, Blacksburg, VA  | 0.5155 | 0.1736 | DATA_ENGINEER_FULLTIME | Data Engineering, Cloud Infrastructure, Python |
| 271 | Oracle EPM Integration Lead | CACI | Remote (Any State) | 0.4128 | 0.1736 | DATA_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, SQL |
| 272 | Lead Engineer 1 - Customer Application Engineering | GE Vernova | Schenectady | 0.4052 | 0.1736 | SWE_FULLTIME, DATA_ENGINEER_FULLTIME | Data Engineering, Backend Engineering, SQL |
| 273 | Software Engr I | Honeywell | Hyderabad, Telangana, India | 0.4632 | 0.1732 | SWE_FULLTIME | Java, Python, SQL |
| 274 | Associate Software Engineer - Analytics | Boeing | IND - Bangalore, India | 0.5019 | 0.1722 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 275 | Cyber Sec Archt/Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5004 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 276 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 277 | IT Developer | Medtronic | Nanakramguda, Hyderabad, India | 0.4813 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 278 | Ingénieur·e en apprentissage automatique, II – App Engine | Torc Robotics | Montreal, Canada, Ann Arbor, MI | 0.448 | 0.1722 | ML_ENGINEER_FULLTIME | Distributed Systems, Python |
| 279 | Associate ATE Software Engineer | Boeing | IND - Bangalore, India | 0.4469 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 280 | Associate Software Engineer - Full Stack | Boeing | IND - Bangalore, India | 0.4327 | 0.1722 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, React |
| 281 | Application Engr II | Honeywell | Tianjin, China | 0.4316 | 0.1722 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 282 | IT SOFTWARE ENGINEER | Micron Technology | Fab 10W, Singapore | 0.4194 | 0.1722 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, SQL |
| 283 | SMTS, Software Engineering (Salesforce Expert) | Salesforce | India - Hyderabad | 0.5494 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Full Stack Development, Cloud Infrastructure, Backend Engineering |
| 284 | Senior Machine Learning Engineer | EarnIn | Bengaluru, India | 0.4591 | 0.1703 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, DevOps |
| 285 | Sr IT Architect | Honeywell | Pune, Maharashtra, India | 0.4327 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, AI Systems, Cloud Infrastructure |
| 286 | Sr IT Architect | Honeywell | Bengaluru, Karnataka, India | 0.4316 | 0.1703 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 287 | Sr Software Engineer | GE Vernova | Bengaluru | 0.4086 | 0.1703 | SWE_FULLTIME, FULLSTACK_ENGINEER_FULLTIME | Full Stack Development, Backend Engineering, Distributed Systems |
| 288 | Senior Cyber Security Engineer – Security Services | General Motors | Warren, Michigan, United States of America | 0.5495 | 0.1649 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | Backend Engineering, Python, Java |
| 289 | Sr. Data Engineer  | Mariana Minerals | Ann Arbor, MI / Houston, TX / San Francisco HQ | 0.4691 | 0.1649 | DATA_ENGINEER_FULLTIME | Data Engineering, Python, SQL |
| 290 | Senior AI/ML Engineer | Sigma Computing | San Francisco, CA | 0.6783 | 0.1649 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python, SQL |
| 291 | Lead DevOps Developer | Boeing | USA - Long Beach, CA | 0.5052 | 0.1643 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure |
| 292 | Sr. Software Engineer, Beam Planning (Starlink)    | SpaceX | Redmond, WA | 0.5479 | 0.1643 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 293 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Palo Alto, CA | 0.5769 | 0.1643 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 294 | Sr. Embedded Software Engineer, Laser Mesh Routing (Starlink)    | SpaceX | Redmond, WA | 0.5758 | 0.1643 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Distributed Systems, Backend Engineering |
| 295 | Senior Domain Architect | Boeing | USA - Seattle, WA | 0.4696 | 0.1643 | SWE_FULLTIME | Cloud Infrastructure, Backend Engineering |
| 296 | Senior Software Engineer - New AI Initiatives | Torc Robotics | Remote - US | 0.6489 | 0.16 | ML_ENGINEER_FULLTIME | AI Systems, Data Engineering, Python |
| 297 | AI Security Architect | Cadence Design Systems | SAN JOSE | 0.696 | 0.16 | SECURITY_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, Python |
| 298 | Software Engineer II-Team Lead (AWS, Typescript) | Travelers | CT - Hartford | 0.5281 | 0.16 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, TypeScript |
| 299 | Software Developer (Mid Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.16 | BACKEND_ENGINEER_FULLTIME, SWE_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 300 | Software Engineer Developer ( Mid-Level or Senior) (Virtual) | Boeing | United States - Remote | 0.4795 | 0.16 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 301 | Senior Software Engineer - Fullstack (SaaS product/Payroll) | EarnIn | Bangkok, Thailand | 0.4587 | 0.1572 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Go |
| 302 | Experienced Software Developer - Java | Boeing | IND - Bangalore, India | 0.4198 | 0.1572 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Java |
| 303 | Sr IT Engineer | Honeywell | Bengaluru, Karnataka, India | 0.5021 | 0.1566 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Cloud Infrastructure, DevOps |
| 304 | Sr. Product Solution Analyst, TD Securities | TD Bank | Toronto, Ontario | 0.4116 | 0.1566 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Data Engineering, Cloud Infrastructure |
| 305 | Senior Network Engineer | NOV | Kochi, Kerala, India | 0.4802 | 0.1566 | SWE_FULLTIME, DEVOPS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, DevOps |
| 306 | Senior Signal Processing Engineer | Whoop | Boston, MA | 0.5929 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 307 | Senior Embedded Software Engineer | Micron Technology | San Jose, CA | 0.7214 | 0.1513 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 308 | Advanced Software Engr | Honeywell | Hamilton Township, NJ, United States | 0.462 | 0.1513 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java |
| 309 | Sr. Data Engineer (Starlink Network Analytics, Wi-Fi)  | SpaceX | Redmond, WA | 0.5885 | 0.1513 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Python |
| 310 | Senior AI Engineer - Generative AI Research & Development - Technology R&D | American Express | Palo Alto, CA, United States | 0.4327 | 0.1513 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 311 | Associate-Digital Product Management | American Express | Gurugram, HR, India | 0.5514 | 0.1505 | DATA_ANALYST_FULLTIME, ML_ENGINEER_FULLTIME | Python, SQL |
| 312 | QE PCT Engineer | Micron Technology | Miaoli - Tongluo, Taiwan | 0.4235 | 0.1505 | SWE_FULLTIME | Python, SQL |
| 313 | Audio Programmer | Sony Interactive Entertainment | United Kingdom, London | 0.5209 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 314 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 315 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.5175 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 316 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4753 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 317 | Software Engr I | Honeywell | Bengaluru, Karnataka, India | 0.4633 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 318 | Cloud Developer I | Honeywell | Bengaluru, Karnataka, India | 0.4516 | 0.1494 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Cloud Infrastructure |
| 319 | Software Developer, Mobile Platform | MaintainX | Toronto, Ontario | 0.4543 | 0.1494 | SWE_FULLTIME, MOBILE_ENGINEER_FULLTIME | DevOps |
| 320 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4086 | 0.1494 | SWE_FULLTIME | Backend Engineering |
| 321 | Senior Commercial Data & Insights Engineer | Dexcom | Remote - Spain | 0.5496 | 0.1469 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Python |
| 322 | Senior ABAP Developer | CACI | Remote (Any State) | 0.3919 | 0.1469 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, SQL |
| 323 | Sr Embedded Software Engineer | Dexcom | San Diego, California | 0.5218 | 0.1463 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 324 | Lead Protection and Control Engineer | GE Vernova | Remote | 0.4757 | 0.1463 | SWE_FULLTIME, SYSTEMS_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure |
| 325 | Senior C++ Developer / Trading Infrastructure / Experienced Hire | Susquehanna International Group (SIG) | Senior C++ Developer / Trading Infrastructure / Experienced Hire in Bala Cynwyd (Philadelphia Area), Pennsylvania / Careers at SIG | 0.52 | 0.1463 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 326 | Senior Software Engineer | EarnIn | Mexico City, Mexico | 0.643 | 0.1436 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Python |
| 327 | Senior Software Developer – Virtualization, SIL, and AI‑Enablement | General Motors | Markham, Ontario, Canada | 0.5397 | 0.1436 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Python |
| 328 | IT Developer (Java), TD Securities | TD Bank | Toronto, Ontario | 0.3363 | 0.1436 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems, Java |
| 329 | Lead Software Engr | Honeywell | Hyderabad, Telangana, India | 0.4327 | 0.143 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Cloud Infrastructure, Distributed Systems |
| 330 | .NET/C# Engineer, TD Securities | TD Bank | Toronto, Ontario | 0.3795 | 0.143 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, Cloud Infrastructure |
| 331 | Product Architect | Monster Energy | USA - Corona, CA | 0.5401 | 0.1377 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 332 | Senior Software Engineer - C++/UI | General Motors | Mountain View, California, United States of America | 0.5715 | 0.1377 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 333 | Senior Data Engineer | Reply | Atlanta, GA / Kansas City, MO / Philadelphia, PA | 0.5327 | 0.1377 | DATA_ENGINEER_FULLTIME | Data Engineering |
| 334 | Engineer I/Engineer II/Sr. Engineer/Sr Engineer II | Berkshire Hathaway Energy | Bridgeport, WV, United States | 0.4631 | 0.1377 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 335 | Engineering Technical Lead - I&C Embedded Software | GE Vernova | Wilmington NC USA | 0.3946 | 0.1377 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 336 | Senior Software Engineer | Cadence Design Systems | SAN JOSE | 0.6448 | 0.1333 | ML_ENGINEER_FULLTIME, BACKEND_ENGINEER_FULLTIME | AI Systems, Python |
| 337 | Senior Advanced Application Engineer - APM | Honeywell | Asker, Viken, Norway | 0.4754 | 0.1333 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 338 | Senior, Machine Learning Engineer - End-to-End | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6359 | 0.1333 | ML_ENGINEER_FULLTIME, SWE_FULLTIME | AI Systems, Python |
| 339 | Senior Machine Learning Engineer - Learned Planning/Reinforcement Learning | Torc Robotics | Remote - U.S, Ann Arbor, MI | 0.6622 | 0.1333 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 340 | Data Integration and Analytics Developer | Boeing | United States - Remote | 0.5223 | 0.1333 | DATA_ENGINEER_FULLTIME | Data Engineering, PostgreSQL, ETL |
| 341 | Sr. Electricity Market Optimization Software Engineer | GE Vernova | Bellevue | 0.448 | 0.1333 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Python |
| 342 | Advanced Data Engineer - PIM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4192 | 0.1306 | DATA_ENGINEER_FULLTIME, ML_ENGINEER_FULLTIME | Data Engineering, Java, Python |
| 343 | Senior Software Developer – DevOps | General Motors | Markham, Ontario, Canada | 0.5412 | 0.13 | DEVOPS_ENGINEER_FULLTIME, SWE_FULLTIME | DevOps, Cloud Infrastructure, Python |
| 344 | Experienced Software Application Development – QA and Test Automation Engineer | Boeing | IND - Bangalore, India | 0.5019 | 0.13 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps, Java |
| 345 | Senior Software Engineer II - JavaScript, React, Node.JS & graphQL | American Express | Chennai, TN, India | 0.4632 | 0.13 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Full Stack Development, React |
| 346 | Package Device Product Engineer (PDPE) Engineer | Micron Technology | Sanand - 303A - AT/SSD/MOD, India | 0.5796 | 0.1277 | SWE_FULLTIME | Python |
| 347 | Sr Software Test Engineer | Medtronic | Lafayette, Colorado, United States of America | 0.4509 | 0.1246 | SWE_FULLTIME | Python |
| 348 | Senior Process Engineer (Oil and Gas, EPC, Midstream) | NOV | Dubai, Dubai, United Arab Emirates | 0.4463 | 0.1197 | SWE_FULLTIME | Backend Engineering |
| 349 | Senior Engineer, Advanced Modeling & AI Solutions | Micron Technology | Boise, ID - Main Site | 0.4079 | 0.1197 | ML_ENGINEER_FULLTIME | AI Systems |
| 350 | Software Engineering MTS - Compliance Automation & Tooling (Apex, Python) | Salesforce | India - Hyderabad | 0.5792 | 0.1169 | SWE_FULLTIME | Backend Engineering, Python, SQL |
| 351 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.5494 | 0.1169 | SWE_FULLTIME | Backend Engineering, Java, Python |
| 352 | Senior Reliability Software Engineer | Medtronic | Galway, County Galway, Ireland | 0.4294 | 0.1169 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 353 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.5001 | 0.1169 | SWE_FULLTIME | Backend Engineering, Python, Java |
| 354 | Advanced Data Analyst -MDM Developer | Honeywell | Bengaluru, Karnataka, India | 0.4874 | 0.1169 | DATA_ENGINEER_FULLTIME | Data Engineering, SQL, Java |
| 355 | Software Engineering, SMTS (Salesforce Developer) | Salesforce | India - Hyderabad | 0.4755 | 0.1169 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Java, Python |
| 356 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, London | 0.5744 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps |
| 357 | Senior Software Engineer | Sony Interactive Entertainment | United Kingdom, Liverpool | 0.5759 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, DevOps |
| 358 | Simulation Software Engineer (Experienced or Senior level) | Boeing | GBR - Crawley, UK | 0.5019 | 0.1163 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering, Distributed Systems |
| 359 | Lead Software Engineer, Android (Kotlin & Jetpack Compose) | Capital One | McLean, VA | 0.5778 | 0.111 | MOBILE_ENGINEER_FULLTIME, SWE_FULLTIME | — |
| 360 | Software Engineer, Security | Notion | San Francisco, California | 0.7173 | 0.111 | SWE_FULLTIME, SECURITY_ENGINEER_FULLTIME | — |
| 361 | Senior Technical Designer | Sony Interactive Entertainment | United States, Santa Monica, CA | 0.4603 | 0.111 | SWE_FULLTIME | — |
| 362 | Software Engr II | Honeywell | Bengaluru, Karnataka, India | 0.4197 | 0.105 | SWE_FULLTIME | — |
| 363 | Quality Engineer Lead | LexisNexis Risk Solutions | Mumbai | 0.5798 | 0.1033 | SWE_FULLTIME | DevOps, TypeScript |
| 364 | Experienced AI-ML Engineer (Artificial Intelligence) | Boeing | IND - Bangalore, India | 0.4813 | 0.1033 | ML_ENGINEER_FULLTIME | AI Systems, Python |
| 365 | Advanced Software Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.0903 | SWE_FULLTIME | Java, SQL |
| 366 | Senior Discipline Engineer - Software Requirements | Valeo | Chennai | 0.5507 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 367 | Advanced Cyber Sec Archt/Engr | Honeywell | Bengaluru, Karnataka, India | 0.4813 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 368 | Sr IT Analyst | Honeywell | Bengaluru, Karnataka, India | 0.4619 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 369 | Senior Associate  - MDG Technical Development | RTX | IN-KA-BENGALURU-NORTHGATE ~ Sy No 2/2 Venkatala Village ~ SY NO 2/2 VENKATALA VILLAGE, Yelahanka Hobli | 0.4327 | 0.0897 | SWE_FULLTIME, BACKEND_ENGINEER_FULLTIME | Backend Engineering |
| 370 | Senior Discipline Engineer | Valeo | Chennai | 0.5507 | 0.0766 | SWE_FULLTIME | Python |
