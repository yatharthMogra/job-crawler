export type PlanTier = "free" | "plus" | "pro"

export type PaidPlan = "plus" | "pro"

/** Feature flags for Pro capabilities not yet live in product. */
export const FEATURE_HIRING_MANAGER_LIVE = false
export const FEATURE_APPLY_AGENT_LIVE = false

export interface PlanDefinition {
  tier: PlanTier
  name: string
  priceLabel: string | null
  priceCents: number | null
  maxCompanies: number
  deliveryLabel: string
  features: string[]
  atsFit: boolean
  hiringManager: boolean
  applyAgent: boolean
}

export const PLANS: Record<PlanTier, PlanDefinition> = {
  free: {
    tier: "free",
    name: "Free",
    priceLabel: null,
    priceCents: null,
    maxCompanies: 0,
    deliveryLabel: "Personalized digest emails",
    features: [
      "Personalized job recommendations",
      "Digest emails on your cadence",
      "Application tracking",
    ],
    atsFit: false,
    hiringManager: false,
    applyAgent: false,
  },
  plus: {
    tier: "plus",
    name: "Job Scout Plus",
    priceLabel: "$4.99/month",
    priceCents: 499,
    maxCompanies: 25,
    deliveryLabel: "Company watch alerts every 30 min–3 hours",
    features: [
      "Everything in Free",
      "Resume checker (ATS fit + semantic signals)",
      "Watch up to 25 companies",
      "Faster company-watch email alerts",
    ],
    atsFit: true,
    hiringManager: false,
    applyAgent: false,
  },
  pro: {
    tier: "pro",
    name: "Job Scout Pro",
    priceLabel: "$19.99/month",
    priceCents: 1999,
    maxCompanies: 100,
    deliveryLabel: "Company watch alerts every 15–60 minutes",
    features: [
      "Everything in Plus",
      "Watch up to 100 companies",
      "Hiring manager contacts (rolling out)",
      "Apply agent / autofill (rolling out)",
      "Best-fit role email notifications (rolling out)",
    ],
    atsFit: true,
    hiringManager: true,
    applyAgent: true,
  },
}

/** @deprecated Use PLANS — kept for older imports */
export const COMPANY_WATCH_PLANS = {
  free: {
    tier: "free" as const,
    name: PLANS.free.name,
    maxCompanies: PLANS.free.maxCompanies,
    deliveryLabel: PLANS.free.deliveryLabel,
    priceLabel: null,
  },
  plus: {
    tier: "plus" as const,
    name: PLANS.plus.name,
    maxCompanies: PLANS.plus.maxCompanies,
    deliveryLabel: PLANS.plus.deliveryLabel,
    priceLabel: PLANS.plus.priceLabel,
  },
  pro: {
    tier: "pro" as const,
    name: PLANS.pro.name,
    maxCompanies: PLANS.pro.maxCompanies,
    deliveryLabel: PLANS.pro.deliveryLabel,
    priceLabel: PLANS.pro.priceLabel,
  },
} as const

export function normalizePlanTier(planTier: string | null | undefined): PlanTier {
  if (planTier === "pro") return "pro"
  if (planTier === "plus") return "plus"
  return "free"
}

export function isPlusTier(planTier: string | null | undefined): boolean {
  const tier = normalizePlanTier(planTier)
  return tier === "plus" || tier === "pro"
}

export function isProTier(planTier: string | null | undefined): boolean {
  return normalizePlanTier(planTier) === "pro"
}

export function planAllowsAtsFit(planTier: string | null | undefined): boolean {
  return PLANS[normalizePlanTier(planTier)].atsFit
}

export function hiringManagerUnlockState(planTier: string | null | undefined): "locked" | "coming_soon" | "live" {
  if (!isProTier(planTier)) return "locked"
  return FEATURE_HIRING_MANAGER_LIVE ? "live" : "coming_soon"
}
