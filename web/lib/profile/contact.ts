export interface ContactInfo {
  location: string
  phone: string
  linkedin: string
  github: string
}

export function emptyContact(): ContactInfo {
  return {
    location: "",
    phone: "",
    linkedin: "",
    github: "",
  }
}

export function contactFromEducationJson(
  education: Record<string, unknown> | undefined,
): ContactInfo {
  const raw = (education?.contact as Record<string, unknown>) ?? {}
  return {
    location: String(raw.location ?? ""),
    phone: String(raw.phone ?? ""),
    linkedin: String(raw.linkedin ?? ""),
    github: String(raw.github ?? ""),
  }
}

export function contactToApiPayload(contact: ContactInfo): Record<string, unknown> {
  return {
    contact: {
      location: contact.location || null,
      phone: contact.phone || null,
      linkedin: contact.linkedin || null,
      github: contact.github || null,
    },
  }
}

export type ResumeSectionOrder = "education_first" | "experience_first"

export function resumeSectionOrderFromProfile(
  education: Record<string, unknown> | undefined,
): ResumeSectionOrder {
  if (education?.section_order === "experience_first") return "experience_first"
  return "education_first"
}

export interface EducationEntry {
  level: "masters" | "undergrad" | "doctoral" | "other"
  degree: string
  university: string
  graduationDate: string
  gpa: string
}

const LEVEL_LABELS: Record<EducationEntry["level"], string> = {
  masters: "Master's",
  undergrad: "Undergraduate",
  doctoral: "Doctoral",
  other: "Other",
}

export function educationLevelLabel(level: EducationEntry["level"]): string {
  return LEVEL_LABELS[level] ?? "Education"
}

export function educationEntriesFromProfile(
  education: Record<string, unknown> | undefined,
): EducationEntry[] {
  if (!education) return []

  const entries = education.entries
  if (Array.isArray(entries) && entries.length > 0) {
    return entries.map((entry) => {
      const row = entry as Record<string, unknown>
      return {
        level: (row.level as EducationEntry["level"]) ?? "other",
        degree: String(row.degree ?? ""),
        university: String(row.university ?? ""),
        graduationDate: String(row.graduation_date ?? ""),
        gpa: String(row.gpa ?? ""),
      }
    })
  }

  if (education.degree || education.university) {
    const degree = String(education.degree ?? "")
    const level: EducationEntry["level"] = /^(ms|m\.s|master|mba)/i.test(degree)
      ? "masters"
      : /^(bs|b\.s|b\.tech|bachelor|ba|b\.a)/i.test(degree)
        ? "undergrad"
        : "other"
    return [
      {
        level,
        degree,
        university: String(education.university ?? ""),
        graduationDate: String(education.graduation_date ?? ""),
        gpa: String(education.gpa ?? ""),
      },
    ]
  }

  return []
}
