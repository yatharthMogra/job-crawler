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
      <div className="flex min-h-screen items-center justify-center bg-zinc-50">
        <p className="text-sm text-red-600">{error}</p>
      </div>
    )
  }

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
