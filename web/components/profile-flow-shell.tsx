"use client"

import { useEffect, useState, type ReactNode } from "react"
import { usePathname, useRouter } from "next/navigation"
import { ProfileFlowProvider } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import {
  getStoredCandidateId,
  MOCK_CANDIDATE_ID,
  setMockCandidateInfo,
  setStoredCandidateId,
  useMockData,
} from "@/lib/session"

export function ProfileFlowShell({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const mockMode = useMockData()
  const { candidateId, loading, setCandidateId } = useSession()
  const [localId, setLocalId] = useState<string | null>(() =>
    typeof window === "undefined" ? null : getStoredCandidateId(),
  )
  const resolvedId = candidateId ?? localId
  const isOnboarding = pathname === "/onboarding"

  // Bootstrap a mock session so profile-flow pages render without a backend.
  useEffect(() => {
    if (!mockMode || getStoredCandidateId()) return
    setMockCandidateInfo("Alex Rivera", "alex.rivera@example.com")
    setStoredCandidateId(MOCK_CANDIDATE_ID)
    setCandidateId(MOCK_CANDIDATE_ID)
    setLocalId(MOCK_CANDIDATE_ID)
  }, [mockMode, setCandidateId])

  useEffect(() => {
    if (loading || isOnboarding) return
    if (!resolvedId) {
      const loginUrl = `/login?callbackUrl=${encodeURIComponent(pathname)}`
      router.replace(loginUrl)
    }
  }, [loading, resolvedId, isOnboarding, pathname, router])

  if (isOnboarding) {
    return <>{children}</>
  }

  if (loading) {
    return (
      <div className="flow-page-bg flex min-h-screen items-center justify-center">
        <div className="flex gap-1.5" aria-label="Loading">
          <span className="size-1.5 animate-bounce rounded-full bg-primary/40 [animation-delay:-0.3s]" />
          <span className="size-1.5 animate-bounce rounded-full bg-brand/50 [animation-delay:-0.15s]" />
          <span className="size-1.5 animate-bounce rounded-full bg-primary/40" />
        </div>
      </div>
    )
  }

  if (!resolvedId) {
    return null
  }

  return <ProfileFlowProvider candidateId={resolvedId}>{children}</ProfileFlowProvider>
}
