"use client"

import { useMemo } from "react"
import { Star } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { InfoBanner } from "@/components/info-banner"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"
import type { JobWithRole } from "@/lib/jobs-data"

export default function RecommendedPage() {
  const { recommendedJobs, hiddenIds, recommendedLoading, error } = useJobs()

  const ranked = useMemo<JobWithRole[]>(() => {
    return recommendedJobs.filter((j) => !hiddenIds.has(j.id))
  }, [recommendedJobs, hiddenIds])

  return (
    <div>
      <div className="sticky top-0 z-20 border-b border-zinc-200 bg-zinc-50/90 px-6 py-3 backdrop-blur">
        <h1 className="text-sm font-semibold text-zinc-900">Recommended for you</h1>
        <p className="text-xs text-zinc-400">
          {recommendedLoading ? "Loading..." : `${ranked.length.toLocaleString()} opportunities`}
        </p>
      </div>
      <InfoBanner />
      {error ? (
        <EmptyState
          icon={Star}
          title="Could not load recommendations."
          description={error}
          ctaLabel="Try All Jobs →"
          ctaHref="/jobs"
        />
      ) : !recommendedLoading && ranked.length === 0 ? (
        <EmptyState
          icon={Star}
          title="No recommendations yet."
          description="Complete your profile and set role preferences to get personalized matches."
          ctaLabel="Complete profile →"
          ctaHref="/profile/upload"
        />
      ) : (
        <JobFeed
          jobs={ranked}
          showMatch
          showRecommendation
          loading={recommendedLoading}
        />
      )}
    </div>
  )
}
