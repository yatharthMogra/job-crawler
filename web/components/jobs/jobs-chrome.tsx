"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Bell, Search, Settings } from "lucide-react"
import { NeuralJobsSidebar } from "@/components/jobs/neural-jobs-sidebar"
import { useSession } from "@/components/session-provider"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import type { ReactNode } from "react"

const TOP_NAV = [
  { href: "/jobs/recommended", label: "Recommended Jobs" },
  { href: "/jobs/applied", label: "My Applications" },
]

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
  const hideJobsSidebar =
    pathname === "/jobs/applied" ||
    pathname.startsWith("/jobs/applied/") ||
    pathname === "/jobs/liked" ||
    pathname.startsWith("/jobs/liked/")
  const initials = (candidate?.name ?? "U")
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <div className="flex min-h-full flex-col">
      <header className="sticky top-0 z-20 border-b border-border/60 bg-card/95 backdrop-blur-md">
        <div className="flex items-center justify-between gap-4 px-4 py-3 lg:px-6">
          <nav className="hidden items-center gap-1 md:flex">
            {TOP_NAV.map((item) => {
              const active = pathname === item.href || pathname.startsWith(`${item.href}/`)
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "relative px-3 py-2 text-sm font-medium transition-colors",
                    active ? "text-primary" : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  {item.label}
                  {active ? (
                    <span className="absolute inset-x-2 -bottom-px h-0.5 rounded-full bg-primary" />
                  ) : null}
                </Link>
              )
            })}
          </nav>

          <div className="relative mx-auto hidden w-full max-w-sm lg:block">
            <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              value={search}
              onChange={(e) => onSearchChange(e.target.value)}
              placeholder="Search roles or companies..."
              className="h-9 border-border/60 bg-surface/50 pl-9 text-sm"
            />
          </div>

          <div className="flex items-center gap-1">
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
              className="flex size-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground transition-opacity hover:opacity-90"
              aria-label="Open profile"
            >
              {initials}
            </Link>
          </div>
        </div>
      </header>

      <div className="flex min-h-0 flex-1">
        {!hideJobsSidebar ? <NeuralJobsSidebar /> : null}
        <div className="min-w-0 flex-1">{children}</div>
      </div>
    </div>
  )
}
