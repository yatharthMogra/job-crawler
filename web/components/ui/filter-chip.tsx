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
          ? "border-zinc-300 bg-zinc-100 text-zinc-800"
          : "border-zinc-200 bg-white text-zinc-700",
        onClick && "cursor-pointer hover:bg-zinc-50",
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
          className="rounded-full p-0.5 hover:bg-zinc-200"
          aria-label={`Remove ${label}`}
        >
          <X className="size-3" />
        </button>
      ) : null}
    </span>
  )
}
