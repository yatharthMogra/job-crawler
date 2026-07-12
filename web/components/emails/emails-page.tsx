"use client"

import { useCallback, useEffect, useState } from "react"
import Link from "next/link"
import { Pencil, Sparkles } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { CompanyWatchPlanCards } from "@/components/emails/company-watch-plan-cards"
import { CompanyWatchPicker } from "@/components/settings/company-watch-picker"
import { Toggle } from "@/components/settings/setting-controls"
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
import { PRODUCT_NAME } from "@/lib/plans/company-watch"
import { cn } from "@/lib/utils"

function EmailsPageSkeleton() {
  return (
    <div className="mx-auto max-w-5xl space-y-6 p-6 lg:p-8">
      <div className="h-16 animate-pulse rounded-xl bg-muted/60" />
      <div className="grid gap-4 lg:grid-cols-3">
        <div className="h-56 animate-pulse rounded-2xl bg-muted/60" />
        <div className="h-56 animate-pulse rounded-2xl bg-muted/60" />
        <div className="h-56 animate-pulse rounded-2xl bg-muted/60" />
      </div>
      <div className="h-24 animate-pulse rounded-2xl bg-muted/60" />
      <div className="h-80 animate-pulse rounded-2xl bg-muted/60" />
    </div>
  )
}

export function EmailsPage() {
  const { candidateId } = useSession()
  const { profileHome, loadProfileHome } = useProfileFlow()
  const [prefs, setPrefs] = useState<NotificationPreferencesApi | null>(null)
  const [watchedCompanyIds, setWatchedCompanyIds] = useState<string[]>([])
  const [watchedCompanies, setWatchedCompanies] = useState<
    Array<{
      company_id: string
      company_name: string
      platform: string
      logo_url?: string | null
    }>
  >([])
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
      setWatchedCompanies(
        watchList.companies.map((c) => ({
          company_id: c.company_id,
          company_name: c.company_name,
          platform: c.platform,
          logo_url: c.logo_url,
        })),
      )
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
      setWatchedCompanies(
        updated.companies.map((c) => ({
          company_id: c.company_id,
          company_name: c.company_name,
          platform: c.platform,
          logo_url: c.logo_url,
        })),
      )
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
    const location = profileHome.preferences.find((p) => p.label === "Location" || p.label === "Locations")
    if (location?.value) filterChips.push(location.value)
  }

  if (!candidateId) {
    return (
      <div className="mx-auto max-w-5xl p-6 lg:p-8">
        <p className="text-sm text-muted-foreground">Sign in to manage {PRODUCT_NAME} email alerts.</p>
      </div>
    )
  }

  if (loading) return <EmailsPageSkeleton />

  if (error && !prefs) {
    return (
      <div className="mx-auto max-w-5xl space-y-4 p-6 lg:p-8">
        <p className="text-sm text-destructive">{error}</p>
        <Button variant="outline" size="sm" onClick={() => setReloadKey((k) => k + 1)}>
          Try again
        </Button>
      </div>
    )
  }

  if (!prefs) return null

  const companyWatchAllowed = prefs.entitlements.max_companies > 0
  const slotsLeft = Math.max(0, maxCompanies - watchedCompanyIds.length)
  const watchEnabled = prefs.company_watch_enabled && companyWatchAllowed

  return (
    <div className="dashboard-page-bg min-h-full">
      <div className="mx-auto max-w-5xl space-y-6 p-6 lg:p-8">
        <header>
          <p className="text-[11px] font-bold uppercase tracking-[0.18em] text-primary">{PRODUCT_NAME}</p>
          <h1 className="mt-1 text-3xl font-bold tracking-tight text-foreground">Email alerts</h1>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            Watch dream companies and get digests when roles match your filters.
          </p>
        </header>

        {error ? (
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-destructive/30 bg-destructive/5 px-4 py-3">
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

        <section className="rounded-2xl border border-border/70 bg-card px-5 py-4 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="min-w-0 flex-1">
              <p className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                Active filters
              </p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {filterChips.slice(0, 8).map((chip) => (
                  <FilterChip key={chip} label={chip} active />
                ))}
                {filterChips.length > 8 ? <FilterChip label={`+${filterChips.length - 8}`} /> : null}
                {filterChips.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No profile filters set yet.</p>
                ) : null}
              </div>
              <p className="mt-2 text-xs text-muted-foreground">
                Filters apply to both Company Watch and Digest emails.
              </p>
            </div>
            <Link href="/filters">
              <Button size="sm" className="gap-1.5 btn-brand">
                <Pencil className="size-3.5" />
                Filters
              </Button>
            </Link>
          </div>
        </section>

        <section className="overflow-hidden rounded-2xl border border-border/70 bg-card shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4 border-b border-border/60 px-5 py-5">
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-3">
                <h2 className="text-lg font-bold text-foreground">Company Watch</h2>
                <Toggle
                  checked={watchEnabled}
                  disabled={saving || !companyWatchAllowed}
                  onChange={(v) => void savePrefs({ company_watch_enabled: v })}
                />
              </div>
              <p className="mt-1 text-sm text-muted-foreground">
                Get notified when specific companies post new roles that match your filters.
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm font-semibold tabular-nums text-foreground">
                {watchedCompanyIds.length} / {Math.max(maxCompanies, 0)} companies watched
              </p>
              <p className="mt-0.5 text-xs text-muted-foreground">
                {slotsLeft > 0
                  ? `${slotsLeft} slot${slotsLeft === 1 ? "" : "s"} remaining`
                  : "All slots filled"}
              </p>
            </div>
          </div>

          {!companyWatchAllowed ? (
            <p className="border-b border-border/60 px-5 py-4 text-sm text-muted-foreground">
              Company watch is unavailable on this plan. Upgrade above to unlock watches in {PRODUCT_NAME}.
            </p>
          ) : null}

          <div
            className={cn(
              "space-y-6 px-5 py-5 transition-opacity",
              !watchEnabled && companyWatchAllowed ? "opacity-55" : "opacity-100",
            )}
          >
            <CompanyWatchPicker
              selectedCompanyIds={watchedCompanyIds}
              knownCompanies={watchedCompanies}
              maxCompanies={maxCompanies}
              disabled={!watchEnabled || saving || !companyWatchAllowed}
              onChange={(ids) => void saveWatchList(ids)}
            />
            {!watchEnabled && companyWatchAllowed ? (
              <p className="text-xs text-muted-foreground">
                Turn on Company Watch above to start adding companies.
              </p>
            ) : null}

            <div className="grid gap-4 border-t border-border/60 pt-5 sm:grid-cols-2">
              <label className="space-y-2">
                <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                  Alert frequency
                </span>
                <select
                  className="w-full rounded-xl border border-border/70 bg-surface px-3 py-2.5 text-sm text-foreground disabled:opacity-50"
                  value={prefs.company_watch_cadence_minutes}
                  disabled={!watchEnabled || saving}
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
              </label>
              <label className="space-y-2">
                <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                  Daily email limit
                </span>
                <select
                  className="w-full rounded-xl border border-border/70 bg-surface px-3 py-2.5 text-sm text-foreground disabled:opacity-50"
                  value={prefs.max_emails_per_day}
                  disabled={saving || !companyWatchAllowed}
                  onChange={(e) => void savePrefs({ max_emails_per_day: Number(e.target.value) })}
                >
                  {Array.from(
                    { length: Math.max(1, prefs.entitlements.max_emails_per_day_cap) },
                    (_, i) => i + 1,
                  ).map((n) => (
                    <option key={n} value={n}>
                      {n} email{n !== 1 ? "s" : ""} / day
                    </option>
                  ))}
                </select>
                <p className="text-xs text-muted-foreground">
                  {prefs.emails_sent_today} of {prefs.max_emails_per_day} emails sent in the last 24 hours.
                </p>
              </label>
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-border/70 bg-card px-5 py-5 shadow-sm">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-3">
                <span className="flex size-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                  <Sparkles className="size-4" />
                </span>
                <h2 className="text-lg font-bold text-foreground">Personalized Digest</h2>
                <Toggle
                  checked={prefs.digest_enabled}
                  disabled={saving}
                  onChange={(v) => void savePrefs({ digest_enabled: v })}
                />
              </div>
              <p className="mt-2 text-sm text-muted-foreground">
                Ranked job matches based on your profile filters. {PRODUCT_NAME} scouts new roles and
                emails your top matches on the schedule you choose.
              </p>
            </div>
          </div>

          <div className="mt-5 max-w-sm">
            <label className="space-y-2">
              <span className="text-[11px] font-bold uppercase tracking-widest text-muted-foreground">
                Digest frequency
              </span>
              <select
                className="w-full rounded-xl border border-border/70 bg-surface px-3 py-2.5 text-sm text-foreground disabled:opacity-50"
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
            </label>
          </div>
        </section>
      </div>
    </div>
  )
}
