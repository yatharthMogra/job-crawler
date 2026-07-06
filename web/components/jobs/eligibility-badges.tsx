import type { Job } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

interface EligibilityBadgesProps {
  job: Pick<Job, "requires_clearance" | "requires_citizenship">
  className?: string
}

export function EligibilityBadges({ job, className }: EligibilityBadgesProps) {
  if (!job.requires_clearance && !job.requires_citizenship) return null

  return (
    <div className={cn("flex flex-wrap items-center gap-2", className)}>
      {job.requires_clearance ? (
        <span className="rounded-full bg-amber-500/12 px-2.5 py-0.5 text-xs font-semibold text-amber-800">
          Clearance required
        </span>
      ) : null}
      {job.requires_citizenship ? (
        <span className="rounded-full bg-rose-500/12 px-2.5 py-0.5 text-xs font-semibold text-rose-800">
          US citizenship / no sponsorship
        </span>
      ) : null}
    </div>
  )
}
