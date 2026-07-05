"use client"

import { useEffect, useMemo, useState } from "react"
import { X } from "lucide-react"
import {
  FiltersCommandPage,
  buildDefaultFiltersState,
} from "@/components/filters/filters-command-page"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { useMockData } from "@/lib/session"
import {
  emptyJobFilters,
  profileToJobFilters,
  jobFiltersToApiPayload,
  type JobFiltersState,
} from "@/lib/profile/job-filters"
import { patchConstraints, patchPreferences } from "@/lib/profile/api"
import { useJobs } from "@/components/jobs-provider"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import { FeedSkeleton } from "@/components/card-skeleton"
import { cn } from "@/lib/utils"

export function RecommendationsFilterPanel({
  open,
  onClose,
  onApplied,
}: {
  open: boolean
  onClose: () => void
  onApplied: (state: JobFiltersState) => void
}) {
  const { candidateId, candidate } = useSession()
  const mockMode = useMockData()
  const { rawProfile, profileHome, loadProfileHome } = useProfileFlow()
  const { refreshJobs } = useJobs()
  const [state, setState] = useState<JobFiltersState | null>(null)
  const [saving, setSaving] = useState(false)
  const [hydrated, setHydrated] = useState(false)

  useEffect(() => {
    if (!open) return
    if (candidateId && !rawProfile) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [open, candidateId, rawProfile, loadProfileHome])

  useEffect(() => {
    if (!open || hydrated) return
    const base = rawProfile
      ? profileToJobFilters(rawProfile)
      : profileHome
        ? {
            ...emptyJobFilters(),
            primaryRoles: profileHome.primaryRoles,
            secondaryRoles: profileHome.secondaryRoles,
            eeo: profileHome.eeo,
          }
        : emptyJobFilters()

    setState(buildDefaultFiltersState(base, profileHome?.primaryRoles ?? base.primaryRoles))
    setHydrated(true)
  }, [open, rawProfile, profileHome, hydrated])

  useEffect(() => {
    if (!open) {
      setHydrated(false)
      setState(null)
    }
  }, [open])

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose()
    }
    document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [open, onClose])

  const summary = useMemo(() => {
    if (!state) return ""
    const roles = state.primaryRoles.slice(0, 2).join(", ")
    const extra = state.primaryRoles.length > 2 ? ` +${state.primaryRoles.length - 2}` : ""
    const location = state.preferredLocations[0] ?? "United States"
    return `${roles || "Any role"}${extra}, ${location}`
  }, [state])

  async function handleConfirm() {
    if (!candidateId || !state) return
    setSaving(true)
    try {
      if (!mockMode) {
        const payload = jobFiltersToApiPayload(state)
        await patchConstraints(candidateId, payload.constraints)
        await patchPreferences(candidateId, payload.preferences)
        await loadProfileHome(candidateId)
        await syncSubscriptionsForCandidate(candidateId)
        await refreshJobs()
      }
      onApplied(state)
      onClose()
    } finally {
      setSaving(false)
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-stretch justify-end">
      <button
        type="button"
        className="absolute inset-0 bg-foreground/20 backdrop-blur-[2px]"
        aria-label="Close filters"
        onClick={onClose}
      />
      <div
        className={cn(
          "relative flex h-full w-full max-w-4xl flex-col border-l border-border/80 bg-background shadow-2xl",
          "animate-in slide-in-from-right duration-300",
        )}
      >
        <div className="flex shrink-0 items-center justify-between gap-4 border-b border-border/60 px-5 py-3">
          <div className="min-w-0">
            <p className="text-sm font-semibold text-foreground">Filters</p>
            <p className="truncate text-xs text-muted-foreground">{summary}</p>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => void handleConfirm()}
              disabled={saving || !state}
              className="btn-brand rounded-lg px-4 py-2 text-sm font-bold disabled:opacity-60"
            >
              {saving ? "Saving…" : "Confirm"}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
              aria-label="Close"
            >
              <X className="size-5" />
            </button>
          </div>
        </div>

        <div className="min-h-0 flex-1 overflow-y-auto">
          {!state ? (
            <div className="px-6 py-8">
              <FeedSkeleton count={4} />
            </div>
          ) : (
            <FiltersCommandPage
              state={state}
              candidateName={candidate?.name ?? profileHome?.candidateName ?? "you"}
              saving={saving}
              onChange={setState}
              onReset={() =>
                setState(
                  buildDefaultFiltersState(
                    emptyJobFilters(),
                    profileHome?.primaryRoles ?? [],
                  ),
                )
              }
              onConfirm={() => void handleConfirm()}
            />
          )}
        </div>
      </div>
    </div>
  )
}
