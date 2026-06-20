"use client"

import { useMemo } from "react"
import { Check } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"
import { useJobsSearch } from "@/app/(dashboard)/jobs/layout"
import type { JobWithRole } from "@/lib/jobs-data"

function matchesSearch(job: JobWithRole, q: string) {
  if (!q.trim()) return true
  const lower = q.toLowerCase()
  return job.title.toLowerCase().includes(lower) || job.company.toLowerCase().includes(lower)
}

function mergeAppliedJobs(
  appliedJobs: JobWithRole[],
  appliedIds: Set<string>,
  allKnownJobs: JobWithRole[],
): JobWithRole[] {
  const byId = new Map<string, JobWithRole>()
  for (const job of appliedJobs) {
    byId.set(job.id, { ...job, is_applied: true })
  }
  for (const job of allKnownJobs) {
    if (appliedIds.has(job.id) && !byId.has(job.id)) {
      byId.set(job.id, { ...job, is_applied: true })
    }
  }
  return [...byId.values()]
}

export default function AppliedPage() {
  const { appliedJobs, appliedIds, allKnownJobs, loading } = useJobs()
  const { search } = useJobsSearch()

  const applied = useMemo(() => {
    return mergeAppliedJobs(appliedJobs, appliedIds, allKnownJobs).filter((j) =>
      matchesSearch(j, search),
    )
  }, [appliedJobs, appliedIds, allKnownJobs, search])

  if (loading) {
    return null
  }

  if (applied.length === 0) {
    return (
      <EmptyState
        icon={Check}
        title="No applied jobs yet."
        description="Jobs you apply to will appear here."
      />
    )
  }

  return (
    <JobFeed
      jobs={applied}
      showMatch
      cardMode="applied"
      title="Applied Jobs"
      subtitle="Roles you've marked as applied."
    />
  )
}
