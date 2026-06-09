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
        <div className="size-3 shrink-0 rounded-full border-2 border-zinc-400 bg-white" />
        {!isLast ? <div className="mt-1 w-px flex-1 bg-zinc-200" /> : null}
      </div>
      <div className="min-w-0 flex-1 -mt-0.5">
        <p className="text-xs text-muted-foreground">{dateRange}</p>
        <p className="mt-1 text-sm font-semibold text-foreground">{title}</p>
        {subtitle ? <p className="text-sm text-foreground">{subtitle}</p> : null}
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
