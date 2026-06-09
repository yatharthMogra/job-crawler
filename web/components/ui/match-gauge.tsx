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

function barGradient(score: number) {
  if (score >= 0.8) return "from-brand to-primary"
  if (score >= 0.65) return "from-primary to-brand"
  if (score >= 0.5) return "from-primary/80 to-brand/80"
  return "from-muted-foreground/40 to-muted-foreground/60"
}

export function MatchGauge({ score, reasons = [], insight, className }: MatchGaugeProps) {
  const pct = Math.round(Math.min(1, Math.max(0, score)) * 100)
  const label = matchLabel(score)

  return (
    <div className={cn("flex flex-col gap-3", className)}>
      <div>
        <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
          Profile match
        </p>
        <div className="mt-1.5 flex items-baseline gap-2">
          <span className="text-3xl font-bold tabular-nums gradient-text">{pct}%</span>
          <span className="rounded-full bg-accent px-2 py-0.5 text-[10px] font-medium text-accent-foreground">
            {label}
          </span>
        </div>
      </div>

      <div className="h-1.5 overflow-hidden rounded-full bg-muted">
        <div
          className={cn("h-full rounded-full bg-gradient-to-r transition-all", barGradient(score))}
          style={{ width: `${pct}%` }}
        />
      </div>

      {reasons.length > 0 ? (
        <ul className="space-y-1.5">
          {reasons.slice(0, 3).map((reason) => (
            <li key={reason} className="flex items-start gap-1.5 text-[11px] leading-snug text-muted-foreground">
              <span className="mt-1.5 size-1 shrink-0 rounded-full bg-brand" />
              {reason}
            </li>
          ))}
        </ul>
      ) : null}

      {insight ? (
        <p className="text-[10px] leading-relaxed text-muted-foreground/80">{insight}</p>
      ) : null}
    </div>
  )
}
