"use client"

import { ArrowRight } from "lucide-react"
import { cn } from "@/lib/utils"

interface FiltersMatchPanelProps {
  matchCount: number
  candidateName: string
  saving: boolean
  onViewMatches: () => void
  className?: string
}

export function FiltersMatchPanel({
  matchCount,
  candidateName,
  saving,
  onViewMatches,
  className,
}: FiltersMatchPanelProps) {
  const formattedCount = matchCount.toLocaleString()

  return (
    <aside className={cn("w-full shrink-0 space-y-4 xl:w-[280px]", className)}>
      <div className="rounded-xl border border-border/70 bg-card p-5">
        <p className="text-sm font-medium text-muted-foreground">Matching roles</p>
        <p className="mt-2 text-3xl font-bold tabular-nums text-foreground">{formattedCount}</p>
        <p className="mt-1 text-sm text-muted-foreground">based on your current filters</p>
      </div>

      <button
        type="button"
        onClick={onViewMatches}
        disabled={saving}
        className="btn-brand flex w-full items-center justify-center gap-2 rounded-xl py-3 text-sm font-semibold disabled:opacity-60"
      >
        {saving ? "Saving…" : `View ${formattedCount} matches`}
        {!saving ? <ArrowRight className="size-4" /> : null}
      </button>
      <p className="text-center text-xs text-muted-foreground">Filters for {candidateName}</p>
    </aside>
  )
}
