import type { DashboardJobApi, RecommendedJobApi } from "@/lib/recommendation/api"
import { resolveJobDescription } from "@/lib/recommendation/parse-description"
import type { Effort, EmploymentType, Job, RemoteType } from "@/lib/jobs-data"
import { mapApiSeniorityToUi } from "@/lib/profile/seniority"

function inferEmploymentType(pools: string[]): EmploymentType {
  if (pools.some((p) => p.endsWith("_INTERNSHIP"))) return "INTERNSHIP"
  return "FULLTIME"
}

function inferRoleCategory(normalizedRoles: string[]): string {
  if (normalizedRoles.includes("BACKEND_ENGINEER")) return "Backend Engineer"
  if (normalizedRoles.includes("FRONTEND_ENGINEER")) return "Frontend Engineer"
  if (normalizedRoles.includes("ML_ENGINEER")) return "ML Engineer"
  if (normalizedRoles.includes("DATA_ENGINEER")) return "Data Engineer"
  if (normalizedRoles.includes("DATA_SCIENTIST")) return "Data Scientist"
  if (normalizedRoles.includes("FULLSTACK_ENGINEER")) return "Full Stack"
  if (normalizedRoles.includes("SWE")) return "SWE"
  return normalizedRoles[0] ?? "SWE"
}

export function mapApiJobToUi(
  job: DashboardJobApi,
  extras?: { personal_score?: number; match_reasons?: string[] },
): Job & { roleCategory: string } {
  const effort = (job.application_effort ?? "MEDIUM") as Effort
  const remote = (job.remote_type ?? "unclear") as RemoteType
  const skills = [...(job.tech_stack ?? []), ...(job.skills ?? [])].slice(0, 8)
  const matchReasons = extras?.match_reasons ?? job.job_capabilities?.slice(0, 5) ?? []

  const description = resolveJobDescription({
    description_text: job.description_text,
    description_preview: job.description_preview,
    responsibilities: job.responsibilities,
    required_qualifications: job.required_qualifications,
    preferred_qualifications: job.preferred_qualifications,
    benefits: job.benefits,
  })

  return {
    id: job.id,
    title: job.title,
    company: job.company_name,
    location: job.location ?? "Location not specified",
    salary_min: job.salary_min,
    salary_max: job.salary_max,
    employment_type: inferEmploymentType(job.retrieval_pools ?? []),
    seniority_level: mapApiSeniorityToUi(job.seniority),
    remote_type: remote,
    application_effort: effort,
    posting_url: job.posting_url ?? "#",
    posted_at: job.posted_at!,
    opportunity_score: job.opportunity_score ?? 0,
    personal_score: extras?.personal_score ?? job.opportunity_score ?? 0,
    match_reasons: matchReasons,
    recommendation_reason:
      matchReasons.length > 0
        ? `Strong ${matchReasons[0].toLowerCase()} alignment.`
        : "Matches your profile preferences.",
    skills,
    responsibilities: description.responsibilities,
    required_qualifications: description.required_qualifications,
    preferred_qualifications: description.preferred_qualifications,
    benefits: description.benefits,
    sponsorship_status: job.sponsorship_status ?? "unclear",
    sponsorship_confidence: job.sponsorship_confidence ?? "low",
    h1b_sponsorship: job.h1b_sponsorship ?? null,
    company_info: job.company_info ?? null,
    about_summary: description.about,
    description_html: description.fallbackHtml,
    is_saved: false,
    is_applied: false,
    roleCategory: inferRoleCategory(job.normalized_roles ?? []),
  }
}

export function mapRecommendedApiJob(job: RecommendedJobApi) {
  return mapApiJobToUi(job, {
    personal_score: job.personal_score,
    match_reasons: job.match_reasons,
  })
}
