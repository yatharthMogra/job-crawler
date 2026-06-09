"use client"

import { EEO_FIELDS, formatEeoValue, type EeoState } from "@/lib/profile/eeo"

interface EeoFormProps {
  state: EeoState
  onChange: (state: EeoState) => void
  compact?: boolean
}

export function EeoForm({ state, onChange, compact = false }: EeoFormProps) {
  function update<K extends keyof EeoState>(key: K, value: EeoState[K]) {
    onChange({ ...state, [key]: value })
  }

  return (
    <div className={compact ? "space-y-4" : "space-y-5"}>
      {EEO_FIELDS.map((field) => (
        <div
          key={field.key}
          className={compact ? "space-y-1.5" : "grid gap-2 sm:grid-cols-[1fr_220px] sm:items-center sm:gap-4"}
        >
          <p className="text-sm text-foreground">{field.label}</p>
          {field.type === "yesno" ? (
            <select
              className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm"
              value={
                state[field.key] === null
                  ? ""
                  : state[field.key]
                    ? "true"
                    : "false"
              }
              onChange={(e) => {
                const val = e.target.value
                update(
                  field.key,
                  val === "" ? null : val === "true",
                )
              }}
            >
              <option value="">Select</option>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          ) : (
            <select
              className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm"
              value={String(state[field.key] ?? "")}
              onChange={(e) => update(field.key, e.target.value)}
            >
              <option value="">Select</option>
              {field.options?.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          )}
        </div>
      ))}
    </div>
  )
}

export function EeoDisplay({ state }: { state: EeoState }) {
  return (
    <dl className="space-y-4">
      {EEO_FIELDS.map((field) => {
        const value = formatEeoValue(field.key, state[field.key])
        if (value === "—") return null
        return (
          <div
            key={field.key}
            className="grid gap-2 sm:grid-cols-[1fr_auto] sm:items-center sm:gap-6"
          >
            <dt className="text-sm text-foreground">{field.label}</dt>
            <dd>
              <span className="inline-flex rounded-md bg-secondary px-3 py-1.5 text-sm font-medium text-secondary-foreground">
                {value}
              </span>
            </dd>
          </div>
        )
      })}
    </dl>
  )
}
