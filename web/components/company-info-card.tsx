import { ExternalLink } from "lucide-react"
import type { CompanyEnrichmentInfo } from "@/lib/recommendation/api"

export function CompanyInfoCard({ info }: { info: CompanyEnrichmentInfo }) {
  const facts: string[] = []
  if (info.founded_year != null) facts.push(`Founded ${info.founded_year}`)
  if (info.headquarters) facts.push(info.headquarters)
  if (info.employee_count_range) facts.push(`${info.employee_count_range} employees`)

  const hasContent =
    facts.length > 0
    || info.one_line_description
    || info.website
    || info.linkedin_url
    || info.glassdoor_rating != null

  if (!hasContent) return null

  return (
    <section className="mb-6 rounded-xl border border-border/80 bg-card p-4">
      <h3 className="mb-2 text-sm font-semibold text-foreground">Company</h3>
      {facts.length > 0 ? (
        <p className="text-xs text-muted-foreground">{facts.join(" · ")}</p>
      ) : null}
      {info.one_line_description ? (
        <p className="mt-2 text-sm text-muted-foreground">{info.one_line_description}</p>
      ) : null}
      {info.glassdoor_rating != null ? (
        <p className="mt-2 text-xs text-muted-foreground">
          Glassdoor: {info.glassdoor_rating.toFixed(1)} / 5
        </p>
      ) : null}
      <div className="mt-3 flex flex-wrap gap-3">
        {info.website ? (
          <a
            href={info.website}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
          >
            Website <ExternalLink className="size-3" />
          </a>
        ) : null}
        {info.linkedin_url ? (
          <a
            href={info.linkedin_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
          >
            LinkedIn <ExternalLink className="size-3" />
          </a>
        ) : null}
      </div>
    </section>
  )
}
