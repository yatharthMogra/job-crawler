"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Search, SlidersHorizontal, Sparkles } from "lucide-react"
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

export function JobsHeader({ search, onSearchChange }: JobsHeaderProps) {
  const pathname = usePathname()
  const { savedIds, appliedIds, filters, clearFilter } = useJobs()

  const activeChips: { label: string; onRemove: () => void }[] = []
  if (filters.role) activeChips.push({ label: filters.role, onRemove: () => clearFilter("role") })
  if (filters.location)
    activeChips.push({ label: filters.location, onRemove: () => clearFilter("location") })
  if (filters.remote)
    activeChips.push({ label: filters.remote, onRemove: () => clearFilter("remote") })
  if (filters.datePosted)
    activeChips.push({ label: filters.datePosted, onRemove: () => clearFilter("datePosted") })

  return (
    <div className="sticky top-0 z-20 border-b border-border/80 bg-card/90 backdrop-blur-md">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <span className="flex size-9 items-center justify-center rounded-xl bg-accent text-primary">
            <Sparkles className="size-4" />
          </span>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-foreground">Jobs</h1>
            <p className="text-xs text-muted-foreground">Roles matched to your profile</p>
          </div>
        </div>
        <div className="relative w-72">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search by title or company"
            className="h-9 border-border/80 bg-surface/50 pl-9 text-sm focus-visible:ring-primary/30"
          />
        </div>
      </div>

      <div className="flex items-center gap-1 border-t border-border/60 px-4">
        {TABS.map((tab) => {
          const active = pathname === tab.href || pathname.startsWith(tab.href + "/")
          const count =
            tab.label === "Liked"
              ? savedIds.size
              : tab.label === "Applied"
                ? appliedIds.size
                : null
          return (
            <Link
              key={tab.href}
              href={tab.href}
              className={cn(
                "relative px-4 py-3 text-sm font-medium transition-colors",
                active ? "text-primary" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {tab.label}
              {count != null && count > 0 ? (
                <span className="ml-1 text-xs text-muted-foreground">({count})</span>
              ) : null}
              {active ? (
                <span className="absolute inset-x-2 bottom-0 h-0.5 rounded-full bg-gradient-to-r from-primary to-brand" />
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
      </div>
    </div>
  )
}
