"use client"

import { useEffect, useMemo } from "react"
import { X, ExternalLink, Bookmark } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchTag, StatPill } from "@/components/badges"
import { CompanyInfoCard } from "@/components/company-info-card"
import { H1bSponsorshipSection, SponsorshipStatusPill } from "@/components/h1b-sponsorship-section"
import {
  JobDescriptionSectionsView,
  buildMatchedLabels,
  hasDescriptionSections,
} from "@/components/job-description-sections"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { timeAgo, formatSalary } from "@/lib/jobs-data"
import { EMP_LABEL, REMOTE_LABEL, SENIORITY_LABEL } from "@/lib/job-meta"
import { cn } from "@/lib/utils"

const EFFORT_LABEL: Record<string, string> = {
  LOW: "Low effort",
  MEDIUM: "Medium effort",
  HIGH: "High effort",
}

function normalizeSkill(value: string): string {
  return value.trim().toLowerCase()
}

function isSkillMatched(skill: string, matchedLabels: Set<string>): boolean {
  const normalized = normalizeSkill(skill)
  if (matchedLabels.has(normalized)) return true
  for (const match of matchedLabels) {
    if (normalized.includes(match) || match.includes(normalized)) return true
  }
  return false
}

export function JobDrawer({ showMatch = false }: { showMatch?: boolean }) {
  const { jobs, recommendedJobs, selectedJobId, selectJob, toggleSave, startApply } = useJobs()
  const { profileHome } = useProfileFlow()
  const job =
    jobs.find((j) => j.id === selectedJobId) ??
    recommendedJobs.find((j) => j.id === selectedJobId) ??
    null
  const open = job != null

  const profileSkillNames = useMemo(
    () => profileHome?.skills.flatMap((group) => group.names) ?? [],
    [profileHome],
  )

  const matchedLabels = useMemo(() => {
    if (!job) return new Set<string>()
    return buildMatchedLabels(job.match_reasons, profileSkillNames)
  }, [job, profileSkillNames])

  const descriptionSections = useMemo(() => {
    if (!job) {
      return {
        responsibilities: [],
        required_qualifications: [],
        preferred_qualifications: [],
        benefits: [],
      }
    }
    return {
      responsibilities: job.responsibilities,
      required_qualifications: job.required_qualifications,
      preferred_qualifications: job.preferred_qualifications,
      benefits: job.benefits,
    }
  }, [job])

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") selectJob(null)
    }
    if (open) document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [open, selectJob])

  return (
    <>
      <div
        onClick={() => selectJob(null)}
        className={cn(
          "fixed inset-0 z-40 bg-primary/10 backdrop-blur-[2px] transition-opacity lg:hidden",
          open ? "opacity-100" : "pointer-events-none opacity-0",
        )}
        aria-hidden="true"
      />
      <aside
        className={cn(
          "fixed inset-y-0 right-0 z-50 flex w-full max-w-[420px] flex-col border-l border-border/80 bg-card shadow-2xl shadow-primary/10 transition-transform duration-300 ease-out",
          open ? "translate-x-0" : "translate-x-full",
        )}
        aria-hidden={!open}
      >
        {job && (
          <>
            <div className="flex items-start justify-between gap-3 border-b border-border/80 bg-gradient-to-br from-accent/40 to-card p-5">
              <div className="flex min-w-0 gap-3">
                <CompanyLogo company={job.company} size={48} />
                <div className="min-w-0">
                  <h2 className="text-pretty text-lg font-semibold leading-tight text-foreground">{job.title}</h2>
                  <p className="mt-0.5 text-sm text-muted-foreground">
                    {job.company} · {job.location}
                  </p>
                  <p className="mt-0.5 text-xs text-muted-foreground/80">Posted {timeAgo(job.posted_at)}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => selectJob(null)}
                aria-label="Close"
                className="shrink-0 rounded-md p-1 text-muted-foreground hover:bg-secondary hover:text-foreground"
              >
                <X className="size-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-5">
              <a
                href={job.posting_url}
                target="_blank"
                rel="noreferrer"
                onClick={() => startApply(job)}
                className="btn-brand mb-5 inline-flex h-10 w-full items-center justify-center gap-1.5 rounded-lg text-sm font-medium"
              >
                Apply Now <ExternalLink className="size-4" />
              </a>

              <div className="mb-6 flex flex-wrap gap-1.5">
                {formatSalary(job.salary_min, job.salary_max) && (
                  <StatPill>{formatSalary(job.salary_min, job.salary_max)}</StatPill>
                )}
                <StatPill>{EMP_LABEL[job.employment_type]}</StatPill>
                <StatPill>{SENIORITY_LABEL[job.seniority_level]}</StatPill>
                <StatPill>{EFFORT_LABEL[job.application_effort]}</StatPill>
                <StatPill>{REMOTE_LABEL[job.remote_type]}</StatPill>
              </div>

              {job.company_info ? <CompanyInfoCard info={job.company_info} /> : null}

              {showMatch && (
                <section className="mb-6 rounded-xl border border-brand-muted/80 bg-brand-muted/30 p-4">
                  <h3 className="mb-2 text-sm font-semibold text-foreground">Why this fits your profile</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {job.match_reasons.map((r) => (
                      <MatchTag key={r} label={r} />
                    ))}
                  </div>
                  <p className="mt-2 text-xs italic text-muted-foreground">{job.recommendation_reason}</p>
                </section>
              )}

              {hasDescriptionSections(descriptionSections) ? (
                <section className="mb-6">
                  <h3 className="mb-2 text-sm font-semibold text-foreground">About the role</h3>
                  <JobDescriptionSectionsView
                    sections={descriptionSections}
                    matchedLabels={matchedLabels}
                  />
                </section>
              ) : job.description_html ? (
                <section className="mb-6">
                  <h3 className="mb-2 text-sm font-semibold text-foreground">About the role</h3>
                  <div className="job-description" dangerouslySetInnerHTML={{ __html: job.description_html }} />
                </section>
              ) : null}

              {job.skills.length > 0 ? (
                <section className="mb-6">
                  <h3 className="mb-2 text-sm font-semibold text-foreground">Skills &amp; Requirements</h3>
                  <div className="flex flex-wrap gap-1.5">
                    {job.skills.map((s) => (
                      <span
                        key={s}
                        className={cn(
                          "rounded-md px-2 py-1 text-xs",
                          isSkillMatched(s, matchedLabels)
                            ? "border border-emerald-500/30 bg-emerald-500/10 text-emerald-900 dark:text-emerald-100"
                            : "bg-secondary text-secondary-foreground",
                        )}
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </section>
              ) : null}

              <SponsorshipStatusPill
                status={job.sponsorship_status}
                confidence={job.sponsorship_confidence}
              />

              {job.h1b_sponsorship ? <H1bSponsorshipSection info={job.h1b_sponsorship} /> : null}
            </div>

            <div className="flex gap-2 border-t border-border/80 bg-card p-4">
              <a
                href={job.posting_url}
                target="_blank"
                rel="noreferrer"
                onClick={() => startApply(job)}
                className="btn-brand inline-flex h-10 flex-1 items-center justify-center gap-1.5 rounded-lg text-sm font-medium"
              >
                Apply <ExternalLink className="size-4" />
              </a>
              <button
                type="button"
                onClick={() => toggleSave(job.id)}
                className={cn(
                  "inline-flex h-10 flex-1 items-center justify-center gap-1.5 rounded-lg border text-sm font-medium transition-colors",
                  job.is_saved
                    ? "border-primary/30 bg-accent text-accent-foreground"
                    : "border-border text-foreground hover:bg-secondary/80",
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
