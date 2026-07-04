"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import {
  Bookmark,
  Briefcase,
  LogOut,
  Settings2,
  User,
} from "lucide-react"
import { signOut } from "next-auth/react"
import { BrandWordmark } from "@/components/profile/brand"
import { useSession } from "@/components/session-provider"
import { clearStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

const NAV = [
  { href: "/jobs/recommended", label: "Feed", icon: Briefcase },
  { href: "/jobs/liked", label: "Saved", icon: Bookmark },
  { href: "/profile", label: "Profile", icon: User },
  { href: "/filters", label: "Filters", icon: Settings2 },
] as const

function isNavActive(pathname: string, href: string): boolean {
  if (href === "/jobs/recommended") {
    return (
      pathname === "/jobs" ||
      pathname === "/jobs/recommended" ||
      pathname.startsWith("/jobs/recommended/")
    )
  }
  return pathname === href || pathname.startsWith(`${href}/`)
}

function NavItem({
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
        "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
        active
          ? "bg-primary text-primary-foreground shadow-md shadow-primary/25"
          : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground",
      )}
    >
      <Icon className="size-5 shrink-0" strokeWidth={active ? 2.5 : 2} />
      {label}
    </Link>
  )
}

export function AppSidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { candidate } = useSession()

  async function handleLogout() {
    clearStoredCandidateId()
    await signOut({ callbackUrl: "/login" })
    router.push("/login")
  }

  return (
    <aside className="dashboard-shell-sidebar sticky top-0 z-30 flex h-screen flex-col">
      <div className="flex h-16 items-center px-5">
        <Link href="/jobs/recommended">
          <BrandWordmark />
        </Link>
      </div>

      <nav className="flex flex-1 flex-col gap-1 px-3 py-2">
        {NAV.map((item) => (
          <NavItem
            key={item.href}
            {...item}
            active={isNavActive(pathname, item.href)}
          />
        ))}
      </nav>

      <div className="border-t border-sidebar-border p-4">
        <div className="mb-3 rounded-xl border border-sidebar-border bg-sidebar-accent/30 p-3">
          <div className="flex items-center gap-3">
            <div className="flex size-10 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
              {(candidate?.name ?? "U")
                .split(" ")
                .map((n) => n[0])
                .join("")
                .slice(0, 2)
                .toUpperCase()}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-semibold text-sidebar-foreground">
                {candidate?.name ?? "Guest"}
              </p>
              <p className="truncate text-[10px] font-bold uppercase tracking-widest text-sidebar-foreground/50">
                Executive
              </p>
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-0.5">
          <button
            type="button"
            onClick={() => void handleLogout()}
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
          >
            <LogOut className="size-4" />
            Log out
          </button>
        </div>
      </div>
    </aside>
  )
}
