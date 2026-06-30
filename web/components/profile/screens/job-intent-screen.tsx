"use client"

import { useState } from "react"
import type { JobIntentState } from "@/lib/profile/job-intent"
import { EeoForm } from "@/components/profile/eeo-form"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { RoleCascader } from "@/components/profile/role-cascader"
import { TagInput } from "@/components/profile/review/tag-input"
import { FlowStepBar } from "@/components/ui/flow-page"
import { ArrowRight } from "lucide-react"

interface JobIntentScreenProps {
  state: JobIntentState
  onChange: (state: JobIntentState) => void
  onSubmit: () => void | Promise<void>
  saving?: boolean
}

export function JobIntentScreen({ state, onChange, onSubmit, saving }: JobIntentScreenProps) {
  const [error, setError] = useState<string | null>(null)
  const canContinue = state.primaryRoles.length > 0

  function update<K extends keyof JobIntentState>(key: K, value: JobIntentState[K]) {
    onChange({ ...state, [key]: value })
    if (key === "primaryRoles") setError(null)
  }

  async function handleSubmit() {
    if (!canContinue) {
      setError("Add at least one primary role to continue.")
      return
    }
    setError(null)
    await onSubmit()
  }

  return (
    <div className="dashboard-page-bg min-h-screen pb-24">
      <header className="sticky top-0 z-30 border-b border-border/80 bg-card/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-2xl items-center justify-between px-4 py-3 sm:px-6">
          <Brand />
        </div>
      </header>

      <main className="mx-auto max-w-2xl px-4 py-8 sm:px-6">
        <div className="mb-8">
          <FlowStepBar current={4} total={4} label="Job preferences" />
          <h1 className="text-balance text-2xl font-bold tracking-tight sm:text-3xl">
            <span className="gradient-text">Define your job search</span>
          </h1>
          <p className="mt-2 text-pretty leading-relaxed text-muted-foreground">
            Tell us what roles you want to pursue. Recommendations follow your choices — not random
            resume keywords.
          </p>
        </div>

        <div className="space-y-6">
          <Card className="card-elevated overflow-visible border-0 p-5">
            <h2 className="text-base font-semibold text-foreground">Target roles</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              What positions are you actively looking to apply for?
            </p>
            <div className="mt-4 space-y-4">
              <p className="mb-2 text-sm font-medium text-foreground">Primary roles (required)</p>
              <RoleCascader
                selected={state.primaryRoles}
                onChange={(tags) => update("primaryRoles", tags)}
                placeholder="Select job functions"
              />
              <TagInput
                label="Secondary roles (optional)"
                tags={state.secondaryRoles}
                onChange={(tags) => update("secondaryRoles", tags)}
              />
            </div>
            {error ? <p className="mt-3 text-sm text-remove">{error}</p> : null}
          </Card>

          <Card className="card-elevated border-0 p-5">
            <h2 className="text-base font-semibold text-foreground">Work constraints</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Optional filters that help narrow compatible opportunities.
            </p>
            <div className="mt-4 space-y-4">
              <label className="block text-sm">
                <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                  Sponsorship required
                </span>
                <select
                  className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm"
                  value={state.sponsorshipRequired ? "true" : "false"}
                  onChange={(e) => update("sponsorshipRequired", e.target.value === "true")}
                >
                  <option value="false">No</option>
                  <option value="true">Yes</option>
                </select>
              </label>
              <Field
                label="Visa type"
                value={state.visaType}
                onChange={(v) => update("visaType", v)}
                placeholder="e.g. F1, OPT"
              />
              <Field
                label="Work authorization"
                value={state.workAuthorization}
                onChange={(v) => update("workAuthorization", v)}
                placeholder="e.g. CPT / OPT"
              />
              <div className="flex flex-wrap gap-4">
                <Checkbox
                  label="Internship only"
                  checked={state.internshipOnly}
                  onChange={(v) => update("internshipOnly", v)}
                />
                <Checkbox
                  label="Full-time only"
                  checked={state.fulltimeOnly}
                  onChange={(v) => update("fulltimeOnly", v)}
                />
              </div>
              <Field
                label="Minimum hourly rate"
                value={state.minimumHourlyRate}
                onChange={(v) => update("minimumHourlyRate", v)}
                placeholder="$ per hour"
              />
            </div>
          </Card>

          <Card className="card-elevated border-0 p-5">
            <h2 className="text-base font-semibold text-foreground">Your experience level</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              We use this to match you with realistic roles — not job titles you pick yourself.
            </p>
            <div className="mt-4 space-y-4">
              <label className="block text-sm">
                <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                  Full-time professional experience (years)
                </span>
                <Input
                  type="number"
                  min={0}
                  step={0.5}
                  value={state.fullTimeExperienceYears ?? ""}
                  onChange={(e) =>
                    update(
                      "fullTimeExperienceYears",
                      e.target.value === "" ? null : Number(e.target.value),
                    )
                  }
                  placeholder="e.g. 2.5"
                />
              </label>
              <label className="block text-sm">
                <span className="mb-1.5 block text-xs font-medium text-muted-foreground">
                  Currently completing a degree?
                </span>
                <select
                  className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm"
                  value={
                    state.isCurrentlyEnrolled === null
                      ? ""
                      : state.isCurrentlyEnrolled
                        ? "true"
                        : "false"
                  }
                  onChange={(e) =>
                    update(
                      "isCurrentlyEnrolled",
                      e.target.value === "" ? null : e.target.value === "true",
                    )
                  }
                >
                  <option value="">Select</option>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </select>
              </label>
              {state.isCurrentlyEnrolled ? (
                <Field
                  label="Expected graduation (YYYY-MM)"
                  value={state.expectedGraduationDate}
                  onChange={(v) => update("expectedGraduationDate", v)}
                  placeholder="2027-05"
                />
              ) : null}
            </div>
          </Card>

          <Card className="card-elevated border-0 p-5">
            <h2 className="text-base font-semibold text-foreground">Location preferences</h2>
            <p className="mt-1 text-sm text-muted-foreground">Where and how you prefer to work.</p>
            <div className="mt-4 space-y-4">
              <TagInput
                label="Preferred locations"
                tags={state.preferredLocations}
                onChange={(tags) => update("preferredLocations", tags)}
              />
              <Field
                label="Remote preference"
                value={state.remotePreference}
                onChange={(v) => update("remotePreference", v)}
                placeholder="Remote, Hybrid, or Onsite"
              />
              <TagInput
                label="Preferred industries"
                tags={state.preferredIndustries}
                onChange={(tags) => update("preferredIndustries", tags)}
              />
            </div>
          </Card>

          <Card className="card-elevated border-0 p-5">
            <h2 className="text-base font-semibold text-foreground">Equal employment authorization</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Standard US application questions. We&apos;ll use these to auto-fill job forms later.
            </p>
            <div className="mt-4">
              <EeoForm
                state={state.eeo}
                onChange={(eeo) => update("eeo", eeo)}
                compact
              />
            </div>
          </Card>
        </div>
      </main>

      <div className="fixed inset-x-0 bottom-0 z-30 border-t-2 border-border/80 bg-card/95 backdrop-blur-md">
        <div className="mx-auto flex max-w-2xl justify-end px-4 py-3 sm:px-6">
          <Button className="btn-brand" disabled={!canContinue || saving} onClick={() => void handleSubmit()}>
            {saving ? "Saving..." : "Save and continue"}
            <ArrowRight className="size-4" aria-hidden="true" />
          </Button>
        </div>
      </div>
    </div>
  )
}

function Field({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string
  value: string
  onChange: (v: string) => void
  placeholder?: string
}) {
  return (
    <label className="block text-sm">
      <span className="mb-1.5 block text-xs font-medium text-muted-foreground">{label}</span>
      <Input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} />
    </label>
  )
}

function Checkbox({
  label,
  checked,
  onChange,
}: {
  label: string
  checked: boolean
  onChange: (v: boolean) => void
}) {
  return (
    <label className="inline-flex items-center gap-2 text-sm text-foreground">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="size-4 rounded border-border"
      />
      {label}
    </label>
  )
}
