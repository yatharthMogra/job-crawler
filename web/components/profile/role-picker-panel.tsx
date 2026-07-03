"use client"

import { useMemo, useState } from "react"
import {
  ROLE_CATEGORIES,
  rolesBySubcategory,
  rolesForDomain,
  type RoleDomainId,
} from "@/lib/profile/role-catalog"
import { cn } from "@/lib/utils"
import { Check, X } from "lucide-react"

interface RolePickerPanelProps {
  selected: string[]
  onChange: (roles: string[]) => void
  domainId: RoleDomainId
  exclude?: string[]
  title?: string
  subtitle?: string
}

export function RolePickerPanel({
  selected,
  onChange,
  domainId,
  exclude = [],
  title = "Core Specialties",
  subtitle = "Select from the catalog — exact titles power recommendation matching.",
}: RolePickerPanelProps) {
  const domainRoles = useMemo(() => rolesForDomain(domainId), [domainId])
  const categoriesInDomain = useMemo(
    () => ROLE_CATEGORIES.filter((cat) => domainRoles.some((r) => r.category === cat)),
    [domainRoles],
  )
  const [activeCategory, setActiveCategory] = useState(categoriesInDomain[0] ?? ROLE_CATEGORIES[0])

  const effectiveCategory = categoriesInDomain.includes(activeCategory)
    ? activeCategory
    : (categoriesInDomain[0] ?? ROLE_CATEGORIES[0])

  const subcategories = rolesBySubcategory(effectiveCategory)
  const domainRoleLabels = new Set(domainRoles.map((r) => r.label))

  function toggle(label: string) {
    if (exclude.includes(label)) return
    if (selected.includes(label)) {
      onChange(selected.filter((r) => r !== label))
    } else {
      onChange([...selected, label])
    }
  }

  return (
    <div className="rounded-2xl border border-border/80 bg-card shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)]">
      <div className="border-b border-border/60 px-5 py-4">
        <h2 className="text-sm font-bold text-foreground">{title}</h2>
        <p className="mt-0.5 text-xs text-muted-foreground">{subtitle}</p>
      </div>

      {selected.length > 0 ? (
        <div className="flex flex-wrap gap-2 border-b border-border/40 bg-primary/5 px-5 py-3">
          {selected.map((role) => (
            <span
              key={role}
              className="inline-flex items-center gap-1.5 rounded-full border border-primary bg-primary px-3 py-1 text-xs font-semibold text-primary-foreground"
            >
              <Check className="size-3" aria-hidden="true" />
              {role}
              <button
                type="button"
                aria-label={`Remove ${role}`}
                onClick={() => toggle(role)}
                className="rounded-full p-0.5 hover:bg-primary-foreground/20"
              >
                <X className="size-3" />
              </button>
            </span>
          ))}
        </div>
      ) : null}

      <div className="flex min-h-[280px] flex-col sm:flex-row">
        <div className="shrink-0 border-b border-border/60 sm:w-52 sm:border-b-0 sm:border-r">
          {categoriesInDomain.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setActiveCategory(cat)}
              className={cn(
                "w-full px-4 py-3 text-left text-sm transition-colors",
                effectiveCategory === cat
                  ? "bg-primary/5 font-semibold text-primary"
                  : "text-foreground hover:bg-muted/50",
              )}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="min-h-0 flex-1 overflow-y-auto p-4">
          {Object.entries(subcategories).map(([sub, roles]) => {
            const visible = roles.filter((r) => domainRoleLabels.has(r.label))
            if (visible.length === 0) return null

            return (
              <div key={sub} className="mb-5 last:mb-0">
                <p className="mb-2.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                  {sub}
                </p>
                <div className="flex flex-wrap gap-2">
                  {visible.map((role) => {
                    const isSelected = selected.includes(role.label)
                    const isExcluded = exclude.includes(role.label)

                    return (
                      <button
                        key={role.id}
                        type="button"
                        disabled={isExcluded}
                        onClick={() => toggle(role.label)}
                        className={cn(
                          "rounded-lg border px-3 py-2 text-sm font-medium transition-all duration-200",
                          isSelected
                            ? "border-primary bg-primary text-primary-foreground shadow-md shadow-primary/20"
                            : isExcluded
                              ? "cursor-not-allowed border-border/40 bg-muted/30 text-muted-foreground opacity-50"
                              : "border-border/80 bg-card text-foreground hover:border-primary/40 hover:shadow-sm",
                        )}
                      >
                        {role.label}
                      </button>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
