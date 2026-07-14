"use client"

import { Suspense } from "react"
import { SettingsPage } from "@/components/settings/settings-page"

export default function SettingsRoute() {
  return (
    <Suspense fallback={<div className="p-6 text-sm text-muted-foreground">Loading settings…</div>}>
      <SettingsPage />
    </Suspense>
  )
}
