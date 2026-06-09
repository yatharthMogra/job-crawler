"use client"

import { useEffect } from "react"
import { ProfileTabs } from "@/components/profile/profile-tabs"
import { ProfileEditDialog } from "@/components/profile/profile-edit-dialog"
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
    openJobIntent,
  } = useProfileFlow()

  useEffect(() => {
    if (candidateId) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, loadProfileHome])

  if (!profileHome) {
    return (
      <div>
        <div className="border-b border-zinc-200/80 bg-white px-6 py-4">
          <h1 className="text-lg font-bold tracking-tight text-zinc-900">Profile</h1>
        </div>
        <div className="px-6 py-4">
          <FeedSkeleton count={3} />
        </div>
      </div>
    )
  }

  return (
    <>
      <ProfileTabs
        data={profileHome}
        onEditSection={setEditSection}
        onSetTargetRoles={openJobIntent}
      />
      <ProfileEditDialog
        section={editSection}
        onClose={() => setEditSection(null)}
        onSave={handleProfileEdit}
        initialValues={
          editSection === "constraints"
            ? (rawProfile?.constraints as Record<string, unknown>)
            : editSection === "preferences"
              ? (rawProfile?.preferences as Record<string, unknown>)
              : editSection === "education"
                ? (rawProfile?.education as Record<string, unknown>)
                : undefined
        }
        contactValues={profileHome.contact}
        eeoValues={profileHome.eeo}
      />
    </>
  )
}
