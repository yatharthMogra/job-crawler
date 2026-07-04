"use client"

import Link from "next/link"
import { useMemo } from "react"
import { ChevronRight, Download, Shield, ShieldCheck, TrendingUp } from "lucide-react"
import { useJobs } from "@/components/jobs-provider"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import { MatchGauge } from "@/components/ui/match-gauge"
import { cn } from "@/lib/utils"

export function ProfileInsightsPanel({
  data,
  className,
}: {
  data: ProfileHomeData
  className?: string
}) {
  const { recommendedJobs } = useJobs()

  const matchScore = useMemo(() => {
    const top = recommendedJobs
      .filter((j) => !j.is_applied)
      .sort((a, b) => b.personal_score - a.personal_score)[0]
    return top?.personal_score ?? 0.94
  }, [recommendedJobs])

  const primaryRole = data.primaryRoles[0] ?? "your target roles"
  const matchPct = Math.round(matchScore * 100)
  const salaryBand = useMemo(() => {
    const salaries = recommendedJobs
      .filter((j) => j.salary_min != null || j.salary_max != null)
      .slice(0, 20)
    if (salaries.length === 0) return "$165k – $210k"
    const mins = salaries
      .map((j) => j.salary_min ?? j.salary_max ?? 0)
      .filter((v) => v >= 80_000)
    const maxs = salaries
      .map((j) => j.salary_max ?? j.salary_min ?? 0)
      .filter((v) => v >= 80_000)
    if (mins.length === 0 || maxs.length === 0) return "$165k – $210k"
    const lo = Math.round(Math.min(...mins) / 1000)
    const hi = Math.round(Math.max(...maxs) / 1000)
    if (hi - lo > 120) return "$165k – $210k"
    return `$${lo}k – $${hi}k`
  }, [recommendedJobs])

  return (
    <aside className={cn("w-full shrink-0 space-y-4 xl:w-[280px]", className)}>
      <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-sm">
        <p className="mb-3 text-center text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          Profile strength
        </p>
        <MatchGauge score={matchScore} variant="ring" className="mx-auto" />
        <p className="mt-4 text-center text-sm leading-relaxed text-muted-foreground">
          Your profile alignment for{" "}
          <span className="font-semibold text-foreground">{primaryRole}</span> roles is{" "}
          {matchPct >= 90 ? "exceptionally high" : "strong"}.
        </p>
      </div>

      <div className="rounded-2xl border border-border/60 bg-card p-4 shadow-sm">
        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          Quick actions
        </p>
        <ul className="mt-3 space-y-1">
          {[
            { icon: ShieldCheck, label: "Verify identity", href: "/settings" },
            { icon: Shield, label: "Privacy settings", href: "/settings" },
            { icon: Download, label: "Download CV", href: "/resume" },
          ].map((item) => (
            <li key={item.label}>
              <Link
                href={item.href}
                className="flex items-center justify-between rounded-xl px-2 py-2.5 text-sm font-medium text-foreground/80 transition-colors hover:bg-muted/60"
              >
                <span className="flex items-center gap-2.5">
                  <item.icon className="size-4 text-muted-foreground" />
                  {item.label}
                </span>
                <ChevronRight className="size-4 text-muted-foreground" />
              </Link>
            </li>
          ))}
        </ul>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-5 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
            Market insights
          </p>
          <TrendingUp className="size-4 text-violet-300" />
        </div>
        <p className="mt-4 text-[10px] font-bold uppercase tracking-widest text-slate-400">
          Salary range
        </p>
        <p className="mt-1 text-2xl font-bold tracking-tight">{salaryBand}</p>
        <p className="mt-1 text-xs text-slate-400">Based on market data for {primaryRole} roles.</p>
        <p className="mt-5 text-[10px] font-bold uppercase tracking-widest text-slate-400">
          Demand
        </p>
        <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-700">
          <div className="h-full w-[85%] rounded-full bg-primary" />
        </div>
        <p className="mt-2 text-xs text-slate-300">Demand is 12% higher than last month.</p>
        <button
          type="button"
          className="btn-brand mt-5 w-full rounded-xl py-2.5 text-sm font-bold"
        >
          Upgrade to Executive
        </button>
      </div>
    </aside>
  )
}
