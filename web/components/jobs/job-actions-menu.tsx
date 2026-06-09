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
        className="rounded-md p-1.5 text-zinc-400 transition-colors hover:bg-zinc-100 hover:text-zinc-600"
        aria-label="Job actions"
      >
        <X className="size-4" />
      </button>

      {open ? (
        <div
          className="absolute right-0 top-full z-20 mt-1 min-w-[180px] overflow-hidden rounded-lg border border-zinc-200 bg-white py-1 shadow-lg"
          onClick={(e) => e.stopPropagation()}
        >
          <button
            type="button"
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-zinc-700 hover:bg-zinc-50"
            onClick={() => run(onApplied)}
          >
            <CheckCircle2 className="size-4 text-zinc-700" />
            {isApplied ? "Applied" : "Mark as applied"}
          </button>
          <button
            type="button"
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-zinc-700 hover:bg-zinc-50"
            onClick={() => run(onNotInterested)}
          >
            <ThumbsDown className="size-4 text-zinc-500" />
            Not interested
          </button>
          <button
            type="button"
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-zinc-700 hover:bg-zinc-50"
            onClick={() => run(onReportIssue)}
          >
            <Flag className="size-4 text-zinc-500" />
            Report issue
          </button>
        </div>
      ) : null}
    </div>
  )
}
