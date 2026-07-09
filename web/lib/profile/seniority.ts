import type { SeniorityLevel } from "@/lib/jobs-data"
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

export const UI_SENIORITY_TO_TARGET: Record<SeniorityLevel, string[]> = {
  internship: ["INTERN"],
  new_grad: ["NEW_GRAD"],
  early_career: ["ENTRY", "JUNIOR"],
  entry: ["ENTRY", "JUNIOR"],
  mid: ["MID"],
  senior: ["SENIOR"],
  staff: ["STAFF", "PRINCIPAL"],
}

export const JOB_INTENT_EXPERIENCE_LEVEL_OPTIONS: {
  value: SeniorityLevel | "any"
  label: string
}[] = [
  { value: "any", label: "Any level" },
  { value: "internship", label: "Internship" },
  { value: "new_grad", label: "New Grad" },
  { value: "mid", label: "Mid Level" },
  { value: "senior", label: "Senior" },
  { value: "staff", label: "Staff+" },
]

export function uiSeniorityToTargetSeniority(level: SeniorityLevel): string[] {
  return UI_SENIORITY_TO_TARGET[level] ?? []
}

export function targetSeniorityToUiSeniority(
  targetSeniority: string[] | undefined,
): SeniorityLevel | null {
  if (!targetSeniority?.length) {
    return null
  }
  const normalized = new Set(targetSeniority.map((level) => level.toUpperCase()))
  if (
    normalized.has("STAFF") ||
    normalized.has("PRINCIPAL") ||
    normalized.has("MANAGEMENT")
  ) {
    return "staff"
  }
  if (normalized.has("SENIOR")) return "senior"
  if (normalized.has("MID")) return "mid"
  if (normalized.has("INTERN")) return "internship"
  if (normalized.has("NEW_GRAD")) return "new_grad"
  if (normalized.has("ENTRY") || normalized.has("JUNIOR")) return "entry"
  return null
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
