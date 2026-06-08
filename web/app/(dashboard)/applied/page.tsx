"use client"

import { Check } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"

export default function AppliedPage() {
  const { allKnownJobs, appliedIds, hiddenIds } = useJobs()
  const applied = allKnownJobs.filter((j) => appliedIds.has(j.id) && !hiddenIds.has(j.id))

  return (
    <div>
      <div className="sticky top-0 z-20 border-b border-zinc-200 bg-zinc-50/90 px-6 py-3 backdrop-blur">
        <h1 className="text-sm font-semibold text-zinc-900">Applied</h1>
        <p className="text-xs text-zinc-400">
          {applied.length.toLocaleString()} {applied.length === 1 ? "application" : "applications"}
        </p>
      </div>
      {applied.length === 0 ? (
        <EmptyState
          icon={Check}
          title="No applications tracked yet."
          description="After applying, mark a job as Applied to track it here."
        />
      ) : (
        <JobFeed jobs={applied} />
      )}
    </div>
  )
}
