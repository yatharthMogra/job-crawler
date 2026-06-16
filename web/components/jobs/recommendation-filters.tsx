"use client"

import { useEffect } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Sparkles } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { useJobs } from "@/components/jobs-provider"
import { FilterChip } from "@/components/ui/filter-chip"
import { REMOTE_LABEL } from "@/lib/job-meta"

export function RecommendationFilters() {
  const pathname = usePathname()
  const { candidateId } = useSession()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const { filters, clearFilter } = useJobs()

  const onRecommended =
    pathname === "/jobs/recommended" || pathname.startsWith("/jobs/recommended/")

  useEffect(() => {
    if (onRecommended && candidateId && !profileHome) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [onRecommended, candidateId, profileHome, loadProfileHome])

  if (!onRecommended) return null

  const roleChips: string[] = []
  if (profileHome) {
    roleChips.push(...profileHome.primaryRoles, ...profileHome.secondaryRoles)
  }

  const prefChips: string[] = []
  if (profileHome) {
    const remotePref = profileHome.preferences.find((p) => p.label === "Remote")?.value
    const locations = profileHome.preferences.find((p) => p.label === "Locations")?.value
    if (remotePref && remotePref !== "—" && remotePref !== "Flexible") {
      prefChips.push(
        remotePref in REMOTE_LABEL
          ? REMOTE_LABEL[remotePref as keyof typeof REMOTE_LABEL]
          : remotePref,
      )
    }
    if (locations && locations !== "—") {
      locations.split(",").forEach((loc) => {
        const trimmed = loc.trim()
        if (trimmed) prefChips.push(trimmed)
      })
    }
  }

  const queryChips: { label: string; onRemove?: () => void }[] = []
  if (filters.role) queryChips.push({ label: filters.role, onRemove: () => clearFilter("role") })
  if (filters.location)
    queryChips.push({ label: filters.location, onRemove: () => clearFilter("location") })
  if (filters.remote)
    queryChips.push({
      label: filters.remote in REMOTE_LABEL ? REMOTE_LABEL[filters.remote as keyof typeof REMOTE_LABEL] : filters.remote,
      onRemove: () => clearFilter("remote"),
    })
  if (filters.datePosted)
    queryChips.push({ label: filters.datePosted, onRemove: () => clearFilter("datePosted") })

  const hasCriteria = roleChips.length > 0 || prefChips.length > 0 || queryChips.length > 0

  if (!hasCriteria && !profileHome) return null

  return (
    <div className="border-b border-border/60 bg-surface/40 px-6 py-3">
      <div className="flex flex-wrap items-center gap-2">
        <span className="mr-1 inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          <Sparkles className="size-3.5 text-primary" />
          Matching
        </span>

        {roleChips.length > 0 ? (
          <>
            {roleChips.map((role) => (
              <FilterChip key={`role-${role}`} label={role} active />
            ))}
          </>
        ) : (
          <Link href="/profile/job-intent">
            <FilterChip label="Set target roles" className="border-dashed" />
          </Link>
        )}

        {prefChips.map((chip) => (
          <FilterChip key={`pref-${chip}`} label={chip} active />
        ))}

        {queryChips.map((chip) => (
          <FilterChip key={`query-${chip.label}`} label={chip.label} active onRemove={chip.onRemove} />
        ))}

        {!hasCriteria ? (
          <Link
            href="/filters"
            className="text-xs font-medium text-primary underline-offset-2 hover:underline"
          >
            Configure filters →
          </Link>
        ) : (
          <Link
            href="/filters"
            className="ml-1 text-xs text-muted-foreground underline-offset-2 hover:text-foreground hover:underline"
          >
            Edit
          </Link>
        )}
      </div>
    </div>
  )
}
