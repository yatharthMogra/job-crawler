'use client'

import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { formatRelativeTime, formatAbsoluteTime } from '@/lib/dashboard-utils'

interface RelativeTimeProps {
  date: Date | string | null
  className?: string
}

export function RelativeTime({ date, className }: RelativeTimeProps) {
  if (!date) return <span className={className}>Never</span>
  
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <span className={className}>{formatRelativeTime(date)}</span>
        </TooltipTrigger>
        <TooltipContent>
          <p>{formatAbsoluteTime(date)}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
