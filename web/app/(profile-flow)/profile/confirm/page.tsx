"use client"

import { useRouter } from "next/navigation"
import { ConfirmationScreen } from "@/components/profile/screens/confirmation-screen"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"

export default function ConfirmPage() {
  const router = useRouter()
  const { confirmationProfile } = useProfileFlow()

  if (!confirmationProfile) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <p className="text-sm text-muted-foreground">Loading confirmation...</p>
      </div>
    )
  }

  return (
    <ConfirmationScreen
      profile={confirmationProfile}
      onViewProfile={() => router.push("/jobs/recommended")}
    />
  )
}
