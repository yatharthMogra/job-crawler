export type PlanTier = "free" | "plus"

export const COMPANY_WATCH_PLANS = {
  free: {
    tier: "free" as const,
    name: "Free",
    maxCompanies: 5,
    deliveryLabel: "Batched alerts every 6–12 hours",
    priceLabel: null,
  },
  plus: {
    tier: "plus" as const,
    name: "Job Scout Plus",
    maxCompanies: 25,
    deliveryLabel: "Instant alerts within 30 minutes",
    priceLabel: "$4.99/month",
  },
} as const

export const PLUS_WAITLIST_MAILTO =
  "mailto:support@careermatch.ai?subject=Job%20Scout%20Plus%20waitlist&body=Hi%2C%20I%27d%20like%20to%20be%20notified%20when%20Job%20Scout%20Plus%20is%20available."

export function isPlusTier(planTier: string | null | undefined): planTier is "plus" {
  return planTier === "plus"
}
