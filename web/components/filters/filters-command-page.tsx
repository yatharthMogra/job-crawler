"use client"

import { useMemo, useState, type ReactNode } from "react"
import {
  Briefcase,
  Building2,
  Check,
  Code2,
  DollarSign,
  Plus,
  Search,
  TrendingUp,
  X,
} from "lucide-react"
import { RoleCascader, poolIdsForSelectedRoles } from "@/components/profile/role-cascader"
import { SalaryRangeControl } from "@/components/filters/salary-range-control"
import { FiltersMatchPanel } from "@/components/filters/filters-match-panel"
import { useJobs } from "@/components/jobs-provider"
import type { JobFiltersState } from "@/lib/profile/job-filters"
import {
  DEFAULT_SALARY_MAX,
  DEFAULT_SALARY_MIN,
  EXPERIENCE_TIERS,
  INDUSTRY_SUGGESTIONS,
  TECH_STACK_OPTIONS,
  WORK_ARRANGEMENTS,
} from "@/lib/filters/filter-options"
import {
  estimateProfileAlignment,
  filterJobsByState,
} from "@/lib/filters/match-estimate"
import { cn } from "@/lib/utils"

function FilterCard({
  icon,
  title,
  subtitle,
  children,
  className,
}: {
  icon: ReactNode
  title: string
  subtitle?: string
  children: ReactNode
  className?: string
}) {
  return (
    <section
      className={cn(
        "rounded-2xl border border-border/60 bg-card p-5 shadow-sm sm:p-6",
        className,
      )}
    >
      <div className="mb-5 flex items-start gap-3">
        <div className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
          {icon}
        </div>
        <div>
          <h3 className="text-base font-bold text-foreground">{title}</h3>
          {subtitle ? (
            <p className="mt-0.5 text-xs text-muted-foreground">{subtitle}</p>
          ) : null}
        </div>
      </div>
      {children}
    </section>
  )
}

interface FiltersCommandPageProps {
  state: JobFiltersState
  candidateName: string
  saving: boolean
  onChange: (next: JobFiltersState) => void
  onReset: () => void
  onConfirm: () => void
}

export function FiltersCommandPage({
  state,
  candidateName,
  saving,
  onChange,
  onReset,
  onConfirm,
}: FiltersCommandPageProps) {
  const { recommendedJobs, allKnownJobs } = useJobs()
  const [salaryMax, setSalaryMax] = useState(DEFAULT_SALARY_MAX)
  const [industryQuery, setIndustryQuery] = useState("")
  const [showMoreTech, setShowMoreTech] = useState(false)

  const salaryMin = state.openToAllSalary
    ? DEFAULT_SALARY_MIN
    : Number(state.minimumSalary || DEFAULT_SALARY_MIN)

  const jobsPool = recommendedJobs.length > 0 ? recommendedJobs : allKnownJobs

  const matchedJobs = useMemo(
    () => filterJobsByState(jobsPool, state, salaryMax),
    [jobsPool, state, salaryMax],
  )

  const matchCount = useMemo(() => {
    if (jobsPool.length === 0) return 1284
    if (matchedJobs.length === 0) return 0
    const ratio = matchedJobs.length / jobsPool.length
    const marketEstimate = Math.round(ratio * 2100)
    return Math.max(matchedJobs.length, marketEstimate)
  }, [jobsPool.length, matchedJobs.length])
  const alignmentScore = estimateProfileAlignment(matchedJobs)

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

  function toggleWorkArrangement(id: string) {
    const arrangement = WORK_ARRANGEMENTS.find((item) => item.id === id)
    if (!arrangement) return
    const isActive = arrangement.models.every((model) => state.workModels.includes(model))
    let next = [...state.workModels]
    if (isActive) {
      next = next.filter((model) => !arrangement.models.includes(model))
    } else {
      next = [...new Set([...next, ...arrangement.models])]
    }
    update("workModels", next)
  }

  function isWorkArrangementActive(id: string): boolean {
    const arrangement = WORK_ARRANGEMENTS.find((item) => item.id === id)
    if (!arrangement) return false
    return arrangement.models.some((model) => state.workModels.includes(model))
  }

  function addIndustry(value: string) {
    const trimmed = value.trim()
    if (!trimmed || state.preferredIndustries.includes(trimmed)) return
    update("preferredIndustries", [...state.preferredIndustries, trimmed])
    setIndustryQuery("")
  }

  function removeIndustry(value: string) {
    update(
      "preferredIndustries",
      state.preferredIndustries.filter((item) => item !== value),
    )
  }

  function toggleSkill(skill: string) {
    const next = state.preferredSkills.includes(skill)
      ? state.preferredSkills.filter((item) => item !== skill)
      : state.preferredSkills.length >= 10
        ? state.preferredSkills
        : [...state.preferredSkills, skill]
    update("preferredSkills", next)
  }

  const visibleTech = showMoreTech ? TECH_STACK_OPTIONS : TECH_STACK_OPTIONS.slice(0, 6)
  const filteredSuggestions = INDUSTRY_SUGGESTIONS.filter(
    (item) =>
      item.toLowerCase().includes(industryQuery.toLowerCase()) &&
      !state.preferredIndustries.includes(item),
  )

  return (
    <div className="min-h-full bg-muted/20">
      <div className="mx-auto flex max-w-[1280px] flex-col gap-8 px-6 py-8 xl:flex-row xl:items-start">
        <div className="min-w-0 flex-1">
          <div className="mb-8 flex flex-wrap items-start justify-between gap-4">
            <div>
              <div className="flex flex-wrap items-center gap-3">
                <h1 className="text-3xl font-bold tracking-tight text-foreground">
                  Advanced search
                </h1>
                <span className="rounded-full bg-primary/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-primary">
                  Beta engine
                </span>
              </div>
              <p className="mt-2 max-w-xl text-sm text-muted-foreground">
                Tune compensation, work style, and stack preferences — match counts update as you
                refine criteria.
              </p>
            </div>
            <button
              type="button"
              onClick={onReset}
              className="text-sm font-semibold text-primary transition-colors hover:text-primary/80"
            >
              Reset all
            </button>
          </div>

          <FilterCard
            icon={<Briefcase className="size-5" />}
            title="Target roles"
            subtitle="Primary job functions used for recommendations"
            className="mb-5"
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
          </FilterCard>

          <div className="grid gap-5 lg:grid-cols-2">
            <FilterCard
              icon={<DollarSign className="size-5" />}
              title="Annual compensation"
              subtitle="Set your target salary band"
            >
              <SalaryRangeControl
                min={salaryMin}
                max={salaryMax}
                onChange={setSalaryRange}
              />
            </FilterCard>

            <FilterCard
              icon={<Building2 className="size-5" />}
              title="Work arrangement"
              subtitle="Where you want to work"
            >
              <div className="space-y-3">
                {WORK_ARRANGEMENTS.map((item) => {
                  const active = isWorkArrangementActive(item.id)
                  return (
                    <button
                      key={item.id}
                      type="button"
                      onClick={() => toggleWorkArrangement(item.id)}
                      className={cn(
                        "flex w-full items-start gap-3 rounded-xl border px-4 py-3.5 text-left transition-all",
                        active
                          ? "border-primary bg-primary/5 shadow-sm"
                          : "border-border/70 bg-muted/20 hover:border-primary/30 hover:bg-muted/40",
                      )}
                    >
                      <span
                        className={cn(
                          "mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-md border",
                          active
                            ? "border-primary bg-primary text-primary-foreground"
                            : "border-border bg-card",
                        )}
                      >
                        {active ? <Check className="size-3.5" strokeWidth={3} /> : null}
                      </span>
                      <span>
                        <span className="block text-sm font-semibold text-foreground">
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
              icon={<TrendingUp className="size-5" />}
              title="Experience level"
              subtitle="Seniority bands you are targeting"
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
                        "rounded-xl border px-4 py-3 text-left text-sm font-semibold transition-all",
                        active
                          ? "border-primary bg-primary/5 text-primary shadow-sm"
                          : "border-border/70 bg-muted/20 text-foreground/80 hover:border-primary/30",
                      )}
                    >
                      {tier.label}
                    </button>
                  )
                })}
              </div>
            </FilterCard>

            <FilterCard
              icon={<Search className="size-5" />}
              title="Target industry"
              subtitle="Focus on sectors that fit your background"
            >
              <div className="relative">
                <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  type="text"
                  value={industryQuery}
                  onChange={(e) => setIndustryQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault()
                      addIndustry(industryQuery)
                    }
                  }}
                  placeholder="Search industries..."
                  className="w-full rounded-xl border border-border/70 bg-muted/20 py-2.5 pl-10 pr-3 text-sm outline-none transition-colors focus:border-primary/40 focus:bg-card"
                />
              </div>

              {filteredSuggestions.length > 0 && industryQuery ? (
                <div className="mt-2 flex flex-wrap gap-2">
                  {filteredSuggestions.slice(0, 4).map((item) => (
                    <button
                      key={item}
                      type="button"
                      onClick={() => addIndustry(item)}
                      className="rounded-full border border-dashed border-primary/30 px-3 py-1 text-xs font-semibold text-primary hover:bg-primary/5"
                    >
                      + {item}
                    </button>
                  ))}
                </div>
              ) : null}

              <div className="mt-4 flex flex-wrap gap-2">
                {state.preferredIndustries.map((item) => (
                  <span
                    key={item}
                    className="inline-flex items-center gap-1.5 rounded-full bg-slate-900 px-3 py-1.5 text-sm font-semibold text-white"
                  >
                    {item}
                    <button
                      type="button"
                      onClick={() => removeIndustry(item)}
                      className="rounded-full p-0.5 hover:bg-white/15"
                      aria-label={`Remove ${item}`}
                    >
                      <X className="size-3.5" />
                    </button>
                  </span>
                ))}
              </div>
            </FilterCard>
          </div>

          <FilterCard
            icon={<Code2 className="size-5" />}
            title="Tech stack preferences"
            subtitle="Select up to 10 technologies"
            className="mt-5"
          >
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {visibleTech.map((item) => {
                const active = state.preferredSkills.includes(item.id)
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => toggleSkill(item.id)}
                    className={cn(
                      "flex items-center justify-between rounded-xl border px-4 py-3 text-left transition-all",
                      active
                        ? "border-primary bg-primary/5 shadow-sm"
                        : "border-border/70 bg-muted/20 hover:border-primary/30",
                    )}
                  >
                    <span className="text-sm font-semibold text-foreground">{item.label}</span>
                    {active ? (
                      <span className="flex size-5 items-center justify-center rounded-full bg-primary text-primary-foreground">
                        <Check className="size-3" strokeWidth={3} />
                      </span>
                    ) : null}
                  </button>
                )
              })}
              {!showMoreTech ? (
                <button
                  type="button"
                  onClick={() => setShowMoreTech(true)}
                  className="flex items-center justify-center gap-2 rounded-xl border border-dashed border-primary/30 px-4 py-3 text-sm font-semibold text-primary transition-colors hover:bg-primary/5"
                >
                  <Plus className="size-4" />
                  Add more
                </button>
              ) : null}
            </div>
          </FilterCard>
        </div>

        <FiltersMatchPanel
          matchCount={matchCount}
          alignmentScore={alignmentScore}
          candidateName={candidateName}
          saving={saving}
          onViewMatches={onConfirm}
          className="xl:sticky xl:top-8"
        />
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
    openToAllSalary: false,
    minimumSalary: base.minimumSalary || String(DEFAULT_SALARY_MIN),
    workModels: base.workModels.length > 0 ? base.workModels : ["Remote"],
    experienceLevels:
      base.experienceLevels.length > 0 ? base.experienceLevels : ["Lead/Staff"],
    preferredIndustries:
      base.preferredIndustries.length > 0
        ? base.preferredIndustries
        : ["FinTech", "SaaS", "AI/ML"],
    preferredSkills:
      base.preferredSkills.length > 0 ? base.preferredSkills : ["Python"],
  }
}
