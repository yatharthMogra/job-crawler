"use client"

import { ExternalLink, Bookmark, EyeOff } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { EffortBadge, MatchTag } from "@/components/badges"
import { timeAgo, formatSalary, type JobWithRole } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

interface JobCardProps {
  job: JobWithRole
  showMatch?: boolean
  showRecommendation?: boolean
}

const EMP_LABEL: Record<string, string> = {
  FULLTIME: "Full-time",
  INTERNSHIP: "Internship",
  CONTRACT: "Contract",
}

const REMOTE_LABEL: Record<string, string> = {
  remote: "Remote",
  hybrid: "Hybrid",
  onsite: "Onsite",
}

export function JobCard({ job, showMatch = false, showRecommendation = false }: JobCardProps) {
  const { toggleSave, markApplied, hideJob, selectJob, selectedJobId } = useJobs()
  const salary = formatSalary(job.salary_min, job.salary_max)
  const selected = selectedJobId === job.id

  function stop(e: React.MouseEvent) {
    e.stopPropagation()
  }

  return (
    <article
      onClick={() => selectJob(job.id)}
      className={cn(
        "group cursor-pointer rounded-md border bg-white px-4 py-3 transition-all hover:shadow-sm",
        selected ? "border-zinc-400 shadow-sm" : "border-zinc-200",
        job.is_applied && "border-l-2 border-l-green-500",
      )}
    >
      <div className="flex gap-4">
        {/* Left column */}
        <div className="flex min-w-0 flex-[3] flex-col gap-1.5">
          <div className="flex items-start gap-2.5">
            <CompanyLogo company={job.company} size={32} />
            <div className="min-w-0 flex-1">
              <div className="flex items-center justify-between gap-2">
                <h3 className="truncate text-sm font-semibold text-zinc-900">{job.title}</h3>
                <span className="shrink-0 text-xs text-zinc-400">{timeAgo(job.posted_at)}</span>
              </div>
              <p className="truncate text-xs text-zinc-500">
                {job.company} · {job.location} · {REMOTE_LABEL[job.remote_type]}
              </p>
              <p className="truncate text-xs text-zinc-500">
                {salary && <>{salary} · </>}
                {EMP_LABEL[job.employment_type]}
              </p>
            </div>
          </div>

          <div className="mt-1 flex items-center gap-1.5">
            <a
              href={job.posting_url}
              target="_blank"
              rel="noreferrer"
              onClick={(e) => {
                stop(e)
                markApplied(job.id)
              }}
              className="inline-flex h-7 items-center gap-1 rounded-md bg-zinc-900 px-2.5 text-xs font-medium text-white transition-colors hover:bg-zinc-800"
            >
              Apply <ExternalLink className="size-3" />
            </a>
            <button
              type="button"
              onClick={(e) => {
                stop(e)
                toggleSave(job.id)
              }}
              className={cn(
                "inline-flex h-7 items-center gap-1 rounded-md border px-2.5 text-xs font-medium transition-colors",
                job.is_saved
                  ? "border-zinc-300 bg-zinc-100 text-zinc-900"
                  : "border-zinc-200 text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900",
              )}
            >
              <Bookmark className={cn("size-3", job.is_saved && "fill-current")} />
              {job.is_saved ? "Saved" : "Save"}
            </button>
            <button
              type="button"
              onClick={(e) => {
                stop(e)
                hideJob(job.id)
              }}
              className="inline-flex h-7 items-center gap-1 rounded-md px-2 text-xs font-medium text-zinc-400 transition-colors hover:bg-zinc-50 hover:text-zinc-600"
            >
              <EyeOff className="size-3" />
              Hide
            </button>
          </div>
        </div>

        {/* Right column */}
        <div className="flex flex-[2] flex-col gap-1.5 border-l border-zinc-100 pl-4">
          {showMatch ? (
            <>
              <div className="flex flex-wrap gap-1">
                {job.match_reasons.slice(0, 4).map((r) => (
                  <MatchTag key={r} label={r} />
                ))}
              </div>
              {showRecommendation && (
                <p className="mt-auto text-xs italic leading-snug text-zinc-500">{job.recommendation_reason}</p>
              )}
            </>
          ) : (
            <div className="flex items-start">
              <EffortBadge effort={job.application_effort} />
            </div>
          )}
          {job.is_applied && (
            <span className="ml-auto inline-flex items-center rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">
              Applied
            </span>
          )}
        </div>
      </div>
    </article>
  )
}
