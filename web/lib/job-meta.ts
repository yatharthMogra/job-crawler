import type { EmploymentType, RemoteType, SeniorityLevel } from "@/lib/jobs-data"

export const EMP_LABEL: Record<EmploymentType, string> = {
  FULLTIME: "Full-time",
  PARTTIME: "Part-time",
  INTERNSHIP: "Internship",
  CONTRACT: "Contract",
}

export const REMOTE_LABEL: Record<RemoteType, string> = {
  remote: "Remote",
  hybrid: "Hybrid",
  onsite: "Onsite",
}

export const SENIORITY_LABEL: Record<SeniorityLevel, string> = {
  internship: "Internship",
  new_grad: "New Grad",
  early_career: "Early Career",
  entry: "Entry Level",
  mid: "Mid Level",
  senior: "Senior",
  staff: "Staff+",
}
