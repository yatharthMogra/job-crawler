"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import Link from "next/link"
import { RefreshCw, Sparkles } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { NeuralJobCard } from "@/components/jobs/neural-job-card"
import { RecsFilterBar } from "@/components/jobs/recs-filter-bar"
import { JobDrawer } from "@/components/job-drawer"
import { FeedSkeleton } from "@/components/card-skeleton"
import { EmptyState } from "@/components/empty-state"
import { Button } from "@/components/ui/button"
import { matchesEmploymentTypeFilter } from "@/lib/employment-type-filter"
import {
  applyDatePostedFilter,
  applyExperienceLevelFilter,
  applyLocationFilter,
  DEFAULT_LOCATION,
} from "@/lib/job-filters"
import { filterJobsByCatalogRoles } from "@/lib/recommendation/neural-display"
import type { JobWithRole } from "@/lib/jobs-data"
import { useJobsSearch } from "@/app/(dashboard)/jobs/layout"
import { cn } from "@/lib/utils"

const BATCH = 8

function matchesSearch(job: JobWithRole, q: string) {
  if (!q.trim()) return true
  const lower = q.toLowerCase()
  return (
    job.title.toLowerCase().includes(lower) ||
    job.company.toLowerCase().includes(lower) ||
    job.skills.some((s) => s.toLowerCase().includes(lower))
  )
}

export function NeuralRecommendationsPage() {
  const { candidateId } = useSession()
  const {
    recommendedJobs,
    hiddenIds,
    recommendedLoading,
    error,
    filters,
    setFilter,
    refreshJobs,
    selectedJobId,
    selectJob,
  } = useJobs()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const { search } = useJobsSearch()
  const [visibleCount, setVisibleCount] = useState(BATCH)
  const [syncing, setSyncing] = useState(false)
  const sentinelRef = useRef<HTMLDivElement>(null)
  const detailOpen = Boolean(selectedJobId)

  useEffect(() => {
    if (candidateId && !profileHome) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, profileHome, loadProfileHome])

  // Seed location from profile; never leave null.
  useEffect(() => {
    if (filters.location) return
    const fromProfile = profileHome?.preferences?.find((p) => p.label === "Locations")?.value
    const first = fromProfile && fromProfile !== "—" ? fromProfile.split(",")[0]?.trim() : null
    setFilter("location", first || DEFAULT_LOCATION)
  }, [filters.location, profileHome, setFilter])

  const primaryRoles = profileHome?.primaryRoles ?? []
  const secondaryRoles = profileHome?.secondaryRoles ?? []

  const ranked = useMemo<JobWithRole[]>(() => {
    const base = recommendedJobs
      .filter((j) => !j.is_applied)
      .filter((j) => !hiddenIds.has(j.id))
      .filter((j) => matchesSearch(j, search))
      .filter((j) => matchesEmploymentTypeFilter(j.employment_type, filters.employmentType))
      .filter((j) => applyDatePostedFilter(j, filters.datePosted))
      .filter((j) => applyLocationFilter(j, filters.location))
      .filter((j) => applyExperienceLevelFilter(j, filters.experienceLevel))

    return filterJobsByCatalogRoles(base, primaryRoles, secondaryRoles).sort(
      (a, b) => b.personal_score - a.personal_score,
    )
  }, [
    recommendedJobs,
    hiddenIds,
    search,
    primaryRoles,
    secondaryRoles,
    filters.employmentType,
    filters.datePosted,
    filters.location,
    filters.experienceLevel,
  ])

  const visible = ranked.slice(0, visibleCount)
  const hasMore = visibleCount < ranked.length

  useEffect(() => {
    if (recommendedLoading || ranked.length === 0) return
    if (selectedJobId && ranked.some((j) => j.id === selectedJobId)) return
    if (typeof window !== "undefined" && window.matchMedia("(min-width: 768px)").matches) {
      selectJob(ranked[0]!.id)
    }
  }, [recommendedLoading, ranked, selectedJobId, selectJob])

  useEffect(() => {
    setVisibleCount(BATCH)
  }, [
    search,
    primaryRoles,
    secondaryRoles,
    filters.employmentType,
    filters.datePosted,
    filters.location,
    filters.experienceLevel,
  ])

  useEffect(() => {
    if (recommendedLoading || !hasMore) return
    const el = sentinelRef.current
    if (!el) return
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          setVisibleCount((c) => c + BATCH)
        }
      },
      { rootMargin: "240px" },
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [recommendedLoading, hasMore, visible.length])

  async function handleSync() {
    setSyncing(true)
    try {
      await refreshJobs()
    } finally {
      setSyncing(false)
    }
  }

  return (
    <div className="flex h-[calc(100vh-3.5rem)] min-h-0 flex-col">
      <div className="flex shrink-0 flex-wrap items-center justify-between gap-3 border-b border-border/50 px-4 py-3 lg:px-6">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-lg font-bold tracking-tight text-foreground">Recommended roles</h1>
            {process.env.NODE_ENV === "development" ? (
              <span className="rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-primary">
                Live preview
              </span>
            ) : null}
          </div>
          <p className="text-sm text-muted-foreground">
            {recommendedLoading ? "Loading…" : `${ranked.length} matches`}
          </p>
        </div>
        <RecsFilterBar />
      </div>

      <div className="flex min-h-0 flex-1">
        <div
          className={cn(
            "min-w-0 overflow-y-auto px-4 pb-8 lg:px-6",
            detailOpen ? "min-w-[360px] flex-[5] border-r border-border/50 bg-muted/[0.18]" : "flex-1",
          )}
        >
          {error ? (
            <EmptyState
              icon={Sparkles}
              title="Could not load recommendations"
              description={error}
              ctaLabel="Open filters"
              ctaHref="/filters"
            />
          ) : recommendedLoading ? (
            <FeedSkeleton count={4} />
          ) : ranked.length === 0 ? (
            <EmptyState
              icon={Sparkles}
              title="No matches yet"
              description="Set your primary roles and filters to unlock personalized recommendations."
              ctaLabel="Define target roles"
              ctaHref="/profile/job-intent"
            />
          ) : (
            <div className="space-y-3">
              {visible.map((job) => (
                <NeuralJobCard key={job.id} job={job} compact={detailOpen} />
              ))}
              {hasMore ? <div ref={sentinelRef} className="h-8" aria-hidden="true" /> : null}
              <div className="flex justify-center pt-4">
                <Button
                  variant="outline"
                  className="h-10 gap-2 rounded-xl px-5"
                  disabled={syncing}
                  onClick={() => void handleSync()}
                >
                  <RefreshCw className={cn("size-4", syncing && "animate-spin")} />
                  {syncing ? "Refreshing..." : "Refresh recommendations"}
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Desktop: in-flow detail — list shrinks, panel does not overlay */}
        {detailOpen ? (
          <JobDrawer showMatch variant="inline" />
        ) : null}
      </div>

      {/* Mobile: overlay drawer only */}
      <div className="md:hidden">
        <JobDrawer showMatch variant="overlay" />
      </div>
    </div>
  )
}
