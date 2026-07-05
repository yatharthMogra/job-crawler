const BASE_URL = process.env.NEXT_PUBLIC_RECOMMENDATION_API_URL ?? "http://localhost:8002"

export type SponsorshipStatus = "yes" | "no" | "unclear"

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
  h1b_sponsorship: H1BSponsorshipInfo | null
  company_info: CompanyEnrichmentInfo | null
}

export interface RecommendedJobApi extends DashboardJobApi {
  personal_score: number
  match_reasons: string[]
}

export interface DashboardJobsResponse {
  jobs: DashboardJobApi[]
  total: number
}

export interface RecommendedJobsResponse {
  jobs: RecommendedJobApi[]
  total: number
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
  params: { limit?: number; offset?: number } = {},
) {
  const query = new URLSearchParams({ candidate_id: candidateId })
  if (params.limit != null) query.set("limit", String(params.limit))
  if (params.offset != null) query.set("offset", String(params.offset))
  return request<RecommendedJobsResponse>(`/dashboard/jobs/recommended?${query}`)
}

export function fetchDashboardJob(candidateId: string, jobId: string) {
  return request<DashboardJobApi>(
    `/dashboard/jobs/${jobId}?candidate_id=${encodeURIComponent(candidateId)}`,
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

export interface NotificationPreferencesApi {
  candidate_id: string
  digest_enabled: boolean
  company_watch_enabled: boolean
  cadence_hours: number
  top_k: number
  digest_filters: Record<string, unknown> | null
  last_digest_sent_at: string | null
  next_digest_due_at: string | null
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

export function fetchNotificationPreferences(candidateId: string) {
  return request<NotificationPreferencesApi>(`/notification-preferences/${candidateId}`)
}

export function updateNotificationPreferences(
  candidateId: string,
  payload: Partial<{
    digest_enabled: boolean
    company_watch_enabled: boolean
    cadence_hours: number
    top_k: number
  }>,
) {
  return request<NotificationPreferencesApi>(`/notification-preferences/${candidateId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  })
}

export function fetchCompanyWatch(candidateId: string) {
  return request<CompanyWatchListApi>(`/company-watch/${candidateId}`)
}

export function updateCompanyWatch(candidateId: string, companyIds: string[]) {
  return request<CompanyWatchListApi>(`/company-watch/${candidateId}`, {
    method: "PUT",
    body: JSON.stringify({ company_ids: companyIds }),
  })
}

export function searchCompanies(q = "", limit = 20) {
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
