"use client"

import { useEffect, useState, type ReactNode } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Pencil, Zap } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { FilterChip } from "@/components/ui/filter-chip"
import { Button } from "@/components/ui/button"
import { clearStoredCandidateId } from "@/lib/session"
import {
  loadJobAlertsSettings,
  persistJobAlertsSettings,
  type JobAlertsSettings,
} from "@/lib/settings-storage"
import { cn } from "@/lib/utils"

const SECTIONS = [
  { id: "login", label: "Login & Security" },
  { id: "subscriptions", label: "Subscriptions" },
  { id: "alerts", label: "Job Alerts" },
  { id: "logout", label: "Log out" },
] as const

type SectionId = (typeof SECTIONS)[number]["id"]

function Toggle({
  checked,
  onChange,
}: {
  checked: boolean
  onChange: (value: boolean) => void
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={cn(
        "relative h-6 w-11 shrink-0 rounded-full transition-colors",
        checked ? "bg-zinc-900" : "bg-zinc-200",
      )}
    >
      <span
        className={cn(
          "absolute top-0.5 size-5 rounded-full bg-white shadow transition-transform",
          checked ? "left-[22px]" : "left-0.5",
        )}
      />
    </button>
  )
}

function SettingRow({
  title,
  description,
  children,
}: {
  title: ReactNode
  description?: string
  children: ReactNode
}) {
  return (
    <div className="flex items-start justify-between gap-6 border-b border-zinc-100 py-5 last:border-0">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-zinc-900">{title}</p>
        {description ? <p className="mt-1 text-sm leading-relaxed text-zinc-500">{description}</p> : null}
      </div>
      <div className="shrink-0">{children}</div>
    </div>
  )
}

export function SettingsPage() {
  const router = useRouter()
  const { candidateId, candidate } = useSession()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const [section, setSection] = useState<SectionId>("alerts")
  const [alerts, setAlerts] = useState<JobAlertsSettings | null>(null)

  useEffect(() => {
    if (candidateId) void loadProfileHome(candidateId).catch(() => undefined)
  }, [candidateId, loadProfileHome])

  useEffect(() => {
    if (candidateId) setAlerts(loadJobAlertsSettings(candidateId))
  }, [candidateId])

  function updateAlerts(patch: Partial<JobAlertsSettings>) {
    if (!candidateId || !alerts) return
    const next = { ...alerts, ...patch }
    setAlerts(next)
    persistJobAlertsSettings(candidateId, next)
  }

  function handleLogout() {
    clearStoredCandidateId()
    router.replace("/onboarding")
  }

  const filterChips: string[] = []
  if (profileHome) {
    filterChips.push(...profileHome.primaryRoles)
    filterChips.push(...profileHome.secondaryRoles.slice(0, 2))
    if (profileHome.preferences.some((p) => p.label === "Remote")) {
      const remote = profileHome.preferences.find((p) => p.label === "Remote")
      if (remote?.value) filterChips.push(remote.value)
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-zinc-50">
      <div className="border-b border-zinc-200 bg-white px-6 py-4">
        <h1 className="text-lg font-bold tracking-tight text-zinc-900">Settings</h1>
        <p className="text-xs text-zinc-500">Account, subscriptions, and notification preferences</p>
      </div>

      <div className="flex flex-1">
        <aside className="w-52 shrink-0 border-r border-zinc-200 bg-white p-3">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => setSection(s.id)}
              className={cn(
                "mb-0.5 w-full rounded-lg px-3 py-2.5 text-left text-sm transition-colors",
                section === s.id
                  ? "bg-zinc-100 font-medium text-zinc-900"
                  : "text-zinc-600 hover:bg-zinc-50",
              )}
            >
              {s.label}
            </button>
          ))}
        </aside>

        <main className="flex-1 p-6">
          {section === "login" ? (
            <div className="mx-auto max-w-2xl rounded-xl border border-zinc-200 bg-white p-6">
              <h2 className="text-base font-semibold text-zinc-900">Login & Security</h2>
              <div className="mt-6">
                <SettingRow title="Email" description={candidate?.email ?? "—"}>
                  <span className="text-xs text-zinc-400">Verified</span>
                </SettingRow>
                <SettingRow title="Password" description="Last updated — not available in demo mode">
                  <Button variant="outline" size="sm" className="border-zinc-300" disabled>
                    Change password
                  </Button>
                </SettingRow>
                <SettingRow
                  title="Two-factor authentication"
                  description="Add an extra layer of security to your account."
                >
                  <Button variant="outline" size="sm" className="border-zinc-300" disabled>
                    Enable
                  </Button>
                </SettingRow>
              </div>
            </div>
          ) : null}

          {section === "subscriptions" ? (
            <div className="mx-auto max-w-2xl rounded-xl border border-zinc-200 bg-white p-6">
              <h2 className="text-base font-semibold text-zinc-900">Subscriptions</h2>
              <div className="mt-6 rounded-lg border border-zinc-200 bg-zinc-50 p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-zinc-900">Free Plan</p>
                    <p className="mt-1 text-sm text-zinc-500">Up to 1 instant job alert per day</p>
                  </div>
                  <span className="rounded-full border border-zinc-300 px-3 py-1 text-xs font-medium text-zinc-600">
                    Current
                  </span>
                </div>
                <Button className="mt-4 bg-zinc-900 text-white hover:bg-zinc-800" size="sm" disabled>
                  Upgrade to Turbo
                </Button>
              </div>
            </div>
          ) : null}

          {section === "alerts" && alerts ? (
            <div className="mx-auto max-w-2xl space-y-6">
              <div className="rounded-xl border border-zinc-200 bg-white p-5">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex flex-wrap gap-1.5">
                    {filterChips.slice(0, 6).map((chip) => (
                      <FilterChip key={chip} label={chip} active />
                    ))}
                    {filterChips.length > 6 ? (
                      <FilterChip label={`+${filterChips.length - 6}`} />
                    ) : null}
                  </div>
                  <Link href="/filters">
                    <Button size="sm" className="gap-1.5 bg-zinc-900 text-white hover:bg-zinc-800">
                      <Pencil className="size-3.5" />
                      Filters
                    </Button>
                  </Link>
                </div>
              </div>

              <div className="rounded-xl border border-zinc-200 bg-white px-6">
                <h2 className="border-b border-zinc-100 py-4 text-base font-semibold text-zinc-900">
                  Instant Job Alerts
                </h2>
                <SettingRow
                  title="Enable Instant Job Alerts"
                  description="Be the first to apply — get fresh, tailored job alerts within an hour of posting."
                >
                  <Toggle checked={alerts.instantEnabled} onChange={(v) => updateAlerts({ instantEnabled: v })} />
                </SettingRow>
                <SettingRow
                  title={
                    <span className="inline-flex items-center gap-1.5">
                      Job Alerts Frequency
                      <Zap className="size-3.5 text-zinc-400" />
                    </span>
                  }
                  description="Turbo Plan gets unlimited job alerts per day, Free Plan gets up to 1."
                >
                  <select
                    className="rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-700"
                    value={alerts.instantFrequency}
                    disabled={!alerts.instantEnabled}
                    onChange={(e) =>
                      updateAlerts({ instantFrequency: e.target.value as JobAlertsSettings["instantFrequency"] })
                    }
                  >
                    <option value="1">Up to 1 alert /day</option>
                    <option value="unlimited" disabled>
                      Unlimited (Turbo)
                    </option>
                  </select>
                </SettingRow>
              </div>

              <div className="rounded-xl border border-zinc-200 bg-white px-6">
                <h2 className="border-b border-zinc-100 py-4 text-base font-semibold text-zinc-900">
                  Digest Job Alerts
                </h2>
                <SettingRow
                  title="Enable Digest Job Alerts"
                  description="Receive a curated list of matching job opportunities in a single email, delivered daily or weekly."
                >
                  <Toggle checked={alerts.digestEnabled} onChange={(v) => updateAlerts({ digestEnabled: v })} />
                </SettingRow>
                <SettingRow title="Job Alerts Frequency">
                  <select
                    className="rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-700"
                    value={alerts.digestFrequency}
                    disabled={!alerts.digestEnabled}
                    onChange={(e) =>
                      updateAlerts({ digestFrequency: e.target.value as JobAlertsSettings["digestFrequency"] })
                    }
                  >
                    <option value="daily">Daily Digest</option>
                    <option value="weekly">Weekly Digest</option>
                  </select>
                </SettingRow>
              </div>
            </div>
          ) : null}

          {section === "logout" ? (
            <div className="mx-auto max-w-2xl rounded-xl border border-zinc-200 bg-white p-6">
              <h2 className="text-base font-semibold text-zinc-900">Log out</h2>
              <p className="mt-2 text-sm text-zinc-500">
                Sign out of your account on this device. Your profile and saved jobs remain stored.
              </p>
              <Button
                variant="outline"
                className="mt-6 border-zinc-300 text-zinc-900 hover:bg-zinc-50"
                onClick={handleLogout}
              >
                Log out
              </Button>
            </div>
          ) : null}
        </main>
      </div>
    </div>
  )
}
