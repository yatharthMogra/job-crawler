"use client"

import { useMemo } from "react"
import { Bookmark } from "lucide-react"
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

export default function LikedPage() {
  const { allKnownJobs, savedIds } = useJobs()
  const { search } = useJobsSearch()

  const saved = useMemo(
    () =>
      allKnownJobs
        .filter((j) => savedIds.has(j.id))
        .filter((j) => matchesSearch(j, search)),
    [allKnownJobs, savedIds, search],
  )

  if (saved.length === 0) {
    return (
      <EmptyState
        icon={Bookmark}
        title="No liked jobs yet."
        description="Save jobs from the feed to review them later."
        ctaLabel="Browse jobs →"
        ctaHref="/jobs/recommended"
      />
    )
  }

  return <JobFeed jobs={saved} />
}
