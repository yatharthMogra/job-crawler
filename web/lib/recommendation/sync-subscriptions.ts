import { getProfile } from "@/lib/profile/api"
import { createSubscriptions, fetchSubscriptions, patchSubscriptions } from "@/lib/recommendation/api"
import { derivePoolNames } from "@/lib/recommendation/pools"

export async function syncSubscriptionsForCandidate(candidateId: string): Promise<string[]> {
  const profile = await getProfile(candidateId)
  const poolNames = derivePoolNames(profile)

  try {
    const existing = await fetchSubscriptions(candidateId)
    if (existing.length > 0) {
      await patchSubscriptions(candidateId, poolNames, true)
    } else {
      await createSubscriptions(candidateId, poolNames)
    }
  } catch {
    await createSubscriptions(candidateId, poolNames)
  }

  return poolNames
}
