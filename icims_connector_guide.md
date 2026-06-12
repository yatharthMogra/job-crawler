# iCIMS Connector — Implementation Guide

This document covers everything needed to implement an iCIMS connector for the job ingestion
pipeline. iCIMS is architecturally distinct from Workday and Oracle HCM — there is no public
JSON REST API. Job discovery and extraction are done via XML sitemap parsing and HTML scraping.

Example URL provided: `https://careers-sri.icims.com/jobs/search?ss=1&searchRelation=keyword_all`
Breaking down: `careers-sri` = subdomain where `sri` is the company slug. iCIMS hosts career
sites at `https://careers-{slug}.icims.com/`.

Companies using iCIMS: UPS, Target, Lowe's, Comcast, CVS Health, SRI International.
Primarily large traditional enterprises, not tech startups.

---

## 1. Critical Architectural Difference

Workday and Oracle HCM both expose structured JSON REST APIs. iCIMS does not.

| Aspect | Workday / Oracle HCM | iCIMS |
|---|---|---|
| Data format | JSON REST API | XML sitemap + HTML pages |
| Job discovery | Paginated JSON list endpoint | `sitemap.xml` |
| Job details | JSON detail endpoint | HTML page (`?in_iframe=1`) |
| Parsing | `response.json()` | BeautifulSoup / lxml |
| Structured data | Yes (JSON keys) | No (text label parsing) |
| Auth headers | Oracle: 3 required / Workday: none | User-Agent only |

This means the connector requires BeautifulSoup (or lxml) as an additional dependency, and
field extraction is positional/label-based rather than key-based. Field availability varies
by iCIMS portal configuration and must be handled gracefully.

---

## 2. Board Token Structure

| Component | Description | Example |
|---|---|---|
| `board_token` | Company slug in the iCIMS subdomain | `sri`, `bcore`, `ups` |
| `platform_config.url_pattern` | Subdomain prefix pattern | `careers-{slug}` (default) |
| `platform_config.base_url` | Full base URL (only for custom domains) | `https://jobs.customdomain.com` |

Standard URL: `https://careers-{board_token}.icims.com`

Some companies use non-standard patterns. If the company's careers page uses a custom domain
pointing at iCIMS, or a different prefix pattern (e.g., `{slug}-jobs.icims.com`), store the
full base URL in `platform_config.base_url` and the connector uses that directly.

```python
def _base_url(self, company: Company) -> str:
    config = company.platform_config or {}
    if config.get("base_url"):
        return config["base_url"].rstrip("/")
    pattern = config.get("url_pattern", "careers-{slug}")
    subdomain = pattern.replace("{slug}", company.board_token)
    return f"https://{subdomain}.icims.com"
```

---

## 3. Two-Step Fetch: Sitemap → HTML Detail

Unlike Workday/Oracle (list endpoint → detail endpoint), iCIMS uses:

**Step 1 — Sitemap discovery (XML):**
`GET https://{base}/sitemap.xml`

Returns an XML file listing every public page on the career site, including all job URLs with
`lastmod` timestamps. A single request gets all job URLs — no pagination required at this
stage. This is the most efficient discovery method.

**Step 2 — Per-job HTML detail:**
`GET https://{base}/jobs/{job_id}/{slug}/job?in_iframe=1`

The `?in_iframe=1` parameter strips the company website wrapper, returning just the iCIMS
job detail HTML. This is essential — without it, the page includes the full company website
navigation which varies by company and makes parsing unreliable.

---

## 4. API Reference

### 4.1 Sitemap (Step 1 — job discovery)

```
GET https://{base}/sitemap.xml
```

No headers required beyond a standard User-Agent.

**Response shape (XML):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://careers-sri.icims.com/jobs/3421/software-engineer/job</loc>
    <lastmod>2026-06-05T14:23:00+00:00</lastmod>
  </url>
  <url>
    <loc>https://careers-sri.icims.com/jobs/3388/research-scientist/job</loc>
    <lastmod>2026-06-01T09:00:00+00:00</lastmod>
  </url>
  <!-- non-job pages also appear — filter for /jobs/ URLs only -->
  <url>
    <loc>https://careers-sri.icims.com/jobs/search</loc>
    <lastmod>2026-06-08</lastmod>
  </url>
</urlset>
```

**Filtering job URLs from sitemap:**
- Include only URLs where path contains `/jobs/` AND path ends with `/job` (not `/search`,
  `/apply`, etc.)
- Exclude: `/jobs/search`, `/jobs/search?*`, application pages

**Stable job ID extraction from URL:**
```
https://careers-sri.icims.com/jobs/3421/software-engineer/job
                                      ^^^^
                                      This numeric ID is stable
```

Pattern: `/jobs/{id}/{slug}/job` — the numeric `{id}` is the iCIMS job requisition ID.
The `{slug}` is derived from the title and changes if the title is edited. Always key on
the numeric ID, never the slug.

```python
import re

def extract_job_id(url: str) -> str | None:
    match = re.search(r'/jobs/(\d+)/', url)
    return match.group(1) if match else None
```

**`lastmod` as posted_at:**
iCIMS does not expose a separate "posted date" in the sitemap. `lastmod` is the closest
proxy — it reflects when the job page was last updated, which for new postings typically
matches the posting date. For long-running postings, `lastmod` updates when the description
is edited. Parse as ISO 8601 datetime; it may be date-only (`YYYY-MM-DD`) or full datetime.

```python
from datetime import datetime, timezone
from dateutil import parser as dateutil_parser

def parse_icims_date(date_str: str | None) -> datetime | None:
    if not date_str:
        return None
    try:
        dt = dateutil_parser.parse(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None
```

---

### 4.2 Job Detail Page (Step 2 — per-job HTML)

```
GET https://{base}/jobs/{job_id}/{slug}/job?in_iframe=1
```

**Required header:**
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

A desktop User-Agent is required. Without it, some iCIMS portals redirect to a mobile version
with different HTML structure. No other headers needed.

**HTML structure:**

iCIMS uses a consistent but not immutable HTML structure. All iCIMS-specific elements use
CSS classes prefixed with `iCIMS_`. Field values follow a label → value pattern.

```html
<!-- Job title -->
<h1 class="iCIMS_Header">Software Engineer, AI Systems</h1>

<!-- Metadata: label followed immediately by value in sibling or adjacent element -->
<span class="iCIMS_Expandable_Label">Job ID:</span>
<span class="iCIMS_Expandable_Field">3421</span>

<span class="iCIMS_Expandable_Label">Job Locations:</span>
<span class="iCIMS_Expandable_Field">Menlo Park, CA</span>

<span class="iCIMS_Expandable_Label">Type:</span>
<span class="iCIMS_Expandable_Field">Full-Time</span>

<span class="iCIMS_Expandable_Label">Category:</span>
<span class="iCIMS_Expandable_Field">Engineering</span>

<!-- Description — expandable container -->
<div class="iCIMS_Expandable_Container" id="jobDescription">
    <p>We are looking for a software engineer...</p>
    <ul><li>5+ years Python experience...</li></ul>
</div>

<!-- Apply button — for posting_url -->
<a class="iCIMS_Button" href="/jobs/3421/software-engineer/job?mode=apply">Apply Now</a>
```

**Label names vary by portal configuration:** Some portals use "Job Locations", others use
"Location". Some have "Department", others "Category". Always try multiple selectors and
fall back to None gracefully.

---

## 5. HTML Parsing Implementation

### 5.1 Field extraction helpers

```python
from bs4 import BeautifulSoup, Tag
from typing import Optional


def _find_field_after_label(soup: BeautifulSoup, label_text: str) -> Optional[str]:
    """
    iCIMS stores metadata as: <label>Field Name:</label> <value>Text</value>
    Find the label by text content, then return the adjacent value text.
    Handles multiple selector patterns across iCIMS portal variants.
    """
    # Pattern 1: iCIMS_Expandable_Label → iCIMS_Expandable_Field (most common)
    for label in soup.find_all(class_="iCIMS_Expandable_Label"):
        if label_text.lower() in label.get_text(strip=True).lower():
            value_el = label.find_next(class_="iCIMS_Expandable_Field")
            if value_el:
                return value_el.get_text(strip=True) or None

    # Pattern 2: Generic text label → next sibling
    for el in soup.find_all(string=lambda t: t and label_text.lower() in t.lower()):
        parent = el.parent
        if parent:
            sibling = parent.find_next_sibling()
            if sibling:
                text = sibling.get_text(strip=True)
                if text:
                    return text

    return None


def _extract_title(soup: BeautifulSoup) -> Optional[str]:
    h1 = soup.find("h1", class_=lambda c: c and "iCIMS" in c)
    if not h1:
        h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else None


def _extract_description_html(soup: BeautifulSoup) -> str:
    """
    Extract raw HTML from the job description container.
    iCIMS uses iCIMS_Expandable_Container for the expandable description section.
    Multiple containers may exist (overview, responsibilities, qualifications).
    Concatenate all — same pattern as Oracle HCM's three-field concat.
    """
    containers = soup.find_all(class_="iCIMS_Expandable_Container")
    if not containers:
        # Fallback: find any div with 'description' in its id or class
        containers = soup.find_all(
            lambda tag: tag.name == "div" and
            any("description" in str(v).lower() for v in [tag.get("id", ""), tag.get("class", "")])
        )

    parts = []
    for container in containers:
        inner = container.decode_contents().strip()
        if inner:
            parts.append(inner)

    return "\n".join(parts)


def _extract_employment_type(soup: BeautifulSoup) -> Optional[str]:
    """Try multiple label variants iCIMS portals use."""
    for label in ("Type", "Job Type", "Employment Type", "Schedule"):
        val = _find_field_after_label(soup, label)
        if val:
            return val
    return None


def _extract_location(soup: BeautifulSoup) -> Optional[str]:
    for label in ("Job Locations", "Location", "Job Location"):
        val = _find_field_after_label(soup, label)
        if val:
            return val
    return None


def _extract_department(soup: BeautifulSoup) -> Optional[str]:
    for label in ("Category", "Department", "Job Category", "Function"):
        val = _find_field_after_label(soup, label)
        if val:
            return val
    return None
```

---

## 6. Connector Implementation

```python
# app/ingestion/connectors/icims.py

import asyncio
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from app.ingestion.connectors.base import BaseConnector
from app.ingestion.exceptions import ConnectorFetchError, ParseError
from app.models.company import Company
import structlog

log = structlog.get_logger()

DETAIL_DELAY = 2.0      # seconds between detail calls — more conservative than Workday/Oracle
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


class ICIMSConnector(BaseConnector):

    def _base_url(self, company: Company) -> str:
        config = company.platform_config or {}
        if config.get("base_url"):
            return config["base_url"].rstrip("/")
        pattern = config.get("url_pattern", "careers-{slug}")
        subdomain = pattern.replace("{slug}", company.board_token)
        return f"https://{subdomain}.icims.com"

    async def fetch_jobs(self, company: Company) -> list[dict]:
        base_url = self._base_url(company)

        # Step 1: Discover all job URLs via sitemap
        job_entries = await self._fetch_sitemap(base_url)
        if not job_entries:
            log.warning("icims_empty_sitemap", company=company.name, base_url=base_url)
            return []

        # Step 2: Fetch HTML detail for each job
        results = []
        async with httpx.AsyncClient(
            timeout=30,
            headers={"User-Agent": DESKTOP_UA},
            follow_redirects=True,
        ) as client:
            for entry in job_entries:
                job_id = entry["job_id"]
                job_url = entry["url"]
                lastmod = entry["lastmod"]
                try:
                    detail = await self._fetch_detail(client, job_url)
                    merged = {
                        "id": job_id,
                        "job_id": job_id,
                        "sitemap_url": job_url,
                        "lastmod": lastmod,
                        **detail,
                    }
                    results.append(merged)
                except ConnectorFetchError as e:
                    log.warning(
                        "icims_detail_fetch_failed",
                        company=company.name,
                        job_id=job_id,
                        error=str(e),
                    )
                    continue
                except Exception as e:
                    log.warning(
                        "icims_detail_unexpected",
                        company=company.name,
                        job_id=job_id,
                        error=str(e),
                    )
                    continue
                await asyncio.sleep(DETAIL_DELAY)

        return results

    async def _fetch_sitemap(self, base_url: str) -> list[dict]:
        """
        Fetch and parse sitemap.xml, returning job entries only.
        Each entry: {"job_id": str, "url": str, "lastmod": str | None}
        """
        sitemap_url = f"{base_url}/sitemap.xml"
        async with httpx.AsyncClient(
            timeout=30,
            headers={"User-Agent": DESKTOP_UA},
            follow_redirects=True,
        ) as client:
            response = await client.get(sitemap_url)

        if response.status_code == 404:
            # Some iCIMS portals don't expose sitemap — fall back to HTML pagination
            log.info("icims_sitemap_not_found_will_paginate", url=sitemap_url)
            return await self._fetch_via_pagination(base_url)

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"iCIMS sitemap failed: {response.status_code}", response.status_code
            )

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as e:
            raise ParseError(f"iCIMS sitemap XML parse error: {e}")

        entries = []
        for url_el in root.findall(f"{{{SITEMAP_NS}}}url"):
            loc_el = url_el.find(f"{{{SITEMAP_NS}}}loc")
            lastmod_el = url_el.find(f"{{{SITEMAP_NS}}}lastmod")
            if loc_el is None:
                continue

            loc = loc_el.text or ""
            # Keep only job detail pages — /jobs/{id}/{slug}/job
            if not re.search(r"/jobs/\d+/.+/job$", loc):
                continue

            job_id = _extract_job_id_from_url(loc)
            if not job_id:
                continue

            entries.append({
                "job_id": job_id,
                "url": loc,
                "lastmod": lastmod_el.text if lastmod_el is not None else None,
            })

        return entries

    async def _fetch_via_pagination(self, base_url: str) -> list[dict]:
        """
        Fallback: paginate through the HTML job listing when sitemap is unavailable.
        Uses ?pr={page}&in_iframe=1 pagination (pr=0 is first page).
        """
        entries = []
        page = 0

        async with httpx.AsyncClient(
            timeout=30,
            headers={"User-Agent": DESKTOP_UA},
            follow_redirects=True,
        ) as client:
            while page <= 100:  # safety cap
                url = f"{base_url}/jobs/search?pr={page}&in_iframe=1"
                response = await client.get(url)
                if response.status_code != 200:
                    break

                soup = BeautifulSoup(response.content, "html.parser")
                links = soup.select("a.iCIMS_Anchor[href*='/jobs/']")
                if not links:
                    break

                for link in links:
                    href = link.get("href", "")
                    if not re.search(r"/jobs/\d+/.+/job", href):
                        continue
                    job_id = _extract_job_id_from_url(href)
                    if not job_id:
                        continue
                    # Normalize to absolute URL
                    if href.startswith("/"):
                        href = f"{base_url}{href}"
                    entries.append({"job_id": job_id, "url": href, "lastmod": None})

                page += 1
                await asyncio.sleep(DETAIL_DELAY)

        return entries

    async def _fetch_detail(self, client: httpx.AsyncClient, job_url: str) -> dict:
        """
        Fetch and parse the HTML detail page for a single job.
        Returns a dict with parsed fields ready for merging.
        """
        detail_url = f"{job_url}?in_iframe=1"
        response = await client.get(detail_url)

        if response.status_code == 429:
            await asyncio.sleep(5.0)
            response = await client.get(detail_url)

        if response.status_code == 404:
            raise ConnectorFetchError(f"iCIMS job 404: {job_url}", 404)

        if response.status_code != 200:
            raise ConnectorFetchError(
                f"iCIMS detail failed {response.status_code}: {job_url}",
                response.status_code,
            )

        soup = BeautifulSoup(response.content, "html.parser")

        return {
            "title": _extract_title(soup),
            "location": _extract_location(soup),
            "department": _extract_department(soup),
            "employment_type_raw": _extract_employment_type(soup),
            "raw_html": _extract_description_html(soup),
            "detail_url": detail_url,
        }


# ── Helpers ──────────────────────────────────────────────────────────────────

def _extract_job_id_from_url(url: str) -> Optional[str]:
    match = re.search(r"/jobs/(\d+)/", url)
    return match.group(1) if match else None
```

---

## 7. Deterministic Extraction

Add `_extract_icims` to `app/ingestion/extractor/deterministic.py`:

```python
from dateutil import parser as dateutil_parser
from datetime import timezone


def _parse_icims_date(date_str: str | None) -> datetime | None:
    """Parse iCIMS lastmod timestamp — ISO 8601 date or datetime."""
    if not date_str:
        return None
    try:
        dt = dateutil_parser.parse(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def _extract_icims_employment_type(raw: str | None) -> str | None:
    if not raw:
        return None
    raw_lower = raw.lower()
    if "full" in raw_lower:
        return "Full-time"
    if "part" in raw_lower:
        return "Part-time"
    if "intern" in raw_lower:
        return "Internship"
    if "contract" in raw_lower:
        return "Contract"
    if "temporary" in raw_lower or "temp" in raw_lower:
        return "Temporary"
    return raw  # return as-is if no mapping found


def _extract_icims(job: dict, company=None) -> dict:
    """
    Deterministic extraction for iCIMS jobs.
    Input job dict has keys from the connector's merged output.
    """
    # Posting URL: use the clean job URL without in_iframe parameter
    posting_url = job.get("sitemap_url") or job.get("detail_url", "").replace("?in_iframe=1", "")

    return {
        "external_job_id": str(job["id"]),
        "title": job.get("title"),
        "location": job.get("location"),
        "department": job.get("department"),
        "posting_url": posting_url,
        "posted_at": _parse_icims_date(job.get("lastmod")),
        "employment_type": _extract_icims_employment_type(job.get("employment_type_raw")),
        "raw_html": job.get("raw_html", ""),
    }
```

**Register:**
```python
# In FIELD_EXTRACTORS:
"icims": _extract_icims,

# In CONNECTORS:
"icims": ICIMSConnector,
```

**Add dependency:**
```
# requirements.txt or pyproject.toml
beautifulsoup4>=4.12.0
lxml>=4.9.0          # faster BeautifulSoup parser
python-dateutil>=2.8.0
```

---

## 8. Field Mapping Reference

| Common field | iCIMS source |
|---|---|
| `external_job_id` | Numeric ID from URL path `/jobs/{id}/` |
| `title` | `<h1 class="iCIMS_Header">` or first `<h1>` |
| `location` | Label "Job Locations" / "Location" → adjacent value |
| `department` | Label "Category" / "Department" → adjacent value |
| `posting_url` | `sitemap.xml` `<loc>` value (without `?in_iframe=1`) |
| `posted_at` | `sitemap.xml` `<lastmod>` (ISO 8601, may be date-only) |
| `employment_type` | Label "Type" / "Job Type" → normalized |
| `raw_html` | Inner HTML of `.iCIMS_Expandable_Container` elements, concatenated |

---

## 9. `companies.json` Seed Format

**Standard subdomain pattern:**
```json
{
  "company": "SRI International",
  "platform": "icims",
  "board_token": "sri",
  "platform_config": {}
}
```
Generates base URL: `https://careers-sri.icims.com`

**Non-standard subdomain prefix:**
```json
{
  "company": "Example Corp",
  "platform": "icims",
  "board_token": "example",
  "platform_config": {
    "url_pattern": "{slug}-jobs"
  }
}
```
Generates base URL: `https://example-jobs.icims.com`

**Custom domain (iCIMS hosted on company domain):**
```json
{
  "company": "Target",
  "platform": "icims",
  "board_token": "target",
  "platform_config": {
    "base_url": "https://jobs.target.com"
  }
}
```

**Finding a company's iCIMS subdomain:**
1. Visit the company's careers page
2. The iCIMS career portal URL is usually embedded in an iframe or linked directly
3. Look for URLs containing `icims.com` in the page source or network requests
4. The subdomain before `.icims.com` is the company's iCIMS identifier

---

## 10. Tests

| Test | What to verify |
|---|---|
| `test_icims_sitemap_success` | Sitemap XML parsed, job URLs filtered correctly, non-job URLs excluded |
| `test_icims_sitemap_url_filter` | Only `/jobs/{id}/{slug}/job` paths included, not `/jobs/search` etc. |
| `test_icims_job_id_extraction` | `/jobs/3421/software-engineer/job` → `"3421"` |
| `test_icims_sitemap_404_falls_back` | 404 on sitemap triggers HTML pagination fallback |
| `test_icims_pagination_fallback` | HTML pagination collects jobs across multiple pages |
| `test_icims_detail_parse_standard` | All four fields extracted from typical iCIMS HTML |
| `test_icims_detail_missing_fields` | Missing location/department/type returns None, not raises |
| `test_icims_detail_429_retry` | 429 triggers 5s sleep and one retry |
| `test_icims_detail_404_skips` | 404 on detail logs warning and continues remaining jobs |
| `test_icims_description_concat` | Multiple `.iCIMS_Expandable_Container` elements joined |
| `test_icims_date_parse_date_only` | `"2026-06-05"` → UTC datetime |
| `test_icims_date_parse_full_iso` | `"2026-06-05T14:23:00+00:00"` → correct UTC datetime |
| `test_icims_date_parse_none` | `None` input → `None` output |
| `test_icims_employment_type_mapping` | "Full-Time" → "Full-time", "Intern" → "Internship" |
| `test_icims_posting_url_no_iframe_param` | posting_url never contains `?in_iframe=1` |
| `test_icims_user_agent_sent` | Desktop User-Agent present on every request |
| `test_icims_detail_delay_between_calls` | 2s delay enforced between detail fetches (mock sleep) |

---

## 11. iCIMS-Specific Anti-Patterns

| Anti-pattern | What happens | Correct approach |
|---|---|---|
| Using JSON parsing on iCIMS responses | `response.json()` raises, there is no JSON | Use BeautifulSoup to parse HTML |
| Keying on the URL slug for dedup | Title edit changes slug, creates duplicate jobs | Always key on the numeric ID from the path |
| Fetching detail URL without `?in_iframe=1` | Returns full company website wrapper with varying HTML structure | Always append `?in_iframe=1` |
| Omitting User-Agent header | Some portals redirect to mobile site with different HTML structure | Always send desktop User-Agent |
| Using 0.5s delay (Workday/Oracle rate) | iCIMS portals use Cloudflare and rate-limit aggressively | Use 2.0s minimum between detail calls |
| Hard-coding `careers-{slug}.icims.com` | Some companies use `{slug}-jobs`, custom domains, or other patterns | Use `platform_config.url_pattern` / `base_url` |
| Assuming `lastmod` = exact post date | `lastmod` updates on description edits — it's approximate | Treat `lastmod` as the best available date proxy, not exact |
| Treating missing HTML fields as errors | iCIMS portal configuration varies — location, department may be absent | Return `None` for missing fields, never raise |
| Scraping the paginated listing without sitemap fallback | Fails silently if sitemap exists and is the correct entry point | Always try sitemap first; paginate only if sitemap returns 404 |
| Including `?in_iframe=1` in `posting_url` | Users clicking the link see raw iframe content without company branding | Strip `?in_iframe=1` from the stored `posting_url` |

---

## 12. Platform Comparison

| Aspect | Workday | Oracle HCM | iCIMS |
|---|---|---|---|
| Data format | JSON (CXS API) | JSON (hcmRestApi) | XML sitemap + HTML |
| Discovery method | POST list endpoint | GET list endpoint | `sitemap.xml` |
| Detail method | GET per-job endpoint | GET per-job endpoint | GET HTML per-job |
| Parsing | `response.json()` | `response.json()` | BeautifulSoup |
| Stable ID field | `jobReqId` | `Id` (numeric) | Numeric from URL path |
| Date field | `postedOn` (MM/DD/YYYY) | `PostedDate` (YYYY-MM-DD) | `lastmod` from sitemap (ISO 8601) |
| Description location | `jobPostingInfo.jobDescription` | Three `External*Str` fields | `.iCIMS_Expandable_Container` HTML |
| Auth headers | None | 3 required (`ora-irc-*`) | User-Agent only |
| Rate limit | 0.35s | 0.5s | 2.0s |
| Structured data | Yes | Yes | No — label parsing |
| Pagination | Offset-based | Offset + `hasMore` | Sitemap (no pagination) |
| SSO risk | Moderate | Moderate | Low (public sitemap is always accessible) |
| Cloudflare risk | Low | Low | Moderate for large enterprises |
| Additional dependency | None | None | `beautifulsoup4`, `python-dateutil` |
