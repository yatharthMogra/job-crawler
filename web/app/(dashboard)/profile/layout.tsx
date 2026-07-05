"use client"

import { type ReactNode } from "react"
import { DashboardPageHeader } from "@/components/layout/dashboard-page-header"

export default function ProfileLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-full flex-col">
      <DashboardPageHeader title="Profile" subtitle="Your career command center" />
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  )
}
