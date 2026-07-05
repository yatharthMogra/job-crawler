"use client"

import { type ReactNode } from "react"
import { DashboardPageHeader } from "@/components/layout/dashboard-page-header"

export default function ResumeLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-full flex-col">
      <DashboardPageHeader title="Resume" subtitle="General and company-specific versions" />
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  )
}
