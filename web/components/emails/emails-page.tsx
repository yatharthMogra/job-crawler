"use client"

import { useCallback, useEffect, useState } from "react"
import Link from "next/link"
import { Pencil } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { CompanyWatchPlanCards } from "@/components/emails/company-watch-plan-cards"
import { CompanyWatchPicker } from "@/components/settings/company-watch-picker"
import { SettingRow, Toggle } from "@/components/settings/setting-controls"
import { FilterChip } from "@/components/ui/filter-chip"
import { Button } from "@/components/ui/button"
import {
  companyWatchCadenceOptions,
  DIGEST_CADENCE_OPTIONS,
  fetchCompanyWatch,
  fetchNotificationPreferences,
  updateCompanyWatch,
  updateNotificationPreferences,
  type NotificationPreferencesApi,
} from "@/lib/recommendation/api"
import { isPlusTier } from "@/lib/plans/company-watch"
import { cn } from "@/lib/utils"

function EmailsPageSkeleton() {
  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="h-48 animate-pulse rounded-xl bg-muted/60" />
        <div className="h-48 animate-pulse rounded-xl bg-muted/60" />
      </div>
      <div className="h-32 animate-pulse rounded-xl bg-muted/60" />
      <div className="h-64 animate-pulse rounded-xl bg-muted/60" />
    </div>
  )
}

export function EmailsPage() {
  const { candidateId } = useSession()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const [prefs, setPrefs] = useState<NotificationPreferencesApi | null>(null)
  const [watchedCompanyIds, setWatchedCompanyIds] = useState<string[]>([])
  const [maxCompanies, setMaxCompanies] = useState(5)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reloadKey, setReloadKey] = useState(0)

  const loadPreferences = useCallback(async (id: string) => {
    setLoading(true)
    setError(null)
    try {
      const [preferences, watchList] = await Promise.all([
        fetchNotificationPreferences(id),
        fetchCompanyWatch(id),
      ])
      setPrefs(preferences)
      setWatchedCompanyIds(watchList.companies.map((c) => c.company_id))
      setMaxCompanies(watchList.max_companies)
    } catch {
      setPrefs(null)
      setError("Could not load email alert preferences. Check your connection and try again.")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (candidateId) void loadProfileHome(candidateId).catch(() => undefined)
  }, [candidateId, loadProfileHome])

  useEffect(() => {
    if (!candidateId) {
      setLoading(false)
      return
    }
    void loadPreferences(candidateId)
  }, [candidateId, loadPreferences, reloadKey])

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
      setMaxCompanies(updated.max_companies)
      setError(null)
    } catch {
      setError("Could not update company watch list.")
    } finally {
      setSaving(false)
    }
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

  if (!candidateId) {
    return (
      <div className="mx-auto max-w-2xl p-6">
        <p className="text-sm text-muted-foreground">Sign in to manage email alerts.</p>
      </div>
    )
  }

  if (loading) return <EmailsPageSkeleton />

  if (error && !prefs) {
    return (
      <div className="mx-auto max-w-2xl space-y-4 p-6">
        <p className="text-sm text-destructive">{error}</p>
        <Button variant="outline" size="sm" onClick={() => setReloadKey((k) => k + 1)}>
          Try again
        </Button>
      </div>
    )
  }

  if (!prefs) return null

  const onPlus = isPlusTier(prefs.plan_tier)

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6">
      {error ? (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3">
          <p className="text-sm text-destructive">{error}</p>
          <Button variant="outline" size="sm" onClick={() => setReloadKey((k) => k + 1)}>
            Retry
          </Button>
        </div>
      ) : null}

      <CompanyWatchPlanCards
        planTier={prefs.plan_tier}
        watchedCount={watchedCompanyIds.length}
        maxCompanies={maxCompanies}
      />

      <div className="rounded-xl card-elevated border-0 p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap gap-1.5">
            {filterChips.slice(0, 6).map((chip) => (
              <FilterChip key={chip} label={chip} active />
            ))}
            {filterChips.length > 6 ? <FilterChip label={`+${filterChips.length - 6}`} /> : null}
            {filterChips.length === 0 ? (
              <p className="text-sm text-muted-foreground">No profile filters set yet.</p>
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
          Profile filters apply to both Company Watch and Personalized Digest emails.
        </p>
      </div>

      <div className="rounded-xl card-elevated border-0 px-6">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border/60 py-4">
          <h2 className="text-base font-semibold text-foreground">Company Watch</h2>
          <span
            className={cn(
              "rounded-full border px-3 py-1 text-xs font-medium",
              onPlus
                ? "border-primary/30 bg-primary/5 text-primary"
                : "border-border bg-surface text-foreground",
            )}
          >
            {onPlus ? "Job Scout Plus" : "Free"} · {watchedCompanyIds.length}/{maxCompanies}{" "}
            companies
          </span>
        </div>
        <SettingRow
          title="Enable Company Watch"
          description="Get batched emails at your chosen frequency when watched companies post new matching roles."
        >
          <Toggle
            checked={prefs.company_watch_enabled}
            disabled={saving}
            onChange={(v) => void savePrefs({ company_watch_enabled: v })}
          />
        </SettingRow>
        <div className="border-b border-border/60 py-5 last:border-0">
          <p className="mb-3 text-sm font-medium text-foreground">Watched companies</p>
          <CompanyWatchPicker
            selectedCompanyIds={watchedCompanyIds}
            maxCompanies={maxCompanies}
            disabled={!prefs.company_watch_enabled || saving}
            onChange={(ids) => void saveWatchList(ids)}
          />
        </div>
        <SettingRow title="Alert frequency">
          <select
            className="rounded-lg card-elevated border-0 px-3 py-2 text-sm text-foreground disabled:opacity-50"
            value={prefs.company_watch_cadence_minutes}
            disabled={!prefs.company_watch_enabled || saving}
            onChange={(e) =>
              void savePrefs({ company_watch_cadence_minutes: Number(e.target.value) })
            }
          >
            {companyWatchCadenceOptions(prefs.plan_tier).map((opt) => (
              <option key={opt.minutes} value={opt.minutes}>
                {opt.label}
              </option>
            ))}
          </select>
        </SettingRow>
        <SettingRow
          title="Daily email limit"
          description={`${prefs.emails_sent_today} of ${prefs.max_emails_per_day} emails sent in the last 24 hours.`}
        >
          <select
            className="rounded-lg card-elevated border-0 px-3 py-2 text-sm text-foreground disabled:opacity-50"
            value={prefs.max_emails_per_day}
            disabled={saving}
            onChange={(e) => void savePrefs({ max_emails_per_day: Number(e.target.value) })}
          >
            {Array.from({ length: prefs.entitlements.max_emails_per_day_cap }, (_, i) => i + 1).map(
              (n) => (
                <option key={n} value={n}>
                  {n} email{n !== 1 ? "s" : ""} / day
                </option>
              ),
            )}
          </select>
        </SettingRow>
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
    </div>
  )
}
