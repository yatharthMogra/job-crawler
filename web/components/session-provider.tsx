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
  const [candidateId, setCandidateIdState] = useState<string | null>(null)
  const [candidate, setCandidate] = useState<CandidateInfo | null>(null)
  const [loading, setLoading] = useState(true)

  const mockMode = useMockData()

  const refreshCandidate = useCallback(async () => {
    const id = getStoredCandidateId()
    setCandidateIdState(id)
    if (!id) {
      setCandidate(null)
      return
    }
    if (mockMode && id === MOCK_CANDIDATE_ID) {
      const info = getMockCandidateInfo()
      setCandidate({ id: MOCK_CANDIDATE_ID, name: info.name, email: info.email })
      return
    }
    try {
      const data = await getCandidate(id)
      setCandidate({ id: data.id, name: data.name, email: data.email })
    } catch {
      setCandidate(null)
    }
  }, [mockMode])

  useEffect(() => {
    void (async () => {
      try {
        await refreshCandidate()
      } finally {
        setLoading(false)
      }
    })()
  }, [refreshCandidate])

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
