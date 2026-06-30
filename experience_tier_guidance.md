# Experience-Tier Matching — Guidance Document

## The problem we're solving

Our recommendation engine currently has no domain-agnostic way to tell whether a job is
within realistic reach of a given candidate's experience level. The one seniority signal
that exists today (`normalized_jobs.seniority`: `SENIOR`, `STAFF`, `PRINCIPAL`,
`MANAGEMENT`, etc.) is a software-engineering career-ladder vocabulary. It works
reasonably for tech titles, but it doesn't generalize — a "Senior Financial Analyst," a
"Lead Operations Manager," or a "Principal Consultant" don't map onto that ladder in any
consistent way, and our platform is explicitly for *all* international students, not
just CS/engineering majors. **Do not modify, repurpose, or extend the existing
`seniority` field for this work — it stays exactly as-is, for whatever it currently
serves.** This is new, additive work.

The real-world failure mode we're trying to fix: a candidate with zero professional
experience gets recommended a "Principal Data Scientist" role, or a candidate with seven
years of experience in their home country gets recommended a "New Grad" program. Both are
technically real, open jobs — but neither is a realistic application for that candidate,
and recommending them erodes trust in the platform. This is a known weakness in
competing products (e.g. ZipRecruiter has been observed recommending Principal-level
roles to clearly non-Principal candidates), and getting this right is a genuine
differentiator, not a nice-to-have polish item.

---

## The core idea

Every job posting implies a level of professional experience a realistic candidate would
need — even when the posting never states a number. A "Staff Engineer" posting and a
"Senior Financial Analyst" posting are both asking for a similar order of magnitude of
experience, even though neither says "8 years" anywhere in the text. People intuitively
read this from title, tone, and the responsibilities described. We want the enrichment
pipeline to make that same judgment, explicitly, for every job, and we want every
candidate to have a comparable value on their profile, so the two can be compared
directly.

**This is not about extracting a literal number of years from the posting text.** Most
postings never state one, and asking an LLM to manufacture a number when none is present
just produces false precision. What we actually want is a **tier classification** — a
judgment call the LLM is well-suited to make by reading the whole posting in context,
the same way a person would.

---

## The tier ladder

Six tiers, ordered, domain-agnostic:

```
INTERN
NEW_GRAD
JUNIOR
MID
SENIOR
ABOVE_SENIOR
```

These are deliberately *not* literal job titles. A posting titled "Staff Engineer," a
posting titled "Principal Consultant," and a posting titled "Engineering Manager" might
all land on `ABOVE_SENIOR` — the label on the ladder describes the *level of experience
realistically required*, not the literal words in the title. Title alone is not a
reliable signal (a "Senior Analyst" at one company can be a junior-equivalent role at
another) — the classification should weigh the actual responsibilities and expectations
described in the posting at least as heavily as the title itself.

This ladder needs to live in exactly two places conceptually:

1. **On every ingested job** — one tier value, representing what level of candidate this
   posting is realistically asking for.
2. **On every user profile** — one tier value, representing what level the candidate
   actually is today.

Both sides use the identical six-value vocabulary. That symmetry is what makes the
comparison possible — we are not comparing a job's tier to a *range of acceptable*
tiers, we are comparing one tier to one tier, directly, the same way distance works on
any ordered scale.

---

## What this is for, specifically

Two distinct uses, both needed, neither a substitute for the other:

**1. A visibility gate.** Jobs at the very top of the ladder (`ABOVE_SENIOR`) should not
be shown to our audience at all, by default. Nobody using this platform is a realistic
candidate for an org-level/principal/director-equivalent role, regardless of which
domain it's in. This should be a deploy-time configurable cutoff (which tier is the
default ceiling), not a hardcoded assumption — we may want to revisit this as our user
base evolves, without needing a code change to do it.

**2. A ranking signal.** Among everything that passes the visibility gate, a job's tier
relative to the candidate's own tier should meaningfully affect how well-matched that job
appears to be. A `MID`-tier candidate should see `MID`-tier jobs ranked above `JUNIOR` or
`SENIOR` jobs, which should in turn rank above `INTERN` or `NEW_GRAD` jobs — distance
on the ladder should translate into a real, graduated difference in how strongly we
recommend something, not a binary in-or-out. This is the part that directly solves the
ZipRecruiter-style failure: even a job that survives the gate (because it's not
*forbidden*) should not appear at the top of someone's recommendations if it's three or
four tiers away from where they actually are.

These two mechanisms are intentionally separate layers doing different jobs. The gate
answers "should this candidate ever see this posting." The ranking signal answers "how
strongly should we recommend it, given everything else they could see instead." Don't
collapse them into one mechanism — we want the flexibility to, for example, loosen the
gate without flattening the ranking signal, or tighten the ranking sensitivity without
changing what's visible at all.

---

## Why this matters more for our specific audience than it might for a generic job board

Our candidates are disproportionately international students and early-career
professionals navigating visa/work-authorization timing, which makes getting this right
unusually consequential for us specifically:

- A student who hasn't yet completed their degree is a realistic candidate for
  internships, and a *bad* candidate for "New Grad" full-time programs that expect a
  completed degree and an immediate start — these are genuinely different audiences even
  though both are "early career."
- A candidate who already has several years of full-time professional experience in
  their home country, now pursuing a Master's in the US, is not a fresh new-grad — they
  are often functionally `JUNIOR` or `MID` tier already, and recommending them
  exclusively new-grad-labeled roles undersells their real experience and makes the
  platform feel useless to them specifically. This is a large and meaningful slice of
  our actual user base, not an edge case.
- Symmetrically, someone with six or seven years of prior experience is not a sensible
  match for an entry-level or new-grad posting, even if that posting happens to be open
  and visible.

Getting the tier comparison right is, in effect, recognizing each person's real starting
point rather than assuming everyone applying through our platform is starting from zero.

---

## How "unknown" should be treated

Some postings will give the enrichment step nothing usable to classify from — this should
be a real, legitimate outcome (`UNKNOWN`), not something we force a guess on. The product
intent here: a job we can't confidently place on the ladder should land in a deliberately
neutral position in the ranking — neither boosted as if it were a confirmed great match,
nor buried as if it were confirmed to be a bad one. It should sit roughly in the middle of
the realistic score range a candidate would see, so someone who has run out of
confidently-matched options still sees it as a reasonable, if uncertain, option — not
hidden, not over-promoted.

---

## Where this needs to show up

- **Every job, at ingestion/enrichment time.** Every job that goes through enrichment
  should come out with a tier value (or `UNKNOWN`). This needs to apply across every
  connector and every domain we ingest from — software, finance, operations, design,
  everything — since the entire point is that this generalizes past the
  software-specific ladder we already have.
- **Every user profile.** Every candidate needs a current-tier value derived from
  something concrete and self-reported (e.g., total years of full-time professional
  experience, whether they're still completing their degree) — not a self-selected label
  like "I am a Senior," which we'd expect people to round up on. The actual onboarding
  question/UX for capturing this is left to your judgment, but the resulting value
  stored should be one of the six tier labels, derived consistently with how we ask the
  enrichment step to think about jobs, so the two sides of the comparison mean the same
  thing.
- **The visibility gate**, applied wherever jobs are retrieved for a candidate (the same
  places the existing per-user seniority filtering already happens today — notifications,
  recommended jobs, and anywhere else jobs are surfaced to a specific profile).
- **The ranking signal**, applied as part of the existing personal-score computation,
  contributing as one component among the others already in that formula (capability
  match, skill match, location, compensation) — not replacing any of those, just adding
  this as another input with its own weight.
- **Backfill.** The existing ~40K already-ingested jobs need to go through this
  classification too, not just newly-ingested jobs going forward — otherwise the signal
  is only partially available and comparisons between an old job and a new job would be
  inconsistent.

---

## What "done" looks like

- Every job in the system (new and backfilled) has a tier value or `UNKNOWN`, derived
  from the job's actual content, not from the old software-specific `seniority` field.
- Every user has a current-tier value derived from a concrete, self-reported signal.
- A deploy-time configurable ceiling controls which tiers are visible at all.
- The personal score for a candidate reflects ladder-distance between their tier and a
  job's tier, with `UNKNOWN` landing in a deliberately neutral middle position.
- A candidate with several years of prior experience no longer gets buried in
  new-grad-only recommendations, and a candidate with no experience no longer sees
  senior/principal-level roles ranked as strong matches.
