"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import type { ExperienceChange, ReviewState } from "@/lib/profile/profile-data"
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
import { cn } from "@/lib/utils"
import {
  Brain,
  Check,
  ChevronRight,
  Code2,
  GraduationCap,
  LayoutGrid,
  LineChart,
  Link2,
  Lock,
  MapPin,
  Phone,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  X,
  Zap,
} from "lucide-react"

interface ReviewScreenProps {
  state: ReviewState
  setState: React.Dispatch<React.SetStateAction<ReviewState>>
  onSave: () => void | Promise<void>
  onSkip: () => void | Promise<void>
  saving?: boolean
}

type NavTab = "skills" | "experiences" | "education"

function formatDuration(months: number): string {
  const yrs = Math.floor(months / 12)
  const mo = months % 12
  if (yrs === 0) return `${mo} mo`
  if (mo === 0) return `${yrs} yr${yrs > 1 ? "s" : ""}`
  return `${yrs} yr${yrs > 1 ? "s" : ""} ${mo} mo`
}

function totalInsights(state: ReviewState): number {
  return (
    state.skills.length +
    state.experiences.length +
    state.education.length +
    state.projects.length +
    state.certifications.length
  )
}

function reviewedCount(state: ReviewState): number {
  const all = [
    ...state.skills,
    ...state.experiences,
    ...state.education,
    ...state.projects,
    ...state.certifications,
  ]
  return all.filter((x) => x.status === "approved" || x.status === "rejected").length
}

function approvedCount(state: ReviewState): number {
  const all = [
    ...state.skills,
    ...state.experiences,
    ...state.education,
    ...state.projects,
    ...state.certifications,
  ]
  return all.filter((x) => x.status === "approved").length
}

function SkillPill({
  name,
  status,
  onApprove,
  onReject,
}: {
  name: string
  status: ReviewState["skills"][number]["status"]
  onApprove: () => void
  onReject: () => void
}) {
  const approved = status === "approved"

  return (
    <button
      type="button"
      onClick={() => (approved ? onReject() : onApprove())}
      className={cn(
        "group inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition-all duration-200",
        approved
          ? "border-primary bg-primary text-primary-foreground shadow-md shadow-primary/20"
          : "border-border/80 bg-card text-foreground hover:border-primary/40 hover:shadow-sm",
      )}
    >
      {approved ? <Check className="size-3.5" aria-hidden="true" /> : null}
      {name}
      {!approved ? (
        <span
          role="presentation"
          onClick={(e) => {
            e.stopPropagation()
            onReject()
          }}
          className="ml-0.5 rounded-full p-0.5 text-muted-foreground opacity-60 transition-opacity hover:bg-muted hover:opacity-100"
        >
          <X className="size-3" aria-hidden="true" />
        </span>
      ) : null}
    </button>
  )
}

function IntelligenceProgress({ percent }: { percent: number }) {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    const t = window.setTimeout(() => setWidth(percent), 300)
    return () => window.clearTimeout(t)
  }, [percent])

  return (
    <div className="rounded-2xl border border-border/60 bg-card p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          Intelligence Progress
        </p>
        <span className="text-sm font-bold text-primary">{percent}%</span>
      </div>
      <div className="mt-3 h-2 overflow-hidden rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-primary transition-all duration-1000 ease-out"
          style={{ width: `${width}%` }}
        />
      </div>
      <p className="mt-2 flex items-center gap-1.5 text-xs text-muted-foreground">
        <span className="relative flex size-1.5">
          <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-60" />
          <span className="relative inline-flex size-1.5 rounded-full bg-emerald-500" />
        </span>
        Real-time analysis active
      </p>
    </div>
  )
}

export function ReviewScreen({ state, setState, onSave, onSkip, saving }: ReviewScreenProps) {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState<NavTab>("skills")
  const [skipOpen, setSkipOpen] = useState(false)

  const insights = totalInsights(state)
  const reviewed = reviewedCount(state)
  const approved = approvedCount(state)
  const progressPercent = insights > 0 ? Math.round((reviewed / insights) * 100) : 0

  const setSkill = (id: string, status: ReviewState["skills"][number]["status"]) =>
    setState((s) => ({ ...s, skills: s.skills.map((x) => (x.id === id ? { ...x, status } : x)) }))

  const setExp = (id: string, status: ReviewState["experiences"][number]["status"]) =>
    setState((s) => ({
      ...s,
      experiences: s.experiences.map((x) => (x.id === id ? { ...x, status } : x)),
    }))

  const setEdu = (id: string, status: ReviewState["education"][number]["status"]) =>
    setState((s) => ({
      ...s,
      education: s.education.map((x) => (x.id === id ? { ...x, status } : x)),
    }))

  function approveAll() {
    setState((s) => ({
      ...s,
      skills: s.skills.map((x) => ({ ...x, status: "approved" })),
      experiences: s.experiences.map((x) => ({ ...x, status: "approved" })),
      projects: s.projects.map((x) => ({ ...x, status: "approved" })),
      certifications: s.certifications.map((x) => ({ ...x, status: "approved" })),
      education: s.education.map((x) => ({ ...x, status: "approved" })),
    }))
  }

  const visibleSkills = useMemo(() => state.skills.slice(0, 7), [state.skills])
  const hiddenSkillCount = Math.max(0, state.skills.length - visibleSkills.length)

  const navItems: { id: NavTab; label: string; sub: string; icon: typeof Brain }[] = [
    {
      id: "skills",
      label: "Skills Matrix",
      sub: `${state.skills.length} Identified`,
      icon: Brain,
    },
    {
      id: "experiences",
      label: "Career Timeline",
      sub: `${state.experiences.length} Milestone${state.experiences.length === 1 ? "" : "s"}`,
      icon: LineChart,
    },
    {
      id: "education",
      label: "Academic Path",
      sub: `${state.education.length} Institution${state.education.length === 1 ? "" : "s"}`,
      icon: GraduationCap,
    },
  ]

  const contact = state.contact

  return (
    <div className="landing-hero-bg relative min-h-screen pb-28">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-32 top-1/4 size-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute -right-24 bottom-1/3 size-80 rounded-full bg-primary/8 blur-3xl" />
      </div>

      <header className="relative z-20 border-b border-border/40 bg-card/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <Link href="/">
              <Brand />
            </Link>
            <span className="hidden rounded-full border border-primary/20 bg-primary/5 px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-primary sm:inline">
              V2.0 Command Center
            </span>
          </div>
          <button
            type="button"
            onClick={() => setSkipOpen(true)}
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            Skip for now
          </button>
        </div>
      </header>

      <div className="relative z-10 mx-auto grid max-w-7xl gap-6 px-6 py-8 lg:grid-cols-[240px_1fr]">
        {/* Sidebar */}
        <aside className="flex flex-col gap-4 lg:sticky lg:top-24 lg:self-start">
          <IntelligenceProgress percent={progressPercent} />

          <nav className="space-y-1" aria-label="Intelligence sections">
            {navItems.map(({ id, label, sub, icon: Icon }) => {
              const pending =
                id === "skills"
                  ? state.skills.some((s) => s.status === "pending")
                  : id === "experiences"
                    ? state.experiences.some((e) => e.status === "pending")
                    : state.education.some((e) => e.status === "pending")

              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => setActiveTab(id)}
                  className={cn(
                    "flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left transition-all duration-200",
                    activeTab === id
                      ? "border-primary/30 bg-primary/5 shadow-sm"
                      : "border-transparent bg-transparent hover:border-border/60 hover:bg-card/60",
                  )}
                >
                  <span
                    className={cn(
                      "flex size-9 shrink-0 items-center justify-center rounded-lg",
                      activeTab === id ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground",
                    )}
                  >
                    <Icon className="size-4" />
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="flex items-center gap-2 text-sm font-semibold text-foreground">
                      {label}
                      {pending && activeTab === id ? (
                        <span className="size-1.5 rounded-full bg-primary" aria-hidden="true" />
                      ) : null}
                    </span>
                    <span className="text-xs text-muted-foreground">{sub}</span>
                  </span>
                  {activeTab === id ? (
                    <span className="hidden size-5 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-primary-foreground lg:flex">
                      !
                    </span>
                  ) : null}
                </button>
              )
            })}
          </nav>

          <div className="mt-auto hidden rounded-2xl border border-dashed border-border/80 bg-card/50 p-4 lg:block">
            <div className="flex items-center gap-2">
              <ShieldCheck className="size-4 text-emerald-600" />
              <div>
                <p className="text-xs font-semibold text-foreground">98% Accuracy</p>
                <p className="text-[10px] text-muted-foreground">Neural Confidence Score</p>
              </div>
            </div>
            <div className="mt-3 flex items-center gap-2 border-t border-border/60 pt-3">
              <Lock className="size-4 text-primary" />
              <div>
                <p className="text-xs font-semibold text-foreground">AES-256 Vault</p>
                <p className="text-[10px] text-muted-foreground">Advanced Identity Protection</p>
              </div>
            </div>
          </div>
        </aside>

        {/* Main */}
        <main className="min-w-0 space-y-6">
          <div className="animate-fade-in-up opacity-0" style={{ animationFillMode: "forwards" }}>
            <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Intelligence Command
            </h1>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-base">
              Our neural engine has decoded your professional DNA.{" "}
              <span className="font-semibold text-primary">
                Review the {insights} extracted insights
              </span>{" "}
              to ensure synchronization with executive-level opportunities.
            </p>
          </div>

          {/* Hero CTA */}
          <div
            className="animate-fade-in-up flex flex-col gap-4 rounded-2xl border border-primary/15 bg-primary/5 p-5 opacity-0 shadow-sm sm:flex-row sm:items-center sm:justify-between"
            style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}
          >
            <div className="flex items-center gap-4">
              <span className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-lg shadow-primary/25">
                <Sparkles className="size-6" />
              </span>
              <div>
                <p className="text-lg font-bold text-foreground">{insights} Strategic Insights</p>
                <p className="text-sm text-muted-foreground">
                  Ready for integration into your master profile
                </p>
              </div>
            </div>
            <Button
              className="btn-brand h-11 shrink-0 rounded-xl px-6 text-sm font-bold uppercase tracking-wide"
              onClick={approveAll}
            >
              <Zap className="size-4" />
              Approve Intelligence
            </Button>
          </div>

          {/* Grid */}
          <div
            className="animate-fade-in-up grid gap-5 opacity-0 lg:grid-cols-2"
            style={{ animationDelay: "0.2s", animationFillMode: "forwards" }}
          >
            {/* Skills Matrix */}
            <section
              className={cn(
                "rounded-2xl border border-border/80 bg-card p-5 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)] transition-opacity",
                activeTab !== "skills" && "lg:opacity-60",
              )}
            >
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <LayoutGrid className="size-4 text-primary" />
                  <h2 className="text-sm font-bold text-foreground">Neural Skills Matrix</h2>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    setState((s) => ({
                      ...s,
                      skills: s.skills.map((x) => ({ ...x, status: "approved" })),
                    }))
                  }
                  className="text-xs font-semibold text-primary hover:underline"
                >
                  Map All
                </button>
              </div>

              <div className="flex flex-wrap gap-2">
                {visibleSkills.map((skill) => (
                  <SkillPill
                    key={skill.id}
                    name={skill.name}
                    status={skill.status}
                    onApprove={() => setSkill(skill.id, "approved")}
                    onReject={() => setSkill(skill.id, "rejected")}
                  />
                ))}
                {hiddenSkillCount > 0 ? (
                  <span className="inline-flex items-center rounded-full border border-primary/20 bg-primary/5 px-3 py-1.5 text-xs font-semibold text-primary">
                    +{hiddenSkillCount} Insights
                  </span>
                ) : null}
              </div>

              <div className="mt-6 flex items-center justify-between border-t border-border/60 pt-4 text-xs text-muted-foreground">
                <span>Derived from {Math.max(1, state.experiences.length)} digital sources</span>
                {state.skills.filter((s) => s.status === "pending").length > 0 ? (
                  <span className="rounded-full bg-primary/10 px-2 py-0.5 font-semibold text-primary">
                    +{state.skills.filter((s) => s.status === "pending").length} pending
                  </span>
                ) : (
                  <span className="flex items-center gap-1 font-semibold text-primary">
                    <Check className="size-3.5" />
                    Mapped
                  </span>
                )}
              </div>
            </section>

            {/* Career Progression */}
            <section
              className={cn(
                "relative rounded-2xl border border-border/80 bg-card p-5 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)] transition-opacity",
                activeTab !== "experiences" && "lg:opacity-60",
              )}
            >
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <LineChart className="size-4 text-primary" />
                  <h2 className="text-sm font-bold text-foreground">Career Progression</h2>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    setState((s) => ({
                      ...s,
                      experiences: s.experiences.map((x) => ({ ...x, status: "approved" })),
                    }))
                  }
                  className="text-xs font-semibold text-primary hover:underline"
                >
                  Review
                </button>
              </div>

              <div className="space-y-0">
                {state.experiences.map((exp, i) => (
                  <ExperienceTimelineItem
                    key={exp.id}
                    exp={exp}
                    isFirst={i === 0}
                    onApprove={() => setExp(exp.id, "approved")}
                    onReject={() => setExp(exp.id, "rejected")}
                  />
                ))}
                {state.experiences.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No career milestones extracted.</p>
                ) : null}
              </div>

              <div className="mt-4 flex items-center justify-between border-t border-border/60 pt-4 text-xs">
                <span className="text-muted-foreground">Structural Consistency</span>
                <span className="flex items-center gap-1 font-semibold text-primary">
                  <Check className="size-3.5" />
                  100% Validated
                </span>
              </div>

              <div className="animate-float absolute -bottom-4 -right-3 hidden w-52 rounded-xl border border-border/60 bg-card p-3 shadow-xl lg:block">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="size-4 text-emerald-600" />
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                      Intelligence Verified
                    </p>
                    <p className="text-xs font-semibold text-foreground">Neural Confidence 99.8%</p>
                  </div>
                </div>
              </div>
            </section>
          </div>

          {/* Academic Path */}
          {state.education.length > 0 ? (
            <section
              className={cn(
                "animate-fade-in-up rounded-2xl border border-border/80 bg-card p-5 opacity-0 shadow-[0_10px_25px_-5px_rgba(0,0,0,0.05)]",
                activeTab !== "education" && "lg:opacity-60",
              )}
              style={{ animationDelay: "0.3s", animationFillMode: "forwards" }}
            >
              <div className="mb-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <GraduationCap className="size-4 text-primary" />
                  <h2 className="text-sm font-bold text-foreground">Academic Path</h2>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    setState((s) => ({
                      ...s,
                      education: s.education.map((x) => ({ ...x, status: "approved" })),
                    }))
                  }
                  className="text-xs font-semibold text-primary hover:underline"
                >
                  Validate All
                </button>
              </div>
              <div className="grid gap-3 sm:grid-cols-2">
                {state.education.map((edu) => (
                  <div
                    key={edu.id}
                    className={cn(
                      "rounded-xl border p-4 transition-colors",
                      edu.status === "approved"
                        ? "border-primary/30 bg-primary/5"
                        : "border-border/60 bg-surface/30",
                    )}
                  >
                    <p className="text-sm font-semibold text-foreground">{edu.degree}</p>
                    <p className="text-xs text-muted-foreground">
                      {edu.university}
                      {edu.graduationDate ? ` · ${edu.graduationDate}` : ""}
                    </p>
                    <div className="mt-3 flex gap-2">
                      <button
                        type="button"
                        onClick={() => setEdu(edu.id, "approved")}
                        className={cn(
                          "rounded-lg px-2.5 py-1 text-xs font-medium",
                          edu.status === "approved"
                            ? "bg-primary text-primary-foreground"
                            : "bg-muted text-muted-foreground hover:bg-primary/10 hover:text-primary",
                        )}
                      >
                        Approve
                      </button>
                      <button
                        type="button"
                        onClick={() => setEdu(edu.id, "rejected")}
                        className="rounded-lg px-2.5 py-1 text-xs font-medium text-muted-foreground hover:bg-muted"
                      >
                        Reject
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ) : null}

          {/* Contact footer bar */}
          <div
            className="animate-fade-in-up grid gap-4 rounded-2xl border border-border/80 bg-card p-4 opacity-0 shadow-sm sm:grid-cols-2 lg:grid-cols-4"
            style={{ animationDelay: "0.35s", animationFillMode: "forwards" }}
          >
            <ContactField icon={MapPin} label="Primary Base" value={contact.location || "—"} />
            <ContactField icon={Link2} label="Neural Link" value={contact.linkedin || "—"} />
            <ContactField icon={Code2} label="Source Node" value={contact.github || "—"} />
            <ContactField icon={Phone} label="Direct Channel" value={contact.phone || "—"} />
          </div>
        </main>
      </div>

      {/* Sticky footer */}
      <div className="fixed inset-x-0 bottom-0 z-30 border-t border-border/60 bg-card/95 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-6 py-4">
          <button
            type="button"
            onClick={() => setSkipOpen(true)}
            className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
          >
            Skip for now
          </button>
          <button
            type="button"
            onClick={() => router.push("/profile/upload")}
            className="hidden items-center gap-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline-flex"
          >
            <RefreshCw className="size-4" />
            Re-scan Documents
          </button>
          <Button
            disabled={approved === 0 || saving}
            onClick={() => void onSave()}
            className="btn-brand h-11 rounded-xl px-6 text-sm font-bold uppercase tracking-wide"
          >
            {saving ? "Integrating..." : "Confirm & Integrate"}
            <ChevronRight className="size-4" />
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

function ExperienceTimelineItem({
  exp,
  isFirst,
  onApprove,
  onReject,
}: {
  exp: ExperienceChange
  isFirst: boolean
  onApprove: () => void
  onReject: () => void
}) {
  const approved = exp.status === "approved"

  return (
    <div className="flex gap-3 pb-5 last:pb-0">
      <div className="flex flex-col items-center">
        <span
          className={cn(
            "size-2.5 shrink-0 rounded-full ring-4",
            approved || isFirst
              ? "bg-primary ring-primary/20"
              : "bg-muted-foreground/40 ring-muted/50",
          )}
        />
        <span className="mt-1 w-px flex-1 bg-border" />
      </div>
      <div className="min-w-0 flex-1 pb-1">
        <button
          type="button"
          onClick={() => (approved ? onReject() : onApprove())}
          className="text-left transition-opacity hover:opacity-80"
        >
          <p className="text-sm font-semibold text-foreground">{exp.title}</p>
          <p className="text-xs text-muted-foreground">
            {exp.company} · {formatDuration(exp.durationMonths)}
          </p>
        </button>
        {exp.status === "pending" ? (
          <div className="mt-2 flex gap-2">
            <button
              type="button"
              onClick={onApprove}
              className="rounded-md bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary hover:bg-primary/20"
            >
              Approve
            </button>
            <button
              type="button"
              onClick={onReject}
              className="rounded-md px-2 py-0.5 text-[10px] font-medium text-muted-foreground hover:bg-muted"
            >
              Reject
            </button>
          </div>
        ) : null}
      </div>
    </div>
  )
}

function ContactField({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof MapPin
  label: string
  value: string
}) {
  return (
    <div className="flex items-start gap-3">
      <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
        <Icon className="size-4" />
      </span>
      <div className="min-w-0">
        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{label}</p>
        <p className="truncate text-sm font-medium text-foreground">{value}</p>
      </div>
    </div>
  )
}
