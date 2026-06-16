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
    // Don't block local/mock sessions while NextAuth is still resolving.
    if (nextAuthStatus === "loading" && !hasLocalSession) return

    void (async () => {
      try {
        await refreshCandidate()
      } finally {
        setLoading(false)
      }
    })()
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
