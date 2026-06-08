"use client"

import { useMemo } from "react"
import { Search } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { FilterBar } from "@/components/filter-bar"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"
import type { JobWithRole } from "@/lib/jobs-data"

function applyDateFilter(job: JobWithRole, value: string | null) {
  if (!value || value === "any") return true
  const ageHours = (Date.now() - new Date(job.posted_at).getTime()) / 3600000
  if (value === "24h") return ageHours <= 24
  if (value === "3d") return ageHours <= 72
  if (value === "1w") return ageHours <= 168
  return true
}

export default function AllJobsPage() {
  const { jobs, hiddenIds, filters, loading, error } = useJobs()

  const count = useMemo(() => {
    let list = jobs.filter((j) => !hiddenIds.has(j.id))
    if (filters.role) list = list.filter((j) => j.roleCategory === filters.role)
    if (filters.location) list = list.filter((j) => j.location.includes(filters.location as string))
    if (filters.remote && filters.remote !== "any") list = list.filter((j) => j.remote_type === filters.remote)
    if (filters.salaryMin != null) list = list.filter((j) => (j.salary_min ?? 0) >= (filters.salaryMin as number))
    list = list.filter((j) => applyDateFilter(j, filters.datePosted))
    return list.length
  }, [jobs, hiddenIds, filters])

  return (
    <div>
      <FilterBar resultCount={count} />
      {error ? (
        <EmptyState
          icon={Search}
          title="Could not load jobs."
          description={error}
          ctaLabel="Go to Preferences →"
          ctaHref="/preferences"
        />
      ) : !loading && count === 0 ? (
        <EmptyState
          icon={Search}
          title="No opportunities found."
          description="Update your role preferences in Preferences to see matching jobs."
          ctaLabel="Go to Preferences →"
          ctaHref="/preferences"
        />
      ) : (
        <JobFeed jobs={jobs} useFilters loading={loading} />
      )}
    </div>
  )
}
