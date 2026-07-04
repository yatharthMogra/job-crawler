"use client"

import { createContext, useContext, useState } from "react"
import { ApplyFollowUpMount } from "@/components/jobs/apply-follow-up-mount"
import { JobsChrome } from "@/components/jobs/jobs-chrome"

const JobsSearchContext = createContext<{ search: string }>({ search: "" })

export function useJobsSearch() {
  return useContext(JobsSearchContext)
}

export default function JobsLayout({ children }: { children: React.ReactNode }) {
  const [search, setSearch] = useState("")

  return (
    <JobsChrome search={search} onSearchChange={setSearch}>
      <JobsSearchContext.Provider value={{ search }}>
        {children}
        <ApplyFollowUpMount />
      </JobsSearchContext.Provider>
    </JobsChrome>
  )
}
