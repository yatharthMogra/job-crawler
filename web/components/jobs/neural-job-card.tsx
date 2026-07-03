"use client"

import { useState } from "react"
import {
  Bookmark,
  Briefcase,
  Building2,
  CheckCircle2,
  MapPin,
  Sparkles,
  ThumbsDown,
  Zap,
} from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchGauge } from "@/components/ui/match-gauge"
import { NotInterestedDialog } from "@/components/jobs/job-feedback-dialogs"
import {
  applicationWindowLabel,
  coreSkillsMatchPercent,
  companySizeLabel,
  isPremiumRole,
  matchTier,
  neuralRationale,
  outreachLabel,
  salaryDisplay,
} from "@/lib/recommendation/neural-display"
import { REMOTE_LABEL } from "@/lib/job-meta"
import { timeAgo, type JobWithRole } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

interface NeuralJobCardProps {
  job: JobWithRole
  featured?: boolean
}

export function NeuralJobCard({ job, featured = false }: NeuralJobCardProps) {
  const { toggleSave, markApplied, startApply, selectJob, selectedJobId, submitNotInterested } =
    useJobs()
  const [notInterestedOpen, setNotInterestedOpen] = useState(false)

  const isApplied = job.is_applied
  const selected = selectedJobId === job.id
  const tier = matchTier(job.personal_score)
  const premium = isPremiumRole(job)
  const skillsPct = coreSkillsMatchPercent(job)

  function stop(e: React.MouseEvent) {
    e.stopPropagation()
  }

  return (
    <>
      <article
        onClick={() => selectJob(job.id)}
        className={cn(
          "group overflow-hidden rounded-2xl border border-border/80 bg-card shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)] transition-all duration-200",
          "hover:border-primary/30 hover:shadow-lg hover:shadow-primary/10",
          selected && "border-primary/40 ring-2 ring-primary/15",
          featured && "border-primary/25",
        )}
      >
        <div className="flex flex-col lg:flex-row">
          <div className="min-w-0 flex-1 p-5 sm:p-6">
            <div className="flex gap-4">
              <CompanyLogo company={job.company} size={48} className="shrink-0" />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full border border-border/60 bg-muted/50 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                    {applicationWindowLabel(job.posted_at)}
                  </span>
                  {tier ? (
                    <span className="rounded-full bg-primary/10 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-primary">
                      {tier}
                    </span>
                  ) : null}
                  {premium ? (
                    <span className="rounded-full bg-amber-500/15 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-amber-700">
                      Premium Role
                    </span>
                  ) : null}
                  <span className="text-[10px] font-medium text-muted-foreground">{timeAgo(job.posted_at)}</span>
                </div>

                <h3 className="mt-2 text-lg font-bold leading-snug text-foreground transition-colors group-hover:text-primary sm:text-xl">
                  {job.title}
                </h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {job.company}
                  {job.skills.length > 0 ? (
                    <span className="text-foreground/70"> · {job.skills.slice(0, 4).join(" · ")}</span>
                  ) : null}
                </p>
              </div>
            </div>

            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              <MetaCell
                icon={MapPin}
                label="Location"
                value={`${job.location} · ${REMOTE_LABEL[job.remote_type]}`}
              />
              <MetaCell icon={Briefcase} label="Compensation" value={salaryDisplay(job)} />
              <MetaCell icon={Building2} label="Company Size" value={companySizeLabel(job)} />
              <MetaCell icon={Sparkles} label="Outreach" value={outreachLabel(job)} />
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-4 border-t border-border/50 pt-4">
              <button
                type="button"
                disabled={isApplied}
                onClick={(e) => {
                  stop(e)
                  if (!isApplied) markApplied(job.id)
                }}
                className={cn(
                  "inline-flex items-center gap-1.5 text-xs font-semibold transition-colors",
                  isApplied ? "text-emerald-600" : "text-muted-foreground hover:text-foreground",
                )}
              >
                <CheckCircle2 className="size-3.5" />
                {isApplied ? "Applied" : "Mark Applied"}
              </button>
              <button
                type="button"
                onClick={(e) => {
                  stop(e)
                  setNotInterestedOpen(true)
                }}
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-muted-foreground transition-colors hover:text-foreground"
              >
                <ThumbsDown className="size-3.5" />
                Not Interested
              </button>
            </div>
          </div>

          <div className="flex shrink-0 flex-col border-t border-border/60 bg-gradient-to-b from-primary/5 to-card lg:w-72 lg:border-l lg:border-t-0">
            <div className="flex flex-1 flex-col p-5">
              <div className="flex justify-center">
                <MatchGauge score={job.personal_score} variant="ring" />
              </div>

              <div className="mt-4 rounded-xl border border-primary/15 bg-card/80 p-3">
                <p className="text-[10px] font-bold uppercase tracking-widest text-primary">
                  Neural Rationale
                </p>
                <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                  {neuralRationale(job)}
                </p>
              </div>

              <div className="mt-4">
                <div className="flex items-center justify-between text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                  <span>Core Skills Match</span>
                  <span className="text-primary">{skillsPct}%</span>
                </div>
                <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-primary transition-all duration-700"
                    style={{ width: `${skillsPct}%` }}
                  />
                </div>
              </div>

              <div className="mt-auto space-y-2 pt-5">
                {isApplied ? (
                  <span className="flex h-11 w-full items-center justify-center rounded-xl border border-border bg-muted/40 text-sm font-semibold text-muted-foreground">
                    Application Tracked
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
                    className="btn-brand flex h-11 w-full items-center justify-center gap-2 rounded-xl text-sm font-bold"
                  >
                    <Zap className="size-4" />
                    Apply via Neural Profile
                  </a>
                )}
                <button
                  type="button"
                  onClick={(e) => {
                    stop(e)
                    toggleSave(job.id)
                  }}
                  className={cn(
                    "flex h-10 w-full items-center justify-center gap-2 rounded-xl border text-sm font-semibold transition-colors",
                    job.is_saved
                      ? "border-primary/30 bg-primary/5 text-primary"
                      : "border-border/80 bg-card text-foreground hover:border-primary/30",
                  )}
                >
                  <Bookmark className={cn("size-4", job.is_saved && "fill-current")} />
                  {job.is_saved ? "Saved" : "Save for Later"}
                </button>
              </div>
            </div>
          </div>
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

function MetaCell({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof MapPin
  label: string
  value: string
}) {
  return (
    <div className="rounded-xl border border-border/50 bg-surface/30 px-3 py-2.5">
      <div className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
        <Icon className="size-3" />
        {label}
      </div>
      <p className="mt-1 text-sm font-medium text-foreground">{value}</p>
    </div>
  )
}
