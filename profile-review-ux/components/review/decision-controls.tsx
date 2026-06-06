"use client"

import type { ChangeKind, ItemStatus } from "@/lib/profile-data"
import { cn } from "@/lib/utils"
import { Check, X } from "lucide-react"

const kindConfig: Record<ChangeKind, { symbol: string; label: string; classes: string }> = {
  add: { symbol: "+", label: "New", classes: "bg-add-muted text-add-foreground" },
  update: { symbol: "~", label: "Updated", classes: "bg-update-muted text-update-foreground" },
  remove: { symbol: "−", label: "Removed", classes: "bg-remove-muted text-remove-foreground" },
}

export function KindBadge({ kind, withLabel = true }: { kind: ChangeKind; withLabel?: boolean }) {
  const c = kindConfig[kind]
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-md px-2 py-0.5 text-xs font-medium",
        c.classes,
      )}
    >
      <span className="font-mono font-semibold leading-none">{c.symbol}</span>
      {withLabel ? <span>{c.label}</span> : null}
    </span>
  )
}

interface DecisionControlsProps {
  status: ItemStatus
  onApprove: () => void
  onReject: () => void
  onEdit?: () => void
  approveLabel?: string
  rejectLabel?: string
  size?: "sm" | "md"
}

export function DecisionControls({
  status,
  onApprove,
  onReject,
  onEdit,
  approveLabel = "Approve",
  rejectLabel = "Reject",
  size = "md",
}: DecisionControlsProps) {
  if (status === "approved") {
    return (
      <div className="flex items-center gap-2">
        <span className="inline-flex items-center gap-1 rounded-md bg-add-muted px-2.5 py-1 text-xs font-medium text-add-foreground">
          <Check className="size-3.5" aria-hidden="true" /> Approved
        </span>
        <button
          type="button"
          onClick={onReject}
          className="text-xs text-muted-foreground underline-offset-2 hover:text-foreground hover:underline"
        >
          Undo
        </button>
      </div>
    )
  }
  if (status === "rejected") {
    return (
      <div className="flex items-center gap-2">
        <span className="inline-flex items-center gap-1 rounded-md bg-secondary px-2.5 py-1 text-xs font-medium text-muted-foreground">
          <X className="size-3.5" aria-hidden="true" /> Rejected
        </span>
        <button
          type="button"
          onClick={onApprove}
          className="text-xs text-muted-foreground underline-offset-2 hover:text-foreground hover:underline"
        >
          Undo
        </button>
      </div>
    )
  }

  const pad = size === "sm" ? "h-7 px-2.5 text-xs" : "h-8 px-3 text-sm"
  return (
    <div className="flex items-center gap-2">
      <button
        type="button"
        onClick={onApprove}
        className={cn(
          "inline-flex items-center gap-1 rounded-md border border-add/40 bg-add-muted/60 font-medium text-add-foreground transition-colors hover:bg-add-muted",
          pad,
        )}
      >
        <Check className="size-3.5" aria-hidden="true" />
        {approveLabel}
      </button>
      <button
        type="button"
        onClick={onReject}
        className={cn(
          "inline-flex items-center gap-1 rounded-md border border-border bg-card font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground",
          pad,
        )}
      >
        <X className="size-3.5" aria-hidden="true" />
        {rejectLabel}
      </button>
      {onEdit ? (
        <button
          type="button"
          onClick={onEdit}
          className={cn(
            "inline-flex items-center gap-1 rounded-md border border-border bg-card font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground",
            pad,
          )}
        >
          Edit
        </button>
      ) : null}
    </div>
  )
}
