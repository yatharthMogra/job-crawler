"use client"

import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type Dispatch,
  type ReactNode,
  type SetStateAction,
} from "react"
import { useRouter } from "next/navigation"
import type { CommittedProfile } from "@/lib/profile/build-profile"
import { buildCommittedProfile } from "@/lib/profile/build-profile"
import type { ProfileResponse } from "@/lib/profile/api-types"
import type { ContactInfo } from "@/lib/profile/contact"
import { eeoFromApiPayload, eeoToDisplayRows } from "@/lib/profile/eeo"
import { initialReviewState, type ReviewState } from "@/lib/profile/profile-data"
import {
  ApiError,
  commitPatch,
  discardPatch,
  getCandidate,
  getEvidence,
  getPendingPatch,
  getProfile,
  listResumes,
  patchConstraints,
  patchEducation,
  patchPreferences,
  patchResumeLabel,
  uploadResume,
} from "@/lib/profile/api"
import {
  mapApiToProfileHome,
  type ProfileHomeData,
} from "@/lib/profile/map-profile"
import {
  collectAllPatchOperationIds,
  collectApprovedOperationIds,
  emptyReviewState,
  mapPendingPatchToReviewState,
} from "@/lib/profile/map-patch"
import {
  emptyJobIntent,
  experienceYearsFromReviewExperiences,
  jobIntentToApiPayload,
  needsJobIntent,
  profileToJobIntent,
  type JobIntentState,
} from "@/lib/profile/job-intent"
import { buildMockProfileHome, defaultMockJobIntent } from "@/lib/profile/mock-profile-home"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import { useMockData, setMockOnboardingComplete } from "@/lib/session"
import type { EditSection } from "@/components/profile/profile-edit-dialog"

interface ProfileFlowContextValue {
  file: File | null
  fileName: string
  patchId: string | null
  reviewState: ReviewState
  setReviewState: Dispatch<SetStateAction<ReviewState>>
  jobIntent: JobIntentState
  setJobIntent: Dispatch<SetStateAction<JobIntentState>>
  confirmationProfile: CommittedProfile | null
  profileHome: ProfileHomeData | null
  rawProfile: ProfileResponse | null
  uploadError: string | null
  saving: boolean
  editSection: EditSection | null
  setEditSection: (section: EditSection | null) => void
  hasExistingProfile: boolean
  setUploadFile: (file: File) => void
  processUpload: () => Promise<void>
  saveReview: () => Promise<void>
  skipReview: () => Promise<void>
  saveJobIntent: (redirectTo?: "confirm" | "profile" | "jobs") => Promise<void>
  loadProfileHome: (id: string) => Promise<void>
  handleProfileEdit: (section: EditSection, values: Record<string, unknown>) => Promise<void>
  handleResumeLabelSave: (resumeId: string, label: string | null) => Promise<void>
  uploadResumeInline: (file: File) => Promise<void>
  resetForNewResume: () => void
  loadPendingReview: (id: string) => Promise<void>
  openJobIntent: () => void
}

const ProfileFlowContext = createContext<ProfileFlowContextValue | null>(null)

export function ProfileFlowProvider({
  children,
  candidateId,
}: {
  children: ReactNode
  candidateId: string
}) {
  const router = useRouter()
  const mockMode = useMockData()

  const [file, setFile] = useState<File | null>(null)
  const [fileName, setFileName] = useState("")
  const [patchId, setPatchId] = useState<string | null>(null)
  const [reviewState, setReviewState] = useState<ReviewState>(emptyReviewState())
  const [jobIntent, setJobIntent] = useState<JobIntentState>(emptyJobIntent())
  const [confirmationProfile, setConfirmationProfile] = useState<CommittedProfile | null>(null)
  const [profileHome, setProfileHome] = useState<ProfileHomeData | null>(null)
  const [rawProfile, setRawProfile] = useState<ProfileResponse | null>(null)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [editSection, setEditSection] = useState<EditSection | null>(null)
  const [hasExistingProfile, setHasExistingProfile] = useState(false)

  const loadProfileHome = useCallback(
    async (id: string) => {
      if (mockMode) {
        setProfileHome((prev) => prev ?? buildMockProfileHome(defaultMockJobIntent()))
        setJobIntent((prev) => (prev.primaryRoles.length > 0 ? prev : defaultMockJobIntent()))
        setHasExistingProfile(true)
        return
      }

      const [candidate, profile, evidence, resumes] = await Promise.all([
        getCandidate(id),
        getProfile(id),
        getEvidence(id),
        listResumes(id),
      ])
      setRawProfile(profile)
      setProfileHome(mapApiToProfileHome(candidate, profile, evidence.evidence, resumes))
      setJobIntent(profileToJobIntent(profile))
      setHasExistingProfile(true)
    },
    [mockMode],
  )

  const loadPendingReview = useCallback(async (id: string) => {
    if (mockMode) {
      setPatchId("mock-patch")
      setReviewState(initialReviewState)
      setHasExistingProfile(false)
      return
    }

    const [pending, evidence] = await Promise.all([getPendingPatch(id), getEvidence(id)])
    setPatchId(pending.patch_id)
    setReviewState(mapPendingPatchToReviewState(pending, evidence.evidence))
    try {
      await getProfile(id)
      setHasExistingProfile(true)
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setHasExistingProfile(false)
      } else {
        throw err
      }
    }
  }, [mockMode])

  const setUploadFile = useCallback((selected: File) => {
    setFile(selected)
    setFileName(selected.name)
    setUploadError(null)
  }, [])

  const processUpload = useCallback(async () => {
    if (mockMode) {
      setReviewState(initialReviewState)
      setPatchId("mock-patch")
      router.push("/profile/review")
      return
    }
    if (!file) throw new Error("Missing file")

    try {
      const result = await uploadResume(candidateId, file)
      setPatchId(result.patch_id)
      const [pending, evidence] = await Promise.all([
        getPendingPatch(candidateId),
        getEvidence(candidateId),
      ])
      setReviewState(mapPendingPatchToReviewState(pending, evidence.evidence))
      router.push("/profile/review")
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        await loadPendingReview(candidateId)
        router.push("/profile/review")
        return
      }
      throw err
    }
  }, [mockMode, candidateId, file, loadPendingReview, router])

  const saveReview = useCallback(async () => {
    if (mockMode) {
      setJobIntent({
        ...emptyJobIntent(),
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
      })
      router.push("/profile/job-intent")
      return
    }
    if (!patchId) return

    setSaving(true)
    try {
      const approvedIds = collectApprovedOperationIds(reviewState)
      await commitPatch(candidateId, patchId, approvedIds)
      const profile = await getProfile(candidateId)
      setRawProfile(profile)
      setHasExistingProfile(true)
      const intent = profileToJobIntent(profile)
      const derivedYears = experienceYearsFromReviewExperiences(reviewState.experiences)
      setJobIntent({
        ...intent,
        fullTimeExperienceYears:
          intent.fullTimeExperienceYears ?? derivedYears,
      })
      router.push("/profile/job-intent")
    } finally {
      setSaving(false)
    }
  }, [mockMode, candidateId, patchId, reviewState, router])

  const skipReview = useCallback(async () => {
    if (mockMode) {
      router.push(hasExistingProfile ? "/profile" : "/profile/upload")
      return
    }
    if (patchId) {
      await discardPatch(candidateId, patchId)
    }
    if (hasExistingProfile) {
      const profile = await getProfile(candidateId)
      if (needsJobIntent(profile)) {
        setJobIntent(profileToJobIntent(profile))
        router.push("/profile/job-intent")
      } else {
        await loadProfileHome(candidateId)
        router.push("/profile")
      }
    } else {
      router.push("/profile/upload")
    }
  }, [mockMode, candidateId, patchId, hasExistingProfile, loadProfileHome, router])

  const saveJobIntent = useCallback(
    async (redirectTo: "confirm" | "profile" | "jobs" = "jobs") => {
      if (mockMode) {
        setProfileHome(buildMockProfileHome(jobIntent))
        setHasExistingProfile(true)
        setMockOnboardingComplete(true)
        if (redirectTo === "profile") {
          router.push("/profile")
        } else if (redirectTo === "confirm") {
          const built = buildCommittedProfile(reviewState)
          built.primaryRoles = jobIntent.primaryRoles
          built.secondaryRoles = jobIntent.secondaryRoles
          built.eeo = jobIntent.eeo
          setConfirmationProfile(built)
          router.push("/profile/confirm")
        } else {
          router.push("/jobs/recommended")
        }
        return
      }

      setSaving(true)
      try {
        const { constraints, preferences } = jobIntentToApiPayload(jobIntent)
        // Sequential: each PATCH creates a new profile version; parallel calls race on DB constraints.
        await patchConstraints(candidateId, constraints)
        await patchPreferences(candidateId, preferences)
        // Navigate immediately; profile refresh + subscription sync continue in background.
        if (redirectTo === "profile") {
          router.push("/profile")
        } else if (redirectTo === "confirm") {
          router.push("/jobs/recommended")
        } else {
          router.push("/jobs/recommended")
        }
        void loadProfileHome(candidateId).catch(() => undefined)
        void syncSubscriptionsForCandidate(candidateId).catch(() => undefined)
      } finally {
        setSaving(false)
      }
    },
    [mockMode, candidateId, jobIntent, reviewState, profileHome, loadProfileHome, router],
  )

  const handleProfileEdit = useCallback(
    async (section: EditSection, values: Record<string, unknown>) => {
      if (mockMode) {
        if (section === "eeo" && values.eeo) {
          const nextEeo = eeoFromApiPayload(values.eeo as Record<string, unknown>)
          setJobIntent((prev) => ({ ...prev, eeo: nextEeo }))
          setProfileHome((prev) =>
            prev
              ? {
                  ...prev,
                  eeo: nextEeo,
                  eeoRows: eeoToDisplayRows(nextEeo),
                  profile: { ...prev.profile, eeo: nextEeo },
                }
              : prev,
          )
        }
        if (section === "contact" && values.contact) {
          const contact = values.contact as ContactInfo
          setProfileHome((prev) =>
            prev
              ? { ...prev, contact, profile: { ...prev.profile, contact } }
              : prev,
          )
        }
        return
      }
      if (section === "constraints" || section === "eeo") {
        await patchConstraints(candidateId, values)
      } else if (section === "preferences") {
        await patchPreferences(candidateId, values)
      } else {
        await patchEducation(candidateId, values)
      }
      await loadProfileHome(candidateId)
      if (section === "preferences" || section === "constraints") {
        await syncSubscriptionsForCandidate(candidateId)
      }
    },
    [mockMode, candidateId, loadProfileHome],
  )

  const handleResumeLabelSave = useCallback(
    async (resumeId: string, label: string | null) => {
      if (mockMode) {
        setProfileHome((prev) => {
          if (!prev) return prev
          return {
            ...prev,
            resumes: prev.resumes.map((r) =>
              r.id === resumeId ? { ...r, displayLabel: label } : r,
            ),
          }
        })
        return
      }
      await patchResumeLabel(candidateId, resumeId, label)
      await loadProfileHome(candidateId)
    },
    [mockMode, candidateId, loadProfileHome],
  )

  const resetForNewResume = useCallback(() => {
    setFile(null)
    setFileName("")
    setPatchId(null)
    setReviewState(emptyReviewState())
    setUploadError(null)
    router.push("/profile/upload")
  }, [router])

  const uploadResumeInline = useCallback(
    async (selected: File) => {
      setUploadError(null)

      if (mockMode) {
        setProfileHome((prev) => {
          const base = prev ?? buildMockProfileHome(defaultMockJobIntent())
          const newResume = {
            id: `mock-resume-${Date.now()}`,
            originalFilename: selected.name,
            displayLabel: null as string | null,
            uploadedAt: new Date().toISOString(),
            fileSizeBytes: selected.size,
          }
          const resumes = [newResume, ...base.resumes]
          return { ...base, resumes, resumeCount: resumes.length }
        })
        setHasExistingProfile(true)
        return
      }

      async function discardPendingIfAny() {
        try {
          const pending = await getPendingPatch(candidateId)
          await discardPatch(candidateId, pending.patch_id)
        } catch (err) {
          if (err instanceof ApiError && err.status === 404) return
          throw err
        }
      }

      await discardPendingIfAny()

      const result = await uploadResume(candidateId, selected)
      const pending = await getPendingPatch(candidateId)
      const approvedIds = collectAllPatchOperationIds(pending)
      if (approvedIds.length > 0) {
        await commitPatch(candidateId, result.patch_id, approvedIds)
      }
      await loadProfileHome(candidateId)
    },
    [mockMode, candidateId, loadProfileHome],
  )

  const openJobIntent = useCallback(() => {
    if (rawProfile) {
      setJobIntent(profileToJobIntent(rawProfile))
    }
    router.push("/profile/job-intent")
  }, [rawProfile, router])

  const value = useMemo(
    () => ({
      file,
      fileName,
      patchId,
      reviewState,
      setReviewState,
      jobIntent,
      setJobIntent,
      confirmationProfile,
      profileHome,
      rawProfile,
      uploadError,
      saving,
      editSection,
      setEditSection,
      hasExistingProfile,
      setUploadFile,
      processUpload,
      saveReview,
      skipReview,
      saveJobIntent,
      loadProfileHome,
      handleProfileEdit,
      handleResumeLabelSave,
      uploadResumeInline,
      resetForNewResume,
      loadPendingReview,
      openJobIntent,
    }),
    [
      file,
      fileName,
      patchId,
      reviewState,
      jobIntent,
      confirmationProfile,
      profileHome,
      rawProfile,
      uploadError,
      saving,
      editSection,
      hasExistingProfile,
      setUploadFile,
      processUpload,
      saveReview,
      skipReview,
      saveJobIntent,
      loadProfileHome,
      handleProfileEdit,
      handleResumeLabelSave,
      uploadResumeInline,
      resetForNewResume,
      loadPendingReview,
      openJobIntent,
    ],
  )

  return <ProfileFlowContext.Provider value={value}>{children}</ProfileFlowContext.Provider>
}

export function useProfileFlow() {
  const ctx = useContext(ProfileFlowContext)
  if (!ctx) throw new Error("useProfileFlow must be used within ProfileFlowProvider")
  return ctx
}
