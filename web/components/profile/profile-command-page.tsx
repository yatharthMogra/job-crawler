"use client"

import { useState } from "react"
import Link from "next/link"
import {
  Link as LinkIcon,
  Mail,
  MapPin,
  Pencil,
} from "lucide-react"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import type { EditSection } from "@/components/profile/profile-edit-dialog"
import { educationLevelLabel } from "@/lib/profile/contact"
import { ProfileExperienceTimeline } from "@/components/profile/profile-experience-timeline"
import { ProfileInsightsPanel } from "@/components/profile/profile-insights-panel"
import { EeoDisplay } from "@/components/profile/eeo-form"
import { BrandLogo } from "@/components/brand-logo"
import { cn } from "@/lib/utils"

const TABS = [
  { id: "experience", label: "Experience" },
  { id: "education", label: "Education" },
  { id: "certifications", label: "Certifications" },
  { id: "preferences", label: "Equal employment" },
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
}

export function ProfileCommandPage({
  data,
  onEditSection,
}: ProfileCommandPageProps) {
  const [tab, setTab] = useState<TabId>("experience")
  const { profile, contact } = data
  const headlineRole = profile.experiences[0]?.title ?? "Professional"

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
              <section>
                <div className="mb-6 flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-bold text-foreground">Work experience</h2>
                    <p className="mt-1 text-sm text-muted-foreground">
                      Roles, impact, and technologies extracted from your resumes.
                    </p>
                  </div>
                  <Link
                    href="/resume"
                    className="text-sm font-semibold text-primary hover:underline"
                  >
                    Update via resume
                  </Link>
                </div>
                <ProfileExperienceTimeline experiences={profile.experiences} />
              </section>
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
              <section>
                <div className="mb-6 flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-bold text-foreground">
                      Equal employment opportunity
                    </h2>
                    <p className="mt-1 max-w-xl text-sm text-muted-foreground">
                      Voluntary self-identification used for compliance and to match roles that fit
                      your work authorization and sponsorship needs.
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => onEditSection("eeo")}
                    className="shrink-0 text-sm font-semibold text-primary hover:underline"
                  >
                    Edit
                  </button>
                </div>
                {data.eeoRows.length > 0 ? (
                  <div className="rounded-2xl border border-border/60 bg-card p-6 shadow-sm">
                    <EeoDisplay state={data.eeo} />
                  </div>
                ) : (
                  <div className="rounded-2xl border border-dashed border-border/70 bg-card px-6 py-10 text-center">
                    <p className="text-sm font-medium text-foreground">No EEO responses yet</p>
                    <p className="mx-auto mt-2 max-w-sm text-sm text-muted-foreground">
                      Add your equal employment opportunity information to improve application
                      matching.
                    </p>
                    <button
                      type="button"
                      onClick={() => onEditSection("eeo")}
                      className="mt-4 text-sm font-semibold text-primary hover:underline"
                    >
                      Add EEO information
                    </button>
                  </div>
                )}
              </section>
            ) : null}
          </div>
        </div>

        <ProfileInsightsPanel data={data} className="xl:sticky xl:top-8" />
      </div>
    </div>
  )
}
