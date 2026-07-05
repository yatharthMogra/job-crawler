"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Bell, Search, Settings } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { useSession } from "@/components/session-provider"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import type { ReactNode } from "react"

const TOP_NAV = [
  { href: "/jobs/recommended", label: "Recommended" },
  { href: "/jobs/liked", label: "Saved" },
  { href: "/jobs/applied", label: "My Applications" },
] as const

export function JobsChrome({
  children,
  search,
  onSearchChange,
}: {
  children: ReactNode
  search: string
  onSearchChange: (value: string) => void
}) {
  const pathname = usePathname()
  const { candidate } = useSession()
  const { savedIds, appliedIds } = useJobs()

  const initials = (candidate?.name ?? "U")
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  function tabLabel(item: (typeof TOP_NAV)[number]) {
    if (item.href === "/jobs/liked" && savedIds.size > 0) {
      return `${item.label} (${savedIds.size})`
    }
    if (item.href === "/jobs/applied" && appliedIds.size > 0) {
      return `${item.label} (${appliedIds.size})`
    }
    return item.label
  }

  return (
    <div className="flex min-h-full flex-col">
      <header className="sticky top-0 z-20 border-b border-border/60 bg-card/95 backdrop-blur-md">
        <div className="flex items-center justify-between gap-3 px-4 py-3 lg:px-6">
          <nav className="flex min-w-0 items-center gap-0.5 overflow-x-auto">
            {TOP_NAV.map((item) => {
              const active = pathname === item.href || pathname.startsWith(`${item.href}/`)
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "relative shrink-0 whitespace-nowrap px-3 py-2 text-sm font-medium transition-colors",
                    active ? "text-primary" : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  {tabLabel(item)}
                  {active ? (
                    <span className="absolute inset-x-2 -bottom-px h-0.5 rounded-full bg-primary" />
                  ) : null}
                </Link>
              )
            })}
          </nav>

          <div className="relative mx-4 hidden min-w-0 flex-1 max-w-sm lg:block">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={search}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Search roles or companies..."
              className="h-9 w-full border-border/60 bg-surface/50 pl-9 text-sm"
            />
          </div>

          <div className="flex shrink-0 items-center gap-1">
            <button
              type="button"
              disabled
              title="Notifications coming soon"
              className="cursor-not-allowed rounded-lg p-2 text-muted-foreground/50"
              aria-label="Notifications coming soon"
            >
              <Bell className="size-4" />
            </button>
            <Link
              href="/settings"
              className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              aria-label="Settings"
            >
              <Settings className="size-4" />
            </Link>
            <Link
              href="/profile"
              className="flex items-center gap-2 rounded-full py-1 pl-1 pr-3 transition-colors hover:bg-muted/60"
              aria-label="Open profile"
            >
              <span className="flex size-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                {initials}
              </span>
              <span className="hidden max-w-[140px] truncate text-sm font-medium text-foreground md:inline">
                {candidate?.name ?? "Profile"}
              </span>
            </Link>
          </div>
        </div>
      </header>

      <div className="min-h-0 flex-1">{children}</div>
    </div>
  )
}
