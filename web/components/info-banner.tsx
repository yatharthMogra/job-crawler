"use client"

import { useState } from "react"
import { Sparkles, X } from "lucide-react"

export function InfoBanner() {
  const [open, setOpen] = useState(true)
  if (!open) return null
  return (
    <div className="mx-6 mt-4 flex items-start gap-3 rounded-xl border border-primary/15 bg-gradient-to-r from-accent/80 via-brand-muted/40 to-transparent px-4 py-3 shadow-sm">
      <Sparkles className="mt-0.5 size-4 shrink-0 text-primary" />
      <p className="flex-1 text-xs leading-relaxed text-foreground/80">
        Ranked by how well each role matches your profile — skills, experience, and location preferences.
      </p>
      <button
        type="button"
        onClick={() => setOpen(false)}
        aria-label="Dismiss"
        className="shrink-0 rounded-md p-1 text-muted-foreground hover:bg-background/60 hover:text-foreground"
      >
        <X className="size-3.5" />
      </button>
    </div>
  )
}
