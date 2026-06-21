# Tesla Careers — Akamai Troubleshooting Log

This document records why automated Tesla ingestion failed and why we moved to a manual browser bridge.

**Operational guide:** see [`connector_tesla_careers.md`](connector_tesla_careers.md) and [`scripts/tesla_careers_bridge.user.js`](scripts/tesla_careers_bridge.user.js).

---

## Problem

Tesla careers APIs sit behind Akamai Bot Manager. Automated fetch (curl, curl_cffi, Playwright headed/headless) consistently returned 403/429. A real human browser session passes without special effort.

**Company ID:** `e686e4bd-4bd4-44c3-80ec-c196fffd9b49`

---

## What Worked vs What Didn't

| Context | Result |
|---|---|
| Real browser / Cursor IDE browser | Works — state + detail APIs return 200 |
| curl / httpx / curl_cffi | 403 / 429 |
| Playwright headless or headed Chrome | Stuck on "Access Denied" |
| Cookie export → HTTP | Partial; details hit 429 at scale |

---

## Resolution

**Manual browser-bridge (push-only):** Tampermonkey userscript on `tesla.com/careers/search/*` fetches state + new details using the page session, pushes to `/ingest/tesla/*`. Server reuses existing normalize + pipeline logic.

Tesla is excluded from `fetch-tick` via `platform_config.ingestion_mode: "manual_push"`.

---

## Attempts Tried (Automated — All Failed)

1. curl_cffi HTTP + search-page warmup → 403
2. Playwright headless → Access Denied
3. Playwright headed Chrome + anti-detection flags → Access Denied (~90s)
4. Cookie export to curl_cffi → partial state, detail 429
5. Full in-browser Playwright crawl → never passed bootstrap
6. CDP sidecar approach → deferred in favor of explicit human-in-the-loop design

---

## Key API Discovery (Still Valid)

- `GET /cua-api/apps/careers/state` — global catalog, no pagination
- Site filter client-side via `geo` location IDs (~4,387 US jobs)
- `GET /cua-api/careers/job/{id}` — per-job detail (descriptions required)

Fixtures: `job_ingestion/tests/fixtures/tesla_careers/`
