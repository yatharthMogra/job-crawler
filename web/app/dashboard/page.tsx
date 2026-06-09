"use client"

import { Suspense, useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"

function DashboardRedirect() {
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const candidateId = searchParams.get("candidate_id")
    router.replace(
      candidateId
        ? `/jobs/recommended?candidate_id=${encodeURIComponent(candidateId)}`
        : "/jobs/recommended",
    )
  }, [router, searchParams])

  return (
    <div className="flow-page-bg flex min-h-screen items-center justify-center text-sm text-muted-foreground">
      Redirecting…
    </div>
  )
}

export default function DashboardRedirectPage() {
  return (
    <Suspense
      fallback={
        <div className="flow-page-bg flex min-h-screen items-center justify-center text-sm text-muted-foreground">
          Redirecting…
        </div>
      }
    >
      <DashboardRedirect />
    </Suspense>
  )
}
