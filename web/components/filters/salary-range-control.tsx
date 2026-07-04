"use client"

import {
  SALARY_CEILING,
  SALARY_FLOOR,
  SALARY_MEDIAN,
  formatSalaryCompact,
  formatSalaryRange,
} from "@/lib/filters/filter-options"
import { cn } from "@/lib/utils"

interface SalaryRangeControlProps {
  min: number
  max: number
  onChange: (next: { min: number; max: number }) => void
  className?: string
}

export function SalaryRangeControl({ min, max, onChange, className }: SalaryRangeControlProps) {
  const span = SALARY_CEILING - SALARY_FLOOR
  const minPct = ((min - SALARY_FLOOR) / span) * 100
  const maxPct = ((max - SALARY_FLOOR) / span) * 100
  const medianPct = ((SALARY_MEDIAN - SALARY_FLOOR) / span) * 100

  function setMin(value: number) {
    onChange({ min: Math.min(value, max - 10_000), max })
  }

  function setMax(value: number) {
    onChange({ min, max: Math.max(value, min + 10_000) })
  }

  return (
    <div className={cn("space-y-5", className)}>
      <p className="text-sm font-semibold text-foreground">{formatSalaryRange(min, max)}</p>

      <div className="relative pt-1 pb-6">
        <div className="relative h-1.5 rounded-full bg-muted">
          <div
            className="absolute inset-y-0 rounded-full bg-primary/80"
            style={{ left: `${minPct}%`, right: `${100 - maxPct}%` }}
          />
        </div>

        <span
          className="absolute top-5 text-[10px] font-semibold uppercase tracking-wide text-muted-foreground"
          style={{ left: `${medianPct}%`, transform: "translateX(-50%)" }}
        >
          Market median ({formatSalaryCompact(SALARY_MEDIAN)})
        </span>

        <input
          type="range"
          min={SALARY_FLOOR}
          max={SALARY_CEILING}
          step={5_000}
          value={min}
          onChange={(e) => setMin(Number(e.target.value))}
          className="salary-range-thumb absolute inset-x-0 top-0 h-1.5 w-full appearance-none bg-transparent pointer-events-none [&::-webkit-slider-thumb]:pointer-events-auto [&::-moz-range-thumb]:pointer-events-auto"
          aria-label="Minimum salary"
        />
        <input
          type="range"
          min={SALARY_FLOOR}
          max={SALARY_CEILING}
          step={5_000}
          value={max}
          onChange={(e) => setMax(Number(e.target.value))}
          className="salary-range-thumb absolute inset-x-0 top-0 h-1.5 w-full appearance-none bg-transparent pointer-events-none [&::-webkit-slider-thumb]:pointer-events-auto [&::-moz-range-thumb]:pointer-events-auto"
          aria-label="Maximum salary"
        />
      </div>

      <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
        <span>Floor ({formatSalaryCompact(SALARY_FLOOR)})</span>
        <span>Ceiling ({formatSalaryCompact(SALARY_CEILING)})</span>
      </div>
    </div>
  )
}
