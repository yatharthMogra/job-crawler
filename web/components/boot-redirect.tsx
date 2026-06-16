"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useSession as useNextAuthSession } from "next-auth/react"
import { useSession } from "@/components/session-provider"
import { resolveBootDestination } from "@/lib/boot-routing"
import { getStoredCandidateId, setMockOnboardingComplete, setStoredCandidateId } from "@/lib/session"

export function BootRedirect() {
  const router = useRouter()
  const { data: nextAuthSession, status: nextAuthStatus } = useNextAuthSession()
  const { candidateId, loading: sessionLoading } = useSession()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (nextAuthStatus === "loading" || sessionLoading) return

    const authCandidateId = nextAuthSession?.candidateId
    if (authCandidateId && authCandidateId !== candidateId) {
      setStoredCandidateId(authCandidateId)
      return
    }

    void (async () => {
      try {
        const dest = await resolveBootDestination()
        if (dest === "/jobs/recommended") {
          setMockOnboardingComplete(true)
        }
        router.replace(dest)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load session")
      }
    })()
  }, [nextAuthStatus, sessionLoading, nextAuthSession?.candidateId, candidateId, router])

  if (error) {
    return (
      <div className="flow-page-bg flex min-h-screen items-center justify-center">
        <p className="text-sm text-destructive">{error}</p>
      </div>
    )
  }

  return (
    <div className="flow-page-bg flex min-h-screen items-center justify-center">
      <div className="flex gap-1.5" aria-label="Loading">
        <span className="size-1.5 animate-bounce rounded-full bg-primary/40 [animation-delay:-0.3s]" />
        <span className="size-1.5 animate-bounce rounded-full bg-primary/50 [animation-delay:-0.15s]" />
        <span className="size-1.5 animate-bounce rounded-full bg-primary/40" />
      </div>
    </div>
  )
}
