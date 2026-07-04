"use client"

import { useEffect } from "react"
import { usePathname } from "next/navigation"
import { useJobs } from "@/components/jobs-provider"

function isJobFeedRoute(pathname: string) {
  return (
    pathname === "/jobs/recommended" ||
    pathname.startsWith("/jobs/recommended/") ||
    pathname === "/jobs/liked" ||
    pathname.startsWith("/jobs/liked/") ||
    pathname === "/jobs/applied" ||
    pathname.startsWith("/jobs/applied/") ||
    pathname === "/recommended"
  )
}

/** Clears stale job selection when leaving job feeds. Detail panels are in-page only. */
export function JobDrawerMount() {
  const pathname = usePathname()
  const { selectedJobId, selectJob } = useJobs()

  useEffect(() => {
    if (!isJobFeedRoute(pathname) && selectedJobId) {
      selectJob(null)
    }
  }, [pathname, selectedJobId, selectJob])

  return null
}
