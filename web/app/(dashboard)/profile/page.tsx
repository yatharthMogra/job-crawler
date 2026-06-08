"use client"

import { useEffect } from "react"
import { ProfileHome } from "@/components/profile/screens/profile-home"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { FeedSkeleton } from "@/components/card-skeleton"

export default function ProfilePage() {
  const { candidateId } = useSession()
  const {
    profileHome,
    rawProfile,
    editSection,
    setEditSection,
    handleProfileEdit,
    loadProfileHome,
    resetForNewResume,
  } = useProfileFlow()

  useEffect(() => {
    if (candidateId) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, loadProfileHome])

  if (!profileHome) {
    return (
      <div>
        <div className="border-b border-zinc-200 bg-zinc-50 px-6 py-3">
          <h1 className="text-sm font-semibold text-zinc-900">Profile</h1>
        </div>
        <div className="px-6 py-4">
          <FeedSkeleton count={3} />
        </div>
      </div>
    )
  }

  return (
    <ProfileHome
      data={profileHome}
      rawProfile={rawProfile}
      editSection={editSection}
      onEditSection={setEditSection}
      onEditSave={handleProfileEdit}
      onUploadNew={resetForNewResume}
    />
  )
}
