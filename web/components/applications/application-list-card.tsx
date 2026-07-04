"use client"

import { ExternalLink } from "lucide-react"
import { CompanyLogo } from "@/components/company-logo"
import {
  formatAppliedDate,
  PIPELINE_STATUS_LABELS,
  PIPELINE_STATUS_STYLES,
  type ApplicationRecord,
} from "@/lib/applications/pipeline-status"
import { REMOTE_LABEL } from "@/lib/job-meta"
import { cn } from "@/lib/utils"

export function ApplicationListCard({
  record,
  onWithdraw,
}: {
  record: ApplicationRecord
  onWithdraw: () => void
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

        <div className="flex shrink-0 items-center gap-2 xl:pl-4">
          <a
            href={job.posting_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex h-10 min-w-[132px] flex-1 items-center justify-center gap-1.5 rounded-xl bg-slate-900 px-4 text-sm font-semibold text-white transition-opacity hover:opacity-90 xl:flex-none"
          >
            View posting
            <ExternalLink className="size-3.5" />
          </a>
          <button
            type="button"
            onClick={onWithdraw}
            className="inline-flex h-10 min-w-[132px] flex-1 items-center justify-center rounded-xl border border-border/70 bg-card px-4 text-sm font-semibold text-foreground/80 transition-colors hover:bg-muted/50 xl:flex-none"
          >
            Withdraw
          </button>
        </div>
      </div>
    </article>
  )
}
