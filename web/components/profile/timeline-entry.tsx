"use client"

import { cn } from "@/lib/utils"

interface TimelineEntryProps {
  dateRange: string
  title: string
  subtitle?: string
  detail?: string
  bullets?: string[]
  isLast?: boolean
  className?: string
}

export function TimelineEntry({
  dateRange,
  title,
  subtitle,
  detail,
  bullets,
  isLast,
  className,
}: TimelineEntryProps) {
  return (
    <div className={cn("relative flex gap-4 pb-8", className)}>
      <div className="flex flex-col items-center">
        <div className="size-3 shrink-0 rounded-full border-2 border-primary bg-card shadow-sm shadow-primary/20" />
        {!isLast ? <div className="mt-1 w-px flex-1 bg-gradient-to-b from-primary/40 to-border" /> : null}
      </div>
      <div className="min-w-0 flex-1 -mt-0.5 rounded-xl bg-surface/60 p-4">
        <p className="text-xs font-medium text-primary">{dateRange}</p>
        <p className="mt-1 text-sm font-semibold text-foreground">{title}</p>
        {subtitle ? <p className="text-sm text-muted-foreground">{subtitle}</p> : null}
        {detail ? <p className="mt-1 text-sm text-muted-foreground">{detail}</p> : null}
        {bullets && bullets.length > 0 ? (
          <ul className="mt-2 list-disc space-y-1 pl-4 text-sm text-muted-foreground">
            {bullets.map((b) => (
              <li key={b}>{b}</li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  )
}
