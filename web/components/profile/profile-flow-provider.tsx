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
import { initialReviewState, type ReviewState } from "@/lib/profile/profile-data"
import {
  ApiError,
  commitPatch,
  discardPatch,
  getCapabilities,
  getEvidence,
  getPendingPatch,
  getProfile,
  uploadResume,
} from "@/lib/profile/api"
import {
  buildConfirmationProfile,
  mapApiToProfileHome,
  type ProfileHomeData,
} from "@/lib/profile/map-profile"
import {
  collectApprovedOperationIds,
  emptyReviewState,
  mapPendingPatchToReviewState,
} from "@/lib/profile/map-patch"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import { useMockData } from "@/lib/session"
import type { EditSection } from "@/components/profile/profile-edit-dialog"
import {
  getCandidate,
  listResumes,
  patchConstraints,
  patchEducation,
  patchPreferences,
} from "@/lib/profile/api"

interface ProfileFlowContextValue {
  file: File | null
  fileName: string
  patchId: string | null
  reviewState: ReviewState
  setReviewState: Dispatch<SetStateAction<ReviewState>>
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
  loadProfileHome: (id: string) => Promise<void>
  handleProfileEdit: (section: EditSection, values: Record<string, unknown>) => Promise<void>
  resetForNewResume: () => void
  loadPendingReview: (id: string) => Promise<void>
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
    setProfileHome(
      mapApiToProfileHome(candidate, profile, capabilities.capabilities, evidence.evidence, resumes.length),
    )
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
  }, [])

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
      const built = buildCommittedProfile(reviewState)
      setConfirmationProfile(built)
      setHasExistingProfile(true)
      router.push("/profile/confirm")
      return
    }
    if (!patchId) return

    setSaving(true)
    try {
      const approvedIds = collectApprovedOperationIds(reviewState)
      await commitPatch(candidateId, patchId, approvedIds)
      const capabilities = await getCapabilities(candidateId)
      setConfirmationProfile(buildConfirmationProfile(reviewState, capabilities.capabilities))
      await loadProfileHome(candidateId)
      await syncSubscriptionsForCandidate(candidateId)
      router.push("/profile/confirm")
    } finally {
      setSaving(false)
    }
  }, [mockMode, candidateId, patchId, reviewState, loadProfileHome, router])

  const skipReview = useCallback(async () => {
    if (mockMode) {
      router.push(hasExistingProfile ? "/profile" : "/profile/upload")
      return
    }
    if (patchId) {
      await discardPatch(candidateId, patchId)
    }
    if (hasExistingProfile) {
      await loadProfileHome(candidateId)
      router.push("/profile")
    } else {
      router.push("/profile/upload")
    }
  }, [mockMode, candidateId, patchId, hasExistingProfile, loadProfileHome, router])

  const handleProfileEdit = useCallback(
    async (section: EditSection, values: Record<string, unknown>) => {
      if (section === "constraints") await patchConstraints(candidateId, values)
      else if (section === "preferences") await patchPreferences(candidateId, values)
      else await patchEducation(candidateId, values)
      await loadProfileHome(candidateId)
      await syncSubscriptionsForCandidate(candidateId)
    },
    [candidateId, loadProfileHome],
  )

  const resetForNewResume = useCallback(() => {
    setFile(null)
    setFileName("")
    setPatchId(null)
    setReviewState(emptyReviewState())
    setUploadError(null)
    router.push("/profile/upload")
  }, [router])

  const value = useMemo(
    () => ({
      file,
      fileName,
      patchId,
      reviewState,
      setReviewState,
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
      loadProfileHome,
      handleProfileEdit,
      resetForNewResume,
      loadPendingReview,
    }),
    [
      file,
      fileName,
      patchId,
      reviewState,
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
      loadProfileHome,
      handleProfileEdit,
      resetForNewResume,
      loadPendingReview,
    ],
  )

  return <ProfileFlowContext.Provider value={value}>{children}</ProfileFlowContext.Provider>
}

export function useProfileFlow() {
  const ctx = useContext(ProfileFlowContext)
  if (!ctx) throw new Error("useProfileFlow must be used within ProfileFlowProvider")
  return ctx
}
