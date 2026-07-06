import type { ProfileResponse } from "@/lib/profile/api-types"
import { eeoFromApiPayload, eeoToApiPayload, type EeoState } from "@/lib/profile/eeo"
import { poolIdsForRoles } from "@/lib/profile/role-catalog"
import type { EmploymentSuffix } from "@/lib/profile/role-catalog"
import {
  experienceLevelsToTargetSeniority,
  targetSeniorityToExperienceLevels,
} from "@/lib/profile/seniority"
import { EXPERIENCE_LEVELS } from "@/lib/profile/job-filters-constants"

export interface JobFiltersState {
  primaryRoles: string[]
  secondaryRoles: string[]
  rolePoolIds: string[]
  internshipOnly: boolean
  fulltimeOnly: boolean
  workModels: string[]
  experienceLevels: string[]
  minYearsExperience: number | null
  maxJobAgeDays: number | null
  openToAllSalary: boolean
  minimumSalary: string
  sponsorshipRequired: boolean
  roleIntents: string[]
  preferredIndustries: string[]
  excludedIndustries: string[]
  preferredSkills: string[]
  excludedSkills: string[]
  roleType: "ic" | "manager" | ""
  preferredLocations: string[]
  remotePreference: string
  eeo: EeoState
}

export function emptyJobFilters(): JobFiltersState {
  return {
    primaryRoles: [],
    secondaryRoles: [],
    rolePoolIds: [],
    internshipOnly: false,
    fulltimeOnly: false,
    workModels: [],
    experienceLevels: [],
    minYearsExperience: null,
    maxJobAgeDays: null,
    openToAllSalary: true,
    minimumSalary: "",
    sponsorshipRequired: false,
    roleIntents: ["engineer", "researcher"],
    preferredIndustries: [],
    excludedIndustries: [],
    preferredSkills: [],
    excludedSkills: [],
    roleType: "",
    preferredLocations: [],
    remotePreference: "",
    eeo: eeoFromApiPayload(undefined),
  }
}

function employmentSuffix(state: JobFiltersState): EmploymentSuffix {
  if (state.internshipOnly && !state.fulltimeOnly) return "INTERNSHIP"
  return "FULLTIME"
}

export function profileToJobFilters(profile: ProfileResponse): JobFiltersState {
  const constraints = profile.constraints ?? {}
  const preferences = profile.preferences ?? {}
  const poolIds = Array.isArray(preferences.role_pool_ids)
    ? (preferences.role_pool_ids as string[])
    : poolIdsForRoles((preferences.primary_roles as string[]) ?? [], employmentSuffix({
        internshipOnly: Boolean(constraints.internship_only),
        fulltimeOnly: Boolean(constraints.fulltime_only),
      } as JobFiltersState))

  const targetSeniority = constraints.target_seniority as string[] | undefined
  const experienceFromTarget = targetSeniorityToExperienceLevels(targetSeniority)
  const experienceLevels =
    experienceFromTarget.length > 0
      ? experienceFromTarget
      : ((preferences.experience_levels as string[]) ?? [])

  return {
    primaryRoles: (preferences.primary_roles as string[]) ?? [],
    secondaryRoles: (preferences.secondary_roles as string[]) ?? [],
    rolePoolIds: poolIds,
    internshipOnly: Boolean(constraints.internship_only),
    fulltimeOnly: Boolean(constraints.fulltime_only),
    workModels: (preferences.work_models as string[]) ?? [],
    experienceLevels,
    minYearsExperience:
      preferences.min_years_experience != null
        ? Number(preferences.min_years_experience)
        : null,
    maxJobAgeDays:
      preferences.max_job_age_days != null ? Number(preferences.max_job_age_days) : null,
    openToAllSalary: constraints.minimum_salary == null,
    minimumSalary:
      constraints.minimum_salary != null ? String(constraints.minimum_salary) : "",
    sponsorshipRequired: Boolean(constraints.sponsorship_required),
    preferredIndustries: (preferences.preferred_industries as string[]) ?? [],
    excludedIndustries: (preferences.excluded_industries as string[]) ?? [],
    preferredSkills: (preferences.preferred_skills as string[]) ?? [],
    excludedSkills: (preferences.excluded_skills as string[]) ?? [],
    roleType: (preferences.role_type as "ic" | "manager" | "") ?? "",
    roleIntents: Array.isArray(preferences.primary_role_intents)
      ? (preferences.primary_role_intents as string[])
      : Array.isArray(preferences.role_intents)
        ? (preferences.role_intents as string[])
        : ["engineer", "researcher"],
    preferredLocations: (preferences.preferred_locations as string[]) ?? [],
    remotePreference: String(preferences.remote_preference ?? ""),
    eeo: eeoFromApiPayload(constraints.eeo as Record<string, unknown> | undefined),
  }
}

export function jobFiltersToApiPayload(state: JobFiltersState): {
  constraints: Record<string, unknown>
  preferences: Record<string, unknown>
} {
  const suffix = employmentSuffix(state)
  const rolePoolIds =
    state.rolePoolIds.length > 0
      ? state.rolePoolIds
      : poolIdsForRoles(state.primaryRoles, suffix)

  return {
    constraints: {
      sponsorship_required: state.sponsorshipRequired,
      internship_only: state.internshipOnly,
      fulltime_only: state.fulltimeOnly,
      minimum_salary: state.openToAllSalary
        ? null
        : state.minimumSalary
          ? Number(state.minimumSalary)
          : null,
      target_seniority: experienceLevelsToTargetSeniority(state.experienceLevels),
      eeo: eeoToApiPayload(state.eeo),
    },
    preferences: {
      primary_roles: state.primaryRoles,
      secondary_roles: state.secondaryRoles,
      role_pool_ids: rolePoolIds,
      work_models: state.workModels,
      experience_levels: state.experienceLevels,
      min_years_experience: state.minYearsExperience,
      max_job_age_days: state.maxJobAgeDays,
      preferred_industries: state.preferredIndustries,
      excluded_industries: state.excludedIndustries,
      preferred_skills: state.preferredSkills,
      excluded_skills: state.excludedSkills,
      role_type: state.roleType || null,
      primary_role_intents: state.roleIntents,
      role_intents: state.roleIntents,
      preferred_locations: state.preferredLocations,
      remote_preference: state.remotePreference || null,
    },
  }
}

export { EXPERIENCE_LEVELS } from "@/lib/profile/job-filters-constants"

export const DATE_POSTED_OPTIONS = [
  { value: 1, label: "Past 24 hours" },
  { value: 3, label: "Past 3 days" },
  { value: 7, label: "Past week" },
  { value: 30, label: "Past month" },
]

export const WORK_MODEL_OPTIONS = ["Onsite", "Hybrid", "Remote"]

export const ROLE_INTENT_OPTIONS = [
  { value: "engineer", label: "Engineer" },
  { value: "researcher", label: "Researcher" },
  { value: "consultant", label: "Consultant" },
  { value: "educator", label: "Educator" },
  { value: "manager", label: "Manager" },
  { value: "analyst", label: "Analyst" },
  { value: "accountant", label: "Accountant" },
  { value: "auditor", label: "Auditor" },
  { value: "investment_banker", label: "Investment banker" },
  { value: "sales", label: "Sales" },
  { value: "operations", label: "Operations" },
  { value: "legal", label: "Legal" },
  { value: "other", label: "Other" },
]

export const JOB_TYPE_OPTIONS = [
  { key: "fulltimeOnly", label: "Full-time" },
  { key: "internshipOnly", label: "Internship" },
]
