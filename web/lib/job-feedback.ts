export type NotInterestedReason =
  | "company"
  | "job_title"
  | "industry"
  | "skills"
  | "location"
  | "experience_level"
  | "work_authorization"
  | "other"

export type ReportIssueReason =
  | "scam"
  | "discriminatory"
  | "incorrect_info"
  | "no_longer_available"
  | "not_in_us"
  | "other"

export interface JobFeedbackEntry {
  jobId: string
  type: "not_interested" | "report_issue"
  reason: NotInterestedReason | ReportIssueReason
  submittedAt: string
}

function storageKey(candidateId: string) {
  return `cma_feedback_${candidateId}`
}

export function loadJobFeedback(candidateId: string): JobFeedbackEntry[] {
  if (typeof window === "undefined") return []
  try {
    const raw = localStorage.getItem(storageKey(candidateId))
    if (!raw) return []
    return JSON.parse(raw) as JobFeedbackEntry[]
  } catch {
    return []
  }
}

export function persistJobFeedback(candidateId: string, entries: JobFeedbackEntry[]) {
  localStorage.setItem(storageKey(candidateId), JSON.stringify(entries))
}

export function appendJobFeedback(
  candidateId: string,
  entry: Omit<JobFeedbackEntry, "submittedAt">,
) {
  const next = [
    ...loadJobFeedback(candidateId).filter((e) => !(e.jobId === entry.jobId && e.type === entry.type)),
    { ...entry, submittedAt: new Date().toISOString() },
  ]
  persistJobFeedback(candidateId, next)
  return next
}
