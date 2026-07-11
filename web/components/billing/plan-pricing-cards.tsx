"use client"

import { useCallback, useState } from "react"
import { Check, Loader2, Sparkles } from "lucide-react"
import { buttonVariants } from "@/components/ui/button"
import { openBillingPortal, startCheckout } from "@/lib/billing/api"
import {
  isPlusTier,
  isProTier,
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
  compact?: boolean
}

function PlanFeature({ children, muted }: { children: React.ReactNode; muted?: boolean }) {
  return (
    <li className={cn("flex items-start gap-2 text-sm", muted ? "text-slate-300" : "text-muted-foreground")}>
      <Check className={cn("mt-0.5 size-4 shrink-0", muted ? "text-violet-300" : "text-primary")} strokeWidth={2.5} />
      <span>{children}</span>
    </li>
  )
}

export function PlanPricingCards({
  planTier,
  candidateId,
  watchedCount,
  maxCompanies,
  className,
  compact = false,
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

  const cards: PlanTier[] = compact && isPlusTier(tier) ? (isProTier(tier) ? ["pro"] : ["plus", "pro"]) : ["free", "plus", "pro"]

  return (
    <div className={cn("space-y-3", className)}>
      {isPlusTier(tier) ? (
        <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-primary/20 bg-gradient-to-br from-primary/5 to-primary/10 p-4">
          <div className="flex items-center gap-2">
            <Sparkles className="size-4 text-primary" />
            <p className="text-sm font-semibold text-foreground">{PLANS[tier].name}</p>
            {typeof watchedCount === "number" && typeof maxCompanies === "number" ? (
              <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
                {watchedCount}/{maxCompanies} companies
              </span>
            ) : null}
          </div>
          <button
            type="button"
            onClick={() => void runPortal()}
            disabled={loadingPlan !== null}
            className={cn(buttonVariants({ size: "sm", variant: "outline" }))}
          >
            {loadingPlan === "portal" ? <Loader2 className="size-4 animate-spin" /> : "Manage billing"}
          </button>
        </div>
      ) : null}

      <div className={cn("grid gap-4", cards.length >= 3 ? "lg:grid-cols-3" : "sm:grid-cols-2")}>
        {cards.map((key) => {
          const plan = PLANS[key]
          const isCurrent = key === tier
          const isDark = key !== "free"
          return (
            <div
              key={key}
              className={cn(
                "rounded-xl border p-5 shadow-sm",
                isDark
                  ? "border-slate-700 bg-gradient-to-br from-slate-900 to-slate-950 text-white"
                  : "border-border bg-card",
                isCurrent && !isDark && "ring-1 ring-primary/30",
              )}
            >
              <div className="flex items-center justify-between gap-2">
                <p className={cn("text-sm font-semibold", isDark ? "text-white" : "text-foreground")}>
                  {plan.name}
                </p>
                {isCurrent ? (
                  <span
                    className={cn(
                      "rounded-full px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-wide",
                      isDark ? "bg-white/10 text-white" : "bg-muted text-muted-foreground",
                    )}
                  >
                    Your plan
                  </span>
                ) : null}
              </div>
              <p className={cn("mt-3 text-2xl font-bold tracking-tight", isDark ? "text-white" : "text-foreground")}>
                {plan.priceLabel ?? "$0"}
              </p>
              <ul className="mt-4 space-y-2">
                {plan.features.map((feature) => (
                  <PlanFeature key={feature} muted={isDark}>
                    {feature}
                  </PlanFeature>
                ))}
              </ul>
              {key === "free" || isCurrent ? (
                <p className={cn("mt-5 text-center text-xs", isDark ? "text-slate-400" : "text-muted-foreground")}>
                  {isCurrent ? "Current plan" : "Included with your account"}
                </p>
              ) : (
                <button
                  type="button"
                  disabled={loadingPlan !== null || !candidateId}
                  onClick={() => void runCheckout(key)}
                  className={cn(
                    buttonVariants({ size: "sm" }),
                    "mt-5 flex w-full",
                    isDark ? "bg-white text-slate-900 hover:bg-white/90" : "",
                  )}
                >
                  {loadingPlan === key ? (
                    <Loader2 className="size-4 animate-spin" />
                  ) : (
                    `Upgrade to ${plan.name}`
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
