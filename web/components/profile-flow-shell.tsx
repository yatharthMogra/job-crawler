"use client"

import { useEffect, type ReactNode } from "react"
import { usePathname, useRouter } from "next/navigation"
import { ProfileFlowProvider } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"

export function ProfileFlowShell({ children }: { children: ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const { candidateId, loading } = useSession()
  const isOnboarding = pathname === "/onboarding"

  useEffect(() => {
    if (loading || isOnboarding) return
    if (!candidateId) {
      router.replace("/onboarding")
    }
  }, [loading, candidateId, isOnboarding, router])

  if (isOnboarding) {
    return <>{children}</>
  }

  if (loading || !candidateId) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50">
        <div className="flex gap-1.5" aria-label="Loading">
          <span className="size-1.5 animate-bounce rounded-full bg-zinc-300 [animation-delay:-0.3s]" />
          <span className="size-1.5 animate-bounce rounded-full bg-zinc-300 [animation-delay:-0.15s]" />
          <span className="size-1.5 animate-bounce rounded-full bg-zinc-300" />
        </div>
      </div>
    )
  }

  return <ProfileFlowProvider candidateId={candidateId}>{children}</ProfileFlowProvider>
}
