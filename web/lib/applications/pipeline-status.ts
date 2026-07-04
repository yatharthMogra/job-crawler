import type { JobWithRole } from "@/lib/jobs-data"

export type ApplicationPipelineStatus = "submitted" | "under_review" | "interview" | "offer"

export const PIPELINE_STATUS_LABELS: Record<ApplicationPipelineStatus, string> = {
  submitted: "Applied",
  under_review: "Under review",
  interview: "Interviewing",
  offer: "Offer",
}

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

function hashId(id: string): number {
  return id.split("").reduce((sum, char) => sum + char.charCodeAt(0), 0)
}

function mapApiStatus(status: string | undefined): ApplicationPipelineStatus {
  const value = (status ?? "").toLowerCase()
  if (value.includes("interview")) return "interview"
  if (value.includes("offer")) return "offer"
  if (value.includes("review") || value.includes("screen")) return "under_review"
  return "submitted"
}

export function derivePipelineStatus(
  job: JobWithRole,
  apiStatus?: string,
): ApplicationPipelineStatus {
  if (apiStatus) return mapApiStatus(apiStatus)
  const bucket = hashId(job.id) % 10
  if (bucket >= 8) return "interview"
  if (bucket >= 5) return "under_review"
  return "submitted"
}

export function deriveAppliedAt(job: JobWithRole): string {
  if (job.posted_at) return job.posted_at
  const daysAgo = (hashId(job.id) % 14) + 1
  const date = new Date()
  date.setDate(date.getDate() - daysAgo)
  return date.toISOString()
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
