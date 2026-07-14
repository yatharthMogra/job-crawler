// Relative time formatting following spec conventions
export function formatRelativeTime(date: Date | string | null): string {
  if (!date) return 'Never'
  
  const now = new Date()
  const d = typeof date === 'string' ? new Date(date) : date
  const diffMs = now.getTime() - d.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)
  
  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} minute${diffMins === 1 ? '' : 's'} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  
  return d.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: d.getFullYear() !== now.getFullYear() ? 'numeric' : undefined 
  })
}

export function formatAbsoluteTime(date: Date | string | null): string {
  if (!date) return 'Never'
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

// Human-readable label mappings
export const processingStateLabels: Record<string, string> = {
  success: 'Success',
  partial_success: 'Partial Success',
  extraction_failed: 'Extraction Failed',
  enrichment_failed: 'Enrichment Failed',
  requires_review: 'Requires Review',
  manually_corrected: 'Manually Corrected',
  pending: 'Pending'
}

export const failureReasonLabels: Record<string, string> = {
  llm_timeout: 'LLM Timeout',
  malformed_response: 'Malformed LLM Response',
  rate_limit: 'Rate Limited',
  parse_error: 'Parse Error',
  network_error: 'Network Error',
  validation_error: 'Validation Error',
  unknown: 'Unknown Error'
}

export const eventCategoryLabels: Record<string, string> = {
  pipeline: 'Pipeline',
  source: 'Source',
  enrichment: 'Enrichment',
  review: 'Review',
  system: 'System'
}

export const severityLabels: Record<string, string> = {
  info: 'Info',
  warning: 'Warning',
  error: 'Error',
  critical: 'Critical'
}

export const platformLabels: Record<string, string> = {
  greenhouse: 'Greenhouse',
  lever: 'Lever',
  ashby: 'Ashby',
  workday: 'Workday',
  oracle_hcm: 'Oracle HCM',
  icims: 'iCIMS',
  eightfold: 'Eightfold',
  successfactors: 'SuccessFactors',
  workable: 'Workable',
  smartrecruiters: 'SmartRecruiters',
  bamboohr: 'BambooHR',
  workatastartup: 'Work at a Startup',
  google_careers: 'Google Careers',
  amazon_jobs: 'Amazon Jobs',
  uber_careers: 'Uber Careers',
}

export function formatPlatformLabel(platform: string): string {
  return platformLabels[platform] ?? platform
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

export const seniorityOptions = [
  { value: 'intern', label: 'Intern' },
  { value: 'entry', label: 'Entry Level' },
  { value: 'mid', label: 'Mid Level' },
  { value: 'senior', label: 'Senior' },
  { value: 'staff', label: 'Staff' },
  { value: 'principal', label: 'Principal' },
  { value: 'director', label: 'Director' },
  { value: 'vp', label: 'VP' },
  { value: 'c_level', label: 'C-Level' }
]

export const sponsorshipStatusOptions = [
  { value: 'sponsors', label: 'Sponsors Visas' },
  { value: 'does_not_sponsor', label: 'Does Not Sponsor' },
  { value: 'unknown', label: 'Unknown' }
]

export const sponsorshipConfidenceOptions = [
  { value: 'high', label: 'High' },
  { value: 'medium', label: 'Medium' },
  { value: 'low', label: 'Low' }
]

export const remoteTypeOptions = [
  { value: 'remote', label: 'Remote' },
  { value: 'hybrid', label: 'Hybrid' },
  { value: 'onsite', label: 'On-site' }
]

// Cost calculation
export function calculateEstimatedCost(inputTokens: number, outputTokens: number): number {
  const inputCostPer1k = 0.0015 // Default cost per 1k input tokens
  const outputCostPer1k = 0.002 // Default cost per 1k output tokens
  return (inputTokens / 1000 * inputCostPer1k) + (outputTokens / 1000 * outputCostPer1k)
}

export function formatCost(cost: number): string {
  if (cost < 0.01) return '<$0.01'
  return `$${cost.toFixed(2)}`
}

export function formatNumber(num: number): string {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`
  return num.toString()
}
