"use client"

import { X } from "lucide-react"
import { cn } from "@/lib/utils"

interface FilterChipProps {
  label: string
  active?: boolean
  onRemove?: () => void
  onClick?: () => void
  className?: string
}

export function FilterChip({ label, active, onRemove, onClick, className }: FilterChipProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs font-medium transition-colors",
        active
          ? "border-primary/25 bg-accent text-accent-foreground"
          : "border-border bg-card text-muted-foreground",
        onClick && "cursor-pointer hover:bg-accent/50",
        className,
      )}
      onClick={onClick}
      role={onClick ? "button" : undefined}
    >
      {label}
      {onRemove ? (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation()
            onRemove()
          }}
          className="rounded-full p-0.5 hover:bg-primary/10"
          aria-label={`Remove ${label}`}
        >
          <X className="size-3" />
        </button>
      ) : null}
    </span>
  )
}
