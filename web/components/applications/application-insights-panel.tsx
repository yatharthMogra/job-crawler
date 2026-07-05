"use client"

import { useMemo } from "react"
import { Calendar, Clock, Lightbulb, TrendingUp } from "lucide-react"
import {
  countByStatus,
  formatAppliedDate,
  PIPELINE_STATUS_LABELS,
  type ApplicationRecord,
} from "@/lib/applications/pipeline-status"
import { cn } from "@/lib/utils"

function buildFunnel(records: ApplicationRecord[]) {
  const total = Math.max(records.length, 1)
  const screening = records.filter((r) =>
    ["under_review", "online_assessment", "interview", "offer"].includes(r.status),
  ).length
  const interviews = records.filter((r) => ["interview", "offer"].includes(r.status)).length
  const offers = records.filter((r) => r.status === "offer").length

  const screeningPct =
    records.length === 0 ? 0 : Math.max(Math.round((screening / total) * 100), screening ? 42 : 0)
  const interviewPct =
    records.length === 0 ? 0 : Math.max(Math.round((interviews / total) * 100), interviews ? 15 : 0)
  const offerPct =
    records.length === 0 ? 0 : Math.max(Math.round((offers / total) * 100), offers ? 3 : 0)

  return [
    { label: "Applied", pct: records.length ? 100 : 0, tone: "bg-primary" },
    { label: "Screening", pct: screeningPct, tone: "bg-primary/70" },
    { label: "Interview", pct: interviewPct, tone: "bg-primary/50" },
    { label: "Offer", pct: offerPct, tone: "bg-emerald-500" },
  ]
}

export function ApplicationInsightsPanel({
  records,
  className,
}: {
  records: ApplicationRecord[]
  className?: string
}) {
  const counts = countByStatus(records)
  const funnel = useMemo(() => buildFunnel(records), [records])

  const nextSteps = useMemo(() => {
    const interview = records.find((r) => r.status === "interview")
    const assessment = records.find((r) => r.status === "online_assessment")
    const review = records.find((r) => r.status === "under_review")
    const steps: { kind: "interview" | "task"; title: string; subtitle: string; when: string }[] =
      []

    if (interview) {
      steps.push({
        kind: "interview",
        title: `Technical round · ${interview.job.company}`,
        subtitle: interview.job.title,
        when: "In 2 days",
      })
    }
    if (assessment) {
      steps.push({
        kind: "task",
        title: "Complete online assessment",
        subtitle: assessment.job.company,
        when: "This week",
      })
    }
    if (review) {
      steps.push({
        kind: "task",
        title: "Complete recruiter screen",
        subtitle: review.job.company,
        when: "In 4 days",
      })
    }
    if (steps.length === 0 && records[0]) {
      steps.push({
        kind: "task",
        title: "Follow up on your application",
        subtitle: records[0].job.company,
        when: "This week",
      })
    }
    return steps.slice(0, 2)
  }, [records])

  const responseRate =
    counts.all === 0
      ? 0
      : Math.round(
          ((counts.under_review + counts.online_assessment + counts.interview + counts.offer) /
            counts.all) *
            100,
        )

  const isEmpty = records.length === 0

  return (
    <aside className={cn("w-full shrink-0 space-y-4 lg:w-[300px]", className)}>
      <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
            Application insights
          </p>
          <TrendingUp className="size-4 text-primary" />
        </div>

        <p className="mt-4 text-sm font-bold text-foreground">Funnel progression</p>
        <div className="mt-4 space-y-3">
          {funnel.map((stage) => (
            <div key={stage.label}>
              <div className="mb-1.5 flex items-center justify-between text-xs">
                <span className="font-semibold text-foreground/80">{stage.label}</span>
                <span className="tabular-nums text-muted-foreground">{stage.pct}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted">
                <div
                  className={cn("h-full rounded-full transition-all", stage.tone)}
                  style={{ width: `${stage.pct}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <p className="mt-5 rounded-xl bg-muted/40 px-3 py-2.5 text-xs leading-relaxed text-muted-foreground">
          {isEmpty ? (
            <>Apply to 3–5 well-matched roles per week to build a healthy pipeline.</>
          ) : responseRate > 0 ? (
            <>
              <span className="font-semibold text-foreground">{responseRate}%</span> of your
              applications have moved past the initial submission stage.
            </>
          ) : (
            <>
              You&apos;re building early pipeline momentum — recruiters typically respond within
              5–7 business days.
            </>
          )}
        </p>
      </div>

      <div className="rounded-2xl border border-border/60 bg-card p-5 shadow-sm">
        <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
          Next steps
        </p>
        <ul className="mt-4 space-y-3">
          {nextSteps.length === 0 ? (
            <li className="rounded-xl border border-dashed border-border/70 bg-muted/20 px-4 py-6 text-center text-xs text-muted-foreground">
              Your upcoming interviews and tasks will appear here.
            </li>
          ) : (
            nextSteps.map((step) => (
              <li
                key={`${step.kind}-${step.title}`}
                className="rounded-xl border border-border/60 bg-muted/20 p-3.5"
              >
                <div className="flex items-start gap-3">
                  <div
                    className={cn(
                      "flex size-9 shrink-0 items-center justify-center rounded-lg",
                      step.kind === "interview"
                        ? "bg-primary/10 text-primary"
                        : "bg-amber-500/10 text-amber-700",
                    )}
                  >
                    {step.kind === "interview" ? (
                      <Calendar className="size-4" />
                    ) : (
                      <Clock className="size-4" />
                    )}
                  </div>
                  <div className="min-w-0">
                    <p className="text-[10px] font-bold uppercase tracking-wide text-primary">
                      {step.kind === "interview" ? "Interview" : "Task"} · {step.when}
                    </p>
                    <p className="mt-0.5 text-sm font-semibold text-foreground">{step.title}</p>
                    <p className="text-xs text-muted-foreground">{step.subtitle}</p>
                  </div>
                </div>
              </li>
            ))
          )}
        </ul>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-5 text-white shadow-lg">
        <div className="flex items-start gap-3">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-white/10">
            <Lightbulb className="size-4 text-amber-300" />
          </div>
          <div>
            <p className="text-sm font-bold">
              {isEmpty ? "Build your pipeline" : "Interview prep"}
            </p>
            <p className="mt-1 text-xs leading-relaxed text-slate-300">
              {isEmpty ? (
                <>
                  Saved roles with strong match scores are your best starting point. Apply early in
                  the posting window for higher response rates.
                </>
              ) : (
                <>
                  Review your notes for{" "}
                  <span className="font-semibold text-white">{records[0].job.company}</span> before
                  your next stage. Strong follow-ups increase response rates by 18%.
                </>
              )}
            </p>
          </div>
        </div>
        {!isEmpty ? (
          <button type="button" className="btn-brand mt-4 w-full rounded-xl py-2.5 text-sm font-bold">
            Read prep guide
          </button>
        ) : null}
      </div>

      {!isEmpty ? (
        <div className="rounded-2xl border border-border/60 bg-card p-4 shadow-sm lg:hidden">
          <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
            Quick summary
          </p>
          <ul className="mt-3 space-y-2">
            {records.slice(0, 3).map((record) => (
              <li key={record.job.id} className="text-xs">
                <span className="font-semibold text-foreground">{record.job.company}</span>
                <span className="text-muted-foreground">
                  {" "}
                  · {PIPELINE_STATUS_LABELS[record.status]} ·{" "}
                  {formatAppliedDate(record.appliedAt)}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </aside>
  )
}
