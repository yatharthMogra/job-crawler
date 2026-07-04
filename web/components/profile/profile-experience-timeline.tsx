"use client"

import { Building2 } from "lucide-react"
import type { CommittedProfile } from "@/lib/profile/build-profile"
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
  return `${range} (${formatDuration(durationMonths)})`
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
    <div className="relative space-y-0 pl-1">
      {experiences.map((exp, index) => {
        const isPresent = index === 0
        const isLast = index === experiences.length - 1
        let endAnchor = new Date()
        if (!isPresent) {
          for (let i = 0; i < index; i++) {
            endAnchor = new Date(endAnchor)
            endAnchor.setMonth(endAnchor.getMonth() - experiences[i].durationMonths)
          }
        }
        const period = experiencePeriod(exp.durationMonths, isPresent, endAnchor)
        return (
          <div key={exp.id} className="relative flex gap-4 pb-10 last:pb-0">
            {!isLast ? (
              <span
                className="absolute left-[19px] top-10 bottom-0 w-px bg-primary/20"
                aria-hidden="true"
              />
            ) : null}
            <div
              className={cn(
                "relative z-[1] flex size-10 shrink-0 items-center justify-center rounded-full border-2",
                isPresent
                  ? "border-primary/30 bg-primary/10 text-primary"
                  : "border-sky-200 bg-sky-50 text-sky-700",
              )}
            >
              <Building2 className="size-4" strokeWidth={2} />
            </div>
            <div className="min-w-0 flex-1 pt-0.5">
              <div className="flex flex-wrap items-start justify-between gap-2">
                <div>
                  <h3 className="text-base font-bold text-slate-900">{exp.title}</h3>
                  <p className="text-[15px] font-semibold text-primary">{exp.company}</p>
                  <p className="mt-0.5 text-sm text-muted-foreground">{period}</p>
                </div>
                {isPresent ? (
                  <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wide text-emerald-800">
                    Present
                  </span>
                ) : null}
              </div>
              {exp.keywords.length > 0 ? (
                <div className="mt-4 rounded-xl border border-border/60 bg-card p-4 shadow-sm">
                  <ul className="space-y-2 text-[14px] leading-relaxed text-foreground/85">
                    {exp.keywords.slice(0, 4).map((kw) => (
                      <li key={kw} className="flex gap-2">
                        <span className="mt-2 size-1.5 shrink-0 rounded-full bg-primary/70" />
                        <span>{kw}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          </div>
        )
      })}
    </div>
  )
}
