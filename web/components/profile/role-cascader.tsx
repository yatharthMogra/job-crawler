"use client"

import { useEffect, useLayoutEffect, useRef, useState } from "react"
import { createPortal } from "react-dom"
import { X } from "lucide-react"
import {
  ROLE_CATEGORIES,
  rolesBySubcategory,
  findRoleByLabel,
} from "@/lib/profile/role-catalog"
import { cn } from "@/lib/utils"

interface RoleCascaderProps {
  selected: string[]
  onChange: (roles: string[]) => void
  placeholder?: string
}

export function RoleCascader({
  selected,
  onChange,
  placeholder = "Select job functions",
}: RoleCascaderProps) {
  const [open, setOpen] = useState(false)
  const [activeCategory, setActiveCategory] = useState(ROLE_CATEGORIES[0] ?? "")
  const [panelStyle, setPanelStyle] = useState<{ top: number; left: number; width: number } | null>(
    null,
  )
  const triggerRef = useRef<HTMLDivElement>(null)
  const rolesScrollRef = useRef<HTMLDivElement>(null)

  function toggleRole(label: string) {
    if (selected.includes(label)) {
      onChange(selected.filter((r) => r !== label))
    } else {
      onChange([...selected, label])
    }
  }

  function removeRole(label: string) {
    onChange(selected.filter((r) => r !== label))
  }

  const subcategories = rolesBySubcategory(activeCategory)

  function updatePanelPosition() {
    const el = triggerRef.current
    if (!el) return
    const rect = el.getBoundingClientRect()
    const panelHeight = 320
    const gap = 4
    const spaceBelow = window.innerHeight - rect.bottom
    const openAbove = spaceBelow < panelHeight && rect.top > spaceBelow
    const top = openAbove ? rect.top - panelHeight - gap : rect.bottom + gap
    setPanelStyle({
      top: Math.max(8, top),
      left: rect.left,
      width: rect.width,
    })
  }

  useLayoutEffect(() => {
    if (!open) return
    updatePanelPosition()
    rolesScrollRef.current?.scrollTo({ top: 0 })
  }, [open, activeCategory])

  useEffect(() => {
    if (!open) return
    function onScrollOrResize() {
      updatePanelPosition()
    }
    window.addEventListener("resize", onScrollOrResize)
    window.addEventListener("scroll", onScrollOrResize, true)
    return () => {
      window.removeEventListener("resize", onScrollOrResize)
      window.removeEventListener("scroll", onScrollOrResize, true)
    }
  }, [open])

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false)
    }
    document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [open])

  const panel =
    open && panelStyle ? (
      <>
        <div className="fixed inset-0 z-[100]" onClick={() => setOpen(false)} aria-hidden="true" />
        <div
          className="fixed z-[101] flex rounded-lg border border-border bg-background shadow-xl"
          style={{
            top: panelStyle.top,
            left: panelStyle.left,
            width: panelStyle.width,
            maxHeight: "min(320px, calc(100vh - 16px))",
          }}
        >
          <div className="w-44 shrink-0 overflow-y-auto border-r border-border bg-muted/30 py-1 sm:w-48">
            {ROLE_CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                className={cn(
                  "w-full px-3 py-2 text-left text-sm transition-colors",
                  activeCategory === cat
                    ? "bg-zinc-100 font-medium text-zinc-900"
                    : "text-foreground hover:bg-muted",
                )}
                onClick={() => setActiveCategory(cat)}
              >
                {cat}
              </button>
            ))}
          </div>
          <div
            ref={rolesScrollRef}
            className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-3"
          >
            {Object.entries(subcategories).map(([sub, roles]) => (
              <div key={sub} className="mb-4 last:mb-0">
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  {sub}
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {roles.map((role) => {
                    const isSelected = selected.includes(role.label)
                    return (
                      <button
                        key={role.id}
                        type="button"
                        className={cn(
                          "rounded-md border px-2.5 py-1.5 text-xs transition-colors",
                          isSelected
                            ? "border-zinc-900 bg-zinc-100 font-medium text-zinc-900"
                            : "border-border bg-background text-foreground hover:bg-muted",
                        )}
                        onClick={() => toggleRole(role.label)}
                      >
                        {role.label}
                      </button>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </>
    ) : null

  return (
    <div className="relative">
      <div
        ref={triggerRef}
        className="flex min-h-10 cursor-text flex-wrap items-center gap-1.5 rounded-lg border border-border bg-background px-3 py-2"
        onClick={() => setOpen((v) => !v)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault()
            setOpen((v) => !v)
          }
        }}
        aria-expanded={open}
        aria-haspopup="listbox"
      >
        {selected.map((role) => (
          <span
            key={role}
            className="inline-flex items-center gap-1 rounded-md bg-zinc-100 px-2 py-0.5 text-xs font-medium text-zinc-800"
          >
            {role}
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation()
                removeRole(role)
              }}
              className="rounded hover:bg-zinc-200"
            >
              <X className="size-3" />
            </button>
          </span>
        ))}
        {selected.length === 0 ? (
          <span className="text-sm text-muted-foreground">{placeholder}</span>
        ) : null}
      </div>

      {typeof document !== "undefined" && panel ? createPortal(panel, document.body) : null}
    </div>
  )
}

export function poolIdsForSelectedRoles(
  labels: string[],
  suffix: "FULLTIME" | "INTERNSHIP" | "NEW_GRAD" = "FULLTIME",
): string[] {
  const pools = new Set<string>()
  for (const label of labels) {
    const entry = findRoleByLabel(label)
    if (entry) {
      pools.add(`${entry.poolBase}_${suffix}`)
      if (entry.poolBase !== "SWE") pools.add(`SWE_${suffix}`)
    }
  }
  return [...pools]
}
