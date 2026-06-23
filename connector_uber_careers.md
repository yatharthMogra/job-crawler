# Netflix Careers Connector — Integration Guide

## Overview

Good news, and a different shape of finding than Google, Uber, or Tesla: **Netflix does
not run a custom-built career site.** It runs on **Eightfold AI**, a third-party
talent-intelligence/career-site vendor — confirmed directly by inspecting
`explore.jobs.netflix.net/careers`, which returned embedded config keys unique to
Eightfold's product (`hideEightfoldBranding`, `pcsx-hero-image-height`,
`pcs-personalization-bar-background`, etc.) and a URL structure
(`?domain=netflix.com&pid={id}&query=...`) matching Eightfold's known pattern.

This means Netflix is architecturally closer to your **SmartRecruiters or Lever**
connectors than to Google/Uber/Tesla. It's not a bespoke in-house build requiring
per-company reverse-engineering — it's **one more ATS platform**, and if other
companies in your pipeline also run Eightfold, this connector covers all of them, not
just Netflix.

**Difficulty: Low-Medium.** Lower than initially expected for a "big tech direct"
company, because the actual integration target is a well-understood third-party
platform with a documented (if unofficial) unauthenticated REST API.

---

## Confirmed Facts

- **Platform:** Eightfold AI (PCS / PCSX career site product)
- **Netflix's instance:** `explore.jobs.netflix.net` (note: NOT `jobs.netflix.com`,
  which is Netflix's own marketing/landing domain that links out to the Eightfold-hosted
  search experience)
- **Domain parameter:** `netflix.com` — confirmed via the `?domain=netflix.com` query
  param present on real Netflix job search URLs
- **No login required** to view job listings
- **Job data appears directly in page-embedded JSON** (`"positions": [{"id":
  790316292023, "name": "Software Engineer 5 – Agent Platform...", "location": "USA -
  Remote", "department": "Data & Insights", ...}]`) — confirmed via direct search result
  content, meaning this is at least partially server-rendered or very easily reachable,
  unlike Uber/Tesla's pure client-side rendering

---

## The Eightfold API — Two Possible Patterns

Eightfold-powered career sites use one of two API shapes depending on which Eightfold
product version a given company is on. **Confirm which one Netflix uses during
reconnaissance** — don't assume; the pattern below is based on third-party documentation
of the platform generally, not confirmed specifically for Netflix's instance.

### Pattern A — SmartApply API (try first)

```
GET https://{company}.eightfold.ai/api/apply/v2/jobs?domain={domain}&hl=en&start=0
```

For a company hosted at the standard `{company}.eightfold.ai` subdomain. Response:

```json
{
  "positions": [
    {
      "id": 790316292023,
      "name": "Software Engineer 5 – Agent Platform, AI Platform",
      "location": "USA - Remote",
      "locations": ["USA - Remote"],
      "department": "Data & Insights",
      "business_unit": "...",
      "t_create": 1234567890,
      "t_update": 1234567890,
      "canonicalPositionUrl": "https://...",
      "job_description": "..."
    }
  ],
  "totalJobs": 412
}
```

Pagination: increment `start` by 10 (the typical default page size) until you've covered
`totalJobs`.

### Pattern B — PCSX API (fallback if A 404s)

```
GET https://{company}.eightfold.ai/api/pcsx/search?domain={domain}&...
```

Detail fetch (if description isn't in the list payload):

```
GET https://{company}.eightfold.ai/api/pcsx/position_details?position_id={id}&domain={domain}
```

### Netflix Specifically — Custom Domain Wrinkle

Netflix's instance is at `explore.jobs.netflix.net`, **not** the standard
`netflix.eightfold.ai` subdomain. This is a "custom domain" deployment — confirmed common
for larger Eightfold customers based on third-party documentation, which explicitly notes
companies can run Eightfold under `jobs.{company}.com`-style domains instead of the
default subdomain.

**This means the API base URL for Netflix is likely still the underlying
`netflix.eightfold.ai` host even though the public-facing site is on
`explore.jobs.netflix.net`** — custom domains are typically a DNS/proxy layer in front of
the same backend. Confirm this during reconnaissance:

1. Try `https://netflix.eightfold.ai/api/apply/v2/jobs?domain=netflix.com&hl=en&start=0`
   directly.
2. If that fails, open `explore.jobs.netflix.net/careers` in a browser with DevTools
   open, Network tab, and check what host the actual XHR calls target — it may proxy
   through `explore.jobs.netflix.net/api/...` instead of hitting `netflix.eightfold.ai`
   directly from the browser.
3. The `domain=netflix.com` query parameter is confirmed present in real URLs regardless
   of which host serves the API — keep this parameter in either case.

---

## Reconnaissance Step (Still Required Despite Good Documentation)

Third-party documentation of "how Eightfold generally works" is not the same as
"confirmed for Netflix's specific instance." Before writing the connector:

1. Try the SmartApply endpoint directly via `curl`/`httpx` with no special headers —
   per third-party reports this requires no auth and no browser. This is worth testing
   as a plain request first, unlike Uber/Tesla, since Eightfold's public job-search API
   is explicitly designed to be called by the career site's own frontend JS without a
   login wall.
2. If `netflix.eightfold.ai` doesn't resolve or 404s, open
   `explore.jobs.netflix.net/careers?domain=netflix.com` in DevTools and find the actual
   XHR call the page makes — confirm the real host and path.
3. Confirm whether `job_description` is populated in the list response or requires the
   detail endpoint — third-party docs show an empty `"job_description": ""` in at least
   one example (the Symetra fixture found during this research), suggesting detail may
   be needed even when other fields are present in the list call.
4. Confirm pagination behavior — `start`/`limit` style, and what the actual default
   page size is (third-party docs suggest 10, Eightfold's own official rate-limit docs
   for their authenticated B2B API mention up to 100 per page for some endpoints, but
   that's a different, authenticated API surface — don't conflate the two).
5. Check actual response headers for rate-limit signals. Third-party scraper
   documentation estimates "~100 requests/minute (unofficial)" for the public surface —
   treat this as an unverified community estimate, not a confirmed Netflix-specific
   limit, and start conservative regardless.

---

## Connector Implementation

```python
# job_ingestion/app/ingestion/connectors/eightfold.py
#
# Generic Eightfold connector — if other companies in your catalog also run
# Eightfold, this single connector class serves all of them via board_token +
# platform_config, same pattern as your multi-tenant Workday/SuccessFactors connectors.

import asyncio
import httpx
from ..base import BaseConnector
from ..models import RawJob

PAGE_SIZE = 10  # confirm actual default during reconnaissance


class EightfoldConnector(BaseConnector):
    ats_type = "eightfold"
    name = "Eightfold AI Career Site"

    def __init__(self, board_token: str, platform_config: dict):
        """
        platform_config must contain:
          - api_host: confirmed API host (e.g. "netflix.eightfold.ai" or
            "explore.jobs.netflix.net" if it proxies its own API)
          - domain: the `domain` query param value (e.g. "netflix.com")
        """
        self.board_token = board_token
        self.api_host = platform_config["api_host"]
        self.domain = platform_config["domain"]

    async def fetch_jobs(self) -> list[RawJob]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            summaries = await self._fetch_all_pages(client)
            return await self._enrich_with_details(client, summaries)

    async def _fetch_all_pages(self, client: httpx.AsyncClient) -> list[dict]:
        all_jobs = []
        start = 0
        while True:
            resp = await client.get(
                f"https://{self.api_host}/api/apply/v2/jobs",
                params={"domain": self.domain, "hl": "en", "start": start},
                headers={"Accept": "application/json"},
            )
            if resp.status_code == 404:
                # Fall back to PCSX pattern — confirm shape during reconnaissance
                # before implementing this branch.
                raise NotImplementedError(
                    f"SmartApply 404 for {self.board_token} — implement PCSX fallback"
                )
            resp.raise_for_status()
            data = resp.json()
            page_jobs = data.get("positions", [])
            all_jobs.extend(page_jobs)
            total = data.get("totalJobs", 0)
            start += PAGE_SIZE
            if start >= total or not page_jobs:
                break
            await asyncio.sleep(0.5)  # conservative pending confirmed rate limit
        return all_jobs

    async def _enrich_with_details(
        self, client: httpx.AsyncClient, summaries: list[dict]
    ) -> list[RawJob]:
        raw_jobs = []
        for job in summaries:
            description = job.get("job_description", "")
            if not description:
                description = await self._fetch_detail(client, job)
            raw_jobs.append(self._to_raw(job, description))
        return raw_jobs

    async def _fetch_detail(self, client: httpx.AsyncClient, job: dict) -> str:
        resp = await client.get(
            f"https://{self.api_host}/api/apply/v2/jobs/{job['id']}",
            params={"domain": self.domain, "hl": "en"},
        )
        if resp.status_code != 200:
            return ""
        return resp.json().get("job_description", "")

    def _to_raw(self, job: dict, description: str) -> RawJob:
        return RawJob(
            external_id=f"eightfold_{self.board_token}_{job['id']}",
            ats_type=self.ats_type,
            title=job.get("name", ""),
            company_name=self.board_token,
            job_location=job.get("location", ""),
            description_html=description,
            job_url=job.get("canonicalPositionUrl", ""),
            posted_at=job.get("t_create"),  # confirm: likely unix timestamp, needs conversion
            raw_metadata={
                "department": job.get("department"),
                "business_unit": job.get("business_unit"),
            },
        )
```

---

## companies.json Entry

```json
{
  "company": "Netflix",
  "platform": "eightfold",
  "board_token": "netflix",
  "fetch_tier": 2,
  "is_active": true,
  "platform_config": {
    "api_host": "netflix.eightfold.ai",
    "domain": "netflix.com"
  }
}
```

**Update `api_host` once reconnaissance confirms the real value** — the placeholder
above is the predicted standard-subdomain host; it may need to be
`explore.jobs.netflix.net` instead if Netflix's custom domain proxies its own API rather
than the browser calling `netflix.eightfold.ai` directly.

---

## Field Mapping

| Eightfold field | Your field |
|---|---|
| `id` | `external_id` (prefix `eightfold_{board_token}_`) |
| `name` | `title` |
| (board_token, e.g. "Netflix") | `company_name` |
| `location` / `locations` | `job_location` |
| `job_description` (list or detail call) | `raw_html` |
| `canonicalPositionUrl` | `job_url` |
| `t_create` | `posted_at` — **confirm unit**; likely Unix epoch seconds based on the
  Symetra fixture value (`1779143537`), needs conversion to your standard datetime format |
| `department` / `business_unit` | preserve in `raw_metadata` — useful secondary
  signal, similar treatment to Google's org-label and Tesla's team-filter discussion |

---

## Why This Connector Is Lower-Risk Than Google/Uber/Tesla

Worth being explicit about the reasoning, since it changes how much reconnaissance
caution to apply:

- **It's a platform, not a bespoke build.** The same engineering investment here likely
  unlocks every other Eightfold-hosted company in your pipeline (American Express and
  Symetra both appeared as Eightfold customers in this research, purely as
  examples turned up during the search — there may be others already in or destined
  for your `companies.json`). Check your existing/planned company list for other
  Eightfold tenants before treating this as a Netflix-only project.
- **The public job-search API is explicitly meant to be called by the career site's own
  frontend without authentication** — this is architecturally different from Uber/Tesla,
  where the SPA's data calls are incidentally exposed but not designed for arbitrary
  third-party consumption. Eightfold's public surface is closer in spirit to
  SmartRecruiters' or Lever's public API.
- **No bot-detection signal observed** in this research, unlike the confirmed Akamai
  wall on Tesla or the confirmed bot-defense split on Uber. Worth testing a plain
  request first rather than assuming you need browser automation.

---

## Testing Checklist

- [ ] Confirmed actual API host for Netflix's instance (`netflix.eightfold.ai` vs. a
      proxy through `explore.jobs.netflix.net`)
- [ ] Confirmed SmartApply vs. PCSX pattern via live request, not assumed
- [ ] Confirmed whether `job_description` is populated in list response or requires
      detail call
- [ ] Confirmed `t_create` field format and conversion to your datetime standard
- [ ] Confirmed actual page size and pagination parameter behavior
- [ ] Tested whether a plain unauthenticated request succeeds before adding any
      browser-impersonation complexity
- [ ] Checked `companies.json` / connector backlog for other Eightfold-hosted companies
      this same connector class could cover
- [ ] Fixture test captures real confirmed response shape

---

## Effort Estimate

1–2 days. Comparable to SmartRecruiters in shape — confirmed public API, predictable
JSON structure, no anti-bot measures observed — with the main open items being which of
the two Eightfold API patterns applies and the exact host/domain resolution for
Netflix's custom-domain deployment. Meaningfully lower-risk than Google, Uber, or Tesla
despite Netflix being a comparably large company, precisely because the underlying
platform is shared infrastructure rather than a custom build.