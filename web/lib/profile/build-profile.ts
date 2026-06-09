import type { ContactInfo, EducationEntry, ResumeSectionOrder } from "@/lib/profile/contact"
import type { EeoState } from "@/lib/profile/eeo"
import type { ReviewState } from "@/lib/profile/profile-data"
import { emptyContact } from "@/lib/profile/contact"
import { emptyEeo } from "@/lib/profile/eeo"

export interface CommittedProfile {
  skills: { category: string; names: string[] }[]
  skillCount: number
  experiences: { id: string; title: string; company: string; durationMonths: number; domains: string[]; keywords: string[] }[]
  projects: { id: string; name: string; type: string; domain: string; keywords: string[] }[]
  certifications: { id: string; name: string; issuer: string }[]
  contact: ContactInfo
  educationEntries: EducationEntry[]
  resumeSectionOrder: ResumeSectionOrder
  eeo: EeoState
  primaryRoles: string[]
  secondaryRoles: string[]
  preferences: { label: string; value: string }[]
}

export function buildCommittedProfile(state: ReviewState): CommittedProfile {
  const skills = state.skills.filter((s) => s.status === "approved")
  const experiences = state.experiences.filter((e) => e.status === "approved")
  const projects = state.projects.filter((p) => p.status === "approved")
  const certifications = state.certifications.filter((c) => c.status === "approved")

  const skillCategories = Array.from(new Set(skills.map((s) => s.category))).map((category) => ({
    category,
    names: skills.filter((s) => s.category === category).map((s) => s.name),
  }))

  const approvedEducation = state.education.filter((e) => e.status === "approved")

  return {
    skills: skillCategories,
    skillCount: skills.length,
    contact: { ...state.contact },
    educationEntries: approvedEducation.map((e) => ({
      level: e.level,
      degree: e.degree,
      university: e.university,
      graduationDate: e.graduationDate,
      gpa: e.gpa,
    })),
    resumeSectionOrder: state.resumeSectionOrder,
    eeo: emptyEeo(),
    experiences: experiences.map((e) => ({
      id: e.id,
      title: e.title,
      company: e.company,
      durationMonths: e.durationMonths,
      domains: e.domains,
      keywords: e.keywords,
    })),
    projects: projects.map((p) => ({
      id: p.id,
      name: p.name,
      type: p.type,
      domain: p.domain,
      keywords: p.keywords,
    })),
    certifications: certifications.map((c) => ({ id: c.id, name: c.name, issuer: c.issuer })),
    primaryRoles: [],
    secondaryRoles: [],
    preferences: [],
  }
}

export function withDefaultProfileFields(profile: CommittedProfile): CommittedProfile {
  return {
    ...profile,
    contact: profile.contact ?? emptyContact(),
    educationEntries: profile.educationEntries ?? [],
    resumeSectionOrder: profile.resumeSectionOrder ?? "education_first",
    eeo: profile.eeo ?? emptyEeo(),
  }
}
