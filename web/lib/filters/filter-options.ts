export const SALARY_FLOOR = 50_000
export const SALARY_MEDIAN = 145_000
export const SALARY_CEILING = 350_000
export const DEFAULT_SALARY_MIN = 120_000
export const DEFAULT_SALARY_MAX = 240_000

export const INDUSTRY_SUGGESTIONS = [
  "FinTech",
  "SaaS",
  "AI/ML",
  "HealthTech",
  "Cybersecurity",
  "E-commerce",
  "Enterprise",
  "Consumer",
] as const

export const TECH_STACK_OPTIONS = [
  { id: "Python", label: "Python" },
  { id: "TypeScript", label: "TypeScript" },
  { id: "React", label: "React" },
  { id: "Go", label: "Golang" },
  { id: "AWS", label: "AWS Cloud" },
  { id: "PostgreSQL", label: "PostgreSQL" },
  { id: "Java", label: "Java" },
  { id: "Kafka", label: "Kafka" },
  { id: "Docker", label: "Docker" },
  { id: "Kubernetes", label: "Kubernetes" },
] as const

export const EXPERIENCE_TIERS = [
  {
    id: "entry",
    label: "Entry Level",
    levels: ["Intern/New Grad", "Entry Level"],
  },
  {
    id: "mid-senior",
    label: "Mid-Senior",
    levels: ["Mid Level", "Senior Level"],
  },
  {
    id: "director",
    label: "Director+",
    levels: ["Lead/Staff"],
  },
  {
    id: "executive",
    label: "Executive",
    levels: ["Director/Executive"],
  },
] as const

export const WORK_ARRANGEMENTS = [
  {
    id: "any",
    label: "Anywhere",
    description: "Open to any work arrangement",
    models: [] as string[],
  },
  {
    id: "onsite",
    label: "Onsite",
    description: "In-office roles",
    models: ["Onsite"],
  },
  {
    id: "hybrid",
    label: "Hybrid",
    description: "Mix of office and remote",
    models: ["Hybrid"],
  },
  {
    id: "remote",
    label: "Remote anywhere in USA",
    description: "Fully remote within the United States",
    models: ["Remote"],
  },
] as const

export function formatSalaryCompact(value: number): string {
  if (value >= SALARY_CEILING) return "$350k+"
  if (value >= 1000) return `$${Math.round(value / 1000)}k`
  return `$${value.toLocaleString()}`
}

export function formatSalaryRange(min: number, max: number): string {
  const maxLabel = max >= SALARY_CEILING ? "$240,000+" : `$${max.toLocaleString()}`
  return `USD $${min.toLocaleString()} - ${maxLabel}`
}
