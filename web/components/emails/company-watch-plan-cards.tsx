"use client"

import { PlanPricingCards } from "@/components/billing/plan-pricing-cards"
import { useSession } from "@/components/session-provider"
import { cn } from "@/lib/utils"

interface CompanyWatchPlanCardsProps {
  planTier: string
  watchedCount: number
  maxCompanies: number
  className?: string
}

export function CompanyWatchPlanCards({
  planTier,
  watchedCount,
  maxCompanies,
  className,
}: CompanyWatchPlanCardsProps) {
  const { candidateId } = useSession()
  return (
    <PlanPricingCards
      planTier={planTier}
      candidateId={candidateId}
      watchedCount={watchedCount}
      maxCompanies={maxCompanies}
      className={cn(className)}
    />
  )
}
