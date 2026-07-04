"use client"

import { ExternalLink, X } from "lucide-react"
import { CompanyLogo } from "@/components/company-logo"
import {
  formatAppliedDate,
  PIPELINE_STATUS_LABELS,
  PIPELINE_STATUS_STYLES,
  type ApplicationRecord,
} from "@/lib/applications/pipeline-status"
import { EMP_LABEL, REMOTE_LABEL } from "@/lib/job-meta"
import { formatSalary } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

const STATUS_STEPS: ApplicationRecord["status"][] = [
  "submitted",
  "under_review",
  "interview",
  "offer",
]

export function ApplicationDetailPanel({
  record,
  onClose,
  onWithdraw,
}: {
  record: ApplicationRecord
  onClose: () => void
  onWithdraw: () => void
}) {
  const { job, status, appliedAt } = record
  const salaryLabel = formatSalary(job.salary_min, job.salary_max)
  const currentStep = STATUS_STEPS.indexOf(status)

  return (
    <aside className="flex h-full min-h-0 flex-col border-l border-border/70 bg-background">
      <div className="flex items-center justify-between border-b border-border/60 px-5 py-4">
        <p className="text-sm font-semibold text-foreground">Application details</p>
        <button
          type="button"
          onClick={onClose}
          className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
          aria-label="Close details"
        >
          <X className="size-4" />
        </button>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-5 py-5">
        <div className="flex items-start gap-4">
          <CompanyLogo
            company={job.company}
            size={56}
            shape="square"
            website={job.company_info?.website}
          />
          <div className="min-w-0 flex-1">
            <span
              className={cn(
                "inline-flex rounded-full px-2.5 py-1 text-[11px] font-bold uppercase tracking-wide",
                PIPELINE_STATUS_STYLES[status].badge,
              )}
            >
              {PIPELINE_STATUS_LABELS[status]}
            </span>
            <h2 className="mt-3 text-2xl font-bold tracking-tight text-foreground">{job.title}</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              {job.company} · {job.location}
            </p>
            <p className="mt-2 text-xs text-muted-foreground">
              Applied on {formatAppliedDate(appliedAt)}
            </p>
          </div>
        </div>

        <div className="mt-6 grid gap-2 sm:grid-cols-2">
          <div className="rounded-xl border border-border/60 bg-muted/20 px-3 py-2.5">
            <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
              Employment
            </p>
            <p className="mt-1 text-sm font-semibold text-foreground">
              {EMP_LABEL[job.employment_type]}
            </p>
          </div>
          <div className="rounded-xl border border-border/60 bg-muted/20 px-3 py-2.5">
            <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
              Work model
            </p>
            <p className="mt-1 text-sm font-semibold text-foreground">
              {REMOTE_LABEL[job.remote_type]}
            </p>
          </div>
          {salaryLabel ? (
            <div className="rounded-xl border border-border/60 bg-muted/20 px-3 py-2.5 sm:col-span-2">
              <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                Compensation
              </p>
              <p className="mt-1 text-sm font-semibold text-foreground">{salaryLabel}</p>
            </div>
          ) : null}
        </div>

        <section className="mt-8">
          <h3 className="text-sm font-bold text-foreground">Application progress</h3>
          <ol className="mt-4 space-y-0">
            {STATUS_STEPS.map((step, index) => {
              const done = index <= currentStep
              const active = index === currentStep
              return (
                <li key={step} className="relative flex gap-3 pb-5 last:pb-0">
                  {index < STATUS_STEPS.length - 1 ? (
                    <span
                      className={cn(
                        "absolute left-[9px] top-5 h-[calc(100%-4px)] w-px",
                        done ? "bg-primary/40" : "bg-border",
                      )}
                      aria-hidden="true"
                    />
                  ) : null}
                  <span
                    className={cn(
                      "relative z-[1] mt-0.5 size-[18px] shrink-0 rounded-full border-2",
                      done
                        ? active
                          ? "border-primary bg-primary"
                          : "border-primary/40 bg-primary/20"
                        : "border-border bg-card",
                    )}
                  />
                  <div>
                    <p
                      className={cn(
                        "text-sm font-semibold",
                        done ? "text-foreground" : "text-muted-foreground",
                      )}
                    >
                      {PIPELINE_STATUS_LABELS[step]}
                    </p>
                    {active ? (
                      <p className="mt-0.5 text-xs text-muted-foreground">Current stage</p>
                    ) : null}
                  </div>
                </li>
              )
            })}
          </ol>
        </section>

        {job.skills.length > 0 ? (
          <section className="mt-8">
            <h3 className="text-sm font-bold text-foreground">Role stack</h3>
            <div className="mt-3 flex flex-wrap gap-2">
              {job.skills.slice(0, 6).map((skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-border/70 bg-muted/30 px-3 py-1 text-xs font-medium text-foreground/80"
                >
                  {skill}
                </span>
              ))}
            </div>
          </section>
        ) : null}
      </div>

      <div className="shrink-0 border-t border-border/60 p-5">
        <div className="flex flex-col gap-2 sm:flex-row">
          <a
            href={job.posting_url}
            target="_blank"
            rel="noreferrer"
            className="btn-brand inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-xl text-sm font-bold"
          >
            Open job posting
            <ExternalLink className="size-4" />
          </a>
          <button
            type="button"
            onClick={onWithdraw}
            className="inline-flex h-11 flex-1 items-center justify-center rounded-xl border border-border/70 text-sm font-semibold text-muted-foreground transition-colors hover:border-red-200 hover:bg-red-50 hover:text-red-700"
          >
            Withdraw application
          </button>
        </div>
      </div>
    </aside>
  )
}
