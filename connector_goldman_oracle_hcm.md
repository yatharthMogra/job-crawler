# Goldman Sachs Careers Connector — Integration Guide

## Overview

Confirmed directly, and another zero-new-code finding: **Goldman Sachs's actual job
postings live on `higher.gs.com`** ("Higher" is Goldman's branded name for their careers
platform), and the "Apply" link on a real job detail page resolves to
**`hdpc.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/...`** — that's **Oracle HCM**,
a platform you already have a working connector for (10 companies currently, per your
platform list).

**Difficulty: Low.** This is a new tenant configuration for your existing Oracle HCM
connector, not a new build — same category outcome as Cisco (Workday) and
Netflix/Microsoft/Millennium (Eightfold).

---

## Confirmed Facts (From Direct Inspection)

- **Public-facing job detail URL:** `https://higher.gs.com/roles/{numeric-id}` — e.g.
  `higher.gs.com/roles/119977`, confirmed fully server-rendered with complete job
  content: "What We Do," "Who We Look For," "RESPONSIBILITIES," "Mandatory"
  qualifications, full EEO/disability statement text — all in plain HTML.
- **Underlying ATS confirmed via the Apply link:** the "Apply" button on that page
  points to `hdpc.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/
  LateralHiring/job/119977/apply/email` — this is Oracle Fusion Cloud HCM, the exact
  platform your `oracle_hcm` connector already targets.
- **Two separate Oracle HCM "sites" observed in this research:** the URL path includes
  `sites/LateralHiring` — suggesting Goldman may run separate Oracle HCM site
  configurations for different hiring tracks (lateral/experienced hires vs. campus
  recruiting, similar to the split seen at Millennium). Confirm whether a second site
  (e.g. `sites/Campus` or similar) exists and needs separate `platform_config` if you
  want campus/intern coverage in addition to experienced-hire roles.
- **`higher.gs.com` itself is likely a thin, branded wrapper/redirect layer** in front of
  the actual Oracle HCM candidate experience — similar in spirit to how Netflix's
  `explore.jobs.netflix.net` sits in front of the underlying Eightfold/ATS
  infrastructure. Confirm during reconnaissance whether `higher.gs.com/roles/{id}` is
  itself server-rendering content (it appears to be, based on this research) or whether
  it's proxying from the Oracle HCM detail endpoint.

---

## Recommended Approach: Extend Your Existing Oracle HCM Connector

Add Goldman Sachs as a new tenant to your existing `oracle_hcm` connector
configuration, following the same pattern as your other 10 Oracle HCM companies:

```json
{
  "company": "Goldman Sachs",
  "platform": "oracle_hcm",
  "board_token": "goldman-sachs",
  "fetch_tier": 2,
  "is_active": true,
  "platform_config": {
    "instance_host": "hdpc.fa.us2.oraclecloud.com",
    "site": "LateralHiring",
    "public_url_base": "https://higher.gs.com/roles"
  }
}
```

The `public_url_base` field is worth adding to your Oracle HCM connector's
`platform_config` schema generally (not just for Goldman) — since you now have direct
evidence that some Oracle HCM tenants present a branded public-facing URL
(`higher.gs.com`) that differs from the raw Oracle instance host, you want `job_url` in
your normalized records to point at the branded, human-readable URL rather than the raw
Oracle Cloud hostname, for link-quality reasons (a user clicking through from your
product should land on Goldman's own branded careers page, not a raw Oracle Cloud URL).

---

## Reconnaissance Still Needed

1. **Confirm whether `higher.gs.com/roles/{id}` is itself the correct fetch target, or
   whether your existing Oracle HCM connector should hit the
   `hdpc.fa.us2.oraclecloud.com` endpoints directly** and merely construct the
   `higher.gs.com` URL for display purposes. Test both — if `higher.gs.com` reliably
   serves full content for all current job IDs without hitting any Oracle-specific
   list/search API quirks your existing connector already handles, it may be simpler to
   fetch from there directly for Goldman specifically.
2. **Confirm the list/search mechanism.** Only a single detail page was directly
   confirmed in this research. Check whether `higher.gs.com` has its own search/listing
   page (analogous to `roles/{id}` but for browsing), or whether your existing Oracle
   HCM connector's standard list-fetch pattern (whatever it currently is for your other
   10 Oracle HCM tenants) applies unchanged here.
3. **Confirm whether a second Oracle HCM "site" exists for campus/intern hiring**,
   given the `sites/LateralHiring` path segment implies site-based segmentation.
4. **Confirm whether Goldman's specific Oracle HCM instance has any tenant-specific
   quirks** your existing connector doesn't already handle — this is standard new-tenant
   verification, the same check you'd run for any new Oracle HCM company.

---

## Field Mapping

Identical to your existing Oracle HCM field mapping — no new extraction logic needed.
The one addition is preserving the `higher.gs.com` branded URL as `job_url` (per the
`public_url_base` config above) rather than the raw Oracle Cloud URL, for link quality.

---

## Testing Checklist

- [ ] Confirmed whether to fetch from `higher.gs.com` directly or from the underlying
      Oracle HCM host, and documented the decision
- [ ] Confirmed list/search mechanism for enumerating all open Goldman roles
- [ ] Confirmed whether a second Oracle HCM site exists for campus/intern hiring
- [ ] Verified your existing `_extract_oracle_hcm` deterministic extraction logic
      handles Goldman's specific HTML/JSON shape without modification
- [ ] Ran existing Oracle HCM connector against this new tenant config in staging
      before marking `is_active: true`

---

## Effort Estimate

A few hours to half a day — primarily tenant configuration and verification against
your existing, already-production Oracle HCM connector, plus resolving the
`higher.gs.com` vs. raw-Oracle-host fetch-target question. No new connector class or
extraction logic is expected to be needed.
