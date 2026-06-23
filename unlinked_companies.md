# Unlinkable Companies

Companies from `internship_apply_links.csv` and `newgrad_apply_links.csv` that cannot be auto-ingested with current connectors and URL-derived board configuration.

A company appears here when **no** apply link in the CSV can be mapped to a supported job board with an extractable board token. In some cases the company uses a supported ATS (e.g. Greenhouse) but the apply URL is an embedded `gh_jid` link on a custom careers page, so the board slug cannot be derived automatically.

## Summary

| Metric | Count |
|--------|------:|
| **Total unique companies** | **42** |
| Internship CSV only | 18 |
| New-grad CSV only | 23 |
| Appear in both CSVs | 1 (Meta) |

Supported connectors today: Ashby, Greenhouse, Lever, Workday, Oracle HCM, ICIMS, SmartRecruiters, Workable, BambooHR, Rippling, SuccessFactors, Tesla Careers, Uber Careers, Google Careers, Amazon Jobs.

---

## Full list

| Company | Job board | Board / site | Reason not linkable | Source |
|---------|-----------|--------------|---------------------|--------|
| Akuna Capital University | Greenhouse | `akunacapital.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Altamira Technologies | Jobvite | `altamiracorps` | No connector for Jobvite | newgrad |
| Apple | Apple Careers | `jobs.apple.com` | No connector for Apple careers | internship |
| BAE Systems | BAE Systems Careers | `jobs.baesystems.com` | No connector for BAE Systems careers | newgrad |
| Brain Corp | Greenhouse | `braincorp.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| ByteDance | ByteDance Careers | `jobs.bytedance.com` | No connector for ByteDance / TikTok careers | internship |
| Cerebras | Greenhouse | `boards.greenhouse.io/embed` | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Cisco | Cisco Careers | `careers.cisco.com` | No connector for Cisco careers | internship |
| Citadel Securities | Citadel Securities Careers | `citadelsecurities.com` | No connector for Citadel Securities careers | newgrad |
| Consensus Cloud Solutions | Greenhouse | `consensus.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| D2L | Greenhouse | `d2l.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| DAT Freight & Analytics | Greenhouse | `careers.dat.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Hudson River Trading | Greenhouse | `hudsonrivertrading.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| IXL Learning | Greenhouse | `ixl.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Illinois Tool Works | Illinois Tool Works Careers | `careers.itw.com` | Custom corporate ATS — no connector and board config not extractable from URL | internship |
| Interact Software | Pinpoint HQ | `interactsoftware` | No connector for Pinpoint HQ | internship |
| Interstates | Greenhouse | `interstates.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| Intuit | Intuit Careers | `jobs.intuit.com` | No connector for Intuit careers | newgrad |
| Jamf | Greenhouse | `jamf.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Konrad Group | Greenhouse | `boards.greenhouse.io/embed` | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| MarketAxess | Greenhouse | `marketaxess.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| Meta | Meta Careers | `metacareers.com` | No connector for Meta careers | internship, newgrad |
| Microsoft | Microsoft Careers | `apply.careers.microsoft.com` | No connector for Microsoft careers | internship |
| Navaide | Breezy HR | `navaide` | No connector for Breezy HR | internship |
| Nuro | Greenhouse | `nuro.ai` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Nymbus | Greenhouse | `nymbus.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Oscar Health | Greenhouse | `hioscar.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Picarro | Greenhouse | `picarro.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| PsiQuantum | Greenhouse | `psiquantum.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| SeatGeek | Greenhouse | `seatgeek.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Skyscanner | Greenhouse | `skyscanner.net` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| Steel Point Solutions | Greenhouse | `steelpoint-llc.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Stripe | Greenhouse | `stripe.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| TIFIN | Greenhouse | `tifin.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| TikTok | TikTok Careers | `lifeattiktok.com` | No connector for ByteDance / TikTok careers | internship |
| Trane Technologies | Trane Technologies Careers | `careers.tranetechnologies.com` | Custom corporate ATS — no connector and board config not extractable from URL | internship |
| Trustpilot | Greenhouse | `trustpilot.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Unity | Greenhouse | `boards.greenhouse.io/embed` | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| Veracyte | Greenhouse | `veracyte.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |
| Visionist | Jobvite | `visionist` | No connector for Jobvite | newgrad |
| Waymo | Greenhouse | `withwaymo.com` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | newgrad |
| X Development | Greenhouse | `x.company` (gh_jid embed) | Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link | internship |

---

## By reason

### No connector for ByteDance / TikTok careers (2)

- **ByteDance** — ByteDance Careers, `jobs.bytedance.com` (internship)
- **TikTok** — TikTok Careers, `lifeattiktok.com` (internship)

### No connector for Apple careers (1)

- **Apple** — Apple Careers, `jobs.apple.com` (internship)

### No connector for Meta careers (1)

- **Meta** — Meta Careers, `metacareers.com` (internship, newgrad)

### No connector for Microsoft careers (1)

- **Microsoft** — Microsoft Careers, `apply.careers.microsoft.com` (internship)

### No connector for Cisco careers (1)

- **Cisco** — Cisco Careers, `careers.cisco.com` (internship)

### No connector for Pinpoint HQ (1)

- **Interact Software** — Pinpoint HQ, `interactsoftware` (internship)

### No connector for Breezy HR (1)

- **Navaide** — Breezy HR, `navaide` (internship)

### No connector for Jobvite (2)

- **Altamira Technologies** — Jobvite, `altamiracorps` (newgrad)
- **Visionist** — Jobvite, `visionist` (newgrad)

### No connector for Intuit careers (1)

- **Intuit** — Intuit Careers, `jobs.intuit.com` (newgrad)

### No connector for Citadel Securities careers (1)

- **Citadel Securities** — Citadel Securities Careers, `citadelsecurities.com` (newgrad)

### No connector for BAE Systems careers (1)

- **BAE Systems** — BAE Systems Careers, `jobs.baesystems.com` (newgrad)

### Custom corporate ATS — no connector and board config not extractable from URL (2)

- **Illinois Tool Works** — Illinois Tool Works Careers, `careers.itw.com` (internship)
- **Trane Technologies** — Trane Technologies Careers, `careers.tranetechnologies.com` (internship)

### Greenhouse job links use embedded `gh_jid` or embed URLs — board slug not present in apply link (27)

These companies host jobs on **Greenhouse**, but the CSV apply links point to a custom careers page or embed widget rather than `boards.greenhouse.io/{board_token}`. They could become linkable if the Greenhouse board token is added to `companies.json` manually.

| Company | Embedded careers host | Source |
|---------|----------------------|--------|
| Akuna Capital University | `akunacapital.com` | newgrad |
| Brain Corp | `braincorp.com` | newgrad |
| Cerebras | `boards.greenhouse.io/embed` | newgrad |
| Consensus Cloud Solutions | `consensus.com` | internship |
| D2L | `d2l.com` | newgrad |
| DAT Freight & Analytics | `careers.dat.com` | newgrad |
| Hudson River Trading | `hudsonrivertrading.com` | newgrad |
| IXL Learning | `ixl.com` | newgrad |
| Jamf | `jamf.com` | newgrad |
| Konrad Group | `boards.greenhouse.io/embed` | newgrad |
| MarketAxess | `marketaxess.com` | internship |
| Nuro | `nuro.ai` | newgrad |
| Nymbus | `nymbus.com` | newgrad |
| Oscar Health | `hioscar.com` | newgrad |
| Picarro | `picarro.com` | internship |
| PsiQuantum | `psiquantum.com` | internship |
| SeatGeek | `seatgeek.com` | newgrad |
| Skyscanner | `skyscanner.net` | internship |
| Steel Point Solutions | `steelpoint-llc.com` | newgrad |
| Stripe | `stripe.com` | newgrad |
| TIFIN | `tifin.com` | internship |
| Trustpilot | `trustpilot.com` | newgrad |
| Unity | `boards.greenhouse.io/embed` | newgrad |
| Veracyte | `veracyte.com` | internship |
| Waymo | `withwaymo.com` | newgrad |
| X Development | `x.company` | internship |
| Interstates | `interstates.com` | internship |

---

## Notes

- Several Greenhouse-embedded companies (e.g. Stripe, Jamf, Trustpilot, Oscar Health) may already exist in `companies.json` under a known board token — they remain on this list because the **CSV apply links themselves** are not parseable.
- Companies like **mthree** and **D3** are not listed: their CSVs include direct Greenhouse board URLs (`mthreerecruitingportal`, `d3`) that are already registered.
- **Cerebras** new-grad links use Greenhouse embed URLs; the registry entry is under board token `earlytalentcerebras` but the CSV links alone do not expose that token.
