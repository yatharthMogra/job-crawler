"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import type { JobIntentState } from "@/lib/profile/job-intent"
import {
  isCatalogRole,
  ROLE_DOMAIN_GROUPS,
  rolesForDomain,
  sanitizeCatalogRoles,
  type RoleDomainId,
} from "@/lib/profile/role-catalog"
import { Brand } from "@/components/profile/brand"
import { RolePickerPanel } from "@/components/profile/role-picker-panel"
import { Button } from "@/components/ui/button"
import {
  DEFAULT_LOCATION,
  EXPERIENCE_LEVEL_OPTIONS,
  ensureLocations,
} from "@/lib/job-filters"
import type { SeniorityLevel } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"
import {
  Bell,
  Brain,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  X,
  Zap,
} from "lucide-react"

interface JobIntentScreenProps {
  state: JobIntentState
  onChange: (state: JobIntentState) => void
  onSubmit: () => void | Promise<void>
  saving?: boolean
}

const ROLE_SUGGESTIONS: Record<string, string> = {
  "Backend Engineer": "Principal Software Architect — deep infra & API leadership fit",
  "Full Stack Engineer": "Staff Full Stack Engineer — end-to-end product velocity",
  "Software Engineer": "Senior Software Engineer — broad SWE trajectory alignment",
  "DevOps Engineer": "Head of Platform Engineering — reliability & scale focus",
  "Machine Learning Engineer": "Principal ML Engineer — model systems at scale",
  "Data Scientist": "Lead Data Scientist — experimentation & insight leadership",
  "Product Manager": "Senior Product Manager — 0→1 product ownership",
}

function confidenceScore(primaryCount: number): number {
  return Math.min(98, 72 + primaryCount * 8)
}

export function JobIntentScreen({ state, onChange, onSubmit, saving }: JobIntentScreenProps) {
  const [error, setError] = useState<string | null>(null)
  const [domainIndex, setDomainIndex] = useState(0)
  const [progress, setProgress] = useState(0)
  const [showSecondaryPicker, setShowSecondaryPicker] = useState(false)

  const activeDomain = ROLE_DOMAIN_GROUPS[domainIndex] ?? ROLE_DOMAIN_GROUPS[0]
  const primaryRoles = sanitizeCatalogRoles(state.primaryRoles)
  const secondaryRoles = sanitizeCatalogRoles(state.secondaryRoles)
  const canContinue = primaryRoles.length > 0

  useEffect(() => {
    const t = window.setTimeout(() => setProgress(100), 400)
    return () => window.clearTimeout(t)
  }, [])

  function update<K extends keyof JobIntentState>(key: K, value: JobIntentState[K]) {
    onChange({ ...state, [key]: value })
    if (key === "primaryRoles" || key === "secondaryRoles") setError(null)
  }

  function setPrimaryRoles(roles: string[]) {
    const clean = sanitizeCatalogRoles(roles)
    const secondary = secondaryRoles.filter((r) => !clean.includes(r))
    update("primaryRoles", clean)
    if (secondary.length !== secondaryRoles.length) {
      update("secondaryRoles", secondary)
    }
  }

  function setSecondaryRoles(roles: string[]) {
    const clean = sanitizeCatalogRoles(roles).filter((r) => !primaryRoles.includes(r))
    update("secondaryRoles", clean)
  }

  function toggleSecondary(role: string) {
    if (!isCatalogRole(role) || primaryRoles.includes(role)) return
    if (secondaryRoles.includes(role)) {
      setSecondaryRoles(secondaryRoles.filter((r) => r !== role))
    } else {
      setSecondaryRoles([...secondaryRoles, role])
    }
  }

  async function handleSubmit() {
    const invalidPrimary = state.primaryRoles.filter((r) => !isCatalogRole(r))
    if (!canContinue || invalidPrimary.length > 0) {
      setError("Select at least one primary role from the catalog.")
      return
    }
    setError(null)
    await onSubmit()
  }

  const suggestions = useMemo(() => {
    return primaryRoles
      .slice(0, 2)
      .map((role) => ({
        role,
        blurb: ROLE_SUGGESTIONS[role] ?? `${role} — high alignment with your extracted profile`,
      }))
  }, [primaryRoles])

  const techFit = Math.min(99, 80 + primaryRoles.length * 4)
  const expMatch = Math.min(95, 75 + secondaryRoles.length * 6)

  return (
    <div className="landing-hero-bg relative min-h-screen pb-28">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-32 top-1/4 size-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute -right-24 bottom-1/4 size-80 rounded-full bg-primary/8 blur-3xl" />
      </div>

      <header className="relative z-20 border-b border-border/40 bg-card/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4">
          <Link href="/">
            <Brand />
          </Link>
          <div className="hidden flex-1 flex-col items-center sm:flex">
            <div className="flex items-center gap-3">
              <span className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                Step 4 of 4
              </span>
              <span className="text-[10px] font-bold uppercase tracking-widest text-primary">
                Neural Role Alignment
              </span>
            </div>
            <div className="mt-1.5 h-1.5 w-48 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-primary transition-all duration-700 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              type="button"
              className="rounded-full p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              aria-label="Notifications"
            >
              <Bell className="size-4" />
            </button>
            <span className="flex size-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
              JD
            </span>
          </div>
        </div>
      </header>

      <div className="relative z-10 mx-auto max-w-7xl px-6 py-8">
        <div className="animate-fade-in-up opacity-0" style={{ animationFillMode: "forwards" }}>
          <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Define your{" "}
            <span className="script-accent text-4xl font-semibold italic sm:text-5xl">
              Executive Path
            </span>
          </h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground sm:text-base">
            Select exact role titles from our neural catalog. Recommendations map precisely to your
            choices — no free-text ambiguity.
          </p>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="space-y-6">
            {/* Domain carousel */}
            <div
              className="animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}
            >
              <div className="mb-3 flex items-center justify-between">
                <p className="text-xs font-bold uppercase tracking-widest text-muted-foreground">
                  Neural Role Domains
                </p>
                <div className="flex gap-1">
                  <button
                    type="button"
                    onClick={() => setDomainIndex((i) => Math.max(0, i - 1))}
                    disabled={domainIndex === 0}
                    className="rounded-lg border border-border/60 p-1.5 text-muted-foreground transition-colors hover:bg-card disabled:opacity-40"
                    aria-label="Previous domain"
                  >
                    <ChevronLeft className="size-4" />
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      setDomainIndex((i) => Math.min(ROLE_DOMAIN_GROUPS.length - 1, i + 1))
                    }
                    disabled={domainIndex === ROLE_DOMAIN_GROUPS.length - 1}
                    className="rounded-lg border border-border/60 p-1.5 text-muted-foreground transition-colors hover:bg-card disabled:opacity-40"
                    aria-label="Next domain"
                  >
                    <ChevronRight className="size-4" />
                  </button>
                </div>
              </div>

              <div className="grid gap-3 sm:grid-cols-3">
                {ROLE_DOMAIN_GROUPS.map((domain, i) => {
                  const selectedInDomain = primaryRoles.filter((r) =>
                    rolesForDomain(domain.id).some((entry) => entry.label === r),
                  ).length
                  const isActive = domainIndex === i

                  return (
                    <button
                      key={domain.id}
                      type="button"
                      onClick={() => setDomainIndex(i)}
                      className={cn(
                        "rounded-2xl border p-4 text-left transition-all duration-200",
                        isActive
                          ? "border-primary bg-primary/5 shadow-md shadow-primary/10"
                          : "border-border/60 bg-card hover:border-primary/30 hover:shadow-sm",
                      )}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <p className="font-bold text-foreground">{domain.label}</p>
                        {selectedInDomain > 0 ? (
                          <span className="flex items-center gap-1 rounded-full bg-primary px-2 py-0.5 text-[10px] font-bold text-primary-foreground">
                            <CheckIcon />
                            {selectedInDomain} Selected
                          </span>
                        ) : (
                          <span className="text-[10px] font-medium text-primary">
                            Click to browse →
                          </span>
                        )}
                      </div>
                      <p className="mt-2 text-xs text-muted-foreground">{domain.description}</p>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Primary role picker — catalog only */}
            <div
              className="animate-fade-in-up opacity-0"
              style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
            >
              <RolePickerPanel
                domainId={activeDomain.id as RoleDomainId}
                selected={primaryRoles}
                onChange={setPrimaryRoles}
                exclude={secondaryRoles}
                title={`${activeDomain.label} Core Specialties`}
                subtitle="Primary roles (required) — select exact titles from the catalog."
              />
              {error ? <p className="mt-2 text-sm text-remove">{error}</p> : null}
            </div>

            {/* Role DNA visualization */}
            <div
              className="animate-fade-in-up rounded-2xl border border-border/80 bg-card p-5 opacity-0 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)]"
              style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}
            >
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Brain className="size-4 text-primary" />
                  <h2 className="text-sm font-bold text-foreground">Role DNA Visualization</h2>
                </div>
                <span className="rounded-full border border-primary/20 bg-primary/5 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-primary">
                  Dynamic Mapping
                </span>
              </div>

              <div className="relative flex h-40 items-center justify-center rounded-xl bg-gradient-to-br from-primary/5 to-muted/30">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="size-16 rounded-full bg-primary text-center text-[10px] font-bold leading-tight text-primary-foreground shadow-lg shadow-primary/30 flex flex-col items-center justify-center">
                    <span>CORE</span>
                    <span>ALIGN</span>
                  </div>
                </div>
                {["Python Arch", "AWS", "Leadership", "System Design"].map((node, i) => {
                  const positions = [
                    "left-[18%] top-[20%]",
                    "right-[15%] top-[25%]",
                    "left-[22%] bottom-[18%]",
                    "right-[18%] bottom-[20%]",
                  ]
                  return (
                    <span
                      key={node}
                      className={cn(
                        "absolute rounded-full border border-border/60 bg-card px-2.5 py-1 text-[10px] font-semibold text-foreground shadow-sm",
                        positions[i],
                      )}
                    >
                      {node}
                    </span>
                  )
                })}
              </div>

              <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                {[
                  { label: "Tech Fit", value: `${techFit}%` },
                  { label: "Exp Match", value: `${expMatch}%` },
                  { label: "Skill Density", value: "91%" },
                  { label: "Candidate Pool", value: "Top 2%" },
                ].map((m) => (
                  <div key={m.label} className="rounded-lg border border-border/60 bg-surface/40 px-3 py-2 text-center">
                    <p className="text-sm font-bold text-primary">{m.value}</p>
                    <p className="text-[10px] font-medium uppercase tracking-wider text-muted-foreground">
                      {m.label}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-border/80 bg-card p-5 shadow-sm">
              <h2 className="text-sm font-bold text-foreground">Matching filters</h2>
              <p className="mt-1 text-xs text-muted-foreground">
                These filters power your recommendations. Location defaults to the United States.
              </p>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                <label className="block text-sm sm:col-span-2">
                  <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                    Location (country)
                  </span>
                  <select
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
                    value={state.preferredLocations[0] ?? DEFAULT_LOCATION}
                    onChange={(e) =>
                      update("preferredLocations", ensureLocations([e.target.value]))
                    }
                  >
                    <option value={DEFAULT_LOCATION}>{DEFAULT_LOCATION}</option>
                    <option value="Remote (US)">Remote (US)</option>
                    <option value="New York, NY">New York, NY</option>
                    <option value="San Francisco, CA">San Francisco, CA</option>
                    <option value="Seattle, WA">Seattle, WA</option>
                    <option value="Austin, TX">Austin, TX</option>
                    <option value="Boston, MA">Boston, MA</option>
                  </select>
                </label>

                <label className="block text-sm">
                  <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                    Employment type
                  </span>
                  <select
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
                    value={
                      state.internshipOnly
                        ? "INTERNSHIP"
                        : state.parttimeOnly
                          ? "PARTTIME"
                          : "FULLTIME"
                    }
                    onChange={(e) => {
                      const v = e.target.value
                      onChange({
                        ...state,
                        fulltimeOnly: v === "FULLTIME",
                        parttimeOnly: v === "PARTTIME",
                        internshipOnly: v === "INTERNSHIP",
                      })
                    }}
                  >
                    <option value="FULLTIME">Full-time</option>
                    <option value="PARTTIME">Part-time</option>
                    <option value="INTERNSHIP">Internship</option>
                  </select>
                </label>

                <label className="block text-sm">
                  <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                    Experience level
                  </span>
                  <select
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
                    value={state.experienceLevel ?? "any"}
                    onChange={(e) =>
                      update(
                        "experienceLevel",
                        e.target.value === "any" ? null : (e.target.value as SeniorityLevel),
                      )
                    }
                  >
                    {EXPERIENCE_LEVEL_OPTIONS.map((o) => (
                      <option key={o.value} value={o.value}>
                        {o.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="block text-sm sm:col-span-2">
                  <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                    Remote preference
                  </span>
                  <select
                    className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
                    value={state.remotePreference || "any"}
                    onChange={(e) =>
                      update("remotePreference", e.target.value === "any" ? "" : e.target.value)
                    }
                  >
                    <option value="any">Any</option>
                    <option value="remote">Remote</option>
                    <option value="hybrid">Hybrid</option>
                    <option value="onsite">Onsite</option>
                  </select>
                </label>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
            <div className="rounded-2xl bg-primary p-5 text-primary-foreground shadow-lg shadow-primary/25">
              <div className="flex items-center gap-2">
                <Sparkles className="size-4" />
                <h2 className="text-sm font-bold">AI Agent Analysis</h2>
              </div>
              <div className="mt-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="opacity-90">Confidence Score</span>
                  <span className="font-bold">{confidenceScore(primaryRoles.length)}% PEAK</span>
                </div>
                <div className="mt-2 h-2 overflow-hidden rounded-full bg-primary-foreground/20">
                  <div
                    className="h-full rounded-full bg-primary-foreground transition-all duration-700"
                    style={{ width: `${confidenceScore(primaryRoles.length)}%` }}
                  />
                </div>
              </div>
              <div className="mt-4 space-y-3">
                <p className="text-[10px] font-bold uppercase tracking-widest opacity-80">
                  Suggested Matches
                </p>
                {suggestions.length > 0 ? (
                  suggestions.map((s) => (
                    <div key={s.role} className="rounded-lg bg-primary-foreground/10 p-3">
                      <p className="text-xs font-semibold">{s.role}</p>
                      <p className="mt-1 text-[11px] leading-relaxed opacity-80">{s.blurb}</p>
                    </div>
                  ))
                ) : (
                  <p className="text-xs opacity-80">Select primary roles to generate matches.</p>
                )}
              </div>
            </div>

            <div className="rounded-2xl border border-border/80 bg-card p-5 shadow-sm">
              <h2 className="text-sm font-bold text-foreground">Role Summary</h2>

              <div className="mt-4">
                <div className="flex items-center justify-between">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                    Primary Goal
                  </p>
                </div>
                <p className="mt-1 text-sm font-semibold text-foreground">
                  {primaryRoles[0] ?? "—"}
                  {primaryRoles.length > 1 ? (
                    <span className="ml-1 text-xs font-normal text-muted-foreground">
                      +{primaryRoles.length - 1} more
                    </span>
                  ) : null}
                </p>
              </div>

              <div className="mt-4">
                <div className="flex items-center justify-between">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                    Secondary Path
                  </p>
                  <button
                    type="button"
                    onClick={() => setShowSecondaryPicker((v) => !v)}
                    className="text-[10px] font-bold uppercase tracking-wider text-primary hover:underline"
                  >
                    {showSecondaryPicker ? "Done" : "Add"}
                  </button>
                </div>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {secondaryRoles.length > 0 ? (
                    secondaryRoles.map((role) => (
                      <button
                        key={role}
                        type="button"
                        onClick={() => toggleSecondary(role)}
                        className="inline-flex items-center gap-1 rounded-full border border-border bg-muted/50 px-2.5 py-1 text-xs font-medium text-foreground hover:border-remove/40"
                      >
                        {role}
                        <X className="size-3 text-muted-foreground" />
                      </button>
                    ))
                  ) : (
                    <p className="text-xs text-muted-foreground">No secondary roles selected</p>
                  )}
                </div>
              </div>

              {showSecondaryPicker ? (
                <div className="mt-3 rounded-xl border border-border/60 bg-surface/40 p-3">
                  <p className="mb-2 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                    Select from catalog
                  </p>
                  <SecondaryRoleChips
                    domainId={activeDomain.id as RoleDomainId}
                    selected={secondaryRoles}
                    exclude={primaryRoles}
                    onToggle={toggleSecondary}
                  />
                </div>
              ) : null}

              <Button
                className="btn-brand mt-5 h-11 w-full rounded-xl text-sm font-bold uppercase tracking-wide"
                disabled={!canContinue || saving}
                onClick={() => void handleSubmit()}
              >
                <Zap className="size-4" />
                {saving ? "Finalizing..." : "Finalize Match Engine"}
              </Button>
              <p className="mt-2 text-center text-[10px] text-muted-foreground">
                Matches update in real-time as you refine roles.
              </p>
            </div>
          </aside>
        </div>
      </div>

      <footer className="fixed inset-x-0 bottom-0 z-30 border-t border-border/60 bg-card/95 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-6 py-4">
          <span className="text-sm text-muted-foreground">Job Scout</span>
          <p className="hidden text-xs text-muted-foreground sm:block">
            {primaryRoles.length} primary · {secondaryRoles.length} secondary · catalog-matched
          </p>
          <Button
            disabled={!canContinue || saving}
            onClick={() => void handleSubmit()}
            className="btn-brand h-11 rounded-xl px-6 text-sm font-bold uppercase tracking-wide"
          >
            Confirm & Integrate
            <ChevronRight className="size-4" />
          </Button>
        </div>
      </footer>
    </div>
  )
}

function CheckIcon() {
  return (
    <svg className="size-3" viewBox="0 0 12 12" fill="none" aria-hidden="true">
      <path
        d="M2 6l3 3 5-5"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

function SecondaryRoleChips({
  domainId,
  selected,
  exclude,
  onToggle,
}: {
  domainId: RoleDomainId
  selected: string[]
  exclude: string[]
  onToggle: (role: string) => void
}) {
  const roles = rolesForDomain(domainId).filter((r) => !exclude.includes(r.label))

  return (
    <div className="flex max-h-32 flex-wrap gap-1.5 overflow-y-auto">
      {roles.map((role) => {
        const isSelected = selected.includes(role.label)
        return (
          <button
            key={role.id}
            type="button"
            onClick={() => onToggle(role.label)}
            className={cn(
              "rounded-md border px-2 py-1 text-[11px] font-medium transition-colors",
              isSelected
                ? "border-primary bg-primary/10 text-primary"
                : "border-border/60 bg-card text-foreground hover:border-primary/30",
            )}
          >
            {role.label}
          </button>
        )
      })}
    </div>
  )
}
