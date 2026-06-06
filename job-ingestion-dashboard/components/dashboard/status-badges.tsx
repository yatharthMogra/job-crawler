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
  warning: { label: 'Warning', className: 'bg-amber-100 text-amber-700 border-amber-200' },
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

const platformConfig: Record<Platform, { label: string; className: string }> = {
  greenhouse: { label: 'Greenhouse', className: 'bg-teal-100 text-teal-700 border-teal-200' },
  lever: { label: 'Lever', className: 'bg-indigo-100 text-indigo-700 border-indigo-200' },
  ashby: { label: 'Ashby', className: 'bg-orange-100 text-orange-700 border-orange-200' },
}

export function PlatformBadge({ platform, className }: PlatformBadgeProps) {
  const config = platformConfig[platform]
  
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
  const config = statusConfig[severity]
  
  return (
    <Badge variant="outline" className={cn(config.className, className)}>
      {config.label}
    </Badge>
  )
}
