"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
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
} from "@/lib/profile/job-filters"
import { patchJobFilters } from "@/lib/profile/api"
import { useJobs } from "@/components/jobs-provider"
import { FeedSkeleton } from "@/components/card-skeleton"

export default function FiltersPage() {
  const router = useRouter()
  const { candidateId } = useSession()
  const mockMode = useMockData()
  const { rawProfile, profileHome, loadProfileHome } = useProfileFlow()
  const { refreshRecommendedJobs } = useJobs()
  const [state, setState] = useState<ReturnType<typeof emptyJobFilters> | null>(null)
  const [saving, setSaving] = useState(false)
  const [hydrated, setHydrated] = useState(false)

  useEffect(() => {
    if (candidateId && !rawProfile) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, rawProfile, loadProfileHome])

  useEffect(() => {
    if (hydrated) return
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

    setState(
      buildDefaultFiltersState(base, profileHome?.primaryRoles ?? base.primaryRoles),
    )
    setHydrated(true)
  }, [rawProfile, profileHome, hydrated])

  async function handleConfirm() {
    if (!candidateId || !state) return
    setSaving(true)
    try {
      const payload = jobFiltersToApiPayload(state)
      if (mockMode) {
        router.push("/jobs/recommended")
        return
      }
      await patchJobFilters(candidateId, payload)
      router.push("/jobs/recommended")
      void refreshRecommendedJobs()
      void loadProfileHome(candidateId).catch(() => undefined)
    } finally {
      setSaving(false)
    }
  }

  function handleReset() {
    const base = emptyJobFilters()
    setState(
      buildDefaultFiltersState(base, profileHome?.primaryRoles ?? []),
    )
  }

  if (!state) {
    return (
      <div className="px-6 py-8">
        <FeedSkeleton count={4} />
      </div>
    )
  }

  return (
    <div className="min-h-full bg-muted/30">
      <FiltersCommandPage
        state={state}
        onChange={setState}
        onReset={handleReset}
      />
      <div className="sticky bottom-0 border-t border-border/60 bg-background/95 px-5 py-4 backdrop-blur">
        <button
          type="button"
          onClick={() => void handleConfirm()}
          disabled={saving}
          className="btn-brand w-full rounded-xl py-3 text-sm font-bold disabled:opacity-60"
        >
          {saving ? "Saving…" : "Confirm filters"}
        </button>
      </div>
    </div>
  )
}
