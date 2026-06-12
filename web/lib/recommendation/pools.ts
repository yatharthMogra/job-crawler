import type { ProfileResponse } from "@/lib/profile/api-types"
import { poolIdsForRoles } from "@/lib/profile/role-catalog"

const ROLE_TO_POOL: Record<string, string> = {
  swe: "SWE",
  "software engineer": "SWE",
  "backend engineer": "BACKEND_ENGINEER",
  "frontend engineer": "FRONTEND_ENGINEER",
  "full stack": "FULLSTACK_ENGINEER",
  "fullstack engineer": "FULLSTACK_ENGINEER",
  "full stack engineer": "FULLSTACK_ENGINEER",
  "ml engineer": "ML_ENGINEER",
  "machine learning engineer": "ML_ENGINEER",
  "ai engineer": "ML_ENGINEER",
  "data engineer": "DATA_ENGINEER",
  "data scientist": "DATA_SCIENTIST",
  "data analyst": "DATA_ANALYST",
  "devops engineer": "DEVOPS_ENGINEER",
  devops: "DEVOPS_ENGINEER",
  "security engineer": "SECURITY_ENGINEER",
  "mobile engineer": "MOBILE_ENGINEER",
  "solutions engineer": "SOLUTIONS_ENGINEER",
  "support engineer": "SUPPORT_ENGINEER",
  "systems engineer": "SYSTEMS_ENGINEER",
  "hardware engineer": "HARDWARE_ENGINEER",
  "mechanical engineer": "HARDWARE_ENGINEER",
  "electrical engineer": "HARDWARE_ENGINEER",
  "manufacturing engineer": "HARDWARE_ENGINEER",
  "technical program manager": "TECHNICAL_PROGRAM_MANAGER",
  tpm: "TECHNICAL_PROGRAM_MANAGER",
  "product manager": "PRODUCT_MANAGER",
  "product designer": "PRODUCT_DESIGNER",
  sales: "SALES",
  "customer success": "CUSTOMER_SUCCESS",
  "solutions consultant": "SOLUTIONS_CONSULTANT",
  partnerships: "PARTNERSHIPS",
  marketing: "MARKETING",
  operations: "OPERATIONS",
  recruiting: "RECRUITING",
  "recruiting / talent": "RECRUITING",
  finance: "FINANCE",
  legal: "LEGAL",
  "legal / compliance": "LEGAL",
  "python engineer": "SWE",
  "java engineer": "SWE",
}

function roleSuffix(profile: ProfileResponse): "FULLTIME" | "INTERNSHIP" | "NEW_GRAD" {
  const constraints = profile.constraints ?? {}
  if (constraints.internship_only) return "INTERNSHIP"
  if (constraints.new_grad_only) return "NEW_GRAD"
  return "FULLTIME"
}

function normalizeRoleLabel(label: string): string {
  return label.toLowerCase().trim()
}

function normalizePoolName(poolName: string): string {
  if (poolName.endsWith("_INTERN")) return `${poolName}SHIP`
  return poolName
}

export function derivePoolNames(profile: ProfileResponse): string[] {
  const prefs = profile.preferences ?? {}
  const explicitPools = prefs.role_pool_ids
  if (Array.isArray(explicitPools) && explicitPools.length > 0) {
    return [...new Set(
      explicitPools
        .filter((p): p is string => typeof p === "string")
        .map(normalizePoolName),
    )]
  }

  const suffix = roleSuffix(profile)
  const primaryRoles = Array.isArray(prefs.primary_roles) ? prefs.primary_roles : []

  if (primaryRoles.length > 0) {
    return poolIdsForRoles(primaryRoles, suffix)
  }

  const pools = new Set<string>()
  for (const role of primaryRoles) {
    if (typeof role !== "string") continue
    const key = normalizeRoleLabel(role)
    const base = ROLE_TO_POOL[key]
    if (base) pools.add(`${base}_${suffix}`)
  }

  if (pools.size === 0) pools.add(`SWE_${suffix}`)
  return [...pools]
}
