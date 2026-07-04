"use client"

import { useJobs } from "@/components/jobs-provider"
import {
  DATE_POSTED_OPTIONS,
  DEFAULT_LOCATION,
  EXPERIENCE_LEVEL_OPTIONS,
} from "@/lib/job-filters"
import type { EmploymentTypeFilter } from "@/lib/employment-type-filter"
import type { SeniorityLevel } from "@/lib/jobs-data"

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

export function RecsFilterBar() {
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
      <CompactSelect
        ariaLabel="Experience level"
        value={filters.experienceLevel ?? "any"}
        onChange={(v) =>
          setFilter("experienceLevel", v === "any" ? null : (v as SeniorityLevel))
        }
        options={EXPERIENCE_LEVEL_OPTIONS.map((o) => ({
          value: o.value,
          label: o.label,
        }))}
      />
    </div>
  )
}
