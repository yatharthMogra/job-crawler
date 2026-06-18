# YC / Work at a Startup Connector — Integration Guide

## Overview

Y Combinator jobs surface through two distinct layers:

1. **Work at a Startup** (`workatastartup.com`) — YC's own job board where any YC company
   can post roles directly. No public API exists. Content is server-rendered React with
   internal XHR calls. Login is required for full detail.

2. **YC Company Directory** (`ycombinator.com/companies`) — The public list of all funded
   companies, each with a website and metadata (batch, industry, headcount range). Many of
   these companies already use Greenhouse, Lever, Ashby, or Workday — ATSes you already have
   connectors for.

The correct integration strategy uses **both layers**:

- Phase 1 crawls the YC company directory to find companies whose native ATS you already
  support (Greenhouse, Lever, Ashby, Workday) so you can add them to those connectors rather
  than building a parallel ingestion path.
- Phase 2 scrapes Work at a Startup for the remainder — companies that post jobs only through
  the YC board and not through a major ATS.

This prevents duplicate job records and keeps enrichment/scoring consistent with the rest of
your corpus.

---

## Why There Is No Public API

Work at a Startup deliberately blocks machine access. An HN thread in 2023 confirmed YC's
position: programmatic access increases unqualified application volume and disrupts the
signal they're trying to provide to founders. All third-party scrapers on GitHub (waasuapi,
etc.) require Selenium + a real YC account login and break whenever the frontend updates.
There is no official JSON endpoint to call with a key.

This means the connector is **HTML scraping with session cookies**, similar to your existing
iCIMS connector, rather than a REST API integration like Greenhouse or Lever.

---

## Phase 1 — YC Company Directory Crawl

### Purpose

`ycombinator.com/companies` lists every funded company with a public website field. A
significant fraction already use Greenhouse, Lever, or Ashby. For those, you add the company
to the existing connector's company list and let the existing ingestion pipeline handle job
fetching. No new job-fetching code needed.

### Endpoint

The company directory page is server-rendered, but the underlying data is available as a
JSON payload embedded in the page. Inspect the network tab and look for a request to:

```
GET https://api.ycombinator.com/v0.1/companies
```

This returns a paginated list. Observed fields per company:

```json
{
  "id": 12345,
  "name": "Airbnb",
  "slug": "airbnb",
  "website": "https://airbnb.com",
  "one_liner": "Book unique accommodations around the world.",
  "long_description": "...",
  "batch": "W09",
  "status": "Public",
  "industries": ["Travel", "Marketplace"],
  "tags": ["Remote", "B2C"],
  "team_size": 6132,
  "locations": ["San Francisco, CA"],
  "hiring": true
}
```

Pagination is cursor-based via `page` parameter. Fetch until `hiring: false` companies are
no longer returned (or until you've scanned all batches).

### ATS Detection Logic

For each company with `hiring: true`, resolve the ATS by probing the career page:

```python
ATS_FINGERPRINTS = {
    "greenhouse": [
        r"boards\.greenhouse\.io/([^/\"']+)",
        r"job-boards\.greenhouse\.io/([^/\"']+)",
    ],
    "lever": [
        r"jobs\.lever\.co/([^/\"']+)",
    ],
    "ashby": [
        r"jobs\.ashbyhq\.com/([^/\"']+)",
        r"jobs\.ashby\.com/([^/\"']+)",
    ],
    "workday": [
        r"([^.]+)\.wd\d+\.myworkdayjobs\.com",
    ],
}

async def detect_ats(career_url: str) -> tuple[str | None, str | None]:
    """
    Returns (ats_type, identifier) where identifier is the board_token / company slug.
    Returns (None, None) if no known ATS detected.
    """
    html = await fetch_with_redirect_follow(career_url)
    for ats, patterns in ATS_FINGERPRINTS.items():
        for pattern in patterns:
            if m := re.search(pattern, html, re.IGNORECASE):
                return ats, m.group(1)
    return None, None
```

### Output of Phase 1

Two outputs:

```python
@dataclass
class Phase1Result:
    # Companies to add to existing ATS connectors
    add_to_greenhouse: list[str]   # board_tokens
    add_to_lever: list[str]        # company slugs
    add_to_ashby: list[str]        # org slugs
    add_to_workday: list[WorkdayTenant]  # (instance, career_site, tenant)

    # Companies with no known ATS — proceed to Phase 2
    yc_native: list[YCCompany]     # id, name, slug, website
```

The `add_to_*` lists feed directly into the existing connector company tables — no new
ingestion code, just new rows. The `yc_native` list is the input to Phase 2.

### Schedule

Run Phase 1 weekly (Sunday night before the weekly connector crawl). The company directory
doesn't change frequently enough to warrant daily runs.

---

## Phase 2 — Work at a Startup Scraper

### Authentication

Work at a Startup uses session cookies from a standard YC account login. Create a dedicated
service account (`crawler@yourproduct.com`) and register it at `ycombinator.com`. The login
flow is a POST to `https://account.ycombinator.com/` — inspect the form to get the current
CSRF token field name, then:

```python
async def login(client: httpx.AsyncClient, email: str, password: str) -> None:
    # Step 1: get CSRF token from login page
    resp = await client.get("https://www.workatastartup.com/login")
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.find("input", {"name": "_csrf_token"})["value"]

    # Step 2: POST credentials
    resp = await client.post(
        "https://account.ycombinator.com/",
        data={
            "email": email,
            "password": password,
            "_csrf_token": csrf,
        },
        follow_redirects=True,
    )
    if resp.status_code != 200 or "Log out" not in resp.text:
        raise AuthError("YC login failed — check credentials or CSRF field name")
    # Session cookies are now stored in client's cookie jar
```

Store the session in an `httpx.AsyncClient` with `follow_redirects=True` and
`cookies=httpx.Cookies()`. Re-login if a request returns a redirect to the login page
(status 302 → `/login`).

### Job Listing Endpoint

After login, the job list is available by hitting the jobs search page directly. The page
makes an XHR call that you can intercept by inspecting the Network tab → Filter: Fetch/XHR.
The internal endpoint as of the last observed version:

```
GET https://www.workatastartup.com/jobs
    ?q=
    &roles[]=eng        # filter to engineering roles
    &jobType=fulltime
    &offset=0
    &limit=50
```

The response is JSON with this shape:

```json
{
  "jobs": [
    {
      "id": 67890,
      "title": "Senior Backend Engineer",
      "company": {
        "id": 12345,
        "name": "Acme AI",
        "slug": "acme-ai",
        "one_liner": "...",
        "batch": "S24",
        "team_size": 8,
        "locations": ["San Francisco, CA"],
        "remote_ok": true
      },
      "location": "San Francisco, CA",
      "remote": true,
      "visa_sponsorship": false,
      "min_experience_years": 3,
      "job_type": "fulltime",
      "created_at": "2026-06-10T18:00:00Z",
      "description": "<p>We are looking for...</p>",
      "apply_url": "https://www.workatastartup.com/jobs/67890"
    }
  ],
  "total": 420
}
```

**Important**: the `apply_url` points back to `workatastartup.com/jobs/{id}`, not to the
company's own ATS. This is the correct URL to store — do not try to resolve it further,
because YC companies that post natively don't have a separate ATS application page.

### Pagination

Increment `offset` by `limit` (50) until `offset >= total`:

```python
async def fetch_all_jobs(client: httpx.AsyncClient) -> list[dict]:
    all_jobs = []
    offset = 0
    limit = 50
    role_filters = ["eng"]  # add "ds", "pm" if desired

    while True:
        params = {
            "q": "",
            "roles[]": role_filters,
            "jobType": "fulltime",
            "offset": offset,
            "limit": limit,
        }
        resp = await client.get("https://www.workatastartup.com/jobs", params=params)
        if resp.status_code == 302:
            raise SessionExpiredError("Session cookie expired, re-login required")
        data = resp.json()
        all_jobs.extend(data["jobs"])
        offset += limit
        if offset >= data["total"]:
            break
        await asyncio.sleep(1.5)  # be polite

    return all_jobs
```

### Roles to Fetch

The `roles[]` filter accepts:
- `eng` — engineering (backend, frontend, fullstack, ML, devops, mobile, data)
- `ds` — data science / research
- `pm` — product management
- `design` — design

Fetch `eng` and `ds` at minimum. `pm` is optional — add it if you want to cover product
roles. Skip `design`, `finance`, `legal`, `marketing` for now.

---

## Deduplication Against Existing Corpus

This is the most important part of the connector. Many YC companies also post to Greenhouse,
Lever, or Ashby. If you've already ingested a job from Figma via Greenhouse and Figma also
posts it on Work at a Startup, you should NOT create a duplicate record.

### Strategy

Before inserting a job scraped from Work at a Startup, run this check:

```python
async def is_duplicate(session: AsyncSession, job: YCJob) -> bool:
    # Match on (company_name, title, location) normalized fingerprint
    fingerprint = build_fingerprint(
        company=job.company_name,
        title=job.title,
        location=job.location,
    )
    result = await session.execute(
        select(NormalizedJob.id)
        .where(NormalizedJob.dedup_fingerprint == fingerprint)
        .where(NormalizedJob.is_active == True)
        .limit(1)
    )
    return result.scalar_one_or_none() is not None

def build_fingerprint(company: str, title: str, location: str) -> str:
    """
    Normalized fingerprint for dedup. Lowercase, strip punctuation/articles,
    take first 3 words of title, first location token.
    """
    def normalize(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^a-z0-9 ]", " ", s)
        s = re.sub(r"\b(the|a|an|inc|llc|corp|ltd)\b", "", s)
        return re.sub(r"\s+", " ", s).strip()

    co = normalize(company)[:40]
    title_words = normalize(title).split()[:4]
    loc = normalize(location).split(",")[0][:20]
    return f"{co}|{' '.join(title_words)}|{loc}"
```

Add a `dedup_fingerprint` column to `normalized_jobs` if not already present, populated
during enrichment. Without this, you'll get duplicate emails showing the same job twice.

---

## Data Mapping

Work at a Startup → `normalized_jobs` schema:

| WaaS field | Your field | Notes |
|---|---|---|
| `job.id` | `external_id` | Prefix: `"yc_{id}"` |
| `job.title` | `title` | Pass through directly |
| `job.description` (HTML) | `description` | Strip HTML tags |
| `job.company.name` | `company_name` | |
| `job.company.batch` | `company_metadata["yc_batch"]` | Store in JSONB extras |
| `job.company.team_size` | `company_metadata["team_size"]` | |
| `job.location` | `job_location` | |
| `job.remote` | `is_remote` | |
| `job.visa_sponsorship` | `visa_sponsorship` | Boolean — rare to have this structured |
| `job.created_at` | `posted_at` | |
| `job.apply_url` | `job_url` | `workatastartup.com/jobs/{id}` |
| `"YC"` | `source` | New source enum value |
| `job.company.slug` | `company_slug` | For URL and dedup |

**ATS type**: Set `ats_type = "workatastartup"` — a new value in your `ATSType` enum.

---

## Codebase Touch Points

### New files

```
job_ingestion/app/ingestion/connectors/
    workatastartup.py        # The connector class

job_ingestion/app/ingestion/connectors/yc_directory.py  # Phase 1 company crawler
```

### Existing files to modify

**`job_ingestion/app/ingestion/connectors/__init__.py`**
Register `WorkAtAStartupConnector` in the connector registry.

**`job_ingestion/app/ingestion/constants_taxonomy.py`** (or wherever `ATSType` lives)
Add `WORKATASTARTUP = "workatastartup"` to the enum.

**`job_ingestion/app/ingestion/scheduler.py`**
Add two new scheduled jobs:
- `yc_directory_crawl` — weekly, runs first, outputs company lists for existing connectors
- `yc_native_crawl` — daily or every 12 hours, runs the Work at a Startup scraper

**`job_ingestion/app/ingestion/deterministic.py`**
Add logic in `extract_job_country` to handle the `job_location` field format from WaaS
(usually `"City, ST"` or `"Remote"` — similar to Lever format, should already work).

**`normalized_jobs` migration**
Add `dedup_fingerprint VARCHAR(200)` if not present. Populate via backfill script for
existing rows. Add index: `CREATE INDEX idx_dedup ON normalized_jobs (dedup_fingerprint)
WHERE is_active = TRUE`.

**`job_ingestion/app/models/company.py`** (wherever active companies live)
Add `yc_batch`, `yc_slug` fields or store in existing JSONB `metadata` column.

**`recommendation_service/app/models/shared.py`**
No changes needed — YC jobs flow through the same `normalized_jobs` table and get enriched
with the same LLM pipeline. They'll pick up `domain`, `pools`, `role_intent`,
`requires_clearance` from enrichment automatically.

---

## Connector Class Structure

```python
# job_ingestion/app/ingestion/connectors/workatastartup.py

import asyncio
import httpx
from bs4 import BeautifulSoup
from dataclasses import dataclass

from ..base import BaseConnector
from ..models import RawJob

ROLES = ["eng", "ds"]
BATCH_DELAY = 1.5  # seconds between paginated requests


class WorkAtAStartupConnector(BaseConnector):
    ats_type = "workatastartup"
    name = "Work at a Startup (YC)"

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                follow_redirects=True,
                headers={
                    "User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)",
                    "Accept": "application/json",
                },
                timeout=30.0,
            )
            await self._login(self._client)
        return self._client

    async def _login(self, client: httpx.AsyncClient) -> None:
        # GET login page for CSRF token
        resp = await client.get("https://www.workatastartup.com/login")
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf_input = soup.find("input", {"name": "_csrf_token"})
        if not csrf_input:
            raise ValueError("CSRF input not found — login page structure may have changed")
        csrf = csrf_input["value"]

        # POST credentials
        resp = await client.post(
            "https://account.ycombinator.com/",
            data={"email": self.email, "password": self.password, "_csrf_token": csrf},
        )
        if "Log out" not in resp.text and resp.status_code not in (200, 302):
            raise RuntimeError(f"YC login failed: status={resp.status_code}")

    async def fetch_raw_jobs(self) -> list[RawJob]:
        client = await self._get_client()
        all_raw = []

        for role in ROLES:
            jobs = await self._fetch_role(client, role)
            all_raw.extend(jobs)

        return all_raw

    async def _fetch_role(
        self, client: httpx.AsyncClient, role: str
    ) -> list[RawJob]:
        collected = []
        offset = 0
        limit = 50

        while True:
            resp = await client.get(
                "https://www.workatastartup.com/jobs",
                params={
                    "q": "",
                    "roles[]": role,
                    "jobType": "fulltime",
                    "offset": offset,
                    "limit": limit,
                },
            )
            # Session expired
            if resp.status_code == 302 and "/login" in resp.headers.get("location", ""):
                await self._login(client)
                continue

            resp.raise_for_status()
            data = resp.json()

            for j in data.get("jobs", []):
                collected.append(self._to_raw(j))

            offset += limit
            if offset >= data.get("total", 0):
                break
            await asyncio.sleep(BATCH_DELAY)

        return collected

    def _to_raw(self, j: dict) -> RawJob:
        company = j.get("company", {})
        return RawJob(
            external_id=f"yc_{j['id']}",
            ats_type=self.ats_type,
            title=j.get("title", ""),
            company_name=company.get("name", ""),
            company_slug=company.get("slug", ""),
            job_location=j.get("location") or ("Remote" if j.get("remote") else ""),
            is_remote=j.get("remote", False),
            description_html=j.get("description", ""),
            job_url=j.get("apply_url", f"https://www.workatastartup.com/jobs/{j['id']}"),
            posted_at=j.get("created_at"),
            visa_sponsorship=j.get("visa_sponsorship", False),
            raw_metadata={
                "yc_batch": company.get("batch"),
                "team_size": company.get("team_size"),
                "company_one_liner": company.get("one_liner"),
            },
        )
```

---

## Phase 1 Company Crawler Structure

```python
# job_ingestion/app/ingestion/connectors/yc_directory.py

import re
import httpx
from dataclasses import dataclass, field

ATS_FINGERPRINTS = {
    "greenhouse": [
        r"boards\.greenhouse\.io/([^/\"'\s]+)",
        r"job-boards\.greenhouse\.io/([^/\"'\s]+)",
    ],
    "lever": [r"jobs\.lever\.co/([^/\"'\s]+)"],
    "ashby": [r"jobs\.ashbyhq\.com/([^/\"'\s]+)"],
    "workday": [r"([\w-]+)\.wd\d+\.myworkdayjobs\.com"],
}


@dataclass
class DirectoryCrawlResult:
    greenhouse_tokens: list[str] = field(default_factory=list)
    lever_slugs: list[str] = field(default_factory=list)
    ashby_slugs: list[str] = field(default_factory=list)
    workday_instances: list[str] = field(default_factory=list)
    yc_native_companies: list[dict] = field(default_factory=list)
    unresolved: list[dict] = field(default_factory=list)


async def crawl_yc_directory() -> DirectoryCrawlResult:
    result = DirectoryCrawlResult()
    companies = await fetch_all_yc_companies()

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        for company in companies:
            if not company.get("hiring"):
                continue
            website = company.get("website", "")
            if not website:
                result.yc_native_companies.append(company)
                continue

            careers_urls = derive_career_urls(website)
            ats_type, identifier = await probe_for_ats(client, careers_urls)

            if ats_type == "greenhouse":
                result.greenhouse_tokens.append(identifier)
            elif ats_type == "lever":
                result.lever_slugs.append(identifier)
            elif ats_type == "ashby":
                result.ashby_slugs.append(identifier)
            elif ats_type == "workday":
                result.workday_instances.append(identifier)
            else:
                # No known ATS — will be scraped from Work at a Startup
                result.yc_native_companies.append(company)

    return result


def derive_career_urls(website: str) -> list[str]:
    """Try common career page paths."""
    base = website.rstrip("/")
    return [
        f"{base}/careers",
        f"{base}/jobs",
        f"{base}/about/careers",
        base,  # some companies link ATS directly from homepage
    ]


async def probe_for_ats(
    client: httpx.AsyncClient, urls: list[str]
) -> tuple[str | None, str | None]:
    for url in urls:
        try:
            resp = await client.get(url, timeout=10.0)
            html = resp.text
            for ats, patterns in ATS_FINGERPRINTS.items():
                for pattern in patterns:
                    if m := re.search(pattern, html, re.IGNORECASE):
                        return ats, m.group(1)
        except Exception:
            continue
    return None, None
```

---

## Scheduling

```python
# In scheduler.py, add:

@scheduler.scheduled_job("cron", day_of_week="sun", hour=1)
async def yc_directory_crawl_job():
    """
    Weekly: discovers YC companies, routes known ATS to existing connectors.
    """
    result = await crawl_yc_directory()
    await upsert_company_batch("greenhouse", result.greenhouse_tokens)
    await upsert_company_batch("lever", result.lever_slugs)
    await upsert_company_batch("ashby", result.ashby_slugs)
    await upsert_company_batch("workday", result.workday_instances)
    logger.info(
        "yc_directory_crawl complete",
        greenhouse=len(result.greenhouse_tokens),
        lever=len(result.lever_slugs),
        ashby=len(result.ashby_slugs),
        workday=len(result.workday_instances),
        yc_native=len(result.yc_native_companies),
    )


@scheduler.scheduled_job("interval", hours=12)
async def yc_native_jobs_job():
    """
    Every 12 hours: scrapes Work at a Startup for companies with no known ATS.
    """
    connector = WorkAtAStartupConnector(
        email=settings.YC_CRAWLER_EMAIL,
        password=settings.YC_CRAWLER_PASSWORD,
    )
    raw_jobs = await connector.fetch_raw_jobs()
    inserted, dupes = 0, 0
    for raw in raw_jobs:
        if await is_duplicate(raw):
            dupes += 1
            continue
        await ingest_raw_job(raw)
        inserted += 1
    logger.info("yc_native_jobs complete", inserted=inserted, dupes=dupes)
```

---

## Configuration

Add to `settings.py` / `.env`:

```env
YC_CRAWLER_EMAIL=crawler@yourproduct.com
YC_CRAWLER_PASSWORD=<strong-password>
```

Do **not** use a personal YC account. If the account gets flagged or blocked, you need to
be able to create a fresh one without losing access to a personal profile.

---

## Operational Notes

### Fragility risk

Work at a Startup will change its HTML or XHR format without notice. The login CSRF field
name and the jobs endpoint path are the two most likely breakage points. Add a health check
that alerts if 0 jobs are returned from 3 consecutive runs — this is the clearest signal
the scraper silently broke.

```python
@scheduler.scheduled_job("interval", hours=12)
async def yc_health_check():
    count = await count_jobs_ingested_since(source="yc", hours=36)
    if count == 0:
        await alert_ops("YC connector returned 0 jobs for 36+ hours — likely broken")
```

### Rate limiting

YC does not publish rate limits. Use `1.5 seconds` between paginated requests. Do not run
parallel requests against the jobs endpoint. Total crawl time for ~500 jobs at 50/page =
10 requests × 1.5s = 15 seconds — well within any reasonable limit.

### Session reuse

The `httpx.AsyncClient` instance should live for the duration of one crawl run, not
be recreated per request. The cookie session is valid for approximately 30 days based on
observed behavior, so re-login on session expiry rather than on every run.

### YC batch as a signal

The `yc_batch` field (e.g., `"S24"`, `"W25"`) is useful metadata. Recent batches (within
the last 4) indicate very early-stage companies — consider a soft seniority penalty for
these when the user's target seniority is `SENIOR` or `STAFF`, since early YC companies
rarely have those levels.

### Job volume expectation

Work at a Startup typically has 400–800 active engineering jobs at any given time. After
dedup against your existing Greenhouse/Lever/Ashby corpus (which will cover ~60% of them),
expect 150–300 net new jobs per run. This is a meaningful addition, particularly for
early-stage roles that don't appear anywhere else.

---

## Testing Checklist

- [ ] Login flow works end-to-end with the service account
- [ ] Pagination correctly stops at `total`
- [ ] Session-expired case (302 → `/login`) triggers re-login and retry
- [ ] Dedup fingerprint correctly matches a job that also exists in Greenhouse corpus
- [ ] `job_country` resolves correctly for "San Francisco, CA", "New York, NY", "Remote"
- [ ] `yc_batch` is stored in metadata and accessible post-enrichment
- [ ] `visa_sponsorship: true` flows through to `sponsorship_eligible` on normalized job
- [ ] Zero-job health alert fires correctly in staging
- [ ] Weekly directory crawl adds new Greenhouse board_tokens to the Greenhouse company table
- [ ] YC-native jobs appear in recommendation results for at least one user within 24 hours
  of first successful crawl
