"use client"

import { useState } from "react"
import { ExternalLink, Heart } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchGauge } from "@/components/ui/match-gauge"
import { JobActionsMenu } from "@/components/jobs/job-actions-menu"
import { NotInterestedDialog, ReportIssueDialog } from "@/components/jobs/job-feedback-dialogs"
import { timeAgo, formatSalary, type JobWithRole } from "@/lib/jobs-data"
import { EMP_LABEL, REMOTE_LABEL, SENIORITY_LABEL } from "@/lib/job-meta"
import { cn } from "@/lib/utils"

interface JobCardProps {
  job: JobWithRole
  showMatch?: boolean
  showRecommendation?: boolean
}

function MetaField({ label, value }: { label: string; value: string }) {
  return (
    <div className="min-w-0 rounded-lg border border-border/80 bg-surface/90 px-2.5 py-2">
      <dt className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">{label}</dt>
      <dd className="mt-0.5 truncate text-sm font-medium text-foreground">{value}</dd>
    </div>
  )
}

export function JobCard({ job, showMatch = false, showRecommendation = false }: JobCardProps) {
  const {
    toggleSave,
    markApplied,
    startApply,
    selectJob,
    selectedJobId,
    submitNotInterested,
    submitReportIssue,
  } = useJobs()
  const [notInterestedOpen, setNotInterestedOpen] = useState(false)
  const [reportOpen, setReportOpen] = useState(false)

  const salary = formatSalary(job.salary_min, job.salary_max) ?? "Not listed"
  const selected = selectedJobId === job.id

  function stop(e: React.MouseEvent) {
    e.stopPropagation()
  }

  return (
    <>
      <article
        onClick={() => selectJob(job.id)}
        className={cn(
          "group job-card-surface cursor-pointer hover:-translate-y-0.5 hover:border-primary/35 hover:shadow-lg hover:shadow-primary/12",
          selected && "border-primary/50 ring-2 ring-primary/25 shadow-lg shadow-primary/15",
        )}
      >
        <div
          className="absolute inset-y-0 left-0 w-1 bg-gradient-to-b from-primary via-brand to-primary/40"
          aria-hidden="true"
        />
        <div className="flex flex-col lg:flex-row lg:items-stretch">
          <div className="flex min-w-0 flex-1 flex-col justify-between p-5 pl-6 lg:p-6 lg:pl-7">
            <div>
              <div className="flex items-start gap-4">
                <CompanyLogo company={job.company} size={48} />
                <div className="min-w-0 flex-1 pt-0.5">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <h3 className="text-[17px] font-semibold leading-snug text-foreground group-hover:text-primary">
                        {job.title}
                      </h3>
                      <p className="mt-1 text-sm text-muted-foreground">
                        {job.company}
                        <span className="mx-1.5 text-border">·</span>
                        {job.roleCategory}
                      </p>
                    </div>
                    <JobActionsMenu
                      isApplied={job.is_applied}
                      onApplied={() => markApplied(job.id)}
                      onNotInterested={() => setNotInterestedOpen(true)}
                      onReportIssue={() => setReportOpen(true)}
                    />
                  </div>

                  <dl className="mt-6 grid grid-cols-2 gap-x-6 gap-y-4 sm:grid-cols-3 lg:grid-cols-5">
                    <MetaField label="Location" value={job.location} />
                    <MetaField label="Work model" value={REMOTE_LABEL[job.remote_type]} />
                    <MetaField label="Type" value={EMP_LABEL[job.employment_type]} />
                    <MetaField label="Level" value={SENIORITY_LABEL[job.seniority_level]} />
                    <MetaField label="Salary" value={salary} />
                  </dl>
                </div>
              </div>
            </div>

            <div className="mt-8 flex flex-wrap items-center justify-between gap-3 border-t-2 border-border/70 pt-4">
              <div className="flex items-center gap-3">
                <span className="text-xs text-muted-foreground">{timeAgo(job.posted_at)}</span>
                {job.is_saved ? (
                  <span className="rounded-full bg-remove-muted px-2 py-0.5 text-[10px] font-medium text-remove">
                    Liked
                  </span>
                ) : null}
                <button
                  type="button"
                  onClick={(e) => {
                    stop(e)
                    toggleSave(job.id)
                  }}
                  className={cn(
                    "inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors",
                    job.is_saved
                      ? "border-remove/30 bg-remove-muted text-remove"
                      : "border-border text-muted-foreground hover:border-primary/30 hover:bg-accent/50 hover:text-foreground",
                  )}
                  aria-label="Like job"
                >
                  <Heart className={cn("size-3.5", job.is_saved && "fill-current")} />
                  {job.is_saved ? "Liked" : "Like"}
                </button>
              </div>

              <div className="flex items-center gap-4">
                <span className="text-xs text-muted-foreground">{EFFORT_COPY[job.application_effort]}</span>
                <a
                  href={job.posting_url}
                  target="_blank"
                  rel="noreferrer"
                  onClick={(e) => {
                    stop(e)
                    startApply(job)
                  }}
                  className="btn-brand inline-flex h-9 items-center justify-center gap-1.5 rounded-lg px-5 text-sm font-medium"
                >
                  Apply <ExternalLink className="size-3.5" />
                </a>
              </div>
            </div>
          </div>

          {showMatch ? (
            <div className="flex items-center border-t-2 border-border/70 bg-gradient-to-b from-brand-muted/40 to-card px-5 py-5 lg:w-[220px] lg:shrink-0 lg:border-l-2 lg:border-t-0 lg:px-4">
              <MatchGauge
                score={job.personal_score}
                reasons={job.match_reasons}
                insight={showRecommendation ? job.recommendation_reason : undefined}
                className="w-full"
              />
            </div>
          ) : null}
        </div>
      </article>

      <NotInterestedDialog
        open={notInterestedOpen}
        onOpenChange={setNotInterestedOpen}
        onSubmit={(reason) => submitNotInterested(job.id, reason)}
      />
      <ReportIssueDialog
        open={reportOpen}
        onOpenChange={setReportOpen}
        onSubmit={(reason) => submitReportIssue(job.id, reason)}
      />
    </>
  )
}

const EFFORT_COPY = {
  LOW: "Low effort apply",
  MEDIUM: "Medium effort apply",
  HIGH: "High effort apply",
} as const
