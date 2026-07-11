# Qualification Fit Score — Redesign Implementation Plan

**Status:** Approved direction, ready for agent implementation
**Replaces:** the `personal_score`-as-display-percentage pattern described in
`match-percentage-spec.md`. `personal_score` continues to exist for **ranking only** — see
Section 4.

---

## 0. What's changing and why (one paragraph, for anyone skimming)

The current display percentage answers "what fraction of the candidate's total background did
this job happen to use" — a metric that's structurally incapable of reaching high values for any
candidate with a normal, broad profile, regardless of true fit. We're replacing it with a metric
that answers the actual question — "how much of what this job needs does the candidate have" — and
removing preference signals (location, compensation) from that number entirely, since those measure
whether the candidate wants the job, not whether they're qualified for it.

---

## 1. Reuse validation — is the ATS engine (Point 1) actually reusable here, or just similar?

Worth being precise about this rather than assuming, since it changes what the agent needs to
build.

**What's genuinely shared, no new infra needed:**
- **Embeddings.** Resume embeddings (max-of-5) and job embeddings are already planned per the
pagination/RRF doc — precomputed, cached, cheap. The semantic partial-credit layer for this score
consumes those same vectors directly.
- **BM25 skill matching doesn't need raw resume text.** This was worth checking carefully: BM25
needs term frequencies, but there's no requirement that the "document" be free-text — the
candidate's existing structured skill lists (`languages`, `frameworks`, `tools`, `databases`,
`other`) and the job's existing structured `tech_stack ∪ skills` work as the term sets directly.
So the skill-coverage component can run on data **already being collected today**, no new resume
parsing pipeline required for this piece specifically.
- **Corpus-wide IDF** (from Point 1's design) applies unchanged — same nightly job, same table.

**What's genuinely new work, not free:**
- **Required vs. preferred skill extraction at ingestion.** The current schema has no such split —
`tech_stack ∪ skills` is one undifferentiated set. This needs new NLP work at ingestion time
(section-aware parsing — "Requirements" vs. "Nice to have" / "Preferred" sections of a job
description, or a classifier if postings aren't cleanly sectioned). This is the one piece with real
net-new engineering effort.
- **A structural (years-of-experience / education) component.** Not present in `personal_score`
today at all — `cap_score`/`skill_score`/`loc_score`/`comp_score` cover capability, skill, location,
compensation, but nothing checks experience level or education against the job's stated
requirements. Point 1's regex-based extraction (years-of-experience from date ranges, education
level from degree keywords) is directly reusable on both sides — this is additive, not a rebuild.

**Verdict:** the reuse is real, not just conceptually similar — most of the underlying machinery
(embeddings, structured skill sets, corpus IDF) either already exists or is already planned for
other reasons. The genuinely new pieces are scoped and small. Proceed with reuse.

---

## 2. The new formula

### 2.1 Keep capability and skill as two distinct components

These currently measure different things (a broader competency/domain taxonomy vs. concrete
tools/tech) and there's no reason to collapse them into one BM25 pass — fix the math on each
independently rather than merging them.

### 2.2 Skill coverage (job-anchored, required/preferred split, BM25 + semantic partial credit)

```
required_coverage  = Σ over job's required_skills of best_fuzzy_match(skill, candidate_skills)
                      / |required_skills|

preferred_coverage = Σ over job's preferred_skills of best_fuzzy_match(skill, candidate_skills)
                      / |preferred_skills|
                    = neutral (e.g. 1.0, so it doesn't penalize) if job lists no preferred skills

skill_coverage = 0.80 × required_coverage + 0.20 × preferred_coverage
```

`best_fuzzy_match(skill, candidate_skills)` is not a strict set-membership check — it's the BM25
term-weighted match (using corpus IDF) blended with embedding similarity for near-misses, same
mechanism as Point 1, just pointed at the candidate's structured skill set instead of free resume
text, and at the job's required/preferred lists instead of a single flat skill set. **Denominator is
the job's requirement count, not the candidate's total skill count** — this is the core fix.

### 2.3 Capability coverage (job-anchored, same directional fix)

```
capability_coverage = |job_capabilities ∩ candidate_capabilities_fuzzy| / |job_capabilities|
                     = neutral if job lists no capabilities
```

Same fix as skills — anchor to what the job asks for, not the candidate's total capability list.
Fuzzy-matched the same way (embedding-assisted), not strict set intersection.

### 2.4 Structural score (new)

```
structural_score = (experience_adequacy + education_adequacy) / 2
```

Same logic designed in Point 1: years-required vs. years-inferred from the candidate's work history
dates; education-level-required vs. inferred, using the same regex extraction already built for the
ATS score. Neutral (1.0) if the job states no explicit requirement on that dimension.

### 2.5 Raw qualification fit

```
qualification_fit_raw = 0.45 × skill_coverage
                       + 0.30 × capability_coverage
                       + 0.25 × structural_score
```

These weights are a starting point, not a derived constant — same caveat as Point 1's blend:
calibrate by spot-checking against a real sample of (candidate, job) pairs you already have, and
adjust until the relative ordering feels right, before locking defaults.

**No location. No compensation. No seniority multiplier.** All removed from this score — see
Section 3 and 5.

---

## 3. Preferences move out of the score entirely — where they go instead

Location, compensation, and any preference-style signal are removed from the qualification fit
score, per the direction agreed: this number answers "how well do you fit the job," not "how well
does the job fit your preferences." They don't disappear from the product:

- **Ranking** (`personal_score`, feed sort order) keeps incorporating them — see Section 4.
- **Display**, alongside the qualification fit percentage, show them as separate strength/gap
indicators (e.g. "Remote-friendly," "Meets your salary expectations," "Outside your preferred
location") rather than folded into the number. This is a `web` / card-rendering change, not a
scoring change — worth a short separate ticket, not detailed further in this doc since it's UI, not
scoring architecture.

---

## 4. `personal_score` (ranking) — what changes, what doesn't

`personal_score` keeps its job: sort order for the recommendation feed. It keeps incorporating
location and compensation, since those legitimately affect what a candidate should see *first*, even
though they shouldn't affect the *qualification* number shown on the card. What changes:

- Its `cap_score` and `skill_score` inputs should be replaced with the new job-anchored
`capability_coverage` / `skill_coverage` computations (Section 2.2/2.3) instead of the old
candidate-anchored Jaccard ratios — there's no reason to keep feeding a known-broken metric into
ranking just because it's not user-facing anymore. Feel free to reuse the *raw*, uncalibrated
values here (Section 6's calibration step is a display-only rescaling; since it's monotonic, it
doesn't change relative order, so ranking can use either raw or calibrated values interchangeably —
raw is simpler, no reason to compute both).
- `loc_score`, `comp_score`: unchanged.
- **Seniority multiplier: removed** — see Section 5.

```
personal_score = 0.40 × capability_coverage
               + 0.25 × skill_coverage
               + 0.20 × loc_score
               + 0.15 × comp_score
```

(Weights here are the existing production defaults, carried forward unchanged — only the
`cap`/`skill` *inputs* change, not the ranking weights themselves. Re-tuning the ranking weights is
a separate concern from this doc.)

---

## 5. Removing the seniority multiplier — confirmed as dead code, not just deprecated

Worth stating precisely why this is safe to remove outright, not just deprioritized: per the current
spec, the SQL hard filter already requires `seniority IN (target_seniority ∪ {UNKNOWN})` before a
job ever reaches scoring. A `SENIOR`-tier job outside the candidate's target set fails that
condition and is excluded at retrieval — it never reaches `score_job()` in the first place under the
filter as currently specified. That means the ×0.6 multiplier in Section 4.3 of the original spec
describes a code path that the current hard filter has already made unreachable — it's not a
redundant safety net, it's dead code left over from before the hard filter existed. Confirms your
account of the history exactly. Delete it; no replacement needed.

---

## 6. Calibration / display rescaling

Applied only to the version of `qualification_fit_raw` that gets displayed (not the ranking-internal
copy per Section 4):

1. Compute `qualification_fit_raw` across a real sample of existing (candidate, job) pairs on the
platform.
2. Take the observed 5th and 95th percentile raw values as the effective floor/ceiling.
3. Map that range onto the 0-100 display scale (linear, or a mild curve if the raw distribution is
skewed), clamped at the edges.
4. Sanity-check the resulting distribution against the tiers you want to be meaningful (90%+ /
70-80% / <70%) — adjust the floor/ceiling percentiles if the bands don't land where they should.
5. Re-run this calibration periodically (e.g. quarterly, or after any change to the underlying
skill taxonomy/corpus) — it's a statistical fit against your own data, not a one-time constant.

This step is explicitly about correcting for the fact that averaging several bounded [0,1]
sub-scores compresses toward the middle by construction — it is not re-introducing the "make it
look better than it is" problem, since it's applied on top of a metric that is now actually
measuring the right thing (Section 2), not on top of the old broken one.

---

## 7. Rollout sequencing

1. Ship the ingestion-time required/preferred skill extraction first — everything downstream depends
on it.
2. Implement `qualification_fit_raw` (Section 2) behind a flag, shadow-compute it alongside the
current score without displaying it yet.
3. Sample real output, sanity-check the distribution, tune the Section 2.5 weights if needed.
4. Fit and apply the calibration layer (Section 6).
5. Cut `personal_score`'s `cap`/`skill` inputs over to the new coverage functions (Section 4),
remove the seniority multiplier (Section 5) — these can ship independently of the display cutover
if you want to de-risk them separately.
6. Switch the card display from the old `personal_score`-derived percentage to the calibrated
qualification fit score. Update the strength/gap tags (Section 3) in the same UI pass.
7. Retire the old `cap_score`/`skill_score` Jaccard functions once nothing references them.

---

## 8. Open items for the team to confirm before/during implementation

1. **Required/preferred extraction method** — rule-based section parsing vs. a small classifier.
Not specified here; depends on how consistently your job sources structure their postings.
2. **Section 2.5 weights** (0.45/0.30/0.25) and the required/preferred split (0.80/0.20 in 2.2) are
starting points — flag for calibration against real data, not treated as final.
3. **Calibration refresh cadence** (Section 6, step 5) — pick a concrete schedule once the team knows
how often the skill taxonomy/corpus shifts in practice.
