"use client"

import { useEffect, useRef, useState } from "react"
import { ChevronDown, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface FilterDropdownProps {
  label: string
  value: string | null
  options: { value: string; label: string }[]
  onSelect: (value: string) => void
  onClear: () => void
}

export function FilterDropdown({ label, value, options, onSelect, onClear }: FilterDropdownProps) {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", onDoc)
    return () => document.removeEventListener("mousedown", onDoc)
  }, [])

  const activeOption = options.find((o) => o.value === value)
  const isActive = value != null

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className={cn(
          "inline-flex h-8 items-center gap-1.5 rounded-lg border px-2.5 text-xs font-medium transition-colors",
          isActive
            ? "border-primary/40 bg-accent text-accent-foreground shadow-sm"
            : "border-border bg-card text-muted-foreground hover:border-primary/25 hover:text-foreground",
        )}
      >
        {isActive ? activeOption?.label ?? value : label}
        {isActive ? (
          <span
            role="button"
            tabIndex={0}
            aria-label={`Clear ${label} filter`}
            onClick={(e) => {
              e.stopPropagation()
              onClear()
              setOpen(false)
            }}
            className="-mr-1 rounded p-0.5 text-muted-foreground hover:bg-primary/10 hover:text-foreground"
          >
            <X className="size-3" />
          </span>
        ) : (
          <ChevronDown className="size-3 text-muted-foreground" />
        )}
      </button>

      {open && (
        <div className="absolute left-0 top-9 z-40 min-w-[180px] overflow-hidden rounded-xl border border-border/80 bg-card py-1 shadow-lg shadow-primary/5">
          {options.map((opt) => (
            <button
              key={opt.value}
              type="button"
              onClick={() => {
                onSelect(opt.value)
                setOpen(false)
              }}
              className={cn(
                "block w-full px-3 py-1.5 text-left text-xs transition-colors hover:bg-secondary/80",
                value === opt.value ? "font-medium text-primary" : "text-muted-foreground",
              )}
            >
              {opt.label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

interface SalaryDropdownProps {
  value: number | null
  onSelect: (value: number) => void
  onClear: () => void
}

export function SalaryDropdown({ value, onSelect, onClear }: SalaryDropdownProps) {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState("")
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", onDoc)
    return () => document.removeEventListener("mousedown", onDoc)
  }, [])

  const isActive = value != null

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className={cn(
          "inline-flex h-8 items-center gap-1.5 rounded-lg border px-2.5 text-xs font-medium transition-colors",
          isActive
            ? "border-primary/40 bg-accent text-accent-foreground shadow-sm"
            : "border-border bg-card text-muted-foreground hover:border-primary/25 hover:text-foreground",
        )}
      >
        {isActive ? `Min $${Math.round((value as number) / 1000)}k` : "Compensation"}
        {isActive ? (
          <span
            role="button"
            tabIndex={0}
            aria-label="Clear compensation filter"
            onClick={(e) => {
              e.stopPropagation()
              onClear()
              setInput("")
              setOpen(false)
            }}
            className="-mr-1 rounded p-0.5 text-muted-foreground hover:bg-primary/10 hover:text-foreground"
          >
            <X className="size-3" />
          </span>
        ) : (
          <ChevronDown className="size-3 text-muted-foreground" />
        )}
      </button>

      {open && (
        <div className="absolute left-0 top-9 z-40 w-[220px] rounded-xl border border-border/80 bg-card p-3 shadow-lg shadow-primary/5">
          <label className="mb-1.5 block text-xs font-medium text-foreground">Minimum salary</label>
          <div className="flex items-center gap-2">
            <div className="flex h-8 flex-1 items-center rounded-lg border border-border px-2">
              <span className="text-xs text-muted-foreground">$</span>
              <input
                type="number"
                value={input}
                placeholder="120000"
                onChange={(e) => setInput(e.target.value)}
                className="w-full bg-transparent px-1 text-xs text-foreground outline-none"
              />
            </div>
            <button
              type="button"
              onClick={() => {
                const n = Number(input)
                if (n > 0) onSelect(n)
                setOpen(false)
              }}
              className="btn-brand h-8 rounded-lg px-2.5 text-xs font-medium"
            >
              Set
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
