# Candidate Profile — Review UX Specification
## Designed for v0 (Vercel) Implementation

---

## 1. Overview

This document describes the user-facing interface for the Candidate Profile Intelligence System. It covers every screen a user sees when uploading a resume, reviewing proposed profile changes, and managing their canonical profile.

The core principle of the UX:

```
LLMs propose. Users approve. The system never mutates silently.
```

Users should always feel in control. Every change to their profile requires an explicit decision.

---

## 2. User Flow Map

```
Landing / Onboarding
        ↓
Resume Upload Screen
        ↓
Processing State (loading)
        ↓
Review Screen  ←──── (most important screen)
        ↓
Confirmation Screen
        ↓
Profile Home Screen
```

Users can also reach the Profile Home directly after initial setup and return to upload a new resume anytime.

---

## 3. Screen 1 — Resume Upload

### Purpose
Entry point for profile creation or update via resume.

### Layout
Clean centered card. Minimal chrome.

### Components

**Header:**
- Title: "Build your profile"
- Subtitle: "Upload your resume and we'll extract your experience, skills, and projects."

**Upload Zone:**
- Large drag-and-drop area
- Label: "Drag your resume here or click to browse"
- Accepted format note: "PDF only"
- File size note: "Max 5MB"
- On file select: show filename + file size + green checkmark

**Action Button:**
- "Analyze Resume" — disabled until file is selected
- Primary color, full width on mobile

**Note (below button):**
- "We'll show you exactly what we found before anything is saved to your profile."

### States
- Default: empty upload zone
- File selected: filename shown, button enabled
- Uploading: progress indicator on button ("Uploading...")
- Error: red border on upload zone + error message below ("Upload failed. Please try again.")

---

## 4. Screen 2 — Processing State

### Purpose
Shown while the backend extracts and analyzes resume content. Typically 5–15 seconds.

### Layout
Centered, minimal. Full-height loading screen.

### Components

**Animated icon** (subtle spinner or document scan animation)

**Status messages** (cycle through these during processing):
1. "Reading your resume..."
2. "Extracting your experience..."
3. "Identifying your skills..."
4. "Generating your profile..."

**Subtext:**
- "This usually takes 10–15 seconds."

### Behavior
- Auto-advances to Review Screen when processing completes
- If processing fails: show error card with "Something went wrong. Try again." + retry button

---

## 5. Screen 3 — Review Screen

### Purpose
The most important screen. Users review every proposed change before anything is saved.

### Layout
Two-column on desktop:
- Left column (narrower): Section navigation sidebar
- Right column (wider): Proposed changes for selected section

Single column on mobile (sidebar becomes a horizontal tab strip at top).

---

### Header (top of page)

**Title:** "Review your profile"
**Subtitle:** "We found the following information in your resume. Approve what looks right."

**Summary bar** (below header, above sections):
- "12 additions · 2 updates · 0 removals"
- "Approve All" button (right-aligned, secondary style)
- "Skip for now" link (far right, low emphasis)

---

### Left Sidebar — Section Navigation

Sections listed vertically. Each shows:
- Section name
- Badge with pending change count (e.g. "Skills  +4")
- Visual indicator: incomplete (grey dot) vs reviewed (green checkmark)

Sections in order:
1. Skills
2. Experiences
3. Projects
4. Certifications
5. Preferences & Constraints

Clicking a section scrolls right panel to that section.

---

### Right Panel — Proposed Changes

Each section renders its proposed changes as semantic diffs. Never raw JSON.

---

#### Section: Skills

Groups changes by skill category.

**Example render:**

```
Skills  ──────────────────────────────────  [Approve All] [Reject All]

Languages
  + Python          [✓ Approve]  [✗ Reject]
  + Java            [✓ Approve]  [✗ Reject]
  + TypeScript      [✓ Approve]  [✗ Reject]

Frameworks
  + FastAPI         [✓ Approve]  [✗ Reject]
  + React           [✓ Approve]  [✗ Reject]

Cloud
  + AWS             [✓ Approve]  [✗ Reject]

AI / ML
  + RAG             [✓ Approve]  [✗ Reject]
  + LLMs            [✓ Approve]  [✗ Reject]
```

**Change indicators:**
- `+` green — new addition
- `~` yellow — update to existing
- `-` red — removal (rare in V1)

---

#### Section: Experiences

Each experience shown as a card.

**New experience card:**
```
┌─────────────────────────────────────────────────┐
│  + New Experience                               │
│                                                 │
│  Software Developer 2                           │
│  Walmart · 24 months                           │
│  Retail Tech                                    │
│                                                 │
│  Keywords: Backend APIs, Distributed Systems,   │
│  Monitoring, Java, Kafka                        │
│                                                 │
│  [✓ Approve]  [✗ Reject]  [✏ Edit]            │
└─────────────────────────────────────────────────┘
```

**Updated experience card:**
```
┌─────────────────────────────────────────────────┐
│  ~ Updated Experience                           │
│                                                 │
│  Walmart                                        │
│  Duration: 22 months  →  24 months             │
│  + New keyword: Kafka                           │
│                                                 │
│  [✓ Approve]  [✗ Reject]  [✏ Edit]            │
└─────────────────────────────────────────────────┘
```

**Edit mode (inline):**
When user clicks Edit on an experience card:
- Card expands with editable fields
- Title, Company, Duration (months), Domains (tag input), Keywords (tag input)
- "Save Edit" and "Cancel" buttons
- Edited value shown with pencil icon after saving

---

#### Section: Projects

Same card pattern as Experiences.

```
┌─────────────────────────────────────────────────┐
│  + New Project                                  │
│                                                 │
│  SpecterRossAI                                  │
│  AI Product · Legal Tech                       │
│                                                 │
│  Keywords: Multi-Agent Systems, RAG, React,     │
│  Voice AI, Real-Time Systems                    │
│                                                 │
│  [✓ Approve]  [✗ Reject]  [✏ Edit]            │
└─────────────────────────────────────────────────┘
```

---

#### Section: Certifications

Simpler card — just name and issuer.

```
┌─────────────────────────────────────────────────┐
│  + New Certification                            │
│                                                 │
│  AWS Solutions Architect                        │
│  Issued by: AWS                                 │
│                                                 │
│  [✓ Approve]  [✗ Reject]  [✏ Edit]            │
└─────────────────────────────────────────────────┘
```

---

#### Section: Preferences & Constraints

This section is handled differently from evidence sections.

**Important UX note:** These are suggestions from the resume, not confirmed facts. The UI makes this explicit.

Header for this section:
> "We made some guesses based on your resume. These are yours to define — please review carefully."

Fields shown as suggestion rows:

```
Sponsorship Required
  Suggested: Yes (detected F1 visa indicators)
  [✓ Confirm]  [✗ Decline]  [✏ Change]

Primary Roles
  Suggested: Software Engineer Intern, AI Engineer Intern
  [✓ Confirm]  [✗ Decline]  [✏ Change]

Preferred Locations
  Suggested: NYC, Remote
  [✓ Confirm]  [✗ Decline]  [✏ Change]

Minimum Hourly Rate
  Not detected — leave blank or set now:
  [$ ______]  [Set]
```

---

### Sticky Footer (Review Screen)

Always visible at bottom of page:

```
[  Skip for now  ]          [ Save Approved Changes → ]
```

- "Save Approved Changes" is enabled only when at least one item is approved
- Shows count of approved items: "Save 8 approved changes →"
- "Skip for now" exits without saving — with a confirmation modal: "No changes will be saved. Continue?"

---

## 6. Screen 4 — Confirmation Screen

### Purpose
Confirms what was saved. Gives user a clear summary of their approved changes.

### Layout
Centered card. Clean success state.

### Components

**Icon:** Green checkmark

**Title:** "Profile updated"

**Summary of committed changes:**
```
Added to your profile:

Skills (6)
  Python, Java, TypeScript, FastAPI, React, AWS

Experiences (1)
  Software Developer 2 at Walmart

Projects (2)
  SpecterRossAI, DocuFlow

Capabilities generated:
  Backend Engineering · AI Systems · Distributed Systems
```

**Note:**
- "Your capabilities have been automatically updated based on your approved evidence."

**Action button:**
- "View my profile →"

---

## 7. Screen 5 — Profile Home

### Purpose
User's view of their current canonical approved profile. Read-mostly, with clear edit pathways.

### Layout
Single-column, structured sections. Not a dense dashboard — clean and readable.

### Header

**User name (large)**
**Education line:** "MS Computer Science · NYU · Graduating May 2027"

**Action buttons (top right):**
- "Upload new resume" (primary)
- "Edit preferences" (secondary)

---

### Capabilities Section (top of profile)

Shown prominently since this is what the recommendation engine uses.

```
Your Capabilities  ──────────────────────────────

  Backend Engineering      ████████████  Supported by: Walmart, APIs
  AI Systems               ████████████  Supported by: SpecterRossAI, RAG
  Distributed Systems      ████████         Supported by: Walmart, Kafka
  Full Stack Development   ██████           Supported by: SpecterRossAI
```

Visual bar is proportional to evidence depth (number of supporting evidence items), not a numeric score.

Hovering/tapping a capability shows the evidence list in a tooltip.

---

### Constraints Section

Read-only summary. Edit button opens a simple form.

```
Constraints  ─────────────────────────  [Edit]

  Sponsorship Required    Yes
  Visa Type               F1
  Work Authorization      CPT / OPT
  Role Type               Both internship and full-time
  Minimum Hourly Rate     $25/hr
```

---

### Preferences Section

Read-only summary. Edit button opens a form.

```
Preferences  ─────────────────────────  [Edit]

  Primary Roles           Software Engineer Intern · AI Engineer Intern
  Preferred Locations     NYC · Remote
  Remote Preference       Hybrid
  Industries              AI · FinTech · Developer Tools
```

---

### Experience Section

List of approved experience cards. Read-only.

Each card shows: title, company, duration, domains, top keywords.

---

### Projects Section

List of approved project cards. Read-only.

---

### Skills Section

Grouped by category. Read-only tags.

---

### Profile Version Footer

Bottom of page, low emphasis:

```
Profile version 4 · Last updated 2 hours ago · Built from 3 resumes
```

---

## 8. Key UX Principles

- **Never show raw JSON or field names.** `evidence_keywords` displays as "Keywords". `duration_months` displays as "24 months".
- **Semantic diffs only.** Users see what changed, not how it changed internally.
- **Every mutation requires a decision.** No auto-approve. No silent saves.
- **Reject is always safe.** Rejecting a change has no side effects. Users can always re-upload.
- **Edit is always available.** If the LLM got something slightly wrong, users can fix it inline before approving.
- **Capabilities are shown as outcomes, not scores.** No percentages or numeric confidence values. Evidence links tell the story.
- **Preferences section is clearly flagged as suggestions.** These are not facts — the UI language reflects that.
