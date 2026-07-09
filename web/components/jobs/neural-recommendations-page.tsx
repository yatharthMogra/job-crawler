"use client"

import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { RefreshCw, Sparkles } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { NeuralJobCard } from "@/components/jobs/neural-job-card"
import { RecsFilterBar } from "@/components/jobs/recs-filter-bar"
import { RecommendationsFilterPanel } from "@/components/filters/recommendations-filter-panel"
import { JobDrawer } from "@/components/job-drawer"
import { FeedSkeleton } from "@/components/card-skeleton"
import { ResizeSplit } from "@/components/ui/resize-split"
import { Button } from "@/components/ui/button"
import { matchesEmploymentTypeFilter } from "@/lib/employment-type-filter"
import {
  applyDatePostedFilter,
  applyExperienceLevelFilter,
  applyLocationFilter,
  DEFAULT_LOCATION,
} from "@/lib/job-filters"
import { DEFAULT_SALARY_MAX } from "@/lib/filters/filter-options"
import { filterJobsByState } from "@/lib/filters/match-estimate"
import { filterJobsByCatalogRoles } from "@/lib/recommendation/neural-display"
import type { JobFiltersState } from "@/lib/profile/job-filters"
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

function countAdvancedFilters(state: JobFiltersState | null): number {
  if (!state) return 0
  let count = 0
  if (state.primaryRoles.length > 0) count += 1
  if (!state.openToAllSalary && state.minimumSalary) count += 1
  if (state.workModels.length > 0) count += 1
  if (state.experienceLevels.length > 0) count += 1
  if (state.sponsorshipRequired) count += 1
  if (state.fulltimeOnly || state.internshipOnly) count += 1
  return count
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
  const [filtersOpen, setFiltersOpen] = useState(false)
  const [advancedFilters, setAdvancedFilters] = useState<JobFiltersState | null>(null)
  const sentinelRef = useRef<HTMLDivElement>(null)
  const [scrollRoot, setScrollRoot] = useState<HTMLDivElement | null>(null)
  const onScrollRoot = useCallback((node: HTMLDivElement | null) => {
    setScrollRoot(node)
  }, [])
  const detailOpen = Boolean(selectedJobId)

  useEffect(() => {
    if (candidateId && !profileHome) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, profileHome, loadProfileHome])

  useEffect(() => {
    if (filters.location) return
    const fromProfile = profileHome?.preferences?.find((p) => p.label === "Locations")?.value
    const first = fromProfile && fromProfile !== "—" ? fromProfile.split(",")[0]?.trim() : null
    setFilter("location", first || DEFAULT_LOCATION)
  }, [filters.location, profileHome, setFilter])

  const primaryRoles = advancedFilters?.primaryRoles.length
    ? advancedFilters.primaryRoles
    : (profileHome?.primaryRoles ?? [])
  const secondaryRoles = profileHome?.secondaryRoles ?? []

  const ranked = useMemo<JobWithRole[]>(() => {
    let base = recommendedJobs
      .filter((j) => !j.is_applied)
      .filter((j) => !hiddenIds.has(j.id))
      .filter((j) => matchesSearch(j, search))
      .filter((j) => matchesEmploymentTypeFilter(j.employment_type, filters.employmentType))
      .filter((j) => applyDatePostedFilter(j, filters.datePosted))
      .filter((j) => applyLocationFilter(j, filters.location))
      .filter((j) => applyExperienceLevelFilter(j, filters.experienceLevel))

    if (advancedFilters) {
      base = filterJobsByState(base, advancedFilters, DEFAULT_SALARY_MAX)
    }

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
    advancedFilters,
  ])

  const visible = ranked.slice(0, visibleCount)
  const hasMore = visibleCount < ranked.length
  const advancedFilterCount = countAdvancedFilters(advancedFilters)

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
    advancedFilters,
  ])

  useEffect(() => {
    if (recommendedLoading || !hasMore || !scrollRoot) return
    const sentinel = sentinelRef.current
    if (!sentinel) return

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0]?.isIntersecting) {
          setVisibleCount((c) => Math.min(c + BATCH, ranked.length))
        }
      },
      { root: scrollRoot, rootMargin: "240px" },
    )
    observer.observe(sentinel)
    return () => observer.disconnect()
  }, [recommendedLoading, hasMore, visible.length, detailOpen, ranked.length, scrollRoot])

  async function handleSync() {
    setSyncing(true)
    try {
      await refreshJobs()
    } finally {
      setSyncing(false)
    }
  }

  const jobList = (
    <div className="px-4 pb-8 pt-3 lg:px-6">
      {error ? (
        <div className="flex flex-col items-center justify-center px-6 py-24 text-center">
          <Sparkles className="mb-4 size-10 text-primary/60" />
          <h3 className="text-sm font-semibold text-foreground">Could not load recommendations</h3>
          <p className="mt-1 max-w-xs text-sm text-muted-foreground">{error}</p>
          <Button className="btn-brand mt-4" onClick={() => setFiltersOpen(true)}>
            Adjust filters
          </Button>
        </div>
      ) : recommendedLoading ? (
        <FeedSkeleton count={4} />
      ) : ranked.length === 0 ? (
        <div className="flex flex-col items-center justify-center px-6 py-24 text-center">
          <Sparkles className="mb-4 size-10 text-primary/60" />
          <h3 className="text-sm font-semibold text-foreground">No matches yet</h3>
          <p className="mt-1 max-w-xs text-sm text-muted-foreground">
            Set your primary roles and filters to unlock personalized recommendations.
          </p>
          <Button className="btn-brand mt-4" onClick={() => setFiltersOpen(true)}>
            Open filters
          </Button>
        </div>
      ) : (
        <div className="space-y-3">
          {visible.map((job) => (
            <NeuralJobCard key={job.id} job={job} compact={detailOpen} />
          ))}
          {hasMore ? <div ref={sentinelRef} className="h-8" aria-hidden="true" /> : null}
          <div className="flex flex-col items-center gap-3 pt-4">
            {hasMore ? (
              <Button
                variant="outline"
                className="h-10 rounded-xl px-5"
                onClick={() => setVisibleCount((c) => Math.min(c + BATCH, ranked.length))}
              >
                Load more ({visible.length} of {ranked.length})
              </Button>
            ) : (
              <p className="text-xs text-muted-foreground">You&apos;ve seen all {ranked.length} matches.</p>
            )}
            <Button
              variant="ghost"
              className="h-9 gap-2 rounded-xl px-4 text-muted-foreground"
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
  )

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
        <RecsFilterBar
          onOpenAllFilters={() => setFiltersOpen(true)}
          advancedFilterCount={advancedFilterCount}
        />
      </div>

      <ResizeSplit
        enabled={detailOpen}
        leftScrollRef={onScrollRoot}
        left={jobList}
        right={detailOpen ? <JobDrawer showMatch variant="inline" /> : null}
      />

      <div className="md:hidden">
        <JobDrawer showMatch variant="overlay" />
      </div>

      <RecommendationsFilterPanel
        open={filtersOpen}
        onClose={() => setFiltersOpen(false)}
        onApplied={(state) => setAdvancedFilters(state)}
      />
    </div>
  )
}
