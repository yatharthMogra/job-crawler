"use client"

import { useRouter } from "next/navigation"
import { OnboardingScreen } from "@/components/profile/screens/onboarding-screen"
import { useSession } from "@/components/session-provider"
import { resolveBootDestination } from "@/lib/boot-routing"

export default function OnboardingPage() {
  const router = useRouter()
  const { setCandidateId } = useSession()

  async function handleComplete(id: string) {
    setCandidateId(id)
    const dest = await resolveBootDestination()
    router.push(dest)
  }

  return <OnboardingScreen onComplete={handleComplete} />
}
