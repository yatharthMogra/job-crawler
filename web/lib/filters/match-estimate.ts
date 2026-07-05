import type { JobWithRole } from "@/lib/jobs-data"
import type { JobFiltersState } from "@/lib/profile/job-filters"
import { EXPERIENCE_TIERS } from "@/lib/filters/filter-options"

function remoteMatches(workModels: string[], remoteType: string): boolean {
  if (workModels.length === 0) return true
  const normalized = workModels.map((m) => m.toLowerCase())
  if (normalized.includes("remote") && remoteType === "remote") return true
  if (normalized.includes("hybrid") && remoteType === "hybrid") return true
  if (normalized.includes("onsite") && remoteType === "onsite") return true
  return false
}

function seniorityMatches(experienceLevels: string[], seniority: string): boolean {
  if (experienceLevels.length === 0) return true
  const tierLevels = EXPERIENCE_TIERS.flatMap((tier) => tier.levels)
  if (!tierLevels.some((level) => experienceLevels.includes(level))) {
    return true
  }
  const seniorityMap: Record<string, string[]> = {
    internship: ["Intern/New Grad"],
    new_grad: ["Intern/New Grad", "Entry Level"],
    early_career: ["Entry Level"],
    entry: ["Entry Level", "Mid Level"],
    mid: ["Mid Level", "Senior Level"],
    senior: ["Senior Level", "Lead/Staff"],
    staff: ["Lead/Staff", "Director/Executive"],
  }
  const allowed = seniorityMap[seniority] ?? []
  return experienceLevels.some((level) => allowed.includes(level))
}

function salaryMatches(
  job: JobWithRole,
  minimumSalary: number | null,
  maximumSalary: number | null,
): boolean {
  if (minimumSalary == null && maximumSalary == null) return true
  const jobMin = job.salary_min ?? job.salary_max
  const jobMax = job.salary_max ?? job.salary_min
  if (jobMin == null && jobMax == null) return true
  if (minimumSalary != null && jobMax != null && jobMax < minimumSalary) return false
  if (maximumSalary != null && jobMin != null && jobMin > maximumSalary) return false
  return true
}


export function filterJobsByState(
  jobs: JobWithRole[],
  state: JobFiltersState,
  maximumSalary: number | null,
): JobWithRole[] {
  const minimumSalary =
    state.openToAllSalary || !state.minimumSalary
      ? null
      : Number(state.minimumSalary)

  return jobs.filter((job) => {
    if (!salaryMatches(job, minimumSalary, maximumSalary)) return false
    if (!remoteMatches(state.workModels, job.remote_type)) return false
    if (!seniorityMatches(state.experienceLevels, job.seniority_level)) return false
    if (state.sponsorshipRequired && job.sponsorship_status !== "yes") return false
    if (state.excludeUsCitizenOnly && job.sponsorship_status === "no") return false
    return true
  })
}

export function estimateProfileAlignment(jobs: JobWithRole[]): number {
  if (jobs.length === 0) return 0.94
  const scores = jobs.map((j) => j.personal_score).filter((s) => s > 0)
  if (scores.length === 0) return 0.94
  return scores.reduce((sum, s) => sum + s, 0) / scores.length
}
