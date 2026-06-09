import type { ProfileResponse } from "@/lib/api-types"
import { eeoFromApiPayload, eeoToApiPayload, emptyEeo, type EeoState } from "@/lib/eeo"

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
    eeo: emptyEeo(),
  }
}

export function profileToJobIntent(profile: ProfileResponse): JobIntentState {
  const constraints = profile.constraints ?? {}
  const preferences = profile.preferences ?? {}
  return {
    primaryRoles: (preferences.primary_roles as string[]) ?? [],
    secondaryRoles: (preferences.secondary_roles as string[]) ?? [],
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
      eeo: eeoToApiPayload(state.eeo),
    },
    preferences: {
      primary_roles: state.primaryRoles,
      secondary_roles: state.secondaryRoles,
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
