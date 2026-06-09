"use client"

import { useRouter } from "next/navigation"
import { OnboardingScreen } from "@/components/profile/screens/onboarding-screen"
import { useSession } from "@/components/session-provider"
import { resolveBootDestination } from "@/lib/boot-routing"
import { useMockData } from "@/lib/session"

export default function OnboardingPage() {
  const router = useRouter()
  const { setCandidateId } = useSession()
  const mockMode = useMockData()

  async function handleComplete(id: string) {
    setCandidateId(id)
    if (mockMode) {
      router.push("/profile/upload")
      return
    }
    const dest = await resolveBootDestination()
    router.push(dest)
  }

  return <OnboardingScreen onComplete={handleComplete} />
}
