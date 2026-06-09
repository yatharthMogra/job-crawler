"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { RoleCascader, poolIdsForSelectedRoles } from "@/components/profile/role-cascader"
import { EeoForm } from "@/components/profile/eeo-form"
import { FilterChip } from "@/components/ui/filter-chip"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { useMockData } from "@/lib/session"
import {
  emptyJobFilters,
  profileToJobFilters,
  jobFiltersToApiPayload,
  EXPERIENCE_LEVELS,
  DATE_POSTED_OPTIONS,
  WORK_MODEL_OPTIONS,
} from "@/lib/profile/job-filters"
import { patchConstraints, patchPreferences } from "@/lib/profile/api"
import { useJobs } from "@/components/jobs-provider"
import { syncSubscriptionsForCandidate } from "@/lib/recommendation/sync-subscriptions"
import { cn } from "@/lib/utils"

const SECTIONS = [
  { id: "basic", label: "Basic Job Criteria", sub: "Job Function / Job Type / Work Model" },
  { id: "comp", label: "Compensation & Sponsorship", sub: "Annual Salary / H1B Sponsorship" },
  { id: "interests", label: "Areas of Interests", sub: "Industry / Skill / Role" },
  { id: "company", label: "Company Insights", sub: "Company Search / Exclude Agencies" },
] as const

type SectionId = (typeof SECTIONS)[number]["id"]

export default function FiltersPage() {
  const router = useRouter()
  const { candidateId } = useSession()
  const mockMode = useMockData()
  const { rawProfile, profileHome, loadProfileHome } = useProfileFlow()
  const { refreshJobs } = useJobs()
  const [section, setSection] = useState<SectionId>("basic")
  const [state, setState] = useState(emptyJobFilters())
  const [saving, setSaving] = useState(false)
  const [industryInput, setIndustryInput] = useState("")
  const [skillInput, setSkillInput] = useState("")

  useEffect(() => {
    if (candidateId && !rawProfile) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, rawProfile, loadProfileHome])

  useEffect(() => {
    if (rawProfile) {
      setState(profileToJobFilters(rawProfile))
    } else if (profileHome) {
      setState((prev) => ({
        ...prev,
        primaryRoles: profileHome.primaryRoles,
        secondaryRoles: profileHome.secondaryRoles,
        eeo: profileHome.eeo,
      }))
    }
  }, [rawProfile, profileHome])

  function update<K extends keyof typeof state>(key: K, value: (typeof state)[K]) {
    setState((prev) => ({ ...prev, [key]: value }))
  }

  function toggleLevel(level: string) {
    const levels = state.experienceLevels.includes(level)
      ? state.experienceLevels.filter((l) => l !== level)
      : [...state.experienceLevels, level]
    update("experienceLevels", levels)
  }

  function toggleWorkModel(model: string) {
    const models = state.workModels.includes(model)
      ? state.workModels.filter((m) => m !== model)
      : [...state.workModels, model]
    update("workModels", models)
  }

  async function handleConfirm() {
    if (!candidateId) return
    setSaving(true)
    try {
      const suffix = state.internshipOnly && !state.fulltimeOnly ? "INTERNSHIP" : "FULLTIME"
      const poolIds = poolIdsForSelectedRoles(state.primaryRoles, suffix)
      const payload = jobFiltersToApiPayload({ ...state, rolePoolIds: poolIds })
      if (mockMode) {
        router.push("/jobs/recommended")
        return
      }
      await patchConstraints(candidateId, payload.constraints)
      await patchPreferences(candidateId, payload.preferences)
      await loadProfileHome(candidateId)
      await syncSubscriptionsForCandidate(candidateId)
      await refreshJobs()
      router.push("/jobs/recommended")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="dashboard-page-bg flex min-h-screen flex-col">
      <div className="sticky top-0 z-10 flex items-center justify-between border-b border-border/80 bg-card/95 px-6 py-3 backdrop-blur-sm">
        <div className="flex flex-wrap gap-2">
          {state.primaryRoles.slice(0, 4).map((r) => (
            <FilterChip key={r} label={r} active />
          ))}
          {state.primaryRoles.length > 4 ? (
            <FilterChip label={`+${state.primaryRoles.length - 4} more`} />
          ) : null}
        </div>
        <Button
          className="btn-brand"
          onClick={() => void handleConfirm()}
          disabled={saving}
        >
          {saving ? "Saving..." : "Confirm"}
        </Button>
      </div>

      <div className="flex flex-1">
        <aside className="w-56 shrink-0 border-r border-border/80 bg-card/60 p-3">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => setSection(s.id)}
              className={cn(
                "mb-1 w-full rounded-lg px-3 py-2.5 text-left transition-colors",
                section === s.id ? "bg-accent text-accent-foreground shadow-sm" : "hover:bg-secondary/80",
              )}
            >
              <p className="text-sm font-medium text-foreground">{s.label}</p>
              <p className="text-xs text-muted-foreground">{s.sub}</p>
            </button>
          ))}
        </aside>

        <main className="flex-1 p-6">
          {section === "basic" ? (
            <div className="mx-auto max-w-2xl space-y-6">
              <div>
                <label className="text-sm font-medium">
                  Job Function <span className="text-red-500">*</span>
                </label>
                <div className="mt-2">
                  <RoleCascader
                    selected={state.primaryRoles}
                    onChange={(roles) => {
                      update("primaryRoles", roles)
                      const suffix =
                        state.internshipOnly && !state.fulltimeOnly ? "INTERNSHIP" : "FULLTIME"
                      update("rolePoolIds", poolIdsForSelectedRoles(roles, suffix))
                    }}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <label className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3">
                  <input
                    type="checkbox"
                    checked={state.fulltimeOnly}
                    onChange={(e) => update("fulltimeOnly", e.target.checked)}
                  />
                  <span className="text-sm">Full-time</span>
                </label>
                <label className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3">
                  <input
                    type="checkbox"
                    checked={state.internshipOnly}
                    onChange={(e) => update("internshipOnly", e.target.checked)}
                  />
                  <span className="text-sm">Internship</span>
                </label>
              </div>

              <div>
                <p className="text-sm font-medium">Work model</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {WORK_MODEL_OPTIONS.map((m) => (
                    <button
                      key={m}
                      type="button"
                      onClick={() => toggleWorkModel(m)}
                      className={cn(
                        "rounded-lg border px-3 py-2 text-sm",
                        state.workModels.includes(m)
                          ? "border-primary bg-accent text-accent-foreground shadow-sm"
                          : "border-border bg-card",
                      )}
                    >
                      {m}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-sm font-medium">
                  Experience Level <span className="text-red-500">*</span>
                </p>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {EXPERIENCE_LEVELS.map((level) => (
                    <label
                      key={level}
                      className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3"
                    >
                      <input
                        type="checkbox"
                        checked={state.experienceLevels.includes(level)}
                        onChange={() => toggleLevel(level)}
                      />
                      <span className="text-sm">{level}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-sm font-medium">Date Posted</p>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {DATE_POSTED_OPTIONS.map((opt) => (
                    <label
                      key={opt.value}
                      className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3"
                    >
                      <input
                        type="radio"
                        name="datePosted"
                        checked={state.maxJobAgeDays === opt.value}
                        onChange={() => update("maxJobAgeDays", opt.value)}
                      />
                      <span className="text-sm">{opt.label}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          ) : null}

          {section === "comp" ? (
            <div className="mx-auto max-w-2xl space-y-6">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium">Minimum Annual Salary</p>
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={state.openToAllSalary}
                    onChange={(e) => update("openToAllSalary", e.target.checked)}
                  />
                  Open to all
                </label>
              </div>
              {!state.openToAllSalary ? (
                <Input
                  type="number"
                  placeholder="e.g. 120000"
                  value={state.minimumSalary}
                  onChange={(e) => update("minimumSalary", e.target.value)}
                />
              ) : null}

              <label className="flex items-start gap-3 rounded-lg border border-border/80 bg-card p-4">
                <input
                  type="checkbox"
                  checked={state.sponsorshipRequired}
                  onChange={(e) => update("sponsorshipRequired", e.target.checked)}
                  className="mt-1"
                />
                <div>
                  <p className="text-sm font-medium">H1B sponsorship</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    Show jobs that explicitly support visa sponsorship or come from companies with
                    sponsorship history.
                  </p>
                </div>
              </label>

              <div className="space-y-2">
                <label className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3">
                  <input
                    type="checkbox"
                    checked={state.excludeSecurityClearance}
                    onChange={(e) => update("excludeSecurityClearance", e.target.checked)}
                  />
                  <span className="text-sm">Exclude jobs requiring security clearance</span>
                </label>
                <label className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3">
                  <input
                    type="checkbox"
                    checked={state.excludeUsCitizenOnly}
                    onChange={(e) => update("excludeUsCitizenOnly", e.target.checked)}
                  />
                  <span className="text-sm">Exclude US citizen only roles</span>
                </label>
              </div>

              <div>
                <p className="mb-3 text-sm font-medium">Equal Employment</p>
                <EeoForm state={state.eeo} onChange={(eeo) => update("eeo", eeo)} compact />
              </div>
            </div>
          ) : null}

          {section === "interests" ? (
            <div className="mx-auto max-w-2xl space-y-6">
              <div>
                <p className="text-sm font-medium">Industry</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {state.preferredIndustries.map((ind) => (
                    <FilterChip
                      key={ind}
                      label={ind}
                      active
                      onRemove={() =>
                        update(
                          "preferredIndustries",
                          state.preferredIndustries.filter((i) => i !== ind),
                        )
                      }
                    />
                  ))}
                </div>
                <div className="mt-2 flex gap-2">
                  <Input
                    value={industryInput}
                    onChange={(e) => setIndustryInput(e.target.value)}
                    placeholder="Add industry"
                    className="max-w-xs"
                  />
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => {
                      if (industryInput.trim()) {
                        update("preferredIndustries", [
                          ...state.preferredIndustries,
                          industryInput.trim(),
                        ])
                        setIndustryInput("")
                      }
                    }}
                  >
                    Add
                  </Button>
                </div>
              </div>

              <div>
                <p className="text-sm font-medium">Skills</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {state.preferredSkills.map((sk) => (
                    <FilterChip
                      key={sk}
                      label={sk}
                      active
                      onRemove={() =>
                        update(
                          "preferredSkills",
                          state.preferredSkills.filter((s) => s !== sk),
                        )
                      }
                    />
                  ))}
                </div>
                <div className="mt-2 flex gap-2">
                  <Input
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    placeholder="Add skill"
                    className="max-w-xs"
                  />
                  <Button
                    size="sm"
                    variant="secondary"
                    onClick={() => {
                      if (skillInput.trim()) {
                        update("preferredSkills", [...state.preferredSkills, skillInput.trim()])
                        setSkillInput("")
                      }
                    }}
                  >
                    Add
                  </Button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <label className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3">
                  <input
                    type="radio"
                    name="roleType"
                    checked={state.roleType === "ic"}
                    onChange={() => update("roleType", "ic")}
                  />
                  <span className="text-sm">IC (Individual Contributor)</span>
                </label>
                <label className="flex items-center gap-2 rounded-lg border border-border/80 bg-card p-3">
                  <input
                    type="radio"
                    name="roleType"
                    checked={state.roleType === "manager"}
                    onChange={() => update("roleType", "manager")}
                  />
                  <span className="text-sm">Manager</span>
                </label>
              </div>
            </div>
          ) : null}

          {section === "company" ? (
            <div className="mx-auto max-w-2xl">
              <p className="text-sm text-muted-foreground">
                Company search and staffing agency filters coming soon. Use job function and industry
                filters to narrow your target companies for now.
              </p>
            </div>
          ) : null}
        </main>
      </div>
    </div>
  )
}
