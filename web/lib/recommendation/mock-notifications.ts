import type {
  CompanySearchResult,
  CompanyWatchListApi,
  NotificationPreferencesApi,
  TierEntitlementsApi,
} from "@/lib/recommendation/api"
import { MOCK_CANDIDATE_ID } from "@/lib/profile/session"

const FREE_ENTITLEMENTS: TierEntitlementsApi = {
  max_companies: 0,
  cadence_min_minutes: 360,
  cadence_max_minutes: 720,
  delivery: "batched",
  max_emails_per_day_cap: 10,
  default_max_emails_per_day: 3,
  ats_fit: false,
  hiring_manager: false,
  apply_agent: false,
}

const PLUS_ENTITLEMENTS: TierEntitlementsApi = {
  max_companies: 25,
  cadence_min_minutes: 30,
  cadence_max_minutes: 180,
  delivery: "batched",
  max_emails_per_day_cap: 20,
  default_max_emails_per_day: 10,
  ats_fit: true,
  hiring_manager: false,
  apply_agent: false,
}

const PRO_ENTITLEMENTS: TierEntitlementsApi = {
  max_companies: 100,
  cadence_min_minutes: 15,
  cadence_max_minutes: 60,
  delivery: "batched",
  max_emails_per_day_cap: 50,
  default_max_emails_per_day: 20,
  ats_fit: true,
  hiring_manager: true,
  apply_agent: true,
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

function entitlementsFor(planTier: "free" | "plus" | "pro"): TierEntitlementsApi {
  if (planTier === "pro") return PRO_ENTITLEMENTS
  if (planTier === "plus") return PLUS_ENTITLEMENTS
  return FREE_ENTITLEMENTS
}

function defaultCadenceMinutes(planTier: "free" | "plus" | "pro"): number {
  if (planTier === "pro") return 15
  if (planTier === "plus") return 30
  return 360
}

function defaultMaxEmails(planTier: "free" | "plus" | "pro"): number {
  if (planTier === "pro") return 20
  if (planTier === "plus") return 10
  return 3
}

function createDefaultState(candidateId: string): MockNotificationState {
  const planTier: "free" | "plus" | "pro" = "free"
  const entitlements = entitlementsFor(planTier)
  return {
    watchedCompanyIds: [...DEFAULT_WATCHED_IDS],
    prefs: {
      candidate_id: candidateId,
      digest_enabled: true,
      company_watch_enabled: false,
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
  const key = candidateId || MOCK_CANDIDATE_ID
  let state = stateByCandidate.get(key)
  if (!state) {
    state = createDefaultState(key)
    stateByCandidate.set(key, state)
  }
  return state
}

export async function mockFetchNotificationPreferences(candidateId: string) {
  return structuredClone(getState(candidateId).prefs)
}

export async function mockUpdateNotificationPreferences(
  candidateId: string,
  payload: Partial<NotificationPreferencesApi>,
) {
  const state = getState(candidateId)
  state.prefs = {
    ...state.prefs,
    ...payload,
    entitlements: state.prefs.entitlements,
    plan_tier: state.prefs.plan_tier,
  }
  return structuredClone(state.prefs)
}

export async function mockFetchCompanyWatch(candidateId: string): Promise<CompanyWatchListApi> {
  const state = getState(candidateId)
  const companies = MOCK_COMPANY_CATALOG.filter((c) => state.watchedCompanyIds.includes(c.id)).map(
    (c) => ({
      company_id: c.id,
      company_name: c.name,
      platform: c.platform,
      is_active: true,
    }),
  )
  return {
    candidate_id: candidateId,
    companies,
    plan_tier: state.prefs.plan_tier,
    max_companies: state.prefs.entitlements.max_companies,
  }
}

export async function mockUpdateCompanyWatch(candidateId: string, companyIds: string[]) {
  const state = getState(candidateId)
  const max = state.prefs.entitlements.max_companies
  const current = new Set(state.watchedCompanyIds)
  const next = [...new Set(companyIds)]
  const added = next.filter((id) => !current.has(id))
  if (added.length > 0 && next.length > max) {
    throw new Error(`Plan allows up to ${max} watched companies`)
  }
  state.watchedCompanyIds = next
  return mockFetchCompanyWatch(candidateId)
}

export async function mockSearchCompanies(q: string, limit = 20): Promise<CompanySearchResult[]> {
  const query = q.trim().toLowerCase()
  return MOCK_COMPANY_CATALOG.filter((c) => !query || c.name.toLowerCase().includes(query)).slice(
    0,
    limit,
  )
}
