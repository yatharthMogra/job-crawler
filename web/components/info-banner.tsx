"use client"

import { useState } from "react"
import { Sparkles, X } from "lucide-react"

export function InfoBanner() {
  const [open, setOpen] = useState(true)
  if (!open) return null
  return (
    <div className="mx-6 mt-4 flex items-start gap-3 rounded-xl border-l-4 border-l-primary bg-accent/40 px-4 py-3">
      <Sparkles className="mt-0.5 size-4 shrink-0 text-primary" />
      <p className="flex-1 text-sm leading-relaxed text-foreground/80">
        Your profile is currently ranking in the <strong>top 5%</strong> for Strategic Leadership
        roles.{" "}
        <button type="button" className="font-medium text-primary underline-offset-2 hover:underline">
          View Details
        </button>
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
