import type {
  CandidateResponse,
  CapabilityResponse,
  EvidenceResponse,
  ProfileResponse,
} from "@/lib/api-types"
import type { CommittedProfile } from "@/lib/build-profile"
import type { ReviewState } from "@/lib/profile-data"
import { buildCommittedProfile } from "@/lib/build-profile"

const SKILL_CATEGORY_LABELS: Record<string, string> = {
  languages: "Languages",
  frameworks: "Frameworks",
  databases: "Databases",
  cloud: "Cloud",
  ai_ml: "AI / ML",
  infrastructure: "Infrastructure",
  product: "Product",
}

function formatEducationLine(education: Record<string, unknown>): string {
  const parts: string[] = []
  if (education.degree) parts.push(String(education.degree))
  if (education.university) parts.push(String(education.university))
  if (education.graduation_date) {
    const date = String(education.graduation_date)
    parts.push(`Graduating ${date.length === 7 ? date.replace("-", " ") : date}`)
  }
  return parts.join(" · ")
}

function formatConstraintLabel(key: string, value: unknown): string {
  const labels: Record<string, string> = {
    sponsorship_required: "Sponsorship Required",
    visa_type: "Visa Type",
    work_authorization: "Work Authorization",
    internship_only: "Internship Only",
    fulltime_only: "Fulltime Only",
    minimum_salary: "Minimum Salary",
    minimum_hourly_rate: "Minimum Hourly Rate",
  }
  return labels[key] ?? key
}

function formatConstraintValue(key: string, value: unknown): string {
  if (value === null || value === undefined) return "—"
  if (typeof value === "boolean") return value ? "Yes" : "No"
  if (key === "minimum_hourly_rate") return `$${value}/hr`
  if (key === "minimum_salary") return `$${Number(value).toLocaleString()}`
  return String(value)
}

function formatPreferenceLabel(key: string): string {
  const labels: Record<string, string> = {
    primary_roles: "Primary Roles",
    secondary_roles: "Secondary Roles",
    preferred_locations: "Preferred Locations",
    acceptable_locations: "Acceptable Locations",
    remote_preference: "Remote Preference",
    relocation_allowed: "Relocation Allowed",
    preferred_company_stages: "Preferred Company Stages",
    preferred_industries: "Preferred Industries",
  }
  return labels[key] ?? key
}

function formatPreferenceValue(value: unknown): string {
  if (value === null || value === undefined) return "—"
  if (typeof value === "boolean") return value ? "Yes" : "No"
  if (Array.isArray(value)) return value.join(" · ")
  return String(value)
}

function deriveRoleType(constraints: Record<string, unknown>): string {
  const intern = Boolean(constraints.internship_only)
  const fulltime = Boolean(constraints.fulltime_only)
  if (intern && fulltime) return "Both internship and full-time"
  if (intern) return "Internship only"
  if (fulltime) return "Full-time only"
  return "Open to both"
}

export interface ProfileHomeData {
  candidateName: string
  educationLine: string
  profile: CommittedProfile
  constraints: { label: string; value: string }[]
  preferences: { label: string; value: string }[]
  version: number
  lastUpdated: string
  resumeCount: number
}

export function mapApiToProfileHome(
  candidate: CandidateResponse,
  profile: ProfileResponse,
  capabilities: CapabilityResponse[],
  evidence: EvidenceResponse[],
  resumeCount: number,
): ProfileHomeData {
  const experiences = evidence
    .filter((e) => e.evidence_type === "experience")
    .map((e) => ({
      id: e.id,
      title: String(e.normalized_data.title ?? ""),
      company: String(e.normalized_data.company ?? ""),
      durationMonths: Number(e.normalized_data.duration_months ?? 0),
      domains: (e.normalized_data.domains as string[]) ?? [],
      keywords: (e.normalized_data.evidence_keywords as string[]) ?? [],
    }))

  const projects = evidence
    .filter((e) => e.evidence_type === "project")
    .map((e) => {
      const domains = (e.normalized_data.domains as string[]) ?? []
      return {
        id: e.id,
        name: String(e.normalized_data.name ?? ""),
        type: String(e.normalized_data.category ?? ""),
        domain: domains[0] ?? "",
        keywords: (e.normalized_data.evidence_keywords as string[]) ?? [],
      }
    })

  const certifications = evidence
    .filter((e) => e.evidence_type === "certification")
    .map((e) => ({
      id: e.id,
      name: String(e.normalized_data.name ?? ""),
      issuer: String(e.normalized_data.issuer ?? ""),
    }))

  const skillGroups = Object.entries(profile.skills ?? {})
    .filter(([, values]) => values.length > 0)
    .map(([key, names]) => ({
      category: SKILL_CATEGORY_LABELS[key] ?? key,
      names,
    }))

  const caps = capabilities.map((c) => ({
    name: c.capability_name,
    evidence: c.supporting_evidence,
    depth: c.supporting_evidence.length,
  }))

  const constraintsEntries = Object.entries(profile.constraints ?? {})
    .filter(([, v]) => v !== null && v !== undefined && v !== "")
    .map(([key, value]) => ({
      label: formatConstraintLabel(key, value),
      value: formatConstraintValue(key, value),
    }))

  if (profile.constraints) {
    constraintsEntries.push({
      label: "Role Type",
      value: deriveRoleType(profile.constraints),
    })
  }

  const preferencesEntries = Object.entries(profile.preferences ?? {})
    .filter(([, v]) => v !== null && v !== undefined && v !== "" && !(Array.isArray(v) && v.length === 0))
    .map(([key, value]) => ({
      label: formatPreferenceLabel(key),
      value: formatPreferenceValue(value),
    }))

  const committedProfile: CommittedProfile = {
    skills: skillGroups,
    skillCount: skillGroups.reduce((n, g) => n + g.names.length, 0),
    experiences,
    projects,
    certifications,
    capabilities: caps,
    preferences: [...constraintsEntries, ...preferencesEntries],
  }

  return {
    candidateName: candidate.name,
    educationLine: formatEducationLine(profile.education ?? {}),
    profile: committedProfile,
    constraints: constraintsEntries,
    preferences: preferencesEntries,
    version: profile.version,
    lastUpdated: profile.created_at,
    resumeCount,
  }
}

export function buildConfirmationProfile(
  reviewState: ReviewState,
  capabilities: CapabilityResponse[],
): CommittedProfile {
  const local = buildCommittedProfile(reviewState)
  local.capabilities = capabilities.map((c) => ({
    name: c.capability_name,
    evidence: c.supporting_evidence,
    depth: c.supporting_evidence.length,
  }))
  return local
}

export function formatRelativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  if (hours < 1) return "just now"
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`
  const days = Math.floor(hours / 24)
  return `${days} day${days === 1 ? "" : "s"} ago`
}
