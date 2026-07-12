"use client"

import { useCallback, useState } from "react"
import { Check, Loader2 } from "lucide-react"
import { openBillingPortal, startCheckout } from "@/lib/billing/api"
import {
  isPlusTier,
  normalizePlanTier,
  PLANS,
  type PaidPlan,
  type PlanTier,
} from "@/lib/plans/company-watch"
import { cn } from "@/lib/utils"

interface PlanPricingCardsProps {
  planTier: string
  candidateId: string | null
  watchedCount?: number
  maxCompanies?: number
  className?: string
}

export function PlanPricingCards({
  planTier,
  candidateId,
  watchedCount = 0,
  maxCompanies = 5,
  className,
}: PlanPricingCardsProps) {
  const tier = normalizePlanTier(planTier)
  const [loadingPlan, setLoadingPlan] = useState<PaidPlan | "portal" | null>(null)
  const [error, setError] = useState<string | null>(null)

  const runCheckout = useCallback(
    async (plan: PaidPlan) => {
      if (!candidateId) {
        setError("Sign in to upgrade.")
        return
      }
      setError(null)
      setLoadingPlan(plan)
      try {
        const url = await startCheckout(candidateId, plan)
        window.location.href = url
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unable to start checkout")
        setLoadingPlan(null)
      }
    },
    [candidateId],
  )

  const runPortal = useCallback(async () => {
    if (!candidateId) {
      setError("Sign in to manage billing.")
      return
    }
    setError(null)
    setLoadingPlan("portal")
    try {
      const url = await openBillingPortal(candidateId)
      window.location.href = url
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to open billing portal")
      setLoadingPlan(null)
    }
  }, [candidateId])

  const cards: PlanTier[] = ["free", "plus", "pro"]
  const slotMax = Math.max(maxCompanies, 1)
  const slotPct = Math.min(100, (watchedCount / slotMax) * 100)

  return (
    <div className={cn("space-y-3", className)}>
      {isPlusTier(tier) ? (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border/70 bg-card px-4 py-3">
          <p className="text-sm text-muted-foreground">
            You&apos;re on <span className="font-semibold text-foreground">{PLANS[tier].name}</span>
          </p>
          <button
            type="button"
            onClick={() => void runPortal()}
            disabled={loadingPlan !== null}
            className="rounded-lg border border-border px-3 py-1.5 text-xs font-semibold text-foreground transition-colors hover:bg-muted disabled:opacity-50"
          >
            {loadingPlan === "portal" ? <Loader2 className="size-4 animate-spin" /> : "Manage billing"}
          </button>
        </div>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-3">
        {cards.map((key) => {
          const plan = PLANS[key]
          const isCurrent = key === tier
          const isPaidCard = key !== "free"
          const isRecommended = key === "plus" && tier === "free"

          return (
            <div
              key={key}
              className={cn(
                "relative flex flex-col rounded-2xl border p-5 shadow-sm",
                isPaidCard
                  ? "border-slate-800 bg-[#0f172a] text-white"
                  : "border-border/80 bg-card text-foreground",
                isRecommended && "ring-2 ring-primary/50",
              )}
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <p className={cn("text-sm font-semibold", isPaidCard ? "text-white" : "text-foreground")}>
                    {key === "plus" ? "Job Scout AI Plus" : plan.name}
                  </p>
                  {key === "free" ? (
                    <p className="mt-1 text-xs text-muted-foreground">{plan.maxCompanies} watched companies</p>
                  ) : (
                    <p className="mt-1 text-2xl font-bold tracking-tight">
                      {plan.priceMonthlyLabel ?? plan.priceLabel}
                    </p>
                  )}
                </div>
                {isCurrent ? (
                  <span
                    className={cn(
                      "rounded-full px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide",
                      isPaidCard ? "bg-white/15 text-white" : "bg-primary text-primary-foreground",
                    )}
                  >
                    Current plan
                  </span>
                ) : null}
                {isRecommended ? (
                  <span className="rounded-full bg-primary px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide text-primary-foreground">
                    Recommended
                  </span>
                ) : null}
              </div>

              <ul className="mt-5 flex-1 space-y-2.5">
                {plan.shortFeatures.map((feature) => (
                  <li
                    key={feature}
                    className={cn(
                      "flex items-start gap-2 text-sm",
                      isPaidCard ? "text-slate-300" : "text-muted-foreground",
                    )}
                  >
                    <Check
                      className={cn("mt-0.5 size-4 shrink-0", isPaidCard ? "text-sky-300" : "text-primary")}
                      strokeWidth={2.5}
                    />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              {key === "free" && isCurrent ? (
                <div className="mt-5 space-y-2">
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>
                      {watchedCount} of {maxCompanies} slots used
                    </span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-muted">
                    <div
                      className="h-full rounded-full bg-primary transition-all duration-500"
                      style={{ width: `${slotPct}%` }}
                    />
                  </div>
                </div>
              ) : null}

              {key === "free" || isCurrent ? (
                <p
                  className={cn(
                    "mt-5 text-center text-xs",
                    isPaidCard ? "text-slate-400" : "text-muted-foreground",
                  )}
                >
                  {isCurrent ? "Your current plan" : "Included with Job Scout AI"}
                </p>
              ) : (
                <button
                  type="button"
                  disabled={loadingPlan !== null || !candidateId}
                  onClick={() => void runCheckout(key)}
                  className={cn(
                    "mt-5 flex w-full items-center justify-center rounded-xl py-2.5 text-sm font-bold transition-colors disabled:opacity-50",
                    isRecommended
                      ? "bg-white text-slate-900 hover:bg-white/90"
                      : "bg-white/10 text-white hover:bg-white/15",
                  )}
                >
                  {loadingPlan === key ? (
                    <Loader2 className="size-4 animate-spin" />
                  ) : key === "plus" ? (
                    "Upgrade Now"
                  ) : (
                    "Upgrade"
                  )}
                </button>
              )}
            </div>
          )
        })}
      </div>
      {error ? <p className="text-sm text-destructive">{error}</p> : null}
    </div>
  )
}
