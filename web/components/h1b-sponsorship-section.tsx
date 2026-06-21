import type { H1BSponsorshipInfo, SponsorshipStatus } from "@/lib/recommendation/api"

const STATUS_LABEL: Record<SponsorshipStatus, string> = {
  yes: "Yes",
  no: "No",
  unclear: "Unclear",
}

export function SponsorshipStatusPill({
  status,
  confidence,
}: {
  status: SponsorshipStatus
  confidence: string
}) {
  return (
    <div className="mb-4 flex flex-wrap items-center gap-2">
      <span className="text-xs font-medium text-muted-foreground">Posting mentions sponsorship:</span>
      <span className="rounded-md bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
        {STATUS_LABEL[status]}
        {confidence === "high" ? " (high confidence)" : ""}
      </span>
    </div>
  )
}

export function H1bSponsorshipSection({ info }: { info: H1BSponsorshipInfo }) {
  const approvalPct =
    info.approval_rate_3yr != null ? `${Math.round(info.approval_rate_3yr * 100)}%` : "N/A"

  return (
    <section className="mb-6 rounded-xl border border-border/80 bg-secondary/30 p-4">
      <h3 className="mb-2 text-sm font-semibold text-foreground">H-1B Sponsorship</h3>
      <ul className="space-y-1.5 text-sm text-muted-foreground">
        <li>
          <span className="font-medium text-foreground">Role category:</span> {info.pool_family}
        </li>
        <li>
          <span className="font-medium text-foreground">LCA filings (3 yr):</span>{" "}
          {info.total_lca_3yr.toLocaleString()}
        </li>
        <li>
          <span className="font-medium text-foreground">Approval rate (3 yr):</span> {approvalPct}
        </li>
        {info.is_top_sponsor ? (
          <li className="font-medium text-emerald-700 dark:text-emerald-400">Top sponsor for this role</li>
        ) : null}
        {info.years_covered.length > 0 ? (
          <li>
            <span className="font-medium text-foreground">Years covered:</span>{" "}
            {info.years_covered.join(", ")}
          </li>
        ) : null}
      </ul>
      <p className="mt-3 text-xs text-muted-foreground/80">
        Data powered by U.S. Department of Labor LCA disclosures
      </p>
    </section>
  )
}
