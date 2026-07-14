import { ApiError } from "@/lib/profile/api"
import type { PaidPlan, PlanTier } from "@/lib/plans/company-watch"

const BASE_URL =
  typeof window !== "undefined"
    ? "/api/profile"
    : (process.env.PROFILE_API_URL ?? process.env.NEXT_PUBLIC_PROFILE_API_URL ?? "http://localhost:8001")

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers)
  if (typeof window === "undefined") {
    const API_KEY =
      process.env.PROFILE_API_KEY ?? process.env.NEXT_PUBLIC_PROFILE_API_KEY ?? "dev-key-change-me"
    headers.set("X-API-Key", API_KEY)
  }
  if (init?.body && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json")
  }

  const response = await fetch(`${BASE_URL}${path}`, { ...init, headers })
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try {
      const body = await response.json()
      if (typeof body.detail === "string") {
        message = body.detail
      }
    } catch {
      // ignore
    }
    throw new ApiError(response.status, message)
  }
  return response.json() as Promise<T>
}

export interface BillingStatus {
  candidate_id: string
  plan_tier: PlanTier | string
  subscription_status: string
  plan_expires_at: string | null
  can_upgrade: boolean
  can_manage: boolean
  stripe_configured: boolean
  effective_plan_tier: PlanTier | string
}

export function fetchBillingStatus(candidateId: string) {
  return request<BillingStatus>(`/billing/status?candidate_id=${encodeURIComponent(candidateId)}`)
}

export async function startCheckout(candidateId: string, plan: PaidPlan): Promise<string> {
  const result = await request<{ url: string }>("/billing/checkout-session", {
    method: "POST",
    body: JSON.stringify({ candidate_id: candidateId, plan }),
  })
  return result.url
}

export async function openBillingPortal(candidateId: string): Promise<string> {
  const result = await request<{ url: string }>("/billing/portal-session", {
    method: "POST",
    body: JSON.stringify({ candidate_id: candidateId }),
  })
  return result.url
}
