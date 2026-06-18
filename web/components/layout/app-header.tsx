"use client"

import Link from "next/link"
import { Bell, Plus, Search } from "lucide-react"
import { useSession } from "@/components/session-provider"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

interface AppHeaderProps {
  title: string
  subtitle?: string
  showSearch?: boolean
  searchPlaceholder?: string
  searchValue?: string
  onSearchChange?: (value: string) => void
  className?: string
  action?: React.ReactNode
}

export function AppHeader({
  title,
  subtitle,
  showSearch = true,
  searchPlaceholder = "Search portal...",
  searchValue,
  onSearchChange,
  className,
  action,
}: AppHeaderProps) {
  const { candidate } = useSession()
  const initials = (candidate?.name ?? "U").charAt(0).toUpperCase()

  return (
    <header
      className={cn(
        "sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b border-border/80 bg-card/95 px-6 backdrop-blur-md",
        className,
      )}
    >
      <div className="min-w-0 shrink-0">
        <h1 className="text-sm font-bold uppercase tracking-widest text-foreground">{title}</h1>
        {subtitle ? <p className="text-xs text-muted-foreground">{subtitle}</p> : null}
      </div>

      {showSearch ? (
        <div className="relative mx-4 hidden max-w-md flex-1 md:block">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={searchValue}
            onChange={(e) => onSearchChange?.(e.target.value)}
            placeholder={searchPlaceholder}
            className="h-9 border-border/80 bg-surface/50 pl-9 text-sm"
          />
        </div>
      ) : (
        <div className="flex-1" />
      )}

      <div className="flex shrink-0 items-center gap-3">
        {action}
        <button
          type="button"
          className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
          aria-label="Notifications"
        >
          <Bell className="size-5" />
        </button>
        <div className="flex size-9 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
          {initials}
        </div>
        {!action ? (
          <Link
            href="/profile/upload"
            className="btn-brand hidden h-8 items-center gap-1 rounded-lg px-3 text-sm font-medium sm:inline-flex"
          >
            <Plus className="size-3.5" />
            EXECUTIVE
          </Link>
        ) : null}
      </div>
    </header>
  )
}
