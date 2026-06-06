export type ChangeKind = "add" | "update" | "remove"
export type ItemStatus = "pending" | "approved" | "rejected"

export interface SkillChange {
  id: string
  kind: ChangeKind
  category: string
  name: string
  status: ItemStatus
}

export interface ExperienceChange {
  id: string
  operationIds?: string[]
  kind: ChangeKind
  status: ItemStatus
  title: string
  company: string
  durationMonths: number
  previousTitle?: string
  previousCompany?: string
  previousDurationMonths?: number
  domains: string[]
  previousDomains?: string[]
  keywords: string[]
  newKeywords?: string[]
}

export interface ProjectChange {
  id: string
  operationIds?: string[]
  kind: ChangeKind
  status: ItemStatus
  name: string
  type: string
  previousType?: string
  domain: string
  previousDomain?: string
  keywords: string[]
  newKeywords?: string[]
}

export interface CertificationChange {
  id: string
  operationIds?: string[]
  kind: ChangeKind
  status: ItemStatus
  name: string
  issuer: string
}

export interface EducationChange {
  id: string
  operationIds?: string[]
  kind: ChangeKind
  status: ItemStatus
  degree: string
  university: string
  graduationDate: string
  previousDegree?: string
  previousUniversity?: string
  previousGraduationDate?: string
}

export type PrefStatus = "pending" | "confirmed" | "declined"

export interface PreferenceSuggestion {
  id: string
  label: string
  suggestion: string
  detail?: string
  detected: boolean
  value: string
  status: PrefStatus
  kind: "text" | "input"
  isConstraint?: boolean
}

export interface ReviewState {
  skills: SkillChange[]
  experiences: ExperienceChange[]
  projects: ProjectChange[]
  certifications: CertificationChange[]
  education: EducationChange[]
  preferences: PreferenceSuggestion[]
}

export const initialReviewState: ReviewState = {
  skills: [
    { id: "s1", kind: "add", category: "Languages", name: "Python", status: "pending" },
    { id: "s2", kind: "add", category: "Languages", name: "Java", status: "pending" },
    { id: "s3", kind: "add", category: "Languages", name: "TypeScript", status: "pending" },
    { id: "s4", kind: "add", category: "Frameworks", name: "FastAPI", status: "pending" },
    { id: "s5", kind: "add", category: "Frameworks", name: "React", status: "pending" },
    { id: "s6", kind: "add", category: "Cloud", name: "AWS", status: "pending" },
    { id: "s7", kind: "add", category: "AI / ML", name: "RAG", status: "pending" },
    { id: "s8", kind: "add", category: "AI / ML", name: "LLMs", status: "pending" },
  ],
  experiences: [
    {
      id: "e1",
      kind: "add",
      status: "pending",
      title: "Software Developer 2",
      company: "Walmart",
      durationMonths: 24,
      domains: ["Retail Tech"],
      keywords: ["Backend APIs", "Distributed Systems", "Monitoring", "Java", "Kafka"],
    },
    {
      id: "e2",
      kind: "update",
      status: "pending",
      title: "Software Developer",
      company: "Bloomberg",
      durationMonths: 24,
      previousDurationMonths: 22,
      domains: ["FinTech"],
      keywords: ["Python", "Data Pipelines"],
      newKeywords: ["Kafka"],
    },
  ],
  projects: [
    {
      id: "p1",
      kind: "add",
      status: "pending",
      name: "SpecterRossAI",
      type: "AI Product",
      domain: "Legal Tech",
      keywords: ["Multi-Agent Systems", "RAG", "React", "Voice AI", "Real-Time Systems"],
    },
    {
      id: "p2",
      kind: "add",
      status: "pending",
      name: "DocuFlow",
      type: "Web App",
      domain: "Developer Tools",
      keywords: ["Next.js", "Document Parsing", "PostgreSQL"],
    },
  ],
  certifications: [
    { id: "c1", kind: "add", status: "pending", name: "AWS Solutions Architect", issuer: "AWS" },
    { id: "c2", kind: "add", status: "pending", name: "Deep Learning Specialization", issuer: "DeepLearning.AI" },
  ],
  education: [],
  preferences: [
    {
      id: "pref1",
      label: "Sponsorship Required",
      suggestion: "Yes",
      detail: "Detected F1 visa indicators",
      detected: true,
      value: "Yes",
      status: "pending",
      kind: "text",
    },
    {
      id: "pref2",
      label: "Primary Roles",
      suggestion: "Software Engineer Intern, AI Engineer Intern",
      detected: true,
      value: "Software Engineer Intern, AI Engineer Intern",
      status: "pending",
      kind: "text",
    },
    {
      id: "pref3",
      label: "Preferred Locations",
      suggestion: "NYC, Remote",
      detected: true,
      value: "NYC, Remote",
      status: "pending",
      kind: "text",
    },
    {
      id: "pref4",
      label: "Minimum Hourly Rate",
      suggestion: "Not detected",
      detail: "Leave blank or set now",
      detected: false,
      value: "",
      status: "pending",
      kind: "input",
    },
  ],
}

export const PROCESSING_MESSAGES = [
  "Reading your resume...",
  "Extracting your experience...",
  "Identifying your skills...",
  "Generating your profile...",
]
