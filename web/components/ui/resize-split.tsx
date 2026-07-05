"use client"

import { useCallback, useEffect, useRef, useState, type ReactNode } from "react"
import { cn } from "@/lib/utils"

/** Narrowest left pane — matches design; divider cannot move left of this. */
const MIN_LIST_PX = 460
/** Widest left pane — drag divider right to narrow the detail panel further. */
const MAX_LIST_PX = 680
const DEFAULT_LEFT_PX = MIN_LIST_PX
const DIVIDER_PX = 4
/** Detail panel can shrink to this width when the list is fully expanded. */
const MIN_RIGHT_PX = 280

export function ResizeSplit({
  left,
  right,
  className,
  enabled = true,
}: {
  left: ReactNode
  right: ReactNode
  className?: string
  enabled?: boolean
}) {
  const containerRef = useRef<HTMLDivElement>(null)
  const leftWidthRef = useRef(DEFAULT_LEFT_PX)
  const dragging = useRef(false)
  const [leftWidth, setLeftWidth] = useState(DEFAULT_LEFT_PX)
  const initialized = useRef(false)

  const clampWidth = useCallback((next: number, containerWidth: number) => {
    const maxByRight = containerWidth - MIN_RIGHT_PX - DIVIDER_PX
    const maxLeft = Math.min(MAX_LIST_PX, maxByRight)
    const minLeft = Math.min(MIN_LIST_PX, maxLeft)
    return Math.min(Math.max(next, minLeft), Math.max(maxLeft, minLeft))
  }, [])

  const applyWidth = useCallback(
    (next: number) => {
      const containerWidth = containerRef.current?.getBoundingClientRect().width ?? 0
      const clamped =
        containerWidth > 0
          ? clampWidth(next, containerWidth)
          : Math.min(Math.max(next, MIN_LIST_PX), MAX_LIST_PX)
      leftWidthRef.current = clamped
      setLeftWidth(clamped)
    },
    [clampWidth],
  )

  useEffect(() => {
    if (initialized.current) return
    initialized.current = true
    applyWidth(DEFAULT_LEFT_PX)
  }, [applyWidth])

  useEffect(() => {
    const el = containerRef.current
    if (!el) return
    const ro = new ResizeObserver(() => {
      applyWidth(leftWidthRef.current)
    })
    ro.observe(el)
    return () => ro.disconnect()
  }, [applyWidth])

  const startDrag = useCallback(
    (clientX: number) => {
      dragging.current = true
      document.body.style.cursor = "col-resize"
      document.body.style.userSelect = "none"
      const rect = containerRef.current?.getBoundingClientRect()
      if (rect) applyWidth(clientX - rect.left)
    },
    [applyWidth],
  )

  const endDrag = useCallback(() => {
    if (!dragging.current) return
    dragging.current = false
    document.body.style.cursor = ""
    document.body.style.userSelect = ""
  }, [])

  useEffect(() => {
    function onPointerMove(e: PointerEvent) {
      if (!dragging.current || !containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      applyWidth(e.clientX - rect.left)
    }

    function onPointerUp() {
      endDrag()
    }

    window.addEventListener("pointermove", onPointerMove)
    window.addEventListener("pointerup", onPointerUp)
    return () => {
      window.removeEventListener("pointermove", onPointerMove)
      window.removeEventListener("pointerup", onPointerUp)
      endDrag()
    }
  }, [applyWidth, endDrag])

  if (!enabled) {
    return <div className={cn("flex min-h-0 flex-1 flex-col", className)}>{left}</div>
  }

  return (
    <div ref={containerRef} className={cn("flex min-h-0 flex-1 overflow-hidden", className)}>
      <div
        className="min-h-0 shrink-0 overflow-y-auto overflow-x-hidden border-r border-border/50 bg-muted/[0.18]"
        style={{ flex: `0 0 ${leftWidth}px`, width: leftWidth, minWidth: MIN_LIST_PX, maxWidth: MAX_LIST_PX }}
      >
        {left}
      </div>

      <div
        role="separator"
        aria-orientation="vertical"
        aria-label="Resize panels"
        aria-valuemin={MIN_LIST_PX}
        aria-valuemax={MAX_LIST_PX}
        aria-valuenow={leftWidth}
        className="relative z-50 shrink-0 touch-none select-none"
        style={{ width: DIVIDER_PX }}
      >
        <div className="absolute inset-y-0 left-1/2 w-px -translate-x-1/2 bg-border/60" />
        <button
          type="button"
          tabIndex={-1}
          aria-hidden="true"
          className="absolute inset-y-0 -left-3 -right-3 cursor-col-resize border-0 bg-transparent p-0"
          onPointerDown={(e) => {
            e.preventDefault()
            e.currentTarget.setPointerCapture(e.pointerId)
            startDrag(e.clientX)
          }}
          onPointerUp={(e) => {
            try {
              e.currentTarget.releasePointerCapture(e.pointerId)
            } catch {
              /* ignore */
            }
            endDrag()
          }}
          onLostPointerCapture={endDrag}
        />
      </div>

      <div className="min-h-0 min-w-0 flex-1 overflow-hidden">{right}</div>
    </div>
  )
}
