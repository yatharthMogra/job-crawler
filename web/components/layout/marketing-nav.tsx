"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Bell, Zap } from "lucide-react"
import { BrandWordmark } from "@/components/profile/brand"
import { cn } from "@/lib/utils"

const NAV_LINKS = [
  { href: "/login", label: "Jobs" },
  { href: "/login", label: "AI Agent" },
  { href: "/login", label: "Resume" },
  { href: "/login", label: "Coaching" },
]

export function MarketingNav() {
  const pathname = usePathname()

  return (
    <header className="sticky top-0 z-50 border-b border-border/60 bg-card/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2">
          <BrandWordmark size="lg" />
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.label}
              href={link.href}
              className={cn(
                "text-sm font-medium tracking-wide text-muted-foreground transition-colors hover:text-foreground",
                pathname === link.href && "text-foreground underline decoration-primary decoration-2 underline-offset-4",
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <button
            type="button"
            className="hidden rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground sm:block"
            aria-label="Notifications"
          >
            <Bell className="size-5" />
          </button>
          <button
            type="button"
            className="hidden rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground sm:block"
            aria-label="Pro features"
          >
            <Zap className="size-5" />
          </button>
          <Link
            href="/login"
            className="btn-brand inline-flex h-9 items-center rounded-lg px-5 text-sm font-semibold"
          >
            JOIN NOW
          </Link>
        </div>
      </div>
    </header>
  )
}
