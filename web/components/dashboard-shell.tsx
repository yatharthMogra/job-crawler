"use client"

import { useEffect, type ReactNode } from "react"
import { useRouter } from "next/navigation"
import { JobsProvider } from "@/components/jobs-provider"
import { JobDrawerMount } from "@/components/job-drawer-mount"
import { ProfileFlowProvider } from "@/components/profile/profile-flow-provider"
import { Sidebar } from "@/components/sidebar"
import { useSession } from "@/components/session-provider"

export function DashboardShell({ children }: { children: ReactNode }) {
  const router = useRouter()
  const { candidateId, loading } = useSession()

  useEffect(() => {
    if (!loading && !candidateId) {
      router.replace("/onboarding")
    }
  }, [loading, candidateId, router])

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

  return (
    <ProfileFlowProvider candidateId={candidateId}>
      <JobsProvider>
        <div className="min-h-screen bg-[#f8f9fa]">
          <Sidebar />
          <main className="ml-[72px] min-h-screen sm:ml-[88px]">{children}</main>
          <JobDrawerMount />
        </div>
      </JobsProvider>
    </ProfileFlowProvider>
  )
}
