# Microsoft Careers Connector — Integration Guide

## Overview

Confirmed directly, and this is a significant finding: **Microsoft does not run a
custom career site either — they run on Eightfold AI, the same platform as Netflix.**
Fetching `apply.careers.microsoft.com/careers?...` returned embedded config identical in
shape to Netflix's confirmed Eightfold instance (`"product": "PCS"`, matching
`varTheme`/`pcsx-*` config keys).

**This means the connector you build for Netflix should directly cover Microsoft too —
same `EightfoldConnector` class, different `board_token`/`platform_config`.** This is
not a new connector; it's a new tenant configuration row.

**Difficulty: Low**, identical to Netflix, assuming the same `EightfoldConnector` is
reused.

---

## Confirmed Facts (From Direct Inspection)

- **URL:** `https://apply.careers.microsoft.com/careers?start=0&sort_by=solr&filter_profession=software+engineering`
  — confirmed Eightfold-hosted via embedded config (`"domain": "microsoft.com"`,
  `"product": "PCS"`, identical `pcsx-*` theme variable structure to Netflix).
- **Significant additional finding: Microsoft's Eightfold instance sits in front of
  their actual underlying ATS, which is SuccessFactors.** The embedded page config
  contains this exact string:
  ```
  "basePositionFq": "((position.type:ATS AND is_externally_posted:1) AND
  (position.system_id:successfactors) AND (position.ats_data.status:(Open)))"
  ```
  This confirms Microsoft's real system of record is SuccessFactors, and Eightfold is
  layered on top as a unified search/discovery experience. **This is good news for
  you** — it means you don't need your SuccessFactors connector framework (with its
  per-tenant reconnaissance burden, as documented in `connector_successfactors.md`) to
  reach Microsoft's jobs at all. The Eightfold layer normalizes SuccessFactors's
  notoriously inconsistent per-tenant API shape into Eightfold's clean, already-solved
  public API. **Use the Eightfold connector for Microsoft, not the SuccessFactors one.**
- **Query parameters confirmed working:** `start` (pagination offset), `sort_by=solr`,
  `filter_profession=software+engineering` (profession-based filtering — directly
  useful for scoping to engineering roles).
- **`filter_profession` values observed in Microsoft's own site copy:** `software
  engineering`, `supply chain`, `technical support`, `quantum computing`, `real estate,
  facilities, & construction`, `governance, risk, & compliance`, `hardware engineering`,
  `human resources` — confirmed via Microsoft's own "Professions" page listing these as
  real filter values with working URLs.
- **Rich server-rendered HTML confirmed on at least one listing page** —
  `careers.microsoft.com/v2/global/en/locations/seattle-area.html` returned full HTML
  job descriptions with proper `<ul><li>` qualification lists, suggesting Microsoft
  also maintains SEO-friendly server-rendered listing pages as an alternative or
  supplementary path to the Eightfold API. Worth checking whether this `v2/global`
  path is a legacy system still serving some traffic, or fully superseded by the
  Eightfold-hosted `apply.careers.microsoft.com` experience — confirm which is
  authoritative/complete before relying on one over the other.

---

## Recommended Approach: Reuse the Eightfold Connector

Do not build Microsoft-specific connector code. Instead, add a second tenant entry using
the exact same `EightfoldConnector` class built for Netflix (see
`connector_netflix_eightfold.md`):

```json
{
  "company": "Microsoft",
  "platform": "eightfold",
  "board_token": "microsoft",
  "fetch_tier": 2,
  "is_active": true,
  "platform_config": {
    "api_host": "apply.careers.microsoft.com",
    "domain": "microsoft.com",
    "extra_params": {
      "filter_profession": "software engineering"
    }
  }
}
```

The `extra_params` field is new relative to the Netflix config — Microsoft's confirmed
`filter_profession` parameter is a clean, working way to scope the crawl to engineering
roles at the source, rather than pulling all professions and filtering downstream. If
you want broader coverage (e.g. also `data engineering`, `applied sciences` per the
Microsoft AI careers page's discipline filter list), pass multiple profession values or
run the connector once per profession of interest.

### Connector class change needed

Your `EightfoldConnector.__init__` and `_fetch_all_pages` (from the Netflix guide) need
a small generalization to support `extra_params`:

```python
def __init__(self, board_token: str, platform_config: dict):
    self.board_token = board_token
    self.api_host = platform_config["api_host"]
    self.domain = platform_config["domain"]
    self.extra_params = platform_config.get("extra_params", {})

async def _fetch_all_pages(self, client: httpx.AsyncClient) -> list[dict]:
    all_jobs = []
    start = 0
    while True:
        params = {"domain": self.domain, "hl": "en", "start": start}
        params.update(self.extra_params)
        resp = await client.get(
            f"https://{self.api_host}/api/apply/v2/jobs", params=params
        )
        # ... rest identical to Netflix implementation
```

This is the only code change needed — everything else (pagination loop, detail fetch,
retry logic, host bucket if you choose to share one across Eightfold tenants) is
identical to Netflix.

---

## Reconnaissance Still Needed

1. **Confirm SmartApply vs PCSX pattern for Microsoft specifically** — don't assume it
   matches Netflix's pattern just because both are Eightfold; verify independently,
   same discipline as the Netflix guide.
2. **Confirm `host` resolution** — test whether `apply.careers.microsoft.com` itself
   serves the API directly (since, unlike Netflix's `explore.jobs.netflix.net`, this
   URL already contains "careers" and "apply" in a way that suggests it might be the
   direct API host, not just a frontend proxy).
3. **Resolve the `v2/global` legacy page question** — confirm whether
   `careers.microsoft.com/v2/global/en/...` is fully redundant with the Eightfold-hosted
   experience or contains any postings not reachable through it. If fully redundant,
   ignore it and use only the Eightfold path for simplicity.
4. **Get the complete profession-filter list relevant to your product** — beyond
   "software engineering," check whether Microsoft's site exposes "data science," "data
   engineering," "applied sciences," or similar values that map to your other pools
   (`ML_ENGINEER_FULLTIME`, `DATA_ENGINEER_FULLTIME`, etc.).

---

## Field Mapping

Identical to Netflix's Eightfold mapping (see `connector_netflix_eightfold.md`) — same
platform, same response shape expected. The one Microsoft-specific addition is
preserving `filter_profession` (or whichever profession value was used for that crawl)
in `raw_metadata`, useful for debugging coverage and cross-checking against your domain
taxonomy.

---

## Testing Checklist

- [ ] Confirmed Microsoft's instance uses the same SmartApply/PCSX pattern as Netflix —
      verified independently, not assumed
- [ ] Confirmed `extra_params` (specifically `filter_profession`) correctly scopes
      results when passed to the API directly (not just the browser-facing URL)
- [ ] Resolved whether `careers.microsoft.com/v2/global` is legacy/redundant or an
      additional needed source
- [ ] Identified full set of profession filter values relevant to your pool taxonomy
- [ ] Confirmed `EightfoldConnector` generalization (the `extra_params` addition) doesn't
      break the existing Netflix configuration — run both tenants through tests

---

## Effort Estimate

Half a day or less, assuming the Eightfold connector for Netflix ships first. This is
almost entirely a configuration and small-generalization task, not new connector
development — the highest-leverage outcome of this research is confirming that your
Eightfold investment pays off across at least two major companies (Netflix, Microsoft)
immediately, with more likely in your existing or future catalog.
