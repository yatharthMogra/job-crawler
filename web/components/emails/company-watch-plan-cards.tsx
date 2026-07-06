"use client"

import type { ReactNode } from "react"
import { Check, Sparkles } from "lucide-react"
import { buttonVariants } from "@/components/ui/button"
import { COMPANY_WATCH_PLANS, isPlusTier, PLUS_WAITLIST_MAILTO } from "@/lib/plans/company-watch"
import { cn } from "@/lib/utils"

interface CompanyWatchPlanCardsProps {
  planTier: string
  watchedCount: number
  maxCompanies: number
  className?: string
}

function PlanFeature({ children }: { children: ReactNode }) {
  return (
    <li className="flex items-start gap-2 text-sm text-muted-foreground">
      <Check className="mt-0.5 size-4 shrink-0 text-primary" strokeWidth={2.5} />
      <span>{children}</span>
    </li>
  )
}

export function CompanyWatchPlanCards({
  planTier,
  watchedCount,
  maxCompanies,
  className,
}: CompanyWatchPlanCardsProps) {
  const onPlus = isPlusTier(planTier)
  const free = COMPANY_WATCH_PLANS.free
  const plus = COMPANY_WATCH_PLANS.plus
  const atFreeLimit = !onPlus && watchedCount >= maxCompanies

  if (onPlus) {
    return (
      <div
        className={cn(
          "rounded-xl border border-primary/20 bg-gradient-to-br from-primary/5 to-primary/10 p-5",
          className,
        )}
      >
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Sparkles className="size-4 text-primary" />
            <p className="text-sm font-semibold text-foreground">{plus.name}</p>
          </div>
          <span className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
            {watchedCount}/{maxCompanies} companies watched
          </span>
        </div>
        <p className="mt-2 text-sm text-muted-foreground">{plus.deliveryLabel}</p>
      </div>
    )
  }

  return (
    <div className={cn("grid gap-4 sm:grid-cols-2", className)}>
      <div className="rounded-xl border border-border bg-card p-5 shadow-sm">
        <div className="flex items-center justify-between gap-2">
          <p className="text-sm font-semibold text-foreground">{free.name}</p>
          <span className="rounded-full bg-muted px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-wide text-muted-foreground">
            Your plan
          </span>
        </div>
        <p className="mt-3 text-2xl font-bold tracking-tight text-foreground">
          {free.maxCompanies}{" "}
          <span className="text-base font-medium text-muted-foreground">companies</span>
        </p>
        <ul className="mt-4 space-y-2">
          <PlanFeature>Watch up to {free.maxCompanies} companies</PlanFeature>
          <PlanFeature>{free.deliveryLabel}</PlanFeature>
        </ul>
        <p className="mt-4 text-xs text-muted-foreground">
          {watchedCount} of {maxCompanies} slots used
        </p>
        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-primary transition-all"
            style={{ width: `${Math.min(100, (watchedCount / maxCompanies) * 100)}%` }}
          />
        </div>
      </div>

      <div
        className={cn(
          "rounded-xl border bg-gradient-to-br from-slate-900 to-slate-950 p-5 text-white shadow-lg",
          atFreeLimit ? "border-violet-400/40 ring-1 ring-violet-400/20" : "border-slate-700",
        )}
      >
        <div className="flex items-center gap-2">
          <Sparkles className="size-4 text-violet-300" />
          <p className="text-sm font-semibold">{plus.name}</p>
        </div>
        <p className="mt-3 text-2xl font-bold tracking-tight">
          {plus.priceLabel}
        </p>
        <ul className="mt-4 space-y-2">
          <li className="flex items-start gap-2 text-sm text-slate-300">
            <Check className="mt-0.5 size-4 shrink-0 text-violet-300" strokeWidth={2.5} />
            <span>Watch up to {plus.maxCompanies} companies</span>
          </li>
          <li className="flex items-start gap-2 text-sm text-slate-300">
            <Check className="mt-0.5 size-4 shrink-0 text-violet-300" strokeWidth={2.5} />
            <span>{plus.deliveryLabel}</span>
          </li>
          <li className="flex items-start gap-2 text-sm text-slate-300">
            <Check className="mt-0.5 size-4 shrink-0 text-violet-300" strokeWidth={2.5} />
            <span>Higher daily email limit</span>
          </li>
        </ul>
        <a
          href={PLUS_WAITLIST_MAILTO}
          className={cn(
            buttonVariants({ size: "sm" }),
            "mt-5 flex w-full bg-white text-slate-900 hover:bg-white/90",
          )}
        >
          Join the waitlist
        </a>
        <p className="mt-2 text-center text-[11px] text-slate-400">
          Billing not live yet — we&apos;ll email you when Plus launches.
        </p>
      </div>
    </div>
  )
}
