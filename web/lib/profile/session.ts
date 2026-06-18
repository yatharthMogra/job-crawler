const CANDIDATE_ID_KEY = "profile_candidate_id"
const CANDIDATE_COOKIE = "candidate_id"
const MOCK_NAME_KEY = "profile_mock_name"
const MOCK_EMAIL_KEY = "profile_mock_email"
const MOCK_ONBOARDING_COMPLETE_KEY = "mock_onboarding_complete"
const MOCK_ONBOARDING_COOKIE = "mock_onboarding_complete"

export const MOCK_CANDIDATE_ID = "00000000-0000-4000-8000-000000000001"

const COOKIE_MAX_AGE = 60 * 60 * 24 * 30

function setCandidateCookie(id: string) {
  if (typeof document === "undefined") return
  document.cookie = `${CANDIDATE_COOKIE}=${encodeURIComponent(id)}; path=/; max-age=${COOKIE_MAX_AGE}; SameSite=Lax`
}

function clearCandidateCookie() {
  if (typeof document === "undefined") return
  document.cookie = `${CANDIDATE_COOKIE}=; path=/; max-age=0; SameSite=Lax`
}

export function getStoredCandidateId(): string | null {
  if (typeof window === "undefined") return null
  return localStorage.getItem(CANDIDATE_ID_KEY)
}

export function setStoredCandidateId(id: string): void {
  localStorage.setItem(CANDIDATE_ID_KEY, id)
  setCandidateCookie(id)
}

export function clearStoredCandidateId(): void {
  localStorage.removeItem(CANDIDATE_ID_KEY)
  localStorage.removeItem(MOCK_NAME_KEY)
  localStorage.removeItem(MOCK_EMAIL_KEY)
  localStorage.removeItem(MOCK_ONBOARDING_COMPLETE_KEY)
  clearCandidateCookie()
  if (typeof document !== "undefined") {
    document.cookie = `${MOCK_ONBOARDING_COOKIE}=; path=/; max-age=0; SameSite=Lax`
  }
}

export function setMockOnboardingComplete(complete = true): void {
  if (typeof window === "undefined") return
  if (complete) {
    localStorage.setItem(MOCK_ONBOARDING_COMPLETE_KEY, "true")
    document.cookie = `${MOCK_ONBOARDING_COOKIE}=true; path=/; max-age=${COOKIE_MAX_AGE}; SameSite=Lax`
  } else {
    localStorage.removeItem(MOCK_ONBOARDING_COMPLETE_KEY)
    document.cookie = `${MOCK_ONBOARDING_COOKIE}=; path=/; max-age=0; SameSite=Lax`
  }
}

export function getMockOnboardingComplete(): boolean {
  if (typeof window === "undefined") return false
  return localStorage.getItem(MOCK_ONBOARDING_COMPLETE_KEY) === "true"
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
