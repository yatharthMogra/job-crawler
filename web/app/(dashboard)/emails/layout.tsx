"use client"

import { type ReactNode } from "react"
import { DashboardPageHeader } from "@/components/layout/dashboard-page-header"

export default function EmailsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-full flex-col">
      <DashboardPageHeader
        title="Emails"
        subtitle="Company watch alerts and personalized digests"
      />
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  )
}
