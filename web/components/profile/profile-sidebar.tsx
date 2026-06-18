"use client"

import Link from "next/link"
import { useMemo } from "react"
import {
  ChevronRight,
  Download,
  History,
  Share2,
  Shield,
  ShieldCheck,
} from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import { useSession } from "@/components/session-provider"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import { MatchGauge } from "@/components/ui/match-gauge"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

interface ProfileSidebarProps {
  data: ProfileHomeData
  className?: string
}

export function ProfileSidebar({ data, className }: ProfileSidebarProps) {
  const { candidate } = useSession()
  const { recommendedJobs } = useJobs()

  const matchScore = useMemo(() => {
    const top = recommendedJobs
      .filter((j) => !j.is_applied)
      .sort((a, b) => b.personal_score - a.personal_score)[0]
    return top?.personal_score ?? 0.85
  }, [recommendedJobs])

  const initials = (candidate?.name ?? data.candidateName).charAt(0).toUpperCase()
  const primaryRole = data.primaryRoles[0] ?? "executive roles"

  async function handleShare() {
    const url = window.location.href
    if (navigator.share) {
      await navigator.share({ title: "My CareerMatch Profile", url })
    } else {
      await navigator.clipboard.writeText(url)
    }
  }

  return (
    <aside className={cn("w-[280px] shrink-0 space-y-4", className)}>
      <div className="rounded-2xl bg-accent/60 p-5 text-center">
        <div className="mx-auto flex size-16 items-center justify-center rounded-full bg-primary text-xl font-bold text-primary-foreground">
          {initials}
        </div>
        <p className="mt-3 font-semibold text-foreground">{data.candidateName}</p>
        <span className="mt-2 inline-block rounded-full bg-primary/15 px-3 py-0.5 text-[10px] font-bold uppercase tracking-wider text-primary">
          Active Executive
        </span>
      </div>

      <Button className="btn-brand h-10 w-full gap-2" disabled title="Coming soon">
        <Download className="size-4" />
        Download Premium CV
      </Button>

      <Button variant="outline" className="h-10 w-full gap-2" onClick={() => void handleShare()}>
        <Share2 className="size-4" />
        Share Executive Profile
      </Button>

      <div className="rounded-xl border border-border bg-card p-4">
        <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Quick Actions
        </p>
        <ul className="space-y-1">
          {[
            { icon: ShieldCheck, label: "Verify Identity", href: "/settings" },
            { icon: Shield, label: "Privacy Settings", href: "/settings" },
            { icon: History, label: "Profile History", href: "/settings" },
          ].map((item) => (
            <li key={item.label}>
              <Link
                href={item.href}
                className="flex items-center justify-between rounded-lg px-2 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
              >
                <span className="flex items-center gap-2">
                  <item.icon className="size-4" />
                  {item.label}
                </span>
                <ChevronRight className="size-4" />
              </Link>
            </li>
          ))}
        </ul>
      </div>

      <div className="card-elevated p-5">
        <MatchGauge score={matchScore} />
        <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
          Your profile alignment for <strong className="text-foreground">{primaryRole}</strong> roles
          is {matchScore >= 0.9 ? "exceptionally high" : "strong"}.
        </p>
      </div>
    </aside>
  )
}
