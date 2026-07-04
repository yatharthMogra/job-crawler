"use client"

import { ArrowRight, Clock, TrendingUp, Zap } from "lucide-react"
import { MatchGauge } from "@/components/ui/match-gauge"
import { cn } from "@/lib/utils"

interface FiltersMatchPanelProps {
  matchCount: number
  alignmentScore: number
  candidateName: string
  saving: boolean
  onViewMatches: () => void
  className?: string
}

export function FiltersMatchPanel({
  matchCount,
  alignmentScore,
  candidateName,
  saving,
  onViewMatches,
  className,
}: FiltersMatchPanelProps) {
  const formattedCount = matchCount.toLocaleString()
  const pct = Math.round(alignmentScore * 100)

  return (
    <aside className={cn("w-full shrink-0 space-y-4 xl:w-[300px]", className)}>
      <div className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-5 text-white shadow-lg">
        <div className="flex items-center justify-between gap-2">
          <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
            Live match impact
          </p>
          <span className="rounded-full bg-emerald-500/15 px-2 py-0.5 text-[9px] font-bold uppercase tracking-wide text-emerald-300">
            Real-time
          </span>
        </div>
        <p className="mt-4 text-4xl font-bold tabular-nums tracking-tight">{formattedCount}</p>
        <p className="mt-1 text-sm text-slate-300">Qualified opportunities found</p>
        <p className="mt-3 inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-300">
          <TrendingUp className="size-3.5" />
          +12.4% vs. previous search criteria
        </p>
      </div>

      <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-sm">
        <div className="flex items-center gap-4">
          <MatchGauge score={alignmentScore} variant="ring" className="shrink-0" />
          <div>
            <p className="text-sm font-bold text-foreground">Profile alignment</p>
            <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
              {pct >= 90
                ? "High relevance score based on your executive history and skills."
                : "Strong relevance based on your profile and selected filters."}
            </p>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-sm">
        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          Market insights
        </p>
        <ul className="mt-4 space-y-4">
          <li className="flex gap-3">
            <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-amber-500/10 text-amber-700">
              <Zap className="size-4" />
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground">High competition</p>
              <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                FinTech roles in this bracket receive 40+ applicants daily.
              </p>
            </div>
          </li>
          <li className="flex gap-3">
            <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
              <Clock className="size-4" />
            </div>
            <div>
              <p className="text-sm font-semibold text-foreground">Fast-track hiring</p>
              <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
                Top companies are closing offers 30% faster this quarter.
              </p>
            </div>
          </li>
        </ul>
      </div>

      <button
        type="button"
        onClick={onViewMatches}
        disabled={saving}
        className="btn-brand flex w-full items-center justify-center gap-2 rounded-xl py-3.5 text-sm font-bold disabled:opacity-60"
      >
        {saving ? "Saving filters..." : `View ${formattedCount} matches`}
        {!saving ? <ArrowRight className="size-4" /> : null}
      </button>
      <p className="text-center text-[11px] text-muted-foreground">
        Personalized for {candidateName}
      </p>
    </aside>
  )
}
