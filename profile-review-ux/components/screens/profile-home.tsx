"use client"

import type { ProfileResponse } from "@/lib/api-types"
import { educationLevelLabel, type EducationEntry, type ResumeSectionOrder } from "@/lib/contact"
import type { CommittedProfile } from "@/lib/build-profile"
import type { ProfileHomeData } from "@/lib/map-profile"
import type { EditSection } from "@/components/profile-edit-dialog"
import { EeoDisplay } from "@/components/profile/eeo-form"
import { ProfileEditDialog } from "@/components/profile-edit-dialog"
import { ResumeLibrary } from "@/components/profile/resume-library"
import { Brand } from "@/components/brand"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { formatRelativeTime } from "@/lib/map-profile"
import { Award, Building2, GraduationCap, Pencil, Upload } from "lucide-react"

interface ProfileHomeProps {
  data: ProfileHomeData
  onUploadNew: () => void
  onEditSection: (section: EditSection | null) => void
  onSetTargetRoles: () => void
  onResumeLabelSave?: (resumeId: string, label: string | null) => Promise<void>
  editSection: EditSection | null
  onEditSave: (section: EditSection, values: Record<string, unknown>) => Promise<void>
  rawProfile?: ProfileResponse | null
  readOnly?: boolean
}

export function ProfileHome({
  data,
  onUploadNew,
  onEditSection,
  onSetTargetRoles,
  onResumeLabelSave,
  editSection,
  onEditSave,
  rawProfile,
  readOnly = false,
}: ProfileHomeProps) {
  const { profile } = data

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
            <ContactSummary
              email={data.email}
              contact={data.contact}
              onEdit={() => onEditSection("contact")}
            />
            <p className="mt-2 text-sm text-muted-foreground">
              Job recommendations follow the roles you choose — not what your resume implies.
            </p>
          </div>
          <div className="flex gap-2">
            <Button size="sm" onClick={onUploadNew}>
              <Upload className="size-4" aria-hidden="true" />
              {data.resumeCount > 0 ? "Add resume" : "Upload resume"}
            </Button>
            <Button size="sm" variant="secondary" onClick={() => onEditSection("preferences")}>
              <Pencil className="size-4" aria-hidden="true" />
              Edit preferences
            </Button>
          </div>
        </div>

        {data.hasTargetRoles ? (
          <Section title="Target roles" editable onEdit={onSetTargetRoles}>
            <div className="space-y-3">
              <div>
                <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  Primary
                </p>
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {data.primaryRoles.map((role) => (
                    <Tag key={role} className="font-medium">
                      {role}
                    </Tag>
                  ))}
                </div>
              </div>
              {data.secondaryRoles.length > 0 ? (
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                    Secondary
                  </p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {data.secondaryRoles.map((role) => (
                      <Tag key={role}>{role}</Tag>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          </Section>
        ) : (
          <div className="mt-8 rounded-xl border border-primary/30 bg-accent/40 p-4">
            <p className="text-sm font-medium text-foreground">Set your target roles</p>
            <p className="mt-1 text-sm text-muted-foreground">
              Tell us what roles you want to apply for. This drives your job recommendations.
            </p>
            <Button size="sm" className="mt-3" onClick={onSetTargetRoles}>
              Define target roles
            </Button>
          </div>
        )}

        <Section title="Your resumes">
          <ResumeLibrary
            resumes={data.resumes}
            onUploadNew={onUploadNew}
            onSaveLabel={onResumeLabelSave}
            readOnly={readOnly}
          />
        </Section>

        <OrderedEducationExperience
          order={data.resumeSectionOrder}
          educationEntries={data.educationEntries}
          experiences={profile.experiences}
          onEditEducation={() => onEditSection("education")}
        />

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

        {profile.skills.length > 0 ? (
          <Section title="Skills">
            <p className="mb-4 text-sm text-muted-foreground">
              Skills from your approved resumes — a factual inventory, not a career recommendation.
            </p>
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

        <Section
          title="Equal employment authorization"
          editable
          onEdit={() => onEditSection("eeo")}
        >
          {data.eeoRows.length > 0 ? (
            <>
              <EeoDisplay state={data.eeo} />
              <p className="mt-4 text-xs leading-relaxed text-muted-foreground">
                Used to auto-fill standard US job application questions. You can update these anytime.
              </p>
            </>
          ) : (
            <div className="rounded-lg border border-dashed border-border p-4">
              <p className="text-sm text-muted-foreground">
                Complete your equal employment authorization answers to speed up future applications.
              </p>
              <Button
                size="sm"
                variant="secondary"
                className="mt-3"
                onClick={() => onEditSection("eeo")}
              >
                Add EEO responses
              </Button>
            </div>
          )}
        </Section>

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
                : editSection === "eeo"
                  ? (rawProfile?.constraints?.eeo as Record<string, unknown> | undefined)
                  : editSection === "contact"
                    ? rawProfile?.education
                    : undefined
        }
        contactValues={data.contact}
        eeoValues={data.eeo}
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

function toExternalUrl(value: string): string {
  if (value.startsWith("http://") || value.startsWith("https://")) return value
  return `https://${value}`
}

function OrderedEducationExperience({
  order,
  educationEntries,
  experiences,
  onEditEducation,
}: {
  order: ResumeSectionOrder
  educationEntries: EducationEntry[]
  experiences: CommittedProfile["experiences"]
  onEditEducation: () => void
}) {
  const educationBlock = (
    <EducationBlock entries={educationEntries} onEdit={onEditEducation} />
  )
  const experienceBlock = <ExperienceBlock experiences={experiences} />

  return (
    <>
      {order === "education_first" ? (
        <>
          {educationBlock}
          {experienceBlock}
        </>
      ) : (
        <>
          {experienceBlock}
          {educationBlock}
        </>
      )}
    </>
  )
}

function EducationBlock({
  entries,
  onEdit,
}: {
  entries: EducationEntry[]
  onEdit: () => void
}) {
  return (
    <Section title="Education" editable onEdit={onEdit}>
      {entries.length > 0 ? (
        <div className="space-y-3">
          {entries.map((entry) => (
            <Card key={`${entry.level}-${entry.degree}-${entry.university}`} className="p-4">
              <div className="flex items-start gap-3">
                <span className="flex size-9 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
                  <GraduationCap className="size-4.5" aria-hidden="true" />
                </span>
                <div>
                  <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                    {educationLevelLabel(entry.level)}
                  </p>
                  <h3 className="mt-1 text-base font-semibold text-foreground">{entry.degree}</h3>
                  <p className="mt-0.5 text-sm text-muted-foreground">
                    {entry.university}
                    {entry.graduationDate ? ` · ${entry.graduationDate}` : ""}
                    {entry.gpa ? ` · GPA ${entry.gpa}` : ""}
                  </p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyEvidence message="No education on your profile yet. Approve education entries when reviewing your resume." />
      )}
    </Section>
  )
}

function ExperienceBlock({
  experiences,
}: {
  experiences: CommittedProfile["experiences"]
}) {
  return (
    <Section title="Experience">
      {experiences.length > 0 ? (
        <div className="space-y-3">
          {experiences.map((e) => (
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
      ) : (
        <EmptyEvidence message="No work experience on your profile yet. Approve experience entries when reviewing your resume." />
      )}
    </Section>
  )
}

function EmptyEvidence({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-dashed border-border p-4">
      <p className="text-sm text-muted-foreground">{message}</p>
    </div>
  )
}

function ContactSummary({
  email,
  contact,
  onEdit,
}: {
  email: string
  contact: ProfileHomeData["contact"]
  onEdit: () => void
}) {
  type Part = { key: string; node: React.ReactNode }
  const parts: Part[] = []

  if (contact.location) parts.push({ key: "location", node: contact.location })
  if (email) parts.push({ key: "email", node: email })
  if (contact.phone) parts.push({ key: "phone", node: contact.phone })
  if (contact.linkedin) {
    parts.push({
      key: "linkedin",
      node: (
        <a
          href={toExternalUrl(contact.linkedin)}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:underline"
        >
          {contact.linkedin}
        </a>
      ),
    })
  }
  if (contact.github) {
    parts.push({
      key: "github",
      node: (
        <a
          href={toExternalUrl(contact.github)}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary hover:underline"
        >
          {contact.github}
        </a>
      ),
    })
  }

  if (parts.length === 0) return null

  return (
    <div className="mt-1 overflow-x-auto">
      <p className="whitespace-nowrap text-sm text-muted-foreground">
        {parts.map((part, index) => (
          <span key={part.key}>
            {index > 0 ? <span className="mx-1.5 text-border">·</span> : null}
            {part.node}
          </span>
        ))}
        <span className="mx-1.5 text-border">·</span>
        <button
          type="button"
          onClick={onEdit}
          className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
        >
          <Pencil className="size-3" aria-hidden="true" />
          Edit
        </button>
      </p>
    </div>
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
