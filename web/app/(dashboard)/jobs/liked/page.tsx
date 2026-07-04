"use client"

import { useMemo } from "react"
import { Bookmark } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { JobsSplitFeed } from "@/components/jobs/jobs-split-feed"
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
      allKnownJobs.filter((j) => savedIds.has(j.id)).filter((j) => matchesSearch(j, search)),
    [allKnownJobs, savedIds, search],
  )

  return (
    <JobsSplitFeed
      jobs={saved}
      emptyIcon={Bookmark}
      emptyTitle="No saved jobs yet"
      emptyDescription="Save jobs from recommendations to review them later."
      emptyCtaLabel="Browse jobs"
      emptyCtaHref="/jobs/recommended"
      title="Saved jobs"
      subtitle="Roles you bookmarked for later."
      feed="saved"
    />
  )
}
