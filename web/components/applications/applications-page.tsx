"use client"

import { useMemo, useState } from "react"
import { CalendarDays, Check, SlidersHorizontal } from "lucide-react"
import Link from "next/link"
import { ApplicationInsightsPanel } from "@/components/applications/application-insights-panel"
import { ApplicationListCard } from "@/components/applications/application-list-card"
import { ApplicationStatusBar } from "@/components/applications/application-status-bar"
import { EmptyState } from "@/components/empty-state"
import { useJobs } from "@/components/jobs-provider"
import {
  toApplicationRecord,
  type ApplicationStatusFilter,
} from "@/lib/applications/pipeline-status"
import type { JobWithRole } from "@/lib/jobs-data"

interface ApplicationsPageProps {
  applications: JobWithRole[]
}

export function ApplicationsPage({ applications }: ApplicationsPageProps) {
  const { unmarkApplied } = useJobs()
  const [statusFilter, setStatusFilter] = useState<ApplicationStatusFilter>("all")

  const records = useMemo(
    () => applications.map((job) => toApplicationRecord(job)),
    [applications],
  )

  const filtered = useMemo(() => {
    if (statusFilter === "all") return records
    return records.filter((record) => record.status === statusFilter)
  }, [records, statusFilter])

  const layout = (
    <div className="mx-auto flex w-full max-w-[1400px] flex-col gap-6 px-4 py-6 lg:flex-row lg:items-start lg:gap-8 lg:px-8 lg:py-8">
      <div className="min-w-0 flex-1">
        {records.length === 0 ? (
          <EmptyState
            icon={Check}
            title="No applications yet"
            description="When you apply to roles, they'll show up here so you can track progress."
            ctaLabel="Browse recommended jobs"
            ctaHref="/jobs/recommended"
          />
        ) : (
          <>
            <header className="mb-6 flex flex-wrap items-end justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold tracking-tight text-foreground">Applications</h1>
                <p className="mt-1.5 text-sm text-muted-foreground">
                  {records.length} {records.length === 1 ? "role" : "roles"} in your pipeline
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  className="inline-flex h-9 items-center gap-2 rounded-lg border border-border/70 bg-card px-3.5 text-sm font-semibold text-foreground/80 shadow-sm transition-colors hover:bg-muted/40"
                >
                  <SlidersHorizontal className="size-4 text-muted-foreground" />
                  Filter
                </button>
                <button
                  type="button"
                  className="inline-flex h-9 items-center gap-2 rounded-lg border border-border/70 bg-card px-3.5 text-sm font-semibold text-foreground/80 shadow-sm transition-colors hover:bg-muted/40"
                >
                  <CalendarDays className="size-4 text-muted-foreground" />
                  Date
                </button>
              </div>
            </header>

            <ApplicationStatusBar
              records={records}
              active={statusFilter}
              onChange={setStatusFilter}
            />

            <section className="mt-8">
              <div className="mb-4 flex items-center justify-between gap-3">
                <h2 className="text-base font-bold text-foreground">Recent activity</h2>
                {statusFilter !== "all" ? (
                  <button
                    type="button"
                    onClick={() => setStatusFilter("all")}
                    className="text-sm font-semibold text-primary hover:underline"
                  >
                    Clear filter
                  </button>
                ) : (
                  <Link
                    href="/jobs/recommended"
                    className="text-sm font-semibold text-primary hover:underline"
                  >
                    Find more roles
                  </Link>
                )}
              </div>

              {filtered.length === 0 ? (
                <div className="rounded-2xl border border-border/60 bg-card px-6 py-16 text-center shadow-sm">
                  <p className="text-sm text-muted-foreground">
                    No applications match this stage yet.
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {filtered.map((record) => (
                    <ApplicationListCard
                      key={record.job.id}
                      record={record}
                      onWithdraw={() => unmarkApplied(record.job.id)}
                    />
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </div>

      <ApplicationInsightsPanel records={records} className="lg:sticky lg:top-24" />
    </div>
  )

  return <div className="min-h-full bg-muted/20">{layout}</div>
}
