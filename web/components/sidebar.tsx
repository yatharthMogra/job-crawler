"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutGrid, Star, Bookmark, Check, User, Settings } from "lucide-react"
import { useSession } from "@/components/session-provider"
import { cn } from "@/lib/utils"

const NAV = [
  { href: "/jobs", label: "All Jobs", icon: LayoutGrid },
  { href: "/recommended", label: "Recommended", icon: Star },
  { href: "/saved", label: "Saved", icon: Bookmark },
  { href: "/applied", label: "Applied", icon: Check },
]

const SECONDARY = [
  { href: "/profile", label: "Profile", icon: User },
  { href: "/preferences", label: "Preferences", icon: Settings },
]

function NavRow({ href, label, icon: Icon, active }: { href: string; label: string; icon: typeof Star; active: boolean }) {
  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-2.5 rounded-md px-2.5 py-1.5 text-sm transition-colors",
        active ? "bg-zinc-900 font-medium text-white" : "text-zinc-600 hover:bg-zinc-200/60 hover:text-zinc-900",
      )}
    >
      <Icon className="size-4 shrink-0" strokeWidth={2} />
      {label}
    </Link>
  )
}

export function Sidebar() {
  const pathname = usePathname()
  const { candidate } = useSession()
  return (
    <aside className="fixed inset-y-0 left-0 z-30 flex w-[220px] flex-col border-r border-zinc-200 bg-zinc-100">
      <div className="flex h-14 items-center px-4">
        <span className="text-sm font-semibold tracking-tight text-zinc-900">Career Match AI</span>
      </div>
      <div className="border-t border-zinc-200" />

      <nav className="flex flex-1 flex-col gap-0.5 px-3 py-3">
        {NAV.map((item) => (
          <NavRow key={item.href} {...item} active={pathname === item.href} />
        ))}
        <div className="my-2 border-t border-zinc-200" />
        {SECONDARY.map((item) => (
          <NavRow key={item.href} {...item} active={pathname === item.href} />
        ))}
      </nav>

      <div className="border-t border-zinc-200 px-4 py-3">
        <p className="truncate text-sm font-medium text-zinc-800">
          {candidate?.name ?? "Your account"}
        </p>
        <p className="truncate text-xs text-zinc-500">{candidate?.email ?? ""}</p>
      </div>
    </aside>
  )
}
