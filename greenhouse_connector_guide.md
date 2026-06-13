# Greenhouse Connector — Implementation Guide

This document covers the Greenhouse connector for the job ingestion pipeline, including the **branded careers supplement** for jobs that apply via Greenhouse but are hosted on a company careers site rather than `boards.greenhouse.io`.

For the shared pipeline contract, see [`job_ingestion/CONNECTOR_GUIDE.md`](job_ingestion/CONNECTOR_GUIDE.md).  
Official API reference: [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html).

---

## 1. Two Greenhouse Surfaces

| Surface | Where jobs appear | How we fetch |
|---|---|---|
| **Public job board** | `boards.greenhouse.io/{token}` or `job-boards.greenhouse.io/{token}` | List API (single call) |
| **Branded careers embed** | Company domain (`careers.example.com`, `jobs.example.com`) with `?gh_jid={id}` | Careers page scrape → per-job API |

Both surfaces use the **same Job Board API** and return the **same native JSON shape**. The deterministic extractor (`_extract_greenhouse`) handles both without changes.

```
Company (platform=greenhouse, board_token, optional platform_config.careers_url)
        │
        ├─► GET /v1/boards/{token}/jobs?content=true     (list — always)
        │
        └─► Scrape careers_url for gh_jid / GH job links   (optional supplement)
                │
                └─► GET /v1/boards/{token}/jobs/{id}?content=true  (per discovered ID)
                        │
                        └─► Merge + dedupe by job id (list wins on conflict)
```

---

## 2. Public Board API (Default)

| | |
|---|---|
| **Auth** | None |
| **List endpoint** | `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true` |
| **Detail endpoint** | `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs/{id}?content=true` |
| **`board_token`** | Greenhouse board slug (e.g. `stripe`, `figma`, `anthropic`) |
| **Implementation** | `job_ingestion/app/ingestion/connectors/greenhouse.py` |

The list endpoint returns full job descriptions in one call. This remains the primary source for all Greenhouse companies.

---

## 3. Branded Careers Supplement

### 3.1 When to enable

Set `platform_config.careers_url` when a company:

- Embeds Greenhouse on their own careers site (iframe or API-driven frontend)
- Links to jobs with `?gh_jid={id}` on a non-`greenhouse.io` domain
- May have postings discoverable on the careers site that are **not** returned by the list API

When `careers_url` is **not** set, behavior is unchanged: list API only.

### 3.2 Company configuration

```json
{
  "company": "Example Corp",
  "platform": "greenhouse",
  "board_token": "examplecorp",
  "platform_config": {
    "careers_url": "https://careers.example.com/jobs",
    "careers_urls": [
      "https://careers.example.com/jobs/engineering"
    ],
    "board_token_override": "examplecorp",
    "validate_absolute_url_domain": true
  },
  "is_active": true
}
```

| Field | Required | Description |
|---|---|---|
| `careers_url` | For supplement | Primary careers listing page to scrape |
| `careers_urls` | Optional | Additional pages (departments, search results) |
| `board_token_override` | Optional | API slug when it differs from hostname (e.g. C3.ai → `c3iot`, Arize → `arizeai`) |
| `validate_absolute_url_domain` | Optional | Default `true` when supplement is enabled. Rejects per-job API responses whose `absolute_url` root domain does not match the careers page (mitigates `gh_jid` collisions across boards). Always allows `greenhouse.io`. |

### 3.3 Careers page discovery

The connector fetches each configured careers URL (via `curl_cffi` browser impersonation, with `httpx` fallback) and scans HTML for job IDs:

| Pattern | Example |
|---|---|
| `gh_jid={id}` | `https://careers.example.com/openings?gh_jid=5551532004` |
| Greenhouse board links | `https://job-boards.greenhouse.io/examplecorp/jobs/4684499006` |
| `/jobs/{id}` on page | Only when page contains Greenhouse signals (`gh_jid`, `greenhouse`, `boards-api.greenhouse.io`, `?for=`) |

Discovered IDs **not already in the list response** are hydrated via the per-job detail API.

### 3.4 Per-job hydration

```
GET https://boards-api.greenhouse.io/v1/boards/{token}/jobs/{id}?content=true
```

- Uses `board_token_override` when set, else `company.board_token`
- Skips 404s and malformed responses (logs warning, continues)
- Requires `id`, `title`, and `content` in the response
- Concurrency: 4 parallel requests, 0.2s delay between completions

### 3.5 Merge rules

- Build `dict[job_id → job]` from list API results first
- Add careers-only jobs that pass validation
- **On ID conflict, list API payload wins** (careers scrape does not overwrite)

---

## 4. Finding the Board Token

1. Open the company's careers page and inspect job links for `boards.greenhouse.io/{token}` or `job-boards.greenhouse.io/{token}`
2. View embed code in Greenhouse Dev Center — look for `?for={token}` in iframe URLs
3. Check network tab for calls to `boards-api.greenhouse.io/v1/boards/{token}/...`
4. If hostname ≠ token (common for rebranded domains), set `board_token_override`

---

## 5. Native Job Dict Shape

Both list and detail endpoints must return dicts compatible with `_extract_greenhouse`:

```json
{
  "id": 5551532004,
  "title": "Software Engineer",
  "location": { "name": "San Francisco, CA" },
  "departments": [{ "name": "Engineering" }],
  "absolute_url": "https://careers.example.com/jobs?gh_jid=5551532004",
  "updated_at": "2026-05-20T10:00:00Z",
  "content": "<p>Job description HTML...</p>",
  "metadata": [{ "name": "Employment Type", "value": "Full-time" }]
}
```

| Field | Used for |
|---|---|
| `id` | External job ID, change detection |
| `title` | Job title |
| `location.name` | Location |
| `departments[0].name` | Department |
| `absolute_url` | Posting URL (often branded domain for supplement jobs) |
| `updated_at` | Posted/updated timestamp |
| `content` | HTML description → `raw_html` |
| `metadata[]` | Employment type |

---

## 6. Slug Mismatch Examples

| Company site | Hostname hint | Greenhouse `board_token` |
|---|---|---|
| c3.ai/careers | `c3.ai` | `c3iot` |
| arize.com/careers | `arize.com` | `arizeai` |
| careers.nebius.com | `nebius.com` | `nebius` |

Use `board_token_override` when the API slug does not match the careers domain.

---

## 7. Out of Scope

| Item | Reason |
|---|---|
| **Harvest API** | Requires authenticated API key; exposes internal/unpublished jobs — different product surface |
| **Internal boards** (`board_token: "internal"`) | Separate board type; not mixed with public careers supplement |
| **Full site crawl / JS rendering** | v1 is static HTML scrape of configured URLs only |
| **`grnh.se` short links** | Phase 2 — requires redirect following |
| **Non-Greenhouse career pages** | Use iCIMS, Workday, or Oracle HCM connectors instead |

---

## 8. Error Handling

| Failure | Behavior |
|---|---|
| List API HTTP/parse error | Raises `ConnectorFetchError` / `ParseError` — entire fetch fails |
| Careers page fetch error | Logs warning, returns list-only results |
| Per-job detail 404/invalid | Logs warning, skips that ID |
| Domain validation failure | Logs warning, skips that ID |

---

## 9. Tests

See `job_ingestion/tests/test_greenhouse_connector.py`:

- List-only backward compatibility
- Supplement merge (list + careers-only job)
- Dedup (list wins on conflict)
- Board token override in detail URL
- Domain mismatch rejection
- 404 detail skip
- HTML ID extraction helpers

Run:

```bash
cd job_ingestion
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db pytest tests/test_greenhouse_connector.py -v
```

---

## 10. File Reference

| File | Purpose |
|---|---|
| `job_ingestion/app/ingestion/connectors/greenhouse.py` | Connector implementation |
| `job_ingestion/app/ingestion/extractor/deterministic.py` | `_extract_greenhouse` field mapping |
| `job_ingestion/app/ingestion/fetcher.py` | Connector registry |
| `job_ingestion/data/companies.json` | Seed data with optional `platform_config` |
| `job_ingestion/tests/test_greenhouse_connector.py` | Unit tests |
