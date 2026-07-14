'use client'

import type {
  CompanyRunDetail,
  Event,
  EventCategory,
  Job,
  PipelineRun,
  Platform,
  ProcessingState,
  Severity,
  Source,
  SourceHealth,
  TrendDataPoint,
  UsageByCompany,
  UsageByPlatform,
} from '@/lib/mock-data'

const API_BASE_URL = process.env.NEXT_PUBLIC_JOB_INGESTION_API_URL || 'http://localhost:8000'

type PipelineRunResponse = {
  id: string
  status: PipelineRun['status']
  started_at: string
  completed_at: string | null
  total_companies: number
  successful_companies: number
  failed_companies: number
  jobs_fetched: number
  jobs_new: number
  jobs_updated: number
  jobs_unchanged: number
}

type CompanyResponse = {
  id: string
  name: string
  platform: Platform
  is_active: boolean
  requires_review: boolean
  active_jobs_count?: number | null
  consecutive_fetch_failures: number
  last_failure_at: string | null
  last_successful_fetch_at: string | null
}

type IngestionEventResponse = {
  id: string
  event_type: string
  event_category: EventCategory
  severity: Severity
  platform: Platform | null
  company_id: string | null
  metadata: Record<string, unknown>
  created_at: string
}

type JobListResponse = {
  id: string
  title: string
  company_name: string
  location: string | null
  department: string | null
  processing_state: ProcessingState
  failure_reason: string | null
  posting_url: string | null
  extracted_at: string
  last_seen_at: string
  last_manual_review_at: string | null
}

type JobDetailResponse = {
  id: string
  title: string
  company_name: string
  company_id: string
  location: string | null
  department: string | null
  employment_type: string | null
  posted_at: string | null
  processing_state: ProcessingState
  failure_reason: string | null
  posting_url: string | null
  last_seen_at: string
  last_manual_review_at: string | null
  seniority?: string | null
  is_internship?: boolean | null
  is_new_grad?: boolean | null
  sponsorship_status?: string | null
  sponsorship_confidence?: string | null
  remote_type?: string | null
  tech_stack?: string[] | null
  skills?: string[] | null
  enrichments: Array<{
    created_at: string
    seniority: string | null
    is_internship: boolean | null
    is_new_grad: boolean | null
    sponsorship_status: string | null
    sponsorship_confidence: string | null
    remote_type: string | null
    tech_stack: string[]
    skills: string[]
  }>
}

type UsageResponse = {
  summary: {
    total_input_tokens: number
    total_output_tokens: number
    estimated_cost: number
    enrichment_failure_rate: number
  }
  breakdown: Array<{
    platform?: Platform
    company?: string
    input_tokens: number
    output_tokens: number
    enrichment_count: number
    failure_count: number
    avg_latency_ms: number
    estimated_cost: number
  }>
}

type TrendResponse = {
  points: Array<{
    bucket: string
    input_tokens: number
    output_tokens: number
    estimated_cost: number
  }>
}

export type JobUpdateInput = {
  seniority: string
  isInternship: boolean
  isNewGrad: boolean
  sponsorshipStatus: string
  sponsorshipConfidence: string
  remoteType: string
  techStack: string[]
  skills: string[]
  comment: string
}

export type UsagePeriod = 'run' | 'day' | 'month'
export type UsageSplitBy = 'platform' | 'company'

export type TaxonomyHealthResponse = {
  generated_at: string
  total_active_enriched: number
  global_no_pool_count: number
  global_no_pool_pct: number
  domains_flagged: number
  domains_needing_review: number
  domains: Array<{
    domain: string
    total: number
    no_pool: number
    no_pool_pct: number
    flagged: boolean
    acknowledged: boolean
    acknowledged_at: string | null
    needs_review: boolean
    top_no_pool_titles: Array<{ title: string; count: number }>
  }>
}

function parseDate(value: string | null | undefined): Date | null {
  if (!value) return null
  const parsed = new Date(value)
  return Number.isNaN(parsed.getTime()) ? null : parsed
}

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = {
    ...(init?.headers as Record<string, string> | undefined),
  }
  if (init?.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
    cache: 'no-store',
  })
  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed: ${response.status}`)
  }
  return (await response.json()) as T
}

export async function getCompanies(params?: {
  includeJobCounts?: boolean
  limit?: number
  offset?: number
}): Promise<Source[]> {
  const query = new URLSearchParams()
  query.set('include_job_counts', String(Boolean(params?.includeJobCounts)))
  query.set('limit', String(params?.limit ?? 200))
  query.set('offset', String(params?.offset ?? 0))
  const rows = await apiRequest<CompanyResponse[]>(`/companies?${query.toString()}`)
  return rows.map((row) => ({
    id: row.id,
    companyName: row.name,
    platform: row.platform,
    health: deriveSourceHealth(row),
    activeJobs: row.active_jobs_count ?? 0,
    lastSuccessfulFetch: parseDate(row.last_successful_fetch_at),
    lastFailure: parseDate(row.last_failure_at),
    consecutiveFailures: row.consecutive_fetch_failures,
    isActive: row.is_active,
    requiresReview: row.requires_review,
  }))
}

export async function patchCompany(companyId: string, payload: { isActive: boolean }): Promise<void> {
  await apiRequest(`/companies/${companyId}`, {
    method: 'PATCH',
    body: JSON.stringify({ is_active: payload.isActive }),
  })
}

export async function flagCompany(companyId: string, comment?: string): Promise<void> {
  await apiRequest(`/companies/${companyId}/flag`, {
    method: 'POST',
    body: JSON.stringify({ comment: comment || '' }),
  })
}

export async function getPipelineRuns(limit = 20, offset = 0): Promise<PipelineRun[]> {
  const rows = await apiRequest<PipelineRunResponse[]>(`/pipeline/runs?limit=${limit}&offset=${offset}`)
  return rows.map((row) => {
    const startedAt = parseDate(row.started_at) ?? new Date()
    const completedAt = parseDate(row.completed_at)
    const durationSeconds = completedAt
      ? Math.max(0, Math.floor((completedAt.getTime() - startedAt.getTime()) / 1000))
      : 0
    return {
      id: row.id,
      timestamp: startedAt,
      status: row.status,
      totalCompanies: row.total_companies,
      successfulCompanies: row.successful_companies,
      failedCompanies: row.failed_companies,
      jobsFetched: row.jobs_fetched,
      jobsNew: row.jobs_new,
      jobsUpdated: row.jobs_updated,
      jobsUnchanged: row.jobs_unchanged,
      duration: durationSeconds,
    }
  })
}

export async function getCompanyRunDetails(runId: string): Promise<CompanyRunDetail[]> {
  const [runDetail, companies] = await Promise.all([
    apiRequest<{ companies: Array<{ company_id: string; status: 'success' | 'failed'; jobs_fetched: number; jobs_new: number; jobs_updated: number; jobs_unchanged: number; error_message: string | null }> }>(`/pipeline/runs/${runId}`),
    getCompanies({ includeJobCounts: false, limit: 500 }),
  ])
  const companyById = new Map(companies.map((company) => [company.id, company]))
  return runDetail.companies.map((row) => {
    const source = companyById.get(row.company_id)
    return {
      companyName: source?.companyName || 'Unknown',
      platform: source?.platform || 'greenhouse',
      status: row.status,
      jobsFetched: row.jobs_fetched,
      jobsNew: row.jobs_new,
      jobsUpdated: row.jobs_updated,
      jobsUnchanged: row.jobs_unchanged,
      errorMessage: row.error_message || undefined,
    }
  })
}

export async function getEvents(filters?: {
  severity?: string
  platform?: string
  category?: string
  companyId?: string
  limit?: number
  offset?: number
}): Promise<Event[]> {
  const query = new URLSearchParams()
  if (filters?.severity && filters.severity !== 'all') query.set('severity', filters.severity)
  if (filters?.platform && filters.platform !== 'all') query.set('platform', filters.platform)
  if (filters?.category && filters.category !== 'all') query.set('category', filters.category)
  if (filters?.companyId) query.set('company_id', filters.companyId)
  query.set('limit', String(filters?.limit ?? 100))
  query.set('offset', String(filters?.offset ?? 0))

  const [rows, companies] = await Promise.all([
    apiRequest<IngestionEventResponse[]>(`/events?${query.toString()}`),
    getCompanies({ includeJobCounts: false, limit: 500 }),
  ])
  const companyNameById = new Map(companies.map((company) => [company.id, company.companyName]))
  return rows.map((row) => ({
    id: row.id,
    timestamp: parseDate(row.created_at) ?? new Date(),
    severity: row.severity,
    category: row.event_category,
    eventType: row.event_type,
    company: row.company_id ? companyNameById.get(row.company_id) : undefined,
    platform: row.platform || undefined,
    message: getEventMessage(row),
  }))
}

export type CadenceHealth = 'on_target' | 'drifting' | 'behind' | 'never_fetched'

export type CadenceCompany = {
  id: string
  name: string
  platform: string
  tier: number
  isActive: boolean
  targetCadenceHours: number
  actualCadenceHours: number | null
  hoursSinceLastSuccess: number | null
  observedIntervalHours: number | null
  lastSuccessfulFetchAt: Date | null
  consecutiveFailures: number
  health: CadenceHealth
  driftRatio: number | null
}

export type CadenceStats = {
  generatedAt: Date
  tickMinutes: number
  batchCap: number
  scheduleIntervalsHours: Record<string, Record<string, number>>
  summary: {
    total: number
    neverFetched: number
    onTarget: number
    drifting: number
    behind: number
    avgDriftPct: number
  }
  companies: CadenceCompany[]
}

type CadenceStatsResponse = {
  generated_at: string
  tick_minutes: number
  batch_cap: number
  schedule_intervals_hours: Record<string, Record<string, number>>
  summary: {
    total: number
    never_fetched: number
    on_target: number
    drifting: number
    behind: number
    avg_drift_pct: number
  }
  companies: Array<{
    id: string
    name: string
    platform: string
    tier: number
    is_active: boolean
    target_cadence_hours: number
    actual_cadence_hours: number | null
    hours_since_last_success: number | null
    observed_interval_hours: number | null
    last_successful_fetch_at: string | null
    consecutive_failures: number
    health: CadenceHealth
    drift_ratio: number | null
  }>
}

export async function getCadenceStats(includeInactive = false): Promise<CadenceStats> {
  const query = new URLSearchParams()
  query.set('include_inactive', String(includeInactive))
  const response = await apiRequest<CadenceStatsResponse>(`/stats/cadence?${query.toString()}`)
  return {
    generatedAt: parseDate(response.generated_at) ?? new Date(),
    tickMinutes: response.tick_minutes,
    batchCap: response.batch_cap,
    scheduleIntervalsHours: response.schedule_intervals_hours,
    summary: {
      total: response.summary.total,
      neverFetched: response.summary.never_fetched,
      onTarget: response.summary.on_target,
      drifting: response.summary.drifting,
      behind: response.summary.behind,
      avgDriftPct: response.summary.avg_drift_pct,
    },
    companies: response.companies.map((row) => ({
      id: row.id,
      name: row.name,
      platform: row.platform,
      tier: row.tier,
      isActive: row.is_active,
      targetCadenceHours: row.target_cadence_hours,
      actualCadenceHours: row.actual_cadence_hours,
      hoursSinceLastSuccess: row.hours_since_last_success,
      observedIntervalHours: row.observed_interval_hours,
      lastSuccessfulFetchAt: parseDate(row.last_successful_fetch_at),
      consecutiveFailures: row.consecutive_failures,
      health: row.health,
      driftRatio: row.drift_ratio,
    })),
  }
}

export async function getTaxonomyHealth(): Promise<TaxonomyHealthResponse> {
  return apiRequest<TaxonomyHealthResponse>('/admin/taxonomy-health')
}

export async function setTaxonomyDomainAcknowledged(
  domain: string,
  acknowledged: boolean,
): Promise<TaxonomyHealthResponse> {
  const encoded = encodeURIComponent(domain)
  return apiRequest<TaxonomyHealthResponse>(
    `/admin/taxonomy-health/domains/${encoded}/acknowledge`,
    {
      method: 'PATCH',
      body: JSON.stringify({ acknowledged }),
    },
  )
}

export type H1bStatsResponse = {
  generated_at: string
  total_employers: number
  matched_employers: number
  unmatched_employers: number
  match_rate_pct: number
  lca_rows_by_year: Array<{ fiscal_year: number; count: number }>
  total_lca_rows: number
}

export type H1bReviewQueueResponse = {
  items: Array<{
    id: number
    employer_name_norm: string
    match_method: string
    match_confidence: number | null
    total_lca: number
  }>
}

export type H1bCoverageResponse = {
  items: Array<{
    pool_family: string
    tracked_companies: number
    companies_with_data: number
    coverage_pct: number
    flagged: boolean
  }>
}

export async function getH1bStats(): Promise<H1bStatsResponse> {
  return apiRequest<H1bStatsResponse>('/admin/h1b-stats')
}

export async function getH1bReviewQueue(): Promise<H1bReviewQueueResponse> {
  return apiRequest<H1bReviewQueueResponse>('/admin/h1b-review-queue')
}

export async function getH1bCoverage(): Promise<H1bCoverageResponse> {
  return apiRequest<H1bCoverageResponse>('/admin/h1b-coverage')
}

export async function linkH1bEmployer(employerId: number, companyId: string): Promise<void> {
  await apiRequest(`/admin/h1b-employer/${employerId}`, {
    method: 'PATCH',
    body: JSON.stringify({ company_id: companyId }),
  })
}

export async function triggerH1bIngest(): Promise<{ status: string; results: Record<string, unknown> }> {
  return apiRequest('/admin/h1b-ingest', { method: 'POST' })
}

export async function getCostUsage(params: {
  period: UsagePeriod
  splitBy: UsageSplitBy
  runId?: string
  date?: string
  month?: string
}): Promise<{
  summary: UsageResponse['summary']
  usageByPlatform: UsageByPlatform[]
  usageByCompany: UsageByCompany[]
}> {
  const query = new URLSearchParams()
  query.set('period', params.period)
  query.set('split_by', params.splitBy)
  if (params.runId) query.set('run_id', params.runId)
  if (params.date) query.set('date', params.date)
  if (params.month) query.set('month', params.month)

  const response = await apiRequest<UsageResponse>(`/enrichments/usage?${query.toString()}`)
  return {
    summary: response.summary,
    usageByPlatform: response.breakdown
      .filter((row) => row.platform)
      .map((row) => ({
        platform: row.platform!,
        inputTokens: row.input_tokens,
        outputTokens: row.output_tokens,
        enrichmentCount: row.enrichment_count,
        failureCount: row.failure_count,
        avgLatency: Math.round(row.avg_latency_ms),
      })),
    usageByCompany: response.breakdown
      .filter((row) => row.company)
      .map((row) => ({
        company: row.company as string,
        inputTokens: row.input_tokens,
        outputTokens: row.output_tokens,
        enrichmentCount: row.enrichment_count,
        failureCount: row.failure_count,
        avgLatency: Math.round(row.avg_latency_ms),
      })),
  }
}

export async function getCostTrend(period: UsagePeriod, days = 30): Promise<TrendDataPoint[]> {
  const response = await apiRequest<TrendResponse>(`/enrichments/usage/trend?period=${period}&days=${days}`)
  return response.points.map((point) => ({
    date: point.bucket,
    inputTokens: point.input_tokens,
    outputTokens: point.output_tokens,
    estimatedCost: point.estimated_cost,
  }))
}

export async function getJobs(filters?: {
  processingState?: string
  platform?: string
  company?: string
  title?: string
  limit?: number
  offset?: number
  sortBy?: string
  sortDir?: 'asc' | 'desc'
}): Promise<Job[]> {
  const query = new URLSearchParams()
  if (filters?.processingState) query.set('processing_state', filters.processingState)
  if (filters?.platform && filters.platform !== 'all') query.set('platform', filters.platform)
  if (filters?.company && filters.company !== 'all') query.set('company', filters.company)
  if (filters?.title) query.set('title', filters.title)
  query.set('limit', String(filters?.limit ?? 200))
  query.set('offset', String(filters?.offset ?? 0))
  query.set('sort_by', filters?.sortBy ?? 'updated_at')
  query.set('sort_dir', filters?.sortDir ?? 'desc')

  const [jobs, companies] = await Promise.all([
    apiRequest<JobListResponse[]>(`/jobs?${query.toString()}`),
    getCompanies({ includeJobCounts: false, limit: 500 }),
  ])
  const platformByCompany = new Map(companies.map((company) => [company.companyName, company.platform]))
  return jobs.map((job) => ({
    id: job.id,
    title: job.title,
    company: job.company_name,
    platform: platformByCompany.get(job.company_name) || 'greenhouse',
    location: job.location || 'Unknown',
    department: job.department || 'Unknown',
    employmentType: 'Unknown',
    postedAt: parseDate(job.posted_at) || parseDate(job.last_seen_at) || new Date(),
    processingState: job.processing_state,
    failureReason: job.failure_reason || undefined,
    lastSeen: parseDate(job.last_seen_at) || new Date(),
    lastEnrichmentAttempt: parseDate(job.extracted_at),
    lastManualReview: parseDate(job.last_manual_review_at),
    postingUrl: job.posting_url || '#',
    seniority: 'unclear',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'unclear',
    sponsorshipConfidence: 'low',
    remoteType: 'unclear',
    techStack: [],
    skills: [],
  }))
}

export async function getJobDetail(jobId: string): Promise<Job> {
  const [job, raw, companies] = await Promise.all([
    apiRequest<JobDetailResponse>(`/jobs/${jobId}`),
    apiRequest<{ raw_api_response: object; raw_html: string }>(`/jobs/${jobId}/raw`),
    getCompanies({ includeJobCounts: false, limit: 500 }),
  ])
  const platformByCompany = new Map(companies.map((company) => [company.companyName, company.platform]))
  const latestEnrichment = job.enrichments?.[0]
  return {
    id: job.id,
    title: job.title,
    company: job.company_name,
    platform: platformByCompany.get(job.company_name) || 'greenhouse',
    location: job.location || 'Unknown',
    department: job.department || 'Unknown',
    employmentType: job.employment_type || 'Unknown',
    postedAt: parseDate(job.posted_at) || parseDate(job.last_seen_at) || new Date(),
    processingState: job.processing_state,
    failureReason: job.failure_reason || undefined,
    lastSeen: parseDate(job.last_seen_at) || new Date(),
    lastEnrichmentAttempt: latestEnrichment ? parseDate(latestEnrichment.created_at) : null,
    lastManualReview: parseDate(job.last_manual_review_at),
    postingUrl: job.posting_url || '#',
    seniority: latestEnrichment?.seniority || 'unclear',
    isInternship: Boolean(latestEnrichment?.is_internship),
    isNewGrad: Boolean(latestEnrichment?.is_new_grad),
    sponsorshipStatus: latestEnrichment?.sponsorship_status || 'unclear',
    sponsorshipConfidence: latestEnrichment?.sponsorship_confidence || 'low',
    remoteType: latestEnrichment?.remote_type || 'unclear',
    techStack: latestEnrichment?.tech_stack || [],
    skills: latestEnrichment?.skills || [],
    rawPayload: raw.raw_api_response,
    rawHtml: raw.raw_html,
  }
}

export async function saveJobReview(jobId: string, payload: JobUpdateInput): Promise<void> {
  await apiRequest(`/jobs/${jobId}`, {
    method: 'PATCH',
    body: JSON.stringify({
      seniority: payload.seniority,
      is_internship: payload.isInternship,
      is_new_grad: payload.isNewGrad,
      sponsorship_status: payload.sponsorshipStatus,
      sponsorship_confidence: payload.sponsorshipConfidence,
      remote_type: payload.remoteType,
      tech_stack: payload.techStack,
      skills: payload.skills,
      comment: payload.comment,
    }),
  })
}

export async function flagJob(jobId: string, comment: string): Promise<void> {
  await apiRequest(`/jobs/${jobId}/flag`, {
    method: 'POST',
    body: JSON.stringify({ comment }),
  })
}

function deriveSourceHealth(row: CompanyResponse): SourceHealth {
  if (!row.is_active || row.consecutive_fetch_failures >= 3) return 'critical'
  if (row.consecutive_fetch_failures > 0 || row.requires_review) return 'warning'
  return 'healthy'
}

function getEventMessage(row: IngestionEventResponse): string {
  const metadata = row.metadata || {}
  const directMessage = metadata.message
  if (typeof directMessage === 'string' && directMessage.trim()) {
    return directMessage
  }
  const errorMessage = metadata.error_message
  if (typeof errorMessage === 'string' && errorMessage.trim()) {
    return errorMessage
  }
  return row.event_type.replaceAll('_', ' ')
}
