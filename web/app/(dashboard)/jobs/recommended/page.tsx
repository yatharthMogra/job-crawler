"use client"

import { useEffect, useMemo } from "react"
import { Star } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"
import { useJobsSearch } from "@/app/(dashboard)/jobs/layout"
import { useSession } from "@/components/session-provider"
import { matchesEmploymentTypeFilter } from "@/lib/employment-type-filter"
import type { JobWithRole } from "@/lib/jobs-data"

function matchesSearch(job: JobWithRole, q: string) {
  if (!q.trim()) return true
  const lower = q.toLowerCase()
  return job.title.toLowerCase().includes(lower) || job.company.toLowerCase().includes(lower)
}

function normalizeRole(value: string) {
  return value.trim().toLowerCase().replace(/[^a-z0-9]+/g, " ")
}

function rolesMatch(target: string, jobRole: string) {
  const a = normalizeRole(target)
  const b = normalizeRole(jobRole)
  if (!a || !b) return false
  if (a === b) return true
  return a.includes(b) || b.includes(a)
}

function matchesTargetRoles(
  job: JobWithRole,
  primaryRoles: string[],
  secondaryRoles: string[],
) {
  if (primaryRoles.length === 0 && secondaryRoles.length === 0) return true
  const targets = [...primaryRoles, ...secondaryRoles]
  return targets.some(
    (target) => rolesMatch(target, job.roleCategory) || rolesMatch(target, job.title),
  )
}

export default function RecommendedPage() {
  const { candidateId } = useSession()
  const { recommendedJobs, hiddenIds, recommendedLoading, error, filters } = useJobs()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const { search } = useJobsSearch()

  useEffect(() => {
    if (candidateId && !profileHome) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, profileHome, loadProfileHome])

  const ranked = useMemo<JobWithRole[]>(() => {
    const primaryRoles = profileHome?.primaryRoles ?? []
    const secondaryRoles = profileHome?.secondaryRoles ?? []

    return recommendedJobs
      .filter((j) => !j.is_applied)
      .filter((j) => !hiddenIds.has(j.id))
      .filter((j) => matchesSearch(j, search))
      .filter((j) => matchesTargetRoles(j, primaryRoles, secondaryRoles))
      .filter((j) => matchesEmploymentTypeFilter(j.employment_type, filters.employmentType))
  }, [recommendedJobs, hiddenIds, search, profileHome, filters.employmentType])

  return (
    <div>
      {error ? (
        <EmptyState
          icon={Star}
          title="Could not load recommendations."
          description={error}
          ctaLabel="Set job filters →"
          ctaHref="/filters"
        />
      ) : !recommendedLoading && ranked.length === 0 ? (
        <EmptyState
          icon={Star}
          title="No recommendations yet."
          description="Complete your profile and set role preferences to get personalized matches."
          ctaLabel="Set job filters →"
          ctaHref="/filters"
        />
      ) : (
        <JobFeed jobs={ranked} showMatch showRecommendation loading={recommendedLoading} />
      )}
    </div>
  )
}
