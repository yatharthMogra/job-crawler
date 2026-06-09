"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { resolveBootDestination } from "@/lib/boot-routing"

export function BootRedirect() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    void (async () => {
      try {
        const dest = await resolveBootDestination()
        router.replace(dest)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load session")
      }
    })()
  }, [router])

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
        <span className="size-1.5 animate-bounce rounded-full bg-brand/50 [animation-delay:-0.15s]" />
        <span className="size-1.5 animate-bounce rounded-full bg-primary/40" />
      </div>
    </div>
  )
}
