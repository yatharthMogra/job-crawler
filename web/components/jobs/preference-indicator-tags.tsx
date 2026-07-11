import type { PreferenceIndicator } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

export function PreferenceIndicatorTags({
  indicators,
  className,
}: {
  indicators: PreferenceIndicator[]
  className?: string
}) {
  if (indicators.length === 0) return null

  return (
    <div className={cn("flex flex-wrap gap-1.5", className)}>
      {indicators.map((indicator) => (
        <span
          key={`${indicator.kind}:${indicator.label}`}
          className={cn(
            "rounded-full px-2.5 py-1 text-[11px] font-semibold",
            indicator.kind === "strength"
              ? "bg-emerald-500/12 text-emerald-800"
              : "bg-amber-500/15 text-amber-900",
          )}
        >
          {indicator.label}
        </span>
      ))}
    </div>
  )
}
