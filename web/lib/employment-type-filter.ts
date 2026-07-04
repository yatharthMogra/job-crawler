import type { EmploymentType } from "@/lib/jobs-data"

export type EmploymentTypeFilter = "FULLTIME" | "PARTTIME" | "INTERNSHIP" | null

export function employmentTypeFromFlags(fulltimeOnly: boolean, internshipOnly: boolean): EmploymentTypeFilter {
  if (fulltimeOnly && !internshipOnly) return "FULLTIME"
  if (internshipOnly && !fulltimeOnly) return "INTERNSHIP"
  return null
}

export function flagsFromEmploymentType(type: EmploymentTypeFilter): {
  fulltimeOnly: boolean
  internshipOnly: boolean
} {
  if (type === "FULLTIME") return { fulltimeOnly: true, internshipOnly: false }
  if (type === "INTERNSHIP") return { fulltimeOnly: false, internshipOnly: true }
  return { fulltimeOnly: false, internshipOnly: false }
}

export function matchesEmploymentTypeFilter(
  jobType: EmploymentType,
  filter: EmploymentTypeFilter,
): boolean {
  if (!filter) return true
  return jobType === filter
}
