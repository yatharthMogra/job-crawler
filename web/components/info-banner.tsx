"use client"

import { useState } from "react"
import { X } from "lucide-react"

export function InfoBanner() {
  const [open, setOpen] = useState(true)
  if (!open) return null
  return (
    <div className="mx-6 mt-4 flex items-start justify-between gap-3 rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3">
      <p className="text-xs leading-relaxed text-zinc-600">
        Ranked by how well each role matches your profile — skills, experience, and location preferences.
      </p>
      <button
        type="button"
        onClick={() => setOpen(false)}
        aria-label="Dismiss"
        className="shrink-0 rounded-md p-1 text-zinc-400 hover:bg-zinc-200/60 hover:text-zinc-700"
      >
        <X className="size-3.5" />
      </button>
    </div>
  )
}
