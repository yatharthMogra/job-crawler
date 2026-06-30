"use client"

import { useEffect, useState, type ReactNode } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { signOut } from "next-auth/react"
import { Pencil } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { CompanyWatchPicker } from "@/components/settings/company-watch-picker"
import { FilterChip } from "@/components/ui/filter-chip"
import { Button } from "@/components/ui/button"
import { clearStoredCandidateId } from "@/lib/session"
import {
  DIGEST_CADENCE_OPTIONS,
  fetchCompanyWatch,
  fetchNotificationPreferences,
  updateCompanyWatch,
  updateNotificationPreferences,
  type NotificationPreferencesApi,
} from "@/lib/recommendation/api"
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
  disabled,
}: {
  checked: boolean
  onChange: (value: boolean) => void
  disabled?: boolean
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={cn(
        "relative h-6 w-11 shrink-0 rounded-full transition-colors disabled:opacity-50",
        checked ? "bg-primary" : "bg-muted",
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
    <div className="flex items-start justify-between gap-6 border-b border-border/60 py-5 last:border-0">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-foreground">{title}</p>
        {description ? <p className="mt-1 text-sm leading-relaxed text-muted-foreground">{description}</p> : null}
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
  const [prefs, setPrefs] = useState<NotificationPreferencesApi | null>(null)
  const [watchedCompanyIds, setWatchedCompanyIds] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (candidateId) void loadProfileHome(candidateId).catch(() => undefined)
  }, [candidateId, loadProfileHome])

  useEffect(() => {
    if (!candidateId) return
    setLoading(true)
    void (async () => {
      try {
        const [preferences, watchList] = await Promise.all([
          fetchNotificationPreferences(candidateId),
          fetchCompanyWatch(candidateId),
        ])
        setPrefs(preferences)
        setWatchedCompanyIds(watchList.companies.map((c) => c.company_id))
        setError(null)
      } catch {
        setError("Could not load notification preferences.")
      } finally {
        setLoading(false)
      }
    })()
  }, [candidateId])

  async function savePrefs(patch: Parameters<typeof updateNotificationPreferences>[1]) {
    if (!candidateId || !prefs) return
    setSaving(true)
    try {
      const updated = await updateNotificationPreferences(candidateId, patch)
      setPrefs(updated)
      setError(null)
    } catch {
      setError("Could not save preferences.")
    } finally {
      setSaving(false)
    }
  }

  async function saveWatchList(companyIds: string[]) {
    if (!candidateId) return
    setWatchedCompanyIds(companyIds)
    setSaving(true)
    try {
      const updated = await updateCompanyWatch(candidateId, companyIds)
      setWatchedCompanyIds(updated.companies.map((c) => c.company_id))
      setError(null)
    } catch {
      setError("Could not update company watch list.")
    } finally {
      setSaving(false)
    }
  }

  async function handleLogout() {
    clearStoredCandidateId()
    await signOut({ callbackUrl: "/login" })
    router.replace("/login")
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
    <div className="dashboard-page-bg flex min-h-screen flex-col">
      <div className="border-b border-border/80 bg-card/80 px-6 py-4 backdrop-blur-sm">
        <h1 className="text-lg font-bold tracking-tight text-foreground">Settings</h1>
        <p className="text-xs text-muted-foreground">Account, subscriptions, and notification preferences</p>
      </div>

      <div className="flex flex-1">
        <aside className="w-52 shrink-0 border-r border-border/80 bg-card/60 p-3">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => setSection(s.id)}
              className={cn(
                "mb-0.5 w-full rounded-lg px-3 py-2.5 text-left text-sm transition-colors",
                section === s.id
                  ? "bg-accent font-medium text-accent-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-secondary/80",
              )}
            >
              {s.label}
            </button>
          ))}
        </aside>

        <main className="flex-1 p-6">
          {section === "login" ? (
            <div className="mx-auto max-w-2xl rounded-xl card-elevated border-0 p-6">
              <h2 className="text-base font-semibold text-foreground">Login & Security</h2>
              <div className="mt-6">
                <SettingRow title="Email" description={candidate?.email ?? "—"}>
                  <span className="text-xs text-muted-foreground/70">Verified</span>
                </SettingRow>
                <SettingRow title="Password" description="Last updated — not available in demo mode">
                  <Button variant="outline" size="sm" className="border-border" disabled>
                    Change password
                  </Button>
                </SettingRow>
              </div>
            </div>
          ) : null}

          {section === "subscriptions" ? (
            <div className="mx-auto max-w-2xl rounded-xl card-elevated border-0 p-6">
              <h2 className="text-base font-semibold text-foreground">Subscriptions</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Job pool subscriptions are synced from your profile filters.
              </p>
            </div>
          ) : null}

          {section === "alerts" ? (
            <div className="mx-auto max-w-2xl space-y-6">
              {error ? <p className="text-sm text-destructive">{error}</p> : null}
              {loading || !prefs ? (
                <p className="text-sm text-muted-foreground">Loading preferences…</p>
              ) : (
                <>
                  <div className="rounded-xl card-elevated border-0 p-5">
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
                        <Button size="sm" className="gap-1.5 btn-brand">
                          <Pencil className="size-3.5" />
                          Filters
                        </Button>
                      </Link>
                    </div>
                    <p className="mt-3 text-xs text-muted-foreground">
                      Profile filters apply to both Company Watch and Personalized Digest.
                    </p>
                  </div>

                  <div className="rounded-xl card-elevated border-0 px-6">
                    <h2 className="border-b border-border/60 py-4 text-base font-semibold text-foreground">
                      Company Watch
                    </h2>
                    <SettingRow
                      title="Enable Company Watch"
                      description="Get notified as soon as a watched company posts a role matching your preferences."
                    >
                      <Toggle
                        checked={prefs.company_watch_enabled}
                        disabled={saving}
                        onChange={(v) => void savePrefs({ company_watch_enabled: v })}
                      />
                    </SettingRow>
                    <div className="border-b border-border/60 py-5 last:border-0">
                      <p className="mb-3 text-sm font-medium text-foreground">Watched companies</p>
                      {candidateId ? (
                        <CompanyWatchPicker
                          selectedCompanyIds={watchedCompanyIds}
                          disabled={!prefs.company_watch_enabled || saving}
                          onChange={(ids) => void saveWatchList(ids)}
                        />
                      ) : null}
                    </div>
                  </div>

                  <div className="rounded-xl card-elevated border-0 px-6">
                    <h2 className="border-b border-border/60 py-4 text-base font-semibold text-foreground">
                      Personalized Digest
                    </h2>
                    <SettingRow
                      title="Enable Personalized Digest"
                      description="Receive top-ranked job recommendations on your chosen schedule."
                    >
                      <Toggle
                        checked={prefs.digest_enabled}
                        disabled={saving}
                        onChange={(v) => void savePrefs({ digest_enabled: v })}
                      />
                    </SettingRow>
                    <SettingRow title="Digest frequency">
                      <select
                        className="rounded-lg card-elevated border-0 px-3 py-2 text-sm text-foreground disabled:opacity-50"
                        value={prefs.cadence_hours}
                        disabled={!prefs.digest_enabled || saving}
                        onChange={(e) => void savePrefs({ cadence_hours: Number(e.target.value) })}
                      >
                        {DIGEST_CADENCE_OPTIONS.map((opt) => (
                          <option key={opt.hours} value={opt.hours}>
                            {opt.label}
                          </option>
                        ))}
                      </select>
                    </SettingRow>
                  </div>
                </>
              )}
            </div>
          ) : null}

          {section === "logout" ? (
            <div className="mx-auto max-w-2xl rounded-xl card-elevated border-0 p-6">
              <h2 className="text-base font-semibold text-foreground">Log out</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Sign out of your account on this device. Your profile and saved jobs remain stored.
              </p>
              <Button
                variant="outline"
                className="mt-6 border-border text-foreground hover:bg-surface"
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
