"use client"

import { useMemo } from "react"
import { Search } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { FilterBar } from "@/components/filter-bar"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"
import { useJobsSearch } from "@/app/(dashboard)/jobs/layout"
import type { JobWithRole } from "@/lib/jobs-data"

function applyDateFilter(job: JobWithRole, value: string | null) {
  if (!value || value === "any") return true
  const ageHours = (Date.now() - new Date(job.posted_at).getTime()) / 3600000
  if (value === "24h") return ageHours <= 24
  if (value === "3d") return ageHours <= 72
  if (value === "1w") return ageHours <= 168
  return true
}

function matchesSearch(job: JobWithRole, q: string) {
  if (!q.trim()) return true
  const lower = q.toLowerCase()
  return job.title.toLowerCase().includes(lower) || job.company.toLowerCase().includes(lower)
}

export default function AllJobsPage() {
  const { jobs, hiddenIds, filters, loading, error } = useJobs()
  const { search } = useJobsSearch()

  const count = useMemo(() => {
    let list = jobs.filter((j) => !hiddenIds.has(j.id))
    if (filters.role) list = list.filter((j) => j.roleCategory === filters.role)
    if (filters.location) list = list.filter((j) => j.location.includes(filters.location as string))
    if (filters.remote && filters.remote !== "any")
      list = list.filter((j) => j.remote_type === filters.remote)
    if (filters.salaryMin != null)
      list = list.filter((j) => (j.salary_min ?? 0) >= (filters.salaryMin as number))
    list = list.filter((j) => applyDateFilter(j, filters.datePosted))
    list = list.filter((j) => matchesSearch(j, search))
    return list.length
  }, [jobs, hiddenIds, filters, search])

  return (
    <div>
      <FilterBar resultCount={count} />
      {error ? (
        <EmptyState
          icon={Search}
          title="Could not load jobs."
          description={error}
          ctaLabel="Set job filters →"
          ctaHref="/filters"
        />
      ) : !loading && count === 0 ? (
        <EmptyState
          icon={Search}
          title="No opportunities found."
          description="Update your filters to see matching jobs."
          ctaLabel="All Filters →"
          ctaHref="/filters"
        />
      ) : (
        <JobFeed jobs={jobs} useFilters loading={loading} />
      )}
    </div>
  )
}
