"use client"

import { useMemo } from "react"
import { useJobs } from "@/components/jobs-provider"
import { ApplicationsPage } from "@/components/applications/applications-page"
import { FeedSkeleton } from "@/components/card-skeleton"
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

  const applications = useMemo(() => {
    return mergeAppliedJobs(appliedJobs, appliedIds, allKnownJobs)
      .filter((job) => matchesSearch(job, search))
      .sort(
        (a, b) => new Date(b.posted_at).getTime() - new Date(a.posted_at).getTime(),
      )
  }, [appliedJobs, appliedIds, allKnownJobs, search])

  if (loading) {
    return (
      <div className="px-4 py-6 lg:px-6">
        <FeedSkeleton count={4} />
      </div>
    )
  }

  return <ApplicationsPage applications={applications} />
}
