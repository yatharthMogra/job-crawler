"use client"

import { useEffect } from "react"
import { X, ExternalLink, Bookmark } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchTag, StatPill } from "@/components/badges"
import { timeAgo, formatSalary } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

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
const EFFORT_LABEL: Record<string, string> = {
  LOW: "Low effort",
  MEDIUM: "Medium effort",
  HIGH: "High effort",
}

export function JobDrawer({ showMatch = false }: { showMatch?: boolean }) {
  const { jobs, recommendedJobs, selectedJobId, selectJob, toggleSave, markApplied } = useJobs()
  const job =
    jobs.find((j) => j.id === selectedJobId) ??
    recommendedJobs.find((j) => j.id === selectedJobId) ??
    null
  const open = job != null

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") selectJob(null)
    }
    if (open) document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [open, selectJob])

  return (
    <>
      {/* Mobile overlay */}
      <div
        onClick={() => selectJob(null)}
        className={cn(
          "fixed inset-0 z-40 bg-black/20 transition-opacity lg:hidden",
          open ? "opacity-100" : "pointer-events-none opacity-0",
        )}
        aria-hidden="true"
      />
      <aside
        className={cn(
          "fixed inset-y-0 right-0 z-50 flex w-full max-w-[420px] flex-col border-l border-zinc-200 bg-white transition-transform duration-300 ease-out",
          open ? "translate-x-0" : "translate-x-full",
        )}
        aria-hidden={!open}
      >
        {job && (
          <>
            {/* Header */}
            <div className="flex items-start justify-between gap-3 border-b border-zinc-200 p-5">
              <div className="flex min-w-0 gap-3">
                <CompanyLogo company={job.company} size={48} />
                <div className="min-w-0">
                  <h2 className="text-pretty text-lg font-semibold leading-tight text-zinc-900">{job.title}</h2>
                  <p className="mt-0.5 text-sm text-zinc-500">
                    {job.company} · {job.location}
                  </p>
                  <p className="mt-0.5 text-xs text-zinc-400">Posted {timeAgo(job.posted_at)}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => selectJob(null)}
                aria-label="Close"
                className="shrink-0 rounded-md p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700"
              >
                <X className="size-4" />
              </button>
            </div>

            {/* Scrollable body */}
            <div className="flex-1 overflow-y-auto p-5">
              <a
                href={job.posting_url}
                target="_blank"
                rel="noreferrer"
                onClick={() => markApplied(job.id)}
                className="mb-5 inline-flex h-9 w-full items-center justify-center gap-1.5 rounded-md bg-zinc-900 text-sm font-medium text-white transition-colors hover:bg-zinc-800"
              >
                Apply Now <ExternalLink className="size-4" />
              </a>

              {/* Quick stats */}
              <div className="mb-6 flex flex-wrap gap-1.5">
                {formatSalary(job.salary_min, job.salary_max) && (
                  <StatPill>{formatSalary(job.salary_min, job.salary_max)}</StatPill>
                )}
                <StatPill>{EMP_LABEL[job.employment_type]}</StatPill>
                <StatPill>{EFFORT_LABEL[job.application_effort]}</StatPill>
                <StatPill>{REMOTE_LABEL[job.remote_type]}</StatPill>
              </div>

              {showMatch && (
                <section className="mb-6">
                  <h3 className="mb-2 text-sm font-semibold text-zinc-900">Why this fits your profile</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {job.match_reasons.map((r) => (
                      <MatchTag key={r} label={r} />
                    ))}
                  </div>
                  <p className="mt-2 text-xs italic text-zinc-500">{job.recommendation_reason}</p>
                </section>
              )}

              <section className="mb-6">
                <h3 className="mb-2 text-sm font-semibold text-zinc-900">About the role</h3>
                <div className="job-description" dangerouslySetInnerHTML={{ __html: job.description_html }} />
              </section>

              <section>
                <h3 className="mb-2 text-sm font-semibold text-zinc-900">Skills &amp; Requirements</h3>
                <div className="flex flex-wrap gap-1.5">
                  {job.skills.map((s) => (
                    <span key={s} className="rounded bg-zinc-100 px-2 py-1 text-xs text-zinc-700">
                      {s}
                    </span>
                  ))}
                </div>
              </section>
            </div>

            {/* Sticky footer */}
            <div className="flex gap-2 border-t border-zinc-200 p-4">
              <a
                href={job.posting_url}
                target="_blank"
                rel="noreferrer"
                onClick={() => markApplied(job.id)}
                className="inline-flex h-9 flex-1 items-center justify-center gap-1.5 rounded-md bg-zinc-900 text-sm font-medium text-white transition-colors hover:bg-zinc-800"
              >
                Apply <ExternalLink className="size-4" />
              </a>
              <button
                type="button"
                onClick={() => toggleSave(job.id)}
                className={cn(
                  "inline-flex h-9 flex-1 items-center justify-center gap-1.5 rounded-md border text-sm font-medium transition-colors",
                  job.is_saved
                    ? "border-zinc-300 bg-zinc-100 text-zinc-900"
                    : "border-zinc-200 text-zinc-700 hover:bg-zinc-50",
                )}
              >
                <Bookmark className={cn("size-4", job.is_saved && "fill-current")} />
                {job.is_saved ? "Saved" : "Save"}
              </button>
            </div>
          </>
        )}
      </aside>
    </>
  )
}
