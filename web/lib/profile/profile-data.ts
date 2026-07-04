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

export type EducationLevel = "masters" | "undergrad" | "doctoral" | "other"

export interface ContactChange {
  location: string
  phone: string
  linkedin: string
  github: string
}

export interface EducationChange {
  id: string
  operationIds?: string[]
  kind: ChangeKind
  status: ItemStatus
  level: EducationLevel
  degree: string
  university: string
  graduationDate: string
  gpa: string
  previousDegree?: string
  previousUniversity?: string
  previousGraduationDate?: string
  previousGpa?: string
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

export type ResumeSectionOrder = "education_first" | "experience_first"

export interface ReviewState {
  skills: SkillChange[]
  experiences: ExperienceChange[]
  projects: ProjectChange[]
  certifications: CertificationChange[]
  contact: ContactChange
  education: EducationChange[]
  resumeSectionOrder: ResumeSectionOrder
  preferences: PreferenceSuggestion[]
}

const MOCK_PARSED_TECHNICAL_SKILLS: Omit<SkillChange, "id" | "status">[] = [
  { kind: "add", category: "Languages", name: "Python" },
  { kind: "add", category: "Languages", name: "Java" },
  { kind: "add", category: "Languages", name: "TypeScript" },
  { kind: "add", category: "Languages", name: "JavaScript" },
  { kind: "add", category: "Languages", name: "C++" },
  { kind: "add", category: "Languages", name: "SQL" },
  { kind: "add", category: "Languages", name: "Go" },
  { kind: "add", category: "Frameworks", name: "FastAPI" },
  { kind: "add", category: "Frameworks", name: "React" },
  { kind: "add", category: "Frameworks", name: "Next.js" },
  { kind: "add", category: "Frameworks", name: "Node.js" },
  { kind: "add", category: "Frameworks", name: "Spring Boot" },
  { kind: "add", category: "Frameworks", name: "Django" },
  { kind: "add", category: "Frameworks", name: "Flask" },
  { kind: "add", category: "Databases", name: "PostgreSQL" },
  { kind: "add", category: "Databases", name: "MongoDB" },
  { kind: "add", category: "Databases", name: "Redis" },
  { kind: "add", category: "Databases", name: "MySQL" },
  { kind: "add", category: "Cloud", name: "AWS" },
  { kind: "add", category: "Cloud", name: "GCP" },
  { kind: "add", category: "Cloud", name: "Docker" },
  { kind: "add", category: "Cloud", name: "Kubernetes" },
  { kind: "add", category: "AI / ML", name: "RAG" },
  { kind: "add", category: "AI / ML", name: "LLMs" },
  { kind: "add", category: "AI / ML", name: "PyTorch" },
  { kind: "add", category: "AI / ML", name: "TensorFlow" },
  { kind: "add", category: "AI / ML", name: "scikit-learn" },
  { kind: "add", category: "Infrastructure", name: "Kafka" },
  { kind: "add", category: "Infrastructure", name: "RabbitMQ" },
  { kind: "add", category: "Infrastructure", name: "CI/CD" },
  { kind: "add", category: "Infrastructure", name: "Terraform" },
  { kind: "add", category: "Infrastructure", name: "Linux" },
]

export const initialReviewState: ReviewState = {
  skills: MOCK_PARSED_TECHNICAL_SKILLS.map((skill, index) => ({
    ...skill,
    id: `s${index + 1}`,
    status: "pending",
  })),
  experiences: [
    {
      id: "e1",
      kind: "add",
      status: "pending",
      title: "Software Developer II",
      company: "Walmart Global Tech",
      durationMonths: 24,
      domains: ["Retail Tech"],
      keywords: ["Architected high-throughput microservices", "Distributed Systems", "Monitoring", "Java", "Kafka"],
    },
    {
      id: "e2",
      kind: "update",
      status: "pending",
      title: "Junior Software Developer",
      company: "Bloomberg LP",
      durationMonths: 29,
      domains: ["FinTech"],
      keywords: ["Built data pipelines for financial analytics", "Python", "Data Pipelines", "Kafka"],
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
  contact: {
    location: "New York, NY",
    phone: "+1 (212) 555-0142",
    linkedin: "linkedin.com/in/alexrivera",
    github: "github.com/alexrivera",
  },
  education: [
    {
      id: "edu1",
      kind: "add",
      status: "pending",
      level: "masters",
      degree: "MS Computer Science",
      university: "NYU",
      graduationDate: "2027-05",
      gpa: "3.92",
    },
    {
      id: "edu2",
      kind: "add",
      status: "pending",
      level: "undergrad",
      degree: "B.Tech Computer Science",
      university: "IIT Mandi",
      graduationDate: "2023-05",
      gpa: "3.78",
    },
  ],
  resumeSectionOrder: "education_first",
  preferences: [],
}

export const PROCESSING_MESSAGES = [
  "Reading your resume...",
  "Extracting your experience...",
  "Identifying your skills...",
  "Preparing your review...",
]
