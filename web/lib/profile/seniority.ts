import { EXPERIENCE_LEVELS } from "@/lib/profile/job-filters-constants"

export const DEFAULT_TARGET_SENIORITY = ["INTERN", "NEW_GRAD", "ENTRY", "MID", "JUNIOR"] as const

export const EXPERIENCE_TO_SENIORITY: Record<string, string[]> = {
  "Intern/New Grad": ["INTERN", "NEW_GRAD"],
  "Entry Level": ["ENTRY", "JUNIOR"],
  "Mid Level": ["MID"],
  "Senior Level": ["SENIOR"],
  "Lead/Staff": ["STAFF", "PRINCIPAL"],
  "Director/Executive": ["MANAGEMENT"],
}

const SENIORITY_TO_EXPERIENCE: Record<string, string> = {}
for (const [experience, levels] of Object.entries(EXPERIENCE_TO_SENIORITY)) {
  for (const level of levels) {
    SENIORITY_TO_EXPERIENCE[level] = experience
  }
}

export function experienceLevelsToTargetSeniority(experienceLevels: string[]): string[] {
  if (experienceLevels.length === 0) {
    return [...DEFAULT_TARGET_SENIORITY]
  }
  const levels = new Set<string>()
  for (const experience of experienceLevels) {
    for (const level of EXPERIENCE_TO_SENIORITY[experience] ?? []) {
      levels.add(level)
    }
  }
  return levels.size > 0 ? [...levels] : [...DEFAULT_TARGET_SENIORITY]
}

export function targetSeniorityToExperienceLevels(targetSeniority: string[] | undefined): string[] {
  if (!targetSeniority?.length) {
    return []
  }
  const experiences = new Set<string>()
  for (const level of targetSeniority) {
    const experience = SENIORITY_TO_EXPERIENCE[level.toUpperCase()]
    if (experience) {
      experiences.add(experience)
    }
  }
  return EXPERIENCE_LEVELS.filter((level) => experiences.has(level))
}

export function mapApiSeniorityToUi(
  seniority: string | null | undefined,
): import("@/lib/jobs-data").SeniorityLevel {
  const normalized = (seniority ?? "UNKNOWN").toUpperCase()
  switch (normalized) {
    case "INTERN":
      return "internship"
    case "NEW_GRAD":
      return "new_grad"
    case "ENTRY":
    case "JUNIOR":
      return "entry"
    case "MID":
      return "mid"
    case "SENIOR":
      return "senior"
    case "STAFF":
    case "PRINCIPAL":
      return "staff"
    case "MANAGEMENT":
      return "staff"
    default:
      return "mid"
  }
}
