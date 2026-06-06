"use client"

import { useCallback, useEffect, useState } from "react"
import { initialReviewState, type ReviewState } from "@/lib/profile-data"
import type { CommittedProfile } from "@/lib/build-profile"
import type { ProfileHomeData } from "@/lib/map-profile"
import {
  ApiError,
  commitPatch,
  discardPatch,
  getCandidate,
  getCapabilities,
  getEvidence,
  getPendingPatch,
  getProfile,
  listResumes,
  patchConstraints,
  patchEducation,
  patchPreferences,
  uploadResume,
} from "@/lib/api"
import {
  buildConfirmationProfile,
  mapApiToProfileHome,
} from "@/lib/map-profile"
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
import { ConfirmationScreen } from "@/components/screens/confirmation-screen"
import { ProfileHome } from "@/components/screens/profile-home"
import type { ProfileResponse } from "@/lib/api-types"
import type { EditSection } from "@/components/profile-edit-dialog"

type Stage = "loading" | "onboarding" | "upload" | "processing" | "review" | "confirmation" | "profile"

export default function Page() {
  const mockMode = useMockData()
  const [stage, setStage] = useState<Stage>("loading")
  const [candidateId, setCandidateId] = useState<string | null>(null)
  const [file, setFile] = useState<File | null>(null)
  const [fileName, setFileName] = useState("")
  const [patchId, setPatchId] = useState<string | null>(null)
  const [reviewState, setReviewState] = useState<ReviewState>(emptyReviewState())
  const [confirmationProfile, setConfirmationProfile] = useState<CommittedProfile | null>(null)
  const [profileHome, setProfileHome] = useState<ProfileHomeData | null>(null)
  const [rawProfile, setRawProfile] = useState<ProfileResponse | null>(null)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)
  const [editSection, setEditSection] = useState<EditSection | null>(null)
  const [hasExistingProfile, setHasExistingProfile] = useState(false)

  const loadProfileHome = useCallback(async (id: string) => {
    const [candidate, profile, capabilities, evidence, resumes] = await Promise.all([
      getCandidate(id),
      getProfile(id),
      getCapabilities(id),
      getEvidence(id),
      listResumes(id),
    ])
    setRawProfile(profile)
    setProfileHome(mapApiToProfileHome(candidate, profile, capabilities.capabilities, evidence.evidence, resumes.length))
    setHasExistingProfile(true)
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
    setStage("review")
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
          await loadProfileHome(storedId)
          setStage("profile")
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
      setStage("review")
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
      setStage("review")
    } catch (err) {
      if (err instanceof ApiError && err.status === 409 && candidateId) {
        await loadPendingReview(candidateId)
        return
      }
      throw err
    }
  }, [mockMode, candidateId, file, loadPendingReview])

  const handleProcessingComplete = useCallback(() => {
    setStage("review")
  }, [])

  const handleProcessingRetry = useCallback(() => {
    setStage("upload")
  }, [])

  async function handleSaveReview() {
    if (mockMode) {
      const built = buildCommittedProfile(reviewState)
      setConfirmationProfile(built)
      setProfileHome({
        candidateName: "Alex Rivera",
        educationLine: "MS Computer Science · NYU · Graduating May 2027",
        profile: built,
        constraints: built.preferences.filter((p) =>
          ["Sponsorship Required", "Visa Type", "Work Authorization", "Minimum Hourly Rate", "Role Type"].includes(p.label),
        ),
        preferences: built.preferences.filter(
          (p) => !["Sponsorship Required", "Visa Type", "Work Authorization", "Minimum Hourly Rate", "Role Type"].includes(p.label),
        ),
        version: 1,
        lastUpdated: new Date().toISOString(),
        resumeCount: 1,
      })
      setHasExistingProfile(true)
      setStage("confirmation")
      return
    }
    if (!candidateId || !patchId) return

    setSaving(true)
    try {
      const approvedIds = collectApprovedOperationIds(reviewState)
      await commitPatch(candidateId, patchId, approvedIds)
      const capabilities = await getCapabilities(candidateId)
      setConfirmationProfile(buildConfirmationProfile(reviewState, capabilities.capabilities))
      await loadProfileHome(candidateId)
      setStage("confirmation")
    } finally {
      setSaving(false)
    }
  }

  async function handleSkipReview() {
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
      await loadProfileHome(candidateId)
      setStage("profile")
    } else {
      setStage("upload")
    }
  }

  async function handleProfileEdit(section: EditSection, values: Record<string, unknown>) {
    if (!candidateId) return
    if (section === "constraints") await patchConstraints(candidateId, values)
    else if (section === "preferences") await patchPreferences(candidateId, values)
    else await patchEducation(candidateId, values)
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
    return <UploadScreen onAnalyze={handleUploadSelected} error={uploadError} />
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

  if (stage === "review") {
    return (
      <ReviewScreen
        state={reviewState}
        setState={setReviewState}
        onSave={handleSaveReview}
        onSkip={handleSkipReview}
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
        editSection={editSection}
        onEditSave={handleProfileEdit}
        rawProfile={rawProfile}
      />
    )
  }

  return <UploadScreen onAnalyze={handleUploadSelected} error={uploadError} />
}
