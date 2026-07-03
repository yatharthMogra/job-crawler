"use client"

import { JobIntentScreen } from "@/components/profile/screens/job-intent-screen"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"

export default function JobIntentPage() {
  const { jobIntent, setJobIntent, saveJobIntent, saving } = useProfileFlow()

  return (
    <JobIntentScreen
      state={jobIntent}
      onChange={setJobIntent}
      onSubmit={() => saveJobIntent("jobs")}
      saving={saving}
    />
  )
}
