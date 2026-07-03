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
import { useSession as useNextAuthSession } from "next-auth/react"
import { getCandidate } from "@/lib/profile/api"
import {
  getMockCandidateInfo,
  getStoredCandidateId,
  MOCK_CANDIDATE_ID,
  setStoredCandidateId,
  useMockData,
} from "@/lib/session"

interface CandidateInfo {
  id: string
  name: string
  email: string
}

interface SessionContextValue {
  candidateId: string | null
  candidate: CandidateInfo | null
  loading: boolean
  setCandidateId: (id: string) => void
  refreshCandidate: () => Promise<void>
}

const SessionContext = createContext<SessionContextValue | null>(null)

export function SessionProvider({ children }: { children: ReactNode }) {
  const { data: nextAuthSession, status: nextAuthStatus } = useNextAuthSession()
  const [candidateId, setCandidateIdState] = useState<string | null>(() => {
    if (typeof window === "undefined") return null
    return getStoredCandidateId()
  })
  const [candidate, setCandidate] = useState<CandidateInfo | null>(null)
  const [loading, setLoading] = useState(true)

  const mockMode = useMockData()
  const hasLocalSession = Boolean(getStoredCandidateId())

  const refreshCandidate = useCallback(async () => {
    const authCandidateId = nextAuthSession?.candidateId
    const storedId = authCandidateId ?? getStoredCandidateId()
    setCandidateIdState(storedId)

    if (authCandidateId && authCandidateId !== getStoredCandidateId()) {
      setStoredCandidateId(authCandidateId)
    }

    if (!storedId) {
      setCandidate(null)
      return
    }
    if (mockMode && storedId === MOCK_CANDIDATE_ID) {
      const info = getMockCandidateInfo()
      setCandidate({ id: MOCK_CANDIDATE_ID, name: info.name, email: info.email })
      return
    }
    try {
      const data = await getCandidate(storedId)
      setCandidate({ id: data.id, name: data.name, email: data.email })
    } catch {
      setCandidate(null)
    }
  }, [mockMode, nextAuthSession?.candidateId])

  useEffect(() => {
    let cancelled = false

    const finishLoading = () => {
      if (!cancelled) setLoading(false)
    }

    // Never block the UI longer than 3s (NextAuth or API can hang offline).
    const safetyTimer = window.setTimeout(finishLoading, 3000)

    const run = async () => {
      if (nextAuthStatus === "loading" && !hasLocalSession) return

      try {
        await Promise.race([
          refreshCandidate(),
          new Promise<void>((_, reject) =>
            window.setTimeout(() => reject(new Error("session refresh timeout")), 5000),
          ),
        ])
      } catch {
        // Offline / slow API — still allow UI to render with stored session.
      } finally {
        window.clearTimeout(safetyTimer)
        finishLoading()
      }
    }

    void run()

    return () => {
      cancelled = true
      window.clearTimeout(safetyTimer)
    }
  }, [refreshCandidate, nextAuthStatus, hasLocalSession])

  const setCandidateId = useCallback(
    (id: string) => {
      setStoredCandidateId(id)
      setCandidateIdState(id)
      void refreshCandidate()
    },
    [refreshCandidate],
  )

  const value = useMemo(
    () => ({
      candidateId,
      candidate,
      loading,
      setCandidateId,
      refreshCandidate,
    }),
    [candidateId, candidate, loading, setCandidateId, refreshCandidate],
  )

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
}

export function useSession() {
  const ctx = useContext(SessionContext)
  if (!ctx) throw new Error("useSession must be used within SessionProvider")
  return ctx
}
