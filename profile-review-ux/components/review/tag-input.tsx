"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { X } from "lucide-react"

interface TagInputProps {
  label: string
  tags: string[]
  onChange: (tags: string[]) => void
}

export function TagInput({ label, tags, onChange }: TagInputProps) {
  const [draft, setDraft] = useState("")

  function add() {
    const t = draft.trim()
    if (t && !tags.includes(t)) onChange([...tags, t])
    setDraft("")
  }

  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium text-muted-foreground">{label}</label>
      <div className="flex flex-wrap gap-1.5 rounded-lg border border-input bg-background p-2">
        {tags.map((t) => (
          <span
            key={t}
            className="inline-flex items-center gap-1 rounded-md bg-secondary px-2 py-0.5 text-xs text-secondary-foreground"
          >
            {t}
            <button
              type="button"
              aria-label={`Remove ${t}`}
              onClick={() => onChange(tags.filter((x) => x !== t))}
              className="text-muted-foreground hover:text-foreground"
            >
              <X className="size-3" aria-hidden="true" />
            </button>
          </span>
        ))}
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault()
              add()
            }
          }}
          onBlur={add}
          placeholder="Add..."
          className="min-w-20 flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
        />
      </div>
    </div>
  )
}

export { Input }
