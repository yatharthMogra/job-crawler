# BlackRock Careers Connector — Integration Guide

## Overview

Confirmed directly: BlackRock's careers site (`careers.blackrock.com`) is built on
**TalentBrew** (a Radancy product) — identified by the `tbcdn.talentbrew.com` asset
domain serving the BlackRock logo and other site assets. The listing page returned is
**fully server-rendered**, with complete pagination ("Page 1/13"), category facets,
country/region/city filters, and clean per-job detail links — all present in plain
HTML, no JavaScript execution required.

This is a new platform for your catalog (not previously confirmed elsewhere in your
connector set), but it's a clean, simple, predictable target — closer to Apple or
Google in difficulty than to Uber or Tesla. If other companies in your catalog or
backlog also run TalentBrew, this connector covers them too, same leverage logic as
Eightfold.

**Difficulty: Low.** Confirmed server-rendered, explicit pagination, no bot-detection
signal observed, clean filter structure.

---

## Confirmed Facts (From Direct Inspection)

- **List URL pattern:** `https://careers.blackrock.com/category/{category-slug}/
  {company-id}/{sub-id}/{page}` — e.g.
  `careers.blackrock.com/category/software-engineering-jobs/45831/8771056/1`
- **`45831` is BlackRock's TalentBrew company ID** — confirmed present consistently
  across both list and detail URLs (`tbcdn.talentbrew.com/company/45831/...` and
  `careers.blackrock.com/job/paris/senior-software-engineer-full-stack/45831/91629470512`).
- **Pagination confirmed working and explicit:** "You are currently on page 1 / 13"
  with direct `Prev`/`Next` links following the predictable URL pattern (incrementing
  the final path segment). No XHR needed — just increment the page number in the URL.
- **Detail URL pattern confirmed:**
  ```
  https://careers.blackrock.com/job/{location-slug}/{title-slug}/{company-id}/{job-id}
  ```
  e.g. `careers.blackrock.com/job/bengaluru/associate-application-engineer/45831/93795941552`
  — the trailing numeric ID (`93795941552`) is your stable `external_id`.
- **Full category list confirmed** directly from the page's filter sidebar — extensive
  and useful for scoping: `Software Engineering`, `System Engineering`, `Data Analytics`,
  `Data Science`, `Data Management`, `Financial Engineering`, `Risk Analytics, Modeling,
  & Reporting`, `Technology Product`, `Technology Audit`, alongside many
  non-engineering categories (Accounting, Legal, Sales & Relationship Mgmt, etc.) — easy
  to scope your crawl to the engineering/data-relevant subset only.
- **Country/region/city facets confirmed present**: France, Hungary, India, Mexico,
  Serbia, Singapore, United Kingdom, United States — confirms BlackRock posts globally;
  apply the same location-parsing caution used for other global employers.
- **No login required, no bot-detection signal observed.**

---

## Recommended Architecture

```python
# job_ingestion/app/ingestion/connectors/talentbrew.py
#
# Generic TalentBrew connector — if other companies turn out to run TalentBrew,
# this class serves all of them via board_token + platform_config, same pattern
# as your Eightfold and Workday multi-tenant connectors.

import re
import httpx
from bs4 import BeautifulSoup
from ..base import BaseConnector
from ..models import RawJob

ENGINEERING_CATEGORIES = [
    "software-engineering-jobs",
    "data-science-jobs",          # confirm exact slug during reconnaissance
    "data-analytics-jobs",        # confirm exact slug
    "data-management-jobs",       # confirm exact slug
    "financial-engineering-jobs", # confirm exact slug
]


class TalentBrewConnector(BaseConnector):
    ats_type = "talentbrew"
    name = "TalentBrew Career Site"

    def __init__(self, board_token: str, platform_config: dict):
        """
        platform_config must contain:
          - base_url: e.g. "https://careers.blackrock.com"
          - company_id: TalentBrew's numeric company ID (e.g. "45831")
          - sub_id: the secondary numeric ID seen in list URLs (e.g. "8771056")
            — confirm whether this is stable/required or category-specific
        """
        self.board_token = board_token
        self.base_url = platform_config["base_url"]
        self.company_id = platform_config["company_id"]
        self.sub_id = platform_config["sub_id"]

    async def fetch_jobs(self) -> list[RawJob]:
        async with httpx.AsyncClient(
            timeout=20.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; CareerMatchBot/1.0)"},
        ) as client:
            all_summaries = []
            for category in ENGINEERING_CATEGORIES:
                summaries = await self._fetch_category_pages(client, category)
                all_summaries.extend(summaries)
            return await self._enrich_with_details(client, all_summaries)

    async def _fetch_category_pages(
        self, client: httpx.AsyncClient, category: str
    ) -> list[dict]:
        all_jobs = []
        page = 1
        total_pages = None

        while True:
            url = f"{self.base_url}/category/{category}/{self.company_id}/{self.sub_id}/{page}"
            resp = await client.get(url)
            if resp.status_code == 404:
                break  # category slug invalid for this tenant, or no jobs in it
            resp.raise_for_status()

            jobs, total_pages = self._parse_list_page(resp.text)
            all_jobs.extend(jobs)

            if total_pages is None or page >= total_pages:
                break
            page += 1

        return all_jobs

    def _parse_list_page(self, html: str) -> tuple[list[dict], int | None]:
        soup = BeautifulSoup(html, "html.parser")
        jobs = []

        for link in soup.select("a[href*='/job/']"):
            href = link["href"]
            id_match = re.search(r"/job/[^/]+/[^/]+/\d+/(\d+)", href)
            if not id_match:
                continue
            title_el = link.find("h2") or link.find("h3")
            jobs.append({
                "id": id_match.group(1),
                "title": title_el.get_text(strip=True) if title_el else link.get_text(strip=True),
                "url": href if href.startswith("http") else f"{self.base_url}{href}",
            })

        # "Page 1 / 13" style text — confirm exact selector against live DOM
        total_pages = None
        page_indicator = soup.find(string=re.compile(r"page\s+\d+\s*/\s*\d+", re.I))
        if page_indicator:
            match = re.search(r"/\s*(\d+)", page_indicator)
            if match:
                total_pages = int(match.group(1))

        return jobs, total_pages

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
        # Confirm container selector against live detail page.
        description_el = soup.select_one("[class*='job-description']") or soup.select_one("main")
        location_el = soup.find(string=re.compile(r"^Location:"))

        return RawJob(
            external_id=f"talentbrew_{self.board_token}_{summary['id']}",
            ats_type=self.ats_type,
            title=summary["title"],
            company_name=self.board_token,
            job_location=location_el.find_next(string=True) if location_el else "",
            description_html=str(description_el) if description_el else "",
            job_url=summary["url"],
            posted_at=None,  # confirm availability and format on detail page
        )
```

---

## companies.json Entry

```json
{
  "company": "BlackRock",
  "platform": "talentbrew",
  "board_token": "blackrock",
  "fetch_tier": 2,
  "is_active": true,
  "platform_config": {
    "base_url": "https://careers.blackrock.com",
    "company_id": "45831",
    "sub_id": "8771056"
  }
}
```

**Confirm whether `sub_id` (`8771056`) is stable across all categories** or whether it
changes per category — only one category (`software-engineering-jobs`) was directly
observed in this research. If it varies, you'll need to discover the correct sub_id
per category during reconnaissance rather than assuming one value works for all.

---

## Reconnaissance Still Needed

1. **Confirm exact category slugs** for Data Science, Data Analytics, Data Management,
   Financial Engineering, etc. — only "software-engineering-jobs" was directly
   confirmed; the others are inferred from the displayed category names and need
   slug verification.
2. **Confirm whether `sub_id` is category-specific or constant** across all categories
   for this tenant.
3. **Confirm detail page structure** — only list pages were directly fetched in this
   pass; verify the description container selector against a live detail page fetch.
4. **Confirm `posted_at` availability and format** on detail pages.

---

## Testing Checklist

- [ ] Confirmed full set of engineering/data-relevant category slugs
- [ ] Confirmed `sub_id` behavior (constant vs. per-category)
- [ ] Confirmed detail page selectors against live DOM
- [ ] Confirmed `posted_at` field availability
- [ ] Verified pagination correctly terminates at the actual last page (test against
      the "Page N / 13" indicator logic)
- [ ] Checked whether any other companies in your catalog/backlog also use TalentBrew
      (same `tbcdn.talentbrew.com` asset pattern) — if so, this connector covers them
      with just a new tenant config

---

## Effort Estimate

1 day. Clean server-rendered structure with explicit pagination significantly reduces
risk relative to API-reverse-engineering connectors — main remaining work is selector
confirmation and category-slug discovery, both bounded tasks.
