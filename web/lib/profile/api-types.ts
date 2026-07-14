export interface CandidateResponse {
  id: string
  email: string
  name: string
  plan_tier?: string
  plan_expires_at?: string | null
  subscription_status?: string
  created_at: string
  updated_at: string
}

export interface ResumeResponse {
  id: string
  candidate_id: string
  file_path: string
  original_filename: string
  display_label: string | null
  file_size_bytes: number
  extraction_method: string | null
  raw_text_char_count: number | null
  extraction_status: string
  uploaded_at: string
  parsed_at: string | null
}

export interface ResumeUploadResponse {
  resume: ResumeResponse
  patch_id: string
}

export interface PatchOperationResponse {
  id: string
  op: string
  category?: string | null
  value?: string | null
  evidence_id?: string | null
  field?: string | null
  from_value?: unknown
  to?: unknown
  suggested_value?: unknown
  data?: Record<string, unknown> | null
  reason?: string | null
}

export interface PendingPatchResponse {
  patch_id: string
  candidate_id: string
  source_resume_id: string
  profile_version_before: number | null
  status: string
  created_at: string
  skills: PatchOperationResponse[]
  experiences: PatchOperationResponse[]
  projects: PatchOperationResponse[]
  certifications: PatchOperationResponse[]
  education: PatchOperationResponse[]
  constraints: PatchOperationResponse[]
  preferences: PatchOperationResponse[]
}

export interface PatchCommitResponse {
  patch_id: string
  profile_version: number
  status: string
}

export interface ProfileResponse {
  id: string
  candidate_id: string
  version: number
  is_current: boolean
  schema_version: string
  constraints: Record<string, unknown>
  preferences: Record<string, unknown>
  skills: Record<string, string[]>
  education: Record<string, unknown>
  patch_id: string | null
  created_at: string
}

export interface CapabilityResponse {
  capability_name: string
  supporting_evidence: string[]
  profile_version: number
  taxonomy_version: string
  computed_at: string
}

export interface CapabilitiesListResponse {
  capabilities: CapabilityResponse[]
}

export interface EvidenceResponse {
  id: string
  evidence_type: string
  normalized_data: Record<string, unknown>
  source_resume_id: string
  is_approved: boolean
  approved_at: string | null
}

export interface EvidenceListResponse {
  evidence: EvidenceResponse[]
}
