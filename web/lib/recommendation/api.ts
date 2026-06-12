const BASE_URL = process.env.NEXT_PUBLIC_RECOMMENDATION_API_URL ?? "http://localhost:8002"

export interface DashboardJobApi {
  id: string
  title: string
  company_name: string
  location: string | null
  posting_url: string | null
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
