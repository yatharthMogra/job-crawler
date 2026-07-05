"use client"

import Link from "next/link"
import { Bell, Settings } from "lucide-react"
import { useSession } from "@/components/session-provider"
import { cn } from "@/lib/utils"

export function DashboardPageHeader({
  title,
  subtitle,
  className,
}: {
  title?: string
  subtitle?: string
  className?: string
}) {
  const { candidate } = useSession()
  const initials = (candidate?.name ?? "U")
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  return (
    <header
      className={cn(
        "sticky top-0 z-20 border-b border-border/60 bg-card/95 backdrop-blur-md",
        className,
      )}
    >
      <div className="flex items-center justify-between gap-4 px-4 py-3 lg:px-6">
        {title ? (
          <div className="min-w-0">
            <h1 className="truncate text-sm font-bold text-foreground">{title}</h1>
            {subtitle ? (
              <p className="truncate text-xs text-muted-foreground">{subtitle}</p>
            ) : null}
          </div>
        ) : (
          <div />
        )}

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
            className="flex items-center gap-2 rounded-full py-1 pl-1 pr-3 transition-colors hover:bg-muted/60"
            aria-label="Open profile"
          >
            <span className="flex size-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
              {initials}
            </span>
            <span className="hidden max-w-[140px] truncate text-sm font-medium text-foreground sm:inline">
              {candidate?.name ?? "Profile"}
            </span>
          </Link>
        </div>
      </div>
    </header>
  )
}
