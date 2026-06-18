"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import {
  Briefcase,
  FileText,
  HelpCircle,
  LogOut,
  Settings,
  User,
} from "lucide-react"
import { signOut } from "next-auth/react"
import { BrandWordmark } from "@/components/profile/brand"
import { useSession } from "@/components/session-provider"
import { clearStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

const NAV = [
  { href: "/jobs/recommended", label: "Jobs", icon: Briefcase, match: "/jobs" },
  { href: "/resume", label: "Resume", icon: FileText, match: "/resume" },
  { href: "/profile", label: "Profile", icon: User, match: "/profile" },
  { href: "/settings", label: "Settings", icon: Settings, match: "/settings" },
]

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
          ? "bg-accent text-primary shadow-sm"
          : "text-muted-foreground hover:bg-muted/80 hover:text-foreground",
      )}
    >
      <Icon className={cn("size-5 shrink-0", active && "text-primary")} strokeWidth={active ? 2.5 : 2} />
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

  const initials = (candidate?.name ?? "U").charAt(0).toUpperCase()

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
            active={pathname.startsWith(item.match)}
          />
        ))}
      </nav>

      <div className="border-t border-sidebar-border p-4">
        <div className="mb-3 flex items-center gap-3 rounded-xl bg-accent/50 px-3 py-2.5">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground">
            {initials}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-foreground">{candidate?.name ?? "Guest"}</p>
            <p className="truncate text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
              Executive
            </p>
          </div>
        </div>
        <div className="flex flex-col gap-0.5">
          <button
            type="button"
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
          >
            <HelpCircle className="size-4" />
            Support
          </button>
          <button
            type="button"
            onClick={() => void handleLogout()}
            className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
          >
            <LogOut className="size-4" />
            Log out
          </button>
        </div>
      </div>
    </aside>
  )
}
