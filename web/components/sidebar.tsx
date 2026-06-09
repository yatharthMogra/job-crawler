"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Briefcase, FileText, Settings, User } from "lucide-react"
import { BrandMark } from "@/components/profile/brand"
import { useSession } from "@/components/session-provider"
import { cn } from "@/lib/utils"

const NAV = [
  { href: "/jobs/recommended", label: "Jobs", icon: Briefcase, match: "/jobs" },
  { href: "/resume", label: "Resume", icon: FileText, match: "/resume" },
  { href: "/profile", label: "Profile", icon: User, match: "/profile" },
  { href: "/settings", label: "Settings", icon: Settings, match: "/settings" },
]

function NavRow({
  href,
  label,
  icon: Icon,
  active,
}: {
  href: string
  label: string
  icon: typeof Briefcase
  active: boolean
}) {
  return (
    <Link
      href={href}
      className={cn(
        "group relative flex flex-col items-center gap-1 rounded-xl px-3 py-2.5 text-xs transition-all",
        active
          ? "bg-accent font-medium text-accent-foreground shadow-sm"
          : "text-muted-foreground hover:bg-muted/80 hover:text-foreground",
      )}
    >
      {active ? (
        <span className="absolute -left-0.5 top-1/2 h-6 w-1 -translate-y-1/2 rounded-full bg-gradient-to-b from-primary to-brand" />
      ) : null}
      <Icon
        className={cn("size-5 shrink-0", active && "text-primary")}
        strokeWidth={active ? 2.5 : 2}
      />
      {label}
    </Link>
  )
}

export function Sidebar() {
  const pathname = usePathname()
  const { candidate } = useSession()

  return (
    <aside className="fixed inset-y-0 left-0 z-30 flex w-[72px] flex-col border-r border-sidebar-border bg-sidebar/95 backdrop-blur-md sm:w-[88px]">
      <div className="flex h-16 items-center justify-center">
        <BrandMark />
      </div>

      <nav className="flex flex-1 flex-col items-center gap-1 px-2 py-2">
        {NAV.map((item) => (
          <NavRow
            key={item.href}
            {...item}
            active={pathname.startsWith(item.match)}
          />
        ))}
      </nav>

      <div className="border-t border-sidebar-border px-2 py-4 text-center">
        <div className="mx-auto flex size-9 items-center justify-center rounded-full bg-gradient-to-br from-primary/15 to-brand/20 text-xs font-semibold text-primary">
          {(candidate?.name ?? "U").charAt(0).toUpperCase()}
        </div>
      </div>
    </aside>
  )
}
