"use client"

import { useEffect, useRef, useState } from "react"
import { CheckCircle2, Flag, ThumbsDown, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface JobActionsMenuProps {
  onApplied: () => void
  onNotInterested: () => void
  onReportIssue: () => void
  isApplied?: boolean
  className?: string
}

export function JobActionsMenu({
  onApplied,
  onNotInterested,
  onReportIssue,
  isApplied,
  className,
}: JobActionsMenuProps) {
  const [open, setOpen] = useState(false)
  const rootRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!open) return
    function onPointerDown(e: MouseEvent) {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", onPointerDown)
    return () => document.removeEventListener("mousedown", onPointerDown)
  }, [open])

  function run(action: () => void) {
    setOpen(false)
    action()
  }

  return (
    <div ref={rootRef} className={cn("relative", className)}>
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation()
          setOpen((v) => !v)
        }}
        className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
        aria-label="Job actions"
      >
        <X className="size-4" />
      </button>

      {open ? (
        <div
          className="absolute right-0 top-full z-20 mt-1 min-w-[180px] overflow-hidden rounded-xl border border-border/80 bg-card py-1 shadow-lg shadow-primary/10"
          onClick={(e) => e.stopPropagation()}
        >
          <button
            type="button"
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-foreground hover:bg-secondary/80"
            onClick={() => run(onApplied)}
          >
            <CheckCircle2 className="size-4 text-add" />
            {isApplied ? "Applied" : "Mark as applied"}
          </button>
          <button
            type="button"
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-foreground hover:bg-secondary/80"
            onClick={() => run(onNotInterested)}
          >
            <ThumbsDown className="size-4 text-muted-foreground" />
            Not interested
          </button>
          <button
            type="button"
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-foreground hover:bg-secondary/80"
            onClick={() => run(onReportIssue)}
          >
            <Flag className="size-4 text-muted-foreground" />
            Report issue
          </button>
        </div>
      ) : null}
    </div>
  )
}
