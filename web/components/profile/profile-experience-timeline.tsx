"use client"

import { Building2, CheckCircle2 } from "lucide-react"
import { BrandLogo } from "@/components/brand-logo"
import type { CommittedProfile } from "@/lib/profile/build-profile"
import { splitExperienceContent } from "@/lib/profile/experience-display"
import { cn } from "@/lib/utils"

function formatDuration(months: number): string {
  if (months < 1) return "—"
  const yrs = Math.floor(months / 12)
  const mo = months % 12
  if (yrs === 0) return `${mo} mo${mo === 1 ? "" : "s"}`
  if (mo === 0) return `${yrs} yr${yrs === 1 ? "" : "s"}`
  return `${yrs} yr${yrs === 1 ? "" : "s"} ${mo} mo${mo === 1 ? "" : "s"}`
}

function monthLabel(date: Date): string {
  return date.toLocaleDateString("en-US", { month: "short", year: "numeric" })
}

function experiencePeriod(
  durationMonths: number,
  isPresent: boolean,
  endAnchor: Date,
): string {
  const end = new Date(endAnchor)
  const start = new Date(end)
  start.setMonth(start.getMonth() - durationMonths)
  const range = isPresent
    ? `${monthLabel(start)} – Present`
    : `${monthLabel(start)} – ${monthLabel(end)}`
  return `${range} · ${formatDuration(durationMonths)}`
}

export function ProfileExperienceTimeline({
  experiences,
}: {
  experiences: CommittedProfile["experiences"]
}) {
  if (experiences.length === 0) {
    return <p className="text-sm text-muted-foreground">No experience on your profile yet.</p>
  }

  return (
    <div className="space-y-5">
      {experiences.map((exp, index) => {
        const isPresent = index === 0
        let endAnchor = new Date()
        if (!isPresent) {
          for (let i = 0; i < index; i++) {
            endAnchor = new Date(endAnchor)
            endAnchor.setMonth(endAnchor.getMonth() - experiences[i].durationMonths)
          }
        }
        const period = experiencePeriod(exp.durationMonths, isPresent, endAnchor)
        const { accomplishments, technologies } = splitExperienceContent(exp.keywords, exp.domains)

        return (
          <article
            key={exp.id}
            className={cn(
              "rounded-2xl border bg-card p-5 shadow-sm transition-colors sm:p-6",
              isPresent ? "border-primary/25 shadow-primary/5" : "border-border/60",
            )}
          >
            <div className="flex gap-4">
              <BrandLogo
                name={exp.company}
                variant="company"
                size={48}
                shape="square"
                className="shrink-0"
              />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div>
                    <h3 className="text-lg font-bold tracking-tight text-foreground">{exp.title}</h3>
                    <p className="mt-0.5 flex flex-wrap items-center gap-x-2 text-sm font-semibold text-primary">
                      <Building2 className="size-3.5 shrink-0" />
                      {exp.company}
                    </p>
                    <p className="mt-1 text-sm text-muted-foreground">{period}</p>
                  </div>
                  {isPresent ? (
                    <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wide text-emerald-800">
                      Current
                    </span>
                  ) : null}
                </div>

                {accomplishments.length > 0 ? (
                  <div className="mt-5">
                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                      Key impact
                    </p>
                    <ul className="mt-3 space-y-2.5">
                      {accomplishments.map((item) => (
                        <li key={item} className="flex gap-2.5 text-[14px] leading-relaxed text-foreground/90">
                          <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-600" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}

                {technologies.length > 0 ? (
                  <div className={cn("mt-5", accomplishments.length === 0 && "mt-4")}>
                    <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                      {accomplishments.length > 0 ? "Technologies" : "Focus areas"}
                    </p>
                    <div className="mt-2.5 flex flex-wrap gap-1.5">
                      {technologies.map((tech) => (
                        <span
                          key={tech}
                          className="rounded-md border border-border/70 bg-muted/40 px-2.5 py-1 text-xs font-medium text-foreground/80"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                ) : null}
              </div>
            </div>
          </article>
        )
      })}
    </div>
  )
}
