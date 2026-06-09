"use client"

import { cn } from "@/lib/utils"

interface MatchGaugeProps {
  score: number
  reasons?: string[]
  insight?: string
  className?: string
}

export function matchLabel(score: number): string {
  if (score >= 0.8) return "Excellent fit"
  if (score >= 0.65) return "Strong fit"
  if (score >= 0.5) return "Good fit"
  return "Fair fit"
}

export function MatchGauge({ score, reasons = [], insight, className }: MatchGaugeProps) {
  const pct = Math.round(Math.min(1, Math.max(0, score)) * 100)
  const label = matchLabel(score)

  return (
    <div className={cn("flex flex-col gap-3", className)}>
      <div>
        <p className="text-[10px] font-medium uppercase tracking-wider text-zinc-400">Profile match</p>
        <div className="mt-1 flex items-baseline gap-2">
          <span className="text-3xl font-semibold tabular-nums text-zinc-900">{pct}%</span>
          <span className="text-[11px] text-zinc-500">{label}</span>
        </div>
      </div>

      <div className="h-1 overflow-hidden rounded-full bg-zinc-100">
        <div className="h-full rounded-full bg-zinc-900 transition-all" style={{ width: `${pct}%` }} />
      </div>

      {reasons.length > 0 ? (
        <ul className="space-y-1.5">
          {reasons.slice(0, 3).map((reason) => (
            <li key={reason} className="text-[11px] leading-snug text-zinc-600">
              {reason}
            </li>
          ))}
        </ul>
      ) : null}

      {insight ? (
        <p className="text-[10px] leading-relaxed text-zinc-400">{insight}</p>
      ) : null}
    </div>
  )
}
