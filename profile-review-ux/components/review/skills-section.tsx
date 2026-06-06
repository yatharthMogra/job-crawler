"use client"

import type { SkillChange } from "@/lib/profile-data"
import { DecisionControls, KindBadge } from "@/components/review/decision-controls"
import { cn } from "@/lib/utils"

interface SkillsSectionProps {
  skills: SkillChange[]
  onDecision: (id: string, status: SkillChange["status"]) => void
  onApproveAll: () => void
  onRejectAll: () => void
}

export function SkillsSection({ skills, onDecision, onApproveAll, onRejectAll }: SkillsSectionProps) {
  const categories = Array.from(new Set(skills.map((s) => s.category)))

  return (
    <div>
      <SectionHeader title="Skills" onApproveAll={onApproveAll} onRejectAll={onRejectAll} />

      <div className="space-y-5">
        {categories.map((cat) => (
          <div key={cat}>
            <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              {cat}
            </h4>
            <ul className="space-y-1.5">
              {skills
                .filter((s) => s.category === cat)
                .map((skill) => (
                  <li
                    key={skill.id}
                    className={cn(
                      "flex items-center justify-between gap-3 rounded-lg border px-3 py-2 transition-colors",
                      skill.status === "approved"
                        ? "border-add/30 bg-add-muted/30"
                        : skill.status === "rejected"
                          ? "border-border bg-secondary/40 opacity-70"
                          : "border-border bg-card",
                    )}
                  >
                    <span className="flex items-center gap-2 text-sm font-medium text-foreground">
                      <KindBadge kind={skill.kind} withLabel={false} />
                      {skill.name}
                    </span>
                    <DecisionControls
                      size="sm"
                      status={skill.status}
                      onApprove={() => onDecision(skill.id, "approved")}
                      onReject={() => onDecision(skill.id, "rejected")}
                    />
                  </li>
                ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  )
}

export function SectionHeader({
  title,
  onApproveAll,
  onRejectAll,
}: {
  title: string
  onApproveAll: () => void
  onRejectAll: () => void
}) {
  return (
    <div className="mb-4 flex items-center justify-between gap-3 border-b border-border pb-3">
      <h3 className="text-lg font-semibold text-foreground">{title}</h3>
      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={onApproveAll}
          className="rounded-md px-2.5 py-1 text-xs font-medium text-add-foreground hover:bg-add-muted/60"
        >
          Approve all
        </button>
        <button
          type="button"
          onClick={onRejectAll}
          className="rounded-md px-2.5 py-1 text-xs font-medium text-muted-foreground hover:bg-secondary"
        >
          Reject all
        </button>
      </div>
    </div>
  )
}
