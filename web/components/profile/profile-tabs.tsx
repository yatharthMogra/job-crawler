"use client"

import { useEffect, useRef, useState } from "react"
import { Pencil, Shield } from "lucide-react"
import Link from "next/link"
import type { ProfileHomeData } from "@/lib/profile/map-profile"
import type { EditSection } from "@/components/profile/profile-edit-dialog"
import { educationLevelLabel } from "@/lib/profile/contact"
import { EeoDisplay } from "@/components/profile/eeo-form"
import { TimelineEntry } from "@/components/profile/timeline-entry"
import { ContactPills } from "@/components/profile/contact-pills"
import { SkillsEditor } from "@/components/profile/skills-editor"
import { FilterChip } from "@/components/ui/filter-chip"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const SECTIONS = [
  { id: "personal", label: "Personal" },
  { id: "education", label: "Education" },
  { id: "experience", label: "Experience" },
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
      { rootMargin: "-120px 0px -60% 0px", threshold: [0, 0.25, 0.5] },
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

  return (
    <div className="bg-zinc-50">
      <div className="border-b border-zinc-200 bg-white px-6 py-4">
        <h1 className="text-lg font-bold tracking-tight text-zinc-900">Profile</h1>
        <div className="mt-3 flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-600">
          <Shield className="size-4 shrink-0 text-zinc-500" />
          Your profile data is kept private and secure.
        </div>
      </div>

      <div className="sticky top-0 z-10 border-b border-zinc-200 bg-white/95 backdrop-blur-sm">
        <nav className="flex gap-1 overflow-x-auto px-6">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => scrollTo(s.id)}
              className={cn(
                "shrink-0 border-b-2 px-3 py-3 text-sm font-medium transition-colors",
                active === s.id
                  ? "border-zinc-900 text-zinc-900"
                  : "border-transparent text-zinc-500 hover:text-zinc-800",
              )}
            >
              {s.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="mx-auto max-w-3xl space-y-16 px-6 py-8">
        <section id="profile-personal" className="scroll-mt-28">
          <div className="flex items-start justify-between">
            <h2 className="text-2xl font-semibold text-zinc-900">{data.candidateName}</h2>
            <Button size="sm" variant="ghost" onClick={() => onEditSection("contact")}>
              <Pencil className="size-4" />
            </Button>
          </div>
          <ContactPills email={data.email} contact={data.contact} />
          <div className="mt-8">
            <p className="text-sm font-medium text-zinc-700">Target roles</p>
            {data.hasTargetRoles ? (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {data.primaryRoles.map((r) => (
                  <FilterChip key={r} label={r} active />
                ))}
              </div>
            ) : (
              <p className="mt-1 text-sm text-zinc-500">No roles selected yet.</p>
            )}
            <div className="mt-3 flex gap-2">
              <Button size="sm" variant="outline" className="border-zinc-300" onClick={onSetTargetRoles}>
                Edit roles
              </Button>
              <Link href="/filters">
                <Button size="sm" variant="outline" className="border-zinc-300">
                  All filters
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <section id="profile-education" className="scroll-mt-28">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-zinc-900">Education</h2>
            <Button size="sm" variant="ghost" onClick={() => onEditSection("education")}>
              <Pencil className="size-4" />
            </Button>
          </div>
          {data.educationEntries.length === 0 ? (
            <p className="text-sm text-zinc-500">No education on your profile yet.</p>
          ) : (
            data.educationEntries.map((entry, i) => (
              <TimelineEntry
                key={`${entry.university}-${i}`}
                dateRange={entry.graduationDate || "—"}
                title={entry.university}
                subtitle={`${educationLevelLabel(entry.level)} · ${entry.degree}`}
                detail={entry.gpa ? `GPA ${entry.gpa}` : undefined}
                isLast={i === data.educationEntries.length - 1}
              />
            ))
          )}
        </section>

        <section id="profile-experience" className="scroll-mt-28">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-zinc-900">Work Experience</h2>
          </div>
          {profile.experiences.length === 0 ? (
            <p className="text-sm text-zinc-500">No experience on your profile yet.</p>
          ) : (
            profile.experiences.map((exp, i) => (
              <TimelineEntry
                key={exp.id}
                dateRange={`${exp.durationMonths} months`}
                title={exp.company}
                subtitle={exp.title}
                bullets={exp.keywords.slice(0, 5)}
                isLast={i === profile.experiences.length - 1}
              />
            ))
          )}
        </section>

        <section id="profile-skills" className="scroll-mt-28">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-zinc-900">Skills</h2>
          </div>
          <SkillsEditor skills={profile.skills} />
        </section>

        <section id="profile-eeo" className="scroll-mt-28 pb-12">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-zinc-900">Equal Employment</h2>
            <Button size="sm" variant="ghost" onClick={() => onEditSection("eeo")}>
              <Pencil className="size-4" />
            </Button>
          </div>
          <EeoDisplay state={data.eeo} />
        </section>
      </div>
    </div>
  )
}
