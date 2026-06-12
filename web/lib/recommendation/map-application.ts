import type { UserApplicationApi } from "@/lib/recommendation/api"
import type { Effort, EmploymentType, Job, RemoteType } from "@/lib/jobs-data"
import { mapApiSeniorityToUi } from "@/lib/profile/seniority"

export function mapApplicationToUi(application: UserApplicationApi): Job & { roleCategory: string } {
  const effort: Effort = "MEDIUM"
  const remote = "unclear" as RemoteType
  const skills = [...(application.tech_stack ?? []), ...(application.skills ?? [])].slice(0, 8)
  const jobId = application.normalized_job_id ?? application.id

  return {
    id: jobId,
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
    description_html: application.description_text ?? "",
    is_saved: false,
    is_applied: true,
    roleCategory: "Applied",
  }
}
