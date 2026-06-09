"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Search, SlidersHorizontal } from "lucide-react"
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
    <div className="sticky top-0 z-20 border-b border-zinc-200/80 bg-white/95 backdrop-blur-sm">
      <div className="flex items-center justify-between px-6 py-4">
        <div>
          <h1 className="text-lg font-bold tracking-tight text-zinc-900">Jobs</h1>
          <p className="text-xs text-zinc-500">Discover roles tailored to your profile</p>
        </div>
        <div className="relative w-72">
          <Search className="absolute left-2.5 top-1/2 size-4 -translate-y-1/2 text-zinc-400" />
          <Input
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            placeholder="Search by title or company"
            className="h-8 pl-8 text-sm"
          />
        </div>
      </div>

      <div className="flex items-center gap-6 border-t border-zinc-100 px-6">
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
                "border-b-2 py-3 text-sm font-medium transition-colors",
                active
                  ? "border-zinc-900 text-zinc-900"
                  : "border-transparent text-zinc-500 hover:text-zinc-800",
              )}
            >
              {tab.label}
              {count != null && count > 0 ? ` (${count})` : ""}
            </Link>
          )
        })}
      </div>

      <div className="flex flex-wrap items-center gap-2 border-t border-zinc-100 px-6 py-2.5">
        {activeChips.map((chip) => (
          <FilterChip key={chip.label} label={chip.label} active onRemove={chip.onRemove} />
        ))}
        <Link href="/filters">
          <Button size="sm" variant="outline" className="h-7 gap-1.5 border-zinc-300">
            <SlidersHorizontal className="size-3.5" />
            All Filters
          </Button>
        </Link>
      </div>
    </div>
  )
}
