# Oracle HCM Connector — Implementation Guide

This document covers everything needed to implement an Oracle HCM (Oracle Recruiting Cloud) connector for the job ingestion pipeline. Follows the same structure as `workday_connector_guide.md`.

The example URL the user provided:
```
https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/jobs
```

Breaking down: `egug` = tenant, `us2` = datacenter, `CX_1` = site number. This is American Express's Oracle HCM career site.

---

## 1. Oracle HCM API Overview

Oracle Recruiting Cloud (part of Oracle HCM) exposes a public REST API called `hcmRestApi` that powers every Oracle-hosted career site. No authentication is required for public job board endpoints. It is not officially documented as a public API, but it is stable, widely used by aggregators, and follows a consistent pattern across all Oracle HCM tenants.

**Base URL pattern:**
```
https://{tenant}.fa.{datacenter}.oraclecloud.com/hcmRestApi/resources/latest/
```

For American Express:
```
https://egug.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/
```

---

## 2. Answering Section 7.2 Questions (from CONNECTOR_GUIDE.md)

### What is the `board_token` equivalent?

Oracle HCM requires three identifiers:

| Component | Description | Example |
|---|---|---|
| `tenant` | Subdomain before `.fa.` | `egug` (American Express), `eeho` (Oracle Corp) |
| `datacenter` | Oracle data center region | `us2`, `us6`, `eu1`, `eu2`, `ap1` |
| `site_number` | Career site identifier | `CX_1`, `CX_45001` |

**Recommendation:** Same split as Workday — `board_token` = tenant, `platform_config` JSONB for the rest:

```json
{
  "platform": "oracle_hcm",
  "board_token": "egug",
  "platform_config": {
    "datacenter": "us2",
    "site_number": "CX_1"
  }
}
```

**Finding tenant/datacenter/site_number:**

Navigate to the company's Oracle career page. If the URL is:
```
https://egug.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/jobs
```
All three components are visible directly: `egug`, `us2`, `CX_1`.

If the company uses a custom domain (e.g., `careers.amex.com`), view the page source or network requests — the `hcmRestApi` calls expose the full Oracle URL.

**If site_number is not in URL (fallback discovery):**

Some career pages embed the site number in their JavaScript. Use a GET request to the career page and regex the response:

```python
import re
import httpx

async def discover_site_number(careers_url: str) -> str | None:
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(careers_url)
    # Check HTML source for embedded siteNumber
    match = re.search(r"siteNumber:\s*['\"](\bCX_[\w]+\b)['\"]", response.text)
    if match:
        return match.group(1)
    # Check cookies
    cookie = response.cookies.get("ORA_CX_SITE_NUMBER")
    if cookie:
        return cookie
    return None
```

Only needed when `platform_config.site_number` is not already set. In practice, add `site_number` to `companies.json` manually after discovery — it rarely changes.

---

### Public API vs scraping?

Public REST API — no scraping, no browser automation. All requests are standard GET with JSON responses. Three required headers must be present (see section 3.1).

---

### Single call or multi-step fetch?

**Two-step fetch, same pattern as Ashby and Workday.**

The list endpoint returns job summaries with `ShortDescriptionStr` only — not the full description. A per-job detail call is required to get `ExternalDescriptionStr`, `ExternalQualificationsStr`, and `ExternalResponsibilitiesStr`.

---

### Stable job ID

Use `Id` — a numeric string (e.g., `"307750"`). It is the Oracle internal requisition ID, assigned at creation and immutable. The detail endpoint also uses this ID in its `finder` parameter.

Do **not** use title-based URL slugs or position codes — these can change if a job is edited.

---

### Description format

HTML. The detail endpoint returns three separate HTML fields that together make the full description:

| Field | Content |
|---|---|
| `ExternalDescriptionStr` | Overview and main description |
| `ExternalQualificationsStr` | Qualifications and requirements |
| `ExternalResponsibilitiesStr` | Responsibilities |

The connector concatenates all three. `raw_html` = `ExternalDescriptionStr + ExternalQualificationsStr + ExternalResponsibilitiesStr`. `clean_job_description` in the pipeline handles stripping.

---

### Rate limits / pagination

**Pagination:** Offset-based, but pagination lives **inside the `finder` string**, not as top-level query params. Top-level `limit`/`offset` paginate the outer `items[]` wrapper (always one container) — they do not advance `requisitionList[]`. Use lowercase `offset` and `limit` in the finder (PascalCase `Offset`/`Limit` returns HTTP 400 on live tenants):

```
finder=findReqs;siteNumber={site_number},offset={offset},limit={limit}
```

Continue until `offset >= items[0].TotalJobsCount`, or `requisitionList` is empty. If `TotalJobsCount` is missing, stop when `len(requisitionList) < limit`. Use `offset += len(jobs_on_page)` not `offset += limit`.

**Rate limiting:**
- List calls: safe at default concurrency.
- Detail calls: `0.5s` delay between requests, exponential backoff on 429. Oracle's undocumented rate limit is approximately 60 requests/minute — stricter than Workday. Use `DETAIL_DELAY = 0.5` for Oracle vs `0.35` for Workday.

**Posted-date recency filter:**

Configured via `platform_config.max_posted_age_days` (default `30`), same as Workday. Oracle list rows include `PostedDate` (`YYYY-MM-DD`), enabling cheap **pre-detail** filtering:

1. If list `PostedDate` parses and is older than the window → skip (no detail HTTP, no sleep).
2. If list `PostedDate` parses and is fresh → fetch detail, include if post-check passes.
3. If list `PostedDate` is missing → fetch detail, then require parseable `PostedDate` on merged job within window (undated jobs are skipped).

---

### Auth requirements

None for public career sites. Three required **request headers** that must be present on every call — they are not auth but Oracle's API rejects requests without them:

```python
headers = {
    "ora-irc-cx-userid": str(uuid.uuid4()),  # any valid UUID, regenerated per session
    "ora-irc-language": "en",
    "content-type": "application/vnd.oracle.adf.resourceitem+json;charset=utf-8",
}
```

`ora-irc-cx-userid` identifies the "session" client-side — use a fresh UUID per connector instantiation, not per request.

**SSO risk:** Some Oracle tenants are configured as internal-only and redirect all requests to SSO. If the list endpoint returns a 302 redirect to a login page, the company's jobs are not publicly accessible. Skip these gracefully with a `ConnectorFetchError` and `skip_company=True` flag. Do not raise on 302 — log and continue.

---

### Location representation

`PrimaryLocation` from the list response is a single string: `"New York, New York, United States"`. The detail endpoint may include `workLocation` and `otherWorkLocations` arrays for multi-location jobs.

For multi-location, join with ` | ` (consistent with Ashby and Workday):

```python
locations = [job.get("PrimaryLocation")]
for loc in job.get("otherWorkLocations", []):
    name = loc.get("Name") or loc.get("LocationName")
    if name and name not in locations:
        locations.append(name)
location_str = " | ".join(filter(None, locations))
```

---

### Timestamp field

Use `PostedDate` from the list response. Format is `YYYY-MM-DD` (ISO date, no time component). Parse as:

```python
from datetime import datetime, timezone

def _parse_oracle_date(date_str: str | None) -> datetime | None:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
```

---

## 3. API Reference

### 3.1 List Endpoint

```
GET https://{tenant}.fa.{datacenter}.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions
```

**Required headers:**
```
ora-irc-cx-userid: {uuid}
ora-irc-language: en
content-type: application/vnd.oracle.adf.resourceitem+json;charset=utf-8
```

**Query parameters:**
```
finder=findReqs;siteNumber={site_number},offset=0,limit=100
onlyData=true
expand=requisitionList.workLocation,requisitionList.otherWorkLocations,requisitionList.secondaryLocations
```

Do **not** use top-level `limit`/`offset` query params for job pagination.

**Response shape:**
```json
{
  "items": [
    {
      "TotalJobsCount": 243,
      "hasMore": true,
      "requisitionList": [
        {
          "Id": "307750",
          "Title": "Software Engineer III",
          "PrimaryLocation": "New York, New York, United States",
          "PrimaryLocationCountry": "US",
          "PostedDate": "2026-05-20",
          "ShortDescriptionStr": "Join our engineering team...",
          "HotJobFlag": false,
          "TrendingFlag": false,
          "workLocation": {
            "Name": "New York, New York, United States"
          },
          "otherWorkLocations": []
        }
      ]
    }
  ],
  "hasMore": false
}
```

**Critical response structure note:**

The response nests jobs inside `items[0].requisitionList[]`, not at the root. `TotalJobsCount` and `hasMore` are also inside `items[0]`, not at root level. `hasMore` at the root level controls whether the outer `items` array has more pages — always use `items[0].requisitionList` to extract jobs.

---

### 3.2 Detail Endpoint

```
GET https://{tenant}.fa.{datacenter}.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails
```

**Required headers:** same as list.

**Query parameters:**
```
finder=ById;Id="{job_id}",siteNumber={site_number}
expand=all
onlyData=true
```

Note: the `Id` value must be **quoted** inside the `finder` string: `ById;Id="307750",siteNumber=CX_1`.

**Response shape:**
```json
{
  "items": [
    {
      "Id": "307750",
      "Title": "Software Engineer III",
      "Category": "Information Technology",
      "ExternalDescriptionStr": "<p>Join our engineering team...</p>",
      "ExternalQualificationsStr": "<ul><li>5+ years Python...</li></ul>",
      "ExternalResponsibilitiesStr": "<ul><li>Build scalable APIs...</li></ul>",
      "WorkplaceType": "On-site",
      "skills": [
        {"Skill": "Python"},
        {"Skill": "Kubernetes"}
      ],
      "requisitionFlexFields": [
        {"Prompt": "Employment Type", "Value": "Full Time"}
      ]
    }
  ]
}
```

---

## 4. Merged Job Dict (Connector Output)

The connector merges list + detail into one dict returned by `fetch_jobs()`:

```json
{
  "id": "307750",
  "Id": "307750",
  "Title": "Software Engineer III",
  "PrimaryLocation": "New York, New York, United States",
  "PostedDate": "2026-05-20",
  "otherWorkLocations": [],
  "Category": "Information Technology",
  "ExternalDescriptionStr": "<p>Join our engineering team...</p>",
  "ExternalQualificationsStr": "<ul><li>5+ years Python...</li></ul>",
  "ExternalResponsibilitiesStr": "<ul><li>Build scalable APIs...</li></ul>",
  "WorkplaceType": "On-site",
  "skills": [{"Skill": "Python"}, {"Skill": "Kubernetes"}],
  "requisitionFlexFields": [{"Prompt": "Employment Type", "Value": "Full Time"}]
}
```

Top-level `id` = `str(Id)`. This is the only field the change detector reads.

---

## 5. Connector Implementation

```python
# app/ingestion/connectors/oracle_hcm.py

import asyncio
import uuid
import httpx
from app.ingestion.connectors.base import BaseConnector
from app.ingestion.exceptions import ConnectorFetchError, ParseError
from app.models.company import Company
import structlog

log = structlog.get_logger()

DETAIL_DELAY = 0.5       # seconds between detail calls — stricter than Workday
MAX_PAGE_SIZE = 100

ORACLE_HEADERS = {
    "ora-irc-language": "en",
    "content-type": "application/vnd.oracle.adf.resourceitem+json;charset=utf-8",
}


class OracleHCMConnector(BaseConnector):

    def __init__(self):
        # Single UUID per connector instance (not per request)
        self._session_user_id = str(uuid.uuid4())

    def _headers(self) -> dict:
        return {**ORACLE_HEADERS, "ora-irc-cx-userid": self._session_user_id}

    def _base_url(self, company: Company) -> str:
        config = company.platform_config or {}
        datacenter = config.get("datacenter", "us2")
        return (
            f"https://{company.board_token}.fa.{datacenter}.oraclecloud.com"
            f"/hcmRestApi/resources/latest"
        )

    def _site_number(self, company: Company) -> str:
        config = company.platform_config or {}
        return config.get("site_number", "CX_1")

    async def fetch_jobs(self, company: Company) -> list[dict]:
        base_url = self._base_url(company)
        site_number = self._site_number(company)

        listings = await self._fetch_all_pages(base_url, site_number)
        jobs_with_detail = []

        async with httpx.AsyncClient(timeout=30) as client:
            for listing in listings:
                job_id = listing.get("Id")
                if not job_id:
                    continue
                try:
                    detail = await self._fetch_detail(client, base_url, site_number, str(job_id))
                    merged = {**listing, **detail}
                    merged["id"] = str(job_id)
                    jobs_with_detail.append(merged)
                except ConnectorFetchError as e:
                    if e.status_code in (401, 403):
                        # SSO-protected tenant — abort entire company
                        raise ConnectorFetchError(
                            f"Oracle HCM requires SSO for {company.name} — skip company",
                            e.status_code,
                        )
                    log.warning(
                        "oracle_detail_fetch_failed",
                        company=company.name,
                        job_id=job_id,
                        error=str(e),
                    )
                    continue
                except Exception as e:
                    log.warning(
                        "oracle_detail_unexpected_error",
                        company=company.name,
                        job_id=job_id,
                        error=str(e),
                    )
                    continue

                await asyncio.sleep(DETAIL_DELAY)

        return jobs_with_detail

    async def _fetch_all_pages(self, base_url: str, site_number: str) -> list[dict]:
        all_jobs = []
        seen_ids = set()
        offset = 0
        limit = MAX_PAGE_SIZE
        total_count = None
        url = f"{base_url}/recruitingCEJobRequisitions"

        async with httpx.AsyncClient(timeout=30) as client:
            while True:
                params = {
                    "onlyData": "true",
                    "expand": (
                        "requisitionList.workLocation,"
                        "requisitionList.otherWorkLocations,"
                        "requisitionList.secondaryLocations"
                    ),
                    "finder": (
                        f"findReqs;siteNumber={site_number},"
                        f"offset={offset},limit={limit}"
                    ),
                }
                response = await client.get(url, params=params, headers=self._headers())

                if response.status_code in (301, 302):
                    raise ConnectorFetchError(
                        "Oracle HCM redirected — likely SSO-protected"
                    )
                if response.status_code != 200:
                    raise ConnectorFetchError(
                        f"Oracle HCM list failed: {response.status_code}"
                    )

                try:
                    data = response.json()
                except Exception:
                    raise ParseError("Oracle HCM list response is not valid JSON")

                items = data.get("items", [])
                if not items:
                    break

                requisition_page = items[0]
                jobs_on_page = requisition_page.get("requisitionList", [])

                if total_count is None:
                    total_count = requisition_page.get("TotalJobsCount") or None

                if not jobs_on_page:
                    break

                for job in jobs_on_page:
                    job_id = job.get("Id")
                    if job_id is not None and str(job_id) in seen_ids:
                        continue
                    if job_id is not None:
                        seen_ids.add(str(job_id))
                    all_jobs.append(job)

                offset += len(jobs_on_page)

                if total_count is not None:
                    if offset >= total_count:
                        break
                elif len(jobs_on_page) < limit:
                    break

                await asyncio.sleep(LIST_PAGE_DELAY)

        return all_jobs

    async def _fetch_detail(
        self,
        client: httpx.AsyncClient,
        base_url: str,
        site_number: str,
        job_id: str,
    ) -> dict:
        url = f"{base_url}/recruitingCEJobRequisitionDetails"
        params = {
            "expand": "all",
            "onlyData": "true",
            "finder": f'ById;Id="{job_id}",siteNumber={site_number}',
        }
        response = await client.get(url, params=params, headers=self._headers())

        if response.status_code == 429:
            await asyncio.sleep(3.0)
            response = await client.get(url, params=params, headers=self._headers())

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"Oracle HCM detail failed for {job_id}: {response.status_code}",
                response.status_code,
            )

        try:
            data = response.json()
        except Exception:
            raise ParseError(f"Oracle HCM detail response not valid JSON: {job_id}")

        items = data.get("items", [])
        if not items:
            raise ParseError(f"Oracle HCM detail returned empty items for {job_id}")

        return items[0]
```

---

## 6. Deterministic Extraction

Add `_extract_oracle_hcm` to `app/ingestion/extractor/deterministic.py`:

```python
from datetime import datetime, timezone


def _parse_oracle_date(date_str: str | None) -> datetime | None:
    """Parse Oracle HCM's YYYY-MM-DD date format to UTC datetime."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _extract_oracle_employment_type(job: dict) -> str | None:
    """Extract employment type from flex fields first, then WorkplaceType."""
    for field in job.get("requisitionFlexFields", []):
        prompt = (field.get("Prompt") or "").lower()
        if "employment" in prompt or "type" in prompt or "schedule" in prompt:
            return field.get("Value")

    workplace = job.get("WorkplaceType")
    if workplace:
        return workplace

    return None


def _build_oracle_description_html(job: dict) -> str:
    """
    Oracle splits description into three fields. Concatenate all three.
    All may be HTML. Missing fields are skipped — don't add empty string noise.
    """
    parts = []
    for field in ("ExternalDescriptionStr", "ExternalQualificationsStr", "ExternalResponsibilitiesStr"):
        val = job.get(field, "").strip()
        if val:
            parts.append(val)
    return "\n".join(parts)


def _extract_oracle_hcm(job: dict, company=None) -> dict:
    # Location: primary + any additional locations
    locations = []
    primary = job.get("PrimaryLocation")
    if primary:
        locations.append(primary)
    for loc in job.get("otherWorkLocations", []):
        name = loc.get("Name") or loc.get("LocationName")
        if name and name not in locations:
            locations.append(name)
    location_str = " | ".join(locations) or None

    # Posting URL: synthesized from company config
    posting_url = None
    if company:
        config = (company.platform_config or {})
        datacenter = config.get("datacenter", "us2")
        site_number = config.get("site_number", "CX_1")
        job_id = job.get("Id") or job.get("id")
        if job_id:
            posting_url = (
                f"https://{company.board_token}.fa.{datacenter}.oraclecloud.com"
                f"/hcmUI/CandidateExperience/en/sites/{site_number}"
                f"/requisitions/{job_id}/details"
            )

    return {
        "external_job_id": str(job["id"]),
        "title": job.get("Title"),
        "location": location_str,
        "department": job.get("Category"),
        "posting_url": posting_url,
        "posted_at": _parse_oracle_date(job.get("PostedDate")),
        "employment_type": _extract_oracle_employment_type(job),
        "raw_html": _build_oracle_description_html(job),
    }
```

**Register in `FIELD_EXTRACTORS`:**
```python
FIELD_EXTRACTORS = {
    "greenhouse": _extract_greenhouse,
    "lever": _extract_lever,
    "ashby": _extract_ashby,
    "workday": _extract_workday,
    "oracle_hcm": _extract_oracle_hcm,   # add this
}
```

**Register in `fetcher.py`:**
```python
CONNECTORS = {
    "greenhouse": GreenhouseConnector,
    "lever": LeverConnector,
    "ashby": AshbyConnector,
    "workday": WorkdayConnector,
    "oracle_hcm": OracleHCMConnector,   # add this
}
```

---

## 7. Field Mapping Reference

Extends the platform mapping table from section 5.2 of the connector guide:

| Common field | Oracle HCM source |
|---|---|
| `external_job_id` | `job["Id"]` (top-level, set by connector) |
| `title` | `job["Title"]` |
| `location` | `job["PrimaryLocation"]` + `otherWorkLocations[].Name` joined with ` \| ` |
| `department` | `job["Category"]` (from detail) |
| `posting_url` | Synthesized: `https://{tenant}.fa.{dc}.oraclecloud.com/hcmUI/CandidateExperience/en/sites/{site_number}/requisitions/{id}/details` |
| `posted_at` | `job["PostedDate"]` parsed from `YYYY-MM-DD` |
| `employment_type` | `requisitionFlexFields[*]` where prompt contains "employment" → fallback `WorkplaceType` |
| `raw_html` | `ExternalDescriptionStr + ExternalQualificationsStr + ExternalResponsibilitiesStr` |

---

## 8. `companies.json` Seed Format

```json
{
  "company": "American Express",
  "platform": "oracle_hcm",
  "board_token": "egug",
  "platform_config": {
    "datacenter": "us2",
    "site_number": "CX_1",
    "max_posted_age_days": 30
  }
}
```

| `platform_config` key | Required | Default | Purpose |
|---|---|---|---|
| `datacenter` | Yes | `us2` | Oracle data center (`us2`, `ocs`, etc.) |
| `site_number` | Yes | `CX_1` | Career site identifier |
| `max_posted_age_days` | No | `30` | Skip jobs with `PostedDate` older than N days |

Common Oracle HCM tenants (for reference when adding companies):

| Company | board_token | datacenter | site_number |
|---|---|---|---|
| American Express | `egug` | `us2` | `CX_1` |
| JPMorgan Chase | varies | varies | varies |
| Goldman Sachs | varies | varies | varies |

Confirm each tenant's datacenter and site_number by inspecting the company's career page URL directly.

---

## 9. Tests

| Test | What to verify |
|---|---|
| `test_oracle_success_path` | List + detail fetch returns merged dicts with `id` = `str(Id)` |
| `test_oracle_pagination` | Finder `Offset=100` triggers second page when `TotalJobsCount` not yet reached |
| `test_oracle_pagination_uses_finder_offset` | Pagination via finder string, not top-level query params |
| `test_oracle_nested_structure` | Jobs extracted from `items[0].requisitionList`, not from root |
| `test_oracle_description_concatenation` | All three description fields concatenated into `raw_html` |
| `test_oracle_missing_description_fields` | Missing `ExternalQualificationsStr` or `ExternalResponsibilitiesStr` handled gracefully |
| `test_oracle_sso_redirect` | 302 response raises `ConnectorFetchError` with skip signal |
| `test_oracle_detail_429_retry` | 429 on detail triggers 3s sleep and one retry |
| `test_oracle_detail_failure_continues` | Single detail failure skips job, rest of company fetch proceeds |
| `test_oracle_missing_id` | Job with no `Id` in list response is skipped |
| `test_oracle_date_parsing` | `YYYY-MM-DD` parses correctly; `None` returns `None` |
| `test_oracle_employment_type_flex_fields` | Flex field with "Employment Type" prompt extracted |
| `test_oracle_location_join` | Multi-location job joins `PrimaryLocation` + `otherWorkLocations` with ` \| ` |
| `test_oracle_headers_present` | All three required headers sent on every request |
| `test_oracle_skips_stale_from_list_posted_date` | Stale list `PostedDate` skips detail fetch |
| `test_oracle_includes_recent_posted_date` | Fresh `PostedDate` fetches detail and returns job |
| `test_oracle_post_detail_rejects_stale_when_list_date_missing` | Undated list + stale detail `PostedDate` skipped |
| `test_oracle_respects_max_posted_age_days_config` | Custom `max_posted_age_days` honored |

---

## 10. Oracle HCM-Specific Anti-Patterns

| Anti-pattern | What happens | Correct approach |
|---|---|---|
| Reading jobs from `data["items"]` directly | `items` is a wrapper — jobs are in `items[0]["requisitionList"]` | Dig one level deeper: `data["items"][0]["requisitionList"]` |
| Omitting required headers | API returns 400 or empty `items[]` | Always include all three `ora-irc-*` headers |
| Using `ShortDescriptionStr` as `raw_html` | Enrichment runs on abbreviated text → poor skill extraction | Always fetch detail for the three `External*Str` fields |
| Forgetting quotes in detail `finder` | `ById;Id=307750,...` → API returns 404 | Must be `ById;Id="307750",...` with the ID in double quotes |
| Not checking for SSO redirect | 302 propagates as a parse error or empty result | Explicitly check `response.status_code in (301, 302)` before JSON parsing |
| Using `DETAIL_DELAY = 0.35` (Workday value) | Oracle's rate limit is stricter — 429s appear | Use `DETAIL_DELAY = 0.5` for Oracle |
| Regenerating `ora-irc-cx-userid` per request | Creates unnecessary session fragmentation | Generate once per connector instance, reuse across all requests |
| Not handling empty `ExternalDescriptionStr` | Concatenation produces empty `raw_html` → enrichment fails | Filter empty strings before joining; log warning if all three fields are empty |
| Top-level `limit`/`offset` query params | Same 25 jobs every page — outer `items[]` has only one container | Put lowercase `offset` and `limit` in the `finder` string; stop when `offset >= TotalJobsCount` |
| PascalCase `Offset`/`Limit` in finder | HTTP 400 — invalid finder parameter | Use lowercase `offset` and `limit` inside the finder string |
| Fetching detail for all jobs without age filter | Wastes HTTP + 0.5s sleep on stale postings; queues them for enrichment | Pre-filter on list `PostedDate`; use `max_posted_age_days` in `platform_config` |

---

## 11. Comparison to Workday

| Aspect | Workday | Oracle HCM |
|---|---|---|
| Auth headers | None required | Three required headers |
| List call method | `POST` with JSON body | `GET` with query params |
| Response nesting | Flat `jobPostings[]` | Nested `items[0].requisitionList[]` |
| Stable ID field | `jobReqId` | `Id` |
| Date format | `MM/DD/YYYY` | `YYYY-MM-DD` |
| Description location | `jobPostingInfo.jobDescription` | Three separate `External*Str` fields |
| Rate limit | ~0.35s safe | ~0.5s required |
| SSO risk | Rare | Moderate — check 302 explicitly |
| Pagination control | `total` + offset query param | `TotalJobsCount` + lowercase `offset`/`limit` in finder string |
| Posted-date filter | `max_posted_age_days` in `platform_config` | Same config key; pre-detail filter on list `PostedDate` |
| Detail finder syntax | URL path appended | `ById;Id="{id}",siteNumber=CX_1` query param |
