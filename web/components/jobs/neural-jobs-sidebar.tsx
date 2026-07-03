"use client"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import {
  BarChart3,
  Bookmark,
  Headphones,
  LayoutDashboard,
  LogOut,
  Sparkles,
  TrendingUp,
} from "lucide-react"
import { signOut } from "next-auth/react"
import { clearStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

const INTEL_NAV = [
  { href: "/jobs/recommended", label: "Intelligence Desk", icon: LayoutDashboard },
  { href: "/jobs/liked", label: "Saved Opportunities", icon: Bookmark },
  { href: "/filters", label: "Market Dynamics", icon: TrendingUp },
  { href: "/profile", label: "Asset Analytics", icon: BarChart3 },
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
    <aside className="hidden w-56 shrink-0 flex-col border-r border-border/60 bg-card/50 xl:flex">
      <div className="border-b border-border/60 px-4 py-4">
        <div className="flex items-center gap-2">
          <span className="relative flex size-2">
            <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-60" />
            <span className="relative inline-flex size-2 rounded-full bg-emerald-500" />
          </span>
          <div>
            <p className="text-[10px] font-bold uppercase tracking-widest text-foreground">
              System Active
            </p>
            <p className="text-[10px] text-muted-foreground">Neural Intelligence Core v4.2</p>
          </div>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-3">
        {INTEL_NAV.map(({ href, label, icon: Icon }) => {
          const active = pathname === href || pathname.startsWith(`${href}/`)
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

      <div className="space-y-2 border-t border-border/60 p-4">
        <button
          type="button"
          className="btn-brand flex h-10 w-full items-center justify-center gap-2 rounded-xl text-xs font-bold uppercase tracking-wide"
        >
          <Sparkles className="size-3.5" />
          Upgrade to Pro
        </button>
        <button
          type="button"
          className="flex w-full items-center gap-2 rounded-lg px-2 py-2 text-xs font-medium text-muted-foreground hover:bg-muted/50 hover:text-foreground"
        >
          <Headphones className="size-3.5" />
          Concierge Support
        </button>
        <button
          type="button"
          onClick={() => void endSession()}
          className="flex w-full items-center gap-2 rounded-lg px-2 py-2 text-xs font-medium text-muted-foreground hover:bg-muted/50 hover:text-foreground"
        >
          <LogOut className="size-3.5" />
          End Session
        </button>
      </div>
    </aside>
  )
}
