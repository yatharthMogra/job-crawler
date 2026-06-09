import type { EvidenceResponse, PendingPatchResponse, PatchOperationResponse } from "@/lib/profile/api-types"
import { emptyContact } from "@/lib/profile/contact"
import type {
  CertificationChange,
  ContactChange,
  EducationChange,
  EducationLevel,
  ExperienceChange,
  PreferenceSuggestion,
  ProjectChange,
  ReviewState,
  SkillChange,
} from "@/lib/profile/profile-data"

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

function buildEvidenceIndex(evidence: EvidenceResponse[]): Map<string, EvidenceResponse> {
  return new Map(evidence.map((item) => [item.id, item]))
}

function experienceBaseline(
  evidenceById: Map<string, EvidenceResponse>,
  evidenceId: string,
) {
  const data = evidenceById.get(evidenceId)?.normalized_data ?? {}
  return {
    title: String(data.title ?? ""),
    company: String(data.company ?? ""),
    durationMonths: Number(data.duration_months ?? 0),
    domains: (data.domains as string[]) ?? [],
    keywords: (data.evidence_keywords as string[]) ?? [],
  }
}

function mergeExperienceUpdates(
  ops: PatchOperationResponse[],
  evidenceById: Map<string, EvidenceResponse>,
): ExperienceChange {
  const first = ops[0]
  const evidenceId = first.evidence_id ?? first.id
  const baseline = experienceBaseline(evidenceById, evidenceId)

  let title = baseline.title
  let company = baseline.company
  let durationMonths = baseline.durationMonths
  let domains = baseline.domains
  let keywords = baseline.keywords
  let previousTitle: string | undefined
  let previousCompany: string | undefined
  let previousDurationMonths: number | undefined
  let previousDomains: string[] | undefined
  let newKeywords: string[] | undefined

  for (const op of ops) {
    if (op.field === "title") {
      previousTitle = String(op.from_value ?? baseline.title)
      title = String(op.to ?? "")
    }
    if (op.field === "company") {
      previousCompany = String(op.from_value ?? baseline.company)
      company = String(op.to ?? "")
    }
    if (op.field === "duration_months") {
      previousDurationMonths = Number(op.from_value ?? baseline.durationMonths)
      durationMonths = Number(op.to ?? 0)
    }
    if (op.field === "domains") {
      previousDomains = (op.from_value as string[]) ?? baseline.domains
      domains = (op.to as string[]) ?? []
    }
    if (op.field === "evidence_keywords") {
      keywords = (op.to as string[]) ?? []
      const prev = (op.from_value as string[]) ?? baseline.keywords
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
    previousTitle,
    previousCompany,
    previousDurationMonths,
    domains,
    previousDomains,
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

function projectBaseline(evidenceById: Map<string, EvidenceResponse>, evidenceId: string) {
  const data = evidenceById.get(evidenceId)?.normalized_data ?? {}
  const domains = (data.domains as string[]) ?? []
  return {
    name: String(data.name ?? ""),
    type: String(data.category ?? ""),
    domain: domains[0] ?? "",
    keywords: (data.evidence_keywords as string[]) ?? [],
  }
}

function mergeProjectUpdates(
  ops: PatchOperationResponse[],
  evidenceById: Map<string, EvidenceResponse>,
): ProjectChange {
  const first = ops[0]
  const evidenceId = first.evidence_id ?? first.id
  const baseline = projectBaseline(evidenceById, evidenceId)

  let name = baseline.name
  let type = baseline.type
  let domain = baseline.domain
  let keywords = baseline.keywords
  let previousType: string | undefined
  let previousDomain: string | undefined
  let newKeywords: string[] | undefined

  for (const op of ops) {
    if (op.field === "category") {
      previousType = String(op.from_value ?? baseline.type)
      type = String(op.to ?? "")
    }
    if (op.field === "domains") {
      const prevDomains = (op.from_value as string[]) ?? []
      previousDomain = prevDomains[0] ?? baseline.domain
      const nextDomains = (op.to as string[]) ?? []
      domain = nextDomains[0] ?? domain
    }
    if (op.field === "evidence_keywords") {
      keywords = (op.to as string[]) ?? []
      const prev = (op.from_value as string[]) ?? baseline.keywords
      newKeywords = keywords.filter((k) => !prev.includes(k))
    }
  }

  return {
    id: evidenceId,
    operationIds: ops.map((o) => o.id),
    kind: "update",
    status: "pending",
    name,
    type,
    previousType,
    domain,
    previousDomain,
    keywords,
    newKeywords,
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

function inferEducationLevel(degree: string): EducationLevel {
  if (/^(ms|m\.s|master|mba)/i.test(degree)) return "masters"
  if (/^(bs|b\.s|b\.tech|bachelor|ba|b\.a)/i.test(degree)) return "undergrad"
  if (/^(phd|doctor)/i.test(degree)) return "doctoral"
  return "other"
}

function mapEducation(op: PatchOperationResponse): EducationChange {
  if (op.op === "ADD_EDUCATION" || op.op === "ADD_EDUCATION_ENTRY") {
    const data = op.data ?? {}
    const degree = String(data.degree ?? "")
    return {
      id: op.id,
      operationIds: [op.id],
      kind: "add",
      status: "pending",
      level: (data.level as EducationLevel) ?? inferEducationLevel(degree),
      degree,
      university: String(data.university ?? ""),
      graduationDate: String(data.graduation_date ?? ""),
      gpa: String(data.gpa ?? ""),
    }
  }

  return {
    id: op.id,
    operationIds: [op.id],
    kind: "update",
    status: "pending",
    level: "other",
    degree: op.field === "degree" ? String(op.to ?? "") : "",
    university: op.field === "university" ? String(op.to ?? "") : "",
    graduationDate: op.field === "graduation_date" ? String(op.to ?? "") : "",
    gpa: op.field === "gpa" ? String(op.to ?? "") : "",
    previousDegree: op.field === "degree" ? String(op.from_value ?? "") : undefined,
    previousUniversity: op.field === "university" ? String(op.from_value ?? "") : undefined,
    previousGraduationDate: op.field === "graduation_date" ? String(op.from_value ?? "") : undefined,
    previousGpa: op.field === "gpa" ? String(op.from_value ?? "") : undefined,
  }
}

function mapContactFromOps(ops: PatchOperationResponse[]): ContactChange {
  const contact = emptyContact()
  for (const op of ops) {
    if (op.op !== "ADD_CONTACT" && op.op !== "UPDATE_CONTACT") continue
    const data = (op.data ?? {}) as Record<string, unknown>
    if (data.location) contact.location = String(data.location)
    if (data.phone) contact.phone = String(data.phone)
    if (data.linkedin) contact.linkedin = String(data.linkedin)
    if (data.github) contact.github = String(data.github)
    if (op.field === "location") contact.location = String(op.to ?? "")
    if (op.field === "phone") contact.phone = String(op.to ?? "")
    if (op.field === "linkedin") contact.linkedin = String(op.to ?? "")
    if (op.field === "github") contact.github = String(op.to ?? "")
  }
  return contact
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

export function mapPendingPatchToReviewState(
  patch: PendingPatchResponse,
  evidence: EvidenceResponse[] = [],
): ReviewState {
  const evidenceById = buildEvidenceIndex(evidence)

  const experiences: ExperienceChange[] = []
  const addExps = patch.experiences.filter((o) => o.op === "ADD_EXPERIENCE")
  const updateExps = patch.experiences.filter((o) => o.op === "UPDATE_EXPERIENCE")
  experiences.push(...addExps.map(mapAddExperience))
  for (const [, ops] of groupByEvidenceId(updateExps)) {
    experiences.push(mergeExperienceUpdates(ops, evidenceById))
  }

  const projects: ProjectChange[] = []
  const addProjects = patch.projects.filter((o) => o.op === "ADD_PROJECT")
  const updateProjects = patch.projects.filter((o) => o.op === "UPDATE_PROJECT")
  projects.push(...addProjects.map(mapAddProject))
  for (const [, ops] of groupByEvidenceId(updateProjects)) {
    projects.push(mergeProjectUpdates(ops, evidenceById))
  }

  const education = patch.education
    .filter((op) => op.op === "ADD_EDUCATION" || op.op === "ADD_EDUCATION_ENTRY" || op.op === "UPDATE_EDUCATION")
    .map(mapEducation)
  const contactOps = patch.education.filter(
    (op) => op.op === "ADD_CONTACT" || op.op === "UPDATE_CONTACT",
  )
  const contact = contactOps.length > 0 ? mapContactFromOps(contactOps) : emptyContact()
  const sectionOrderOp = patch.education.find((op) => op.op === "SET_SECTION_ORDER")
  const resumeSectionOrder =
    sectionOrderOp?.value === "experience_first" ? "experience_first" : "education_first"

  return {
    skills: patch.skills.map(mapSkill),
    experiences,
    projects,
    certifications: patch.certifications.map(mapCertification),
    contact,
    education: education.filter((e) => e.degree || e.university),
    resumeSectionOrder,
    preferences: [],
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

  return ids
}

export function emptyReviewState(): ReviewState {
  return {
    skills: [],
    experiences: [],
    projects: [],
    certifications: [],
    contact: emptyContact(),
    education: [],
    resumeSectionOrder: "education_first",
    preferences: [],
  }
}
