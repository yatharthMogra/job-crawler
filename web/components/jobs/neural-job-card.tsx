"use client"

import { useState } from "react"
import {
  Bookmark,
  Calendar,
  Check,
  CheckCircle2,
  Clock,
  Crown,
  DollarSign,
  ExternalLink,
  Home,
  MapPin,
  ThumbsDown,
  type LucideIcon,
} from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { EligibilityBadges } from "@/components/jobs/eligibility-badges"
import { MatchGauge } from "@/components/ui/match-gauge"
import { NotInterestedDialog } from "@/components/jobs/job-feedback-dialogs"
import { PreferenceIndicatorTags } from "@/components/jobs/preference-indicator-tags"
import { matchTier } from "@/lib/recommendation/neural-display"
import { EMP_LABEL, REMOTE_LABEL, SENIORITY_LABEL } from "@/lib/job-meta"
import { timeAgo, type JobWithRole } from "@/lib/jobs-data"
import type { JobFeedKind } from "@/lib/job-feed"
import { cn } from "@/lib/utils"

interface NeuralJobCardProps {
  job: JobWithRole
  /** Narrow list column when detail panel is open */
  compact?: boolean
  feed?: JobFeedKind
}

function formatSalaryYr(min: number | null, max: number | null): string {
  if (min == null && max == null) return "—"
  const fmt = (n: number) => {
    if (n >= 1000) return `$${Math.round(n / 1000)}K`
    return `$${n}`
  }
  if (min != null && max != null) return `${fmt(min)}/yr - ${fmt(max)}/yr`
  if (min != null) return `${fmt(min)}/yr+`
  return `${fmt(max!)}/yr`
}

function experienceLabel(job: JobWithRole): string {
  switch (job.seniority_level) {
    case "internship":
      return "0 years exp"
    case "new_grad":
    case "entry":
    case "early_career":
      return "0–2 years exp"
    case "mid":
      return "2+ years exp"
    case "senior":
      return "5+ years exp"
    case "staff":
      return "8+ years exp"
    default:
      return "2+ years exp"
  }
}

function MetaRow({ icon: Icon, label }: { icon: LucideIcon; label: string }) {
  return (
    <div className="flex min-w-0 items-center gap-2 text-[13px] leading-snug text-foreground/85">
      <Icon className="size-4 shrink-0 text-muted-foreground" strokeWidth={1.75} />
      <span className="truncate">{label}</span>
    </div>
  )
}

export function NeuralJobCard({ job, compact = false, feed = "recommended" }: NeuralJobCardProps) {
  const {
    toggleSave,
    markApplied,
    startApply,
    selectJob,
    selectedJobId,
    submitNotInterested,
    atsFitByJobId,
  } = useJobs()
  const [notInterestedOpen, setNotInterestedOpen] = useState(false)

  const isApplied = job.is_applied
  const selected = selectedJobId === job.id
  const tier = matchTier(job.qualification_fit)
  const atsFitState = atsFitByJobId[job.id]
  const poolBadge =
    atsFitState?.status === "ready" &&
    atsFitState.data.pool_percentile_label &&
    (atsFitState.data.pool_percentile_label === "Top 5%" ||
      atsFitState.data.pool_percentile_label === "Top 10%")
      ? atsFitState.data.pool_percentile_label
      : null
  const salary = formatSalaryYr(job.salary_min, job.salary_max)
  const highlights = (
    job.match_reasons.length > 0
      ? job.match_reasons
      : [
          ...(job.sponsorship_status === "yes" ? ["H1B Sponsored"] : []),
          ...job.skills.slice(0, 2),
        ]
  ).slice(0, 2)
  const industryLine = [job.roleCategory, job.skills[0], job.skills[1]].filter(Boolean).join(" · ")

  function stop(e: React.MouseEvent) {
    e.stopPropagation()
  }

  if (compact) {
    return (
      <>
        <article
          onClick={() => selectJob(job.id)}
          className={cn(
            "group relative flex cursor-pointer overflow-hidden rounded-xl border bg-card transition-all duration-200",
            selected
              ? "border-primary border-b-[3px] border-l-[4px] bg-primary/[0.05] shadow-lg shadow-primary/10"
              : "border-border/70 shadow-sm hover:border-primary/25 hover:shadow-md",
          )}
        >
          <div className="min-w-0 flex-1 py-4 pl-4 pr-3">
            <div className="flex gap-3.5">
              <CompanyLogo
                company={job.company}
                size={52}
                shape="square"
                logoUrl={job.company_info?.logo_url}
              />
              <div className="min-w-0 flex-1">
                <h3
                  className={cn(
                    "text-lg font-bold leading-snug tracking-tight",
                    selected ? "text-primary" : "text-foreground group-hover:text-primary",
                  )}
                >
                  {job.title}
                </h3>
                <div className="mt-1.5 flex flex-wrap items-center gap-1.5">
                  {selected ? (
                    <span className="rounded-full bg-primary px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wide text-primary-foreground">
                      Viewing
                    </span>
                  ) : null}
                  <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-800">
                    {timeAgo(job.posted_at)}
                  </span>
                  {tier ? (
                    <span className="rounded-full bg-violet-500/12 px-2.5 py-0.5 text-[11px] font-bold uppercase tracking-wide text-violet-800">
                      {tier}
                    </span>
                  ) : null}
                  {poolBadge ? (
                    <span className="rounded-full bg-amber-500/15 px-2.5 py-0.5 text-[11px] font-bold uppercase tracking-wide text-amber-900">
                      {poolBadge}
                    </span>
                  ) : null}
                </div>
                <PreferenceIndicatorTags
                  indicators={job.preference_indicators}
                  className="mt-2"
                />
                <p className="mt-0.5 text-sm font-medium text-foreground/80">
                  {job.company}
                  {job.roleCategory ? (
                    <span className="font-normal text-muted-foreground"> · {job.roleCategory}</span>
                  ) : null}
                </p>
                <p className="mt-2 text-sm text-muted-foreground">
                  {job.location} · {REMOTE_LABEL[job.remote_type]}
                  {salary !== "—" ? (
                    <span className="font-semibold text-foreground"> · {salary}</span>
                  ) : null}
                </p>
              </div>
            </div>
            {!compact ? (
              <div className="mt-3.5 flex items-center justify-end gap-2">
                <ActionButtons
                  job={job}
                  feed={feed}
                  isApplied={isApplied}
                  compact
                  onApply={(e) => {
                    stop(e)
                    startApply(job)
                  }}
                  onSave={(e) => {
                    stop(e)
                    toggleSave(job.id)
                  }}
                  onMarkApplied={(e) => {
                    stop(e)
                    if (!isApplied) markApplied(job.id)
                  }}
                  onNotInterested={(e) => {
                    stop(e)
                    setNotInterestedOpen(true)
                  }}
                />
              </div>
            ) : null}
          </div>
          <div className="navy-section flex w-[112px] shrink-0 flex-col items-center justify-center border-l border-white/10 px-2 py-4 sm:w-[120px]">
            <MatchGauge score={job.qualification_fit} variant="sidebar" />
          </div>
        </article>
        <NotInterestedDialog
          open={notInterestedOpen}
          onOpenChange={setNotInterestedOpen}
          onSubmit={(reason) => submitNotInterested(job.id, reason)}
        />
      </>
    )
  }

  // Full-width card — Jobright-style consistent layout
  return (
    <>
      <article
        onClick={() => selectJob(job.id)}
        className={cn(
          "group relative flex cursor-pointer overflow-hidden rounded-2xl border bg-card transition-all duration-300",
          selected
            ? "border-primary bg-primary/[0.04] shadow-lg shadow-primary/10 ring-2 ring-primary/20"
            : "border-border/60 shadow-sm hover:border-border hover:shadow-md",
        )}
      >
        <span
          className={cn(
            "absolute inset-y-0 left-0 w-1.5 transition-colors",
            selected ? "bg-primary" : "bg-transparent",
          )}
          aria-hidden="true"
        />
        <div className="flex min-w-0 flex-1 flex-col p-5 pl-6">
          {/* Header: logo + badges + title + company line */}
          <div className="flex gap-4">
            <CompanyLogo
              company={job.company}
              size={52}
              shape="square"
              logoUrl={job.company_info?.logo_url}
            />
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                {selected ? (
                  <span className="rounded-full bg-primary px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide text-primary-foreground">
                    Viewing
                  </span>
                ) : null}
                <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-xs font-semibold text-emerald-800">
                  {timeAgo(job.posted_at)}
                </span>
                {tier ? (
                  <span className="rounded-full bg-violet-500/12 px-2.5 py-0.5 text-xs font-semibold text-violet-800">
                    {tier}
                  </span>
                ) : null}
                {poolBadge ? (
                  <span className="rounded-full bg-amber-500/15 px-2.5 py-0.5 text-xs font-semibold text-amber-900">
                    {poolBadge}
                  </span>
                ) : null}
                {job.sponsorship_status === "yes" ? (
                  <span className="rounded-full bg-sky-500/12 px-2.5 py-0.5 text-xs font-semibold text-sky-800">
                    H1-B friendly
                  </span>
                ) : null}
                <EligibilityBadges job={job} />
              </div>
              <h3
                className={cn(
                  "mt-2 text-xl font-bold leading-snug tracking-tight",
                  selected ? "text-primary" : "text-foreground",
                )}
              >
                {job.title}
              </h3>
              <p className="mt-1 text-sm text-muted-foreground">
                <span className="font-medium text-foreground/80">{job.company}</span>
                {industryLine ? <span> / {industryLine}</span> : null}
              </p>
            </div>
          </div>

          {/* Consistent 2×3 meta grid */}
          <div className="mt-5 grid grid-cols-2 gap-x-6 gap-y-3 sm:grid-cols-3">
            <MetaRow icon={MapPin} label={job.location} />
            <MetaRow icon={Clock} label={EMP_LABEL[job.employment_type]} />
            <MetaRow icon={DollarSign} label={salary} />
            <MetaRow icon={Home} label={REMOTE_LABEL[job.remote_type]} />
            <MetaRow icon={Crown} label={SENIORITY_LABEL[job.seniority_level]} />
            <MetaRow icon={Calendar} label={experienceLabel(job)} />
          </div>
          <PreferenceIndicatorTags indicators={job.preference_indicators} className="mt-4" />

          {/* Footer: meta left, actions right */}
          <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-border/50 pt-4">
            <p className="text-sm text-muted-foreground">
              {job.roleCategory ? `${job.roleCategory} track` : "Recommended for you"}
            </p>
            <ActionButtons
              job={job}
              feed={feed}
              isApplied={isApplied}
              onApply={(e) => {
                stop(e)
                startApply(job)
              }}
              onSave={(e) => {
                stop(e)
                toggleSave(job.id)
              }}
              onMarkApplied={(e) => {
                stop(e)
                if (!isApplied) markApplied(job.id)
              }}
              onNotInterested={(e) => {
                stop(e)
                setNotInterestedOpen(true)
              }}
            />
          </div>
        </div>

        {/* Dark match rail */}
        <div className="navy-section flex w-[140px] shrink-0 flex-col items-center px-3 py-5 sm:w-[156px]">
          <MatchGauge score={job.qualification_fit} variant="sidebar" />
          <div className="my-3 h-px w-full bg-white/15" />
          <ul className="w-full space-y-2">
            {highlights.map((item) => (
              <li
                key={item}
                className="flex items-start gap-1.5 text-[11px] font-medium leading-snug text-white/90"
              >
                <Check className="mt-0.5 size-3 shrink-0 text-teal-300" strokeWidth={2.5} />
                <span className="line-clamp-2">{item}</span>
              </li>
            ))}
            {job.sponsorship_status === "yes" &&
            !highlights.some((h) => h.toLowerCase().includes("h1")) ? (
              <li className="flex items-start gap-1.5 text-[11px] font-medium text-white/90">
                <Check className="mt-0.5 size-3 shrink-0 text-teal-300" strokeWidth={2.5} />
                H1B Sponsored
              </li>
            ) : null}
          </ul>
        </div>
      </article>

      <NotInterestedDialog
        open={notInterestedOpen}
        onOpenChange={setNotInterestedOpen}
        onSubmit={(reason) => submitNotInterested(job.id, reason)}
      />
    </>
  )
}

function ActionButtons({
  job,
  feed = "recommended",
  isApplied,
  compact,
  onApply,
  onSave,
  onMarkApplied,
  onNotInterested,
}: {
  job: JobWithRole
  feed?: JobFeedKind
  isApplied: boolean
  compact?: boolean
  onApply: (e: React.MouseEvent) => void
  onSave: (e: React.MouseEvent) => void
  onMarkApplied: (e: React.MouseEvent) => void
  onNotInterested: (e: React.MouseEvent) => void
}) {
  const showNotInterested = feed === "recommended"
  const showSave = feed !== "applied"
  const saveLabel = feed === "saved" && job.is_saved ? "Unsave" : job.is_saved ? "Saved" : "Save"

  return (
    <div className="flex flex-wrap items-center gap-2">
      {showNotInterested ? (
        <button
          type="button"
          onClick={onNotInterested}
          className="flex size-9 items-center justify-center rounded-full border border-border/80 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
          aria-label="Not interested"
        >
          <ThumbsDown className="size-4" />
        </button>
      ) : null}
      {showSave ? (
        <button
          type="button"
          onClick={onSave}
          className={cn(
            "flex items-center justify-center rounded-full border transition-colors",
            compact ? "size-9" : "h-9 gap-1.5 px-3 text-sm font-semibold",
            job.is_saved
              ? "border-primary/30 bg-primary/10 text-primary"
              : "border-border/80 text-muted-foreground hover:bg-muted hover:text-foreground",
          )}
          aria-label={saveLabel}
        >
          <Bookmark className={cn("size-4", job.is_saved && "fill-current")} />
          {!compact ? <span>{saveLabel}</span> : null}
        </button>
      ) : null}
      {!compact ? (
        <button
          type="button"
          disabled={isApplied}
          onClick={onMarkApplied}
          className={cn(
            "flex size-9 items-center justify-center rounded-full border border-border/80 transition-colors",
            isApplied
              ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-700"
              : "text-muted-foreground hover:bg-muted hover:text-foreground",
          )}
          aria-label="Mark applied"
        >
          <CheckCircle2 className="size-4" />
        </button>
      ) : null}
      {isApplied ? (
        <span className="inline-flex h-10 items-center rounded-full bg-muted px-4 text-sm font-semibold text-muted-foreground">
          Applied
        </span>
      ) : (
        <a
          href={job.posting_url}
          target="_blank"
          rel="noreferrer"
          onClick={onApply}
          className="btn-brand inline-flex h-10 items-center gap-1.5 rounded-full px-5 text-sm font-bold"
        >
          Apply
          <ExternalLink className="size-3.5" />
        </a>
      )}
    </div>
  )
}
