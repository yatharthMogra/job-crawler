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
    <div className="min-w-0">
      <dt className="text-[10px] font-medium uppercase tracking-wider text-zinc-400">{label}</dt>
      <dd className="mt-0.5 truncate text-sm text-zinc-800">{value}</dd>
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
          "group cursor-pointer overflow-hidden rounded-xl border bg-white transition-shadow hover:shadow-sm",
          selected ? "border-zinc-400 shadow-sm" : "border-zinc-200",
        )}
      >
        <div className="flex flex-col lg:flex-row lg:items-stretch">
          <div className="flex min-w-0 flex-1 flex-col justify-between p-5 lg:p-6">
            <div>
              <div className="flex items-start gap-4">
                <CompanyLogo company={job.company} size={48} />
                <div className="min-w-0 flex-1 pt-0.5">
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <h3 className="text-[17px] font-semibold leading-snug text-zinc-900">{job.title}</h3>
                      <p className="mt-1 text-sm text-zinc-500">
                        {job.company}
                        <span className="mx-1.5 text-zinc-300">·</span>
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

            <div className="mt-8 flex flex-wrap items-center justify-between gap-3 border-t border-zinc-100 pt-4">
              <div className="flex items-center gap-3">
                <span className="text-xs text-zinc-400">{timeAgo(job.posted_at)}</span>
                {job.is_saved ? (
                  <span className="rounded border border-zinc-200 px-2 py-0.5 text-[10px] font-medium text-zinc-600">
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
                      ? "border-zinc-900 bg-zinc-900 text-white"
                      : "border-zinc-200 text-zinc-600 hover:border-zinc-300 hover:bg-zinc-50",
                  )}
                  aria-label="Like job"
                >
                  <Heart className={cn("size-3.5", job.is_saved && "fill-current")} />
                  {job.is_saved ? "Liked" : "Like"}
                </button>
              </div>

              <div className="flex items-center gap-4">
                <span className="text-xs text-zinc-400">{EFFORT_COPY[job.application_effort]}</span>
                <a
                  href={job.posting_url}
                  target="_blank"
                  rel="noreferrer"
                  onClick={(e) => {
                    stop(e)
                    startApply(job)
                  }}
                  className="inline-flex h-9 items-center justify-center gap-1.5 rounded-lg bg-zinc-900 px-5 text-sm font-medium text-white transition-colors hover:bg-zinc-800"
                >
                  Apply <ExternalLink className="size-3.5" />
                </a>
              </div>
            </div>
          </div>

          {showMatch ? (
            <div className="flex items-center border-t border-zinc-100 px-5 py-5 lg:w-[210px] lg:shrink-0 lg:border-l lg:border-t-0 lg:px-4">
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
