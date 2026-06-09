"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import { useJobs } from "@/components/jobs-provider"
import { JobCard } from "@/components/job-card"
import { FeedSkeleton } from "@/components/card-skeleton"
import type { JobWithRole } from "@/lib/jobs-data"

const BATCH = 8

function applyDateFilter(job: JobWithRole, value: string | null) {
  if (!value || value === "any") return true
  const ageHours = (Date.now() - new Date(job.posted_at).getTime()) / 3600000
  if (value === "24h") return ageHours <= 24
  if (value === "3d") return ageHours <= 72
  if (value === "1w") return ageHours <= 168
  return true
}

interface JobFeedProps {
  jobs: JobWithRole[]
  showMatch?: boolean
  showRecommendation?: boolean
  useFilters?: boolean
  loading?: boolean
}

export function JobFeed({
  jobs,
  showMatch = false,
  showRecommendation = false,
  useFilters = false,
  loading: externalLoading,
}: JobFeedProps) {
  const { hiddenIds, filters, loading: contextLoading } = useJobs()
  const [initialLoading, setInitialLoading] = useState(true)
  const apiLoading = externalLoading ?? (useFilters ? contextLoading : false)
  const [visibleCount, setVisibleCount] = useState(BATCH)
  const [loadingMore, setLoadingMore] = useState(false)
  const sentinelRef = useRef<HTMLDivElement>(null)

  const filtered = useMemo(() => {
    let list = jobs.filter((j) => !hiddenIds.has(j.id))
    if (useFilters) {
      if (filters.role) list = list.filter((j) => j.roleCategory === filters.role)
      if (filters.location) list = list.filter((j) => j.location.includes(filters.location as string))
      if (filters.remote && filters.remote !== "any") list = list.filter((j) => j.remote_type === filters.remote)
      if (filters.salaryMin != null) list = list.filter((j) => (j.salary_min ?? 0) >= (filters.salaryMin as number))
      list = list.filter((j) => applyDateFilter(j, filters.datePosted))
    }
    return list
  }, [jobs, hiddenIds, filters, useFilters])

  useEffect(() => {
    setVisibleCount(BATCH)
    if (apiLoading) {
      setInitialLoading(true)
      return
    }
    setInitialLoading(true)
    const t = setTimeout(() => setInitialLoading(false), 300)
    return () => clearTimeout(t)
  }, [filters, useFilters, apiLoading])

  const visible = filtered.slice(0, visibleCount)
  const hasMore = visibleCount < filtered.length

  useEffect(() => {
    if (initialLoading || !hasMore) return
    const el = sentinelRef.current
    if (!el) return
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !loadingMore) {
          setLoadingMore(true)
          setTimeout(() => {
            setVisibleCount((c) => c + BATCH)
            setLoadingMore(false)
          }, 600)
        }
      },
      { rootMargin: "200px" },
    )
    observer.observe(el)
    return () => observer.disconnect()
  }, [initialLoading, hasMore, loadingMore])

  if (initialLoading) {
    return (
      <div className="px-6 py-4">
        <FeedSkeleton count={5} />
      </div>
    )
  }

  return (
    <div className="px-6 py-5">
      <div className="flex flex-col gap-5">
        {visible.map((job) => (
          <JobCard key={job.id} job={job} showMatch={showMatch} showRecommendation={showRecommendation} />
        ))}
      </div>

      {hasMore && (
        <div ref={sentinelRef} className="flex justify-center py-8">
          <div className="flex gap-1.5" aria-label="Loading more jobs">
            <span className="size-1.5 animate-bounce rounded-full bg-primary/40 [animation-delay:-0.3s]" />
            <span className="size-1.5 animate-bounce rounded-full bg-brand/50 [animation-delay:-0.15s]" />
            <span className="size-1.5 animate-bounce rounded-full bg-primary/40" />
          </div>
        </div>
      )}

      {!hasMore && filtered.length > 0 && (
        <p className="py-8 text-center text-xs text-muted-foreground">You&apos;ve seen all available opportunities.</p>
      )}
    </div>
  )
}
