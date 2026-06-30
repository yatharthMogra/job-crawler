# Email Notification System — Guidance Document

## Overview

The notification system adds two distinct, opt-in email channels on top of the existing
recommendation engine. Both consume the same underlying job data and enrichment output
that the platform already produces — this is not a new data pipeline, it is a new
delivery layer sitting above the existing one.

Both notification types are independent of each other. A job can appear in both a
Company Watch email and a Personalized Digest without any cross-checking or dedup
between them. Users who receive both should expect that — these are not competing
channels, they serve different intentions.

---

## Notification Type 1: Company Watch

### What it is

A user-defined list of specific companies they consider high-priority targets. When any
of those companies posts a new role that matches the user's saved preferences, the user
is notified as quickly as the platform is able to — the intent is that the user is among
the first applicants.

### What the user provides

A list of companies, selected from the platform's existing company catalog. Search is
against the catalog only — if a company does not appear in search results, it is not in
the catalog and cannot be watched. Users may request that a company be added to the
catalog, but this does not trigger automatic addition and does not change the watch until
the catalog is updated on the platform's own timeline.

Because Company Watch is scoped to the catalog, every watchable company already has an
active connector. There is no "we don't have a connector for this yet" case to handle at
the watch level — it's structurally impossible given the catalog constraint.

### What triggers a notification

A new job from a watched company enters the system, clears enrichment, and satisfies
**all** of the user's preference filters simultaneously:

- Role family / domain matches what the user is looking for (e.g., SWE, ML, Data
  Engineering — not every role the company posts, only the ones relevant to this user)
- Employment type matches (e.g., internship only, not full-time roles from the same
  company)
- Hard constraints pass (sponsorship requirement, experience tier from the new
  experience-tier system, location if the user has location constraints)

The personal recommendation score is **not** a gate for Company Watch. The question is
not "is this a good match" — it's "did this company post something that fits what I said
I'm looking for." A job that scores modestly on personal fit should still trigger a
Company Watch notification if it passes the user's preference filters. The user made an
explicit declaration that this company matters to them regardless of score.

### Timing

The notification fires as soon as the platform is aware of the job — specifically, once
the job has cleared enrichment and is confirmed to match the user's preferences. The
practical latency from real-world posting to notification is bounded by how frequently
the company's connector runs, not by any separate notification-side delay. If a company's
connector fetches every four hours, Company Watch can only be as fast as four hours from
posting. The user-facing promise should therefore be framed as "within 30 minutes of us
learning about it," not "within 30 minutes of the company posting it."

There is no batching within Company Watch. If three watched companies post on the same
day, the user receives up to three separate notifications — one per event. Batching works
against the core purpose of this channel, which is speed.

### Volume control

The only volume control is the user's own preference filters. The platform does not
impose an additional cap on how many Company Watch emails a user can receive — if the
user watches 20 companies and all 20 post matching roles on the same day, they receive 20
notifications. This is the intended behavior: the user explicitly opted into being
informed about these companies as fast as possible.

---

## Notification Type 2: Personalized Digest

### What it is

A scheduled email containing the top-K job recommendations for the user, optionally
constrained by user-defined filters, sent at a cadence the user chooses. This is the
merge of what were previously "Daily Recommendations" and "Filtered Digest" into a single
unified concept.

**Daily Recommendations are simply Personalized Digest with no user-set filters and a
daily default cadence.** There is no separate "Daily Recommendations" product anymore —
users who don't set any filters get the same experience they had before, just expressed
through the same underlying system.

### What the user provides

**Filters (optional):** location(s), compensation floor, domain(s)/role families,
employment type. These narrow the pool of jobs the digest considers. A user who sets no
filters gets the platform's full recommendation pool, same as before the merge. A user
who sets filters gets recommendations drawn only from the jobs that satisfy those filters.

**Cadence:** how frequently the digest sends. Minimum is 3 hours; default is 24 hours;
maximum is 7 days (weekly). The user picks from this range. The digest only sends if
there are jobs to send — if no new matching jobs have entered the system since the last
digest, no email goes out.

**K (top-K):** how many jobs appear in the email. This is configurable, with a platform
default. The intent is that the digest is scannable in a reasonable amount of time —
not an exhaustive list of everything that matched.

### Selection and ranking logic

This is the critical design decision for the merge: **user-set filters are a constraint
on the recommendation pool, not a replacement for the recommendation model.**

Concretely:

1. The system takes all jobs that have entered the platform since the user's last digest
   send and that satisfy the user's hard constraints (sponsorship, experience tier, etc.)
2. It further narrows by the user's optional digest filters (location, comp floor,
   domain, employment type) — jobs that don't match these are excluded from
   consideration for this digest
3. From what remains, it ranks by the user's personal score (the existing
   capability/skill/location/comp/tier-alignment weighted formula)
4. It takes the top-K from that ranked list and sends them

The platform is still exercising its recommendation judgment — the user's filters narrow
the input pool, but the platform decides the order within that pool. This is what
distinguishes the Personalized Digest from a generic job board search result: the
ranking reflects the user's actual profile, not just filter-match. A job that perfectly
matches all the user's filters but scores poorly on personal fit will still appear below
a job that matches all filters and scores well on personal fit.

The global opportunity score (which reflects freshness and external signals independent
of this specific user) acts as a secondary sort signal when personal scores are close —
fresher, higher-opportunity-score jobs break ties.

### What "since last send" means

The digest window is rolling, not fixed to a calendar day. A user who sets a 3-hour
cadence gets jobs that entered the system in the last 3 hours. A user who sets a 24-hour
cadence gets jobs from the last 24 hours. The timestamp of the previous send is what
anchors the window, not midnight or any fixed clock.

If no qualifying jobs entered the system in the window, no email is sent. The clock
resets from the last actual send, not from the scheduled-but-skipped send time — so a
user with a 3-hour cadence who gets no email for 9 hours (because nothing matched)
doesn't receive a 9-hour backlog all at once when something finally matches. The next
send covers only the period since the previous successful send.

---

## How the two types relate to each other

They are independent. A job can appear in a Company Watch notification and then also
appear in a subsequent Personalized Digest for the same user. This is expected and fine —
the user may want the speed of Company Watch for a specific company AND the ranked
context of seeing that same job alongside other recommendations in their digest. No
cross-checking between the two is needed.

The three things a user can receive:

| Channel | Trigger | Selection logic | Cadence |
|---|---|---|---|
| Company Watch | New job from watched company passes preference filters | Filter-match only; personal score not a gate | Event-driven, as fast as ingestion allows |
| Personalized Digest | Scheduled | Filter-constrained pool, ranked by personal score, top-K | User-chosen: 3hr to 7d, default 24hr |

---

## What is out of scope for this system

- **Auto-adding companies to the catalog based on user requests.** User requests are
  tracked but fulfilled on the platform's own timeline. The notification system has no
  influence on catalog additions.
- **Cross-notification deduplication.** The three channels (Company Watch, Personalized
  Digest, and any future channel) do not check each other before sending. A job can
  legitimately appear in more than one notification to the same user.
- **Application tracking or confirmation.** Notifications link to the job posting and
  drive the user to apply externally. Whether the user applied, was screened, or got an
  offer is outside the scope of this system.
- **Real-time push notifications (mobile/browser).** Email is the delivery mechanism.
  Other notification surfaces are out of scope for this phase.

---

## Open implementation considerations (for the implementing agent)

These are decisions that affect implementation shape but are not resolved in this
guidance document — they should be made in context of the existing codebase:

- **Where Company Watch matching runs.** Whether Company Watch preference-filter matching
  happens inline at job ingestion time (as each job hits the DB) or asynchronously
  (similar to how enrichment is queued separately from ingestion) is an implementation
  choice. The product requirement is just: it fires as soon as possible after the job
  clears enrichment.
- **Email sending infrastructure.** Choice of sending service (SendGrid, Postmark, SES,
  etc.), deliverability setup (SPF/DKIM/DMARC), bounce handling, and unsubscribe
  mechanics are implementation concerns not covered here.
- **Per-user digest scheduling.** Whether individual user digest schedules are managed
  via APScheduler (like the existing fetch-tick), a DB-driven queue polled on a tight
  interval, or another mechanism is an implementation concern. The product requirement is
  just: the cadence is per-user, user-configurable, and the send window anchors to the
  previous actual send time.
- **K default and configurability.** The platform should set a default K and optionally
  allow users to adjust it. What those values are is an implementation/product decision
  not fixed here.
