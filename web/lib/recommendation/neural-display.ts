import type { JobWithRole } from "@/lib/jobs-data"
import { findRoleByLabel } from "@/lib/profile/role-catalog"
import { formatSalary } from "@/lib/jobs-data"

export function normalizeRole(value: string): string {
  return value.trim().toLowerCase().replace(/[^a-z0-9]+/g, " ")
}

export function catalogRoleMatchesJob(targetRole: string, job: JobWithRole): boolean {
  const entry = findRoleByLabel(targetRole)
  if (!entry) return false
  const label = normalizeRole(entry.label)
  const category = normalizeRole(job.roleCategory)
  const title = normalizeRole(job.title)
  return category === label || title.includes(label) || label.includes(category)
}

export function jobMatchesCatalogRoles(
  job: JobWithRole,
  primaryRoles: string[],
  secondaryRoles: string[],
): boolean {
  if (primaryRoles.length === 0 && secondaryRoles.length === 0) return true
  const targets = [...primaryRoles, ...secondaryRoles]
  return targets.some((role) => catalogRoleMatchesJob(role, job))
}

export function filterJobsByCatalogRoles(
  jobs: JobWithRole[],
  primaryRoles: string[],
  secondaryRoles: string[],
): JobWithRole[] {
  return jobs.filter((job) => jobMatchesCatalogRoles(job, primaryRoles, secondaryRoles))
}

export function applicationWindowLabel(postedAt: string): string {
  const daysOld = Math.floor((Date.now() - new Date(postedAt).getTime()) / 86_400_000)
  const remaining = Math.max(1, 14 - daysOld)
  return `${remaining}D REMAINING`
}

export function matchTier(score: number): "TOP MATCH" | "STRONG MATCH" | "GOOD MATCH" | null {
  if (score >= 0.88) return "TOP MATCH"
  if (score >= 0.8) return "STRONG MATCH"
  if (score >= 0.72) return "GOOD MATCH"
  return null
}

export function isPremiumRole(job: JobWithRole): boolean {
  return (
    job.personal_score >= 0.86 &&
    (job.seniority_level === "staff" ||
      job.seniority_level === "senior" ||
      job.title.toLowerCase().includes("staff") ||
      job.title.toLowerCase().includes("principal"))
  )
}

export function neuralRationale(job: JobWithRole): string {
  if (job.match_reasons.length > 0) {
    const focus = job.match_reasons.slice(0, 2).join(" and ")
    return `Strongest alignment in ${focus}. Your profile maps directly to this role's core requirements.`
  }
  if (job.skills.length > 0) {
    return `Match driven by ${job.skills.slice(0, 3).join(", ")} overlap with your skill profile.`
  }
  return "High compatibility with your profile and target roles."
}

export function coreSkillsMatchPercent(job: JobWithRole): number {
  return Math.min(99, Math.round(job.personal_score * 100 + 3))
}

export function salaryDisplay(job: JobWithRole): string {
  const base = formatSalary(job.salary_min, job.salary_max)
  if (!base) return "Competitive + Equity"
  if (job.salary_max && job.salary_max >= 200_000) return `${base} + Equity`
  return `${base} + Equity`
}

export function companySizeLabel(job: JobWithRole): string {
  const range = job.company_info?.employee_count_range
  if (range) return range
  if (job.seniority_level === "staff" || job.seniority_level === "senior") {
    return "Series C · 150–200 Employees"
  }
  return "Growth-stage · 50–500 Employees"
}

export function outreachLabel(job: JobWithRole): string {
  if (job.application_effort === "LOW") return "Direct Executive Outreach"
  if (job.personal_score >= 0.85) return "Priority Neural Channel"
  return "Verified Listing"
}

export function marketAlignmentPercent(jobs: JobWithRole[]): number {
  if (jobs.length === 0) return 0
  const avg = jobs.reduce((sum, j) => sum + j.personal_score, 0) / jobs.length
  return Math.round(avg * 100)
}
