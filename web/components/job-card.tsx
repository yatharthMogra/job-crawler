"use client"

import { useState } from "react"
import type { LucideIcon } from "lucide-react"
import {
  Bookmark,
  Briefcase,
  Building2,
  Check,
  CheckCircle2,
  DollarSign,
  ExternalLink,
  Flag,
  GraduationCap,
  MapPin,
  Sparkles,
  ThumbsDown,
} from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchGauge } from "@/components/ui/match-gauge"
import { NotInterestedDialog, ReportIssueDialog } from "@/components/jobs/job-feedback-dialogs"
import { EMP_LABEL, REMOTE_LABEL, SENIORITY_LABEL } from "@/lib/job-meta"
import { timeAgo, formatSalary, type JobWithRole } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

interface JobCardProps {
  job: JobWithRole
  showMatch?: boolean
  showRecommendation?: boolean
  featured?: boolean
  cardMode?: "default" | "applied"
}

function MetaItem({ icon: Icon, label }: { icon: LucideIcon; label: string }) {
  return (
    <div className="flex min-w-0 items-center gap-2">
      <Icon className="size-3.5 shrink-0 text-muted-foreground" aria-hidden="true" />
      <span className="truncate text-sm font-medium leading-snug text-foreground/85">{label}</span>
    </div>
  )
}

function WhyThisFitsColumn({ items, className }: { items: string[]; className?: string }) {
  if (items.length === 0) return null

  return (
    <div
      className={cn(
        "relative flex shrink-0 flex-col justify-center overflow-hidden border-l border-add/25 px-3.5 py-4",
        "bg-gradient-to-b from-add-muted via-add-muted/80 to-emerald-50/40",
        "before:absolute before:inset-y-3 before:left-0 before:w-0.5 before:rounded-full before:bg-add/70",
        className,
      )}
    >
      <div className="flex items-center gap-1.5">
        <span className="inline-flex size-5 items-center justify-center rounded-full bg-white/80 shadow-sm ring-1 ring-add/20">
          <Sparkles className="size-3 text-add" aria-hidden="true" />
        </span>
        <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-add-foreground">
          Why this fits
        </p>
      </div>

      <ul className="mt-3 flex flex-col gap-2">
        {items.map((item) => (
          <li
            key={item}
            className="flex items-start gap-1.5 rounded-lg border border-add/15 bg-white/75 px-2 py-1.5 shadow-sm backdrop-blur-[1px]"
          >
            <Check className="mt-0.5 size-3 shrink-0 text-add" aria-hidden="true" />
            <span className="text-[11px] font-medium leading-snug text-add-foreground">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

export function JobCard({
  job,
  showMatch = false,
  featured = false,
  cardMode = "default",
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
  const isApplied = cardMode === "applied" || job.is_applied
  const isStrongMatch = job.qualification_fit >= 0.85
  const whyFitItems =
    job.match_reasons.length > 0
      ? job.match_reasons.slice(0, 3)
      : job.skills.slice(0, 3)

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
        <div className="flex min-h-[160px]">
          <div className="flex min-w-0 flex-1 gap-3.5 p-4 sm:gap-4">
            <div className="flex w-12 shrink-0 items-start justify-center pt-0.5 sm:w-14">
              <CompanyLogo company={job.company} size={52} logoUrl={job.company_info?.logo_url} />
            </div>

            <div className="flex min-w-0 flex-1 flex-col">
              <div className="flex flex-wrap items-center gap-1.5">
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

              <h3 className="mt-1.5 line-clamp-2 text-base font-semibold leading-snug text-foreground group-hover:text-primary">
                {job.title}
              </h3>
              <p className="mt-0.5 truncate text-sm text-muted-foreground">
                {job.company}
                {job.skills.length > 0 ? (
                  <span> · {job.skills.slice(0, 3).join(" · ")}</span>
                ) : null}
              </p>

              <div className="mt-2.5 grid grid-cols-2 gap-x-4 gap-y-2 sm:grid-cols-3">
                <MetaItem icon={MapPin} label={job.location} />
                <MetaItem icon={Briefcase} label={EMP_LABEL[job.employment_type]} />
                <MetaItem icon={DollarSign} label={salary ?? "Competitive"} />
                <MetaItem icon={Building2} label={REMOTE_LABEL[job.remote_type]} />
                <MetaItem icon={GraduationCap} label={SENIORITY_LABEL[job.seniority_level]} />
              </div>

              {!showMatch ? (
                <WhyThisFitsColumn
                  items={whyFitItems}
                  className="mt-3 rounded-xl border border-add/20 sm:hidden"
                />
              ) : null}

              <div className="mt-auto flex flex-wrap items-center justify-between gap-3 border-t border-border/50 pt-3">
                <div className="flex flex-wrap items-center gap-3">
                  <button
                    type="button"
                    disabled={isApplied}
                    onClick={(e) => {
                      stop(e)
                      if (!isApplied) markApplied(job.id)
                    }}
                    className={cn(
                      "inline-flex items-center gap-1.5 text-xs font-medium transition-colors",
                      isApplied
                        ? "cursor-default text-add-foreground"
                        : "text-muted-foreground hover:text-foreground",
                    )}
                  >
                    <CheckCircle2 className="size-3.5" />
                    {isApplied ? "Already applied" : "Mark as applied"}
                  </button>
                  <button
                    type="button"
                    onClick={(e) => {
                      stop(e)
                      setNotInterestedOpen(true)
                    }}
                    className="inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground transition-colors hover:text-foreground"
                  >
                    <ThumbsDown className="size-3.5" />
                    Not interested
                  </button>
                  <button
                    type="button"
                    onClick={(e) => {
                      stop(e)
                      setReportOpen(true)
                    }}
                    className="inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground transition-colors hover:text-foreground"
                  >
                    <Flag className="size-3.5" />
                    Report issue
                  </button>
                </div>

                <div className="flex shrink-0 items-center gap-2">
                  <button
                    type="button"
                    onClick={(e) => {
                      stop(e)
                      toggleSave(job.id)
                    }}
                    className={cn(
                      "inline-flex size-10 items-center justify-center rounded-lg border transition-colors",
                      job.is_saved
                        ? "border-primary/30 bg-accent text-primary"
                        : "border-border text-muted-foreground hover:border-primary/30 hover:text-primary",
                    )}
                    aria-label={job.is_saved ? "Remove bookmark" : "Bookmark job"}
                  >
                    <Bookmark className={cn("size-4", job.is_saved && "fill-current")} />
                  </button>
                  {isApplied ? (
                    <span
                      className="inline-flex h-10 min-w-[88px] cursor-default items-center justify-center rounded-lg border border-border bg-muted/40 px-4 text-sm font-semibold text-muted-foreground"
                      aria-disabled="true"
                    >
                      Applied
                    </span>
                  ) : (
                    <a
                      href={job.posting_url}
                      target="_blank"
                      rel="noreferrer"
                      onClick={(e) => {
                        stop(e)
                        startApply(job)
                      }}
                      className="btn-brand inline-flex h-10 min-w-[88px] items-center justify-center rounded-lg px-5 text-sm font-semibold transition-colors"
                    >
                      Apply
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>

          {showMatch && whyFitItems.length > 0 ? (
            <WhyThisFitsColumn
              items={whyFitItems}
              className="hidden w-[124px] sm:flex lg:w-[140px]"
            />
          ) : null}

          {showMatch ? (
            <div className="navy-section flex w-[108px] shrink-0 flex-col items-center justify-center border-l border-border/40 px-2 py-4 sm:w-[120px]">
              <MatchGauge score={job.qualification_fit} variant="sidebar" />
            </div>
          ) : null}
        </div>

        {isApplied && cardMode !== "applied" ? (
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
