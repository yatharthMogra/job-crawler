import type {
  CompanyEnrichmentInfo,
  H1BSponsorshipInfo,
  SponsorshipStatus,
} from "@/lib/recommendation/api"
import { resolveBrandDomain } from "@/lib/brand-logos"

export type EmploymentType = "FULLTIME" | "PARTTIME" | "INTERNSHIP" | "CONTRACT"
export type RemoteType = "remote" | "hybrid" | "onsite"
export type SeniorityLevel =
  | "internship"
  | "new_grad"
  | "early_career"
  | "entry"
  | "mid"
  | "senior"
  | "staff"
export type Effort = "LOW" | "MEDIUM" | "HIGH"

export interface Job {
  id: string
  title: string
  company: string
  location: string
  salary_min: number | null
  salary_max: number | null
  employment_type: EmploymentType
  seniority_level: SeniorityLevel
  remote_type: RemoteType
  application_effort: Effort
  posting_url: string
  posted_at: string
  opportunity_score: number
  personal_score: number
  match_reasons: string[]
  recommendation_reason: string
  skills: string[]
  responsibilities: string[]
  required_qualifications: string[]
  preferred_qualifications: string[]
  benefits: string[]
  sponsorship_status: SponsorshipStatus
  sponsorship_confidence: string
  requires_clearance: boolean
  requires_citizenship: boolean
  h1b_sponsorship: H1BSponsorshipInfo | null
  company_info: CompanyEnrichmentInfo | null
  about_summary: string | null
  description_html: string
  is_saved: boolean
  is_applied: boolean
  application_status?: string
  application_id?: string
}

const COMPANIES = [
  "ScaleAI",
  "Ramp",
  "Vercel",
  "Stripe",
  "Notion",
  "Linear",
  "Databricks",
  "Anthropic",
  "Figma",
  "Retool",
  "Plaid",
  "Brex",
  "Mercury",
  "Airtable",
  "Cohere",
  "Snowflake",
  "Datadog",
  "Coinbase",
  "Robinhood",
  "Instacart",
  "DoorDash",
  "Rippling",
  "Deel",
  "Census",
  "Clearbit",
]

function mockCompanyInfo(company: string): CompanyEnrichmentInfo {
  const domain = resolveBrandDomain(company, "company")
  return {
    founded_year: null,
    headquarters: null,
    employee_count_range: null,
    one_line_description: null,
    website: `https://${domain}`,
    linkedin_url: null,
    glassdoor_rating: null,
  }
}

const ROLES = [
  { title: "Infrastructure Software Engineer", role: "Backend Engineer", skills: ["Go", "Kubernetes", "AWS", "Distributed Systems"], reasons: ["Backend Engineering", "Distributed Systems", "AWS"] },
  { title: "Senior Backend Engineer", role: "Backend Engineer", skills: ["Python", "Kafka", "PostgreSQL", "gRPC"], reasons: ["Backend Engineering", "Data Pipelines", "PostgreSQL"] },
  { title: "Frontend Engineer", role: "Frontend Engineer", skills: ["React", "TypeScript", "Next.js", "CSS"], reasons: ["Frontend Engineering", "React", "TypeScript"] },
  { title: "Full Stack Engineer", role: "Full Stack", skills: ["TypeScript", "Node.js", "React", "PostgreSQL"], reasons: ["Full Stack", "TypeScript", "Node.js"] },
  { title: "Machine Learning Engineer", role: "ML Engineer", skills: ["Python", "PyTorch", "CUDA", "MLOps"], reasons: ["Machine Learning", "PyTorch", "Model Serving"] },
  { title: "Data Engineer", role: "Data Engineer", skills: ["Spark", "Airflow", "Snowflake", "SQL"], reasons: ["Data Engineering", "Spark", "ETL"] },
  { title: "Data Scientist", role: "Data Scientist", skills: ["Python", "Pandas", "Statistics", "SQL"], reasons: ["Data Science", "Statistics", "Experimentation"] },
  { title: "Platform Engineer", role: "DevOps", skills: ["Terraform", "AWS", "Docker", "CI/CD"], reasons: ["Platform Engineering", "Terraform", "AWS"] },
  { title: "Site Reliability Engineer", role: "DevOps", skills: ["Kubernetes", "Prometheus", "Go", "Linux"], reasons: ["Reliability", "Kubernetes", "Observability"] },
  { title: "Product Manager, Growth", role: "Product Manager", skills: ["Analytics", "Roadmapping", "SQL", "A/B Testing"], reasons: ["Product Strategy", "Growth", "Analytics"] },
  { title: "Software Engineer, New Grad", role: "SWE", skills: ["Java", "Algorithms", "REST", "Git"], reasons: ["Software Engineering", "Fundamentals", "New Grad Fit"] },
  { title: "Software Engineering Intern", role: "SWE", skills: ["Python", "Git", "Data Structures"], reasons: ["Internship Fit", "Software Engineering", "Strong Fundamentals"] },
]

const LOCATIONS = [
  { loc: "San Francisco, CA", remote: "hybrid" as RemoteType },
  { loc: "New York, NY", remote: "hybrid" as RemoteType },
  { loc: "Remote (US)", remote: "remote" as RemoteType },
  { loc: "Seattle, WA", remote: "onsite" as RemoteType },
  { loc: "Austin, TX", remote: "hybrid" as RemoteType },
  { loc: "Remote (Global)", remote: "remote" as RemoteType },
  { loc: "Boston, MA", remote: "onsite" as RemoteType },
  { loc: "Los Angeles, CA", remote: "hybrid" as RemoteType },
]

const EFFORTS: Effort[] = ["LOW", "MEDIUM", "HIGH"]

const REC_REASONS = [
  "Strong backend alignment + high compensation.",
  "Matches your top skills and location preference.",
  "High upside role at a fast-growing company.",
  "Excellent fit based on your distributed systems experience.",
  "Aligns with your frontend and product interests.",
  "Great compensation and low application effort.",
]

function seededRandom(seed: number) {
  let s = seed % 2147483647
  if (s <= 0) s += 2147483646
  return () => {
    s = (s * 16807) % 2147483647
    return (s - 1) / 2147483646
  }
}

function descriptionHtml(title: string, company: string, skills: string[]): string {
  return `
    <p>${company} is looking for a <strong>${title}</strong> to join our team. You'll work on high-impact systems that serve millions of users and collaborate closely with product and design.</p>
    <h4>What you'll do</h4>
    <ul>
      <li>Design, build, and maintain scalable services and features.</li>
      <li>Collaborate with cross-functional teams to ship products end to end.</li>
      <li>Write clean, well-tested code and participate in code reviews.</li>
      <li>Contribute to technical decisions and architecture.</li>
    </ul>
    <h4>What we're looking for</h4>
    <ul>
      <li>Strong experience with ${skills.slice(0, 2).join(" and ")}.</li>
      <li>Familiarity with ${skills.slice(2).join(", ") || "modern tooling"}.</li>
      <li>A bias for action and a growth mindset.</li>
      <li>Excellent communication and collaboration skills.</li>
    </ul>
    <p>We offer competitive compensation, equity, comprehensive benefits, and a flexible work environment.</p>
  `
}

const TOTAL = 60

export const ALL_JOBS: Job[] = Array.from({ length: TOTAL }).map((_, i) => {
  const rand = seededRandom((i + 1) * 7919)
  const role = ROLES[(i + Math.floor(rand() * ROLES.length)) % ROLES.length]
  const company = COMPANIES[Math.floor(rand() * COMPANIES.length)]
  const location = LOCATIONS[Math.floor(rand() * LOCATIONS.length)]
  const isIntern = role.title.includes("Intern")
  const isNewGrad = role.title.includes("New Grad")
  const isSenior = role.title.includes("Senior") || role.title.includes("Staff")
  const seniority: SeniorityLevel = isIntern
    ? "internship"
    : isNewGrad
      ? "new_grad"
      : isSenior
        ? "senior"
        : rand() > 0.7
          ? "early_career"
          : rand() > 0.5
            ? "mid"
            : "entry"

  const empRoll = rand()
  const employment_type: EmploymentType = isIntern
    ? "INTERNSHIP"
    : empRoll > 0.88
      ? "CONTRACT"
      : empRoll > 0.82
        ? "PARTTIME"
        : "FULLTIME"

  const base = isIntern ? 8000 : employment_type === "PARTTIME" ? 45000 : 140000
  const span = isIntern ? 4000 : employment_type === "PARTTIME" ? 25000 : 90000
  const salaryMin = Math.round((base + rand() * span) / 1000) * 1000
  const salaryMax = salaryMin + Math.round((20000 + rand() * 45000) / 1000) * 1000
  const hoursAgo = Math.floor(rand() * 240)
  const postedAt = new Date(Date.now() - hoursAgo * 3600 * 1000).toISOString()

  return {
    id: `job-${i + 1}`,
    title: role.title,
    company,
    location: location.loc,
    salary_min: rand() > 0.08 ? salaryMin : null,
    salary_max: rand() > 0.08 ? salaryMax : null,
    employment_type,
    seniority_level: seniority,
    remote_type: location.remote,
    application_effort: EFFORTS[Math.floor(rand() * EFFORTS.length)],
    posting_url: "https://vercel.com/careers",
    posted_at: postedAt,
    opportunity_score: Math.round((0.4 + rand() * 0.55) * 1000) / 1000,
    personal_score: Math.round((0.4 + rand() * 0.55) * 1000) / 1000,
    match_reasons: role.reasons,
    recommendation_reason: REC_REASONS[Math.floor(rand() * REC_REASONS.length)],
    skills: role.skills,
    responsibilities: [
      "Design, build, and maintain scalable services and features.",
      "Collaborate with cross-functional teams to ship products end to end.",
    ],
    required_qualifications: [
      `Strong experience with ${role.skills.slice(0, 2).join(" and ")}.`,
      "Excellent communication and collaboration skills.",
    ],
    preferred_qualifications: [`Familiarity with ${role.skills.slice(2).join(", ") || "modern tooling"}.`],
    benefits: ["Competitive compensation", "Equity", "Flexible work environment"],
    sponsorship_status: "unclear",
    sponsorship_confidence: "low",
    requires_clearance: false,
    requires_citizenship: false,
    h1b_sponsorship: null,
    company_info: mockCompanyInfo(company),
    about_summary: `${company} is looking for a ${role.title} to join our team. You'll work on high-impact systems and collaborate closely with product and design.`,
    description_html: descriptionHtml(role.title, company, role.skills),
    is_saved: false,
    is_applied: false,
    // role tag used for filtering
    ...({ roleCategory: role.role } as object),
  } as Job & { roleCategory: string }
})

export type JobWithRole = Job & { roleCategory: string }

export const ROLE_OPTIONS = [
  "SWE",
  "Backend Engineer",
  "Frontend Engineer",
  "ML Engineer",
  "Data Engineer",
  "Data Scientist",
  "Full Stack",
  "DevOps",
  "Product Manager",
]

export function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return "just now"
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.floor(hours / 24)
  return `${days}d ago`
}

export function formatSalary(min: number | null, max: number | null): string | null {
  if (min == null) return null
  const fmt = (n: number) => (n >= 1000 ? `$${Math.round(n / 1000)}k` : `$${n}`)
  if (max == null) return fmt(min)
  return `${fmt(min)}–${fmt(max)}`
}
