"use client"

import { useEffect, type ReactNode } from "react"
import { usePathname, useRouter } from "next/navigation"
import { JobsProvider } from "@/components/jobs-provider"
import { JobDrawerMount } from "@/components/job-drawer-mount"
import { DashboardSidebar } from "@/components/layout/dashboard-sidebar"
import { ProfileFlowProvider } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { getStoredCandidateId } from "@/lib/session"

export function DashboardShell({ children }: { children: ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const { candidateId, loading } = useSession()
  const resolvedId = candidateId ?? getStoredCandidateId()

  useEffect(() => {
    if (!loading && !resolvedId) {
      router.replace("/login")
    }
  }, [loading, resolvedId, router])

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

  return (
    <ProfileFlowProvider candidateId={resolvedId}>
      <JobsProvider>
        <div className="dashboard-page-bg dashboard-shell">
          <DashboardSidebar />
          <main className="dashboard-shell-main">{children}</main>
          <JobDrawerMount />
        </div>
      </JobsProvider>
    </ProfileFlowProvider>
  )
}
