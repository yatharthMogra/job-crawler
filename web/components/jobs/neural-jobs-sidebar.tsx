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
import { clearStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

const JOBS_NAV = [
  { href: "/jobs/recommended", label: "Recommended Jobs", icon: Briefcase },
  { href: "/jobs/liked", label: "Saved Jobs", icon: Bookmark },
  { href: "/filters", label: "Filters", icon: Settings2 },
  { href: "/profile", label: "Profile", icon: User },
]

export function NeuralJobsSidebar() {
  const pathname = usePathname()
  const router = useRouter()

  async function endSession() {
    clearStoredCandidateId()
    await signOut({ callbackUrl: "/login" })
    router.push("/login")
  }

  return (
    <aside className="hidden w-52 shrink-0 flex-col border-r border-border/60 bg-card/50 xl:flex">
      <div className="border-b border-border/60 px-4 py-4">
        <div className="flex items-center gap-2">
          <span className="relative flex size-2">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-60" />
            <span className="relative inline-flex size-2 rounded-full bg-emerald-500" />
          </span>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-foreground">Live</p>
            <p className="text-[10px] text-muted-foreground">Matching active</p>
          </div>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-3">
        {JOBS_NAV.map(({ href, label, icon: Icon }) => {
          const active =
            pathname === href ||
            (href !== "/filters" && pathname.startsWith(`${href}/`)) ||
            (href === "/filters" && pathname.startsWith("/filters"))
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all",
                active
                  ? "border-l-2 border-primary bg-primary/5 text-primary"
                  : "text-muted-foreground hover:bg-muted/50 hover:text-foreground",
              )}
            >
              <Icon className="size-4 shrink-0" />
              {label}
            </Link>
          )
        })}
      </nav>

      <div className="space-y-1 border-t border-border/60 p-4">
        <button
          type="button"
          onClick={() => void endSession()}
          className="flex w-full items-center gap-2 rounded-lg px-2 py-2 text-xs font-medium text-muted-foreground hover:bg-muted/50 hover:text-foreground"
        >
          <LogOut className="size-3.5" />
          Log out
        </button>
      </div>
    </aside>
  )
}
