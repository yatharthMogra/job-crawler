"use client"

import { useJobs } from "@/components/jobs-provider"
import { NeuralJobCard } from "@/components/jobs/neural-job-card"
import { JobDrawer } from "@/components/job-drawer"
import type { JobWithRole } from "@/lib/jobs-data"
import type { LucideIcon } from "lucide-react"
import type { JobFeedKind } from "@/lib/job-feed"
import { EmptyState } from "@/components/empty-state"
import { cn } from "@/lib/utils"

export function JobsSplitFeed({
  jobs,
  showMatch = false,
  emptyIcon,
  emptyTitle,
  emptyDescription,
  emptyCtaLabel,
  emptyCtaHref,
  title,
  subtitle,
  feed = "recommended",
}: {
  jobs: JobWithRole[]
  showMatch?: boolean
  feed?: JobFeedKind
  emptyIcon: LucideIcon
  emptyTitle: string
  emptyDescription: string
  emptyCtaLabel?: string
  emptyCtaHref?: string
  title: string
  subtitle?: string
}) {
  const { selectedJobId } = useJobs()
  const detailOpen = Boolean(selectedJobId)

  if (jobs.length === 0) {
    return (
      <div className="px-4 py-8 lg:px-6">
        <EmptyState
          icon={emptyIcon}
          title={emptyTitle}
          description={emptyDescription}
          ctaLabel={emptyCtaLabel}
          ctaHref={emptyCtaHref}
        />
      </div>
    )
  }

  return (
    <div className="flex h-[calc(100vh-3.5rem)] min-h-0 flex-col">
      <div className="shrink-0 px-4 pt-5 lg:px-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">{title}</h1>
        {subtitle ? <p className="mt-1 text-sm text-muted-foreground">{subtitle}</p> : null}
      </div>

      <div className="mt-4 flex min-h-0 flex-1">
        <div
          className={cn(
            "space-y-3 overflow-y-auto px-4 pb-8 lg:px-6",
            detailOpen
              ? "min-w-[360px] flex-[5] border-r border-border/50 bg-muted/[0.18]"
              : "min-w-0 flex-1",
          )}
        >
          {jobs.map((job) => (
            <NeuralJobCard key={job.id} job={job} compact={detailOpen} feed={feed} />
          ))}
        </div>
        {detailOpen ? <JobDrawer showMatch={showMatch} variant="inline" feed={feed} /> : null}
      </div>

      <div className="md:hidden">
        <JobDrawer showMatch={showMatch} variant="overlay" feed={feed} />
      </div>
    </div>
  )
}
