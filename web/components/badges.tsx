import type { Effort } from "@/lib/jobs-data"

const STYLES: Record<Effort, string> = {
  LOW: "bg-green-50 text-green-700",
  MEDIUM: "bg-amber-50 text-amber-700",
  HIGH: "bg-orange-50 text-orange-700",
}

const LABELS: Record<Effort, string> = {
  LOW: "Low effort",
  MEDIUM: "Medium effort",
  HIGH: "High effort",
}

export function EffortBadge({ effort, className = "" }: { effort: Effort; className?: string }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${STYLES[effort]} ${className}`}
    >
      {LABELS[effort]}
    </span>
  )
}

export function MatchTag({ label }: { label: string }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-green-50 px-2 py-0.5 text-xs font-medium text-green-700">
      <svg viewBox="0 0 16 16" className="size-3" fill="none" aria-hidden="true">
        <path d="M13 4.5 6.5 11 3 7.5" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {label}
    </span>
  )
}

export function StatPill({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex items-center rounded-md border border-zinc-200 bg-zinc-50 px-2 py-1 text-xs font-medium text-zinc-700">
      {children}
    </span>
  )
}
