// Mock data for the dashboard - simulates API responses

// Helper to generate dates
const hoursAgo = (hours: number) => new Date(Date.now() - hours * 60 * 60 * 1000)
const daysAgo = (days: number) => new Date(Date.now() - days * 24 * 60 * 60 * 1000)

export type PipelineRunStatus = 'completed' | 'partial_success' | 'failed'
export type ProcessingState = 'success' | 'partial_success' | 'extraction_failed' | 'enrichment_failed' | 'requires_review' | 'manually_corrected' | 'pending'
export type SourceHealth = 'healthy' | 'warning' | 'critical'
export type Platform = 'greenhouse' | 'lever' | 'ashby'
export type Severity = 'info' | 'warning' | 'error' | 'critical'
export type EventCategory = 'pipeline' | 'source' | 'enrichment' | 'review' | 'system'

export interface PipelineRun {
  id: string
  timestamp: Date
  status: PipelineRunStatus
  totalCompanies: number
  successfulCompanies: number
  failedCompanies: number
  jobsFetched: number
  jobsNew: number
  jobsUpdated: number
  jobsUnchanged: number
  duration: number // seconds
}

export interface CompanyRunDetail {
  companyName: string
  platform: Platform
  status: 'success' | 'failed'
  jobsFetched: number
  jobsNew: number
  jobsUpdated: number
  jobsUnchanged: number
  errorMessage?: string
}

export interface Source {
  id: string
  companyName: string
  platform: Platform
  health: SourceHealth
  activeJobs: number
  lastSuccessfulFetch: Date | null
  lastFailure: Date | null
  consecutiveFailures: number
  isActive: boolean
  requiresReview: boolean
}

export interface Event {
  id: string
  timestamp: Date
  severity: Severity
  category: EventCategory
  eventType: string
  company?: string
  platform?: Platform
  message: string
}

export interface Job {
  id: string
  title: string
  company: string
  platform: Platform
  location: string
  department: string
  employmentType: string
  postedAt: Date
  processingState: ProcessingState
  failureReason?: string
  lastSeen: Date
  lastEnrichmentAttempt: Date | null
  lastManualReview: Date | null
  postingUrl: string
  // Enrichment fields
  seniority: string
  isInternship: boolean
  isNewGrad: boolean
  sponsorshipStatus: string
  sponsorshipConfidence: string
  remoteType: string
  techStack: string[]
  skills: string[]
  rawPayload?: object
  rawHtml?: string
}

export interface UsageData {
  inputTokens: number
  outputTokens: number
  enrichmentCount: number
  failureCount: number
  avgLatency: number
}

export interface UsageByPlatform extends UsageData {
  platform: Platform
}

export interface UsageByCompany extends UsageData {
  company: string
}

export interface TrendDataPoint {
  date: string
  inputTokens: number
  outputTokens: number
  estimatedCost: number
}

// Mock Pipeline Runs
export const mockPipelineRuns: PipelineRun[] = [
  {
    id: 'run-001',
    timestamp: hoursAgo(2),
    status: 'completed',
    totalCompanies: 45,
    successfulCompanies: 45,
    failedCompanies: 0,
    jobsFetched: 1247,
    jobsNew: 89,
    jobsUpdated: 156,
    jobsUnchanged: 1002,
    duration: 342
  },
  {
    id: 'run-002',
    timestamp: hoursAgo(8),
    status: 'partial_success',
    totalCompanies: 45,
    successfulCompanies: 42,
    failedCompanies: 3,
    jobsFetched: 1189,
    jobsNew: 67,
    jobsUpdated: 134,
    jobsUnchanged: 988,
    duration: 298
  },
  {
    id: 'run-003',
    timestamp: hoursAgo(14),
    status: 'completed',
    totalCompanies: 45,
    successfulCompanies: 45,
    failedCompanies: 0,
    jobsFetched: 1256,
    jobsNew: 112,
    jobsUpdated: 145,
    jobsUnchanged: 999,
    duration: 356
  },
  {
    id: 'run-004',
    timestamp: hoursAgo(20),
    status: 'failed',
    totalCompanies: 45,
    successfulCompanies: 12,
    failedCompanies: 33,
    jobsFetched: 423,
    jobsNew: 23,
    jobsUpdated: 45,
    jobsUnchanged: 355,
    duration: 156
  },
  {
    id: 'run-005',
    timestamp: daysAgo(1),
    status: 'completed',
    totalCompanies: 44,
    successfulCompanies: 44,
    failedCompanies: 0,
    jobsFetched: 1234,
    jobsNew: 78,
    jobsUpdated: 167,
    jobsUnchanged: 989,
    duration: 334
  },
  {
    id: 'run-006',
    timestamp: daysAgo(1.5),
    status: 'partial_success',
    totalCompanies: 44,
    successfulCompanies: 43,
    failedCompanies: 1,
    jobsFetched: 1201,
    jobsNew: 56,
    jobsUpdated: 189,
    jobsUnchanged: 956,
    duration: 312
  },
  {
    id: 'run-007',
    timestamp: daysAgo(2),
    status: 'completed',
    totalCompanies: 44,
    successfulCompanies: 44,
    failedCompanies: 0,
    jobsFetched: 1198,
    jobsNew: 92,
    jobsUpdated: 143,
    jobsUnchanged: 963,
    duration: 345
  },
]

// Mock Company Run Details
export const mockCompanyRunDetails: Record<string, CompanyRunDetail[]> = {
  'run-001': [
    { companyName: 'OpenAI', platform: 'greenhouse', status: 'success', jobsFetched: 156, jobsNew: 12, jobsUpdated: 23, jobsUnchanged: 121 },
    { companyName: 'Anthropic', platform: 'lever', status: 'success', jobsFetched: 89, jobsNew: 8, jobsUpdated: 15, jobsUnchanged: 66 },
    { companyName: 'Notion', platform: 'ashby', status: 'success', jobsFetched: 67, jobsNew: 5, jobsUpdated: 12, jobsUnchanged: 50 },
    { companyName: 'Stripe', platform: 'greenhouse', status: 'success', jobsFetched: 234, jobsNew: 18, jobsUpdated: 34, jobsUnchanged: 182 },
    { companyName: 'Figma', platform: 'lever', status: 'success', jobsFetched: 78, jobsNew: 6, jobsUpdated: 11, jobsUnchanged: 61 },
  ],
  'run-002': [
    { companyName: 'OpenAI', platform: 'greenhouse', status: 'failed', jobsFetched: 0, jobsNew: 0, jobsUpdated: 0, jobsUnchanged: 0, errorMessage: 'Rate limit exceeded' },
    { companyName: 'Anthropic', platform: 'lever', status: 'success', jobsFetched: 87, jobsNew: 7, jobsUpdated: 14, jobsUnchanged: 66 },
    { companyName: 'Notion', platform: 'ashby', status: 'failed', jobsFetched: 0, jobsNew: 0, jobsUpdated: 0, jobsUnchanged: 0, errorMessage: 'Connection timeout' },
    { companyName: 'Stripe', platform: 'greenhouse', status: 'success', jobsFetched: 231, jobsNew: 15, jobsUpdated: 32, jobsUnchanged: 184 },
    { companyName: 'Figma', platform: 'lever', status: 'failed', jobsFetched: 0, jobsNew: 0, jobsUpdated: 0, jobsUnchanged: 0, errorMessage: 'Invalid API key' },
  ],
}

// Mock Sources
export const mockSources: Source[] = [
  { id: 'src-001', companyName: 'OpenAI', platform: 'greenhouse', health: 'healthy', activeJobs: 156, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-002', companyName: 'Anthropic', platform: 'lever', health: 'healthy', activeJobs: 89, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-003', companyName: 'Notion', platform: 'ashby', health: 'warning', activeJobs: 67, lastSuccessfulFetch: hoursAgo(8), lastFailure: hoursAgo(2), consecutiveFailures: 1, isActive: true, requiresReview: false },
  { id: 'src-004', companyName: 'Stripe', platform: 'greenhouse', health: 'healthy', activeJobs: 234, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-005', companyName: 'Figma', platform: 'lever', health: 'critical', activeJobs: 78, lastSuccessfulFetch: daysAgo(2), lastFailure: hoursAgo(2), consecutiveFailures: 5, isActive: false, requiresReview: true },
  { id: 'src-006', companyName: 'Linear', platform: 'ashby', health: 'healthy', activeJobs: 45, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-007', companyName: 'Vercel', platform: 'greenhouse', health: 'healthy', activeJobs: 112, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-008', companyName: 'Supabase', platform: 'lever', health: 'warning', activeJobs: 56, lastSuccessfulFetch: hoursAgo(4), lastFailure: hoursAgo(2), consecutiveFailures: 2, isActive: true, requiresReview: false },
  { id: 'src-009', companyName: 'Clerk', platform: 'greenhouse', health: 'healthy', activeJobs: 34, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-010', companyName: 'Resend', platform: 'ashby', health: 'healthy', activeJobs: 23, lastSuccessfulFetch: hoursAgo(2), lastFailure: daysAgo(5), consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-011', companyName: 'Neon', platform: 'lever', health: 'healthy', activeJobs: 41, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
  { id: 'src-012', companyName: 'Upstash', platform: 'greenhouse', health: 'healthy', activeJobs: 28, lastSuccessfulFetch: hoursAgo(2), lastFailure: null, consecutiveFailures: 0, isActive: true, requiresReview: false },
]

// Mock Events
export const mockEvents: Event[] = [
  { id: 'evt-001', timestamp: hoursAgo(0.5), severity: 'info', category: 'pipeline', eventType: 'pipeline_completed', message: 'Pipeline completed successfully' },
  { id: 'evt-002', timestamp: hoursAgo(1), severity: 'warning', category: 'source', eventType: 'fetch_failure', company: 'Notion', platform: 'ashby', message: 'Source fetch failed - connection timeout' },
  { id: 'evt-003', timestamp: hoursAgo(1.5), severity: 'info', category: 'review', eventType: 'job_corrected', company: 'Anthropic', platform: 'lever', message: 'Reviewer corrected job metadata' },
  { id: 'evt-004', timestamp: hoursAgo(2), severity: 'error', category: 'enrichment', eventType: 'llm_timeout', company: 'OpenAI', platform: 'greenhouse', message: 'LLM timeout during enrichment' },
  { id: 'evt-005', timestamp: hoursAgo(2.5), severity: 'critical', category: 'source', eventType: 'threshold_reached', company: 'Figma', platform: 'lever', message: 'Source failure threshold reached - auto-disabled' },
  { id: 'evt-006', timestamp: hoursAgo(3), severity: 'warning', category: 'enrichment', eventType: 'malformed_response', company: 'Stripe', platform: 'greenhouse', message: 'Malformed LLM response detected' },
  { id: 'evt-007', timestamp: hoursAgo(4), severity: 'info', category: 'pipeline', eventType: 'pipeline_started', message: 'Pipeline run started' },
  { id: 'evt-008', timestamp: hoursAgo(5), severity: 'warning', category: 'enrichment', eventType: 'token_spike', company: 'Notion', platform: 'ashby', message: 'Token spike detected - 12,400 input tokens' },
  { id: 'evt-009', timestamp: hoursAgo(6), severity: 'info', category: 'review', eventType: 'job_flagged', company: 'Linear', platform: 'ashby', message: 'Job flagged for engineering review' },
  { id: 'evt-010', timestamp: hoursAgo(7), severity: 'error', category: 'source', eventType: 'api_error', company: 'Supabase', platform: 'lever', message: 'API returned 500 error' },
  { id: 'evt-011', timestamp: hoursAgo(8), severity: 'info', category: 'system', eventType: 'config_updated', message: 'System configuration updated' },
  { id: 'evt-012', timestamp: hoursAgo(9), severity: 'warning', category: 'pipeline', eventType: 'partial_success', message: 'Pipeline completed with partial success' },
]

// Mock Jobs
export const mockJobs: Job[] = [
  {
    id: 'job-001',
    title: 'Senior Software Engineer',
    company: 'OpenAI',
    platform: 'greenhouse',
    location: 'San Francisco, CA',
    department: 'Engineering',
    employmentType: 'Full-time',
    postedAt: daysAgo(3),
    processingState: 'success',
    lastSeen: hoursAgo(2),
    lastEnrichmentAttempt: hoursAgo(2),
    lastManualReview: null,
    postingUrl: 'https://openai.com/careers/senior-software-engineer',
    seniority: 'senior',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'sponsors',
    sponsorshipConfidence: 'high',
    remoteType: 'hybrid',
    techStack: ['Python', 'PyTorch', 'Kubernetes'],
    skills: ['Machine Learning', 'Distributed Systems', 'API Design'],
    rawPayload: { id: 'ext-001', source: 'greenhouse' },
    rawHtml: '<div class="job-description"><h1>Senior Software Engineer</h1><p>Join our team...</p></div>'
  },
  {
    id: 'job-002',
    title: 'Product Designer',
    company: 'Anthropic',
    platform: 'lever',
    location: 'Remote',
    department: 'Design',
    employmentType: 'Full-time',
    postedAt: daysAgo(5),
    processingState: 'requires_review',
    lastSeen: hoursAgo(2),
    lastEnrichmentAttempt: hoursAgo(2),
    lastManualReview: null,
    postingUrl: 'https://anthropic.com/careers/product-designer',
    seniority: 'mid',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'unknown',
    sponsorshipConfidence: 'low',
    remoteType: 'remote',
    techStack: ['Figma', 'Framer'],
    skills: ['Product Design', 'User Research', 'Prototyping'],
    rawPayload: { id: 'ext-002', source: 'lever' },
    rawHtml: '<div class="job-description"><h1>Product Designer</h1><p>We are looking for...</p></div>'
  },
  {
    id: 'job-003',
    title: 'ML Research Intern',
    company: 'Notion',
    platform: 'ashby',
    location: 'New York, NY',
    department: 'Research',
    employmentType: 'Internship',
    postedAt: daysAgo(1),
    processingState: 'enrichment_failed',
    failureReason: 'llm_timeout',
    lastSeen: hoursAgo(2),
    lastEnrichmentAttempt: hoursAgo(2),
    lastManualReview: null,
    postingUrl: 'https://notion.com/careers/ml-research-intern',
    seniority: 'intern',
    isInternship: true,
    isNewGrad: false,
    sponsorshipStatus: 'does_not_sponsor',
    sponsorshipConfidence: 'medium',
    remoteType: 'onsite',
    techStack: ['Python', 'TensorFlow'],
    skills: ['Machine Learning', 'Research'],
    rawPayload: { id: 'ext-003', source: 'ashby' },
    rawHtml: '<div class="job-description"><h1>ML Research Intern</h1><p>Summer 2025...</p></div>'
  },
  {
    id: 'job-004',
    title: 'Staff Engineer - Platform',
    company: 'Stripe',
    platform: 'greenhouse',
    location: 'Seattle, WA',
    department: 'Engineering',
    employmentType: 'Full-time',
    postedAt: daysAgo(7),
    processingState: 'partial_success',
    lastSeen: hoursAgo(2),
    lastEnrichmentAttempt: hoursAgo(4),
    lastManualReview: null,
    postingUrl: 'https://stripe.com/jobs/staff-engineer',
    seniority: 'staff',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'sponsors',
    sponsorshipConfidence: 'high',
    remoteType: 'hybrid',
    techStack: ['Ruby', 'Go', 'AWS'],
    skills: ['Platform Engineering', 'Scalability', 'Team Leadership'],
    rawPayload: { id: 'ext-004', source: 'greenhouse' },
    rawHtml: '<div class="job-description"><h1>Staff Engineer - Platform</h1><p>Lead our platform...</p></div>'
  },
  {
    id: 'job-005',
    title: 'Frontend Engineer',
    company: 'Figma',
    platform: 'lever',
    location: 'San Francisco, CA',
    department: 'Engineering',
    employmentType: 'Full-time',
    postedAt: daysAgo(2),
    processingState: 'extraction_failed',
    failureReason: 'parse_error',
    lastSeen: daysAgo(2),
    lastEnrichmentAttempt: null,
    lastManualReview: null,
    postingUrl: 'https://figma.com/careers/frontend-engineer',
    seniority: 'mid',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'unknown',
    sponsorshipConfidence: 'low',
    remoteType: 'onsite',
    techStack: ['TypeScript', 'React', 'WebGL'],
    skills: ['Frontend Development', 'Performance Optimization'],
    rawPayload: { id: 'ext-005', source: 'lever' },
    rawHtml: '<div class="job-description"><h1>Frontend Engineer</h1><p>Build the future...</p></div>'
  },
  {
    id: 'job-006',
    title: 'New Grad Software Engineer',
    company: 'Linear',
    platform: 'ashby',
    location: 'Remote',
    department: 'Engineering',
    employmentType: 'Full-time',
    postedAt: daysAgo(4),
    processingState: 'manually_corrected',
    lastSeen: hoursAgo(2),
    lastEnrichmentAttempt: hoursAgo(8),
    lastManualReview: hoursAgo(6),
    postingUrl: 'https://linear.app/careers/new-grad',
    seniority: 'entry',
    isInternship: false,
    isNewGrad: true,
    sponsorshipStatus: 'sponsors',
    sponsorshipConfidence: 'high',
    remoteType: 'remote',
    techStack: ['TypeScript', 'React', 'Node.js'],
    skills: ['Full Stack Development', 'Problem Solving'],
    rawPayload: { id: 'ext-006', source: 'ashby' },
    rawHtml: '<div class="job-description"><h1>New Grad Software Engineer</h1><p>Start your career...</p></div>'
  },
  {
    id: 'job-007',
    title: 'DevOps Engineer',
    company: 'Vercel',
    platform: 'greenhouse',
    location: 'Remote',
    department: 'Infrastructure',
    employmentType: 'Full-time',
    postedAt: daysAgo(6),
    processingState: 'success',
    lastSeen: hoursAgo(2),
    lastEnrichmentAttempt: hoursAgo(2),
    lastManualReview: null,
    postingUrl: 'https://vercel.com/careers/devops',
    seniority: 'senior',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'sponsors',
    sponsorshipConfidence: 'medium',
    remoteType: 'remote',
    techStack: ['Terraform', 'Kubernetes', 'AWS'],
    skills: ['CI/CD', 'Infrastructure as Code', 'Monitoring'],
    rawPayload: { id: 'ext-007', source: 'greenhouse' },
    rawHtml: '<div class="job-description"><h1>DevOps Engineer</h1><p>Scale our infrastructure...</p></div>'
  },
  {
    id: 'job-008',
    title: 'Backend Engineer',
    company: 'Supabase',
    platform: 'lever',
    location: 'Remote',
    department: 'Engineering',
    employmentType: 'Full-time',
    postedAt: daysAgo(8),
    processingState: 'pending',
    lastSeen: hoursAgo(1),
    lastEnrichmentAttempt: null,
    lastManualReview: null,
    postingUrl: 'https://supabase.com/careers/backend',
    seniority: 'mid',
    isInternship: false,
    isNewGrad: false,
    sponsorshipStatus: 'unknown',
    sponsorshipConfidence: 'low',
    remoteType: 'remote',
    techStack: ['Elixir', 'PostgreSQL', 'Go'],
    skills: ['Database Design', 'API Development'],
    rawPayload: { id: 'ext-008', source: 'lever' },
    rawHtml: '<div class="job-description"><h1>Backend Engineer</h1><p>Build open source...</p></div>'
  },
]

// Mock Usage Data
export const mockUsageByPlatform: UsageByPlatform[] = [
  { platform: 'greenhouse', inputTokens: 245000, outputTokens: 89000, enrichmentCount: 456, failureCount: 12, avgLatency: 1240 },
  { platform: 'lever', inputTokens: 178000, outputTokens: 67000, enrichmentCount: 312, failureCount: 8, avgLatency: 1120 },
  { platform: 'ashby', inputTokens: 98000, outputTokens: 34000, enrichmentCount: 189, failureCount: 5, avgLatency: 980 },
]

export const mockUsageByCompany: UsageByCompany[] = [
  { company: 'OpenAI', inputTokens: 89000, outputTokens: 32000, enrichmentCount: 156, failureCount: 3, avgLatency: 1340 },
  { company: 'Anthropic', inputTokens: 67000, outputTokens: 24000, enrichmentCount: 89, failureCount: 2, avgLatency: 1180 },
  { company: 'Stripe', inputTokens: 78000, outputTokens: 28000, enrichmentCount: 234, failureCount: 4, avgLatency: 1220 },
  { company: 'Notion', inputTokens: 45000, outputTokens: 16000, enrichmentCount: 67, failureCount: 3, avgLatency: 1090 },
  { company: 'Figma', inputTokens: 34000, outputTokens: 12000, enrichmentCount: 78, failureCount: 5, avgLatency: 1450 },
  { company: 'Linear', inputTokens: 28000, outputTokens: 10000, enrichmentCount: 45, failureCount: 1, avgLatency: 920 },
  { company: 'Vercel', inputTokens: 56000, outputTokens: 20000, enrichmentCount: 112, failureCount: 2, avgLatency: 1080 },
  { company: 'Supabase', inputTokens: 32000, outputTokens: 11000, enrichmentCount: 56, failureCount: 3, avgLatency: 1150 },
]

export const mockTrendData: TrendDataPoint[] = Array.from({ length: 30 }, (_, i) => {
  const date = daysAgo(29 - i)
  const baseInput = 400000 + Math.random() * 150000
  const baseOutput = 150000 + Math.random() * 50000
  return {
    date: date.toISOString().split('T')[0],
    inputTokens: Math.round(baseInput),
    outputTokens: Math.round(baseOutput),
    estimatedCost: Number(((baseInput / 1000 * 0.0015) + (baseOutput / 1000 * 0.002)).toFixed(2))
  }
})

// Summary calculations
export const getSummaryStats = () => {
  const lastRun = mockPipelineRuns[0]
  const totalActiveJobs = mockSources.reduce((sum, s) => sum + s.activeJobs, 0)
  const sourcesWithFailures = mockSources.filter(s => s.consecutiveFailures > 0).length
  const pausedSources = mockSources.filter(s => !s.isActive).length
  const flaggedSources = mockSources.filter(s => s.requiresReview).length
  const jobsRequiringReview = mockJobs.filter(j => j.processingState === 'requires_review').length
  const enrichmentFailures = mockJobs.filter(j => j.processingState === 'enrichment_failed' || j.processingState === 'extraction_failed').length
  const manualCorrectionsToday = mockJobs.filter(j => j.lastManualReview && j.lastManualReview > daysAgo(1)).length
  const oldestPendingReview = mockJobs
    .filter(j => j.processingState === 'requires_review')
    .sort((a, b) => a.lastSeen.getTime() - b.lastSeen.getTime())[0]

  const totalInputTokens = mockUsageByPlatform.reduce((sum, p) => sum + p.inputTokens, 0)
  const totalOutputTokens = mockUsageByPlatform.reduce((sum, p) => sum + p.outputTokens, 0)
  const totalEnrichments = mockUsageByPlatform.reduce((sum, p) => sum + p.enrichmentCount, 0)
  const totalFailures = mockUsageByPlatform.reduce((sum, p) => sum + p.failureCount, 0)

  return {
    pipeline: {
      lastRunStatus: lastRun.status,
      lastRunTime: lastRun.timestamp,
      jobsFetched: lastRun.jobsFetched,
      failedCompanies: lastRun.failedCompanies
    },
    sources: {
      totalActive: mockSources.filter(s => s.isActive).length,
      withFailures: sourcesWithFailures,
      paused: pausedSources,
      flaggedForReview: flaggedSources
    },
    cost: {
      totalInputTokens,
      totalOutputTokens,
      estimatedCost: (totalInputTokens / 1000 * 0.0015) + (totalOutputTokens / 1000 * 0.002),
      enrichmentFailureRate: totalEnrichments > 0 ? (totalFailures / totalEnrichments * 100) : 0
    },
    jobs: {
      requiresReview: jobsRequiringReview,
      enrichmentFailures,
      manualCorrectionsToday,
      oldestPendingReview: oldestPendingReview?.lastSeen || null
    }
  }
}
