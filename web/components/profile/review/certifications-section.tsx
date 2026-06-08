"use client"

import type { CertificationChange } from "@/lib/profile/profile-data"
import { DecisionControls, KindBadge } from "@/components/profile/review/decision-controls"
import { SectionHeader } from "@/components/profile/review/skills-section"
import { cn } from "@/lib/utils"
import { Award } from "lucide-react"

interface CertificationsSectionProps {
  certifications: CertificationChange[]
  onDecision: (id: string, status: CertificationChange["status"]) => void
  onApproveAll: () => void
  onRejectAll: () => void
}

export function CertificationsSection({
  certifications,
  onDecision,
  onApproveAll,
  onRejectAll,
}: CertificationsSectionProps) {
  return (
    <div>
      <SectionHeader
        title="Certifications"
        onApproveAll={onApproveAll}
        onRejectAll={onRejectAll}
      />
      <div className="space-y-3">
        {certifications.map((c) => (
          <article
            key={c.id}
            className={cn(
              "flex flex-wrap items-center justify-between gap-3 rounded-xl border p-4 transition-colors",
              c.status === "approved"
                ? "border-add/40 bg-add-muted/20"
                : c.status === "rejected"
                  ? "border-border bg-secondary/40 opacity-70"
                  : "border-border bg-card",
            )}
          >
            <div className="flex items-center gap-3">
              <span className="flex size-9 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
                <Award className="size-4.5" aria-hidden="true" />
              </span>
              <div>
                <div className="mb-1">
                  <KindBadge kind={c.kind} withLabel={false} />
                </div>
                <h4 className="text-sm font-semibold text-foreground">{c.name}</h4>
                <p className="text-xs text-muted-foreground">Issued by {c.issuer}</p>
              </div>
            </div>
            <DecisionControls
              size="sm"
              status={c.status}
              onApprove={() => onDecision(c.id, "approved")}
              onReject={() => onDecision(c.id, "rejected")}
            />
          </article>
        ))}
      </div>
    </div>
  )
}
