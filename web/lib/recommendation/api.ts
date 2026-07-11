const BASE_URL = process.env.NEXT_PUBLIC_RECOMMENDATION_API_URL ?? "http://localhost:8002"

function useMockNotifications(): boolean {
  if (process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true") return true
  if (process.env.NEXT_PUBLIC_USE_MOCK_DATA === "false") return false
  // Local dev: use in-memory notification mocks so Settings UI works without :8002
  return process.env.NODE_ENV === "development"
}

export type SponsorshipStatus = "yes" | "no" | "unclear"

export interface PreferenceIndicatorApi {
  label: string
  kind: "strength" | "gap"
}

export interface H1BSponsorshipInfo {
  pool_family: string
  total_lca_3yr: number
  approval_rate_3yr: number | null
  is_top_sponsor: boolean
  years_covered: number[]
}

export interface CompanyEnrichmentInfo {
  founded_year: number | null
  headquarters: string | null
  employee_count_range: string | null
  one_line_description: string | null
  website: string | null
  linkedin_url: string | null
  glassdoor_rating: number | null
  logo_url: string | null
}

export interface DashboardJobApi {
  id: string
  title: string
  company_name: string
  location: string | null
  posting_url: string | null
  description_text: string | null
  description_preview: string | null
  posted_at: string | null
  remote_type: string
  application_effort: string | null
  salary_min: number | null
  salary_max: number | null
  opportunity_score: number | null
  retrieval_pools: string[]
  normalized_roles: string[]
  job_capabilities: string[]
  tech_stack: string[]
  skills: string[]
  seniority: string
  responsibilities: string[]
  required_qualifications: string[]
  preferred_qualifications: string[]
  benefits: string[]
  sponsorship_status: SponsorshipStatus
  sponsorship_confidence: string
  requires_clearance: boolean
  requires_citizenship: boolean
  h1b_sponsorship: H1BSponsorshipInfo | null
  company_info: CompanyEnrichmentInfo | null
}

export interface RecommendedJobApi extends DashboardJobApi {
  personal_score: number
  qualification_fit: number | null
  match_reasons: string[]
  preference_indicators: PreferenceIndicatorApi[]
}

export interface DashboardJobsResponse {
  jobs: DashboardJobApi[]
  total: number
}

export interface RecommendedJobsResponse {
  jobs: RecommendedJobApi[]
  total: number
  reference_token?: string | null
  offset?: number
  has_more?: boolean
  returned?: number
  total_ranked?: number
  // Deprecated legacy fields
  next_cursor?: string | null
  scanned?: number
}

export interface SubscriptionOut {
  id: string
  candidate_id: string
  pool_name: string
  is_active: boolean
  created_at: string
}

export interface SubscriptionListResponse {
  candidate_id: string
  subscriptions: SubscriptionOut[]
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers)
  if (init?.body && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json")
  }
  const response = await fetch(`${BASE_URL}${path}`, { ...init, headers })
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try {
      const body = await response.json()
      if (typeof body.detail === "string") message = body.detail
    } catch {
      // ignore
    }
    throw new Error(message)
  }
  return response.json() as Promise<T>
}

export function fetchDashboardJobs(
  candidateId: string,
  params: Record<string, string | number | undefined> = {},
) {
  const query = new URLSearchParams({ candidate_id: candidateId })
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, String(value))
    }
  }
  return request<DashboardJobsResponse>(`/dashboard/jobs?${query}`)
}

export function fetchRecommendedJobs(
  candidateId: string,
  params: {
    referenceToken?: string
    offset?: number
    limit?: number
    /** @deprecated legacy offset cursor */
    cursor?: string
    scanBatch?: number
  } = {},
) {
  const query = new URLSearchParams({ candidate_id: candidateId })
  if (params.referenceToken) query.set("reference_token", params.referenceToken)
  if (params.offset != null) query.set("offset", String(params.offset))
  if (params.limit != null) query.set("limit", String(params.limit))
  if (params.scanBatch != null) query.set("scan_batch", String(params.scanBatch))
  if (params.cursor) query.set("cursor", params.cursor)
  return request<RecommendedJobsResponse>(`/dashboard/jobs/recommended?${query}`)
}

export function fetchDashboardJob(candidateId: string, jobId: string) {
  return request<DashboardJobApi>(
    `/dashboard/jobs/${jobId}?candidate_id=${encodeURIComponent(candidateId)}`,
  )
}

export interface AtsFitSignalsApi {
  bm25?: number | null
  semantic?: number | null
  structural?: number | null
  title?: number | null
  experience?: number | null
  education?: number | null
}

export interface AtsFitApi {
  ats_fit_score: number | null
  pool_percentile: number | null
  pool_percentile_label: string | null
  signals: AtsFitSignalsApi
  unavailable_reason: string | null
}

export function fetchJobAtsFit(candidateId: string, jobId: string) {
  return request<AtsFitApi>(
    `/dashboard/jobs/${encodeURIComponent(jobId)}/ats-fit?candidate_id=${encodeURIComponent(candidateId)}`,
  )
}

export function fetchSubscriptions(candidateId: string) {
  return request<SubscriptionListResponse>(`/subscriptions/${candidateId}`)
}

export function patchSubscriptions(
  candidateId: string,
  poolNames: string[],
  isActive = true,
) {
  return request<SubscriptionOut[]>(`/subscriptions/${candidateId}`, {
    method: "PATCH",
    body: JSON.stringify({ pool_names: poolNames, is_active: isActive }),
  })
}

export function createSubscriptions(candidateId: string, poolNames: string[]) {
  return request<SubscriptionOut[]>("/subscriptions", {
    method: "POST",
    body: JSON.stringify({ candidate_id: candidateId, pool_names: poolNames }),
  })
}

export interface TierEntitlementsApi {
  max_companies: number
  cadence_min_minutes: number
  cadence_max_minutes: number
  delivery: "batched" | "instant"
  max_emails_per_day_cap: number
  default_max_emails_per_day: number
}

export interface NotificationPreferencesApi {
  candidate_id: string
  digest_enabled: boolean
  company_watch_enabled: boolean
  cadence_hours: number
  top_k: number
  digest_filters: Record<string, unknown> | null
  last_digest_sent_at: string | null
  next_digest_due_at: string | null
  company_watch_cadence_minutes: number
  max_emails_per_day: number
  last_company_watch_batch_at: string | null
  next_company_watch_due_at: string | null
  plan_tier: "free" | "plus"
  entitlements: TierEntitlementsApi
  emails_sent_today: number
}

export interface CompanyWatchItemApi {
  company_id: string
  company_name: string
  platform: string
  is_active: boolean
}

export interface CompanyWatchListApi {
  candidate_id: string
  companies: CompanyWatchItemApi[]
  plan_tier: "free" | "plus"
  max_companies: number
}

export interface CompanySearchResult {
  id: string
  name: string
  platform: string
  is_active: boolean
}

export type DigestCadenceHours = 3 | 6 | 12 | 24 | 72 | 168

export const DIGEST_CADENCE_OPTIONS: { label: string; hours: DigestCadenceHours }[] = [
  { label: "Every 3 hours", hours: 3 },
  { label: "Every 6 hours", hours: 6 },
  { label: "Every 12 hours", hours: 12 },
  { label: "Daily (24 hours)", hours: 24 },
  { label: "Every 3 days", hours: 72 },
  { label: "Weekly (7 days)", hours: 168 },
]

export const FREE_COMPANY_WATCH_CADENCE_OPTIONS = [
  { label: "Every 6 hours", minutes: 360 },
  { label: "Every 8 hours", minutes: 480 },
  { label: "Every 10 hours", minutes: 600 },
  { label: "Every 12 hours", minutes: 720 },
] as const

export const PLUS_COMPANY_WATCH_CADENCE_OPTIONS = [
  { label: "Every 30 minutes", minutes: 30 },
  { label: "Every 1 hour", minutes: 60 },
  { label: "Every 2 hours", minutes: 120 },
  { label: "Every 3 hours", minutes: 180 },
] as const

export function companyWatchCadenceOptions(planTier: "free" | "plus") {
  return planTier === "plus" ? PLUS_COMPANY_WATCH_CADENCE_OPTIONS : FREE_COMPANY_WATCH_CADENCE_OPTIONS
}

const FALLBACK_ENTITLEMENTS: Record<"free" | "plus", TierEntitlementsApi> = {
  free: {
    max_companies: 5,
    cadence_min_minutes: 360,
    cadence_max_minutes: 720,
    delivery: "batched",
    max_emails_per_day_cap: 10,
    default_max_emails_per_day: 3,
  },
  plus: {
    max_companies: 25,
    cadence_min_minutes: 30,
    cadence_max_minutes: 180,
    delivery: "instant",
    max_emails_per_day_cap: 20,
    default_max_emails_per_day: 10,
  },
}

/**
 * Older/deployed API builds may omit tier fields. Backfill safe defaults so the
 * Emails UI never crashes on `prefs.entitlements.*`.
 */
function normalizeNotificationPreferences(
  prefs: NotificationPreferencesApi,
): NotificationPreferencesApi {
  const planTier: "free" | "plus" = prefs.plan_tier === "plus" ? "plus" : "free"
  const entitlements = prefs.entitlements ?? FALLBACK_ENTITLEMENTS[planTier]
  return {
    ...prefs,
    plan_tier: planTier,
    entitlements,
    max_emails_per_day: prefs.max_emails_per_day ?? entitlements.default_max_emails_per_day,
    company_watch_cadence_minutes:
      prefs.company_watch_cadence_minutes ?? entitlements.cadence_min_minutes,
    emails_sent_today: prefs.emails_sent_today ?? 0,
  }
}

export function fetchNotificationPreferences(candidateId: string) {
  if (useMockNotifications()) {
    return import("@/lib/recommendation/mock-notifications").then((m) =>
      m.mockFetchNotificationPreferences(candidateId),
    )
  }
  return request<NotificationPreferencesApi>(`/notification-preferences/${candidateId}`).then(
    normalizeNotificationPreferences,
  )
}

export function updateNotificationPreferences(
  candidateId: string,
  payload: Partial<{
    digest_enabled: boolean
    company_watch_enabled: boolean
    cadence_hours: number
    top_k: number
    company_watch_cadence_minutes: number
    max_emails_per_day: number
  }>,
) {
  if (useMockNotifications()) {
    return import("@/lib/recommendation/mock-notifications").then((m) =>
      m.mockUpdateNotificationPreferences(candidateId, payload),
    )
  }
  return request<NotificationPreferencesApi>(`/notification-preferences/${candidateId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  }).then(normalizeNotificationPreferences)
}

export function fetchCompanyWatch(candidateId: string) {
  if (useMockNotifications()) {
    return import("@/lib/recommendation/mock-notifications").then((m) =>
      m.mockFetchCompanyWatch(candidateId),
    )
  }
  return request<CompanyWatchListApi>(`/company-watch/${candidateId}`)
}

export function updateCompanyWatch(candidateId: string, companyIds: string[]) {
  if (useMockNotifications()) {
    return import("@/lib/recommendation/mock-notifications").then((m) =>
      m.mockUpdateCompanyWatch(candidateId, companyIds),
    )
  }
  return request<CompanyWatchListApi>(`/company-watch/${candidateId}`, {
    method: "PUT",
    body: JSON.stringify({ company_ids: companyIds }),
  })
}

export function searchCompanies(q = "", limit = 20) {
  if (useMockNotifications()) {
    return import("@/lib/recommendation/mock-notifications").then((m) =>
      m.mockSearchCompanies(q, limit),
    )
  }
  const query = new URLSearchParams({ limit: String(limit) })
  if (q.trim()) query.set("q", q.trim())
  return request<CompanySearchResult[]>(`/companies/search?${query}`)
}

export interface UserApplicationApi {
  id: string
  candidate_id: string
  job_archive_id: string | null
  normalized_job_id: string | null
  company_name: string
  job_title: string
  location: string | null
  platform: string | null
  external_job_id: string | null
  posting_url: string | null
  salary_min: number | null
  salary_max: number | null
  seniority: string | null
  skills: string[]
  tech_stack: string[]
  description_text: string | null
  logo_url: string | null
  applied_at: string
  status: string
  notes: string | null
}

export interface UserApplicationsResponse {
  applications: UserApplicationApi[]
  total: number
}

export function fetchApplications(candidateId: string) {
  return request<UserApplicationsResponse>(
    `/dashboard/applications?candidate_id=${encodeURIComponent(candidateId)}`,
  )
}

export function applyToJob(candidateId: string, jobId: string) {
  return request<UserApplicationApi>(
    `/dashboard/jobs/${encodeURIComponent(jobId)}/apply?candidate_id=${encodeURIComponent(candidateId)}`,
    { method: "POST" },
  )
}

export function patchApplication(
  candidateId: string,
  applicationId: string,
  payload: { status?: string; notes?: string },
) {
  return request<UserApplicationApi>(
    `/dashboard/applications/${encodeURIComponent(applicationId)}?candidate_id=${encodeURIComponent(candidateId)}`,
    {
      method: "PATCH",
      body: JSON.stringify(payload),
    },
  )
}
