import type { JobWithRole } from "@/lib/jobs-data"

export const DEFAULT_LOCATION = "United States"

export const DATE_POSTED_OPTIONS = [
  { value: "any", label: "Any time" },
  { value: "24h", label: "Past 24 hours" },
  { value: "3d", label: "Past 3 days" },
  { value: "1w", label: "Past week" },
] as const

export function ensureLocations(locations: string[] | null | undefined): string[] {
  const cleaned = (locations ?? []).map((l) => l.trim()).filter(Boolean)
  return cleaned.length > 0 ? cleaned : [DEFAULT_LOCATION]
}

export function applyDatePostedFilter(job: JobWithRole, value: string | null): boolean {
  if (!value || value === "any") return true
  const ageHours = (Date.now() - new Date(job.posted_at).getTime()) / 3_600_000
  if (value === "24h") return ageHours <= 24
  if (value === "3d") return ageHours <= 72
  if (value === "1w") return ageHours <= 168
  return true
}

export function applyLocationFilter(job: JobWithRole, location: string | null): boolean {
  if (!location || location === DEFAULT_LOCATION) {
    // Country-level US: keep US-ish and remote US listings; exclude explicit non-US only when we can tell.
    const loc = job.location.toLowerCase()
    if (loc.includes("global") && !loc.includes("us") && !loc.includes("united states")) {
      return job.remote_type === "remote"
    }
    return true
  }
  const needle = location.toLowerCase()
  return job.location.toLowerCase().includes(needle)
}
