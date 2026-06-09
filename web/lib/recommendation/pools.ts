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
  "data analyst": "DATA_SCIENTIST",
  "devops engineer": "DEVOPS_ENGINEER",
  devops: "DEVOPS_ENGINEER",
  "security engineer": "SECURITY_ENGINEER",
  "mobile engineer": "MOBILE_ENGINEER",
  "product manager": "PRODUCT_MANAGER",
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

export function derivePoolNames(profile: ProfileResponse): string[] {
  const prefs = profile.preferences ?? {}
  const explicitPools = prefs.role_pool_ids
  if (Array.isArray(explicitPools) && explicitPools.length > 0) {
    return explicitPools.filter((p): p is string => typeof p === "string")
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
