import type { UserApplicationApi } from "@/lib/recommendation/api"
import { resolveJobDescription } from "@/lib/recommendation/parse-description"
import type { CompanyEnrichmentInfo, Effort, EmploymentType, Job, RemoteType } from "@/lib/jobs-data"
import { mapApiSeniorityToUi } from "@/lib/profile/seniority"

function companyInfoFromLogoUrl(logoUrl: string | null | undefined): CompanyEnrichmentInfo | null {
  if (!logoUrl?.trim()) return null
  return {
    founded_year: null,
    headquarters: null,
    employee_count_range: null,
    one_line_description: null,
    website: null,
    linkedin_url: null,
    glassdoor_rating: null,
    logo_url: logoUrl.trim(),
  }
}

export function mapApplicationToUi(application: UserApplicationApi): Job & { roleCategory: string } {
  const effort: Effort = "MEDIUM"
  const remote = "unclear" as RemoteType
  const skills = [...(application.tech_stack ?? []), ...(application.skills ?? [])].slice(0, 8)
  const jobId = application.normalized_job_id ?? application.id

  const description = resolveJobDescription({
    description_text: application.description_text,
  })

  return {
    id: jobId,
    application_id: application.id,
    title: application.job_title,
    company: application.company_name,
    location: application.location ?? "Location not specified",
    salary_min: application.salary_min,
    salary_max: application.salary_max,
    employment_type: "FULLTIME" as EmploymentType,
    seniority_level: mapApiSeniorityToUi(application.seniority ?? "unclear"),
    remote_type: remote,
    application_effort: effort,
    posting_url: application.posting_url ?? "#",
    posted_at: application.applied_at,
    opportunity_score: 0,
    personal_score: 0,
    match_reasons: [],
    recommendation_reason: "You applied to this role.",
    skills,
    responsibilities: description.responsibilities,
    required_qualifications: description.required_qualifications,
    preferred_qualifications: description.preferred_qualifications,
    benefits: description.benefits,
    sponsorship_status: "unclear",
    sponsorship_confidence: "low",
    requires_clearance: false,
    requires_citizenship: false,
    h1b_sponsorship: null,
    company_info: companyInfoFromLogoUrl(application.logo_url),
    about_summary: description.about,
    description_html: description.fallbackHtml,
    is_saved: false,
    is_applied: true,
    application_status: application.status,
    roleCategory: "Applied",
  }
}
