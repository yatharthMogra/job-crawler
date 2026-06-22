# Cisco Careers Connector — Integration Guide

## Overview

Confirmed directly, and this is the simplest finding of the entire batch: **Cisco runs
on Workday.** Fetching `cisco.wd5.myworkdayjobs.com/Cisco_Careers` returned a clean,
standard Workday-hosted careers page — identical URL shape and structure to your
existing Workday tenants (Micron, NVIDIA, Northrop Grumman).

**This requires zero new connector code.** It's a new row in your existing Workday
tenant configuration, using the exact same `WorkdayConnector` class you already have in
production.

**Difficulty: Trivial.** This is configuration, not engineering.

---

## Confirmed Facts (From Direct Inspection)

- **URL:** `https://cisco.wd5.myworkdayjobs.com/Cisco_Careers` — confirmed live,
  returns standard Workday meta tags and page structure (`canonical`,
  `meta-og:title: Careers`, asset paths under `/Cisco_Careers/assets/`).
- **Workday instance:** `wd5` (the numbered subdomain indicating which Workday
  data-center cluster hosts this tenant — same pattern as your other Workday tenants).
- **Career site name:** `Cisco_Careers` (the path segment after the instance — this is
  the `career_site` value your existing Workday connector config expects).

---

## Configuration

Add directly to your Workday tenant list, following the exact pattern your existing
Workday companies (Micron, NVIDIA, Northrop Grumman, etc.) already use:

```json
{
  "company": "Cisco",
  "platform": "workday",
  "board_token": "cisco",
  "fetch_tier": 2,
  "is_active": true,
  "platform_config": {
    "instance": "wd5",
    "career_site": "Cisco_Careers"
  }
}
```

No connector code changes are needed. Your existing `WorkdayConnector`'s CXS API call
pattern (`POST` to the list endpoint, `GET` for detail, using `instance` +
`career_site` from `platform_config`) should work against this tenant exactly as it
does for your other Workday companies.

---

## What's Worth Double-Checking (Not Reconnaissance, Just Verification)

Since this is a known, already-solved connector pattern, the only real work is
confirming the standard things you'd check for any new Workday tenant onboarding:

1. **Run your existing Workday connector against this config in a test/staging pass**
   before marking `is_active: true` in production, same as you would for any new
   Workday company — confirm the CXS list and detail endpoints return data correctly
   for this specific tenant.
2. **Check Cisco's posting volume** — Cisco is a large company (314+ open positions per
   Glassdoor at time of this research) — set an appropriate `fetch_tier` given that
   volume relative to your existing Workday tenants.
3. **Confirm location/team filtering needs** — Cisco hires across networking,
   cybersecurity, software, hardware, and sales — same scoping question as your other
   large-company connectors (Tesla, Apple, Amazon) about whether you want all postings
   or only the software/ML/data-relevant subset. Check whether Workday's CXS API for
   this tenant exposes a job-family or category filter you can apply at fetch time,
   consistent with how you've handled this for other large multi-discipline employers.

---

## Field Mapping

Identical to your existing Workday field mapping — no changes needed. `instance: wd5`
and `career_site: Cisco_Careers` are the only tenant-specific values; everything
downstream (CXS list/detail call shape, field extraction in `deterministic.py`,
`_extract_workday`) is already built and tested against your other Workday tenants.

---

## Testing Checklist

- [ ] Confirmed `wd5` instance and `Cisco_Careers` career site resolve correctly
      through the existing Workday connector in a staging/test run
- [ ] Set an appropriate `fetch_tier` given Cisco's posting volume
- [ ] Decided whether to scope to software/ML/data roles only, consistent with your
      approach for other large multi-discipline companies
- [ ] Confirmed dedup fingerprinting correctly distinguishes Cisco postings from any
      other Workday tenant already in your catalog (should already work given your
      existing multi-tenant Workday dedup logic, but worth a sanity check on first run)

---

## Effort Estimate

Under an hour. This is the addition of one `companies.json` entry plus a verification
run against your existing, already-production Workday connector — no new code, no
reconnaissance, no API discovery required.
