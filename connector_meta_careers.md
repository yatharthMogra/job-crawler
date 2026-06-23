# Meta Careers Connector — Integration Guide

## Overview

Confirmed directly: Meta's careers site (`metacareers.com`) is a **client-side-rendered
React SPA**, same category as Uber and Tesla. Fetching the search page
(`metacareers.com/jobsearch/`) returns only meta tags and a canonical link — zero job
data in the raw HTML. The actual job list and detail content are loaded via JavaScript
after page load, meaning this connector requires DevTools reconnaissance to find the
internal API, not a simple HTML scrape.

**Difficulty: Medium-high.** Same category as Uber and Tesla — reconnaissance-first,
build against whatever you actually observe, not against guessed shapes.

---

## Confirmed Facts (From Direct Inspection)

- **Search page:** `https://www.metacareers.com/jobsearch/` — confirmed pure SPA shell,
  no job content in raw HTML.
- **No authentication observed** required to view listings.
- **Two distinct detail URL patterns observed** in search results, which is worth
  noting as a possible signal of two different underlying systems or a migration in
  progress:
  - `metacareers.com/jobs/{numeric-id}` (e.g. `/jobs/1079158160340219`)
  - `metacareers.com/profile/job_details/{numeric-id}` (e.g.
    `/profile/job_details/727671609895617`)
  Confirm during reconnaissance whether these are interchangeable aliases for the same
  underlying job record or represent genuinely different systems (e.g. one for
  external candidates, one tied to a logged-in candidate profile flow).
- **Full structured job descriptions are indexed and appear in search results** —
  qualifications, compensation ranges (e.g. "$58.65/hour to $181,000/year + bonus +
  equity + benefits"), and full EEO statement text all appeared in plain-text search
  snippets. This strongly suggests the detail pages **are** server-rendered or
  pre-rendered for SEO purposes even though the search/list page is not — a common
  pattern where a company server-renders individual job pages (for search engine
  indexing and link-sharing) while keeping the interactive search experience
  client-rendered. **Confirm this directly** by fetching one live, currently-open job
  detail URL plainly — if confirmed, detail fetching may be much easier than list
  fetching for this connector.
- One previously-indexed job ID (`1079158160340219`) returned a 404 on direct fetch
  during this research — expected, since individual postings close and get removed
  reasonably quickly. Don't treat a single 404 as a sign the URL pattern is wrong; it
  likely just means the job filled.

---

## Reconnaissance Step (Mandatory Before Writing Code)

1. **First, test the detail-page hypothesis** — fetch a currently-live job detail URL
   (find one via a fresh search) plainly, no browser automation. If full job content
   appears in the raw HTML, detail fetching is solved immediately and cheaply, same
   tier of difficulty as Apple or Google. This is worth checking before assuming the
   whole connector is Uber/Tesla-tier difficulty — it may only be the *list* step that's
   hard.
2. **For the list/search step**, open `metacareers.com/jobsearch/` in a real browser
   with DevTools open, Network tab, filter to Fetch/XHR/GraphQL. Meta's products
   commonly use GraphQL internally — expect a POST to a single endpoint with an
   operation name, rather than a REST-style GET with query params.
3. Apply a filter (team, technology, location) and observe how the request payload
   changes — this gives you the filter parameter names.
4. Check whether the list response includes enough data to construct detail URLs
   directly (numeric ID + title slug) without needing a separate detail call per job,
   especially if reconnaissance confirms detail pages are server-rendered — in that
   case you only need the list call to enumerate IDs, then plain fetches for detail.
5. Check for rate-limiting signals and bot-protection challenge pages. Meta is a
   large, security-conscious organization; apply the same conservative posture as
   Uber/Tesla — test a plain request first, escalate only if actually blocked.

---

## Connector Skeleton (Fill In After Reconnaissance)

```python
# job_ingestion/app/ingestion/connectors/meta_careers.py

import httpx
from bs4 import BeautifulSoup
from ..base import BaseConnector
from ..models import RawJob

# CONFIRM via DevTools before filling in — structural placeholder only.
META_CAREERS_API = "https://www.metacareers.com/graphql"  # placeholder, likely GraphQL


class MetaCareersConnector(BaseConnector):
    ats_type = "meta_careers"
    name = "Meta Careers"

    async def fetch_jobs(self) -> list[RawJob]:
        async with httpx.AsyncClient(
            timeout=20.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"},
        ) as client:
            job_ids = await self._fetch_all_job_ids(client)
            return await self._fetch_details(client, job_ids)

    async def _fetch_all_job_ids(self, client: httpx.AsyncClient) -> list[dict]:
        """
        Confirm actual list mechanism (GraphQL POST vs REST GET) before
        implementing. Returns minimal records (id, title, url) — full
        description comes from the detail fetch if detail pages are
        confirmed server-rendered.
        """
        raise NotImplementedError("Confirm Meta's list API shape via DevTools first")

    async def _fetch_details(
        self, client: httpx.AsyncClient, job_ids: list[dict]
    ) -> list[RawJob]:
        raw_jobs = []
        for job in job_ids:
            # If reconnaissance confirms detail pages are server-rendered,
            # this is a plain GET + BeautifulSoup parse — much simpler than
            # an API-based detail fetch.
            resp = await client.get(job["url"])
            if resp.status_code != 200:
                continue
            raw_jobs.append(self._parse_detail(job, resp.text))
        return raw_jobs

    def _parse_detail(self, job: dict, html: str) -> RawJob:
        soup = BeautifulSoup(html, "html.parser")
        # Confirm exact container selector against live page.
        description_el = soup.select_one("[class*='job']") or soup.select_one("main")

        return RawJob(
            external_id=f"meta_{job['id']}",
            ats_type=self.ats_type,
            title=job.get("title", ""),
            company_name="Meta",
            job_location=job.get("location", ""),
            description_html=str(description_el) if description_el else "",
            job_url=job["url"],
            posted_at=None,  # confirm availability
        )
```

---

## Field Mapping (Tentative)

| Likely source | Your field |
|---|---|
| numeric job ID from URL | `external_id` (prefix `meta_`) |
| title | `title` |
| (constant) | `company_name` = "Meta" |
| location | `job_location` — Meta hires globally across many offices; apply the same
  international location-parsing caution as Uber/Amazon |
| compensation range (confirmed present in search snippets, e.g. "$58.65/hour to
  $181,000/year") | `salary_min`/`salary_max` — this is genuinely useful structured
  comp data if it's reliably present on detail pages, worth extracting directly rather
  than relying solely on LLM enrichment to parse it from prose |
| qualifications text | fold into `raw_html` for enrichment |

---

## Things Specific to Meta Worth Checking

- **Two URL patterns (`/jobs/{id}` and `/profile/job_details/{id}`)** — resolve this
  during reconnaissance. It's possible one is the canonical public-facing URL and the
  other is what renders inside a logged-in candidate's session; if so, standardize on
  whichever one works for an unauthenticated request.
- **Meta hires across distinct product surfaces** (Facebook/Instagram core apps,
  Reality Labs/VR/AR, AI/Superintelligence Labs, infrastructure) — confirm whether the
  list API supports filtering by these areas, similar to Tesla's business-unit
  question, so you can scope to what's relevant to your software/ML/data user base
  without pulling in non-engineering roles.
- **AI-specific roles appear to be a major, actively-growing category** based on search
  results (Superintelligence Labs, AssetGen 3D foundation models, etc.) — high
  relevance for your `ML_ENGINEER_FULLTIME` pool if reachable via a clean filter.

---

## Testing Checklist

- [ ] Confirmed whether detail pages are server-rendered (test before assuming
      Uber/Tesla-tier difficulty applies to the whole connector)
- [ ] Confirmed actual list API shape (GraphQL vs REST) via DevTools
- [ ] Resolved the two detail URL pattern question
- [ ] Confirmed filter parameter names for team/area scoping
- [ ] Tested whether plain `httpx` works for both list and detail steps before adding
      any browser-impersonation complexity
- [ ] Confirmed compensation field reliability and format for direct extraction
- [ ] Location parsing tested against Meta's actual global office location strings

---

## Effort Estimate

Cannot be precisely bounded until the detail-page-rendering question is answered — that
single fact determines whether this is a half-day connector (if detail pages are
server-rendered and only the list step needs reconnaissance) or a multi-day Uber-tier
project (if both list and detail require API reverse-engineering). Resolve that question
first, before estimating further.
