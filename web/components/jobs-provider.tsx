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
  clearPendingApply,
  getPendingApply,
  loadAppliedIds,
  loadApplicationStatuses,
  loadHiddenIds,
  loadSavedIds,
  persistAppliedIds,
  persistApplicationStatus,
  persistHiddenIds,
  persistSavedIds,
  setPendingApply,
  type PendingApply,
} from "@/lib/job-storage"
import {
  fetchApplications,
  fetchDashboardJobs,
  fetchRecommendedJobs,
  applyToJob,
  patchApplication,
} from "@/lib/recommendation/api"
import { mapApplicationToUi } from "@/lib/recommendation/map-application"
import { mapApiJobToUi, mapRecommendedApiJob } from "@/lib/recommendation/map-job"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import {
  appendJobFeedback,
  type NotInterestedReason,
  type ReportIssueReason,
} from "@/lib/job-feedback"
import { useMockData } from "@/lib/session"
import { ALL_JOBS } from "@/lib/jobs-data"
import {
  toApiStatus,
  type ApplicationPipelineStatus,
} from "@/lib/applications/pipeline-status"

import type { EmploymentTypeFilter } from "@/lib/employment-type-filter"
import type { SeniorityLevel } from "@/lib/jobs-data"
import { DEFAULT_LOCATION } from "@/lib/job-filters"

export interface Filters {
  role: string | null
  location: string | null
  remote: string | null
  salaryMin: number | null
  datePosted: string | null
  employmentType: EmploymentTypeFilter
  experienceLevel: SeniorityLevel | "any" | null
}

const EMPTY_FILTERS: Filters = {
  role: null,
  location: DEFAULT_LOCATION,
  remote: null,
  salaryMin: null,
  datePosted: null,
  employmentType: null,
  experienceLevel: null,
}

interface JobsContextValue {
  jobs: JobWithRole[]
  recommendedJobs: JobWithRole[]
  allKnownJobs: JobWithRole[]
  savedIds: Set<string>
  appliedIds: Set<string>
  appliedJobs: JobWithRole[]
  hiddenIds: Set<string>
  filters: Filters
  selectedJobId: string | null
  loading: boolean
  recommendedLoading: boolean
  error: string | null
  hasProfile: boolean
  pendingApply: PendingApply | null
  toggleSave: (id: string) => void
  markApplied: (id: string) => void
  unmarkApplied: (id: string) => void
  updateApplicationStatus: (jobId: string, status: ApplicationPipelineStatus) => void
  startApply: (job: JobWithRole) => void
  resolvePendingApply: (applied: boolean) => void
  hideJob: (id: string) => void
  submitNotInterested: (id: string, reason: NotInterestedReason) => void
  submitReportIssue: (id: string, reason: ReportIssueReason) => void
  setFilter: (key: keyof Filters, value: Filters[keyof Filters]) => void
  clearFilter: (key: keyof Filters) => void
  setEmploymentTypeFilter: (value: EmploymentTypeFilter) => void
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
  const [appliedJobs, setAppliedJobs] = useState<JobWithRole[]>([])
  const [hiddenIds, setHiddenIds] = useState<Set<string>>(new Set())
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS)
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [recommendedLoading, setRecommendedLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [hasProfile, setHasProfile] = useState(true)
  const [pendingApply, setPendingApplyState] = useState<PendingApply | null>(null)

  const refreshJobs = useCallback(async () => {
    if (!candidateId) {
      setAllJobs([])
      setRecommendedJobs([])
      setLoading(false)
      setRecommendedLoading(false)
      return
    }

    setSavedIds(loadSavedIds(candidateId))
    setHiddenIds(loadHiddenIds(candidateId))
    setPendingApplyState(getPendingApply(candidateId))

    if (mockMode) {
      const mockApplied = loadAppliedIds(candidateId)
      const mockStatuses = loadApplicationStatuses(candidateId)
      setAppliedIds(mockApplied)
      setAllJobs(ALL_JOBS as JobWithRole[])
      setRecommendedJobs(
        [...(ALL_JOBS as JobWithRole[])].sort((a, b) => b.personal_score - a.personal_score),
      )
      setAppliedJobs(
        (ALL_JOBS as JobWithRole[])
          .filter((job) => mockApplied.has(job.id))
          .map((job) => ({
            ...job,
            is_applied: true,
            application_status: mockStatuses[job.id] ?? "applied",
          })),
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

      const [dashboard, recommended, applications] = await Promise.all([
        fetchDashboardJobs(candidateId, query),
        fetchRecommendedJobs(candidateId, { limit: 200 }),
        fetchApplications(candidateId).catch(() => ({ applications: [], total: 0 })),
      ])

      setAllJobs(dashboard.jobs.map((j) => mapApiJobToUi(j)))
      setRecommendedJobs(recommended.jobs.map((j) => mapRecommendedApiJob(j)))
      const serverApplied = applications.applications.map((app) => mapApplicationToUi(app))
      setAppliedJobs(serverApplied)

      const appliedIdSet = new Set<string>()
      for (const app of applications.applications) {
        if (app.normalized_job_id) appliedIdSet.add(app.normalized_job_id)
      }
      const legacyApplied = loadAppliedIds(candidateId)
      if (appliedIdSet.size === 0 && legacyApplied.size > 0) {
        for (const jobId of legacyApplied) {
          try {
            const created = await applyToJob(candidateId, jobId)
            if (created.normalized_job_id) appliedIdSet.add(created.normalized_job_id)
            else appliedIdSet.add(jobId)
          } catch {
            appliedIdSet.add(jobId)
          }
        }
        persistAppliedIds(candidateId, new Set())
        const refreshed = await fetchApplications(candidateId).catch(() => ({
          applications: [],
          total: 0,
        }))
        setAppliedJobs(refreshed.applications.map((app) => mapApplicationToUi(app)))
      }
      setAppliedIds(appliedIdSet)
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

      if (mockMode) {
        setAppliedIds((prev) => {
          const next = new Set(prev)
          next.add(id)
          persistAppliedIds(candidateId, next)
          return next
        })
        setAppliedJobs((prev) => {
          if (prev.some((job) => job.id === id)) return prev
          const fromCatalog =
            (ALL_JOBS as JobWithRole[]).find((job) => job.id === id) ??
            allJobs.find((job) => job.id === id) ??
            recommendedJobs.find((job) => job.id === id)
          if (!fromCatalog) return prev
          return [{ ...fromCatalog, is_applied: true, application_status: "applied" }, ...prev]
        })
        clearPendingApply(candidateId)
        setPendingApplyState(null)
        return
      }
      void (async () => {
        try {
          const application = await applyToJob(candidateId, id)
          const appliedJob = mapApplicationToUi(application)
          setAppliedJobs((prev) => {
            const withoutDup = prev.filter(
              (job) =>
                job.id !== id &&
                job.id !== application.id &&
                job.id !== (application.normalized_job_id ?? ""),
            )
            return [appliedJob, ...withoutDup]
          })
          setAppliedIds((prev) => {
            const next = new Set(prev)
            next.add(application.normalized_job_id ?? id)
            return next
          })
        } catch {
          setAppliedIds((prev) => {
            const next = new Set(prev)
            next.add(id)
            return next
          })
        } finally {
          clearPendingApply(candidateId)
          setPendingApplyState(null)
        }
      })()
    },
    [candidateId, mockMode, allJobs, recommendedJobs],
  )

  const unmarkApplied = useCallback(
    (id: string) => {
      if (!candidateId) return
      setAppliedIds((prev) => {
        const next = new Set(prev)
        next.delete(id)
        persistAppliedIds(candidateId, next)
        return next
      })
      setAppliedJobs((prev) => prev.filter((job) => job.id !== id))
      setSelectedJobId((current) => (current === id ? null : current))
    },
    [candidateId],
  )

  const updateApplicationStatus = useCallback(
    (jobId: string, status: ApplicationPipelineStatus) => {
      if (!candidateId) return
      const apiStatus = toApiStatus(status)

      if (mockMode) {
        persistApplicationStatus(candidateId, jobId, apiStatus)
      }

      setAppliedJobs((prev) => {
        const existing =
          prev.find((job) => job.id === jobId) ??
          allJobs.find((job) => job.id === jobId) ??
          recommendedJobs.find((job) => job.id === jobId)
        if (!existing) return prev

        const updatedJob = {
          ...existing,
          is_applied: true,
          application_status: apiStatus,
        }
        const withoutDup = prev.filter((job) => job.id !== jobId)
        const next = [updatedJob, ...withoutDup]

        if (!mockMode) {
          const applicationId = existing.application_id
          if (applicationId) {
            void patchApplication(candidateId, applicationId, { status: apiStatus })
              .then((updated) => {
                const mapped = mapApplicationToUi(updated)
                setAppliedJobs((current) => {
                  const rest = current.filter((job) => job.id !== jobId)
                  return [mapped, ...rest]
                })
              })
              .catch(() => undefined)
          }
        }

        return next
      })
    },
    [candidateId, mockMode, allJobs, recommendedJobs],
  )

  const startApply = useCallback(
    (job: JobWithRole) => {
      if (!candidateId) return
      const pending: PendingApply = {
        jobId: job.id,
        jobTitle: job.title,
        company: job.company,
        startedAt: new Date().toISOString(),
      }
      setPendingApply(candidateId, pending)
      setPendingApplyState(pending)
    },
    [candidateId],
  )

  const resolvePendingApply = useCallback(
    (applied: boolean) => {
      if (!candidateId || !pendingApply) return
      if (applied) {
        markApplied(pendingApply.jobId)
        return
      }
      clearPendingApply(candidateId)
      setPendingApplyState(null)
    },
    [candidateId, pendingApply, markApplied],
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

  const submitNotInterested = useCallback(
    (id: string, reason: NotInterestedReason) => {
      if (!candidateId) return
      appendJobFeedback(candidateId, { jobId: id, type: "not_interested", reason })
      hideJob(id)
    },
    [candidateId, hideJob],
  )

  const submitReportIssue = useCallback(
    (id: string, reason: ReportIssueReason) => {
      if (!candidateId) return
      appendJobFeedback(candidateId, { jobId: id, type: "report_issue", reason })
      hideJob(id)
    },
    [candidateId, hideJob],
  )

  const setFilter = useCallback((key: keyof Filters, value: Filters[keyof Filters]) => {
    setFilters((prev) => ({ ...prev, [key]: value }))
  }, [])

  const clearFilter = useCallback((key: keyof Filters) => {
    setFilters((prev) => ({
      ...prev,
      [key]: key === "location" ? DEFAULT_LOCATION : null,
    }))
  }, [])

  const setEmploymentTypeFilter = useCallback((value: EmploymentTypeFilter) => {
    setFilters((prev) => ({ ...prev, employmentType: value }))
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
      appliedJobs,
      hiddenIds,
      filters,
      selectedJobId,
      loading,
      recommendedLoading,
      error,
      hasProfile,
      pendingApply,
      toggleSave,
      markApplied,
      unmarkApplied,
      updateApplicationStatus,
      startApply,
      resolvePendingApply,
      hideJob,
      submitNotInterested,
      submitReportIssue,
      setFilter,
      clearFilter,
      setEmploymentTypeFilter,
      selectJob: setSelectedJobId,
      refreshJobs,
    }),
    [
      jobs,
      recommendedWithFlags,
      allKnownJobs,
      savedIds,
      appliedIds,
      appliedJobs,
      hiddenIds,
      filters,
      selectedJobId,
      loading,
      recommendedLoading,
      error,
      hasProfile,
      pendingApply,
      toggleSave,
      markApplied,
      unmarkApplied,
      updateApplicationStatus,
      startApply,
      resolvePendingApply,
      hideJob,
      submitNotInterested,
      submitReportIssue,
      setFilter,
      clearFilter,
      setEmploymentTypeFilter,
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
