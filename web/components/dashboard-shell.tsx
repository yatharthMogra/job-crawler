"use client"

import { useEffect, type ReactNode } from "react"
import { usePathname, useRouter } from "next/navigation"
import { JobsProvider } from "@/components/jobs-provider"
import { JobDrawerMount } from "@/components/job-drawer-mount"
import { AppSidebar } from "@/components/layout/app-sidebar"
import { ProfileFlowProvider } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { getStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

function isJobsRoute(pathname: string) {
  return pathname === "/jobs" || pathname.startsWith("/jobs/")
}

function usesAppSidebar(pathname: string) {
  if (!isJobsRoute(pathname)) return true
  return (
    pathname === "/jobs/applied" ||
    pathname.startsWith("/jobs/applied/") ||
    pathname === "/jobs/liked" ||
    pathname.startsWith("/jobs/liked/")
  )
}

export function DashboardShell({ children }: { children: ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()
  const { candidateId, loading } = useSession()
  const resolvedId = candidateId ?? getStoredCandidateId()
  const jobsChrome = isJobsRoute(pathname)
  const showSidebar = usesAppSidebar(pathname)

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
          {!showSidebar ? null : <AppSidebar />}
          <main className={cn("dashboard-shell-main", jobsChrome && !showSidebar && "w-full")}>
            {children}
          </main>
          <JobDrawerMount />
        </div>
      </JobsProvider>
    </ProfileFlowProvider>
  )
}
