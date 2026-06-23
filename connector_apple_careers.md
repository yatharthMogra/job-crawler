# Apple Careers Connector — Integration Guide

## Overview

Confirmed directly: Apple's careers site (`jobs.apple.com`) is the **easiest of all
"direct company" connectors built so far** — easier than Google. A plain GET request to
the search page returns the full job list server-rendered in raw HTML: titles, role
numbers, locations, posting dates, and description snippets, all present with no
JavaScript execution, no login, and no API to reverse-engineer.

**Difficulty: Low.** Comparable to SmartRecruiters or Lever in simplicity — possibly
the single easiest connector in your "big tech" batch.

---

## Confirmed Facts (From Direct Inspection)

- **Search URL:** `https://jobs.apple.com/en-us/search?location=united-states-USA&team={team-slug}`
  — confirmed server-rendered with full job listings in the raw HTML response.
- **No authentication required** to view listings.
- **Team filter is a confirmed, working URL parameter** — e.g.
  `team=apps-and-frameworks-SFTWR-AF` correctly scoped results to that team in the
  fetched page. Apple organizes engineering into named teams with stable codes (`SFTWR`
  = general Software and Services, with sub-team suffixes like `-AF` for Apps and
  Frameworks, `-SQAT` for Software Quality/Automation/Tools, `-CLD` for Cloud and
  Infrastructure; `HRDWR` for Hardware). This is a strong, already-confirmed dimension
  for scoping crawls to engineering-relevant teams only.
- **Location filter confirmed working** — `location=united-states-USA`.
- **Each job card includes inline:** title, "Role Number" (e.g. `200626700-3337` — this
  is your stable external ID), posting date (e.g. "May 07, 2026"), location, weekly
  hours, and a truncated description snippet.
- **Detail page URL pattern confirmed:**
  ```
  https://jobs.apple.com/en-us/details/{role-number}/{title-slug}?team={team-code}
  ```
  e.g. `jobs.apple.com/en-us/details/200626700-3337/large-machine-learning-model-optimization-engineer-siml?team=SFTWR`
- **Result count shown on page** — "600+ Result(s)" — useful for sanity-checking crawl
  completeness, same pattern as Google's "N jobs matched" counter.
- **Pagination present** — result set is large (600+ for just one team filter), so the
  list page paginates; exact parameter not yet confirmed (see Reconnaissance below).

---

## What Still Needs Reconnaissance

1. **Pagination parameter.** Apple's search results clearly paginate (600+ results
   can't all be on one page), but the exact mechanism (`page=N` query param vs.
   infinite-scroll XHR for subsequent pages) wasn't confirmed in this pass — only the
   first page was fetched directly. Test by appending `&page=2` and checking if the
   server-rendered response changes accordingly; if it doesn't, check DevTools for a
   separate XHR call on scroll/pagination-click.
2. **Whether the detail page is also server-rendered.** Only the search/list page was
   directly confirmed in this research. Given the list page's strong server-rendering
   behavior, the detail page is likely the same, but confirm directly before assuming —
   fetch one real detail URL plainly and check for full job description content
   (responsibilities, minimum qualifications, preferred qualifications) in the raw HTML.
3. **Full list of relevant team codes.** Only a handful of team slugs were observed in
   this pass (`apps-and-frameworks-SFTWR-AF`, `software-quality-automation-and-tools-SFTWR-SQAT`,
   `cloud-and-infrastructure-SFTWR-CLD`). Apple's site has a "View all teams" expandable
   list in the filter sidebar — visit that to get the complete set of engineering-relevant
   team codes before deciding which ones to crawl for your product's audience
   (software/ML/data candidates).
4. **Rate limiting / pagination depth for 600+ results per team.** With multiple
   engineering teams each potentially having hundreds of open roles, total crawl volume
   across all relevant teams could be substantial. Confirm safe pagination pacing
   empirically rather than assuming.

---

## Recommended Architecture

```python
# job_ingestion/app/ingestion/connectors/apple_careers.py

import re
import httpx
from bs4 import BeautifulSoup
from ..base import BaseConnector
from ..models import RawJob

SEARCH_URL = "https://jobs.apple.com/en-us/search"

# Confirmed-relevant team codes for software/ML/data roles — expand this list
# after checking Apple's full "View all teams" sidebar during reconnaissance.
ENGINEERING_TEAMS = [
    "apps-and-frameworks-SFTWR-AF",
    "software-quality-automation-and-tools-SFTWR-SQAT",
    "cloud-and-infrastructure-SFTWR-CLD",
    # add more confirmed team slugs here
]


class AppleCareersConnector(BaseConnector):
    ats_type = "apple_careers"
    name = "Apple Careers"

    async def fetch_jobs(self) -> list[RawJob]:
        async with httpx.AsyncClient(
            timeout=20.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"},
        ) as client:
            all_summaries = []
            for team in ENGINEERING_TEAMS:
                summaries = await self._fetch_team_pages(client, team)
                all_summaries.extend(summaries)
            return await self._enrich_with_details(client, all_summaries)

    async def _fetch_team_pages(
        self, client: httpx.AsyncClient, team: str
    ) -> list[dict]:
        """
        Pagination mechanism unconfirmed — placeholder assumes a `page` query
        param; confirm and adjust during reconnaissance.
        """
        all_jobs = []
        page = 1
        while True:
            resp = await client.get(
                SEARCH_URL,
                params={
                    "location": "united-states-USA",
                    "team": team,
                    "page": page,
                },
            )
            resp.raise_for_status()
            jobs, has_more = self._parse_list_page(resp.text)
            all_jobs.extend(jobs)
            if not has_more or not jobs:
                break
            page += 1
        return all_jobs

    def _parse_list_page(self, html: str) -> tuple[list[dict], bool]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        # Each job result is an <li> or similar container with a "Role Number:"
        # label and a details link — confirm exact container selector against
        # live DOM; the pattern below is based on observed structure.
        for heading in soup.find_all(string=re.compile(r"Role Number:\s*")):
            container = heading.find_parent("li") or heading.find_parent("div")
            if not container:
                continue

            link = container.find("a", href=re.compile(r"/details/"))
            if not link:
                continue

            role_number_match = re.search(r"Role Number:\s*([\w-]+)", heading)
            location_el = container.find(string=re.compile(r"^Location"))

            jobs.append({
                "role_number": role_number_match.group(1) if role_number_match else None,
                "title": link.get_text(strip=True),
                "url": f"https://jobs.apple.com{link['href']}" if link["href"].startswith("/") else link["href"],
                "location_raw": location_el.find_next(string=True) if location_el else "",
            })

        # Determine if more pages exist — confirm mechanism (compare result
        # count against "N Result(s)" header, or check for a disabled "next"
        # control)
        has_more = False  # placeholder — confirm during reconnaissance
        return jobs, has_more

    async def _enrich_with_details(
        self, client: httpx.AsyncClient, summaries: list[dict]
    ) -> list[RawJob]:
        raw_jobs = []
        for summary in summaries:
            resp = await client.get(summary["url"])
            if resp.status_code != 200:
                continue
            raw_jobs.append(self._parse_detail(summary, resp.text))
        return raw_jobs

    def _parse_detail(self, summary: dict, html: str) -> RawJob:
        soup = BeautifulSoup(html, "html.parser")

        # Confirm exact container for full description, qualifications, etc.
        # against live page — placeholder selector below.
        description_el = soup.select_one("[class*='jd']") or soup.select_one("main")

        return RawJob(
            external_id=f"apple_{summary['role_number']}",
            ats_type=self.ats_type,
            title=summary["title"],
            company_name="Apple",
            job_location=summary["location_raw"],
            description_html=str(description_el) if description_el else "",
            job_url=summary["url"],
            posted_at=None,  # confirm date format from "May 07, 2026" style text on page
        )
```

**All selectors marked as placeholders must be confirmed against the live DOM** before
this connector is considered ready — the URL structure, server-rendering behavior, and
overall data shape are confirmed; exact CSS classes are not.

---

## Field Mapping

| Source | Your field |
|---|---|
| "Role Number" (e.g. `200626700-3337`) | `external_id` (prefix `apple_`) — this is a
  clean, stable, already-labeled identifier, better than having to extract one from a
  URL slug |
| job title | `title` |
| (constant) | `company_name` = "Apple" |
| Location text (e.g. "Seattle", "Cupertino") | `job_location` — appears to be simpler,
  single-city strings per posting rather than Google's multi-location-per-posting
  pattern; confirm whether any Apple postings list multiple locations before assuming
  this is always single-location |
| Posting date (e.g. "May 07, 2026") | `posted_at` — confirm exact date format and
  parse accordingly |
| Team code (`SFTWR`, `HRDWR`, etc.) | worth preserving in `raw_metadata` — useful
  secondary signal, same treatment as Tesla's team filter and Google's org label |
| "Weekly Hours" (e.g. "40 Hours") | optional — could inform a full-time vs. part-time
  signal if your schema tracks that distinctly from `employment_type` |

---

## Operational Notes

- **No bot-detection signal observed** in this research — the page fetched cleanly with
  no special headers, no impersonation, no challenge page. Start with plain `httpx` and
  only escalate if reconnaissance reveals otherwise.
- **Team-based scoping is a deliberate scope decision, same as Tesla and Amazon.**
  Apple has corporate/retail/hardware/software teams; you almost certainly only want
  the software/ML/data-relevant team codes. Confirm the full team list and make this
  choice explicit rather than crawling everything by default.
- **"As soon as they post" cadence:** given 600+ results per team and multiple relevant
  teams, total job volume is likely in the thousands. An hourly or every-few-hours
  cadence with incremental diffing by `role_number` (which appears stable and
  unique) is reasonable — don't re-fetch full detail for unchanged role numbers on
  every cycle, same incremental principle as your Ashby and Eightfold fixes.

---

## Testing Checklist

- [ ] Confirmed pagination mechanism for result sets beyond the first page
- [ ] Confirmed detail page is server-rendered (not yet directly verified — only list
      page confirmed in this pass)
- [ ] Confirmed and replaced all placeholder CSS selectors against live DOM
- [ ] Retrieved full "View all teams" list and selected the engineering-relevant subset
- [ ] Confirmed date format for `posted_at` parsing
- [ ] Confirmed whether any postings list multiple locations (unlike the single-location
      pattern observed in this pass)
- [ ] Verified crawled job count roughly matches the "N Result(s)" counter per team, as
      a completeness check

---

## Effort Estimate

1 day, possibly less. This may be the most straightforward "big tech direct" connector
in your batch — confirmed server-rendering, clean stable IDs already labeled on the
page, confirmed working filters, and no bot-detection signal. The main remaining work
is selector confirmation and pagination mechanics, both bounded tasks.
