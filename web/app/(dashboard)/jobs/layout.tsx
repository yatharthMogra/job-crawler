"use client"

import { createContext, useContext, useState } from "react"
import { ApplyFollowUpMount } from "@/components/jobs/apply-follow-up-mount"
import { JobsHeader } from "@/components/jobs/jobs-header"
import { RecommendationFilters } from "@/components/jobs/recommendation-filters"

const JobsSearchContext = createContext<{ search: string }>({ search: "" })

export function useJobsSearch() {
  return useContext(JobsSearchContext)
}

export default function JobsLayout({ children }: { children: React.ReactNode }) {
  const [search, setSearch] = useState("")

  return (
    <div>
      <JobsHeader search={search} onSearchChange={setSearch} />
      <RecommendationFilters />
      <JobsSearchContext.Provider value={{ search }}>
        {children}
        <ApplyFollowUpMount />
      </JobsSearchContext.Provider>
    </div>
  )
}
