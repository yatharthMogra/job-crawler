"use client"

import { useJobs } from "@/components/jobs-provider"
import { FilterDropdown, SalaryDropdown } from "@/components/filter-dropdown"
import { ROLE_OPTIONS } from "@/lib/jobs-data"

const ROLE_OPTS = ROLE_OPTIONS.map((r) => ({ value: r, label: r }))
const REMOTE_OPTS = [
  { value: "remote", label: "Remote" },
  { value: "hybrid", label: "Hybrid" },
  { value: "onsite", label: "Onsite" },
  { value: "any", label: "Any" },
]
const LOCATION_OPTS = [
  { value: "San Francisco", label: "San Francisco, CA" },
  { value: "New York", label: "New York, NY" },
  { value: "Seattle", label: "Seattle, WA" },
  { value: "Austin", label: "Austin, TX" },
  { value: "Boston", label: "Boston, MA" },
  { value: "Los Angeles", label: "Los Angeles, CA" },
  { value: "Remote", label: "Remote" },
]
const DATE_OPTS = [
  { value: "24h", label: "Last 24h" },
  { value: "3d", label: "Last 3 days" },
  { value: "1w", label: "Last week" },
  { value: "any", label: "Any time" },
]

export function FilterBar({ resultCount }: { resultCount: number }) {
  const { filters, setFilter, clearFilter } = useJobs()

  return (
    <div className="sticky top-0 z-20 border-b border-zinc-200 bg-zinc-50/90 backdrop-blur">
      <div className="flex flex-wrap items-center gap-2 px-6 py-3">
        <FilterDropdown
          label="Role"
          value={filters.role}
          options={ROLE_OPTS}
          onSelect={(v) => setFilter("role", v)}
          onClear={() => clearFilter("role")}
        />
        <FilterDropdown
          label="Location"
          value={filters.location}
          options={LOCATION_OPTS}
          onSelect={(v) => setFilter("location", v)}
          onClear={() => clearFilter("location")}
        />
        <FilterDropdown
          label="Remote"
          value={filters.remote}
          options={REMOTE_OPTS}
          onSelect={(v) => setFilter("remote", v)}
          onClear={() => clearFilter("remote")}
        />
        <SalaryDropdown
          value={filters.salaryMin}
          onSelect={(v) => setFilter("salaryMin", v)}
          onClear={() => clearFilter("salaryMin")}
        />
        <FilterDropdown
          label="Date Posted"
          value={filters.datePosted}
          options={DATE_OPTS}
          onSelect={(v) => setFilter("datePosted", v)}
          onClear={() => clearFilter("datePosted")}
        />
      </div>
      <p className="px-6 pb-2 text-xs text-zinc-400">
        {resultCount.toLocaleString()} {resultCount === 1 ? "opportunity" : "opportunities"}
      </p>
    </div>
  )
}
