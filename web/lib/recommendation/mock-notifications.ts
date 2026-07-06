import type {
  CompanySearchResult,
  CompanyWatchListApi,
  NotificationPreferencesApi,
  TierEntitlementsApi,
} from "@/lib/recommendation/api"
import { MOCK_CANDIDATE_ID } from "@/lib/profile/session"

const FREE_ENTITLEMENTS: TierEntitlementsApi = {
  max_companies: 5,
  cadence_min_minutes: 360,
  cadence_max_minutes: 720,
  delivery: "batched",
  max_emails_per_day_cap: 10,
  default_max_emails_per_day: 3,
}

const PLUS_ENTITLEMENTS: TierEntitlementsApi = {
  max_companies: 25,
  cadence_min_minutes: 30,
  cadence_max_minutes: 180,
  delivery: "instant",
  max_emails_per_day_cap: 20,
  default_max_emails_per_day: 10,
}

export const MOCK_COMPANY_CATALOG: CompanySearchResult[] = [
  { id: "a1000000-0000-4000-8000-000000000001", name: "Stripe", platform: "greenhouse", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000002", name: "Notion", platform: "ashby", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000003", name: "Anthropic", platform: "greenhouse", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000004", name: "Figma", platform: "greenhouse", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000005", name: "Databricks", platform: "greenhouse", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000006", name: "Airbnb", platform: "greenhouse", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000007", name: "Coinbase", platform: "greenhouse", is_active: true },
  { id: "a1000000-0000-4000-8000-000000000008", name: "Scale AI", platform: "greenhouse", is_active: true },
]

const DEFAULT_WATCHED_IDS = [
  "a1000000-0000-4000-8000-000000000001",
  "a1000000-0000-4000-8000-000000000002",
  "a1000000-0000-4000-8000-000000000003",
]

interface MockNotificationState {
  prefs: NotificationPreferencesApi
  watchedCompanyIds: string[]
}

const stateByCandidate = new Map<string, MockNotificationState>()

function entitlementsFor(planTier: "free" | "plus"): TierEntitlementsApi {
  return planTier === "plus" ? PLUS_ENTITLEMENTS : FREE_ENTITLEMENTS
}

function defaultCadenceMinutes(planTier: "free" | "plus"): number {
  return planTier === "plus" ? 30 : 360
}

function defaultMaxEmails(planTier: "free" | "plus"): number {
  return planTier === "plus" ? 10 : 3
}

function createDefaultState(candidateId: string): MockNotificationState {
  const planTier: "free" | "plus" = "free"
  const entitlements = entitlementsFor(planTier)
  return {
    watchedCompanyIds: [...DEFAULT_WATCHED_IDS],
    prefs: {
      candidate_id: candidateId,
      digest_enabled: true,
      company_watch_enabled: true,
      cadence_hours: 24,
      top_k: 4,
      digest_filters: null,
      last_digest_sent_at: null,
      next_digest_due_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      company_watch_cadence_minutes: defaultCadenceMinutes(planTier),
      max_emails_per_day: defaultMaxEmails(planTier),
      last_company_watch_batch_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
      next_company_watch_due_at: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
      plan_tier: planTier,
      entitlements,
      emails_sent_today: 1,
    },
  }
}

function getState(candidateId: string): MockNotificationState {
  let state = stateByCandidate.get(candidateId)
  if (!state) {
    state = createDefaultState(candidateId)
    stateByCandidate.set(candidateId, state)
  }
  return state
}

function buildWatchList(candidateId: string, state: MockNotificationState): CompanyWatchListApi {
  const catalog = new Map(MOCK_COMPANY_CATALOG.map((c) => [c.id, c]))
  return {
    candidate_id: candidateId,
    plan_tier: state.prefs.plan_tier,
    max_companies: state.prefs.entitlements.max_companies,
    companies: state.watchedCompanyIds
      .map((id) => catalog.get(id))
      .filter((c): c is CompanySearchResult => Boolean(c))
      .map((c) => ({
        company_id: c.id,
        company_name: c.name,
        platform: c.platform,
        is_active: c.is_active,
      })),
  }
}

function delay<T>(value: T): Promise<T> {
  return new Promise((resolve) => window.setTimeout(() => resolve(value), 120))
}

export function mockFetchNotificationPreferences(candidateId: string) {
  return delay({ ...getState(candidateId).prefs })
}

export function mockUpdateNotificationPreferences(
  candidateId: string,
  payload: Partial<{
    digest_enabled: boolean
    company_watch_enabled: boolean
    cadence_hours: number
    top_k: number
    company_watch_cadence_minutes: number
    max_emails_per_day: number
  }>,
) {
  const state = getState(candidateId)
  const next = { ...state.prefs, ...payload }

  if (payload.max_emails_per_day != null) {
    next.max_emails_per_day = Math.min(
      Math.max(1, payload.max_emails_per_day),
      next.entitlements.max_emails_per_day_cap,
    )
  }

  state.prefs = next
  return delay({ ...next })
}

export function mockFetchCompanyWatch(candidateId: string) {
  const state = getState(candidateId)
  return delay(buildWatchList(candidateId, state))
}

export function mockUpdateCompanyWatch(candidateId: string, companyIds: string[]) {
  const state = getState(candidateId)
  const max = state.prefs.entitlements.max_companies
  if (companyIds.length > max) {
    return Promise.reject(new Error(`Your plan allows up to ${max} watched companies.`))
  }
  const validIds = new Set(MOCK_COMPANY_CATALOG.map((c) => c.id))
  state.watchedCompanyIds = companyIds.filter((id) => validIds.has(id))
  return delay(buildWatchList(candidateId, state))
}

export function mockSearchCompanies(q = "", limit = 20) {
  const pattern = q.trim().toLowerCase()
  const results = MOCK_COMPANY_CATALOG.filter(
    (c) =>
      !pattern ||
      c.name.toLowerCase().includes(pattern) ||
      c.platform.toLowerCase().includes(pattern),
  ).slice(0, limit)
  return delay(results)
}

export function ensureMockCandidateSession() {
  if (typeof window === "undefined") return
  if (!localStorage.getItem("profile_candidate_id")) {
    localStorage.setItem("profile_candidate_id", MOCK_CANDIDATE_ID)
  }
}
