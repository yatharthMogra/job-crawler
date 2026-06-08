"use client"

import { useState } from "react"
import type { PreferenceSuggestion } from "@/lib/profile/profile-data"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Check, Lightbulb, Pencil, X } from "lucide-react"

interface PreferencesSectionProps {
  preferences: PreferenceSuggestion[]
  onDecision: (id: string, status: PreferenceSuggestion["status"], value?: string) => void
}

export function PreferencesSection({ preferences, onDecision }: PreferencesSectionProps) {
  return (
    <div>
      <div className="mb-4 border-b border-border pb-3">
        <h3 className="text-lg font-semibold text-foreground">Preferences &amp; Constraints</h3>
      </div>

      <div className="mb-5 flex items-start gap-2 rounded-xl border border-update/40 bg-update-muted/40 p-3 text-sm text-update-foreground">
        <Lightbulb className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
        <p>
          We made some guesses based on your resume. These are yours to define — please review
          carefully.
        </p>
      </div>

      <div className="space-y-3">
        {preferences.map((pref) => (
          <PreferenceRow key={pref.id} pref={pref} onDecision={onDecision} />
        ))}
      </div>
    </div>
  )
}

function PreferenceRow({
  pref,
  onDecision,
}: {
  pref: PreferenceSuggestion
  onDecision: (id: string, status: PreferenceSuggestion["status"], value?: string) => void
}) {
  const [editing, setEditing] = useState(false)
  const [value, setValue] = useState(pref.value)

  return (
    <div
      className={cn(
        "rounded-xl border p-4 transition-colors",
        pref.status === "confirmed"
          ? "border-add/40 bg-add-muted/20"
          : pref.status === "declined"
            ? "border-border bg-secondary/40 opacity-70"
            : "border-border bg-card",
      )}
    >
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <h4 className="text-sm font-semibold text-foreground">{pref.label}</h4>
          {pref.kind === "input" && pref.status === "pending" ? null : (
            <p className="mt-0.5 text-sm text-muted-foreground">
              {pref.detected ? (
                <>
                  Suggested:{" "}
                  <span className="font-medium text-foreground">
                    {pref.status === "confirmed" ? value || pref.value : pref.suggestion}
                  </span>
                </>
              ) : (
                <span>{pref.suggestion}</span>
              )}
              {pref.detail ? (
                <span className="text-muted-foreground"> ({pref.detail})</span>
              ) : null}
            </p>
          )}
        </div>

        {pref.status === "confirmed" ? (
          <button
            type="button"
            onClick={() => onDecision(pref.id, "pending")}
            className="inline-flex items-center gap-1 rounded-md bg-add-muted px-2.5 py-1 text-xs font-medium text-add-foreground"
          >
            <Check className="size-3.5" aria-hidden="true" /> Confirmed
          </button>
        ) : pref.status === "declined" ? (
          <button
            type="button"
            onClick={() => onDecision(pref.id, "pending")}
            className="inline-flex items-center gap-1 rounded-md bg-secondary px-2.5 py-1 text-xs font-medium text-muted-foreground"
          >
            <X className="size-3.5" aria-hidden="true" /> Declined
          </button>
        ) : null}
      </div>

      {pref.status === "pending" ? (
        editing || pref.kind === "input" ? (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <Input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder={pref.kind === "input" ? "$ per hour" : pref.label}
              className="max-w-xs"
            />
            <Button
              size="sm"
              onClick={() => {
                onDecision(pref.id, "confirmed", value)
                setEditing(false)
              }}
            >
              {pref.kind === "input" ? "Set" : "Save"}
            </Button>
            {editing ? (
              <Button size="sm" variant="ghost" onClick={() => setEditing(false)}>
                Cancel
              </Button>
            ) : null}
          </div>
        ) : (
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={() => onDecision(pref.id, "confirmed", pref.value)}
              className="inline-flex h-8 items-center gap-1 rounded-md border border-add/40 bg-add-muted/60 px-3 text-sm font-medium text-add-foreground hover:bg-add-muted"
            >
              <Check className="size-3.5" aria-hidden="true" /> Confirm
            </button>
            <button
              type="button"
              onClick={() => onDecision(pref.id, "declined")}
              className="inline-flex h-8 items-center gap-1 rounded-md border border-border bg-card px-3 text-sm font-medium text-muted-foreground hover:bg-secondary hover:text-foreground"
            >
              <X className="size-3.5" aria-hidden="true" /> Decline
            </button>
            <button
              type="button"
              onClick={() => setEditing(true)}
              className="inline-flex h-8 items-center gap-1 rounded-md border border-border bg-card px-3 text-sm font-medium text-muted-foreground hover:bg-secondary hover:text-foreground"
            >
              <Pencil className="size-3.5" aria-hidden="true" /> Change
            </button>
          </div>
        )
      ) : null}
    </div>
  )
}
