import type { CandidateResponse, EvidenceResponse, ProfileResponse, ResumeResponse } from "@/lib/api-types"
import type { CommittedProfile } from "@/lib/build-profile"
import { withDefaultProfileFields } from "@/lib/build-profile"
import {
  contactFromEducationJson,
  educationEntriesFromProfile,
  resumeSectionOrderFromProfile,
  type ContactInfo,
  type EducationEntry,
  type ResumeSectionOrder,
} from "@/lib/contact"
import { eeoFromApiPayload, eeoToDisplayRows, type EeoState } from "@/lib/eeo"
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

function formatConstraintLabel(key: string): string {
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

export interface ProfileResumeItem {
  id: string
  originalFilename: string
  displayLabel: string | null
  uploadedAt: string
  fileSizeBytes: number
}

export interface ProfileHomeData {
  candidateName: string
  email: string
  contact: ContactInfo
  educationEntries: EducationEntry[]
  resumeSectionOrder: ResumeSectionOrder
  eeo: EeoState
  eeoRows: { label: string; value: string }[]
  profile: CommittedProfile
  primaryRoles: string[]
  secondaryRoles: string[]
  hasTargetRoles: boolean
  resumes: ProfileResumeItem[]
  constraints: { label: string; value: string }[]
  preferences: { label: string; value: string }[]
  version: number
  lastUpdated: string
  resumeCount: number
}

export function mapApiToProfileHome(
  candidate: CandidateResponse,
  profile: ProfileResponse,
  evidence: EvidenceResponse[],
  resumes: ResumeResponse[],
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

  const constraintsEntries = Object.entries(profile.constraints ?? {})
    .filter(([key, v]) => key !== "eeo" && v !== null && v !== undefined && v !== "")
    .map(([key, value]) => ({
      label: formatConstraintLabel(key),
      value: formatConstraintValue(key, value),
    }))

  if (profile.constraints) {
    constraintsEntries.push({
      label: "Role Type",
      value: deriveRoleType(profile.constraints),
    })
  }

  const primaryRoles = (profile.preferences?.primary_roles as string[]) ?? []
  const secondaryRoles = (profile.preferences?.secondary_roles as string[]) ?? []

  const preferencesEntries = Object.entries(profile.preferences ?? {})
    .filter(([key, v]) => {
      if (key === "primary_roles" || key === "secondary_roles" || key === "dream_companies") {
        return false
      }
      return v !== null && v !== undefined && v !== "" && !(Array.isArray(v) && v.length === 0)
    })
    .map(([key, value]) => ({
      label: formatPreferenceLabel(key),
      value: formatPreferenceValue(value),
    }))

  const resumeItems: ProfileResumeItem[] = resumes.map((r) => ({
    id: r.id,
    originalFilename: r.original_filename,
    displayLabel: r.display_label ?? null,
    uploadedAt: r.uploaded_at,
    fileSizeBytes: r.file_size_bytes,
  }))

  const contact = contactFromEducationJson(profile.education)
  const educationEntries = educationEntriesFromProfile(profile.education)
  const resumeSectionOrder = resumeSectionOrderFromProfile(profile.education)
  const eeo = eeoFromApiPayload(profile.constraints?.eeo as Record<string, unknown> | undefined)

  const committedProfile = withDefaultProfileFields({
    skills: skillGroups,
    skillCount: skillGroups.reduce((n, g) => n + g.names.length, 0),
    experiences,
    projects,
    certifications,
    contact,
    educationEntries,
    resumeSectionOrder,
    eeo,
    primaryRoles,
    secondaryRoles,
    preferences: [...constraintsEntries, ...preferencesEntries],
  })

  return {
    candidateName: candidate.name,
    email: candidate.email,
    contact,
    educationEntries,
    resumeSectionOrder,
    eeo,
    eeoRows: eeoToDisplayRows(eeo),
    profile: committedProfile,
    primaryRoles,
    secondaryRoles,
    hasTargetRoles: primaryRoles.length > 0,
    resumes: resumeItems,
    constraints: constraintsEntries,
    preferences: preferencesEntries,
    version: profile.version,
    lastUpdated: profile.created_at,
    resumeCount: resumes.length,
  }
}

export function buildConfirmationProfile(reviewState: ReviewState): CommittedProfile {
  return buildCommittedProfile(reviewState)
}

export function buildConfirmationFromProfileHome(data: ProfileHomeData): CommittedProfile {
  return data.profile
}

export function formatRelativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  if (hours < 1) return "just now"
  if (hours < 24) return `${hours} hour${hours === 1 ? "" : "s"} ago`
  const days = Math.floor(hours / 24)
  return `${days} day${days === 1 ? "" : "s"} ago`
}
