"use client"

import { useMemo } from "react"
import { Star } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { InfoBanner } from "@/components/info-banner"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"
import { useJobsSearch } from "@/app/(dashboard)/jobs/layout"
import type { JobWithRole } from "@/lib/jobs-data"

function matchesSearch(job: JobWithRole, q: string) {
  if (!q.trim()) return true
  const lower = q.toLowerCase()
  return job.title.toLowerCase().includes(lower) || job.company.toLowerCase().includes(lower)
}

export default function RecommendedPage() {
  const { recommendedJobs, hiddenIds, recommendedLoading, error } = useJobs()
  const { search } = useJobsSearch()

  const ranked = useMemo<JobWithRole[]>(() => {
    return recommendedJobs
      .filter((j) => !j.is_applied)
      .filter((j) => !hiddenIds.has(j.id))
      .filter((j) => matchesSearch(j, search))
  }, [recommendedJobs, hiddenIds, search])

  return (
    <div>
      <InfoBanner />
      {error ? (
        <EmptyState
          icon={Star}
          title="Could not load recommendations."
          description={error}
          ctaLabel="Try All Jobs →"
          ctaHref="/jobs/all"
        />
      ) : !recommendedLoading && ranked.length === 0 ? (
        <EmptyState
          icon={Star}
          title="No recommendations yet."
          description="Complete your profile and set role preferences to get personalized matches."
          ctaLabel="Set job filters →"
          ctaHref="/filters"
        />
      ) : (
        <JobFeed jobs={ranked} showMatch showRecommendation loading={recommendedLoading} />
      )}
    </div>
  )
}
