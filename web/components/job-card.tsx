"use client"

import { useState } from "react"
import type { LucideIcon } from "lucide-react"
import {
  Bookmark,
  Briefcase,
  Building2,
  DollarSign,
  ExternalLink,
  GraduationCap,
  MapPin,
  Zap,
} from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchGauge } from "@/components/ui/match-gauge"
import { JobActionsMenu } from "@/components/jobs/job-actions-menu"
import { NotInterestedDialog, ReportIssueDialog } from "@/components/jobs/job-feedback-dialogs"
import { EMP_LABEL, REMOTE_LABEL, SENIORITY_LABEL } from "@/lib/job-meta"
import { timeAgo, formatSalary, type JobWithRole } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

const EFFORT_LABEL = {
  LOW: "Low effort apply",
  MEDIUM: "Medium effort",
  HIGH: "High effort",
} as const

interface JobCardProps {
  job: JobWithRole
  showMatch?: boolean
  showRecommendation?: boolean
  featured?: boolean
}

function MetaItem({ icon: Icon, label }: { icon: LucideIcon; label: string }) {
  return (
    <div className="flex min-w-0 items-center gap-2">
      <Icon className="size-3.5 shrink-0 text-muted-foreground" aria-hidden="true" />
      <span className="truncate text-sm font-medium leading-snug text-foreground/85">{label}</span>
    </div>
  )
}

export function JobCard({
  job,
  showMatch = false,
  featured = false,
}: JobCardProps) {
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

  const salary = formatSalary(job.salary_min, job.salary_max)
  const selected = selectedJobId === job.id
  const isStrongMatch = job.personal_score >= 0.85
  const matchHints = job.match_reasons.slice(0, 3).join(" · ")

  function stop(e: React.MouseEvent) {
    e.stopPropagation()
  }

  return (
    <>
      <article
        onClick={() => selectJob(job.id)}
        className={cn(
          "job-card-surface group cursor-pointer hover:border-primary/30 hover:shadow-md hover:shadow-primary/10",
          selected && "border-primary/40 ring-2 ring-primary/20",
          featured && "border-primary/25",
        )}
      >
        <div className="flex">
          <div className="flex min-w-0 flex-1 gap-3.5 p-3.5 sm:gap-4 sm:p-4">
            <div className="flex w-12 shrink-0 items-start justify-center pt-0.5 sm:w-14">
              <CompanyLogo company={job.company} size={48} />
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex items-start justify-between gap-2">
                <div className="flex min-w-0 flex-wrap items-center gap-1.5">
                  <span className="rounded-full bg-add-muted px-2.5 py-0.5 text-xs font-semibold text-add-foreground">
                    {timeAgo(job.posted_at)}
                  </span>
                  {isStrongMatch ? (
                    <span className="rounded-full bg-sky-100 px-2.5 py-0.5 text-xs font-semibold text-sky-800 dark:bg-sky-950 dark:text-sky-200">
                      Early applicant
                    </span>
                  ) : null}
                  {job.roleCategory ? (
                    <span className="rounded-full bg-accent px-2.5 py-0.5 text-xs font-semibold text-accent-foreground">
                      {job.roleCategory}
                    </span>
                  ) : null}
                </div>
                <JobActionsMenu
                  isApplied={job.is_applied}
                  onApplied={() => markApplied(job.id)}
                  onNotInterested={() => setNotInterestedOpen(true)}
                  onReportIssue={() => setReportOpen(true)}
                />
              </div>

              <h3 className="mt-1.5 line-clamp-2 text-base font-semibold leading-snug text-foreground group-hover:text-primary">
                {job.title}
              </h3>
              <p className="mt-1 truncate text-sm text-primary">
                {job.company}
                {job.skills.length > 0 ? (
                  <span className="font-normal text-muted-foreground">
                    {" "}
                    · {job.skills.slice(0, 3).join(" · ")}
                  </span>
                ) : null}
              </p>

              <div className="mt-2.5 grid grid-cols-2 gap-x-5 gap-y-2 sm:grid-cols-3">
                <MetaItem icon={MapPin} label={job.location} />
                <MetaItem icon={Briefcase} label={EMP_LABEL[job.employment_type]} />
                <MetaItem icon={DollarSign} label={salary ?? "Competitive"} />
                <MetaItem icon={Building2} label={REMOTE_LABEL[job.remote_type]} />
                <MetaItem icon={GraduationCap} label={SENIORITY_LABEL[job.seniority_level]} />
                <MetaItem icon={Zap} label={EFFORT_LABEL[job.application_effort]} />
              </div>

              <div className="mt-2.5 flex items-center justify-between gap-3 border-t border-border/50 pt-2.5">
                <p className="min-w-0 flex-1 truncate text-xs text-muted-foreground">
                  {matchHints || job.recommendation_reason}
                </p>
                <div className="flex shrink-0 items-center gap-1.5">
                  <button
                    type="button"
                    onClick={(e) => {
                      stop(e)
                      toggleSave(job.id)
                    }}
                    className={cn(
                      "inline-flex size-8 items-center justify-center rounded-lg border transition-colors",
                      job.is_saved
                        ? "border-primary/30 bg-accent text-primary"
                        : "border-border text-muted-foreground hover:border-primary/30 hover:text-primary",
                    )}
                    aria-label={job.is_saved ? "Remove bookmark" : "Bookmark job"}
                  >
                    <Bookmark className={cn("size-3.5", job.is_saved && "fill-current")} />
                  </button>
                  <a
                    href={job.posting_url}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => {
                      stop(e)
                      startApply(job)
                    }}
                    className={cn(
                      "inline-flex h-8 items-center justify-center rounded-lg px-3.5 text-xs font-semibold transition-colors",
                      featured || isStrongMatch
                        ? "btn-brand"
                        : "border border-border bg-muted/50 text-foreground hover:bg-muted",
                    )}
                  >
                    Apply
                  </a>
                </div>
              </div>
            </div>
          </div>

          {showMatch ? (
            <div className="navy-section flex w-[76px] shrink-0 flex-col items-center justify-center border-l border-border/40 px-2 py-3 sm:w-[84px]">
              <MatchGauge score={job.personal_score} variant="sidebar" />
            </div>
          ) : null}
        </div>

        {job.is_applied ? (
          <div className="border-t border-border/60 px-4 py-1.5 text-[11px] text-muted-foreground">
            <ExternalLink className="mr-1 inline size-3" />
            Applied
          </div>
        ) : null}
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
