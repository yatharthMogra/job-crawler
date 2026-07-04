"use client"

import { useEffect, useMemo } from "react"
import { ExternalLink, Bookmark } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { CompanyLogo } from "@/components/company-logo"
import { MatchTag } from "@/components/badges"
import { CompanyInfoCard } from "@/components/company-info-card"
import { H1bSponsorshipSection, SponsorshipStatusPill } from "@/components/h1b-sponsorship-section"
import {
  JobDescriptionSectionsView,
  buildMatchedLabels,
  hasDescriptionSections,
} from "@/components/job-description-sections"
import {
  HiringTeamUpsell,
  JobScoutPlusUpsell,
  ResponsibilityList,
  buildRoleAboutIntro,
} from "@/components/jobs/job-detail-extras"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { timeAgo, formatSalary, type JobWithRole } from "@/lib/jobs-data"
import type { JobFeedKind } from "@/lib/job-feed"
import { EMP_LABEL, REMOTE_LABEL } from "@/lib/job-meta"
import { cn } from "@/lib/utils"

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

function JobDetailActions({ job, feed = "recommended" }: { job: JobWithRole; feed?: JobFeedKind }) {
  const { toggleSave, startApply } = useJobs()
  const showSave = feed !== "applied"
  const saveLabel = feed === "saved" && job.is_saved ? "Unsave" : job.is_saved ? "Saved" : "Save"

  if (job.is_applied) {
    return (
      <div className="mt-4">
        <span className="inline-flex h-12 w-full items-center justify-center rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-[15px] font-semibold text-emerald-800">
          Applied
        </span>
      </div>
    )
  }

  return (
    <div className="mt-4 flex gap-2.5">
      {showSave ? (
        <button
          type="button"
          onClick={() => toggleSave(job.id)}
          className={cn(
            "inline-flex h-12 min-w-0 flex-1 items-center justify-center gap-1.5 rounded-xl border text-[15px] font-semibold transition-colors",
            job.is_saved
              ? "border-primary/30 bg-primary/5 text-primary"
              : "border-border bg-card text-foreground hover:bg-muted/60",
          )}
        >
          <Bookmark className={cn("size-4 shrink-0", job.is_saved && "fill-current")} />
          <span className="truncate">{saveLabel}</span>
        </button>
      ) : null}
      <a
        href={job.posting_url}
        target="_blank"
        rel="noreferrer"
        onClick={() => startApply(job)}
        className={cn(
          "btn-brand inline-flex h-12 min-w-0 items-center justify-center gap-1.5 rounded-xl text-[15px] font-bold",
          showSave ? "flex-1" : "w-full",
        )}
      >
        Apply now <ExternalLink className="size-4 shrink-0" />
      </a>
    </div>
  )
}

export function JobDetailContent({
  job,
  showMatch = false,
  feed = "recommended",
}: {
  job: JobWithRole
  showMatch?: boolean
  feed?: JobFeedKind
}) {
  const { profileHome } = useProfileFlow()

  const profileSkillNames = useMemo(
    () => profileHome?.profile.skills?.flatMap((group) => group.names) ?? [],
    [profileHome],
  )

  const matchedLabels = useMemo(
    () => buildMatchedLabels(job.match_reasons, profileSkillNames),
    [job.match_reasons, profileSkillNames],
  )

  const descriptionSections = useMemo(
    () => ({
      responsibilities: job.responsibilities,
      required_qualifications: job.required_qualifications,
      preferred_qualifications: job.preferred_qualifications,
      benefits: job.benefits,
    }),
    [job],
  )

  const hasStructured = hasDescriptionSections(descriptionSections)
  const matchPct = Math.round(Math.min(1, Math.max(0, job.personal_score)) * 100)
  const salaryLabel = formatSalary(job.salary_min, job.salary_max)

  return (
    <div className="flex h-full min-h-0 flex-col bg-background">
      <div className="shrink-0 border-b border-border/70 bg-card px-5 py-5 sm:px-6">
        <div className="flex items-start gap-4">
          <CompanyLogo
            company={job.company}
            size={64}
            shape="square"
            website={job.company_info?.website}
          />
          <div className="min-w-0 flex-1">
            <h2 className="text-pretty text-2xl font-bold leading-tight tracking-tight text-foreground">
              {job.title}
            </h2>
            <p className="mt-1.5 text-[15px] font-medium text-muted-foreground">
              {job.company} · {job.location}
              {job.roleCategory ? (
                <span className="text-foreground/60"> ({REMOTE_LABEL[job.remote_type]})</span>
              ) : null}
            </p>
            {showMatch && matchPct > 0 ? (
              <div className="mt-3">
                <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                  Match quality
                </p>
                <p className="text-xl font-bold text-emerald-600">{matchPct}% match</p>
              </div>
            ) : null}
          </div>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-3">
          <div className="rounded-lg border border-border/60 bg-muted/40 px-3 py-2.5 text-sm font-semibold text-foreground">
            {EMP_LABEL[job.employment_type]}
          </div>
          <div className="rounded-lg border border-border/60 bg-muted/40 px-3 py-2.5 text-sm font-semibold text-foreground">
            {salaryLabel ?? "Competitive pay"}
          </div>
          <div className="rounded-lg border border-border/60 bg-muted/40 px-3 py-2.5 text-sm font-semibold text-foreground">
            Posted {timeAgo(job.posted_at)}
          </div>
        </div>

        <JobDetailActions job={job} feed={feed} />
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-5 py-5 sm:px-6">
        <div className="flex flex-col gap-6 xl:grid xl:grid-cols-[minmax(0,1fr)_200px] xl:gap-6">
          <div className="min-w-0">
            {showMatch && (job.match_reasons.length > 0 || job.recommendation_reason) ? (
              <section className="mb-6 rounded-xl border border-primary/20 bg-primary/[0.06] p-5">
                <h3 className="mb-3 text-base font-bold text-foreground">Why this matches</h3>
                {job.match_reasons.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {job.match_reasons.map((r) => (
                      <MatchTag key={r} label={r} />
                    ))}
                  </div>
                ) : null}
                {job.recommendation_reason ? (
                  <p className="mt-3 text-[15px] leading-relaxed text-muted-foreground">
                    {job.recommendation_reason}
                  </p>
                ) : null}
              </section>
            ) : null}

            <section className="mb-6">
              <h3 className="mb-3 text-lg font-bold text-foreground">About the role</h3>
              <p className="text-[15px] leading-relaxed text-foreground/90">
                {buildRoleAboutIntro(job)}
              </p>
            </section>

            {job.responsibilities.length > 0 ? (
              <section className="mb-6">
                <h3 className="mb-3 text-lg font-bold text-foreground">Key responsibilities</h3>
                <ResponsibilityList items={job.responsibilities} />
              </section>
            ) : null}

            {hasStructured ? (
              <section className="mb-6">
                <div className="text-[15px] leading-relaxed [&_h4]:mb-2 [&_h4]:mt-5 [&_h4]:text-[15px] [&_h4]:font-bold [&_li]:mb-2 [&_li]:text-[15px] [&_li]:leading-relaxed">
                  <JobDescriptionSectionsView
                    sections={{
                      responsibilities: [],
                      required_qualifications: descriptionSections.required_qualifications,
                      preferred_qualifications: descriptionSections.preferred_qualifications,
                      benefits: descriptionSections.benefits,
                    }}
                    matchedLabels={matchedLabels}
                  />
                </div>
              </section>
            ) : job.description_html ? (
              <section className="mb-6">
                <h3 className="mb-3 text-lg font-bold text-foreground">Full description</h3>
                <div
                  className="job-description text-[15px] leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: job.description_html }}
                />
              </section>
            ) : null}

            {job.skills.length > 0 ? (
              <section className="mb-6">
                <h3 className="mb-3 text-lg font-bold text-foreground">Skills &amp; requirements</h3>
                <div className="flex flex-wrap gap-2">
                  {job.skills.map((s) => (
                    <span
                      key={s}
                      className={cn(
                        "rounded-md px-2.5 py-1 text-sm",
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

            {job.company_info ? (
              <section className="mb-6">
                <h3 className="mb-3 text-lg font-bold text-foreground">About {job.company}</h3>
                <CompanyInfoCard info={job.company_info} />
              </section>
            ) : null}

            <SponsorshipStatusPill
              status={job.sponsorship_status}
              confidence={job.sponsorship_confidence}
            />

            {job.h1b_sponsorship ? <H1bSponsorshipSection info={job.h1b_sponsorship} /> : null}
          </div>

          <aside className="space-y-4 xl:sticky xl:top-0 xl:self-start">
            <HiringTeamUpsell job={job} />
            <JobScoutPlusUpsell />
          </aside>
        </div>
      </div>
    </div>
  )
}

export function JobDetailPanel({
  showMatch = false,
  feed = "recommended",
  className,
}: {
  showMatch?: boolean
  feed?: JobFeedKind
  className?: string
}) {
  const { jobs, recommendedJobs, selectedJobId, selectJob } = useJobs()
  const job =
    jobs.find((j) => j.id === selectedJobId) ??
    recommendedJobs.find((j) => j.id === selectedJobId) ??
    null

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") selectJob(null)
    }
    if (job) document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [job, selectJob])

  if (!job) return null

  return (
    <aside
      className={cn(
        "flex h-full min-h-0 w-full max-w-[480px] shrink-0 flex-col border-l border-border/80 bg-card",
        className,
      )}
    >
      <JobDetailContent job={job} showMatch={showMatch} feed={feed} />
    </aside>
  )
}

export function JobDrawer({
  showMatch = false,
  feed = "recommended",
  variant = "overlay",
}: {
  showMatch?: boolean
  feed?: JobFeedKind
  variant?: "overlay" | "inline"
}) {
  const { jobs, recommendedJobs, selectedJobId, selectJob } = useJobs()
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

  if (variant === "inline") {
    if (!job) return null
    return (
      <aside className="hidden h-full min-h-0 min-w-0 flex-[7] flex-col overflow-hidden border-l border-border/70 bg-background shadow-[inset_4px_0_12px_-8px_rgba(0,0,0,0.08)] md:flex">
        <JobDetailContent job={job} showMatch={showMatch} feed={feed} />
      </aside>
    )
  }

  return (
    <>
      <div
        onClick={() => selectJob(null)}
        className={cn(
          "fixed inset-0 z-40 bg-primary/10 backdrop-blur-[2px] transition-opacity",
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
        {job ? (
          <JobDetailContent job={job} showMatch={showMatch} feed={feed} />
        ) : null}
      </aside>
    </>
  )
}
