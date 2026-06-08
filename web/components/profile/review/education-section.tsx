"use client"

import type { EducationChange } from "@/lib/profile/profile-data"
import { DecisionControls, KindBadge } from "@/components/profile/review/decision-controls"
import { SectionHeader } from "@/components/profile/review/skills-section"
import { cn } from "@/lib/utils"
import { GraduationCap } from "lucide-react"

interface EducationSectionProps {
  education: EducationChange[]
  onDecision: (id: string, status: EducationChange["status"]) => void
  onApproveAll: () => void
  onRejectAll: () => void
}

export function EducationSection({
  education,
  onDecision,
  onApproveAll,
  onRejectAll,
}: EducationSectionProps) {
  if (education.length === 0) return null

  return (
    <div>
      <SectionHeader title="Education" onApproveAll={onApproveAll} onRejectAll={onRejectAll} />
      <div className="space-y-3">
        {education.map((e) => (
          <article
            key={e.id}
            className={cn(
              "flex flex-wrap items-center justify-between gap-3 rounded-xl border p-4 transition-colors",
              e.status === "approved"
                ? "border-add/40 bg-add-muted/20"
                : e.status === "rejected"
                  ? "border-border bg-secondary/40 opacity-70"
                  : "border-border bg-card",
            )}
          >
            <div className="flex items-center gap-3">
              <span className="flex size-9 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
                <GraduationCap className="size-4.5" aria-hidden="true" />
              </span>
              <div>
                <div className="mb-1">
                  <KindBadge kind={e.kind} withLabel={false} />
                </div>
                <h4 className="text-sm font-semibold text-foreground">{e.degree || "Degree"}</h4>
                <p className="text-xs text-muted-foreground">
                  {e.university}
                  {e.graduationDate ? ` · ${e.graduationDate}` : ""}
                </p>
                {e.kind === "update" && e.previousDegree ? (
                  <p className="mt-1 text-xs text-update-foreground">
                    Updated from {e.previousDegree}
                    {e.previousUniversity ? ` at ${e.previousUniversity}` : ""}
                  </p>
                ) : null}
              </div>
            </div>
            <DecisionControls
              size="sm"
              status={e.status}
              onApprove={() => onDecision(e.id, "approved")}
              onReject={() => onDecision(e.id, "rejected")}
            />
          </article>
        ))}
      </div>
    </div>
  )
}
