"use client"

import { ChevronDown, ExternalLink } from "lucide-react"
import { CompanyLogo } from "@/components/company-logo"
import {
  CARD_STATUS_OPTIONS,
  formatAppliedDate,
  PIPELINE_STATUS_LABELS,
  PIPELINE_STATUS_STYLES,
  type ApplicationPipelineStatus,
  type ApplicationRecord,
} from "@/lib/applications/pipeline-status"
import { REMOTE_LABEL } from "@/lib/job-meta"
import { cn } from "@/lib/utils"

export function ApplicationListCard({
  record,
  onStatusChange,
}: {
  record: ApplicationRecord
  onStatusChange: (status: ApplicationPipelineStatus) => void
}) {
  const { job, status, appliedAt } = record
  const statusStyle = PIPELINE_STATUS_STYLES[status]
  const remoteLabel = REMOTE_LABEL[job.remote_type as keyof typeof REMOTE_LABEL]

  return (
    <article className="overflow-hidden rounded-2xl border border-border/60 bg-card shadow-sm transition-shadow hover:shadow-md">
      <div className="flex flex-col gap-4 p-5 xl:flex-row xl:items-center xl:justify-between">
        <div className="flex min-w-0 flex-1 gap-4">
          <CompanyLogo
            company={job.company}
            size={56}
            shape="square"
            logoUrl={job.company_info?.logo_url}
            website={job.company_info?.website}
            className="shrink-0 rounded-xl"
          />
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <h3 className="text-lg font-bold tracking-tight text-foreground">{job.title}</h3>
              <span
                className={cn(
                  "shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide",
                  statusStyle.badge,
                )}
              >
                {PIPELINE_STATUS_LABELS[status]}
              </span>
            </div>
            <p className="mt-1 text-sm text-muted-foreground">
              {job.company} · {job.location}
              {remoteLabel ? <span> · {remoteLabel}</span> : null}
            </p>
            <p className="mt-2 text-xs font-medium text-muted-foreground">
              Applied on {formatAppliedDate(appliedAt)}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 flex-col gap-2 sm:flex-row sm:items-center xl:pl-4">
          <a
            href={job.posting_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex h-10 min-w-[132px] flex-1 items-center justify-center gap-1.5 rounded-xl bg-slate-900 px-4 text-sm font-semibold text-white transition-opacity hover:opacity-90 xl:flex-none"
          >
            View posting
            <ExternalLink className="size-3.5" />
          </a>
          <label className="relative inline-flex h-10 min-w-[180px] flex-1 xl:flex-none">
            <span className="sr-only">Application stage</span>
            <select
              value={status}
              onChange={(event) =>
                onStatusChange(event.target.value as ApplicationPipelineStatus)
              }
              className={cn(
                "h-full w-full appearance-none rounded-xl border border-border/70 bg-card pl-3.5 pr-9 text-sm font-semibold text-foreground shadow-sm transition-colors hover:bg-muted/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/30",
                statusStyle.badge,
              )}
            >
              {CARD_STATUS_OPTIONS.map((option) => (
                <option key={option} value={option}>
                  {PIPELINE_STATUS_LABELS[option]}
                </option>
              ))}
            </select>
            <ChevronDown
              className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
              aria-hidden="true"
            />
          </label>
        </div>
      </div>
    </article>
  )
}
