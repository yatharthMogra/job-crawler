'use client'

import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { PipelineRunStatus, ProcessingState, SourceHealth, Platform, Severity } from '@/lib/mock-data'

interface StatusBadgeProps {
  status: PipelineRunStatus | ProcessingState | SourceHealth | Severity
  className?: string
}

const statusConfig: Record<string, { label: string; className: string }> = {
  // Pipeline status
  completed: { label: 'Completed', className: 'bg-emerald-100 text-emerald-700 border-emerald-200' },
  partial_success: { label: 'Partial Success', className: 'bg-amber-100 text-amber-700 border-amber-200' },
  failed: { label: 'Failed', className: 'bg-red-100 text-red-700 border-red-200' },

  // Processing state
  success: { label: 'Success', className: 'bg-emerald-100 text-emerald-700 border-emerald-200' },
  extraction_failed: { label: 'Extraction Failed', className: 'bg-amber-100 text-amber-700 border-amber-200' },
  enrichment_failed: { label: 'Enrichment Failed', className: 'bg-amber-100 text-amber-700 border-amber-200' },
  requires_review: { label: 'Requires Review', className: 'bg-red-100 text-red-700 border-red-200' },
  manually_corrected: { label: 'Manually Corrected', className: 'bg-blue-100 text-blue-700 border-blue-200' },
  pending: { label: 'Pending', className: 'bg-slate-100 text-slate-600 border-slate-200' },

  // Source health
  healthy: { label: 'Healthy', className: 'bg-emerald-100 text-emerald-700 border-emerald-200' },
  warning: { label: 'Warning', className: 'bg-amber-100 text-amber-700 border-amber-200' },
  critical: { label: 'Critical', className: 'bg-red-100 text-red-700 border-red-200' },

  // Severity
  info: { label: 'Info', className: 'bg-blue-100 text-blue-700 border-blue-200' },
  error: { label: 'Error', className: 'bg-red-100 text-red-700 border-red-200' },
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = statusConfig[status] || { label: status, className: 'bg-slate-100 text-slate-600' }

  return (
    <Badge variant="outline" className={cn(config.className, className)}>
      {config.label}
    </Badge>
  )
}

interface PlatformBadgeProps {
  platform: Platform
  className?: string
}

const DEFAULT_PLATFORM_STYLE = 'bg-slate-100 text-slate-600 border-slate-200'

const platformConfig: Record<string, { label: string; className: string }> = {
  greenhouse: { label: 'Greenhouse', className: 'bg-teal-100 text-teal-700 border-teal-200' },
  lever: { label: 'Lever', className: 'bg-indigo-100 text-indigo-700 border-indigo-200' },
  ashby: { label: 'Ashby', className: 'bg-orange-100 text-orange-700 border-orange-200' },
  workday: { label: 'Workday', className: 'bg-sky-100 text-sky-700 border-sky-200' },
  oracle_hcm: { label: 'Oracle HCM', className: 'bg-red-100 text-red-700 border-red-200' },
  icims: { label: 'iCIMS', className: 'bg-fuchsia-100 text-fuchsia-700 border-fuchsia-200' },
  eightfold: { label: 'Eightfold', className: 'bg-cyan-100 text-cyan-700 border-cyan-200' },
  successfactors: { label: 'SuccessFactors', className: 'bg-blue-100 text-blue-700 border-blue-200' },
  workable: { label: 'Workable', className: 'bg-lime-100 text-lime-700 border-lime-200' },
  smartrecruiters: { label: 'SmartRecruiters', className: 'bg-pink-100 text-pink-700 border-pink-200' },
  bamboohr: { label: 'BambooHR', className: 'bg-emerald-100 text-emerald-700 border-emerald-200' },
  workatastartup: { label: 'Work at a Startup', className: 'bg-amber-100 text-amber-700 border-amber-200' },
  google_careers: { label: 'Google Careers', className: 'bg-blue-100 text-blue-700 border-blue-200' },
  amazon_jobs: { label: 'Amazon Jobs', className: 'bg-orange-100 text-orange-700 border-orange-200' },
  uber_careers: { label: 'Uber Careers', className: 'bg-zinc-100 text-zinc-700 border-zinc-200' },
}

function formatPlatformLabel(platform: string): string {
  return platform
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

export function PlatformBadge({ platform, className }: PlatformBadgeProps) {
  const config = platformConfig[platform] ?? {
    label: formatPlatformLabel(platform),
    className: DEFAULT_PLATFORM_STYLE,
  }

  return (
    <Badge variant="outline" className={cn(config.className, className)}>
      {config.label}
    </Badge>
  )
}

interface SeverityBadgeProps {
  severity: Severity
  className?: string
}

export function SeverityBadge({ severity, className }: SeverityBadgeProps) {
  const config = statusConfig[severity] || {
    label: severity,
    className: 'bg-slate-100 text-slate-600 border-slate-200',
  }

  return (
    <Badge variant="outline" className={cn(config.className, className)}>
      {config.label}
    </Badge>
  )
}
