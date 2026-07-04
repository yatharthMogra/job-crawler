"use client"

import { useEffect } from "react"
import { ProfileCommandPage } from "@/components/profile/profile-command-page"
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
      <div className="px-6 py-8">
        <FeedSkeleton count={3} />
      </div>
    )
  }

  return (
    <>
      <ProfileCommandPage
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
