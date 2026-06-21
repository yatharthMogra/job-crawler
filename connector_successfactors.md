# Amazon Careers Connector — Integration Guide

## Overview

Amazon's career site (`amazon.jobs`) is its own dedicated domain rather than a path under
`amazon.com`, which is itself a signal worth noting — it suggests a more purpose-built
job-search application than Uber's careers section bolted onto the main consumer site.
This connector has not yet been directly inspected in this research pass (unlike Google
and Uber, which were checked live) — **treat everything below as a reconnaissance plan,
not confirmed findings**, and run the same live-inspection process used for Google and
Uber before writing any code.

**Difficulty: Unknown until reconnaissance — plan for Medium-high.** Amazon is large
enough and security-conscious enough that I'd default to expecting an API-backed SPA
(Uber-shape) rather than server-rendered HTML (Google-shape), but this must be confirmed
rather than assumed, since guessing wrong wastes a full implementation pass.

---

## Reconnaissance Step (Do This First — Same Discipline as Google and Uber)

1. Fetch `https://www.amazon.jobs/en/search` (or the equivalent search/listing URL —
   confirm exact path by visiting the site) with a plain unauthenticated GET request,
   no browser. If the response HTML contains actual job titles and listings, you're in
   the Google shape — server-rendered, no API needed.
2. If the plain GET returns only a shell/skeleton (Uber shape), open DevTools, Network
   tab, filter to Fetch/XHR, and identify the request that populates the job list.
   Amazon has historically run a dedicated jobs search API at a path like
   `amazon.jobs/en/search.json` for at least some periods of their site's history — check
   whether a `.json` variant of the search URL returns structured data directly. This is
   a hypothesis to test, not a confirmed fact for the current version of the site.
3. Click into a single job listing and confirm the detail page URL pattern and whether
   it's server-rendered or also API-backed.
4. Check for pagination parameters and any team/location filter parameters by applying
   filters manually and observing the resulting URL or request payload changes.
5. Check for rate-limiting signals and any bot-protection challenge pages.

---

## Two Possible Shapes — Plan for Both, Confirm Before Building

### If Server-Rendered (Google-shape)

Reuse the Google Careers connector architecture directly:

```python
# job_ingestion/app/ingestion/connectors/amazon_jobs.py

import httpx
from bs4 import BeautifulSoup
from ..base import BaseConnector
from ..models import RawJob

SEARCH_URL = "https://www.amazon.jobs/en/search"  # confirm exact path


class AmazonJobsConnector(BaseConnector):
    ats_type = "amazon_jobs"
    name = "Amazon Jobs"

    async def fetch_jobs(self) -> list[RawJob]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            summaries = await self._fetch_all_pages(client)
            return await self._enrich_with_details(client, summaries)

    # Implementation mirrors GoogleCareersConnector if this shape is confirmed —
    # see connector_google_careers.md for the full pattern to adapt.
```

### If API-Backed SPA (Uber-shape)

Reuse the Uber Careers connector architecture directly — list endpoint, optional detail
endpoint, confirmed empirically before any code is written. See
`connector_uber_careers.md` for the pattern to adapt.

**Do not build a third, novel architecture speculatively.** Whichever shape Amazon turns
out to be, you already have a working template from this round of connectors. The
engineering work here is reconnaissance + adaptation, not invention.

---

## Things Specific to Amazon Worth Checking During Reconnaissance

- **Amazon job postings often include a `job_id` visible directly in the URL** (Amazon
  has historically used numeric job IDs in their job posting URLs) — confirm this remains
  true and use it as `external_id`.
- **Amazon's job descriptions are typically long and highly structured** (Basic
  Qualifications, Preferred Qualifications, About the team, etc. as separate labeled
  sections) — similar to how SmartRecruiters splits sections. If the API/HTML separates
  these into distinct fields rather than one blob, preserve that structure in
  `raw_html` with clear section breaks rather than flattening, since your enrichment LLM
  prompt may benefit from cleanly labeled sections.
- **Amazon hires at enormous global scale** — expect international locations at a scale
  comparable to or exceeding Uber. Same caution applies to country/location resolution
  testing as flagged in the Uber doc.
- **Amazon subsidiaries** (AWS is the main one relevant to your engineering-focused
  pools, also Whole Foods, Twitch, Ring, Zoox, etc.) may either share the same
  `amazon.jobs` search and be filterable by business unit, or have entirely separate
  career sites. Confirm during reconnaissance whether AWS-specific roles are reachable
  through the same `amazon.jobs` search or need their own discovery pass — given your
  user base's interest in software/ML/data roles, AWS coverage matters more than Whole
  Foods coverage for your specific product.

---

## Field Mapping (Tentative — Adjust After Reconnaissance)

| Likely source field | Your field |
|---|---|
| Amazon job ID | `external_id` (prefix `amzn_`) |
| title | `title` |
| business unit / team (if exposed — e.g. "AWS", "Amazon Robotics") | consider
  preserving in `raw_metadata`, similar treatment to the Google org-label question;
  may be more useful for Amazon than for Google given how distinct AWS roles are from
  retail-side roles |
| location | `job_location` |
| Basic Qualifications / Preferred Qualifications / job description sections | fold into
  `raw_html` with clear section breaks preserved |
| posted date | `posted_at` — confirm availability |

---

## Recommended Sequencing

Given you're studying Google, Uber, and Amazon together as your first three custom
connectors, build in this order:

1. **Google first** — confirmed server-rendered, lowest implementation risk, gets you a
   working "direct career site" connector pattern in production fastest.
2. **Amazon second** — run reconnaissance immediately after Google ships. If Amazon
   turns out to be server-rendered like Google, it's a fast follow using the same
   pattern. If it's API-backed like Uber, you'll have learned the reconnaissance process
   once already on a simpler case before tackling Uber's likely-harder SPA.
3. **Uber third** — confirmed API-backed SPA, the most reconnaissance-intensive of the
   three. Doing this last means your team has already built and shipped one
   server-rendered connector (Google) and has the muscle memory for the reconnaissance
   process before tackling the harder case.

This sequencing differs from the order you listed (Google, Uber, Amazon) — I'd swap Uber
and Amazon specifically because Amazon's actual shape is still unknown and might turn out
to be the easy case, whereas Uber is now confirmed to be the hard case. Don't burn your
team's energy on the confirmed-hard one second; do the unknown one second so you find out
fast whether it's easy or hard.

---

## Testing Checklist

- [ ] Confirmed server-rendered vs. API-backed shape via direct inspection (do not
      assume based on this document — Amazon was not directly inspected in this pass)
- [ ] Confirmed job ID format and URL pattern
- [ ] Confirmed whether AWS-specific roles are reachable through the same search/API or
      need separate handling
- [ ] Confirmed section structure of job descriptions (Basic/Preferred Qualifications
      etc.) and decided how to preserve that structure into `raw_html`
- [ ] Location parsing tested against Amazon's actual global location spread
- [ ] Fixture test captures real confirmed response shape, whichever architecture
      applies

---

## Effort Estimate

Cannot be estimated precisely until reconnaissance determines the architecture shape.
Budget a half-day reconnaissance spike specifically to answer "is this Google-shape or
Uber-shape" before committing to a timeline — that answer determines whether this is a
1-day connector or a 2-3 day connector.