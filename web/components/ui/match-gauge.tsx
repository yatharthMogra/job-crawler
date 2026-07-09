"use client"

import { cn } from "@/lib/utils"

interface MatchGaugeProps {
  score: number
  reasons?: string[]
  insight?: string
  className?: string
  variant?: "bar" | "ring" | "sidebar"
  compact?: boolean
}

export function matchLabel(score: number): string {
  if (score >= 0.85) return "STRONG"
  if (score >= 0.75) return "GOOD"
  if (score >= 0.65) return "FAIR"
  return "LOW"
}

/** Human-readable descriptor consistent with the gauge band shown to the user. */
export function matchDescriptor(score: number): string {
  if (score >= 0.9) return "exceptionally high"
  if (score >= 0.85) return "strong"
  if (score >= 0.75) return "solid"
  if (score >= 0.65) return "moderate"
  return "still developing"
}

function ringColor(score: number) {
  if (score >= 0.85) return "text-add stroke-add"
  if (score >= 0.75) return "text-primary stroke-primary"
  return "text-muted-foreground stroke-muted-foreground"
}

function MatchRing({
  score,
  className,
  sidebar = false,
  size: sizeProp = "md",
}: {
  score: number
  className?: string
  sidebar?: boolean
  size?: "md" | "lg"
}) {
  const pct = Math.round(Math.min(1, Math.max(0, score)) * 100)
  const size = sidebar ? 92 : sizeProp === "lg" ? 104 : 72
  const radius = sidebar ? 36 : sizeProp === "lg" ? 40 : 28
  const strokeWidth = sidebar ? 5 : 5
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (pct / 100) * circumference
  const label = matchLabel(score)

  const ringClass = sidebar
    ? score >= 0.85
      ? "stroke-teal-300"
      : score >= 0.75
        ? "stroke-teal-400"
        : "stroke-teal-500/55"
    : ringColor(score)

  const textClass = sidebar
    ? score >= 0.85
      ? "text-teal-200"
      : score >= 0.75
        ? "text-teal-300"
        : "text-teal-400/90"
    : ringColor(score).split(" ")[0]

  return (
    <div className={cn("flex flex-col items-center gap-0.5", className)}>
      <div className="relative" style={{ width: size, height: size }}>
        <svg className="size-full -rotate-90" viewBox={`0 0 ${size} ${size}`}>
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            strokeWidth={strokeWidth}
            className={sidebar ? "stroke-white/15" : "stroke-muted"}
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className={cn("transition-all", ringClass)}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn(
            sidebar ? "text-xl sm:text-2xl" : sizeProp === "lg" ? "text-2xl" : "text-sm",
            "font-bold tabular-nums",
            textClass,
          )}>
            {pct}%
          </span>
        </div>
      </div>
      <span
        className={cn(
          "font-bold tracking-wider",
          sidebar ? "text-[10px] text-white" : "text-[9px]",
          !sidebar && textClass,
        )}
      >
        {sidebar ? `${label} MATCH` : sizeProp === "lg" ? label : label}
      </span>
    </div>
  )
}

function barGradient(score: number) {
  if (score >= 0.8) return "from-primary to-primary/70"
  if (score >= 0.65) return "from-primary/80 to-primary/60"
  return "from-muted-foreground/40 to-muted-foreground/60"
}

export function MatchGauge({
  score,
  reasons = [],
  insight,
  className,
  variant = "bar",
  compact = false,
}: MatchGaugeProps) {
  if (variant === "sidebar") {
    return <MatchRing score={score} className={className} sidebar />
  }

  if (variant === "ring" || compact) {
    return <MatchRing score={score} className={className} size="lg" />
  }

  const pct = Math.round(Math.min(1, Math.max(0, score)) * 100)
  const label = matchLabel(score)

  return (
    <div className={cn("flex flex-col gap-3", className)}>
      <div>
        <p className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
          Profile match
        </p>
        <div className="mt-1.5 flex items-baseline gap-2">
          <span className="text-3xl font-bold tabular-nums text-primary">{pct}%</span>
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
              <span className="mt-1.5 size-1 shrink-0 rounded-full bg-primary" />
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
