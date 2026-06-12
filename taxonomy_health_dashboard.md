# Taxonomy Health — Admin Dashboard Spec

Add a fifth tab to the existing admin dashboard (Pipeline / Sources / Cost / Jobs / **Taxonomy**).
This tab surfaces the no-pool health signal described in Problem 4, making the 10%-per-domain
threshold easy to monitor after each ingestion batch.

---

## 1. API Endpoint

```
GET /admin/taxonomy-health
```

No query params. Returns a snapshot of the current active job corpus grouped by domain,
with no-pool counts and the top job titles accumulating in no-pool per domain.

**Response shape:**

```json
{
  "generated_at": "2026-06-12T02:00:00Z",
  "total_active_enriched": 4955,
  "global_no_pool_count": 1393,
  "global_no_pool_pct": 28.1,
  "domains": [
    {
      "domain": "Aerospace_Defense",
      "total": 675,
      "no_pool": 351,
      "no_pool_pct": 52.0,
      "flagged": true,
      "top_no_pool_titles": [
        { "title": "Systems Engineer (Mid-Level)", "count": 34 },
        { "title": "Principal Scientist, Electronic Warfare", "count": 18 },
        { "title": "Technical Program Manager", "count": 15 }
      ]
    },
    {
      "domain": "Software",
      "total": 1316,
      "no_pool": 136,
      "no_pool_pct": 10.3,
      "flagged": true,
      "top_no_pool_titles": [
        { "title": "Software Engineer, Mission Systems", "count": 41 },
        { "title": "Software Engineer", "count": 28 }
      ]
    },
    {
      "domain": "Research_Science",
      "total": 123,
      "no_pool": 98,
      "no_pool_pct": 79.7,
      "flagged": true,
      "top_no_pool_titles": [
        { "title": "Research Scientist", "count": 22 },
        { "title": "Principal Scientist, Biosciences", "count": 14 }
      ]
    }
  ]
}
```

**`flagged: true`** when `no_pool_pct >= 10.0`.

---

## 2. Backend Implementation

### 2.1 SQLAlchemy query

```python
# app/api/admin.py — new endpoint

from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.database import get_db
from app.models.normalized_job import NormalizedJob
from datetime import datetime, timezone

router = APIRouter(prefix="/admin", tags=["admin"])

NO_POOL_THRESHOLD_PCT = 10.0
TOP_TITLES_LIMIT = 10


@router.get("/taxonomy-health")
async def get_taxonomy_health(db: AsyncSession = Depends(get_db)):
    # Per-domain no-pool counts
    domain_rows = await db.execute(text("""
        SELECT
            COALESCE(job_domain, '(none)') AS domain,
            COUNT(*)                        AS total,
            COUNT(*) FILTER (
                WHERE retrieval_pools IS NULL
                   OR retrieval_pools = '{}'
            )                               AS no_pool
        FROM normalized_jobs
        WHERE is_active = TRUE
          AND processing_state IN ('success', 'partial_success')
        GROUP BY job_domain
        ORDER BY no_pool DESC
    """))
    domain_stats = domain_rows.fetchall()

    total_enriched = sum(r.total for r in domain_stats)
    total_no_pool = sum(r.no_pool for r in domain_stats)

    # Top no-pool titles per domain
    titles_rows = await db.execute(text("""
        SELECT
            COALESCE(job_domain, '(none)') AS domain,
            title,
            COUNT(*)                        AS cnt
        FROM normalized_jobs
        WHERE is_active = TRUE
          AND processing_state IN ('success', 'partial_success')
          AND (retrieval_pools IS NULL OR retrieval_pools = '{}')
          AND title IS NOT NULL
        GROUP BY job_domain, title
        ORDER BY job_domain, cnt DESC
    """))
    all_titles = titles_rows.fetchall()

    # Group titles by domain
    titles_by_domain: dict[str, list] = {}
    for row in all_titles:
        titles_by_domain.setdefault(row.domain, []).append(
            {"title": row.title, "count": row.cnt}
        )

    domains = []
    for row in domain_stats:
        no_pool_pct = round(100.0 * row.no_pool / row.total, 1) if row.total else 0.0
        domains.append({
            "domain": row.domain,
            "total": row.total,
            "no_pool": row.no_pool,
            "no_pool_pct": no_pool_pct,
            "flagged": no_pool_pct >= NO_POOL_THRESHOLD_PCT,
            "top_no_pool_titles": titles_by_domain.get(row.domain, [])[:TOP_TITLES_LIMIT],
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_active_enriched": total_enriched,
        "global_no_pool_count": total_no_pool,
        "global_no_pool_pct": round(100.0 * total_no_pool / total_enriched, 1) if total_enriched else 0.0,
        "domains": domains,
    }
```

---

## 3. React Component (new Taxonomy tab)

Add `"Taxonomy"` to the tab list alongside Pipeline / Sources / Cost / Jobs. The tab renders
a `TaxonomyHealthPanel` component.

```jsx
// components/TaxonomyHealthPanel.jsx

import { useEffect, useState } from "react";

const FLAG_COLOR   = "#dc2626";   // red-600
const OK_COLOR     = "#16a34a";   // green-600
const WARN_COLOR   = "#d97706";   // amber-600
const THRESHOLD    = 10.0;

function PctBadge({ pct, flagged }) {
  const color = flagged
    ? pct >= 50 ? FLAG_COLOR : WARN_COLOR
    : OK_COLOR;
  return (
    <span style={{ color, fontWeight: 600 }}>
      {pct.toFixed(1)}%
    </span>
  );
}

export default function TaxonomyHealthPanel() {
  const [data, setData] = useState(null);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    fetch("/admin/taxonomy-health")
      .then(r => r.json())
      .then(setData);
  }, []);

  if (!data) return <p>Loading taxonomy health…</p>;

  const flaggedCount = data.domains.filter(d => d.flagged).length;

  return (
    <div style={{ padding: "1.5rem" }}>
      {/* Header summary */}
      <div style={{ display: "flex", gap: "2rem", marginBottom: "1.5rem" }}>
        <Stat label="Active enriched jobs" value={data.total_active_enriched.toLocaleString()} />
        <Stat label="No-pool jobs (global)" value={data.global_no_pool_count.toLocaleString()} />
        <Stat label="Global no-pool %" value={`${data.global_no_pool_pct}%`} />
        <Stat
          label="Domains flagged (≥10%)"
          value={flaggedCount}
          highlight={flaggedCount > 0}
        />
      </div>

      {/* Per-domain table */}
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.875rem" }}>
        <thead>
          <tr style={{ background: "#f3f4f6", textAlign: "left" }}>
            <Th>Domain</Th>
            <Th>Total</Th>
            <Th>No-pool</Th>
            <Th>No-pool %</Th>
            <Th>Status</Th>
            <Th></Th>
          </tr>
        </thead>
        <tbody>
          {data.domains.map(domain => (
            <>
              <tr
                key={domain.domain}
                style={{
                  borderBottom: "1px solid #e5e7eb",
                  background: domain.flagged ? "#fef2f2" : "white",
                }}
              >
                <Td><code>{domain.domain}</code></Td>
                <Td>{domain.total.toLocaleString()}</Td>
                <Td>{domain.no_pool.toLocaleString()}</Td>
                <Td><PctBadge pct={domain.no_pool_pct} flagged={domain.flagged} /></Td>
                <Td>
                  {domain.flagged
                    ? <span style={{ color: WARN_COLOR }}>⚠ Review taxonomy</span>
                    : <span style={{ color: OK_COLOR }}>✓ OK</span>
                  }
                </Td>
                <Td>
                  {domain.top_no_pool_titles.length > 0 && (
                    <button
                      onClick={() => setExpanded(
                        expanded === domain.domain ? null : domain.domain
                      )}
                      style={{ fontSize: "0.75rem", cursor: "pointer" }}
                    >
                      {expanded === domain.domain ? "Hide titles ▲" : "Top titles ▼"}
                    </button>
                  )}
                </Td>
              </tr>

              {/* Expanded titles row */}
              {expanded === domain.domain && (
                <tr key={`${domain.domain}-titles`}>
                  <td colSpan={6} style={{ padding: "0.5rem 1rem", background: "#fafafa" }}>
                    <p style={{ fontSize: "0.75rem", color: "#6b7280", marginBottom: "0.5rem" }}>
                      Top no-pool job titles in <strong>{domain.domain}</strong>
                      {domain.flagged && " — consider adding a new pool/taxonomy entry"}
                    </p>
                    <table style={{ fontSize: "0.75rem" }}>
                      <tbody>
                        {domain.top_no_pool_titles.map(t => (
                          <tr key={t.title}>
                            <td style={{ paddingRight: "2rem" }}>{t.title}</td>
                            <td style={{ color: "#6b7280" }}>{t.count} jobs</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>

      <p style={{ fontSize: "0.75rem", color: "#9ca3af", marginTop: "1rem" }}>
        Generated {new Date(data.generated_at).toLocaleString()}.
        Threshold: flag domains with no-pool ≥ {THRESHOLD}%.
        To fix: expand pool taxonomy, update LLM prompt, re-enrich flagged domain jobs.
      </p>
    </div>
  );
}

// Helper components
function Stat({ label, value, highlight }) {
  return (
    <div style={{ minWidth: 160 }}>
      <div style={{ fontSize: "0.75rem", color: "#6b7280" }}>{label}</div>
      <div style={{
        fontSize: "1.5rem", fontWeight: 700,
        color: highlight ? FLAG_COLOR : "#111827"
      }}>
        {value}
      </div>
    </div>
  );
}
function Th({ children }) {
  return <th style={{ padding: "0.5rem 0.75rem", fontWeight: 600 }}>{children}</th>;
}
function Td({ children }) {
  return <td style={{ padding: "0.5rem 0.75rem" }}>{children}</td>;
}
```

---

## 4. Taxonomy Expansion Workflow (visible in the dashboard)

When a domain is flagged, the operator's workflow is:

1. Click "Top titles ▼" for the flagged domain
2. Check whether the titles cluster around a coherent role category
3. If yes (e.g., 22 "Research Scientist" + 14 "Principal Scientist" → `RESEARCH_SCIENTIST_FULLTIME`):
   - Add pool to `POOL_DOMAIN_MAP` in `taxonomy.py`
   - Add pool to LLM enrichment prompt vocabulary
   - Trigger targeted re-enrichment: active jobs in that domain with empty `retrieval_pools`
4. If no clear cluster (titles are disparate): leave as-is, no new pool needed

The dashboard threshold is 10% per domain. Check after any major company batch ingestion.
