"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { Briefcase, FileText, LogOut, Mail } from "lucide-react"
import { signOut } from "next-auth/react"
import { BrandMark } from "@/components/profile/brand"
import { useSession } from "@/components/session-provider"
import { clearStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

const NAV = [
  { href: "/jobs/recommended", label: "Jobs", icon: Briefcase },
  { href: "/resume", label: "Resume", icon: FileText },
  { href: "/emails", label: "Emails", icon: Mail },
] as const

function isNavActive(pathname: string, href: string): boolean {
  if (href === "/jobs/recommended") {
    return pathname === "/jobs" || pathname.startsWith("/jobs/")
  }
  return pathname === href || pathname.startsWith(`${href}/`)
}

export function DashboardSidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { candidate } = useSession()

  const initials = (candidate?.name ?? "U")
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()

  async function handleLogout() {
    clearStoredCandidateId()
    await signOut({ callbackUrl: "/login" })
    router.push("/login")
  }

  return (
    <aside className="sticky top-0 z-30 flex h-screen w-[72px] shrink-0 flex-col border-r border-sidebar-border bg-sidebar">
      <div className="flex h-16 items-center justify-center">
        <Link
          href="/jobs/recommended"
          title="Job Scout"
          className="transition-opacity hover:opacity-80"
        >
          <BrandMark />
        </Link>
      </div>

      <nav className="flex flex-1 flex-col items-center gap-2 px-2 py-2">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = isNavActive(pathname, href)
          return (
            <Link
              key={href}
              href={href}
              title={label}
              className={cn(
                "flex size-11 items-center justify-center rounded-xl transition-all",
                active
                  ? "bg-primary text-primary-foreground shadow-md shadow-primary/25"
                  : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground",
              )}
            >
              <Icon className="size-5 shrink-0" strokeWidth={active ? 2.5 : 2} />
              <span className="sr-only">{label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="flex flex-col items-center gap-2 border-t border-sidebar-border p-3">
        <Link
          href="/profile"
          title={candidate?.name ?? "Profile"}
          className="flex size-10 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground transition-opacity hover:opacity-90"
        >
          {initials}
        </Link>
        <button
          type="button"
          title="Log out"
          onClick={() => void handleLogout()}
          className="flex size-9 items-center justify-center rounded-lg text-sidebar-foreground/60 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
        >
          <LogOut className="size-4" />
          <span className="sr-only">Log out</span>
        </button>
      </div>
    </aside>
  )
}
