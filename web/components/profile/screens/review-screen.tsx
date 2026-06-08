"use client"

import { useMemo, useRef, useState } from "react"
import type { ExperienceChange, PreferenceSuggestion, ReviewState } from "@/lib/profile/profile-data"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { SkillsSection } from "@/components/profile/review/skills-section"
import { ExperiencesSection } from "@/components/profile/review/experiences-section"
import { ProjectsSection } from "@/components/profile/review/projects-section"
import { CertificationsSection } from "@/components/profile/review/certifications-section"
import { EducationSection } from "@/components/profile/review/education-section"
import { PreferencesSection } from "@/components/profile/review/preferences-section"
import { cn } from "@/lib/utils"
import { ArrowRight, Check, CircleDashed } from "lucide-react"

interface ReviewScreenProps {
  state: ReviewState
  setState: React.Dispatch<React.SetStateAction<ReviewState>>
  onSave: () => void | Promise<void>
  onSkip: () => void | Promise<void>
  saving?: boolean
}

type SectionId = "skills" | "experiences" | "projects" | "certifications" | "education" | "preferences"

const SECTION_LABELS: { id: SectionId; label: string }[] = [
  { id: "skills", label: "Skills" },
  { id: "experiences", label: "Experiences" },
  { id: "projects", label: "Projects" },
  { id: "certifications", label: "Certifications" },
  { id: "education", label: "Education" },
  { id: "preferences", label: "Preferences & Constraints" },
]

export function ReviewScreen({ state, setState, onSave, onSkip, saving }: ReviewScreenProps) {
  const [active, setActive] = useState<SectionId>("skills")
  const [skipOpen, setSkipOpen] = useState(false)
  const refs = {
    skills: useRef<HTMLDivElement>(null),
    experiences: useRef<HTMLDivElement>(null),
    projects: useRef<HTMLDivElement>(null),
    certifications: useRef<HTMLDivElement>(null),
    education: useRef<HTMLDivElement>(null),
    preferences: useRef<HTMLDivElement>(null),
  }

  const counts = useMemo(() => {
    const additions =
      state.skills.filter((s) => s.kind === "add").length +
      state.experiences.filter((e) => e.kind === "add").length +
      state.projects.filter((p) => p.kind === "add").length +
      state.certifications.filter((c) => c.kind === "add").length +
      state.education.filter((e) => e.kind === "add").length
    const updates =
      state.experiences.filter((e) => e.kind === "update").length +
      state.skills.filter((s) => s.kind === "update").length +
      state.education.filter((e) => e.kind === "update").length
    const removals =
      state.skills.filter((s) => s.kind === "remove").length +
      state.experiences.filter((e) => e.kind === "remove").length
    return { additions, updates, removals }
  }, [state])

  const approvedCount = useMemo(() => {
    return (
      state.skills.filter((s) => s.status === "approved").length +
      state.experiences.filter((e) => e.status === "approved").length +
      state.projects.filter((p) => p.status === "approved").length +
      state.certifications.filter((c) => c.status === "approved").length +
      state.education.filter((e) => e.status === "approved").length +
      state.preferences.filter((p) => p.status === "confirmed").length
    )
  }, [state])

  const sectionMeta = useMemo<Record<SectionId, { pending: number; reviewed: boolean }>>(() => {
    const skillsPending = state.skills.filter((s) => s.status === "pending").length
    const expPending = state.experiences.filter((e) => e.status === "pending").length
    const projPending = state.projects.filter((p) => p.status === "pending").length
    const certPending = state.certifications.filter((c) => c.status === "pending").length
    const eduPending = state.education.filter((e) => e.status === "pending").length
    const prefPending = state.preferences.filter((p) => p.status === "pending").length
    return {
      skills: { pending: state.skills.filter((s) => s.kind === "add").length, reviewed: skillsPending === 0 },
      experiences: { pending: state.experiences.length, reviewed: expPending === 0 },
      projects: { pending: state.projects.length, reviewed: projPending === 0 },
      certifications: { pending: state.certifications.length, reviewed: certPending === 0 },
      education: { pending: state.education.length, reviewed: eduPending === 0 },
      preferences: { pending: state.preferences.length, reviewed: prefPending === 0 },
    }
  }, [state])

  function scrollTo(id: SectionId) {
    setActive(id)
    refs[id].current?.scrollIntoView({ behavior: "smooth", block: "start" })
  }

  // decision helpers
  const setSkill = (id: string, status: ReviewState["skills"][number]["status"]) =>
    setState((s) => ({ ...s, skills: s.skills.map((x) => (x.id === id ? { ...x, status } : x)) }))
  const setExp = (id: string, status: ReviewState["experiences"][number]["status"]) =>
    setState((s) => ({
      ...s,
      experiences: s.experiences.map((x) => (x.id === id ? { ...x, status } : x)),
    }))
  const editExp = (updated: ExperienceChange) =>
    setState((s) => ({
      ...s,
      experiences: s.experiences.map((x) => (x.id === updated.id ? { ...updated } : x)),
    }))
  const setProj = (id: string, status: ReviewState["projects"][number]["status"]) =>
    setState((s) => ({
      ...s,
      projects: s.projects.map((x) => (x.id === id ? { ...x, status } : x)),
    }))
  const setCert = (id: string, status: ReviewState["certifications"][number]["status"]) =>
    setState((s) => ({
      ...s,
      certifications: s.certifications.map((x) => (x.id === id ? { ...x, status } : x)),
    }))
  const setEdu = (id: string, status: ReviewState["education"][number]["status"]) =>
    setState((s) => ({
      ...s,
      education: s.education.map((x) => (x.id === id ? { ...x, status } : x)),
    }))
  const setPref = (id: string, status: PreferenceSuggestion["status"], value?: string) =>
    setState((s) => ({
      ...s,
      preferences: s.preferences.map((x) =>
        x.id === id ? { ...x, status, value: value ?? x.value } : x,
      ),
    }))

  function approveAll() {
    setState((s) => ({
      skills: s.skills.map((x) => ({ ...x, status: "approved" })),
      experiences: s.experiences.map((x) => ({ ...x, status: "approved" })),
      projects: s.projects.map((x) => ({ ...x, status: "approved" })),
      certifications: s.certifications.map((x) => ({ ...x, status: "approved" })),
      education: s.education.map((x) => ({ ...x, status: "approved" })),
      preferences: s.preferences.map((x) => ({ ...x, status: "confirmed" })),
    }))
  }

  return (
    <div className="min-h-screen bg-background pb-24">
      <header className="sticky top-0 z-30 border-b border-border bg-background/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
          <Brand />
          <button
            type="button"
            onClick={() => setSkipOpen(true)}
            className="text-sm text-muted-foreground underline-offset-2 hover:text-foreground hover:underline"
          >
            Skip for now
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6">
        <div className="mb-6">
          <h1 className="text-balance text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">
            Review your profile
          </h1>
          <p className="mt-2 text-pretty leading-relaxed text-muted-foreground">
            We found the following information in your resume. Approve what looks right.
          </p>
        </div>

        {/* summary bar */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border bg-card p-3 sm:px-4">
          <p className="text-sm text-foreground">
            <span className="font-semibold text-add-foreground">{counts.additions} additions</span>
            <span className="text-muted-foreground"> · </span>
            <span className="font-semibold text-update-foreground">{counts.updates} updates</span>
            <span className="text-muted-foreground"> · </span>
            <span className="font-semibold text-muted-foreground">{counts.removals} removals</span>
          </p>
          <Button variant="secondary" size="sm" onClick={approveAll}>
            Approve all
          </Button>
        </div>

        <div className="flex flex-col gap-6 lg:flex-row">
          {/* sidebar / tab strip */}
          <nav
            aria-label="Profile sections"
            className="flex gap-2 overflow-x-auto pb-1 lg:sticky lg:top-20 lg:h-fit lg:w-60 lg:shrink-0 lg:flex-col lg:overflow-visible lg:pb-0"
          >
            {SECTION_LABELS.map(({ id, label }) => {
              const meta = sectionMeta[id]
              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => scrollTo(id)}
                  className={cn(
                    "flex shrink-0 items-center justify-between gap-2 rounded-lg border px-3 py-2 text-left text-sm transition-colors lg:w-full",
                    active === id
                      ? "border-primary/40 bg-accent text-accent-foreground"
                      : "border-transparent text-muted-foreground hover:bg-secondary hover:text-foreground",
                  )}
                >
                  <span className="flex items-center gap-2 whitespace-nowrap font-medium">
                    {meta.reviewed ? (
                      <Check className="size-3.5 text-add" aria-hidden="true" />
                    ) : (
                      <CircleDashed className="size-3.5 text-muted-foreground" aria-hidden="true" />
                    )}
                    {label}
                  </span>
                  {!meta.reviewed && meta.pending > 0 ? (
                    <span className="rounded-full bg-add-muted px-1.5 py-0.5 text-xs font-semibold text-add-foreground">
                      +{meta.pending}
                    </span>
                  ) : null}
                </button>
              )
            })}
          </nav>

          {/* sections */}
          <div className="min-w-0 flex-1 space-y-10">
            <div ref={refs.skills} className="scroll-mt-24">
              <SkillsSection
                skills={state.skills}
                onDecision={setSkill}
                onApproveAll={() =>
                  setState((s) => ({
                    ...s,
                    skills: s.skills.map((x) => ({ ...x, status: "approved" })),
                  }))
                }
                onRejectAll={() =>
                  setState((s) => ({
                    ...s,
                    skills: s.skills.map((x) => ({ ...x, status: "rejected" })),
                  }))
                }
              />
            </div>
            <div ref={refs.experiences} className="scroll-mt-24">
              <ExperiencesSection
                experiences={state.experiences}
                onDecision={setExp}
                onEdit={editExp}
                onApproveAll={() =>
                  setState((s) => ({
                    ...s,
                    experiences: s.experiences.map((x) => ({ ...x, status: "approved" })),
                  }))
                }
                onRejectAll={() =>
                  setState((s) => ({
                    ...s,
                    experiences: s.experiences.map((x) => ({ ...x, status: "rejected" })),
                  }))
                }
              />
            </div>
            <div ref={refs.projects} className="scroll-mt-24">
              <ProjectsSection
                projects={state.projects}
                onDecision={setProj}
                onApproveAll={() =>
                  setState((s) => ({
                    ...s,
                    projects: s.projects.map((x) => ({ ...x, status: "approved" })),
                  }))
                }
                onRejectAll={() =>
                  setState((s) => ({
                    ...s,
                    projects: s.projects.map((x) => ({ ...x, status: "rejected" })),
                  }))
                }
              />
            </div>
            <div ref={refs.certifications} className="scroll-mt-24">
              <CertificationsSection
                certifications={state.certifications}
                onDecision={setCert}
                onApproveAll={() =>
                  setState((s) => ({
                    ...s,
                    certifications: s.certifications.map((x) => ({ ...x, status: "approved" })),
                  }))
                }
                onRejectAll={() =>
                  setState((s) => ({
                    ...s,
                    certifications: s.certifications.map((x) => ({ ...x, status: "rejected" })),
                  }))
                }
              />
            </div>
            {state.education.length > 0 ? (
              <div ref={refs.education} className="scroll-mt-24">
                <EducationSection
                  education={state.education}
                  onDecision={setEdu}
                  onApproveAll={() =>
                    setState((s) => ({
                      ...s,
                      education: s.education.map((x) => ({ ...x, status: "approved" })),
                    }))
                  }
                  onRejectAll={() =>
                    setState((s) => ({
                      ...s,
                      education: s.education.map((x) => ({ ...x, status: "rejected" })),
                    }))
                  }
                />
              </div>
            ) : null}
            <div ref={refs.preferences} className="scroll-mt-24">
              <PreferencesSection preferences={state.preferences} onDecision={setPref} />
            </div>
          </div>
        </div>
      </div>

      {/* sticky footer */}
      <div className="fixed inset-x-0 bottom-0 z-30 border-t border-border bg-background/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
          <Button variant="ghost" onClick={() => setSkipOpen(true)}>
            Skip for now
          </Button>
          <Button disabled={approvedCount === 0 || saving} onClick={() => void onSave()}>
            {saving
              ? "Saving..."
              : approvedCount > 0
                ? `Save ${approvedCount} approved changes`
                : "Save approved changes"}
            <ArrowRight className="size-4" aria-hidden="true" />
          </Button>
        </div>
      </div>

      <Dialog open={skipOpen} onOpenChange={setSkipOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Skip for now?</DialogTitle>
            <DialogDescription>
              No changes will be saved to your profile. You can re-upload your resume anytime.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="ghost" onClick={() => setSkipOpen(false)}>
              Keep reviewing
            </Button>
            <Button variant="secondary" onClick={() => void onSkip()}>
              Continue without saving
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
