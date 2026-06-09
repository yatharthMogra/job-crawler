const CANDIDATE_ID_KEY = "profile_candidate_id"
const MOCK_NAME_KEY = "profile_mock_name"
const MOCK_EMAIL_KEY = "profile_mock_email"

export const MOCK_CANDIDATE_ID = "00000000-0000-4000-8000-000000000001"

export function getStoredCandidateId(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem(CANDIDATE_ID_KEY)
}

export function setStoredCandidateId(id: string): void {
  localStorage.setItem(CANDIDATE_ID_KEY, id)
}

export function clearStoredCandidateId(): void {
  localStorage.removeItem(CANDIDATE_ID_KEY)
  localStorage.removeItem(MOCK_NAME_KEY)
  localStorage.removeItem(MOCK_EMAIL_KEY)
}

export function setMockCandidateInfo(name: string, email: string): void {
  localStorage.setItem(MOCK_NAME_KEY, name)
  localStorage.setItem(MOCK_EMAIL_KEY, email)
}

export function getMockCandidateInfo(): { name: string; email: string } {
  return {
    name: localStorage.getItem(MOCK_NAME_KEY) ?? "Alex Rivera",
    email: localStorage.getItem(MOCK_EMAIL_KEY) ?? "alex.rivera@example.com",
  }
}

export function useMockData(): boolean {
  return process.env.NEXT_PUBLIC_USE_MOCK_DATA === "true"
}
