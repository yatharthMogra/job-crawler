# Workday Connector — Implementation Guide

This document covers everything needed to implement a Workday connector for the job ingestion pipeline. It follows the same structure as the existing connector guide (sections 4.x and 5.x) and answers all open questions from section 7.2.

---

## 1. Workday API Overview

Workday does not publish an official public job board API. However, every Workday-hosted career site exposes an undocumented but stable internal API called the **CXS API** (Consumer Experience Services). This API powers the Workday career site UI and is safe to use for read-only job fetching — it requires no authentication, no API key, and no scraping.

All existing open-source job aggregators (Jobspy, SimpleScraper derivatives, etc.) use this same API. It has been stable for several years.

**Base URL pattern:**
```
https://{tenant}.wd{instance}.myworkdayjobs.com/wday/cxs/{tenant}/{career_site}/jobs
```

Example for Stripe:
```
https://stripe.wd1.myworkdayjobs.com/wday/cxs/stripe/External/jobs
```

---

## 2. Answering Section 7.2 Questions

### What is the `board_token` equivalent?

Workday requires **three** identifiers to construct the API URL:

| Component | Description | Example |
|---|---|---|
| `tenant` | Workday subdomain — unique per company | `stripe`, `apple`, `databricks` |
| `instance` | Workday data center number | `wd1`, `wd3`, `wd5` |
| `career_site` | Career site path segment — varies per company | `External`, `careers`, `US-Corporate` |

**Recommendation:** Use `board_token` for the `tenant` only (consistent with how other platforms use it as the primary company identifier). Store `instance` and `career_site` in `platform_config` JSONB, which already exists on the `companies` table for exactly this purpose.

```json
{
  "platform": "workday",
  "board_token": "stripe",
  "platform_config": {
    "instance": "wd1",
    "career_site": "External"
  }
}
```

The connector constructs the base URL as:
```python
def _base_url(self, company: Company) -> str:
    config = company.platform_config or {}
    instance = config.get("instance", "wd1")
    career_site = config.get("career_site", "External")
    return (
        f"https://{company.board_token}.{instance}.myworkdayjobs.com"
        f"/wday/cxs/{company.board_token}/{career_site}"
    )
```

**How to find a company's tenant/instance/career_site:**

Navigate to the company's careers page. If the URL contains `myworkdayjobs.com`, the components are directly visible. If they use a custom domain (e.g., `careers.stripe.com`), view page source or network requests — the Workday API calls will expose the tenant and instance.

---

### Public API vs scraping?

Public API — no scraping required. The CXS API is an HTTP JSON API. All requests are standard POST/GET with `Content-Type: application/json`. No browser automation, no HTML parsing of the career page itself.

---

### Single call or multi-step fetch?

**Two-step fetch, same pattern as Ashby.**

The list endpoint returns job summaries but does **not** include the job description. A per-job detail call is required to get `jobDescription` (HTML).

Step 1 — paginated list:
```
POST {base_url}/jobs
Body: {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": ""}
```

Step 2 — per-job detail:
```
GET {base_url}/job{externalPath}
```

where `externalPath` comes from the list response.

---

### Stable job ID

Use `jobReqId` — **not** `externalPath` and not the full title-slug URL.

The `externalPath` embeds the job title in the URL slug (e.g., `/job/New-York-NY/Senior-Engineer_JR-12345`). If a job's title is edited, the `externalPath` changes, which would incorrectly trigger a "new job" detection. `jobReqId` is the internal requisition ID assigned at creation and never changes.

`jobReqId` examples: `JR-12345`, `R0023456`, `REQ-00089`, `12345` (format varies by company).

The connector must map `jobReqId` → `id` in the returned dict:
```python
job["id"] = job_detail["jobPostingInfo"]["jobReqId"]
```

---

### Description format

HTML. The detail endpoint returns `jobDescription` as an HTML string (typically `<ul>`, `<p>`, `<b>` tags). Maps directly to `raw_html`. No stripping required by the connector — `clean_job_description` in the pipeline handles that.

---

### Rate limits / pagination

**Pagination:** Offset-based. Default page size is 20. Loop until `offset >= total` from the response.

```
total: 150 jobs → pages at offset 0, 20, 40, ... 140
```

**Rate limiting:**
- List calls: no strict limit observed; safe at default concurrency.
- Detail calls: apply the same pattern as Ashby — `concurrency=1`, `0.35s` delay between requests, exponential backoff on HTTP 429 or 503. Some tenants (large companies with heavy traffic) are stricter; `0.5s` delay is safer for companies with 200+ jobs.

**Practical cap:** Most companies have under 500 active postings. At 0.35s per detail call, 500 jobs takes ~3 minutes. This is acceptable within the pipeline's per-company timeout.

---

### Auth requirements

None. The CXS API is fully public. `platform_config` is used only for the `instance` and `career_site` routing parameters, not auth.

If a company's Workday site requires login to view jobs (rare — applies to internal-only postings), those jobs are not accessible and should be skipped gracefully.

---

### Location representation

`locationsText` from the list call is a comma-separated string of locations: `"Mountain View, California, USA"`, or `"Remote"`, or `"New York, NY, USA; San Francisco, CA, USA"` (semicolon-separated for multi-location).

For multi-location jobs, the detail call also returns a `locations` array. The connector should prefer the detail call's location data.

**Recommended normalization in `deterministic.py`:** join multiple locations with ` | ` (consistent with Ashby's secondary location handling).

---

### Timestamp field

Use `postedOn` from the detail response.

**Critical:** Workday returns dates in `MM/DD/YYYY` format — **not ISO 8601**. The deterministic extractor must parse this explicitly:

```python
from datetime import datetime, timezone

def _parse_workday_date(date_str: str | None) -> datetime | None:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
```

---

## 3. API Reference

### 3.1 List Endpoint

```
POST https://{tenant}.wd{instance}.myworkdayjobs.com/wday/cxs/{tenant}/{career_site}/jobs
Content-Type: application/json
```

**Request body:**
```json
{
  "appliedFacets": {},
  "limit": 20,
  "offset": 0,
  "searchText": ""
}
```

**Response shape:**
```json
{
  "total": 87,
  "jobPostings": [
    {
      "title": "Senior Software Engineer",
      "externalPath": "/job/New-York-NY-USA/Senior-Software-Engineer_JR-12345",
      "locationsText": "New York, NY, USA",
      "postedOn": "05/15/2026",
      "bulletFields": ["Full time"],
      "jobReqId": "JR-12345"
    }
  ]
}
```

**Key fields from list:**

| Field | Notes |
|---|---|
| `total` | Total jobs — used to determine pagination |
| `jobPostings[].jobReqId` | Stable job ID — map to `id` |
| `jobPostings[].externalPath` | Used to construct detail URL and posting URL |
| `jobPostings[].title` | Job title (available at list stage) |
| `jobPostings[].locationsText` | Location summary string |
| `jobPostings[].postedOn` | Date in `MM/DD/YYYY` format |
| `jobPostings[].bulletFields` | May contain employment type hint |

---

### 3.2 Detail Endpoint

```
GET https://{tenant}.wd{instance}.myworkdayjobs.com/wday/cxs/{tenant}/{career_site}/job{externalPath}
```

Example:
```
GET https://stripe.wd1.myworkdayjobs.com/wday/cxs/stripe/External/job/New-York-NY-USA/Senior-Software-Engineer_JR-12345
```

**Response shape:**
```json
{
  "jobPostingInfo": {
    "title": "Senior Software Engineer",
    "jobReqId": "JR-12345",
    "jobDescription": "<p>Join our infrastructure team...</p><ul><li>Python</li></ul>",
    "locationsText": "New York, NY, USA",
    "location": "New York, NY, USA",
    "postedOn": "05/15/2026",
    "jobScheduleType": "Full_Time",
    "timeType": "Full_Time",
    "department": "Engineering",
    "supervisoryOrganization": "Platform - Infrastructure"
  }
}
```

**Key fields from detail:**

| Field | Notes |
|---|---|
| `jobPostingInfo.jobDescription` | Full HTML description → `raw_html` |
| `jobPostingInfo.department` | Department (not in list response) |
| `jobPostingInfo.jobScheduleType` | Employment type — values: `Full_Time`, `Part_Time`, `Temporary`, `Internship` |
| `jobPostingInfo.postedOn` | Authoritative date (prefer over list `postedOn`) |
| `jobPostingInfo.location` | May be more specific than `locationsText` |

---

## 4. Merged Job Dict (Connector Output)

The connector merges list + detail into a single dict. This is the **platform-native dict** returned by `fetch_jobs()` and stored in `raw_api_response`.

```json
{
  "id": "JR-12345",
  "title": "Senior Software Engineer",
  "externalPath": "/job/New-York-NY-USA/Senior-Software-Engineer_JR-12345",
  "locationsText": "New York, NY, USA",
  "postedOn": "05/15/2026",
  "bulletFields": ["Full time"],
  "jobReqId": "JR-12345",
  "jobPostingInfo": {
    "title": "Senior Software Engineer",
    "jobReqId": "JR-12345",
    "jobDescription": "<p>Join our infrastructure team...</p>",
    "locationsText": "New York, NY, USA",
    "location": "New York, NY, USA",
    "postedOn": "05/15/2026",
    "jobScheduleType": "Full_Time",
    "department": "Engineering",
    "supervisoryOrganization": "Platform - Infrastructure"
  }
}
```

The top-level `id` field is mandatory and must equal `jobReqId`. The change detector keys on `job["id"]`.

The synthesized `posting_url` is constructed by the deterministic extractor (not the connector) from the tenant base URL + `externalPath`.

---

## 5. Connector Implementation

### 5.1 Fetch pattern

```python
# app/ingestion/connectors/workday.py

import asyncio
import httpx
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.exceptions import ConnectorFetchError, ParseError
from app.models.company import Company

DETAIL_DELAY = 0.35  # seconds between detail calls
MAX_PAGE_SIZE = 20


class WorkdayConnector(BaseConnector):
    async def fetch_jobs(self, company: Company) -> list[dict]:
        base_url = self._base_url(company)
        jobs_list = await self._fetch_all_pages(base_url)
        jobs_with_detail = []

        async with httpx.AsyncClient(timeout=30) as client:
            for listing in jobs_list:
                external_path = listing.get("externalPath")
                if not external_path:
                    continue  # skip malformed listings
                try:
                    detail = await self._fetch_detail(client, base_url, external_path)
                    merged = {**listing, "jobPostingInfo": detail.get("jobPostingInfo", {})}
                    # Guarantee top-level id field
                    req_id = listing.get("jobReqId") or detail.get("jobPostingInfo", {}).get("jobReqId")
                    if not req_id:
                        continue  # no stable ID — skip
                    merged["id"] = str(req_id)
                    jobs_with_detail.append(merged)
                except Exception as e:
                    # Log and skip — don't abort full company fetch for one detail failure
                    log.warning("workday_detail_fetch_failed", company=company.name,
                                external_path=external_path, error=str(e))
                    continue
                await asyncio.sleep(DETAIL_DELAY)

        return jobs_with_detail

    def _base_url(self, company: Company) -> str:
        config = company.platform_config or {}
        instance = config.get("instance", "wd1")
        career_site = config.get("career_site", "External")
        return (
            f"https://{company.board_token}.{instance}.myworkdayjobs.com"
            f"/wday/cxs/{company.board_token}/{career_site}"
        )

    async def _fetch_all_pages(self, base_url: str) -> list[dict]:
        all_jobs = []
        offset = 0
        async with httpx.AsyncClient(timeout=30) as client:
            while True:
                response = await client.post(
                    f"{base_url}/jobs",
                    json={"appliedFacets": {}, "limit": MAX_PAGE_SIZE,
                          "offset": offset, "searchText": ""},
                )
                if response.status_code != 200:
                    raise ConnectorFetchError(
                        f"Workday list failed: {response.status_code}", response.status_code
                    )
                try:
                    data = response.json()
                except Exception:
                    raise ParseError("Workday list response is not valid JSON")

                postings = data.get("jobPostings", [])
                if not isinstance(postings, list):
                    raise ParseError("Workday list response missing jobPostings array")

                all_jobs.extend(postings)
                total = data.get("total", 0)
                offset += MAX_PAGE_SIZE
                if offset >= total or not postings:
                    break

        return all_jobs

    async def _fetch_detail(self, client: httpx.AsyncClient,
                             base_url: str, external_path: str) -> dict:
        url = f"{base_url}/job{external_path}"
        response = await client.get(url)
        if response.status_code == 429:
            await asyncio.sleep(2.0)
            response = await client.get(url)
        if response.status_code != 200:
            raise ConnectorFetchError(
                f"Workday detail failed: {response.status_code}", response.status_code
            )
        try:
            return response.json()
        except Exception:
            raise ParseError(f"Workday detail response is not valid JSON: {external_path}")
```

---

## 6. Deterministic Extraction

Add `_extract_workday` to `app/ingestion/extractor/deterministic.py` and register it in `FIELD_EXTRACTORS`.

```python
from datetime import datetime, timezone

def _parse_workday_date(date_str: str | None) -> datetime | None:
    """Parse Workday's MM/DD/YYYY date format to UTC datetime."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").replace(tzinfo=timezone.utc)
    except ValueError:
        return None

def _extract_workday_employment_type(job: dict) -> str | None:
    info = job.get("jobPostingInfo", {})
    schedule = info.get("jobScheduleType", "")
    SCHEDULE_MAP = {
        "Full_Time": "Full-time",
        "Part_Time": "Part-time",
        "Temporary": "Temporary",
        "Internship": "Internship",
        "Contract": "Contract",
    }
    if schedule in SCHEDULE_MAP:
        return SCHEDULE_MAP[schedule]
    # Fallback: scan bulletFields from list response
    for bullet in job.get("bulletFields", []):
        b = bullet.lower()
        if "full" in b:
            return "Full-time"
        if "intern" in b:
            return "Internship"
        if "part" in b:
            return "Part-time"
        if "contract" in b:
            return "Contract"
    return None

def _extract_workday(job: dict, company=None) -> dict:
    info = job.get("jobPostingInfo", {})

    # Posting URL: synthesized from board_token + externalPath
    # company.board_token and platform_config available if needed
    external_path = job.get("externalPath", "")
    posting_url = None
    if company and external_path:
        config = (company.platform_config or {}) if company else {}
        instance = config.get("instance", "wd1")
        career_site = config.get("career_site", "External")
        posting_url = (
            f"https://{company.board_token}.{instance}.myworkdayjobs.com"
            f"/job{external_path}"
        )

    # Location: prefer detail, fall back to list locationsText
    location = (
        info.get("location")
        or info.get("locationsText")
        or job.get("locationsText")
    )

    # Posted date: prefer detail, fall back to list
    posted_at = _parse_workday_date(
        info.get("postedOn") or job.get("postedOn")
    )

    return {
        "external_job_id": str(job["id"]),
        "title": info.get("title") or job.get("title"),
        "location": location,
        "department": info.get("department") or info.get("supervisoryOrganization"),
        "posting_url": posting_url,
        "posted_at": posted_at,
        "employment_type": _extract_workday_employment_type(job),
        "raw_html": info.get("jobDescription", ""),
    }
```

**Register in `FIELD_EXTRACTORS`:**
```python
FIELD_EXTRACTORS = {
    "greenhouse": _extract_greenhouse,
    "lever": _extract_lever,
    "ashby": _extract_ashby,
    "workday": _extract_workday,   # add this
}
```

**Register in `fetcher.py`:**
```python
CONNECTORS = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
    "ashby": AshbyConnector,
    "workday": WorkdayConnector,   # add this
}
```

---

## 7. Field Mapping Reference

Extends the table in section 5.2 of the connector guide:

| Common field | Workday source |
|---|---|
| `external_job_id` | `job["id"]` (= `jobReqId`, set by connector) |
| `title` | `jobPostingInfo.title` → fallback `job.title` |
| `location` | `jobPostingInfo.location` → `jobPostingInfo.locationsText` → `job.locationsText` |
| `department` | `jobPostingInfo.department` → `jobPostingInfo.supervisoryOrganization` |
| `posting_url` | Synthesized: `https://{tenant}.wd{instance}.myworkdayjobs.com/job{externalPath}` |
| `posted_at` | `jobPostingInfo.postedOn` parsed from `MM/DD/YYYY` |
| `employment_type` | `jobPostingInfo.jobScheduleType` mapped via `SCHEDULE_MAP` → `bulletFields` fallback |
| `raw_html` | `jobPostingInfo.jobDescription` |

---

## 8. `companies.json` Seed Format

```json
{
  "company": "Stripe",
  "platform": "workday",
  "board_token": "stripe",
  "platform_config": {
    "instance": "wd1",
    "career_site": "External"
  }
}
```

Common patterns for locating `instance` and `career_site`:
- Visit the company careers page, look for `myworkdayjobs.com` in URLs or network requests
- The instance (`wd1`, `wd3`, `wd5`) is in the subdomain
- The career site name is the path segment after the tenant name in the API URL

---

## 9. Tests

Follow the pattern in `tests/test_ashby_connector.py`. Minimum coverage:

| Test | What to verify |
|---|---|
| `test_workday_success_path` | List + detail fetch returns merged dicts with `id` = `jobReqId` |
| `test_workday_pagination` | `total > 20` triggers second page fetch |
| `test_workday_list_http_error` | `ConnectorFetchError` raised on non-200 list response |
| `test_workday_detail_http_error` | Job skipped (logged) on detail failure; remaining jobs still returned |
| `test_workday_missing_req_id` | Job with no `jobReqId` in list or detail is skipped |
| `test_workday_malformed_list_json` | `ParseError` raised |
| `test_workday_date_parsing` | `MM/DD/YYYY` parses to UTC datetime; `None` input returns `None` |
| `test_workday_employment_type_mapping` | `Full_Time` → `Full-time`, `Internship` → `Internship`, unknown → `None` |

---

## 10. Workday-Specific Anti-Patterns

| Anti-pattern | What happens | Correct approach |
|---|---|---|
| Using `externalPath` as the job ID | Title edits change the URL slug, triggering false "new job" events | Use `jobReqId` always |
| Skipping the detail call | `jobDescription` and `department` are absent from list response; jobs enrich with empty descriptions and fail skill extraction | Always fetch detail, like Ashby |
| Parsing `postedOn` as ISO 8601 | Workday uses `MM/DD/YYYY` — strptime with `%Y-%m-%dT...` raises ValueError silently | Use `_parse_workday_date()` with `%m/%d/%Y` |
| Hardcoding `instance = "wd1"` | Some companies use `wd3` or `wd5`; wrong instance returns 404 | Read from `platform_config.instance`, default `wd1` |
| Hardcoding `career_site = "External"` | Companies use `careers`, `US-Corporate`, `jobs`, or custom names | Read from `platform_config.career_site`, default `External` |
| Raising on single detail failure | One malformed job shouldn't abort the full company fetch | Log warning, skip job, continue |
| Not delaying between detail calls | Some Workday tenants rate-limit aggressively | Keep `DETAIL_DELAY = 0.35s`, back off on 429 |
