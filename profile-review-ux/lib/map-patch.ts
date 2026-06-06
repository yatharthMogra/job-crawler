import type { PendingPatchResponse, PatchOperationResponse } from "@/lib/api-types"
import type {
  CertificationChange,
  EducationChange,
  ExperienceChange,
  PreferenceSuggestion,
  ProjectChange,
  ReviewState,
  SkillChange,
} from "@/lib/profile-data"

const SKILL_CATEGORY_LABELS: Record<string, string> = {
  languages: "Languages",
  frameworks: "Frameworks",
  databases: "Databases",
  cloud: "Cloud",
  ai_ml: "AI / ML",
  infrastructure: "Infrastructure",
  product: "Product",
}

const CONSTRAINT_FIELDS = new Set([
  "sponsorship_required",
  "visa_type",
  "work_authorization",
  "internship_only",
  "fulltime_only",
  "minimum_salary",
  "minimum_hourly_rate",
])

const FIELD_LABELS: Record<string, string> = {
  sponsorship_required: "Sponsorship Required",
  visa_type: "Visa Type",
  work_authorization: "Work Authorization",
  internship_only: "Internship Only",
  fulltime_only: "Fulltime Only",
  minimum_salary: "Minimum Salary",
  minimum_hourly_rate: "Minimum Hourly Rate",
  primary_roles: "Primary Roles",
  secondary_roles: "Secondary Roles",
  preferred_locations: "Preferred Locations",
  acceptable_locations: "Acceptable Locations",
  remote_preference: "Remote Preference",
  relocation_allowed: "Relocation Allowed",
  preferred_company_stages: "Preferred Company Stages",
  preferred_industries: "Preferred Industries",
}

function formatSuggestionValue(value: unknown): string {
  if (value === null || value === undefined) return ""
  if (typeof value === "boolean") return value ? "Yes" : "No"
  if (Array.isArray(value)) return value.join(", ")
  return String(value)
}

function mapSkill(op: PatchOperationResponse): SkillChange {
  const category = SKILL_CATEGORY_LABELS[op.category ?? ""] ?? op.category ?? "Other"
  return {
    id: op.id,
    kind: "add",
    category,
    name: op.value ?? "",
    status: "pending",
  }
}

function mapAddExperience(op: PatchOperationResponse): ExperienceChange {
  const data = op.data ?? {}
  return {
    id: op.id,
    operationIds: [op.id],
    kind: "add",
    status: "pending",
    title: String(data.title ?? ""),
    company: String(data.company ?? ""),
    durationMonths: Number(data.duration_months ?? 0),
    domains: (data.domains as string[]) ?? [],
    keywords: (data.evidence_keywords as string[]) ?? [],
  }
}

function mergeExperienceUpdates(ops: PatchOperationResponse[]): ExperienceChange {
  const first = ops[0]
  const evidenceId = first.evidence_id ?? first.id
  let title = ""
  let company = ""
  let durationMonths = 0
  let previousDurationMonths: number | undefined
  let domains: string[] = []
  let keywords: string[] = []
  let newKeywords: string[] | undefined

  for (const op of ops) {
    if (op.field === "title") title = String(op.to ?? "")
    if (op.field === "company") company = String(op.to ?? "")
    if (op.field === "duration_months") {
      durationMonths = Number(op.to ?? 0)
      previousDurationMonths = Number(op.from_value ?? 0)
    }
    if (op.field === "domains") domains = (op.to as string[]) ?? []
    if (op.field === "evidence_keywords") {
      keywords = (op.to as string[]) ?? []
      const prev = (op.from_value as string[]) ?? []
      newKeywords = keywords.filter((k) => !prev.includes(k))
    }
  }

  return {
    id: evidenceId,
    operationIds: ops.map((o) => o.id),
    kind: "update",
    status: "pending",
    title,
    company,
    durationMonths,
    previousDurationMonths,
    domains,
    keywords,
    newKeywords,
  }
}

function mapAddProject(op: PatchOperationResponse): ProjectChange {
  const data = op.data ?? {}
  const domains = (data.domains as string[]) ?? []
  return {
    id: op.id,
    operationIds: [op.id],
    kind: "add",
    status: "pending",
    name: String(data.name ?? ""),
    type: String(data.category ?? ""),
    domain: domains[0] ?? "",
    keywords: (data.evidence_keywords as string[]) ?? [],
  }
}

function mergeProjectUpdates(ops: PatchOperationResponse[]): ProjectChange {
  const first = ops[0]
  const evidenceId = first.evidence_id ?? first.id
  let name = ""
  let type = ""
  let domain = ""
  let keywords: string[] = []

  for (const op of ops) {
    if (op.field === "category") type = String(op.to ?? "")
    if (op.field === "domains") {
      const domains = (op.to as string[]) ?? []
      domain = domains[0] ?? domain
    }
    if (op.field === "evidence_keywords") keywords = (op.to as string[]) ?? []
  }

  return {
    id: evidenceId,
    operationIds: ops.map((o) => o.id),
    kind: "update",
    status: "pending",
    name,
    type,
    domain,
    keywords,
  }
}

function mapCertification(op: PatchOperationResponse): CertificationChange {
  const data = op.data ?? {}
  return {
    id: op.id,
    operationIds: [op.id],
    kind: "add",
    status: "pending",
    name: String(data.name ?? ""),
    issuer: String(data.issuer ?? ""),
  }
}

function mapEducation(op: PatchOperationResponse): EducationChange {
  if (op.op === "ADD_EDUCATION") {
    const data = op.data ?? {}
    return {
      id: op.id,
      operationIds: [op.id],
      kind: "add",
      status: "pending",
      degree: String(data.degree ?? ""),
      university: String(data.university ?? ""),
      graduationDate: String(data.graduation_date ?? ""),
    }
  }

  return {
    id: op.id,
    operationIds: [op.id],
    kind: "update",
    status: "pending",
    degree: op.field === "degree" ? String(op.to ?? "") : "",
    university: op.field === "university" ? String(op.to ?? "") : "",
    graduationDate: op.field === "graduation_date" ? String(op.to ?? "") : "",
    previousDegree: op.field === "degree" ? String(op.from_value ?? "") : undefined,
    previousUniversity: op.field === "university" ? String(op.from_value ?? "") : undefined,
    previousGraduationDate: op.field === "graduation_date" ? String(op.from_value ?? "") : undefined,
  }
}

function mapSuggestion(op: PatchOperationResponse): PreferenceSuggestion {
  const field = op.field ?? ""
  const suggested = op.suggested_value
  const isRate = field === "minimum_hourly_rate"
  const formatted = formatSuggestionValue(suggested)

  return {
    id: op.id,
    label: FIELD_LABELS[field] ?? field,
    suggestion: isRate && !formatted ? "Not detected" : formatted || "Not detected",
    detail: op.reason ?? undefined,
    detected: suggested !== null && suggested !== undefined && formatted !== "",
    value: formatted,
    status: "pending",
    kind: isRate ? "input" : "text",
    isConstraint: CONSTRAINT_FIELDS.has(field),
  }
}

function groupByEvidenceId(ops: PatchOperationResponse[]): Map<string, PatchOperationResponse[]> {
  const groups = new Map<string, PatchOperationResponse[]>()
  for (const op of ops) {
    const key = op.evidence_id ?? op.id
    const list = groups.get(key) ?? []
    list.push(op)
    groups.set(key, list)
  }
  return groups
}

export function mapPendingPatchToReviewState(patch: PendingPatchResponse): ReviewState {
  const experiences: ExperienceChange[] = []
  const addExps = patch.experiences.filter((o) => o.op === "ADD_EXPERIENCE")
  const updateExps = patch.experiences.filter((o) => o.op === "UPDATE_EXPERIENCE")
  experiences.push(...addExps.map(mapAddExperience))
  for (const [, ops] of groupByEvidenceId(updateExps)) {
    experiences.push(mergeExperienceUpdates(ops))
  }

  const projects: ProjectChange[] = []
  const addProjects = patch.projects.filter((o) => o.op === "ADD_PROJECT")
  const updateProjects = patch.projects.filter((o) => o.op === "UPDATE_PROJECT")
  projects.push(...addProjects.map(mapAddProject))
  for (const [, ops] of groupByEvidenceId(updateProjects)) {
    projects.push(mergeProjectUpdates(ops))
  }

  const education = patch.education.map(mapEducation)
  const constraints = patch.constraints.map(mapSuggestion)
  const preferences = patch.preferences.map(mapSuggestion)

  return {
    skills: patch.skills.map(mapSkill),
    experiences,
    projects,
    certifications: patch.certifications.map(mapCertification),
    education,
    preferences: [...constraints, ...preferences],
  }
}

export function collectApprovedOperationIds(state: ReviewState): string[] {
  const ids: string[] = []

  const collect = (items: { id: string; status: string; operationIds?: string[] }[], approvedStatus: string) => {
    for (const item of items) {
      if (item.status === approvedStatus) {
        if (item.operationIds?.length) {
          ids.push(...item.operationIds)
        } else {
          ids.push(item.id)
        }
      }
    }
  }

  collect(state.skills, "approved")
  collect(state.experiences, "approved")
  collect(state.projects, "approved")
  collect(state.certifications, "approved")
  collect(state.education, "approved")
  collect(
    state.preferences.map((p) => ({ id: p.id, status: p.status, operationIds: [p.id] })),
    "confirmed",
  )

  return ids
}

export function emptyReviewState(): ReviewState {
  return {
    skills: [],
    experiences: [],
    projects: [],
    certifications: [],
    education: [],
    preferences: [],
  }
}
