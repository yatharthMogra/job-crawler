"use client"

import { Bookmark } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { JobFeed } from "@/components/job-feed"
import { EmptyState } from "@/components/empty-state"

export default function SavedPage() {
  const { allKnownJobs, savedIds, hiddenIds } = useJobs()
  const saved = allKnownJobs.filter((j) => savedIds.has(j.id) && !hiddenIds.has(j.id))

  return (
    <div>
      <div className="sticky top-0 z-20 border-b border-zinc-200 bg-zinc-50/90 px-6 py-3 backdrop-blur">
        <h1 className="text-sm font-semibold text-zinc-900">Saved</h1>
        <p className="text-xs text-zinc-400">
          {saved.length.toLocaleString()} {saved.length === 1 ? "job" : "jobs"}
        </p>
      </div>
      {saved.length === 0 ? (
        <EmptyState
          icon={Bookmark}
          title="No saved jobs yet."
          description="Browse All Jobs and save roles you want to revisit."
          ctaLabel="Browse All Jobs →"
          ctaHref="/jobs"
        />
      ) : (
        <JobFeed jobs={saved} />
      )}
    </div>
  )
}
