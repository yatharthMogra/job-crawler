# ATS Fit Score & Pool Percentile Ranking — Guidance Document

## Context: what exists today and what this adds

The platform currently computes a **personal score** for every job-candidate pair using
a weighted formula:

```
personal_score = 0.40 × capability + 0.25 × skill + 0.20 × location + 0.15 × comp
                 + seniority alignment (from the experience-tier system)
```

This score drives ranking in the Personalized Digest, the dashboard's recommended jobs
view, and the notification system. It answers the question: **"given everything we know
about this candidate, how well does this job match their profile overall?"**

What it does not answer — and what this feature adds — is: **"if this candidate applied
to this job today, how strong would their resume look to an ATS or recruiter screening
it?"** Those are related but different questions. A job can be a strong personal match
(right domain, right location, right tier) but the candidate's resume might be weak
against the specific skills and language of that posting. Or vice versa — a
lower-personal-score job might actually be one where the candidate's resume would look
exceptional compared to other applicants in the same pool.

This feature adds two new signals that together answer that second question:

1. **ATS Fit Score** — a per-candidate, per-job score reflecting how well the
   candidate's resume content matches the job's content, computed from three
   complementary signals blended together.
2. **Pool Percentile** — where that same ATS fit score sits relative to other candidates
   in the platform who are subscribed to the same job category (pool), so a user can see
   not just "I'm a 74/100 fit" but "I'm in the top 12% of people like me competing for
   this kind of role."

These are additive to the existing personal score, not a replacement for it. The
personal score answers "is this job right for you." The ATS fit score answers "are you
right for this job." Both are needed.

---

## What the ATS Fit Score is made of

Three signals, blended into a single 0–100 score:

### Signal 1: Skill and keyword match (primary signal)

The most direct measure of overlap between what the job asks for and what the candidate's
resume demonstrates. This should be the heaviest-weighted component because it's the most
directly actionable — a candidate can see exactly which skills are creating the gap.

The right technique here is **BM25** (a standard information-retrieval scoring function,
an improvement over simple keyword counting). BM25 accounts for:
- How often a term appears in the resume (term frequency)
- How rare or distinctive that term is across all job postings (inverse document
  frequency) — common words like "team" or "experience" matter less than distinctive
  terms like "Kubernetes" or "Monte Carlo simulation"
- Document length normalization — a long resume shouldn't automatically outscore a short
  one just because it mentions more words

The IDF component requires a **corpus** — specifically, how often each term appears
across all ingested job postings. This corpus needs to be built once and refreshed on a
schedule (nightly is sufficient). It is the thing that makes "Python" score lower as a
differentiator than "JAX" — because Python appears in almost every software posting
while JAX is specific.

The score from this signal should be **normalized to 0–1 by comparing against the job's
theoretical maximum** (how well the job description matches itself). This prevents a very
short or very narrow posting from artificially inflating scores.

The skills taxonomy used in this signal should be **phrase-aware**: "project management"
should match as a unit, not as "project" + "management" separately. The existing
enrichment pipeline already extracts skills from both resumes and job postings — those
extracted skill lists are the right foundation, supplemented by BM25 over the full text
for coverage of terms the taxonomy doesn't explicitly capture.

### Signal 2: Semantic similarity (supporting signal)

Two pieces of text can cover the same topic using completely different words — a resume
that says "built distributed data pipelines" and a job that says "experience with
large-scale ETL systems" are talking about the same thing, but keyword matching misses
this.

Semantic similarity uses **embedding vectors** — dense numerical representations of text
meaning, typically 384 dimensions for the model sizes appropriate to this use case.
Similarity between two embeddings (cosine similarity) reflects meaning-overlap regardless
of vocabulary.

Both the resume and the job description need to be converted to embedding vectors:
- The job's embedding is computed once at ingestion time and stored alongside the job
  record.
- The resume's embedding is computed once when the resume is saved/updated and stored
  alongside the resume record.
- At scoring time, this signal is just a dot product between two stored vectors —
  effectively free to compute.

**Important calibration note:** raw cosine similarity between sentence embeddings does
not naturally sit near 0 for unrelated content — embeddings tend to cluster, meaning
even unrelated texts may have similarity scores in the 0.5–0.7 range. The raw cosine
value needs to be **rescaled against your actual data** (what's the minimum and maximum
similarity you observe across real resume/job pairs on the platform) before it's
comparable to the other two signals. Do not use the raw cosine similarity as a 0–1
value without this calibration step.

### Signal 3: Structural match (supporting signal)

Direct, factual comparisons between what the job states and what the resume demonstrates:

- **Title similarity**: how closely the candidate's most recent or most prominent job
  title matches the target role's title. A "Data Engineer" applying to a "Data Engineer"
  role vs. a "Software Developer" applying to the same role.
- **Experience alignment**: the candidate's inferred years of experience vs. the job's
  implied experience tier (from the new experience-tier system being built in parallel).
  This reuses work already in progress — do not duplicate it.
- **Education alignment**: the candidate's stated degree level vs. what the posting
  implies or requires. Not all postings state this explicitly; infer when possible, leave
  neutral when not.

This signal is deliberately narrower in scope than the other two — it catches cases where
the other signals might look fine on surface (vocabulary overlap, semantic similarity)
but there's a fundamental structural mismatch (the job wants a PhD, the candidate has a
bachelor's; the job wants 8+ years, the candidate has 1).

### Blending the three signals

The three signals should be combined into a single 0–100 score with the skill/keyword
signal weighted most heavily, semantic and structural as supporting signals. Exact weights
are an implementation and calibration decision — the ordering (skill > semantic >
structural) is the product intent, not a specific number.

Before locking weights, spot-check the blended score against real resume/job pairs
already on the platform. The score should pass a basic sanity test: a "Data Engineer"
resume applying to a "Data Engineer" role should score substantially higher than a
"Marketing Manager" resume applying to the same role, and within the right roles, a
stronger-skill-match resume should consistently rank above a weaker one. If the ranking
doesn't feel right on spot-check, the weights need adjustment before shipping to users.

---

## What the Pool Percentile is

Once a candidate has an ATS fit score for a job, the natural next question is: **is that
score good?** A 65/100 means very little in isolation — it matters whether the average
candidate in the same pool is scoring 40 or scoring 80.

The pool percentile answers this by comparing the candidate's ATS fit score for a job
against the scores of all other platform users who are subscribed to the same job
category (pool). If a candidate scores in the 88th percentile for a Data Engineering
role, that means their resume looks stronger than 88% of Data Engineering candidates
on the platform who are competing for similar roles.

### How pools work in this context

Pools are the job categories already used by the recommendation engine (Software
Engineering, Data Engineering, AI/ML Engineering, Finance, Operations, etc.). Every job
is tagged with at least one pool at ingestion time. Every user subscribes to one or more
pools based on what they're looking for.

The percentile is computed **within the relevant pool** — a Data Engineering job's
percentile is computed against Data Engineering pool subscribers only, not all 10,000
users on the platform. This is the correct comparison group: an ML Engineer's resume
should be compared against other ML Engineers competing for the same roles, not against
a Finance candidate whose resume looks nothing like this posting and would naturally score
low regardless of the candidate's actual competitiveness.

### The efficient computation approach

Rather than storing a score per user per job (which would mean tens of thousands of rows
per job ingestion and massive write amplification), the system should store **only two
numbers per job**:

- The score at the **90th percentile** of the pool subscriber set
- The score at the **95th percentile** of the pool subscriber set

At display time, when a candidate's individual ATS fit score has been computed, these two
cutoffs are the only lookup needed:
- Score ≥ 95th percentile cutoff → show "Top 5%"
- Score ≥ 90th percentile cutoff → show "Top 10%"
- Below 90th → show the raw percentile or no badge, depending on UX decision

This eliminates per-user storage at ingestion time and makes the display-time lookup
trivial. The only compute that happens at ingestion is one matrix-vector multiply (the
job's embedding against all pool subscribers' resume embeddings) to get the distribution
of scores from which the two cutoffs are extracted.

### How the cutoff computation works at ingestion

1. When a new job enters the system, it gets tagged with its pool(s).
2. The pool's subscriber list is loaded — specifically, their stored resume embedding
   vectors. This should be kept as a warm in-memory or cached structure keyed by pool_id
   (rebuilt when users join/leave pools or update resumes), not re-queried from the DB
   on every job ingestion.
3. One matrix-vector multiplication: the job's embedding against the pool's subscriber
   matrix. This produces one similarity score per pool subscriber in a single operation.
4. The 90th and 95th percentile values of that score distribution are computed and stored
   against the job record.
5. Done — two numbers stored, no per-user rows written.

The cost of this operation is low: even for a pool with several thousand subscribers,
a single matrix-vector multiply in a numeric computing library (NumPy, PyTorch, etc.)
runs in milliseconds. It does not require a GPU or special infrastructure.

### Keeping cutoffs fresh

The pool membership changes over time as users join, update resumes, and unsubscribe.
The 90th/95th percentile thresholds stored at ingestion time will drift as the pool grows
or changes. For jobs that are still actively accepting applications, the cutoffs should
be recomputed on a schedule (nightly is sufficient) to keep the percentile badges honest.
This is the same cheap matrix-vector multiply — it is not expensive to rerun.

---

## Where these signals surface in the product

**ATS Fit Score** — displayed on the job detail view when a user opens a specific job.
This is a per-candidate, per-job computation that happens when the user views the job,
using their stored resume profile against the job's stored content profile. Not displayed
on the job list/card view (too much compute to do for every job in a list; surface it
when the user has expressed enough interest to open the posting).

**Pool Percentile badge** — displayed on job cards in the list view (e.g., "Top 10%")
using the precomputed cutoffs stored at ingestion time. This is fast to display because
the two cutoffs are already stored — the only work at display time is comparing the
user's score (computed when they open the card or lazily for the ones in view) against
the stored thresholds.

Both signals are **additive to the existing personal score and recommendation ranking** —
they do not change which jobs are recommended or in what order. They add a new layer of
information helping the user understand their competitive position, which is a different
question from whether the job is a good match for their preferences.

---

## Rollout sequencing

These two signals depend on different infrastructure. Build and ship them in order:

**Phase 1 — Skill/keyword score + structural score**
No new infrastructure required beyond the corpus IDF table, which can be built from
existing job data. Resume and job profiles already extract skills. Ship this first and
validate that the blended score feels correct on real data before adding more complexity.

**Phase 2 — Semantic similarity (embeddings)**
Requires adding embedding computation to both the job ingestion pipeline (at enrichment
time) and the resume save/update flow. Requires storing embedding vectors on both job
and resume records. This is new infrastructure — add it as a second phase once Phase 1
is validated.

**Phase 3 — Pool percentile**
Depends on embeddings (Phase 2) being live. Once embedding vectors exist for both jobs
and resumes, the matrix-vector multiply at ingestion time and the two-cutoff storage are
straightforward additions to the ingestion pipeline.

Never block Phase 1 waiting for Phase 2 or 3 — the skill and structural signals alone
are a meaningful and shippable improvement. The phases build on each other but each one
delivers real value independently.

---

## What "done" looks like

- Every job that a user opens shows an ATS Fit Score (0–100) reflecting how well their
  resume matches that specific job's content.
- Job cards for jobs where the user's fit is in the top 10% or 5% of the relevant pool
  show a badge reflecting that percentile.
- The score ranking is directionally correct on spot-check: stronger skill/experience
  matches consistently outscore weaker ones for the same job.
- The personal score and recommendation ranking are unchanged — this is purely additive.
- Percentile cutoffs are recomputed nightly for active jobs to stay current as pool
  membership evolves.
