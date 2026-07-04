"use client"

import {
  countByStatus,
  type ApplicationRecord,
  type ApplicationStatusFilter,
} from "@/lib/applications/pipeline-status"
import { cn } from "@/lib/utils"

const FILTERS: { id: ApplicationStatusFilter; label: string }[] = [
  { id: "all", label: "Active" },
  { id: "under_review", label: "Under review" },
  { id: "interview", label: "Interviews" },
  { id: "submitted", label: "Applied" },
]

export function ApplicationStatusBar({
  records,
  active,
  onChange,
}: {
  records: ApplicationRecord[]
  active: ApplicationStatusFilter
  onChange: (filter: ApplicationStatusFilter) => void
}) {
  const counts = countByStatus(records)

  return (
    <div className="flex flex-wrap gap-2">
      {FILTERS.map((filter) => {
        const count =
          filter.id === "all" ? counts.all : counts[filter.id as keyof typeof counts]
        const selected = active === filter.id
        return (
          <button
            key={filter.id}
            type="button"
            onClick={() => onChange(filter.id)}
            className={cn(
              "inline-flex min-w-[120px] flex-1 items-center justify-between gap-3 rounded-xl border px-4 py-3 text-left transition-all sm:min-w-0 sm:flex-none",
              selected
                ? "border-slate-900 bg-slate-900 text-white shadow-md"
                : "border-border/70 bg-card text-foreground shadow-sm hover:border-primary/25 hover:bg-muted/30",
            )}
          >
            <span className="text-sm font-semibold">{filter.label}</span>
            <span
              className={cn(
                "text-xl font-bold tabular-nums leading-none",
                selected
                  ? "text-white"
                  : filter.id === "interview" && count > 0
                    ? "text-primary"
                    : "text-foreground",
              )}
            >
              {count}
            </span>
          </button>
        )
      })}
    </div>
  )
}
