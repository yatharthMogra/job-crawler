"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { JobScoutWordmark } from "@/components/profile/brand"
import { cn } from "@/lib/utils"

const NAV_LINKS = [
  { href: "/login", label: "Marketplace" },
  { href: "/login", label: "AI Agent" },
  { href: "/login", label: "Trajectory" },
  { href: "/login", label: "Coaching" },
]

export function MarketingNav() {
  const pathname = usePathname()

  return (
    <header className="sticky top-0 z-50 border-b border-border/40 bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2">
          <JobScoutWordmark size="lg" />
        </Link>

        <nav className="hidden items-center gap-8 lg:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.label}
              href={link.href}
              className={cn(
                "text-sm font-medium text-muted-foreground transition-colors hover:text-foreground",
                pathname === link.href && "text-foreground",
              )}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-4">
          <Link
            href="/login"
            className="hidden text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline"
          >
            Sign in
          </Link>
          <Link
            href="/login"
            className="inline-flex h-10 items-center rounded-full bg-primary px-6 text-sm font-semibold text-primary-foreground shadow-md shadow-primary/25 transition-all hover:bg-primary/90 hover:shadow-lg hover:shadow-primary/30"
          >
            Join Elite
          </Link>
        </div>
      </div>
    </header>
  )
}
