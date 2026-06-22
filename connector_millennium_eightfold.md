# Millennium Management Careers Connector — Integration Guide

## Overview

Confirmed directly: **Millennium Management also runs on Eightfold AI** — the third
confirmed Eightfold tenant in your research alongside Netflix and Microsoft. Identified
by the exact same config fingerprint (`talent_form_mandatory_fields`,
`microsite=campus-site` URL parameter, matching i18n/privacy config structure).

**Use your `EightfoldConnector` class for Millennium too.** This is tenant
configuration, not new connector development — but Millennium has one structural
wrinkle worth designing for: **two separate microsites**, not one.

**Difficulty: Low**, same tier as Netflix and Microsoft.

---

## Confirmed Facts (From Direct Inspection)

- **Two distinct Eightfold-hosted microsites confirmed for Millennium:**
  - `career.mlp.com/careers` — labeled "Experienced Hires" in the site's own nav
  - `campusjobs.mlp.com/careers` — labeled "Campus" in the site's own nav, confirmed via
    URL parameter `?domain=mlp.com&microsite=campus-site`
  Both are explicitly cross-linked in each other's navigation bar, confirming they are
  two intentional, separate entry points to (likely) overlapping or complementary job
  pools on the same underlying Eightfold tenant for `mlp.com`.
- **Detail URL pattern confirmed**, consistent across both microsites:
  ```
  https://career.mlp.com/careers/job/{numeric-id}-{title-slug}
  https://campusjobs.mlp.com/careers/job/{numeric-id}-{title-slug}?domain=mlp.com&microsite=campus-site
  ```
  e.g. `career.mlp.com/careers/job/755943471581` (Software Engineer - Trade Capture),
  `campusjobs.mlp.com/careers/job/755944533188-software-engineer-intern-miami-...`
- **Numeric job IDs are large** (e.g. `755943471581`) but stable — confirmed consistent
  with Eightfold's general ID format (similar magnitude to Netflix's observed IDs).
- **Domain parameter confirmed:** `domain=mlp.com` — Millennium's corporate domain for
  Eightfold purposes is `mlp.com`, not `millennium.com`, despite the company's public
  brand name. This is an easy detail to get wrong if guessing rather than confirming.
- **Roles observed span both quant/trading-adjacent and general software engineering** —
  "Software Engineer - Trade Capture," "Software Engineer - Fixed Income Technology,"
  "Senior Software Engineer - EQ Derivatives Pricing & Risk," "AI Engineer," "Forward
  Deployed Software Engineer - Equities Technology" — strong signal that Millennium's
  engineering postings are highly relevant to your `SWE_FULLTIME` and
  `ML_ENGINEER_FULLTIME` pools, with a clear quant-finance specialization angle worth
  preserving as metadata (team/desk name) since it's a meaningful differentiator for
  candidates interested in finance-adjacent engineering roles specifically.

---

## Recommended Approach: Two Tenant Configs, One Connector Class

Configure Millennium as **two separate `companies.json` entries**, both using the same
`EightfoldConnector`, distinguished by `api_host`:

```json
[
  {
    "company": "Millennium Management",
    "platform": "eightfold",
    "board_token": "millennium-experienced",
    "fetch_tier": 2,
    "is_active": true,
    "platform_config": {
      "api_host": "career.mlp.com",
      "domain": "mlp.com"
    }
  },
  {
    "company": "Millennium Management (Campus)",
    "platform": "eightfold",
    "board_token": "millennium-campus",
    "fetch_tier": 2,
    "is_active": true,
    "platform_config": {
      "api_host": "campusjobs.mlp.com",
      "domain": "mlp.com",
      "extra_params": {
        "microsite": "campus-site"
      }
    }
  }
]
```

This reuses the `extra_params` generalization already added for Microsoft's
profession-filter need (see `connector_microsoft_eightfold.md`) — `microsite=campus-site`
slots into the same mechanism.

**Why two entries instead of one:** the campus and experienced-hire pools are presented
as genuinely separate site experiences by Millennium themselves (separate nav links,
separate subdomains). Treating them as two tenant configs keeps your `company_name`
normalization clean (you may want "Millennium Management" to read distinctly for
intern/campus roles vs. full-time experienced roles in your taxonomy) and makes it easy
to independently tune fetch cadence if campus postings churn on a different schedule
than experienced-hire postings (which is typical — campus roles often post seasonally in
bulk, as you've already seen documented for Tesla's and Amazon's new-grad programs).

---

## Reconnaissance Still Needed

1. **Confirm the actual API host for each microsite** — same question as Netflix:
   verify whether `career.mlp.com` and `campusjobs.mlp.com` proxy their own APIs, or
   whether both ultimately call a shared `mlp.eightfold.ai`-style backend host. Test
   directly via DevTools on both microsites independently — don't assume they share
   identical backend behavior just because they share a domain (`mlp.com`) and visual
   template.
2. **Confirm SmartApply vs. PCSX pattern for this tenant** — independently verified,
   not assumed, same discipline as every other Eightfold tenant.
3. **Check for overlap between the two microsites** — it's possible some roles are
   cross-posted to both `career.mlp.com` and `campusjobs.mlp.com`. If so, your dedup
   fingerprint logic (already built for cross-ATS dedup, e.g. the YC/Greenhouse case)
   should naturally catch this, but worth an explicit check on the first real run.

---

## Field Mapping

Identical to your Eightfold mapping established for Netflix — same platform, same
expected response shape. Worth adding for Millennium specifically: preserve any
team/desk name (e.g. "Trade Capture," "Fixed Income Technology," "EQ Derivatives
Pricing & Risk") in `raw_metadata`, since this is a much stronger and more specific
signal at a quant fund than at a tech company — it's effectively the difference between
"general software engineer" and "engineer embedded in a specific trading desk," which
matters more for finance-adjacent candidate matching than typical `department` fields
do elsewhere.

---

## Testing Checklist

- [ ] Confirmed actual API host(s) for both microsites independently
- [ ] Confirmed `domain=mlp.com` (not millennium.com) is correct in all API calls
- [ ] Confirmed whether the two microsites share a backend or are genuinely independent
- [ ] Checked for cross-posted role overlap between the two microsites and confirmed
      dedup logic handles it
- [ ] Preserved team/desk name in `raw_metadata` for both microsites

---

## Effort Estimate

Half a day, assuming the Eightfold connector is already built for Netflix. The main
incremental work is the two-microsite configuration and confirming whether they share
backend infrastructure — otherwise this is configuration, not new development.
