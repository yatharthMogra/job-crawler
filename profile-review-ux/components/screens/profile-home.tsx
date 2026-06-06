"use client"

import type { ProfileResponse } from "@/lib/api-types"
import type { ProfileHomeData } from "@/lib/map-profile"
import type { EditSection } from "@/components/profile-edit-dialog"
import { ProfileEditDialog } from "@/components/profile-edit-dialog"
import { Brand } from "@/components/brand"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import { formatRelativeTime } from "@/lib/map-profile"
import { Award, Building2, Pencil, Upload } from "lucide-react"

interface ProfileHomeProps {
  data: ProfileHomeData
  onUploadNew: () => void
  onEditSection: (section: EditSection | null) => void
  editSection: EditSection | null
  onEditSave: (section: EditSection, values: Record<string, unknown>) => Promise<void>
  rawProfile?: ProfileResponse | null
}

export function ProfileHome({
  data,
  onUploadNew,
  onEditSection,
  editSection,
  onEditSave,
  rawProfile,
}: ProfileHomeProps) {
  const { profile } = data
  const maxDepth = Math.max(1, ...profile.capabilities.map((c) => c.depth))

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-background">
        <div className="mx-auto flex max-w-3xl items-center justify-between px-4 py-3 sm:px-6">
          <Brand />
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8 sm:px-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">
              {data.candidateName}
            </h1>
            {data.educationLine ? (
              <p className="mt-1 text-sm text-muted-foreground">{data.educationLine}</p>
            ) : null}
          </div>
          <div className="flex gap-2">
            <Button size="sm" onClick={onUploadNew}>
              <Upload className="size-4" aria-hidden="true" />
              Upload new resume
            </Button>
            <Button size="sm" variant="secondary" onClick={() => onEditSection("preferences")}>
              <Pencil className="size-4" aria-hidden="true" />
              Edit preferences
            </Button>
          </div>
        </div>

        {profile.capabilities.length > 0 ? (
          <Section title="Your Capabilities">
            <TooltipProvider delayDuration={150}>
              <div className="flex flex-col gap-4">
                {profile.capabilities.map((c) => (
                  <div key={c.name} className="w-full">
                    <div className="mb-1.5 flex flex-wrap items-baseline justify-between gap-x-3 gap-y-0.5">
                      <span className="text-sm font-medium text-foreground">{c.name}</span>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <span className="cursor-default text-xs text-muted-foreground">
                            Supported by {c.evidence.slice(0, 2).join(", ")}
                            {c.evidence.length > 2 ? ` +${c.evidence.length - 2}` : ""}
                          </span>
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="text-xs font-medium">Evidence</p>
                          <p className="text-xs text-muted-foreground">{c.evidence.join(", ")}</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                    <div className="h-2.5 w-full overflow-hidden rounded-full bg-secondary">
                      <div
                        className="h-full rounded-full bg-primary transition-all"
                        style={{ width: `${Math.max(18, (c.depth / maxDepth) * 100)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </TooltipProvider>
          </Section>
        ) : null}

        {data.constraints.length > 0 ? (
          <Section title="Constraints" editable onEdit={() => onEditSection("constraints")}>
            <dl className="divide-y divide-border">
              {data.constraints.map((p) => (
                <div key={p.label} className="flex justify-between gap-4 py-2.5">
                  <dt className="text-sm text-muted-foreground">{p.label}</dt>
                  <dd className="text-right text-sm font-medium text-foreground">{p.value}</dd>
                </div>
              ))}
            </dl>
          </Section>
        ) : null}

        {data.preferences.length > 0 ? (
          <Section title="Preferences" editable onEdit={() => onEditSection("preferences")}>
            <dl className="divide-y divide-border">
              {data.preferences.map((p) => (
                <div key={p.label} className="flex justify-between gap-4 py-2.5">
                  <dt className="text-sm text-muted-foreground">{p.label}</dt>
                  <dd className="text-right text-sm font-medium text-foreground">{p.value}</dd>
                </div>
              ))}
            </dl>
          </Section>
        ) : null}

        {profile.experiences.length > 0 ? (
          <Section title="Experience">
            <div className="space-y-3">
              {profile.experiences.map((e) => (
                <Card key={e.id} className="p-4">
                  <h3 className="text-base font-semibold text-foreground">{e.title}</h3>
                  <p className="mt-0.5 flex items-center gap-1.5 text-sm text-muted-foreground">
                    <Building2 className="size-3.5" aria-hidden="true" />
                    {e.company} · {e.durationMonths} months
                    {e.domains.length ? ` · ${e.domains.join(", ")}` : ""}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {e.keywords.slice(0, 5).map((k) => (
                      <Tag key={k}>{k}</Tag>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          </Section>
        ) : null}

        {profile.projects.length > 0 ? (
          <Section title="Projects">
            <div className="space-y-3">
              {profile.projects.map((p) => (
                <Card key={p.id} className="p-4">
                  <h3 className="text-base font-semibold text-foreground">{p.name}</h3>
                  <p className="mt-0.5 text-sm text-muted-foreground">
                    {p.type} · {p.domain}
                  </p>
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {p.keywords.slice(0, 5).map((k) => (
                      <Tag key={k}>{k}</Tag>
                    ))}
                  </div>
                </Card>
              ))}
            </div>
          </Section>
        ) : null}

        {profile.skills.length > 0 ? (
          <Section title="Skills">
            <div className="space-y-4">
              {profile.skills.map((group) => (
                <div key={group.category}>
                  <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                    {group.category}
                  </h4>
                  <div className="flex flex-wrap gap-1.5">
                    {group.names.map((n) => (
                      <Tag key={n}>{n}</Tag>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Section>
        ) : null}

        {profile.certifications.length > 0 ? (
          <Section title="Certifications">
            <div className="space-y-2">
              {profile.certifications.map((c) => (
                <div
                  key={c.id}
                  className="flex items-center gap-3 rounded-lg border border-border bg-card p-3"
                >
                  <span className="flex size-8 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
                    <Award className="size-4" aria-hidden="true" />
                  </span>
                  <div>
                    <p className="text-sm font-medium text-foreground">{c.name}</p>
                    <p className="text-xs text-muted-foreground">{c.issuer}</p>
                  </div>
                </div>
              ))}
            </div>
          </Section>
        ) : null}

        <p className="mt-10 text-center text-xs text-muted-foreground">
          Profile version {data.version} · Last updated {formatRelativeTime(data.lastUpdated)} · Built
          from {data.resumeCount} {data.resumeCount === 1 ? "resume" : "resumes"}
        </p>
      </main>

      <ProfileEditDialog
        section={editSection}
        onClose={() => onEditSection(null)}
        onSave={onEditSave}
        initialValues={
          editSection === "constraints"
            ? rawProfile?.constraints
            : editSection === "preferences"
              ? rawProfile?.preferences
              : editSection === "education"
                ? rawProfile?.education
                : undefined
        }
      />
    </div>
  )
}

function Section({
  title,
  children,
  editable,
  onEdit,
}: {
  title: string
  children: React.ReactNode
  editable?: boolean
  onEdit?: () => void
}) {
  return (
    <section className="mt-8">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          {title}
        </h2>
        {editable && onEdit ? (
          <button
            type="button"
            onClick={onEdit}
            className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
          >
            <Pencil className="size-3" aria-hidden="true" /> Edit
          </button>
        ) : null}
      </div>
      {children}
    </section>
  )
}

function Tag({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "rounded-md bg-secondary px-2 py-0.5 text-xs text-secondary-foreground",
        className,
      )}
    >
      {children}
    </span>
  )
}
