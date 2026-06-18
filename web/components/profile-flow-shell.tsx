"use client"

import { useEffect, type ReactNode } from "react"
import { usePathname, useRouter } from "next/navigation"
import { ProfileFlowProvider } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { getStoredCandidateId } from "@/lib/session"

export function ProfileFlowShell({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const { candidateId, loading } = useSession()
  const resolvedId = candidateId ?? getStoredCandidateId()
  const isOnboarding = pathname === "/onboarding"

  useEffect(() => {
    if (loading || isOnboarding) return
    if (!resolvedId) {
      router.replace("/login")
    }
  }, [loading, resolvedId, isOnboarding, router])

  if (isOnboarding) {
    return <>{children}</>
  }

  if (loading || !resolvedId) {
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

  return <ProfileFlowProvider candidateId={resolvedId}>{children}</ProfileFlowProvider>
}
