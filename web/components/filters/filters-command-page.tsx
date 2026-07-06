"use client"

import { useState, type ReactNode } from "react"
import { Check } from "lucide-react"
import { RoleCascader, poolIdsForSelectedRoles } from "@/components/profile/role-cascader"
import { SalaryRangeControl } from "@/components/filters/salary-range-control"
import type { JobFiltersState } from "@/lib/profile/job-filters"
import {
  DEFAULT_SALARY_MAX,
  DEFAULT_SALARY_MIN,
  EXPERIENCE_TIERS,
  WORK_ARRANGEMENTS,
} from "@/lib/filters/filter-options"
import { cn } from "@/lib/utils"

function FilterCard({
  title,
  subtitle,
  children,
  className,
}: {
  title: string
  subtitle?: string
  children: ReactNode
  className?: string
}) {
  return (
    <section
      className={cn(
        "rounded-xl border border-border/70 bg-card p-5",
        className,
      )}
    >
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-foreground">{title}</h3>
        {subtitle ? (
          <p className="mt-0.5 text-xs text-muted-foreground">{subtitle}</p>
        ) : null}
      </div>
      {children}
    </section>
  )
}

interface FiltersCommandPageProps {
  state: JobFiltersState
  onChange: (next: JobFiltersState) => void
  onReset: () => void
}

export function FiltersCommandPage({
  state,
  onChange,
  onReset,
}: FiltersCommandPageProps) {
  const [salaryMax, setSalaryMax] = useState(DEFAULT_SALARY_MAX)

  const salaryMin = state.openToAllSalary
    ? DEFAULT_SALARY_MIN
    : Number(state.minimumSalary || DEFAULT_SALARY_MIN)

  function update<K extends keyof JobFiltersState>(key: K, value: JobFiltersState[K]) {
    onChange({ ...state, [key]: value })
  }

  function setSalaryRange(next: { min: number; max: number }) {
    setSalaryMax(next.max)
    update("openToAllSalary", false)
    update("minimumSalary", String(next.min))
  }

  function toggleExperienceTier(tierId: string) {
    const tier = EXPERIENCE_TIERS.find((item) => item.id === tierId)
    if (!tier) return
    const isActive = tier.levels.every((level) => state.experienceLevels.includes(level))
    const next = isActive
      ? state.experienceLevels.filter((level) => !tier.levels.includes(level))
      : [...new Set([...state.experienceLevels, ...tier.levels])]
    update("experienceLevels", next)
  }

  function isTierActive(tierId: string): boolean {
    const tier = EXPERIENCE_TIERS.find((item) => item.id === tierId)
    if (!tier) return false
    return tier.levels.some((level) => state.experienceLevels.includes(level))
  }

  function selectWorkArrangement(id: string) {
    if (id === "any") {
      update("workModels", [])
      return
    }
    const arrangement = WORK_ARRANGEMENTS.find((item) => item.id === id)
    if (!arrangement) return
    const isActive = arrangement.models.every((model) => state.workModels.includes(model))
    if (isActive) {
      update(
        "workModels",
        state.workModels.filter((model) => !arrangement.models.includes(model)),
      )
    } else {
      update("workModels", [...new Set([...state.workModels, ...arrangement.models])])
    }
  }

  function isWorkArrangementActive(id: string): boolean {
    if (id === "any") return state.workModels.length === 0
    const arrangement = WORK_ARRANGEMENTS.find((item) => item.id === id)
    if (!arrangement) return false
    return arrangement.models.some((model) => state.workModels.includes(model))
  }

  return (
    <div className="min-h-full bg-muted/30">
      <div className="mx-auto max-w-[820px] space-y-5 px-5 py-6">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h1 className="text-xl font-bold text-foreground">Job search filters</h1>
              <p className="mt-1 text-sm text-muted-foreground">
                Refine roles, compensation, and work preferences. Results update as you change
                filters.
              </p>
            </div>
            <button
              type="button"
              onClick={onReset}
              className="text-sm font-medium text-primary hover:text-primary/80"
            >
              Reset all
            </button>
          </div>

          <FilterCard
            title="Target roles"
            subtitle="Job functions used for recommendations"
          >
            <RoleCascader
              selected={state.primaryRoles}
              onChange={(roles) => {
                const suffix =
                  state.internshipOnly && !state.fulltimeOnly ? "INTERNSHIP" : "FULLTIME"
                onChange({
                  ...state,
                  primaryRoles: roles,
                  rolePoolIds: poolIdsForSelectedRoles(roles, suffix),
                })
              }}
              placeholder="Select target roles"
            />
            <div className="mt-3 flex flex-wrap gap-2">
              {[
                { key: "fulltimeOnly" as const, label: "Full-time" },
                { key: "internshipOnly" as const, label: "Internship" },
              ].map(({ key, label }) => {
                const active = state[key]
                return (
                  <button
                    key={key}
                    type="button"
                    onClick={() => update(key, !active)}
                    className={cn(
                      "rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors",
                      active
                        ? "border-primary bg-primary/10 text-primary"
                        : "border-border text-muted-foreground hover:border-primary/40",
                    )}
                  >
                    {label}
                  </button>
                )
              })}
            </div>
          </FilterCard>

          <FilterCard title="Compensation & eligibility">
            <div className="space-y-5">
              <div>
                <div className="mb-3 flex items-center justify-between gap-3">
                  <p className="text-sm font-medium text-foreground">Minimum annual salary</p>
                  <label className="flex cursor-pointer items-center gap-2 text-xs text-muted-foreground">
                    <span>Open to all</span>
                    <input
                      type="checkbox"
                      checked={state.openToAllSalary}
                      onChange={(e) => update("openToAllSalary", e.target.checked)}
                      className="size-4 rounded border-border accent-primary"
                    />
                  </label>
                </div>
                {!state.openToAllSalary ? (
                  <SalaryRangeControl
                    min={salaryMin}
                    max={salaryMax}
                    onChange={setSalaryRange}
                  />
                ) : (
                  <p className="text-sm text-muted-foreground">Any salary range</p>
                )}
              </div>

              <div className="border-t border-border/60 pt-5">
                <label className="flex cursor-pointer items-start gap-3 rounded-lg border border-border/70 px-4 py-3">
                  <input
                    type="checkbox"
                    checked={state.sponsorshipRequired}
                    onChange={(e) => update("sponsorshipRequired", e.target.checked)}
                    className="mt-0.5 size-4 shrink-0 rounded border-border accent-primary"
                  />
                  <span>
                    <span className="block text-sm font-medium text-foreground">
                      Exclude jobs with restricted eligibility
                    </span>
                    <span className="mt-1 block text-xs leading-relaxed text-muted-foreground">
                      Hide postings that explicitly require security clearance, US citizenship, or
                      state they will not sponsor visas. We do not filter on H-1B history — only
                      what is clearly stated in the job description.
                    </span>
                  </span>
                </label>
              </div>
            </div>
          </FilterCard>

          <div className="grid gap-5 lg:grid-cols-2">
            <FilterCard
              title="Work arrangement"
              subtitle="Where you prefer to work"
            >
              <div className="space-y-2">
                {WORK_ARRANGEMENTS.map((item) => {
                  const active = isWorkArrangementActive(item.id)
                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => selectWorkArrangement(item.id)}
                      className={cn(
                        "flex w-full items-start gap-3 rounded-lg border px-3 py-3 text-left transition-colors",
                        active
                          ? "border-primary/50 bg-primary/5"
                          : "border-border/70 hover:border-primary/30",
                      )}
                    >
                      <span
                        className={cn(
                          "mt-0.5 flex size-4 shrink-0 items-center justify-center rounded border",
                          active
                            ? "border-primary bg-primary text-primary-foreground"
                            : "border-border bg-background",
                        )}
                      >
                        {active ? <Check className="size-2.5" strokeWidth={3} /> : null}
                      </span>
                      <span>
                        <span className="block text-sm font-medium text-foreground">
                          {item.label}
                        </span>
                        <span className="mt-0.5 block text-xs text-muted-foreground">
                          {item.description}
                        </span>
                      </span>
                    </button>
                  )
                })}
              </div>
            </FilterCard>

            <FilterCard
              title="Experience level"
              subtitle="Seniority you are targeting"
            >
              <div className="flex flex-col gap-2">
                {EXPERIENCE_TIERS.map((tier) => {
                  const active = isTierActive(tier.id)
                  return (
                    <button
                      key={tier.id}
                      type="button"
                      onClick={() => toggleExperienceTier(tier.id)}
                      className={cn(
                        "rounded-lg border px-3 py-2.5 text-left text-sm font-medium transition-colors",
                        active
                          ? "border-primary/50 bg-primary/5 text-primary"
                          : "border-border/70 text-foreground hover:border-primary/30",
                      )}
                    >
                      {tier.label}
                    </button>
                  )
                })}
              </div>
            </FilterCard>
          </div>
      </div>
    </div>
  )
}

export function buildDefaultFiltersState(
  base: JobFiltersState,
  profileRoles: string[],
): JobFiltersState {
  const suffix = base.internshipOnly && !base.fulltimeOnly ? "INTERNSHIP" : "FULLTIME"
  const primaryRoles =
    base.primaryRoles.length > 0
      ? base.primaryRoles
      : profileRoles.length > 0
        ? profileRoles
        : ["Backend Engineer"]

  return {
    ...base,
    primaryRoles,
    rolePoolIds:
      base.rolePoolIds.length > 0
        ? base.rolePoolIds
        : poolIdsForSelectedRoles(primaryRoles, suffix),
    openToAllSalary: base.openToAllSalary,
    minimumSalary: base.minimumSalary || String(DEFAULT_SALARY_MIN),
    workModels: base.workModels,
    experienceLevels: base.experienceLevels,
    preferredIndustries: [],
    preferredSkills: [],
    sponsorshipRequired: base.sponsorshipRequired,
  }
}
