import type {
  CandidateResponse,
  CapabilitiesListResponse,
  EvidenceListResponse,
  PatchCommitResponse,
  PendingPatchResponse,
  ProfileResponse,
  ResumeUploadResponse,
} from "@/lib/profile/api-types"

const BASE_URL =
  typeof window !== "undefined"
    ? "/api/profile"
    : (process.env.PROFILE_API_URL ?? process.env.NEXT_PUBLIC_PROFILE_API_URL ?? "http://localhost:8001")

export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
    this.name = "ApiError"
  }
}

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
      // ignore parse errors
    }
    throw new ApiError(response.status, message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export function createCandidate(name: string, email: string) {
  return request<CandidateResponse>("/candidates", {
    method: "POST",
    body: JSON.stringify({ name, email }),
  })
}

export interface ChallengeResponse {
  challenge_token: string
  expires_in: number
}

export function requestSignupOtp(name: string, email: string, password: string) {
  return request<ChallengeResponse>("/auth/signup/request", {
    method: "POST",
    body: JSON.stringify({ name, email, password }),
  })
}

export function verifySignupOtp(email: string, code: string, challengeToken: string) {
  return request<CandidateResponse>("/auth/signup/verify", {
    method: "POST",
    body: JSON.stringify({ email, code, challenge_token: challengeToken }),
  })
}

export function requestLoginOtp(email: string, password: string) {
  return request<ChallengeResponse>("/auth/login/request", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  })
}

export function verifyLoginOtp(email: string, code: string, challengeToken: string) {
  return request<CandidateResponse>("/auth/login/verify", {
    method: "POST",
    body: JSON.stringify({ email, code, challenge_token: challengeToken }),
  })
}

export function getCandidate(candidateId: string) {
  return request<CandidateResponse>(`/candidates/${candidateId}`)
}

export function uploadResume(candidateId: string, file: File) {
  const form = new FormData()
  form.append("file", file)
  return request<ResumeUploadResponse>(`/candidates/${candidateId}/resumes/upload`, {
    method: "POST",
    body: form,
  })
}

export function getPendingPatch(candidateId: string) {
  return request<PendingPatchResponse>(`/candidates/${candidateId}/patches/pending`)
}

export function commitPatch(candidateId: string, patchId: string, approvedOperationIds: string[]) {
  return request<PatchCommitResponse>(`/candidates/${candidateId}/patches/${patchId}/commit`, {
    method: "POST",
    body: JSON.stringify({ approved_operation_ids: approvedOperationIds }),
  })
}

export function discardPatch(candidateId: string, patchId: string) {
  return request<void>(`/candidates/${candidateId}/patches/${patchId}`, { method: "DELETE" })
}

export function getProfile(candidateId: string) {
  return request<ProfileResponse>(`/candidates/${candidateId}/profile`)
}

export function getCapabilities(candidateId: string) {
  return request<CapabilitiesListResponse>(`/candidates/${candidateId}/capabilities`)
}

export function getEvidence(candidateId: string, approvedOnly = true) {
  return request<EvidenceListResponse>(
    `/candidates/${candidateId}/evidence?approved_only=${approvedOnly}`,
  )
}

export function listResumes(candidateId: string) {
  return request<import("@/lib/profile/api-types").ResumeResponse[]>(`/candidates/${candidateId}/resumes`)
}

export function patchConstraints(candidateId: string, updates: Record<string, unknown>) {
  return request<ProfileResponse>(`/candidates/${candidateId}/profile/constraints`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  })
}

export function patchPreferences(candidateId: string, updates: Record<string, unknown>) {
  return request<ProfileResponse>(`/candidates/${candidateId}/profile/preferences`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  })
}

export function patchEducation(candidateId: string, updates: Record<string, unknown>) {
  return request<ProfileResponse>(`/candidates/${candidateId}/profile/education`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  })
}

export function patchResumeLabel(
  candidateId: string,
  resumeId: string,
  displayLabel: string | null,
) {
  return request<import("@/lib/profile/api-types").ResumeResponse>(
    `/candidates/${candidateId}/resumes/${resumeId}`,
    {
      method: "PATCH",
      body: JSON.stringify({ display_label: displayLabel }),
    },
  )
}
