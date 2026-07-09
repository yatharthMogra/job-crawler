"use client"

import { SlidersHorizontal } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import {
  DATE_POSTED_OPTIONS,
  DEFAULT_LOCATION,
} from "@/lib/job-filters"
import type { EmploymentTypeFilter } from "@/lib/employment-type-filter"
import { cn } from "@/lib/utils"

const LOCATION_OPTIONS = [
  DEFAULT_LOCATION,
  "Remote (US)",
  "New York, NY",
  "San Francisco, CA",
  "Seattle, WA",
  "Austin, TX",
  "Boston, MA",
]

const EMPLOYMENT_OPTIONS: { value: EmploymentTypeFilter; label: string }[] = [
  { value: null, label: "Any type" },
  { value: "FULLTIME", label: "Full-time" },
  { value: "PARTTIME", label: "Part-time" },
  { value: "INTERNSHIP", label: "Internship" },
]

function CompactSelect({
  value,
  onChange,
  options,
  ariaLabel,
}: {
  value: string
  onChange: (v: string) => void
  options: { value: string; label: string }[]
  ariaLabel: string
}) {
  return (
    <select
      aria-label={ariaLabel}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="h-8 min-w-0 flex-1 rounded-md border border-border/70 bg-background px-2 text-sm text-foreground outline-none focus:border-primary/40 sm:max-w-[11rem]"
    >
      {options.map((opt) => (
        <option key={opt.value || "any"} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  )
}

export function RecsFilterBar({
  onOpenAllFilters,
  advancedFilterCount = 0,
}: {
  onOpenAllFilters?: () => void
  advancedFilterCount?: number
}) {
  const { filters, setFilter, setEmploymentTypeFilter } = useJobs()

  return (
    <div className="flex flex-wrap items-center gap-2">
      <CompactSelect
        ariaLabel="Location"
        value={filters.location ?? DEFAULT_LOCATION}
        onChange={(v) => setFilter("location", v || DEFAULT_LOCATION)}
        options={LOCATION_OPTIONS.map((l) => ({ value: l, label: l }))}
      />
      <CompactSelect
        ariaLabel="Employment type"
        value={filters.employmentType ?? ""}
        onChange={(v) => setEmploymentTypeFilter((v || null) as EmploymentTypeFilter)}
        options={EMPLOYMENT_OPTIONS.map((o) => ({
          value: o.value ?? "",
          label: o.label,
        }))}
      />
      <CompactSelect
        ariaLabel="Date posted"
        value={filters.datePosted ?? "any"}
        onChange={(v) => setFilter("datePosted", v === "any" ? null : v)}
        options={DATE_POSTED_OPTIONS.map((o) => ({ value: o.value, label: o.label }))}
      />
      {onOpenAllFilters ? (
        <button
          type="button"
          onClick={onOpenAllFilters}
          className={cn(
            "inline-flex h-8 items-center gap-1.5 rounded-md border px-3 text-sm font-medium transition-colors",
            advancedFilterCount > 0
              ? "border-primary/40 bg-primary/5 text-primary"
              : "border-border/70 bg-background text-foreground hover:border-primary/30",
          )}
        >
          <SlidersHorizontal className="size-3.5" />
          All filters
          {advancedFilterCount > 0 ? (
            <span className="rounded-full bg-primary px-1.5 py-0.5 text-[10px] font-bold text-primary-foreground">
              {advancedFilterCount}
            </span>
          ) : null}
        </button>
      ) : null}
    </div>
  )
}
