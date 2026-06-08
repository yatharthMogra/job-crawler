"use client"

import { usePathname } from "next/navigation"
import { JobDrawer } from "@/components/job-drawer"

export function JobDrawerMount() {
  const pathname = usePathname()
  const showMatch = pathname === "/recommended"
  return <JobDrawer showMatch={showMatch} />
}
