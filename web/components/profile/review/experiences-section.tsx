"use client"

import { useState } from "react"
import type { ExperienceChange } from "@/lib/profile/profile-data"
import { DecisionControls, KindBadge } from "@/components/profile/review/decision-controls"
import { SectionHeader } from "@/components/profile/review/skills-section"
import { TagInput } from "@/components/profile/review/tag-input"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { ArrowRight, Building2, Pencil } from "lucide-react"

interface ExperiencesSectionProps {
  experiences: ExperienceChange[]
  onDecision: (id: string, status: ExperienceChange["status"]) => void
  onEdit: (exp: ExperienceChange) => void
  onApproveAll: () => void
  onRejectAll: () => void
}

export function ExperiencesSection({
  experiences,
  onDecision,
  onEdit,
  onApproveAll,
  onRejectAll,
}: ExperiencesSectionProps) {
  return (
    <div>
      <SectionHeader title="Experiences" onApproveAll={onApproveAll} onRejectAll={onRejectAll} />
      <div className="space-y-4">
        {experiences.map((exp) => (
          <ExperienceCard
            key={exp.id}
            exp={exp}
            onApprove={() => onDecision(exp.id, "approved")}
            onReject={() => onDecision(exp.id, "rejected")}
            onSave={(updated) => onEdit(updated)}
          />
        ))}
      </div>
    </div>
  )
}

function ExperienceCard({
  exp,
  onApprove,
  onReject,
  onSave,
}: {
  exp: ExperienceChange
  onApprove: () => void
  onReject: () => void
  onSave: (e: ExperienceChange) => void
}) {
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(exp)
  const [edited, setEdited] = useState(false)

  function save() {
    onSave(draft)
    setEditing(false)
    setEdited(true)
  }

  const e = edited ? draft : exp

  return (
    <article
      className={cn(
        "rounded-xl border p-4 transition-colors",
        exp.status === "approved"
          ? "border-add/40 bg-add-muted/20"
          : exp.status === "rejected"
            ? "border-border bg-secondary/40 opacity-70"
            : "border-border bg-card",
      )}
    >
      <div className="mb-3 flex items-center justify-between">
        <KindBadge kind={exp.kind} />
        {edited ? (
          <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
            <Pencil className="size-3" aria-hidden="true" /> Edited
          </span>
        ) : null}
      </div>

      {editing ? (
        <div className="space-y-3">
          <div className="grid gap-3 sm:grid-cols-2">
            <Field label="Title">
              <Input
                value={draft.title}
                onChange={(ev) => setDraft({ ...draft, title: ev.target.value })}
              />
            </Field>
            <Field label="Company">
              <Input
                value={draft.company}
                onChange={(ev) => setDraft({ ...draft, company: ev.target.value })}
              />
            </Field>
            <Field label="Duration (months)">
              <Input
                type="number"
                value={draft.durationMonths}
                onChange={(ev) =>
                  setDraft({ ...draft, durationMonths: Number(ev.target.value) || 0 })
                }
              />
            </Field>
          </div>
          <TagInput
            label="Domains"
            tags={draft.domains}
            onChange={(domains) => setDraft({ ...draft, domains })}
          />
          <TagInput
            label="Keywords"
            tags={draft.keywords}
            onChange={(keywords) => setDraft({ ...draft, keywords })}
          />
          <div className="flex gap-2 pt-1">
            <Button size="sm" onClick={save}>
              Save edit
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => {
                setDraft(e)
                setEditing(false)
              }}
            >
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <>
          <h4 className="text-base font-semibold text-foreground">
            <UpdateText
              kind={exp.kind}
              previous={exp.previousTitle}
              current={e.title}
            />
          </h4>
          <p className="mt-0.5 flex flex-wrap items-center gap-1.5 text-sm text-muted-foreground">
            <Building2 className="size-3.5 shrink-0" aria-hidden="true" />
            <UpdateText
              kind={exp.kind}
              previous={exp.previousCompany}
              current={e.company}
            />
            <span aria-hidden="true">·</span>
            {exp.kind === "update" && exp.previousDurationMonths !== undefined ? (
              <span className="inline-flex items-center gap-1">
                <span className="text-muted-foreground/70 line-through">
                  {exp.previousDurationMonths} months
                </span>
                <ArrowRight className="size-3 text-update-foreground" aria-hidden="true" />
                <span className="font-medium text-update-foreground">
                  {e.durationMonths} months
                </span>
              </span>
            ) : (
              <span>{e.durationMonths} months</span>
            )}
          </p>

          {e.domains.length > 0 ? (
            <p className="mt-1 text-sm text-muted-foreground">
              {exp.kind === "update" && exp.previousDomains !== undefined ? (
                <span className="inline-flex flex-wrap items-center gap-1">
                  <span className="text-muted-foreground/70 line-through">
                    {exp.previousDomains.join(" · ") || "None"}
                  </span>
                  <ArrowRight className="size-3 shrink-0 text-update-foreground" aria-hidden="true" />
                  <span className="font-medium text-update-foreground">
                    {e.domains.join(" · ")}
                  </span>
                </span>
              ) : (
                e.domains.join(" · ")
              )}
            </p>
          ) : null}

          {exp.kind === "update" && exp.newKeywords?.length ? (
            <p className="mt-3 text-sm">
              <span className="font-medium text-update-foreground">New keywords: </span>
              {exp.newKeywords.join(", ")}
            </p>
          ) : (
            <div className="mt-3">
              <p className="mb-1.5 text-xs font-medium text-muted-foreground">Keywords</p>
              <div className="flex flex-wrap gap-1.5">
                {e.keywords.map((k) => (
                  <span
                    key={k}
                    className="rounded-md bg-secondary px-2 py-0.5 text-xs text-secondary-foreground"
                  >
                    {k}
                  </span>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {!editing ? (
        <div className="mt-4 border-t border-border pt-3">
          <DecisionControls
            status={exp.status}
            onApprove={onApprove}
            onReject={onReject}
            onEdit={() => setEditing(true)}
          />
        </div>
      ) : null}
    </article>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="mb-1.5 block text-xs font-medium text-muted-foreground">{label}</label>
      {children}
    </div>
  )
}

function UpdateText({
  kind,
  previous,
  current,
}: {
  kind: ExperienceChange["kind"]
  previous?: string
  current: string
}) {
  if (kind === "update" && previous !== undefined && previous !== current) {
    return (
      <span className="inline-flex flex-wrap items-center gap-1">
        <span className="text-muted-foreground/70 line-through">{previous}</span>
        <ArrowRight className="size-3 shrink-0 text-update-foreground" aria-hidden="true" />
        <span className="font-medium text-update-foreground">{current}</span>
      </span>
    )
  }

  return <>{current}</>
}
