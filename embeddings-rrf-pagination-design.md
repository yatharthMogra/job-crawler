# Embeddings, RRF Placement, and Recommendation Pagination — Design Doc

**Status:** Draft for review
**Scope:** Extends the existing `recommendation_service` pipeline (see current-state spec) with an
embedding-based semantic signal, RRF-based retrieval fusion, and a cache-backed pagination model.
**Non-goals:** This doc does not change `personal_score`'s formula or its UI meaning (match tiers,
`isPremiumRole`, `coreSkillsMatchPercent` stay as-is per prior agreement) — it changes what gets
*into* the batch that `score_job()` runs on, and how results are paginated back to the client.

---

## 1. Embedding Computation — Jobs

| | |
|---|---|
| **Stage** | Job ingestion / enrichment (same stage that computes `opportunity_score`) |
| **Trigger** | New job ingested; re-triggered if `description_text` is edited post-ingestion |
| **Input** | Job title + description text (the same text used for the BM25/skills pipeline) |
| **Output** | One 384-dim float vector per job |
| **Storage** | New column on the job record, e.g. `embedding vector(384)` (pgvector) or a serialized float array. Indexed if you later need approximate nearest-neighbor lookups; not required for the RRF use case below since we compare against a bounded per-request candidate set, not the whole table. |
| **Side effect** | Feed the job's tokenized terms into the nightly corpus-IDF job (from the Point 1 doc) at the same time — no separate pass needed. |

**Recompute policy:** if a job's `description_text` changes after ingestion, re-embed. If only
`salary`, `is_active`, or other structured fields change, no re-embed needed.

---

## 2. Embedding Computation — Candidates / Resumes

| | |
|---|---|
| **Stage** | Resume save/update (not per job-view, not per recommendation request) |
| **Trigger** | Candidate uploads or edits any of their up to 5 saved resumes |
| **Input** | Resume text |
| **Output** | One 384-dim vector per resume (up to 5 per candidate) |
| **Storage** | Alongside each resume record, same as the BM25 term-frequency profile from Point 1 |

**Consistency decision (needs your sign-off, flagging explicitly):** the ATS per-job score already
uses "best of 5 resumes" (max similarity across the candidate's saved resumes) per the original
design. For the recommendation feed's embedding-similarity signal, I'd keep this identical — take
the **max cosine similarity across all 5 resume vectors** for each job, rather than picking one
"primary" resume. It's the same handful of extra dot products (5x instead of 1x, still trivial),
and it keeps the semantic signal consistent between the two features rather than having "recommend"
and "how do I score against this job" quietly disagree with each other about which resume is the
candidate's best foot forward.

---

## 3. Where RRF Fits — Before Hard Constraints

Per your preference, RRF fusion runs **before** the profile-specific hard constraint filters
(clearance, sponsorship, salary floor, seniority, domain, role intent, experience tier ceiling —
Section 3.3 of the current spec). It runs **after** the one filter that has to come first no matter
what: pool membership (`retrieval_pools(job) ∩ active_subscribed_pools(candidate)`), since that's
what bounds the candidate set to something rankable at all — without it you'd be ranking against
the entire platform's job corpus, which isn't meaningful and isn't cheap.

### 3.1 Why this ordering, concretely

Hard constraints are excludes, not down-ranks — a job either can be shown to this candidate or it
can't (sponsorship, clearance, salary floor are hard requirements, not preferences). Running RRF
before them doesn't change *which* jobs a candidate is ultimately allowed to see — it changes
*when* the pass/fail check happens relative to the ranking pass. Two practical benefits from doing
it this way:

- **Separation of concerns.** The RRF/embedding ranking pass becomes a generic relevance signal
computed over "everything in the candidate's pools," independent of the fiddlier, per-candidate
constraint logic. Constraint filtering becomes a fast boolean pass over an already-ordered list, not
tangled into the SQL query plan.
- **It produces one clean, full ranked-and-filtered list per candidate**, which is exactly what the
caching/pagination design in Section 5 wants to slice pages out of — compute it once, serve many
pages from it, rather than re-deriving order per page.

### 3.2 The pipeline, in order

1. **Pool-matched skinny retrieval.** Fetch jobs where `pool ∈ active_subscribed_pools(candidate)`,
`is_active = true`, `processing_state = 'success'`, `opportunity_score IS NOT NULL`. Add a
reasonable freshness bound here too (e.g., last 30-60 days) — not present in the current spec's
retrieval step, but worth adding specifically to keep this ranking corpus bounded for high-volume
pools (a popular pool like `SOFTWARE_ENGINEER_FULLTIME` could otherwise accumulate a large backlog
of still-"active" but effectively stale postings). Columns fetched: `id`, `opportunity_score`,
`embedding`, `reference_at`, plus every column needed for (a) hard-constraint evaluation and (b)
`score_job()` — seniority, salary_min/max, sponsorship_status, requires_clearance, domain,
role_intent, is_internship, tech_stack/skills, capabilities, location fields. **Explicitly exclude**
`description_text` / `description_preview` — this was the single largest cost in the latency
report (≈3.7KB/job, ≈748KB for 200 rows) and none of it is needed for ranking or scoring, only for
display.
2. **Embedding similarity.** For each job in this set, cosine similarity against the candidate's
resume vector(s) (max-of-5, per Section 2). Cheap — sub-millisecond per comparison, same math
costed out for the ATS and percentile features.
3. **RRF fusion.** Two ranked lists over this same job set — one by `opportunity_score` descending,
one by embedding similarity descending — fused via `Σ 1/(k + rank)`, `k = 60`. Produces one fused
ordering across the full pool-matched, freshness-bounded set.
4. **Hard constraint pass.** Walk the RRF-ordered list, evaluate the Section 3.3 constraints
in-process against the columns already fetched in step 1 (no new DB round trip), drop jobs that
fail. Order is preserved for everything that survives.
5. **`score_job()` / `personal_score`.** Computed for the constraint-passing jobs. Per the latency
report, this step is cheap (111µs/job) and needs none of the deferred fat fields — so running it
across the *entire* surviving set (not just the first page) is fine, not just the first 40-100.
6. **Final sort, dedup, diversify.** Unchanged from the current spec:
`(personal_score, opportunity_score, reference_timestamp)` descending, dedup by
`(company, normalized_title)`, per-company diversification cap.

The output of step 6 is the candidate's full, ordered, eligible job-ID list for this session — this
is what gets cached (Section 5), not any intermediate stage.

---

## 4. Pagination & Caching

### 4.1 Your proposed approach, and why it's directionally right

Computing the ranking once for the wider candidate set and serving pages out of a cache, keyed by a
reference token, is the correct shape — everything costed out above (skinny retrieval, embedding
math, RRF fusion, constraint filtering, and even full `score_job()` scoring) is cheap enough to do
for the whole set up front, not just per-page. The one adjustment I'd make: **don't defer only
pagination — also defer and cache the profile/aux load**, because that's actually where most of
your current latency lives.

### 4.2 What gets cached, and why

Per the latency report: `profile_load` (4 sequential queries) was 1,365ms — ~59% of total warm
latency — and `aux_queries` (H1B, company enrichment, applied counts) was another 427ms (~19%).
Both of these are **candidate-scoped**, not job-scoped, and don't change mid-session. If we're
already introducing a 30-minute cache keyed by a reference token for the job list, the same cache
entry should carry the candidate's profile + capabilities + aux data too — so page 2 onward pays
none of that cost, not just the ranking cost.

**Cache entry (keyed by a generated reference token, e.g. UUID):**

```
{
  candidate_id,
  profile_snapshot,          # avoids re-running the 4-query profile load
  aux_snapshot,              # H1B/company/applied-count data
  ranked_job_ids: [...],     # full output of Section 3.2, step 6 — just IDs + order
  created_at,
  ttl: 30 minutes
}
```

Storing just IDs (not full job payloads) in the ranked list keeps this cache entry small — a few KB
even for a thousand-job list — cheap to store and cheap to slice.

### 4.3 Request flow

**First call (no reference token):**
1. Run the full pipeline in Section 3.2 end-to-end (profile load → skinny retrieval → RRF →
constraints → scoring → dedup/diversify).
2. Mint a reference token, cache the entry above with a 30-minute TTL.
3. Take the first page (40, per your stated cap) of `ranked_job_ids`, fat-fetch **only those**
(this is where `description_text` finally gets fetched), return jobs + reference token to the
client.

**Subsequent "load more" calls (reference token present):**
1. Look up the cache entry. If present: skip profile load, skip retrieval, skip RRF, skip scoring —
all already done. Slice the next batch of IDs (e.g. next 40, or up to 100 if the client requests a
larger page), fat-fetch just those, return.
2. If the token is missing or expired (>30 min, or evicted under memory pressure): transparently
re-run the full pipeline as if it were a first call, mint a new token. This should be invisible to
the client — same response shape, just slower on that one request.

### 4.4 Cache invalidation

Invalidate a candidate's active reference token (forcing a fresh pipeline run on their next request)
when their profile changes mid-session — same principle already suggested for the standalone
profile cache in the latency report. Otherwise, a candidate who edits their target seniority or
location mid-browse would keep seeing recommendations computed against their old profile for up to
30 minutes.

### 4.5 Does 100-at-a-time vs. 40-at-a-time matter here?

Not for backend cost — slicing 40 vs. 100 IDs out of an already-ranked, already-cached list and
fat-fetching them is the same shape of work either way, just linearly more or less of it. The 40-cap
you mentioned is a frontend/payload-size concern (matches the latency report's finding that JSON
payload size, driven by `description_text`, was a real cost) — that constraint should live in the
fat-fetch step (page size), not in how much of the ranking gets computed or cached up front.

---

## 5. Open Decisions (need your call before implementation)

1. **Freshness bound for the RRF ranking corpus** (Section 3.2, step 1) — proposed 30-60 days.
Needs a real number tied to how fast your pools accumulate active postings; too generous and the
ranking corpus grows unbounded for popular pools, too tight and you might exclude jobs that are
still genuinely open and relevant.
2. **Multi-pool jobs** (a job tagged into more than one of a candidate's subscribed pools) — counted
once in retrieval, or does pool overlap affect ranking at all? Current spec doesn't appear to
special-case this; flagging in case it matters for RRF's rank-position math (a job appearing in the
retrieval set only once regardless of how many pools it matches is the assumed default here).
3. **Cache store** — Redis (or equivalent) for the reference-token entries, sized for
concurrent-session volume. Not costed here since it's a standard infra choice, not a new compute
question.
