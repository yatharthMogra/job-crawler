export type EmploymentSuffix = "FULLTIME" | "INTERNSHIP" | "NEW_GRAD"

export interface RoleCatalogEntry {
  id: string
  label: string
  category: string
  subcategory: string
  poolBase: string
}

const ENGINEERING_POOL_BASES = new Set([
  "SWE",
  "BACKEND_ENGINEER",
  "FRONTEND_ENGINEER",
  "FULLSTACK_ENGINEER",
  "ML_ENGINEER",
  "DATA_ENGINEER",
  "DATA_SCIENTIST",
  "DEVOPS_ENGINEER",
  "SECURITY_ENGINEER",
  "MOBILE_ENGINEER",
  "SOLUTIONS_ENGINEER",
  "SUPPORT_ENGINEER",
  "SYSTEMS_ENGINEER",
  "HARDWARE_ENGINEER",
])

export const ROLE_CATALOG: RoleCatalogEntry[] = [
  // Backend Engineering
  { id: "backend-engineer", label: "Backend Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "BACKEND_ENGINEER" },
  { id: "fullstack-engineer", label: "Full Stack Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "FULLSTACK_ENGINEER" },
  { id: "software-engineer", label: "Software Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "SWE" },
  { id: "python-engineer", label: "Python Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "SWE" },
  { id: "java-engineer", label: "Java Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "SWE" },
  { id: "devops-engineer", label: "DevOps Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "DEVOPS_ENGINEER" },
  { id: "solutions-engineer", label: "Solutions Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "SOLUTIONS_ENGINEER" },
  { id: "support-engineer", label: "Support Engineer", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "SUPPORT_ENGINEER" },
  { id: "systems-engineer", label: "Systems Engineer", category: "Aerospace & Defense", subcategory: "Systems Engineering", poolBase: "SYSTEMS_ENGINEER" },
  { id: "hardware-engineer", label: "Hardware Engineer", category: "Aerospace & Defense", subcategory: "Hardware Engineering", poolBase: "HARDWARE_ENGINEER" },
  { id: "tpm", label: "Technical Program Manager", category: "Software/Internet/AI", subcategory: "Backend Engineering", poolBase: "TECHNICAL_PROGRAM_MANAGER" },
  // Frontend Engineering
  { id: "frontend-engineer", label: "Frontend Engineer", category: "Software/Internet/AI", subcategory: "Frontend Engineering", poolBase: "FRONTEND_ENGINEER" },
  { id: "mobile-engineer", label: "Mobile Engineer", category: "Software/Internet/AI", subcategory: "Frontend Engineering", poolBase: "MOBILE_ENGINEER" },
  // Data & Analytics
  { id: "data-analyst", label: "Data Analyst", category: "Software/Internet/AI", subcategory: "Data & Analytics", poolBase: "DATA_ANALYST" },
  { id: "data-scientist", label: "Data Scientist", category: "Software/Internet/AI", subcategory: "Data & Analytics", poolBase: "DATA_SCIENTIST" },
  { id: "data-engineer", label: "Data Engineer", category: "Software/Internet/AI", subcategory: "Data & Analytics", poolBase: "DATA_ENGINEER" },
  // Machine Learning & AI
  { id: "ml-engineer", label: "Machine Learning Engineer", category: "Software/Internet/AI", subcategory: "Machine Learning & AI", poolBase: "ML_ENGINEER" },
  { id: "ai-engineer", label: "AI Engineer", category: "Software/Internet/AI", subcategory: "Machine Learning & AI", poolBase: "ML_ENGINEER" },
  // Security
  { id: "security-engineer", label: "Security Engineer", category: "Software/Internet/AI", subcategory: "Security", poolBase: "SECURITY_ENGINEER" },
  // Product & Design
  { id: "product-manager", label: "Product Manager", category: "Software/Internet/AI", subcategory: "Product", poolBase: "PRODUCT_MANAGER" },
  { id: "product-designer", label: "Product Designer", category: "Software/Internet/AI", subcategory: "Design", poolBase: "PRODUCT_DESIGNER" },
  // Sales & GTM
  { id: "sales", label: "Sales", category: "Sales & GTM", subcategory: "Sales", poolBase: "SALES" },
  { id: "customer-success", label: "Customer Success", category: "Sales & GTM", subcategory: "Customer Success", poolBase: "CUSTOMER_SUCCESS" },
  { id: "solutions-consultant", label: "Solutions Consultant", category: "Sales & GTM", subcategory: "Customer Success", poolBase: "SOLUTIONS_CONSULTANT" },
  { id: "partnerships", label: "Partnerships", category: "Sales & GTM", subcategory: "Partnerships", poolBase: "PARTNERSHIPS" },
  { id: "marketing", label: "Marketing", category: "Sales & GTM", subcategory: "Marketing", poolBase: "MARKETING" },
  // Operations
  { id: "operations", label: "Operations", category: "Operations", subcategory: "Business Operations", poolBase: "OPERATIONS" },
  { id: "recruiting", label: "Recruiting / Talent", category: "Operations", subcategory: "People", poolBase: "RECRUITING" },
  { id: "finance", label: "Finance", category: "Operations", subcategory: "Finance", poolBase: "FINANCE" },
  { id: "legal", label: "Legal / Compliance", category: "Operations", subcategory: "Legal", poolBase: "LEGAL" },
]

export const ROLE_CATEGORIES = [...new Set(ROLE_CATALOG.map((r) => r.category))]

export function rolesByCategory(category: string): RoleCatalogEntry[] {
  return ROLE_CATALOG.filter((r) => r.category === category)
}

export function rolesBySubcategory(category: string): Record<string, RoleCatalogEntry[]> {
  const roles = rolesByCategory(category)
  const groups: Record<string, RoleCatalogEntry[]> = {}
  for (const role of roles) {
    if (!groups[role.subcategory]) groups[role.subcategory] = []
    groups[role.subcategory].push(role)
  }
  return groups
}

export function findRoleByLabel(label: string): RoleCatalogEntry | undefined {
  const normalized = label.toLowerCase().trim()
  return ROLE_CATALOG.find((r) => r.label.toLowerCase() === normalized)
}

export function findRoleById(id: string): RoleCatalogEntry | undefined {
  return ROLE_CATALOG.find((r) => r.id === id)
}

export function poolIdsForRoles(labels: string[], suffix: EmploymentSuffix = "FULLTIME"): string[] {
  const pools = new Set<string>()
  for (const label of labels) {
    const entry = findRoleByLabel(label)
    if (entry) {
      pools.add(`${entry.poolBase}_${suffix}`)
      if (ENGINEERING_POOL_BASES.has(entry.poolBase) && entry.poolBase !== "SWE") {
        pools.add(`SWE_${suffix}`)
      }
    }
  }
  if (pools.size === 0) pools.add(`SWE_${suffix}`)
  return [...pools]
}

export function poolIdsFromCatalogIds(ids: string[], suffix: EmploymentSuffix = "FULLTIME"): string[] {
  const labels = ids.map((id) => findRoleById(id)?.label).filter(Boolean) as string[]
  return poolIdsForRoles(labels, suffix)
}
