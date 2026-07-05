import type { JobWithRole } from "@/lib/jobs-data"

export type ApplicationPipelineStatus =
  | "submitted"
  | "under_review"
  | "online_assessment"
  | "interview"
  | "offer"

export const PIPELINE_STATUS_LABELS: Record<ApplicationPipelineStatus, string> = {
  submitted: "Active",
  under_review: "Under review",
  online_assessment: "Online assessment",
  interview: "Interview",
  offer: "Offer",
}

export const CARD_STATUS_OPTIONS: ApplicationPipelineStatus[] = [
  "submitted",
  "under_review",
  "online_assessment",
  "interview",
]

export const PIPELINE_STATUS_STYLES: Record<
  ApplicationPipelineStatus,
  { badge: string; counter: string }
> = {
  submitted: {
    badge: "bg-muted text-foreground/70",
    counter: "text-foreground",
  },
  under_review: {
    badge: "bg-sky-500/10 text-sky-800",
    counter: "text-foreground",
  },
  online_assessment: {
    badge: "bg-violet-500/10 text-violet-800",
    counter: "text-foreground",
  },
  interview: {
    badge: "bg-primary/10 text-primary",
    counter: "text-primary",
  },
  offer: {
    badge: "bg-emerald-500/10 text-emerald-800",
    counter: "text-emerald-700",
  },
}

export type ApplicationStatusFilter = "all" | ApplicationPipelineStatus

export interface ApplicationRecord {
  job: JobWithRole
  status: ApplicationPipelineStatus
  appliedAt: string
}

function mapApiStatus(status: string | undefined): ApplicationPipelineStatus {
  const value = (status ?? "").toLowerCase().replace(/-/g, "_").trim()
  if (!value || value === "applied" || value === "submitted" || value === "active") {
    return "submitted"
  }
  if (value.includes("online") || value.includes("assessment") || value === "oa") {
    return "online_assessment"
  }
  if (value.includes("interview")) return "interview"
  if (value.includes("offer")) return "offer"
  if (value.includes("review") || value.includes("screen")) return "under_review"
  return "submitted"
}

export function toApiStatus(status: ApplicationPipelineStatus): string {
  if (status === "submitted") return "applied"
  return status
}

export function derivePipelineStatus(
  job: JobWithRole,
  apiStatus?: string,
): ApplicationPipelineStatus {
  if (apiStatus ?? job.application_status) {
    return mapApiStatus(apiStatus ?? job.application_status)
  }
  return "submitted"
}

export function deriveAppliedAt(job: JobWithRole): string {
  if (job.posted_at) return job.posted_at
  return new Date().toISOString()
}

export function toApplicationRecord(
  job: JobWithRole,
  apiStatus?: string,
): ApplicationRecord {
  const status = derivePipelineStatus(job, apiStatus ?? job.application_status)
  return {
    job: { ...job, is_applied: true },
    status,
    appliedAt: deriveAppliedAt(job),
  }
}

export function countByStatus(records: ApplicationRecord[]) {
  return {
    all: records.length,
    submitted: records.filter((r) => r.status === "submitted").length,
    under_review: records.filter((r) => r.status === "under_review").length,
    online_assessment: records.filter((r) => r.status === "online_assessment").length,
    interview: records.filter((r) => r.status === "interview").length,
    offer: records.filter((r) => r.status === "offer").length,
  }
}

export function formatAppliedDate(iso: string): string {
  const date = new Date(iso)
  if (Number.isNaN(date.getTime())) return "Recently"
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  })
}
