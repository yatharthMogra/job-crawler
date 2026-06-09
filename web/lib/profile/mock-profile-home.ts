import { buildCommittedProfile, withDefaultProfileFields } from "@/lib/profile/build-profile"
import { eeoToDisplayRows } from "@/lib/profile/eeo"
import type { JobIntentState } from "@/lib/profile/job-intent"
import { emptyJobIntent } from "@/lib/profile/job-intent"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import { initialReviewState } from "@/lib/profile/profile-data"

function approvedReviewState() {
  const approve = <T extends { status: string }>(items: T[]) =>
    items.map((item) => ({ ...item, status: "approved" as const }))
  return {
    ...initialReviewState,
    skills: approve(initialReviewState.skills),
    experiences: approve(initialReviewState.experiences),
    projects: approve(initialReviewState.projects),
    certifications: approve(initialReviewState.certifications),
    education: approve(initialReviewState.education),
  }
}

export function defaultMockJobIntent(): JobIntentState {
  return {
    ...emptyJobIntent(),
    primaryRoles: ["Backend Engineer", "Full Stack Engineer"],
    secondaryRoles: ["Platform Engineer"],
    preferredLocations: ["New York, NY", "Remote (US)"],
    remotePreference: "hybrid",
    eeo: {
      authorizedToWorkUs: true,
      hasDisability: false,
      gender: "Male",
      requiresSponsorship: true,
      identifiesLgbtq: false,
      isVeteran: false,
      race: "Asian",
      hispanicLatino: false,
      sexualOrientation: "Heterosexual",
    },
  }
}

export function buildMockProfileHome(
  jobIntent: JobIntentState = defaultMockJobIntent(),
): ProfileHomeData {
  const built = withDefaultProfileFields(buildCommittedProfile(approvedReviewState()))
  built.primaryRoles = jobIntent.primaryRoles
  built.secondaryRoles = jobIntent.secondaryRoles
  built.eeo = jobIntent.eeo

  const mockResumes = [
    {
      id: "mock-resume-1",
      originalFilename: "Alex_Rivera_Resume.pdf",
      displayLabel: null as string | null,
      uploadedAt: new Date(Date.now() - 3 * 24 * 3600 * 1000).toISOString(),
      fileSizeBytes: 245_000,
    },
  ]

  return {
    candidateName: "Alex Rivera",
    email: "alex.rivera@example.com",
    contact: built.contact,
    educationEntries: built.educationEntries,
    resumeSectionOrder: built.resumeSectionOrder,
    eeo: jobIntent.eeo,
    eeoRows: eeoToDisplayRows(jobIntent.eeo),
    profile: built,
    primaryRoles: jobIntent.primaryRoles,
    secondaryRoles: jobIntent.secondaryRoles,
    hasTargetRoles: jobIntent.primaryRoles.length > 0,
    resumes: mockResumes,
    constraints: [
      { label: "Work Authorization", value: "Authorized to work in the US" },
      { label: "Sponsorship", value: "Requires sponsorship" },
    ],
    preferences: [
      { label: "Primary Roles", value: jobIntent.primaryRoles.join(", ") || "—" },
      { label: "Locations", value: jobIntent.preferredLocations.join(", ") || "—" },
      { label: "Remote", value: jobIntent.remotePreference || "Flexible" },
    ],
    version: 1,
    lastUpdated: new Date().toISOString(),
    resumeCount: mockResumes.length,
  }
}
