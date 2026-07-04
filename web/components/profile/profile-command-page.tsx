"use client"

import { useState } from "react"
import Link from "next/link"
import {
  Link as LinkIcon,
  Mail,
  MapPin,
  Pencil,
  Plus,
} from "lucide-react"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import type { EditSection } from "@/components/profile/profile-edit-dialog"
import { educationLevelLabel } from "@/lib/profile/contact"
import { ProfileExperienceTimeline } from "@/components/profile/profile-experience-timeline"
import { ProfileInsightsPanel } from "@/components/profile/profile-insights-panel"
import { BrandLogo } from "@/components/brand-logo"
import { cn } from "@/lib/utils"

const TABS = [
  { id: "experience", label: "Experience" },
  { id: "education", label: "Education" },
  { id: "certifications", label: "Certifications" },
  { id: "preferences", label: "Preferences" },
] as const

type TabId = (typeof TABS)[number]["id"]

function initials(name: string): string {
  return name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase()
}

interface ProfileCommandPageProps {
  data: ProfileHomeData
  onEditSection: (section: EditSection | null) => void
  onSetTargetRoles: () => void
}

export function ProfileCommandPage({
  data,
  onEditSection,
  onSetTargetRoles,
}: ProfileCommandPageProps) {
  const [tab, setTab] = useState<TabId>("experience")
  const { profile, contact } = data
  const headlineRole = data.primaryRoles[0] ?? profile.experiences[0]?.title ?? "Professional"
  const allSkills = profile.skills.flatMap((g) => g.names)

  const linkedinHref = contact.linkedin
    ? contact.linkedin.startsWith("http")
      ? contact.linkedin
      : `https://${contact.linkedin}`
    : null
  const githubHref = contact.github
    ? contact.github.startsWith("http")
      ? contact.github
      : `https://${contact.github}`
    : null

  return (
    <div className="min-h-full bg-muted/20">
      <div className="mx-auto flex max-w-[1280px] flex-col gap-8 px-6 py-8 xl:flex-row xl:items-start">
        <div className="min-w-0 flex-1">
          {/* Profile hero */}
          <section className="rounded-2xl border border-border/60 bg-card p-6 shadow-sm sm:p-8">
            <div className="flex flex-col gap-6 sm:flex-row sm:items-start">
              <div className="relative shrink-0">
                <div className="flex size-24 items-center justify-center rounded-2xl bg-primary text-3xl font-bold text-primary-foreground shadow-lg shadow-primary/20">
                  {initials(data.candidateName)}
                </div>
                <span className="absolute -bottom-0.5 -right-0.5 size-4 rounded-full border-2 border-card bg-emerald-500" />
              </div>

              <div className="min-w-0 flex-1">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h1 className="text-3xl font-bold tracking-tight text-foreground">
                      {data.candidateName}
                    </h1>
                    <p className="mt-1.5 flex flex-wrap items-center gap-x-2 text-[15px] text-muted-foreground">
                      {contact.location ? (
                        <>
                          <MapPin className="size-4 shrink-0" />
                          {contact.location}
                          <span>·</span>
                        </>
                      ) : null}
                      <span className="font-medium text-foreground/80">{headlineRole}</span>
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => onEditSection("contact")}
                    className="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
                    aria-label="Edit profile"
                  >
                    <Pencil className="size-4" />
                  </button>
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                  {linkedinHref ? (
                    <a
                      href={linkedinHref}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-2 rounded-lg border border-border/70 bg-muted/30 px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-muted/60"
                    >
                      <LinkIcon className="size-4 text-primary" />
                      LinkedIn
                    </a>
                  ) : null}
                  {githubHref ? (
                    <a
                      href={githubHref}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-2 rounded-lg border border-border/70 bg-muted/30 px-3 py-2 text-sm font-medium text-foreground/80 transition-colors hover:bg-muted/60"
                    >
                      <LinkIcon className="size-4 text-primary" />
                      GitHub
                    </a>
                  ) : null}
                  <span className="inline-flex items-center gap-2 rounded-lg border border-border/70 bg-muted/30 px-3 py-2 text-sm font-medium text-foreground/80">
                    <Mail className="size-4 text-primary" />
                    {data.email}
                  </span>
                </div>

                <div className="mt-6 border-t border-border/60 pt-5">
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                    Target roles
                  </p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {data.primaryRoles.map((role) => (
                      <span
                        key={role}
                        className="rounded-full bg-slate-900 px-3.5 py-1.5 text-sm font-semibold text-white"
                      >
                        {role}
                      </span>
                    ))}
                    {data.secondaryRoles.slice(0, 2).map((role) => (
                      <span
                        key={role}
                        className="rounded-full border border-border bg-muted/40 px-3.5 py-1.5 text-sm font-medium text-foreground/80"
                      >
                        {role}
                      </span>
                    ))}
                    <button
                      type="button"
                      onClick={onSetTargetRoles}
                      className="inline-flex items-center gap-1.5 rounded-full border border-dashed border-primary/40 px-3.5 py-1.5 text-sm font-semibold text-primary transition-colors hover:bg-primary/5"
                    >
                      <Plus className="size-3.5" />
                      Add role
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Tabs */}
          <div className="mt-8 border-b border-border/70">
            <nav className="-mb-px flex gap-6 overflow-x-auto">
              {TABS.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setTab(item.id)}
                  className={cn(
                    "relative shrink-0 pb-3 text-sm font-semibold transition-colors",
                    tab === item.id
                      ? "text-primary"
                      : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  {item.label}
                  {tab === item.id ? (
                    <span className="absolute inset-x-0 -bottom-px h-0.5 rounded-full bg-primary" />
                  ) : null}
                </button>
              ))}
            </nav>
          </div>

          {/* Tab panels */}
          <div className="mt-8">
            {tab === "experience" ? (
              <div className="space-y-10">
                <section>
                  <div className="mb-6 flex items-center justify-between">
                    <h2 className="text-xl font-bold text-foreground">Work experience</h2>
                    <Link
                      href="/resume"
                      className="text-sm font-semibold text-primary hover:underline"
                    >
                      + Add position
                    </Link>
                  </div>
                  <ProfileExperienceTimeline experiences={profile.experiences} />
                </section>

                <section>
                  <h2 className="mb-4 text-xl font-bold text-foreground">Skills &amp; expertise</h2>
                  {allSkills.length === 0 ? (
                    <p className="text-sm text-muted-foreground">No skills on your profile yet.</p>
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {allSkills.map((name, index) => (
                        <span
                          key={name}
                          className={cn(
                            "rounded-full px-3.5 py-1.5 text-sm font-medium",
                            index < 6
                              ? "border border-emerald-500/25 bg-emerald-500/10 text-emerald-900"
                              : "border border-border/70 bg-muted/40 text-foreground/80",
                          )}
                        >
                          {name}
                        </span>
                      ))}
                    </div>
                  )}
                </section>
              </div>
            ) : null}

            {tab === "education" ? (
              <section>
                <div className="mb-6 flex items-center justify-between">
                  <h2 className="text-xl font-bold text-foreground">Education</h2>
                  <button
                    type="button"
                    onClick={() => onEditSection("education")}
                    className="text-sm font-semibold text-primary hover:underline"
                  >
                    Edit
                  </button>
                </div>
                {data.educationEntries.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No education on your profile yet.</p>
                ) : (
                  <div className="grid gap-4 sm:grid-cols-2">
                    {data.educationEntries.map((entry, i) => (
                      <div
                        key={`${entry.university}-${i}`}
                        className="rounded-2xl border border-border/60 bg-card p-5 shadow-sm"
                      >
                        <BrandLogo name={entry.university} variant="school" size={44} shape="circle" />
                        <p className="mt-4 text-lg font-bold text-foreground">{entry.university}</p>
                        <p className="text-sm font-semibold text-primary">{entry.degree}</p>
                        <p className="mt-1 text-sm text-muted-foreground">
                          {educationLevelLabel(entry.level)} · {entry.graduationDate || "—"}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            ) : null}

            {tab === "certifications" ? (
              <section>
                <h2 className="mb-6 text-xl font-bold text-foreground">Certifications</h2>
                {profile.certifications.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No certifications on your profile yet.</p>
                ) : (
                  <div className="space-y-3">
                    {profile.certifications.map((cert) => (
                      <div
                        key={cert.id}
                        className="rounded-xl border border-border/60 bg-card px-4 py-3.5 shadow-sm"
                      >
                        <p className="font-semibold text-foreground">{cert.name}</p>
                        <p className="text-sm text-muted-foreground">{cert.issuer}</p>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            ) : null}

            {tab === "preferences" ? (
              <section className="space-y-6">
                <div>
                  <div className="mb-4 flex items-center justify-between">
                    <h2 className="text-xl font-bold text-foreground">Job preferences</h2>
                    <button
                      type="button"
                      onClick={() => onEditSection("preferences")}
                      className="text-sm font-semibold text-primary hover:underline"
                    >
                      Edit
                    </button>
                  </div>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {data.preferences.map((row) => (
                      <div
                        key={row.label}
                        className="rounded-xl border border-border/60 bg-card px-4 py-3.5 shadow-sm"
                      >
                        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                          {row.label}
                        </p>
                        <p className="mt-1 text-sm font-semibold text-foreground">{row.value}</p>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="mb-4 text-lg font-bold text-foreground">Constraints</h3>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {data.constraints.map((row) => (
                      <div
                        key={row.label}
                        className="rounded-xl border border-border/60 bg-card px-4 py-3.5 shadow-sm"
                      >
                        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                          {row.label}
                        </p>
                        <p className="mt-1 text-sm font-semibold text-foreground">{row.value}</p>
                      </div>
                    ))}
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">
                  <Link href="/filters" className="font-semibold text-primary hover:underline">
                    Open all filters
                  </Link>{" "}
                  to refine recommendations.
                </p>
              </section>
            ) : null}
          </div>
        </div>

        <ProfileInsightsPanel data={data} className="xl:sticky xl:top-8" />
      </div>
    </div>
  )
}
