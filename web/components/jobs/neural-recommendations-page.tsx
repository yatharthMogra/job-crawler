"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  BadgeCheck,
  Bell,
  ChevronRight,
  MessageCircle,
  RefreshCw,
  Search,
  Settings,
  SlidersHorizontal,
  Sparkles,
  TrendingUp,
} from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { NeuralJobCard } from "@/components/jobs/neural-job-card"
import { NeuralJobsSidebar } from "@/components/jobs/neural-jobs-sidebar"
import { FeedSkeleton } from "@/components/card-skeleton"
import { EmptyState } from "@/components/empty-state"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { matchesEmploymentTypeFilter } from "@/lib/employment-type-filter"
import {
  filterJobsByCatalogRoles,
  marketAlignmentPercent,
} from "@/lib/recommendation/neural-display"
import type { JobWithRole } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

const TOP_NAV = [
  { href: "/jobs/recommended", label: "Recommended Jobs" },
  { href: "/jobs/applied", label: "My Applications" },
  { href: "/profile", label: "Profile Intelligence" },
  { href: "/settings", label: "Career Coaching" },
]

const BATCH = 6

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
  const pathname = usePathname()
  const { candidateId, candidate } = useSession()
  const {
    recommendedJobs,
    hiddenIds,
    recommendedLoading,
    error,
    filters,
    appliedIds,
    refreshJobs,
  } = useJobs()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const [search, setSearch] = useState("")
  const [visibleCount, setVisibleCount] = useState(BATCH)
  const [syncing, setSyncing] = useState(false)
  const sentinelRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (candidateId && !profileHome) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, profileHome, loadProfileHome])

  const primaryRoles = profileHome?.primaryRoles ?? []
  const secondaryRoles = profileHome?.secondaryRoles ?? []

  const ranked = useMemo<JobWithRole[]>(() => {
    const base = recommendedJobs
      .filter((j) => !j.is_applied)
      .filter((j) => !hiddenIds.has(j.id))
      .filter((j) => matchesSearch(j, search))
      .filter((j) => matchesEmploymentTypeFilter(j.employment_type, filters.employmentType))

    const filtered = filterJobsByCatalogRoles(base, primaryRoles, secondaryRoles)
    return filtered.sort((a, b) => b.personal_score - a.personal_score)
  }, [recommendedJobs, hiddenIds, search, primaryRoles, secondaryRoles, filters.employmentType])

  const activeChips = useMemo(() => {
    const chips: string[] = [...primaryRoles.slice(0, 2)]
    if (secondaryRoles[0]) chips.push(secondaryRoles[0])
    const loc = profileHome?.preferences?.find((p) => p.label === "Locations")?.value
    if (loc && loc !== "—") chips.push(loc.split(",")[0]?.trim() ?? "")
    const remote = profileHome?.preferences?.find((p) => p.label === "Remote")?.value
    if (remote && remote !== "Flexible") chips.push(remote)
    return chips.filter(Boolean)
  }, [primaryRoles, secondaryRoles, profileHome])

  const topSkills = useMemo(() => {
    const counts = new Map<string, number>()
    for (const job of ranked.slice(0, 12)) {
      for (const skill of job.skills) {
        counts.set(skill, (counts.get(skill) ?? 0) + 1)
      }
    }
    return [...counts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4)
      .map(([skill]) => skill)
  }, [ranked])

  const visible = ranked.slice(0, visibleCount)
  const hasMore = visibleCount < ranked.length
  const alignment = marketAlignmentPercent(ranked)

  useEffect(() => {
    setVisibleCount(BATCH)
  }, [search, primaryRoles, secondaryRoles, filters.employmentType])

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

  const initials = (candidate?.name ?? "U")
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="flex min-h-full flex-col">
      <header className="sticky top-0 z-20 border-b border-border/60 bg-card/95 backdrop-blur-md">
        <div className="flex items-center justify-between gap-4 px-4 py-3 lg:px-6">
          <nav className="hidden items-center gap-1 md:flex">
            {TOP_NAV.map((item) => {
              const active = pathname === item.href || pathname.startsWith(`${item.href}/`)
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "relative px-3 py-2 text-sm font-medium transition-colors",
                    active ? "text-primary" : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  {item.label}
                  {active ? (
                    <span className="absolute inset-x-2 -bottom-px h-0.5 rounded-full bg-primary" />
                  ) : null}
                </Link>
              )
            })}
          </nav>

          <div className="relative mx-auto hidden w-full max-w-sm lg:block">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search executive roles..."
              className="h-9 border-border/60 bg-surface/50 pl-9 text-sm"
            />
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
              aria-label="Notifications"
            >
              <Bell className="size-4" />
            </button>
            <Link
              href="/settings"
              className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
              aria-label="Settings"
            >
              <Settings className="size-4" />
            </Link>
            <span className="flex size-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
              {initials}
            </span>
          </div>
        </div>
      </header>

      <div className="flex flex-1">
        <NeuralJobsSidebar />

        <div className="min-w-0 flex-1">
          <div className="px-4 py-6 lg:px-8">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                  Command <ChevronRight className="inline size-3" /> Neural Feed
                </p>
                <h1 className="mt-1 text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                  Recommended Roles
                </h1>
                <p className="mt-1 max-w-xl text-sm text-muted-foreground">
                  Synchronizing executive opportunities with your professional DNA.
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-700">
                  <BadgeCheck className="size-3.5" />
                  Verified Direct Listings
                </span>
                <Link href="/filters">
                  <Button variant="outline" size="sm" className="h-9 gap-1.5 rounded-full">
                    <SlidersHorizontal className="size-3.5" />
                    Intelligence Filters
                  </Button>
                </Link>
              </div>
            </div>

            <div className="mt-6 grid gap-4 md:grid-cols-3">
              <StatCard
                title="Market Alignment"
                value={ranked.length > 0 ? `Strong Match (${alignment}%)` : "Calibrating..."}
                detail={
                  ranked.length > 0
                    ? "SaaS infrastructure demand aligns with your target trajectory."
                    : "Complete role selection to activate neural matching."
                }
                progress={alignment}
              />
              <StatCard
                title="Applied Intelligence"
                value={`${appliedIds.size} Applications`}
                detail="Engine prioritizes roles matching your AWS & distributed systems profile."
                badge="Active"
              />
              <StatCard
                title="Asset Momentum"
                value={topSkills.length > 0 ? topSkills.join(" · ") : "Analyzing skills..."}
                detail={topSkills.length > 3 ? "+4 Insight" : "Trending in your match pool"}
                chips={topSkills}
              />
            </div>

            {activeChips.length > 0 ? (
              <div className="mt-6 rounded-2xl border border-border/60 bg-card/60 px-4 py-3">
                <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                  Active Matching
                </p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {activeChips.map((chip) => (
                    <span
                      key={chip}
                      className="rounded-full border border-primary/25 bg-primary/5 px-3 py-1 text-xs font-semibold text-primary"
                    >
                      {chip}
                    </span>
                  ))}
                </div>
              </div>
            ) : null}

            <div className="mt-8 space-y-5">
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
                  title="No neural matches yet"
                  description="Set your primary roles in Profile Intelligence to unlock catalog-precise recommendations."
                  ctaLabel="Define executive path"
                  ctaHref="/profile/job-intent"
                />
              ) : (
                <>
                  {visible.map((job, index) => (
                    <NeuralJobCard key={job.id} job={job} featured={index === 0} />
                  ))}
                  {hasMore ? <div ref={sentinelRef} className="h-8" aria-hidden="true" /> : null}
                </>
              )}
            </div>

            {!recommendedLoading && ranked.length > 0 ? (
              <div className="mt-8 flex justify-center pb-8">
                <Button
                  variant="outline"
                  className="h-11 gap-2 rounded-xl px-6"
                  disabled={syncing}
                  onClick={() => void handleSync()}
                >
                  <RefreshCw className={cn("size-4", syncing && "animate-spin")} />
                  {syncing ? "Synchronizing..." : "Synchronize More Recommendations"}
                </Button>
              </div>
            ) : null}
          </div>
        </div>
      </div>

      <button
        type="button"
        className="fixed bottom-6 right-6 z-40 flex size-14 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-xl shadow-primary/30 transition-transform hover:scale-105"
        aria-label="Neural assistant"
      >
        <MessageCircle className="size-6" />
        <span className="absolute -right-0.5 -top-0.5 flex size-5 items-center justify-center rounded-full bg-remove text-[10px] font-bold text-white">
          2
        </span>
      </button>
    </div>
  )
}

function StatCard({
  title,
  value,
  detail,
  progress,
  badge,
  chips,
}: {
  title: string
  value: string
  detail: string
  progress?: number
  badge?: string
  chips?: string[]
}) {
  return (
    <div className="rounded-2xl border border-border/80 bg-card p-4 shadow-sm">
      <div className="flex items-center justify-between gap-2">
        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          {title}
        </p>
        {badge ? (
          <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-bold text-emerald-700">
            {badge}
          </span>
        ) : (
          <TrendingUp className="size-3.5 text-primary" />
        )}
      </div>
      <p className="mt-2 text-sm font-bold text-foreground">{value}</p>
      {progress != null ? (
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-primary transition-all duration-700"
            style={{ width: `${progress}%` }}
          />
        </div>
      ) : null}
      {chips && chips.length > 0 ? (
        <div className="mt-2 flex flex-wrap gap-1">
          {chips.map((c) => (
            <span
              key={c}
              className="rounded-md bg-primary/10 px-1.5 py-0.5 text-[10px] font-semibold text-primary"
            >
              {c}
            </span>
          ))}
        </div>
      ) : null}
      <p className="mt-2 text-xs leading-relaxed text-muted-foreground">{detail}</p>
    </div>
  )
}
