/**
 * Precise brand logo resolution for companies and universities.
 * Priority: explicit domain → known alias map → cleaned name guess → multi-CDN fallbacks.
 */

const LEGAL_SUFFIXES =
  /\b(inc|incorporated|llc|l\.l\.c|ltd|limited|corp|corporation|co|company|plc|gmbh|ag|sa|nv|bv|technologies|technology|tech|software|systems|group|holdings|holding|partners|ventures|labs|lab|ai|pbc|pc)\b\.?/gi

const SCHOOL_NOISE =
  /\b(the|university|of|at|college|institute|school|for|and|&)\b/gi

/** Known company name / alias → domain */
const COMPANY_DOMAINS: Record<string, string> = {
  // Mock / common startups
  scaleai: "scale.com",
  "scale ai": "scale.com",
  scale: "scale.com",
  ramp: "ramp.com",
  vercel: "vercel.com",
  stripe: "stripe.com",
  notion: "notion.so",
  linear: "linear.app",
  databricks: "databricks.com",
  anthropic: "anthropic.com",
  figma: "figma.com",
  retool: "retool.com",
  plaid: "plaid.com",
  brex: "brex.com",
  mercury: "mercury.com",
  airtable: "airtable.com",
  cohere: "cohere.com",
  snowflake: "snowflake.com",
  datadog: "datadoghq.com",
  coinbase: "coinbase.com",
  robinhood: "robinhood.com",
  instacart: "instacart.com",
  doordash: "doordash.com",
  rippling: "rippling.com",
  deel: "deel.com",
  census: "getcensus.com",
  clearbit: "clearbit.com",
  // Big tech
  google: "google.com",
  alphabet: "abc.xyz",
  meta: "meta.com",
  facebook: "meta.com",
  amazon: "amazon.com",
  aws: "aws.amazon.com",
  apple: "apple.com",
  microsoft: "microsoft.com",
  netflix: "netflix.com",
  uber: "uber.com",
  airbnb: "airbnb.com",
  openai: "openai.com",
  nvidia: "nvidia.com",
  intel: "intel.com",
  amd: "amd.com",
  oracle: "oracle.com",
  salesforce: "salesforce.com",
  adobe: "adobe.com",
  ibm: "ibm.com",
  cisco: "cisco.com",
  // Finance / enterprise
  walmart: "walmart.com",
  bloomberg: "bloomberg.com",
  goldman: "goldmansachs.com",
  "goldman sachs": "goldmansachs.com",
  jpmorgan: "jpmorganchase.com",
  "jp morgan": "jpmorganchase.com",
  "jpmorgan chase": "jpmorganchase.com",
  "morgan stanley": "morganstanley.com",
  citadel: "citadel.com",
  "jane street": "janestreet.com",
  two: "twosigma.com",
  "two sigma": "twosigma.com",
  blackrock: "blackrock.com",
  "black rock": "blackrock.com",
  capital: "capitalone.com",
  "capital one": "capitalone.com",
  // Other common employers
  linkedin: "linkedin.com",
  twitter: "x.com",
  x: "x.com",
  snap: "snap.com",
  snapchat: "snap.com",
  tiktok: "tiktok.com",
  bytedance: "bytedance.com",
  shopify: "shopify.com",
  square: "squareup.com",
  block: "block.xyz",
  paypal: "paypal.com",
  tesla: "tesla.com",
  spacex: "spacex.com",
  anduril: "anduril.com",
  palantir: "palantir.com",
  snow: "snowflake.com",
  cloudflare: "cloudflare.com",
  mongodb: "mongodb.com",
  elastic: "elastic.co",
  atlassian: "atlassian.com",
  asana: "asana.com",
  slack: "slack.com",
  zoom: "zoom.us",
  dropbox: "dropbox.com",
  box: "box.com",
  twitch: "twitch.tv",
  discord: "discord.com",
  reddit: "reddit.com",
  pinterest: "pinterest.com",
  spotify: "spotify.com",
  lyft: "lyft.com",
  "wayfair": "wayfair.com",
  target: "target.com",
  nike: "nike.com",
  disney: "disney.com",
  "warner bros": "wbd.com",
  comcast: "comcast.com",
  verizon: "verizon.com",
  att: "att.com",
  "at&t": "att.com",
  tmobile: "t-mobile.com",
  "t mobile": "t-mobile.com",
  lockheed: "lockheedmartin.com",
  "lockheed martin": "lockheedmartin.com",
  "northrop grumman": "northropgrumman.com",
  raytheon: "rtx.com",
  boeing: "boeing.com",
  "general electric": "ge.com",
  ge: "ge.com",
  "general motors": "gm.com",
  gm: "gm.com",
  ford: "ford.com",
  "johnson johnson": "jnj.com",
  pfizer: "pfizer.com",
  moderna: "modernatx.com",
  "cvs health": "cvshealth.com",
  unitedhealth: "unitedhealthgroup.com",
  accenture: "accenture.com",
  deloitte: "deloitte.com",
  "ernst young": "ey.com",
  ey: "ey.com",
  kpmg: "kpmg.com",
  pwc: "pwc.com",
  mckinsey: "mckinsey.com",
  bcg: "bcg.com",
  "boston consulting": "bcg.com",
  bain: "bain.com",
}

/** University / school name → domain */
const SCHOOL_DOMAINS: Record<string, string> = {
  // Mock profile schools
  nyu: "nyu.edu",
  "new york university": "nyu.edu",
  "iit mandi": "iitmandi.ac.in",
  "indian institute of technology mandi": "iitmandi.ac.in",
  // Top US
  mit: "mit.edu",
  "massachusetts institute of technology": "mit.edu",
  stanford: "stanford.edu",
  "stanford university": "stanford.edu",
  harvard: "harvard.edu",
  "harvard university": "harvard.edu",
  "carnegie mellon": "cmu.edu",
  "carnegie mellon university": "cmu.edu",
  cmu: "cmu.edu",
  berkeley: "berkeley.edu",
  "uc berkeley": "berkeley.edu",
  "university of california berkeley": "berkeley.edu",
  "columbia university": "columbia.edu",
  columbia: "columbia.edu",
  princeton: "princeton.edu",
  yale: "yale.edu",
  upenn: "upenn.edu",
  "university of pennsylvania": "upenn.edu",
  penn: "upenn.edu",
  cornell: "cornell.edu",
  "cornell university": "cornell.edu",
  caltech: "caltech.edu",
  "california institute of technology": "caltech.edu",
  "university of chicago": "uchicago.edu",
  uchicago: "uchicago.edu",
  "northwestern university": "northwestern.edu",
  northwestern: "northwestern.edu",
  duke: "duke.edu",
  "duke university": "duke.edu",
  "johns hopkins": "jhu.edu",
  "johns hopkins university": "jhu.edu",
  "brown university": "brown.edu",
  brown: "brown.edu",
  dartmouth: "dartmouth.edu",
  "dartmouth college": "dartmouth.edu",
  "university of michigan": "umich.edu",
  umich: "umich.edu",
  "georgia tech": "gatech.edu",
  "georgia institute of technology": "gatech.edu",
  gatech: "gatech.edu",
  "university of texas": "utexas.edu",
  "ut austin": "utexas.edu",
  "university of texas at austin": "utexas.edu",
  "university of washington": "uw.edu",
  uw: "uw.edu",
  "university of illinois": "illinois.edu",
  uiuc: "illinois.edu",
  "university of illinois urbana champaign": "illinois.edu",
  "ucla": "ucla.edu",
  "university of california los angeles": "ucla.edu",
  "uc san diego": "ucsd.edu",
  ucsd: "ucsd.edu",
  "university of california san diego": "ucsd.edu",
  "university of southern california": "usc.edu",
  usc: "usc.edu",
  "new york university tandon": "nyu.edu",
  "nyu tandon": "nyu.edu",
  "boston university": "bu.edu",
  bu: "bu.edu",
  "northeastern university": "northeastern.edu",
  northeastern: "northeastern.edu",
  "purdue university": "purdue.edu",
  purdue: "purdue.edu",
  "texas a m": "tamu.edu",
  "texas am": "tamu.edu",
  tamu: "tamu.edu",
  "ohio state": "osu.edu",
  "ohio state university": "osu.edu",
  "penn state": "psu.edu",
  "pennsylvania state university": "psu.edu",
  "university of wisconsin": "wisc.edu",
  "university of maryland": "umd.edu",
  umd: "umd.edu",
  "university of florida": "ufl.edu",
  "arizona state": "asu.edu",
  "arizona state university": "asu.edu",
  // International
  "university of toronto": "utoronto.ca",
  "university of waterloo": "uwaterloo.ca",
  waterloo: "uwaterloo.ca",
  "university of british columbia": "ubc.ca",
  ubc: "ubc.ca",
  "oxford": "ox.ac.uk",
  "university of oxford": "ox.ac.uk",
  cambridge: "cam.ac.uk",
  "university of cambridge": "cam.ac.uk",
  eth: "ethz.ch",
  "eth zurich": "ethz.ch",
  "iit bombay": "iitb.ac.in",
  "iit delhi": "iitd.ac.in",
  "iit madras": "iitm.ac.in",
  "iit kanpur": "iitk.ac.in",
  "iit kharagpur": "iitkgp.ac.in",
  "iit roorkee": "iitr.ac.in",
  "iit hyderabad": "iith.ac.in",
  "iit guwahati": "iitg.ac.in",
  "national university of singapore": "nus.edu.sg",
  nus: "nus.edu.sg",
  "nanyang technological university": "ntu.edu.sg",
  ntu: "ntu.edu.sg",
  "tsinghua university": "tsinghua.edu.cn",
  tsinghua: "tsinghua.edu.cn",
  "peking university": "pku.edu.cn",
}

function normalizeKey(name: string): string {
  return name
    .trim()
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
}

function stripLegalSuffixes(name: string): string {
  return normalizeKey(name)
    .replace(LEGAL_SUFFIXES, " ")
    .replace(/\s+/g, " ")
    .trim()
}

function schoolSearchKey(name: string): string {
  return normalizeKey(name)
    .replace(SCHOOL_NOISE, " ")
    .replace(/\s+/g, " ")
    .trim()
}

function resolveMapEntry(name: string, map: Record<string, string>, variant: "company" | "school"): string | null {
  const key = normalizeKey(name)
  if (!key) return null
  if (map[key]) return map[key]

  const stripped = variant === "company" ? stripLegalSuffixes(name) : schoolSearchKey(name)
  if (stripped && map[stripped]) return map[stripped]

  // Prefer longer aliases to avoid short false positives (e.g. "ge", "x")
  const aliases = Object.keys(map).sort((a, b) => b.length - a.length)
  for (const alias of aliases) {
    if (alias.length < 3) {
      // Short aliases: exact token match only
      const tokens = stripped.split(" ")
      if (tokens.includes(alias) || key === alias) return map[alias]
      continue
    }
    if (key === alias || stripped === alias) return map[alias]
    if (key.startsWith(`${alias} `) || key.endsWith(` ${alias}`) || key.includes(` ${alias} `)) {
      return map[alias]
    }
    if (stripped.startsWith(`${alias} `) || stripped.endsWith(` ${alias}`) || stripped.includes(` ${alias} `)) {
      return map[alias]
    }
    // Multi-word alias fully contained
    if (alias.includes(" ") && (key.includes(alias) || stripped.includes(alias))) {
      return map[alias]
    }
  }

  return null
}

function guessCompanyDomain(name: string): string {
  const cleaned = stripLegalSuffixes(name).replace(/\s+/g, "")
  if (!cleaned) return "example.com"
  return `${cleaned}.com`
}

function guessSchoolDomain(name: string): string {
  const key = schoolSearchKey(name)
  if (!key) return "edu"
  // Common pattern: acronyms
  const words = key.split(" ").filter(Boolean)
  if (words.length >= 2 && words.every((w) => w.length <= 4)) {
    return `${words.join("")}.edu`
  }
  const slug = words.join("").slice(0, 24)
  return `${slug}.edu`
}

/** Extract hostname from a website URL if present. */
export function domainFromWebsite(website: string | null | undefined): string | null {
  if (!website?.trim()) return null
  try {
    const url = website.includes("://") ? website : `https://${website}`
    const host = new URL(url).hostname.replace(/^www\./, "")
    return host || null
  } catch {
    return null
  }
}

export function resolveBrandDomain(
  name: string,
  variant: "company" | "school" = "company",
  explicitDomain?: string | null,
): string {
  if (explicitDomain?.trim()) {
    return explicitDomain.replace(/^www\./, "").trim()
  }
  const map = variant === "school" ? SCHOOL_DOMAINS : COMPANY_DOMAINS
  const mapped = resolveMapEntry(name, map, variant)
  if (mapped) return mapped
  return variant === "school" ? guessSchoolDomain(name) : guessCompanyDomain(name)
}

export function getBrandLogoSources(
  name: string,
  variant: "company" | "school" = "company",
  explicitDomain?: string | null,
): string[] {
  const domain = resolveBrandDomain(name, variant, explicitDomain)
  const encoded = encodeURIComponent(domain)

  // Google favicons first (most reliable); Clearbit is deprecated.
  return [
    `https://www.google.com/s2/favicons?domain=${encoded}&sz=128`,
    `https://icons.duckduckgo.com/ip3/${domain}.ico`,
    `https://unavatar.io/${encoded}`,
    `https://logo.clearbit.com/${domain}`,
  ]
}

export function getBrandInitial(name: string): string {
  const trimmed = name.trim()
  if (!trimmed) return "?"
  const words = trimmed.split(/\s+/).filter(Boolean)
  if (words.length >= 2) {
    return (words[0][0] + words[1][0]).toUpperCase()
  }
  return trimmed.charAt(0).toUpperCase()
}
