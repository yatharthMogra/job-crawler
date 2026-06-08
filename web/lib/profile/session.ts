const CANDIDATE_ID_KEY = "profile_candidate_id"

export function getStoredCandidateId(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem(CANDIDATE_ID_KEY)
}

export function setStoredCandidateId(id: string): void {
  localStorage.setItem(CANDIDATE_ID_KEY, id)
}

export function clearStoredCandidateId(): void {
  localStorage.removeItem(CANDIDATE_ID_KEY)
}

export function useMockData(): boolean {
  return process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true"
}
