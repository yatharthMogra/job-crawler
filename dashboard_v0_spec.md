# Career Match AI — User Dashboard
## V0 Build Specification

---

## What We Are Building

A job discovery and recommendation dashboard for students and early-career candidates. Users come here to find relevant job opportunities, see personalized recommendations, and apply quickly.

The dashboard is optimized for **speed, signal density, and decision throughput** — not storytelling. Think Jobright or Linear, not LinkedIn or Greenhouse.

**Tech stack:** React, Tailwind CSS, light theme, desktop-first (mobile responsiveness is a bonus, not a requirement for V1).

---

## Overall Layout

Three-column layout on desktop:

```
┌──────────────┬────────────────────────────────┬───────────────────┐
│              │                                │                   │
│  Left        │     Main Feed                  │  Job Detail       │
│  Sidebar     │     (job cards)                │  Drawer           │
│  (fixed)     │                                │  (slides in when  │
│              │                                │   job is clicked) │
│  ~220px      │     flexible width             │  ~420px           │
│              │                                │                   │
└──────────────┴────────────────────────────────┴───────────────────┘
```

The drawer is hidden by default. When a job card is clicked, the drawer slides in from the right. The feed remains visible and scrollable behind it.

The left sidebar is always visible and never collapses on desktop.

---

## Color Palette and Visual Style

**Theme:** Light. Clean whites and very light grays as backgrounds. No gradients.

**Palette:**
- Background: `#FAFAFA` (page) / `#FFFFFF` (cards, drawer)
- Sidebar background: `#F4F4F5`
- Border/dividers: `#E4E4E7`
- Primary text: `#09090B`
- Secondary text: `#71717A`
- Muted text: `#A1A1AA`
- Accent (CTAs, links, active states): `#18181B` (near-black) or a subtle indigo `#4F46E5`
- Apply button: solid dark — `#09090B` text on white, or inverted
- Save button: ghost/outline style
- Success green (for match tags): `#16A34A` text on `#F0FDF4` bg
- Card hover: very subtle shadow lift `shadow-sm`

**Typography:**
- Font: Inter or Geist (both available in Tailwind/Vercel ecosystem)
- Job title: `font-semibold text-sm` or `text-base`
- Company name: `text-sm text-zinc-500`
- Meta info (location, comp): `text-xs text-zinc-500`
- Match tags: `text-xs font-medium`

**Feel:** Minimal, dense, purposeful. No rounded corners larger than `rounded-md`. No drop shadows larger than `shadow-sm`. No colorful gradients.

---

## Left Sidebar

Fixed, full-height sidebar. Width ~220px.

**Top of sidebar:**
- App logo/wordmark: "Career Match AI" — small, left-aligned, top padding
- Small divider

**Navigation items (vertical list):**

```
○  All Jobs
★  Recommended
🔖  Saved
✓  Applied
────
👤  Profile
⚙  Preferences
```

Each item is a clickable row with:
- Icon (small, 16px)
- Label
- Active state: dark background pill or left border accent
- Hover state: light gray background

**Bottom of sidebar:**
- User's name and email (small, muted)
- No logout button needed for V1

---

## Tab Behavior

The main navigation items map to feed tabs. Clicking a nav item changes the feed content. The URL should update (`/jobs`, `/recommended`, `/saved`, `/applied`).

The active tab is visually indicated in the sidebar.

---

## Main Feed — All Jobs Tab

### Filter Bar

Sticky at top of the feed area. Does not scroll away.

```
┌─────────────────────────────────────────────────────────────────┐
│  [Role ▾]  [Location ▾]  [Remote ▾]  [Compensation ▾]  [Date ▾] │
└─────────────────────────────────────────────────────────────────┘
```

Each filter is a dropdown button. When active (a filter is set), the button shows the selected value and a small `×` to clear it. Active filters have a slightly darker border.

Dropdowns are small, clean, not full-screen overlays.

Role filter options: SWE, Backend Engineer, Frontend Engineer, ML Engineer, Data Engineer, Data Scientist, Full Stack, DevOps, Product Manager

Remote filter options: Remote, Hybrid, Onsite, Any

Compensation: simple input range (min salary)

Date Posted: Last 24h, Last 3 days, Last week, Any

Below the filter bar: a faint result count — `"317 opportunities"` — left-aligned, `text-xs text-zinc-400`.

---

### Job Cards

Cards are the core UI element. They appear in a vertical list in the feed. Each card is compact — maximum ~120px tall. No wasted whitespace.

**Card layout — two columns:**

```
┌──────────────────────────────────────────────────────────────────┐
│ [Logo] Job Title                    │  ✓ Backend Engineering     │
│        Company · Location           │  ✓ Distributed Systems     │
│        $180k–$225k · Full-time      │  ✓ AWS                     │
│        Posted 2h ago                │                            │
│                                     │  Strong backend alignment. │
│  [Apply ↗]  [Save]  [Hide]          │  Effort: Low               │
└──────────────────────────────────────────────────────────────────┘
```

**Left column (~60% width):**

Top row:
- Company logo: 32×32px rounded square. Use a placeholder gray square with company initial if no logo. Do NOT call any external logo API.
- Job title: `font-semibold text-sm text-zinc-900` — single line, truncate if too long
- Freshness: `text-xs text-zinc-400` — "2h ago" / "just now" / "3d ago"

Middle row:
- Company name · Location · Remote type (e.g. "ScaleAI · New York, NY · Hybrid")
- Salary range if available: "$180k–$225k"
- Employment type: "Full-time" or "Internship"
- All in `text-xs text-zinc-500`, dot-separated on one line

Bottom row (action buttons, small):
- **Apply ↗** — primary button, small, opens posting URL in new tab
- **Save** — ghost button, small, toggles saved state (bookmark icon fills on save)
- **Hide** — ghost button, very muted, removes card from feed

**Right column (~40% width):**

Separated by a faint vertical divider.

Match evidence tags (only shown in **Recommended** tab and **All Jobs** when personalization is active):
- Up to 4 tags, each a small pill: `✓ Backend Engineering` in green-tinted pill
- `text-xs font-medium text-green-700 bg-green-50 rounded-full px-2 py-0.5`

If no personalization context (All Jobs tab, no profile match): this column shows just the opportunity metadata compactly:
- Effort badge: `Low / Medium / High` — color coded (green/yellow/orange)

One-line recommendation reason (Recommended tab only):
- `text-xs text-zinc-500 italic` — e.g. "Strong backend alignment + high compensation."
- Maximum one sentence. No wrapping beyond one line.

**Card states:**
- Default: white bg, `border border-zinc-100`
- Hover: `shadow-sm` lift, cursor pointer
- Saved: bookmark icon filled
- Applied: subtle green left border accent
- Hidden: removed from feed immediately

---

## Main Feed — Recommended Tab

Same card layout as All Jobs. The right column is always populated with match evidence tags and recommendation reasoning.

A small info banner at the top of the feed (dismissible):
> "Ranked by how well each opportunity matches your profile. Based on your capabilities, skills, and location preferences."

Small, `text-xs`, light gray background, dismissible with ×.

---

## Main Feed — Saved Tab

Same card layout. Shows only saved jobs.

Empty state if no saved jobs:
```
        🔖
   No saved jobs yet.
   Browse All Jobs and save roles you want to revisit.
   [Browse All Jobs →]
```

Centered, muted, with a CTA button.

---

## Main Feed — Applied Tab

Same card layout. Shows jobs the user has marked as applied.

Each card has an additional "Applied" badge (small green pill, top-right of card).

Empty state:
```
        ✓
   No applications tracked yet.
   After applying, mark a job as Applied to track it here.
```

---

## Infinite Scroll Behavior

The feed uses infinite scroll. No page numbers.

As the user scrolls near the bottom:
- Show a subtle loading spinner (3 dots or a thin bar)
- Load next batch of cards
- Append to list

If no more jobs:
- Show `"You've seen all available opportunities."` — centered, muted text

---

## Job Detail Drawer

Opens when a job card is clicked anywhere except the action buttons. Slides in from the right. Width ~420px. Feed narrows to accommodate.

Drawer has a close button (`×`) top-right.

**Drawer sections (top to bottom):**

**1. Job Header**
- Company logo (larger, 48×48)
- Job title (larger, `text-lg font-semibold`)
- Company name · Location
- Posted X ago
- Big **Apply Now ↗** button — full width, prominent

**2. Quick Stats Row**
Horizontal row of compact pills:
- Salary: `$180k–$225k`
- Type: `Full-time`
- Effort: `Low effort`
- Remote: `Hybrid`

**3. Why This Fits (only in Recommended tab context)**
Section header: "Why this fits your profile"
- List of match reasons: `✓ Backend Engineering`, `✓ Distributed Systems`, `✓ AWS`
- Each as a green-tinted tag
- One sentence reasoning below: *"Strong backend + distributed systems alignment."*

**4. Job Description**
Section header: "About the role"
- Full job description rendered as clean HTML (strip any inline styles from source)
- `prose prose-sm` Tailwind typography
- Scrollable within the drawer

**5. Extracted Details**
Section header: "Skills & Requirements"
- Skills as tags: Python, AWS, Distributed Systems, Kafka...
- `text-xs bg-zinc-100 text-zinc-700 rounded px-2 py-1`

**6. Apply Footer (sticky at drawer bottom)**
- Apply button (full width)
- Save button (ghost, full width)

---

## Empty States

Each tab needs a clean empty state for when there's no data.

**All Jobs — no pool subscriptions:**
```
     🔍
  No opportunities found.
  Update your role preferences in Preferences
  to see matching jobs.
  [Go to Preferences →]
```

**Recommended — no profile:**
```
     ★
  Set up your profile to see recommendations.
  Upload your resume to get personalized job matches.
  [Complete Profile →]
```

---

## Loading States

- Initial feed load: show 4–6 skeleton card placeholders (gray animated shimmer blocks matching card dimensions)
- Drawer open: skeleton for description section while content loads
- Filter change: brief skeleton reload of card list

---

## What Is Explicitly Hidden in V1

Do NOT build these — omit entirely, no placeholder:
- Priority badges (APPLY NOW / HIGH UPSIDE / FAST APPLY / GOOD FIT) — hidden, no placeholder
- Visa Signal — hidden, no "coming soon" label
- Competition signal — hidden
- Alumni indicator — hidden
- Ask AI button — hidden
- Autofill button — hidden
- Application count — hidden
- Dark mode toggle — hidden

---

## API Contract (for wiring)

The frontend calls these backend endpoints. Mock with realistic data if backend is not yet connected.

```
GET  /dashboard/jobs                         All Jobs feed
     ?role=&location=&remote=&salary_min=
     &date_posted=&limit=50&cursor=

GET  /dashboard/jobs/recommended             Recommended feed
     ?limit=50&cursor=

GET  /dashboard/saved                        Saved jobs

GET  /dashboard/applied                      Applied jobs

POST /dashboard/jobs/{id}/save               Save a job
DELETE /dashboard/jobs/{id}/save             Unsave

POST /dashboard/jobs/{id}/apply              Mark as applied
```

Each job object returned includes:
```json
{
  "id": "uuid",
  "title": "Infrastructure Software Engineer",
  "company": "ScaleAI",
  "location": "San Francisco, CA; New York, NY",
  "salary_min": 180000,
  "salary_max": 225000,
  "employment_type": "FULLTIME",
  "remote_type": "hybrid",
  "application_effort": "MEDIUM",
  "posting_url": "https://...",
  "posted_at": "2026-06-06T...",
  "opportunity_score": 0.529,
  "personal_score": 0.5654,
  "match_reasons": ["Backend Engineering", "Distributed Systems", "AWS"],
  "recommendation_reason": "Strong backend alignment + high compensation.",
  "skills": ["Python", "Kafka", "AWS"],
  "description_html": "<p>...</p>",
  "is_saved": false,
  "is_applied": false
}
```
