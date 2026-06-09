"use client"

import { Suspense, useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import Link from "next/link"
import { fetchSubscriptions, patchSubscriptions } from "@/lib/recommendation/api"

function UnsubscribeContent() {
  const searchParams = useSearchParams()
  const candidateId = searchParams.get("candidate_id")
  const [status, setStatus] = useState<"loading" | "done" | "error" | "invalid">("loading")
  const [message, setMessage] = useState("")

  useEffect(() => {
    if (!candidateId) {
      setStatus("invalid")
      return
    }

    void (async () => {
      try {
        const { subscriptions } = await fetchSubscriptions(candidateId)
        const poolNames = subscriptions.map((s) => s.pool_name)
        if (poolNames.length === 0) {
          setMessage("You are not subscribed to job alerts.")
          setStatus("done")
          return
        }
        if (!subscriptions.some((s) => s.is_active)) {
          setMessage("You are already unsubscribed from daily job briefing emails.")
          setStatus("done")
          return
        }
        await patchSubscriptions(candidateId, poolNames, false)
        setMessage("You have been unsubscribed from daily job briefing emails.")
        setStatus("done")
      } catch {
        setStatus("error")
      }
    })()
  }, [candidateId])

  return (
    <div className="flow-page-bg flex min-h-screen items-center justify-center px-6">
      <div className="w-full max-w-md rounded-xl border border-border bg-card p-8 text-center shadow-sm">
        <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">Career Match AI</p>
        <h1 className="mb-4 text-xl font-semibold text-foreground">Email preferences</h1>
        {status === "loading" && <p className="text-sm text-muted-foreground">Updating your preferences…</p>}
        {status === "invalid" && (
          <p className="text-sm text-muted-foreground">This unsubscribe link is invalid or missing a user id.</p>
        )}
        {status === "error" && (
          <p className="text-sm text-destructive">
            Something went wrong. Please try again or contact support.
          </p>
        )}
        {status === "done" && <p className="text-sm text-muted-foreground">{message}</p>}
        <Link href="/" className="mt-6 inline-block text-sm text-brand hover:underline">
          Back to Career Match AI
        </Link>
      </div>
    </div>
  )
}

export default function UnsubscribePage() {
  return (
    <Suspense
      fallback={
        <div className="flow-page-bg flex min-h-screen items-center justify-center text-sm text-muted-foreground">
          Loading…
        </div>
      }
    >
      <UnsubscribeContent />
    </Suspense>
  )
}
