"use client"

import { useEffect } from "react"
import { ReviewScreen } from "@/components/profile/screens/review-screen"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"

export default function ReviewPage() {
  const { candidateId } = useSession()
  const { reviewState, setReviewState, saveReview, skipReview, saving, loadPendingReview } =
    useProfileFlow()

  useEffect(() => {
    if (candidateId) {
      void loadPendingReview(candidateId).catch(() => undefined)
    }
  }, [candidateId, loadPendingReview])

  return (
    <ReviewScreen
      state={reviewState}
      setState={setReviewState}
      onSave={saveReview}
      onSkip={skipReview}
      saving={saving}
    />
  )
}
