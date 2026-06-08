"use client"

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react"
import { useSession } from "@/components/session-provider"
import type { JobWithRole } from "@/lib/jobs-data"
import {
  loadAppliedIds,
  loadHiddenIds,
  loadSavedIds,
  persistAppliedIds,
  persistHiddenIds,
  persistSavedIds,
} from "@/lib/job-storage"
import { fetchDashboardJobs, fetchRecommendedJobs } from "@/lib/recommendation/api"
import { mapApiJobToUi, mapRecommendedApiJob } from "@/lib/recommendation/map-job"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import { useMockData } from "@/lib/session"
import { ALL_JOBS } from "@/lib/jobs-data"

export interface Filters {
  role: string | null
  location: string | null
  remote: string | null
  salaryMin: number | null
  datePosted: string | null
}

const EMPTY_FILTERS: Filters = {
  role: null,
  location: null,
  remote: null,
  salaryMin: null,
  datePosted: null,
}

interface JobsContextValue {
  jobs: JobWithRole[]
  recommendedJobs: JobWithRole[]
  allKnownJobs: JobWithRole[]
  savedIds: Set<string>
  appliedIds: Set<string>
  hiddenIds: Set<string>
  filters: Filters
  selectedJobId: string | null
  loading: boolean
  recommendedLoading: boolean
  error: string | null
  hasProfile: boolean
  toggleSave: (id: string) => void
  markApplied: (id: string) => void
  hideJob: (id: string) => void
  setFilter: (key: keyof Filters, value: Filters[keyof Filters]) => void
  clearFilter: (key: keyof Filters) => void
  selectJob: (id: string | null) => void
  refreshJobs: () => Promise<void>
}

const JobsContext = createContext<JobsContextValue | null>(null)

export function JobsProvider({ children }: { children: ReactNode }) {
  const { candidateId } = useSession()
  const mockMode = useMockData()

  const [allJobs, setAllJobs] = useState<JobWithRole[]>([])
  const [recommendedJobs, setRecommendedJobs] = useState<JobWithRole[]>([])
  const [savedIds, setSavedIds] = useState<Set<string>>(new Set())
  const [appliedIds, setAppliedIds] = useState<Set<string>>(new Set())
  const [hiddenIds, setHiddenIds] = useState<Set<string>>(new Set())
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS)
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [recommendedLoading, setRecommendedLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [hasProfile, setHasProfile] = useState(true)

  const refreshJobs = useCallback(async () => {
    if (!candidateId) {
      setAllJobs([])
      setRecommendedJobs([])
      setLoading(false)
      setRecommendedLoading(false)
      return
    }

    setSavedIds(loadSavedIds(candidateId))
    setAppliedIds(loadAppliedIds(candidateId))
    setHiddenIds(loadHiddenIds(candidateId))

    if (mockMode) {
      setAllJobs(ALL_JOBS as JobWithRole[])
      setRecommendedJobs(
        [...(ALL_JOBS as JobWithRole[])].sort((a, b) => b.personal_score - a.personal_score),
      )
      setLoading(false)
      setRecommendedLoading(false)
      setHasProfile(true)
      return
    }

    setLoading(true)
    setRecommendedLoading(true)
    setError(null)

    try {
      await syncSubscriptionsForCandidate(candidateId).catch(() => undefined)

      const query: Record<string, string | number | undefined> = { limit: 200 }
      if (filters.location) query.location = filters.location
      if (filters.remote) query.remote_type = filters.remote
      if (filters.salaryMin) query.salary_min = filters.salaryMin
      if (filters.role) query.role_type = "FULLTIME"

      const [dashboard, recommended] = await Promise.all([
        fetchDashboardJobs(candidateId, query),
        fetchRecommendedJobs(candidateId, { limit: 200 }),
      ])

      setAllJobs(dashboard.jobs.map((j) => mapApiJobToUi(j)))
      setRecommendedJobs(recommended.jobs.map((j) => mapRecommendedApiJob(j)))
      setHasProfile(recommended.total > 0 || dashboard.total > 0)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load jobs")
      setAllJobs([])
      setRecommendedJobs([])
    } finally {
      setLoading(false)
      setRecommendedLoading(false)
    }
  }, [candidateId, mockMode, filters.location, filters.remote, filters.salaryMin, filters.role])

  useEffect(() => {
    void refreshJobs()
  }, [refreshJobs])

  const toggleSave = useCallback(
    (id: string) => {
      if (!candidateId) return
      setSavedIds((prev) => {
        const next = new Set(prev)
        if (next.has(id)) next.delete(id)
        else next.add(id)
        persistSavedIds(candidateId, next)
        return next
      })
    },
    [candidateId],
  )

  const markApplied = useCallback(
    (id: string) => {
      if (!candidateId) return
      setAppliedIds((prev) => {
        const next = new Set(prev)
        next.add(id)
        persistAppliedIds(candidateId, next)
        return next
      })
    },
    [candidateId],
  )

  const hideJob = useCallback(
    (id: string) => {
      if (!candidateId) return
      setHiddenIds((prev) => {
        const next = new Set(prev)
        next.add(id)
        persistHiddenIds(candidateId, next)
        return next
      })
      setSelectedJobId((cur) => (cur === id ? null : cur))
    },
    [candidateId],
  )

  const setFilter = useCallback((key: keyof Filters, value: Filters[keyof Filters]) => {
    setFilters((prev) => ({ ...prev, [key]: value }))
  }, [])

  const clearFilter = useCallback((key: keyof Filters) => {
    setFilters((prev) => ({ ...prev, [key]: null }))
  }, [])

  const jobs = useMemo<JobWithRole[]>(() => {
    return allJobs.map((j) => ({
      ...j,
      is_saved: savedIds.has(j.id),
      is_applied: appliedIds.has(j.id),
    }))
  }, [allJobs, savedIds, appliedIds])

  const recommendedWithFlags = useMemo<JobWithRole[]>(() => {
    return recommendedJobs.map((j) => ({
      ...j,
      is_saved: savedIds.has(j.id),
      is_applied: appliedIds.has(j.id),
    }))
  }, [recommendedJobs, savedIds, appliedIds])

  const allKnownJobs = useMemo<JobWithRole[]>(() => {
    const byId = new Map<string, JobWithRole>()
    for (const job of jobs) byId.set(job.id, job)
    for (const job of recommendedWithFlags) {
      if (!byId.has(job.id)) byId.set(job.id, job)
    }
    return [...byId.values()]
  }, [jobs, recommendedWithFlags])

  const value = useMemo<JobsContextValue>(
    () => ({
      jobs,
      recommendedJobs: recommendedWithFlags,
      allKnownJobs,
      savedIds,
      appliedIds,
      hiddenIds,
      filters,
      selectedJobId,
      loading,
      recommendedLoading,
      error,
      hasProfile,
      toggleSave,
      markApplied,
      hideJob,
      setFilter,
      clearFilter,
      selectJob: setSelectedJobId,
      refreshJobs,
    }),
    [
      jobs,
      recommendedWithFlags,
      allKnownJobs,
      savedIds,
      appliedIds,
      hiddenIds,
      filters,
      selectedJobId,
      loading,
      recommendedLoading,
      error,
      hasProfile,
      toggleSave,
      markApplied,
      hideJob,
      setFilter,
      clearFilter,
      refreshJobs,
    ],
  )

  return <JobsContext.Provider value={value}>{children}</JobsContext.Provider>
}

export function useJobs() {
  const ctx = useContext(JobsContext)
  if (!ctx) throw new Error("useJobs must be used within JobsProvider")
  return ctx
}
