"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { ChevronRight, Search, SlidersHorizontal } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { FilterChip } from "@/components/ui/filter-chip"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const TABS = [
  { href: "/jobs/recommended", label: "Recommended" },
  { href: "/jobs/liked", label: "Liked" },
  { href: "/jobs/applied", label: "Applied" },
  { href: "/jobs/all", label: "All Jobs" },
]

interface JobsHeaderProps {
  search: string
  onSearchChange: (value: string) => void
}

function tabLabel(pathname: string) {
  const tab = TABS.find((t) => pathname === t.href || pathname.startsWith(t.href + "/"))
  return tab?.label ?? "Jobs"
}

export function JobsHeader({ search, onSearchChange }: JobsHeaderProps) {
  const pathname = usePathname()
  const { savedIds, appliedIds, appliedJobs, filters, clearFilter } = useJobs()

  const activeChips: { label: string; onRemove: () => void }[] = []
  if (filters.role) activeChips.push({ label: filters.role, onRemove: () => clearFilter("role") })
  if (filters.location)
    activeChips.push({ label: filters.location, onRemove: () => clearFilter("location") })
  if (filters.remote)
    activeChips.push({ label: filters.remote, onRemove: () => clearFilter("remote") })
  if (filters.datePosted)
    activeChips.push({ label: filters.datePosted, onRemove: () => clearFilter("datePosted") })

  const currentTab = tabLabel(pathname)

  return (
    <div className="sticky top-0 z-20 border-b border-border/80 bg-card/95 backdrop-blur-md">
      <div className="flex items-center justify-between gap-4 px-6 py-4">
        <div className="flex items-center gap-2 text-sm">
          <span className="font-bold uppercase tracking-widest text-muted-foreground">Jobs</span>
          <ChevronRight className="size-4 text-muted-foreground" />
          <span className="font-bold uppercase tracking-widest text-foreground">{currentTab}</span>
        </div>
        <div className="relative hidden w-80 md:block">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search by title or company"
            className="h-9 border-border/80 bg-surface/50 pl-9 text-sm"
          />
        </div>
      </div>

      <div className="flex items-center gap-1 overflow-x-auto border-t border-border/60 px-4">
        {TABS.map((tab) => {
          const active = pathname === tab.href || pathname.startsWith(tab.href + "/")
          const count =
            tab.label === "Liked"
              ? savedIds.size
              : tab.label === "Applied"
                ? appliedJobs.length || appliedIds.size
                : null
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                "relative shrink-0 px-4 py-3 text-sm font-medium transition-colors",
                active ? "text-primary" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {tab.label}
              {count != null && count > 0 ? (
                <span className="ml-1 text-xs text-muted-foreground">({count})</span>
              ) : null}
              {active ? (
                <span className="absolute inset-x-2 bottom-0 h-0.5 rounded-full bg-primary" />
              ) : null}
            </Link>
          )
        })}
      </div>

      <div className="flex flex-wrap items-center gap-2 border-t border-border/60 px-6 py-2.5">
        {activeChips.map((chip) => (
          <FilterChip key={chip.label} label={chip.label} active onRemove={chip.onRemove} />
        ))}
        <Link href="/filters">
          <Button size="sm" className="btn-brand h-8 gap-1.5">
            <SlidersHorizontal className="size-3.5" />
            All Filters
          </Button>
        </Link>
        <Button size="sm" variant="outline" className="h-8 border-add/40 text-add-foreground">
          Hidden Jobs
        </Button>
      </div>
    </div>
  )
}
