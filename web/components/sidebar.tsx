"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Briefcase, FileText, Settings, User } from "lucide-react"
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
        "flex flex-col items-center gap-1 rounded-lg px-3 py-2.5 text-xs transition-colors",
        active ? "bg-zinc-100 font-medium text-zinc-900" : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-800",
      )}
    >
      <Icon className="size-5 shrink-0" strokeWidth={active ? 2.5 : 2} />
      {label}
    </Link>
  )
}

export function Sidebar() {
  const pathname = usePathname()
  const { candidate } = useSession()

  return (
    <aside className="fixed inset-y-0 left-0 z-30 flex w-[72px] flex-col border-r border-zinc-200/80 bg-white sm:w-[88px]">
      <div className="flex h-14 items-center justify-center">
        <span className="text-lg font-bold text-zinc-900">C</span>
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

      <div className="border-t border-zinc-200 px-2 py-3 text-center">
        <div className="mx-auto flex size-8 items-center justify-center rounded-full bg-zinc-100 text-xs font-semibold text-zinc-700">
          {(candidate?.name ?? "U").charAt(0).toUpperCase()}
        </div>
      </div>
    </aside>
  )
}
