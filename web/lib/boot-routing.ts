import { ApiError, getCandidate, getPendingPatch, getProfile } from "@/lib/profile/api"
import { getStoredCandidateId, useMockData } from "@/lib/session"

export type BootDestination =
  | "/onboarding"
  | "/profile/upload"
  | "/profile/review"
  | "/jobs/recommended"

export async function resolveBootDestination(): Promise<BootDestination> {
  const candidateId = getStoredCandidateId()
  if (!candidateId) {
    return "/onboarding"
  }

  if (useMockData()) {
    return "/profile/upload"
  }

  try {
    await getCandidate(candidateId)
  } catch {
    return "/onboarding"
  }

  try {
    await getPendingPatch(candidateId)
    return "/profile/review"
  } catch (err) {
    if (!(err instanceof ApiError && err.status === 404)) {
      throw err
    }
  }

  try {
    await getProfile(candidateId)
    return "/jobs/recommended"
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) {
      return "/profile/upload"
    }
    throw err
  }
}
