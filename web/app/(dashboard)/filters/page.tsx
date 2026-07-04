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
import { patchConstraints, patchPreferences } from "@/lib/profile/api"
import { useJobs } from "@/components/jobs-provider"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import { FeedSkeleton } from "@/components/card-skeleton"

export default function FiltersPage() {
  const router = useRouter()
  const { candidateId, candidate } = useSession()
  const mockMode = useMockData()
  const { rawProfile, profileHome, loadProfileHome } = useProfileFlow()
  const { refreshJobs } = useJobs()
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
      await patchConstraints(candidateId, payload.constraints)
      await patchPreferences(candidateId, payload.preferences)
      await loadProfileHome(candidateId)
      await syncSubscriptionsForCandidate(candidateId)
      await refreshJobs()
      router.push("/jobs/recommended")
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
    <FiltersCommandPage
      state={state}
      candidateName={candidate?.name ?? profileHome?.candidateName ?? "you"}
      saving={saving}
      onChange={setState}
      onReset={handleReset}
      onConfirm={() => void handleConfirm()}
    />
  )
}
