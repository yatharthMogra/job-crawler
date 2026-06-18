"use client"

import { useEffect, useRef, useState } from "react"
import { Link as LinkIcon, MapPin, Mail, Pencil, Phone, Shield } from "lucide-react"
import Link from "next/link"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import type { EditSection } from "@/components/profile/profile-edit-dialog"
import { educationLevelLabel } from "@/lib/profile/contact"
import { EeoDisplay } from "@/components/profile/eeo-form"
import { ProfileSidebar } from "@/components/profile/profile-sidebar"
import { SkillsEditor } from "@/components/profile/skills-editor"
import { AppHeader } from "@/components/layout/app-header"
import { BrandLogo } from "@/components/brand-logo"
import { FilterChip } from "@/components/ui/filter-chip"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const SECTIONS = [
  { id: "personal", label: "Personal" },
  { id: "education", label: "Education" },
  { id: "experience", label: "Work Experience" },
  { id: "skills", label: "Skills" },
  { id: "eeo", label: "Equal Employment" },
] as const

interface ProfileTabsProps {
  data: ProfileHomeData
  onEditSection: (section: EditSection | null) => void
  onSetTargetRoles: () => void
}

export function ProfileTabs({ data, onEditSection, onSetTargetRoles }: ProfileTabsProps) {
  const [active, setActive] = useState<string>("personal")
  const { profile } = data
  const observerRef = useRef<IntersectionObserver | null>(null)
  const { contact } = data

  useEffect(() => {
    observerRef.current?.disconnect()
    observerRef.current = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)
        if (visible[0]?.target.id) {
          setActive(visible[0].target.id.replace("profile-", ""))
        }
      },
      { rootMargin: "-140px 0px -60% 0px", threshold: [0, 0.25, 0.5] },
    )

    for (const s of SECTIONS) {
      const el = document.getElementById(`profile-${s.id}`)
      if (el) observerRef.current.observe(el)
    }

    return () => observerRef.current?.disconnect()
  }, [])

  function scrollTo(id: string) {
    document.getElementById(`profile-${id}`)?.scrollIntoView({ behavior: "smooth", block: "start" })
    setActive(id)
  }

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
    <div className="dashboard-page-bg min-h-screen">
      <AppHeader title="Profile" showSearch />

      <div className="border-b border-border/80 bg-accent/30 px-6 py-3">
        <div className="flex items-center gap-2 text-sm text-accent-foreground">
          <Shield className="size-4 shrink-0 text-primary" />
          Your profile data is kept private and secure.{" "}
          <Link href="/settings" className="font-medium text-primary underline-offset-2 hover:underline">
            Learn more
          </Link>
        </div>
      </div>

      <div className="sticky top-16 z-10 border-b border-border/80 bg-card/95 backdrop-blur-md">
        <nav className="flex gap-1 overflow-x-auto px-6">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => scrollTo(s.id)}
              className={cn(
                "relative shrink-0 px-4 py-3 text-sm font-medium transition-colors",
                active === s.id ? "text-primary" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {active === s.id ? (
                <span className="absolute inset-x-1 bottom-0 h-0.5 rounded-full bg-primary" />
              ) : null}
              {s.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="flex gap-8 px-6 py-8">
        <div className="min-w-0 flex-1 space-y-12">
          <section id="profile-personal" className="scroll-mt-36">
            <div className="card-elevated p-6">
              <div className="flex items-start justify-between">
                <h2 className="text-2xl font-bold text-foreground">{data.candidateName}</h2>
                <Button size="sm" variant="ghost" onClick={() => onEditSection("contact")}>
                  <Pencil className="size-4" />
                </Button>
              </div>

              <div className="mt-4 space-y-2 text-sm text-muted-foreground">
                {contact.location ? (
                  <p className="flex items-center gap-2">
                    <MapPin className="size-4 shrink-0 text-primary" />
                    {contact.location}
                  </p>
                ) : null}
                <p className="flex items-center gap-2">
                  <Mail className="size-4 shrink-0 text-primary" />
                  {data.email}
                </p>
                {contact.phone ? (
                  <p className="flex items-center gap-2">
                    <Phone className="size-4 shrink-0 text-primary" />
                    {contact.phone}
                  </p>
                ) : null}
              </div>

              <div className="mt-4 flex gap-2">
                {linkedinHref ? (
                  <a
                    href={linkedinHref}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted"
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
                    className="inline-flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted"
                  >
                    <LinkIcon className="size-4" />
                    GitHub
                  </a>
                ) : null}
              </div>

              <div className="mt-6 border-t border-border pt-6">
                <p className="text-sm font-medium text-foreground">Target roles</p>
                {data.hasTargetRoles ? (
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {data.primaryRoles.map((r) => (
                      <FilterChip key={r} label={r} active />
                    ))}
                  </div>
                ) : (
                  <p className="mt-1 text-sm text-muted-foreground">No roles selected yet.</p>
                )}
                <div className="mt-3 flex gap-2">
                  <Button size="sm" variant="outline" onClick={onSetTargetRoles}>
                    Edit roles
                  </Button>
                  <Link href="/filters">
                    <Button size="sm" className="btn-brand">
                      All filters
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </section>

          <section id="profile-education" className="scroll-mt-36">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-foreground">Education</h2>
              <Button size="sm" variant="ghost" onClick={() => onEditSection("education")}>
                <Pencil className="size-4" />
              </Button>
            </div>
            {data.educationEntries.length === 0 ? (
              <p className="text-sm text-muted-foreground">No education on your profile yet.</p>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2">
                {data.educationEntries.map((entry, i) => (
                  <div key={`${entry.university}-${i}`} className="card-elevated p-5">
                    <BrandLogo name={entry.university} variant="school" size={40} shape="circle" />
                    <p className="mt-3 font-semibold text-foreground">{entry.university}</p>
                    <p className="text-sm text-primary">{entry.degree}</p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {educationLevelLabel(entry.level)} · {entry.graduationDate || "—"}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </section>

          <section id="profile-experience" className="scroll-mt-36">
            <h2 className="mb-6 text-lg font-semibold text-foreground">Work Experience</h2>
            {profile.experiences.length === 0 ? (
              <p className="text-sm text-muted-foreground">No experience on your profile yet.</p>
            ) : (
              <div className="relative space-y-0 border-l-2 border-primary/20 pl-6">
                {profile.experiences.map((exp, i) => {
                  const isPresent = i === 0
                  return (
                    <div key={exp.id} className="relative pb-8 last:pb-0">
                      <span className="absolute -left-[31px] top-1 size-4 rounded-full border-2 border-primary bg-card" />
                      <div className="flex flex-wrap items-center gap-2">
                        <p className="font-semibold text-foreground">{exp.company}</p>
                        {isPresent ? (
                          <span className="rounded-full bg-add-muted px-2 py-0.5 text-[10px] font-semibold text-add-foreground">
                            Present
                          </span>
                        ) : null}
                      </div>
                      <p className="text-sm font-medium text-primary">{exp.title}</p>
                      <p className="mt-1 text-xs text-muted-foreground">{exp.durationMonths} months</p>
                      {exp.keywords.length > 0 ? (
                        <ul className="mt-3 list-disc space-y-1 pl-4 text-sm text-muted-foreground">
                          {exp.keywords.slice(0, 5).map((kw) => (
                            <li key={kw}>{kw}</li>
                          ))}
                        </ul>
                      ) : null}
                    </div>
                  )
                })}
              </div>
            )}
          </section>

          <section id="profile-skills" className="scroll-mt-36">
            <h2 className="mb-4 text-lg font-semibold text-foreground">Skills & Expertise</h2>
            <SkillsEditor skills={profile.skills} />
          </section>

          <section id="profile-eeo" className="scroll-mt-36 pb-12">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-foreground">Equal Employment</h2>
              <Button size="sm" variant="ghost" onClick={() => onEditSection("eeo")}>
                <Pencil className="size-4" />
              </Button>
            </div>
            <EeoDisplay state={data.eeo} />
          </section>
        </div>

        <div className="hidden shrink-0 lg:block">
          <div className="sticky top-36">
            <ProfileSidebar data={data} />
          </div>
        </div>
      </div>
    </div>
  )
}
