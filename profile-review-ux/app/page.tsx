"use client"

import { useCallback, useEffect, useState } from "react"
import { initialReviewState, type ReviewState } from "@/lib/profile-data"
import type { CommittedProfile } from "@/lib/build-profile"
import type { ProfileHomeData } from "@/lib/map-profile"
import {
  emptyJobIntent,
  jobIntentToApiPayload,
  needsJobIntent,
  profileToJobIntent,
  type JobIntentState,
} from "@/lib/job-intent"
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
} from "@/lib/api"
import { eeoFromApiPayload, eeoToDisplayRows } from "@/lib/eeo"
import type { ContactInfo } from "@/lib/contact"
import { buildConfirmationFromProfileHome, mapApiToProfileHome } from "@/lib/map-profile"
import {
  collectApprovedOperationIds,
  emptyReviewState,
  mapPendingPatchToReviewState,
} from "@/lib/map-patch"
import { getStoredCandidateId, setStoredCandidateId, useMockData } from "@/lib/session"
import { buildCommittedProfile } from "@/lib/build-profile"
import { OnboardingScreen } from "@/components/screens/onboarding-screen"
import { UploadScreen } from "@/components/screens/upload-screen"
import { ProcessingScreen } from "@/components/screens/processing-screen"
import { ReviewScreen } from "@/components/screens/review-screen"
import { JobIntentScreen } from "@/components/screens/job-intent-screen"
import { ConfirmationScreen } from "@/components/screens/confirmation-screen"
import { ProfileHome } from "@/components/screens/profile-home"
import type { ProfileResponse } from "@/lib/api-types"
import type { EditSection } from "@/components/profile-edit-dialog"

type Stage =
  | "loading"
  | "onboarding"
  | "upload"
  | "processing"
  | "evidence-review"
  | "job-intent"
  | "confirmation"
  | "profile"

export default function Page() {
  const mockMode = useMockData()
  const [stage, setStage] = useState<Stage>("loading")
  const [candidateId, setCandidateId] = useState<string | null>(null)
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
  const [jobIntentSource, setJobIntentSource] = useState<"onboarding" | "profile">("onboarding")

  const loadProfileHome = useCallback(async (id: string) => {
    const [candidate, profile, evidence, resumes] = await Promise.all([
      getCandidate(id),
      getProfile(id),
      getEvidence(id),
      listResumes(id),
    ])
    const home = mapApiToProfileHome(candidate, profile, evidence.evidence, resumes)
    setRawProfile(profile)
    setProfileHome(home)
    setHasExistingProfile(true)
    return { profile, home }
  }, [])

  const loadPendingReview = useCallback(async (id: string) => {
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
    setStage("evidence-review")
  }, [])

  useEffect(() => {
    async function boot() {
      if (mockMode) {
        setReviewState(initialReviewState)
        setStage("upload")
        return
      }

      const storedId = getStoredCandidateId()
      if (!storedId) {
        setStage("onboarding")
        return
      }

      setCandidateId(storedId)
      try {
        await getCandidate(storedId)

        try {
          await loadPendingReview(storedId)
          return
        } catch (err) {
          if (!(err instanceof ApiError && err.status === 404)) {
            throw err
          }
        }

        try {
          const { profile } = await loadProfileHome(storedId)
          if (needsJobIntent(profile)) {
            setJobIntent(profileToJobIntent(profile))
            setJobIntentSource("onboarding")
            setStage("job-intent")
          } else {
            setStage("profile")
          }
        } catch (err) {
          if (err instanceof ApiError && err.status === 404) {
            setStage("upload")
          } else {
            throw err
          }
        }
      } catch {
        setStage("onboarding")
      }
    }

    void boot()
  }, [mockMode, loadProfileHome, loadPendingReview])

  async function handleUploadSelected(selected: File) {
    setFile(selected)
    setFileName(selected.name)
    setUploadError(null)
    setStage("processing")
  }

  const processUpload = useCallback(async () => {
    if (mockMode) {
      setReviewState(initialReviewState)
      setPatchId("mock-patch")
      setStage("evidence-review")
      return
    }
    if (!candidateId || !file) throw new Error("Missing candidate or file")

    try {
      const result = await uploadResume(candidateId, file)
      setPatchId(result.patch_id)
      const [pending, evidence] = await Promise.all([
        getPendingPatch(candidateId),
        getEvidence(candidateId),
      ])
      setReviewState(mapPendingPatchToReviewState(pending, evidence.evidence))
      setStage("evidence-review")
    } catch (err) {
      if (err instanceof ApiError && err.status === 409 && candidateId) {
        await loadPendingReview(candidateId)
        return
      }
      throw err
    }
  }, [mockMode, candidateId, file, loadPendingReview])

  const handleProcessingComplete = useCallback(() => {
    setStage("evidence-review")
  }, [])

  const handleProcessingRetry = useCallback(() => {
    setStage("upload")
  }, [])

  async function handleSaveEvidenceReview() {
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
      setJobIntentSource("onboarding")
      setStage("job-intent")
      return
    }
    if (!candidateId || !patchId) return

    setSaving(true)
    try {
      const approvedIds = collectApprovedOperationIds(reviewState)
      await commitPatch(candidateId, patchId, approvedIds)
      const profile = await getProfile(candidateId)
      setRawProfile(profile)
      setHasExistingProfile(true)
      setJobIntent(profileToJobIntent(profile))
      setJobIntentSource("onboarding")
      setStage("job-intent")
    } finally {
      setSaving(false)
    }
  }

  async function handleSkipEvidenceReview() {
    if (mockMode) {
      if (hasExistingProfile && profileHome) {
        setStage("profile")
      } else {
        setStage("upload")
      }
      return
    }
    if (candidateId && patchId) {
      await discardPatch(candidateId, patchId)
    }
    if (hasExistingProfile && candidateId) {
      const { profile } = await loadProfileHome(candidateId)
      if (needsJobIntent(profile)) {
        setJobIntent(profileToJobIntent(profile))
        setJobIntentSource("onboarding")
        setStage("job-intent")
      } else {
        setStage("profile")
      }
    } else {
      setStage("upload")
    }
  }

  async function handleSaveJobIntent() {
    if (mockMode) {
      const built = buildCommittedProfile(reviewState)
      built.primaryRoles = jobIntent.primaryRoles
      built.secondaryRoles = jobIntent.secondaryRoles
      built.eeo = jobIntent.eeo
      setConfirmationProfile(built)
      const mockResumes = [
        {
          id: "mock-resume-1",
          originalFilename: "Alex_Rivera_Resume.pdf",
          displayLabel: null as string | null,
          uploadedAt: new Date().toISOString(),
          fileSizeBytes: 245_000,
        },
      ]
      setProfileHome({
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
        constraints: [],
        preferences: [
          ...(jobIntent.preferredLocations.length
            ? [{ label: "Preferred Locations", value: jobIntent.preferredLocations.join(" · ") }]
            : []),
          ...(jobIntent.remotePreference
            ? [{ label: "Remote Preference", value: jobIntent.remotePreference }]
            : []),
        ],
        version: 1,
        lastUpdated: new Date().toISOString(),
        resumeCount: mockResumes.length,
      })
      setHasExistingProfile(true)
      if (jobIntentSource === "profile") {
        setStage("profile")
      } else {
        setStage("confirmation")
      }
      return
    }
    if (!candidateId) return

    setSaving(true)
    try {
      const { constraints, preferences } = jobIntentToApiPayload(jobIntent)
      await patchConstraints(candidateId, constraints)
      await patchPreferences(candidateId, preferences)
      const { home } = await loadProfileHome(candidateId)
      if (jobIntentSource === "profile") {
        setStage("profile")
      } else {
        setConfirmationProfile(buildConfirmationFromProfileHome(home))
        setStage("confirmation")
      }
    } finally {
      setSaving(false)
    }
  }

  async function handleProfileEdit(section: EditSection, values: Record<string, unknown>) {
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
            ? {
                ...prev,
                contact,
                profile: { ...prev.profile, contact },
              }
            : prev,
        )
      }
      return
    }
    if (!candidateId) return
    if (section === "constraints" || section === "eeo") await patchConstraints(candidateId, values)
    else if (section === "preferences") await patchPreferences(candidateId, values)
    else await patchEducation(candidateId, values)
    await loadProfileHome(candidateId)
  }

  async function handleResumeLabelSave(resumeId: string, label: string | null) {
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
    if (!candidateId) return
    await patchResumeLabel(candidateId, resumeId, label)
    await loadProfileHome(candidateId)
  }

  function resetForNewResume() {
    setFile(null)
    setFileName("")
    setPatchId(null)
    setReviewState(emptyReviewState())
    setUploadError(null)
    setStage("upload")
  }

  function openJobIntentFromProfile() {
    if (rawProfile) {
      setJobIntent(profileToJobIntent(rawProfile))
    } else {
      setJobIntent(emptyJobIntent())
    }
    setJobIntentSource("profile")
    setStage("job-intent")
  }

  if (stage === "loading") {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background">
        <p className="text-sm text-muted-foreground">Loading...</p>
      </main>
    )
  }

  if (stage === "onboarding") {
    return (
      <OnboardingScreen
        onComplete={(id) => {
          setCandidateId(id)
          setStoredCandidateId(id)
          setStage("upload")
        }}
      />
    )
  }

  if (stage === "upload") {
    return (
      <UploadScreen
        onAnalyze={handleUploadSelected}
        error={uploadError}
        hasExistingResumes={hasExistingProfile && (profileHome?.resumeCount ?? 0) > 0}
      />
    )
  }

  if (stage === "processing") {
    return (
      <ProcessingScreen
        fileName={fileName}
        onProcess={processUpload}
        onComplete={handleProcessingComplete}
        onRetry={handleProcessingRetry}
      />
    )
  }

  if (stage === "evidence-review") {
    return (
      <ReviewScreen
        state={reviewState}
        setState={setReviewState}
        onSave={handleSaveEvidenceReview}
        onSkip={handleSkipEvidenceReview}
        saving={saving}
      />
    )
  }

  if (stage === "job-intent") {
    return (
      <JobIntentScreen
        state={jobIntent}
        onChange={setJobIntent}
        onSubmit={handleSaveJobIntent}
        saving={saving}
      />
    )
  }

  if (stage === "confirmation" && confirmationProfile) {
    return (
      <ConfirmationScreen
        profile={confirmationProfile}
        onViewProfile={() => setStage("profile")}
      />
    )
  }

  if (stage === "profile" && profileHome) {
    return (
      <ProfileHome
        data={profileHome}
        onUploadNew={resetForNewResume}
        onEditSection={setEditSection}
        onSetTargetRoles={openJobIntentFromProfile}
        onResumeLabelSave={handleResumeLabelSave}
        editSection={editSection}
        onEditSave={handleProfileEdit}
        rawProfile={rawProfile}
      />
    )
  }

  return (
    <UploadScreen
      onAnalyze={handleUploadSelected}
      error={uploadError}
      hasExistingResumes={hasExistingProfile && (profileHome?.resumeCount ?? 0) > 0}
    />
  )
}
