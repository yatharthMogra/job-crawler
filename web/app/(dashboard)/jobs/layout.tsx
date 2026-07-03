"use client"

import { createContext, useContext, useState } from "react"
import { usePathname } from "next/navigation"
import { ApplyFollowUpMount } from "@/components/jobs/apply-follow-up-mount"
import { JobsHeader } from "@/components/jobs/jobs-header"
import { RecommendationFilters } from "@/components/jobs/recommendation-filters"

const JobsSearchContext = createContext<{ search: string }>({ search: "" })

export function useJobsSearch() {
  return useContext(JobsSearchContext)
}

export default function JobsLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const [search, setSearch] = useState("")
  const isNeuralFeed = pathname === "/jobs/recommended"

  return (
    <div>
      {!isNeuralFeed ? (
        <>
          <JobsHeader search={search} onSearchChange={setSearch} />
          <RecommendationFilters />
        </>
      ) : null}
      <JobsSearchContext.Provider value={{ search }}>
        {children}
        <ApplyFollowUpMount />
      </JobsSearchContext.Provider>
    </div>
  )
}
