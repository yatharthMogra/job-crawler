"use client"

import type { ProjectChange } from "@/lib/profile-data"
import { DecisionControls, KindBadge } from "@/components/review/decision-controls"
import { SectionHeader } from "@/components/review/skills-section"
import { cn } from "@/lib/utils"

interface ProjectsSectionProps {
  projects: ProjectChange[]
  onDecision: (id: string, status: ProjectChange["status"]) => void
  onApproveAll: () => void
  onRejectAll: () => void
}

export function ProjectsSection({
  projects,
  onDecision,
  onApproveAll,
  onRejectAll,
}: ProjectsSectionProps) {
  return (
    <div>
      <SectionHeader title="Projects" onApproveAll={onApproveAll} onRejectAll={onRejectAll} />
      <div className="space-y-4">
        {projects.map((p) => (
          <article
            key={p.id}
            className={cn(
              "rounded-xl border p-4 transition-colors",
              p.status === "approved"
                ? "border-add/40 bg-add-muted/20"
                : p.status === "rejected"
                  ? "border-border bg-secondary/40 opacity-70"
                  : "border-border bg-card",
            )}
          >
            <div className="mb-3">
              <KindBadge kind={p.kind} />
            </div>
            <h4 className="text-base font-semibold text-foreground">{p.name}</h4>
            <p className="mt-0.5 text-sm text-muted-foreground">
              {p.type} · {p.domain}
            </p>
            <div className="mt-3">
              <p className="mb-1.5 text-xs font-medium text-muted-foreground">Keywords</p>
              <div className="flex flex-wrap gap-1.5">
                {p.keywords.map((k) => (
                  <span
                    key={k}
                    className="rounded-md bg-secondary px-2 py-0.5 text-xs text-secondary-foreground"
                  >
                    {k}
                  </span>
                ))}
              </div>
            </div>
            <div className="mt-4 border-t border-border pt-3">
              <DecisionControls
                status={p.status}
                onApprove={() => onDecision(p.id, "approved")}
                onReject={() => onDecision(p.id, "rejected")}
              />
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}
