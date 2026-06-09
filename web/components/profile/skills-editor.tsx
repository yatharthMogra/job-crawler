"use client"

import { useState } from "react"
import { Plus, X } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface SkillsEditorProps {
  skills: { category: string; names: string[] }[]
  onChange?: (skills: { category: string; names: string[] }[]) => void
  readOnly?: boolean
}

export function SkillsEditor({ skills, onChange, readOnly = true }: SkillsEditorProps) {
  const [local, setLocal] = useState(skills)
  const [newSkill, setNewSkill] = useState("")
  const allNames = local.flatMap((g) => g.names)

  function removeSkill(name: string) {
    if (readOnly || !onChange) return
    const next = local
      .map((g) => ({ ...g, names: g.names.filter((n) => n !== name) }))
      .filter((g) => g.names.length > 0)
    setLocal(next)
    onChange(next)
  }

  function addSkill() {
    if (readOnly || !onChange || !newSkill.trim()) return
    const name = newSkill.trim()
    const next = [...local]
    const other = next.find((g) => g.category === "Other")
    if (other) {
      other.names.push(name)
    } else {
      next.push({ category: "Other", names: [name] })
    }
    setLocal(next)
    onChange(next)
    setNewSkill("")
  }

  if (allNames.length === 0 && readOnly) {
    return <p className="text-sm text-muted-foreground">No skills on your profile yet.</p>
  }

  return (
    <div>
      <div className="flex flex-wrap gap-2">
        {allNames.map((name) => (
          <span
            key={name}
            className="inline-flex items-center gap-1 rounded-md bg-accent px-2.5 py-1 text-sm text-accent-foreground"
          >
            {name}
            {!readOnly && onChange ? (
              <button type="button" onClick={() => removeSkill(name)} className="rounded hover:bg-primary/10">
                <X className="size-3" />
              </button>
            ) : null}
          </span>
        ))}
      </div>
      {!readOnly && onChange ? (
        <div className="mt-4 flex gap-2">
          <Input
            value={newSkill}
            onChange={(e) => setNewSkill(e.target.value)}
            placeholder="Add a skill"
            className="max-w-xs"
            onKeyDown={(e) => e.key === "Enter" && addSkill()}
          />
          <Button size="sm" variant="secondary" onClick={addSkill}>
            <Plus className="size-4" />
            Add
          </Button>
        </div>
      ) : null}
    </div>
  )
}
