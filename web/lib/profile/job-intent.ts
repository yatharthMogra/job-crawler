import type { ProfileResponse } from "@/lib/profile/api-types"
import { eeoFromApiPayload, eeoToApiPayload, emptyEeo, type EeoState } from "@/lib/profile/eeo"
import { poolIdsForRoles, sanitizeCatalogRoles } from "@/lib/profile/role-catalog"

export interface JobIntentState {
  primaryRoles: string[]
  secondaryRoles: string[]
  sponsorshipRequired: boolean
  visaType: string
  workAuthorization: string
  internshipOnly: boolean
  fulltimeOnly: boolean
  minimumHourlyRate: string
  preferredLocations: string[]
  remotePreference: string
  preferredIndustries: string[]
  fullTimeExperienceYears: number | null
  isCurrentlyEnrolled: boolean | null
  expectedGraduationDate: string
  eeo: EeoState
}

export function emptyJobIntent(): JobIntentState {
  return {
    primaryRoles: [],
    secondaryRoles: [],
    sponsorshipRequired: false,
    visaType: "",
    workAuthorization: "",
    internshipOnly: false,
    fulltimeOnly: false,
    minimumHourlyRate: "",
    preferredLocations: [],
    remotePreference: "",
    preferredIndustries: [],
    fullTimeExperienceYears: null,
    isCurrentlyEnrolled: null,
    expectedGraduationDate: "",
    eeo: emptyEeo(),
  }
}

export function profileToJobIntent(profile: ProfileResponse): JobIntentState {
  const constraints = profile.constraints ?? {}
  const preferences = profile.preferences ?? {}
  return {
    primaryRoles: sanitizeCatalogRoles((preferences.primary_roles as string[]) ?? []),
    secondaryRoles: sanitizeCatalogRoles((preferences.secondary_roles as string[]) ?? []),
    sponsorshipRequired: Boolean(constraints.sponsorship_required),
    visaType: String(constraints.visa_type ?? ""),
    workAuthorization: String(constraints.work_authorization ?? ""),
    internshipOnly: Boolean(constraints.internship_only),
    fulltimeOnly: Boolean(constraints.fulltime_only),
    minimumHourlyRate:
      constraints.minimum_hourly_rate != null ? String(constraints.minimum_hourly_rate) : "",
    preferredLocations: (preferences.preferred_locations as string[]) ?? [],
    remotePreference: String(preferences.remote_preference ?? ""),
    preferredIndustries: (preferences.preferred_industries as string[]) ?? [],
    fullTimeExperienceYears:
      constraints.full_time_experience_years != null
        ? Number(constraints.full_time_experience_years)
        : null,
    isCurrentlyEnrolled:
      constraints.is_currently_enrolled != null
        ? Boolean(constraints.is_currently_enrolled)
        : null,
    expectedGraduationDate: String(constraints.expected_graduation_date ?? ""),
    eeo: eeoFromApiPayload(constraints.eeo as Record<string, unknown> | undefined),
  }
}

export function jobIntentToApiPayload(state: JobIntentState): {
  constraints: Record<string, unknown>
  preferences: Record<string, unknown>
} {
  return {
    constraints: {
      sponsorship_required: state.sponsorshipRequired,
      visa_type: state.visaType || null,
      work_authorization: state.workAuthorization || null,
      internship_only: state.internshipOnly,
      fulltime_only: state.fulltimeOnly,
      minimum_hourly_rate: state.minimumHourlyRate ? Number(state.minimumHourlyRate) : null,
      full_time_experience_years: state.fullTimeExperienceYears,
      is_currently_enrolled: state.isCurrentlyEnrolled,
      expected_graduation_date: state.expectedGraduationDate || null,
      eeo: eeoToApiPayload(state.eeo),
    },
    preferences: {
      primary_roles: sanitizeCatalogRoles(state.primaryRoles),
      secondary_roles: sanitizeCatalogRoles(state.secondaryRoles).filter(
        (r) => !sanitizeCatalogRoles(state.primaryRoles).includes(r),
      ),
      role_pool_ids: poolIdsForRoles(
        sanitizeCatalogRoles(state.primaryRoles),
        state.internshipOnly && !state.fulltimeOnly ? "INTERNSHIP" : "FULLTIME",
      ),
      preferred_locations: state.preferredLocations,
      remote_preference: state.remotePreference || null,
      preferred_industries: state.preferredIndustries,
    },
  }
}

export function needsJobIntent(profile: ProfileResponse): boolean {
  const roles = profile.preferences?.primary_roles
  return !Array.isArray(roles) || roles.length === 0
}

export function experienceYearsFromReviewExperiences(
  experiences: Array<{ durationMonths: number }>,
): number | null {
  const months = experiences.reduce((sum, item) => sum + (item.durationMonths || 0), 0)
  if (months <= 0) {
    return null
  }
  return Math.round((months / 12) * 10) / 10
}
