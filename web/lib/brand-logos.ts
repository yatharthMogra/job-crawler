/** Known company name → domain for remote logo lookup */
const COMPANY_DOMAINS: Record<string, string> = {
  scaleai: "scale.com",
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
  walmart: "walmart.com",
  bloomberg: "bloomberg.com",
  google: "google.com",
  meta: "meta.com",
  amazon: "amazon.com",
  apple: "apple.com",
  microsoft: "microsoft.com",
  netflix: "netflix.com",
  uber: "uber.com",
  airbnb: "airbnb.com",
  openai: "openai.com",
}

/** Company name → local asset slug under /logos/companies/ */
const COMPANY_LOGO_SLUGS: Record<string, string> = {
  scaleai: "scaleai",
  ramp: "ramp",
  vercel: "vercel",
  stripe: "stripe",
  notion: "notion",
  linear: "linear",
  databricks: "databricks",
  anthropic: "anthropic",
  figma: "figma",
  retool: "retool",
  plaid: "plaid",
  brex: "brex",
  mercury: "mercury",
  airtable: "airtable",
  cohere: "cohere",
  snowflake: "snowflake",
  datadog: "datadog",
  coinbase: "coinbase",
  robinhood: "robinhood",
  instacart: "instacart",
  doordash: "doordash",
  rippling: "rippling",
  deel: "deel",
  census: "census",
  clearbit: "clearbit",
}

/** University / school name → domain */
const SCHOOL_DOMAINS: Record<string, string> = {
  nyu: "nyu.edu",
  "new york university": "nyu.edu",
  "iit mandi": "iitmandi.ac.in",
  "indian institute of technology mandi": "iitmandi.ac.in",
  mit: "mit.edu",
  stanford: "stanford.edu",
  "carnegie mellon": "cmu.edu",
  "columbia university": "columbia.edu",
  berkeley: "berkeley.edu",
  harvard: "harvard.edu",
}

const SCHOOL_LOGO_SLUGS: Record<string, string> = {
  nyu: "nyu",
  "new york university": "nyu",
  "iit mandi": "iit-mandi",
  "indian institute of technology mandi": "iit-mandi",
}

function normalizeKey(name: string) {
  return name.trim().toLowerCase().replace(/[^a-z0-9\s]/g, "")
}

function guessDomain(name: string): string {
  const slug = name.toLowerCase().replace(/[^a-z0-9]/g, "")
  return `${slug}.com`
}

function resolveMapEntry(name: string, map: Record<string, string>): string | null {
  const key = normalizeKey(name)
  if (map[key]) return map[key]

  for (const [alias, value] of Object.entries(map)) {
    if (key.includes(alias) || alias.includes(key)) return value
  }

  return null
}

export function resolveBrandDomain(name: string, variant: "company" | "school" = "company"): string {
  const map = variant === "school" ? SCHOOL_DOMAINS : COMPANY_DOMAINS
  return resolveMapEntry(name, map) ?? guessDomain(name)
}

function resolveLocalLogoPath(name: string, variant: "company" | "school"): string | null {
  const map = variant === "school" ? SCHOOL_LOGO_SLUGS : COMPANY_LOGO_SLUGS
  const slug = resolveMapEntry(name, map)
  if (!slug) return null
  const folder = variant === "school" ? "schools" : "companies"
  return `/logos/${folder}/${slug}.png`
}

export function getBrandLogoSources(name: string, variant: "company" | "school" = "company"): string[] {
  const domain = resolveBrandDomain(name, variant)
  const sources: string[] = []

  const local = resolveLocalLogoPath(name, variant)
  if (local) sources.push(local)

  sources.push(
    `https://www.google.com/s2/favicons?domain=${domain}&sz=128`,
    `https://unavatar.io/${encodeURIComponent(domain)}?fallback=false`,
    `https://icons.duckduckgo.com/ip3/${domain}.ico`,
  )

  return sources
}

export function getBrandInitial(name: string): string {
  const trimmed = name.trim()
  if (!trimmed) return "?"
  return trimmed.charAt(0).toUpperCase()
}
