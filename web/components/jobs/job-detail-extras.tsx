"use client"

import { Check, Lock, Mail, Sparkles } from "lucide-react"
import type { JobWithRole } from "@/lib/jobs-data"
import { cn } from "@/lib/utils"

const RECRUITER_NAMES = [
  "Sarah Chen",
  "Marcus Webb",
  "Priya Nair",
  "Jordan Lee",
  "Alex Rivera",
  "Emily Hart",
]

const MANAGER_TITLES: Record<string, string> = {
  "Backend Engineer": "Engineering Manager",
  "Full Stack": "Engineering Manager",
  DevOps: "Platform Lead",
  "Product Designer": "Design Director",
  "Data Engineer": "Data Science Lead",
}

function hashId(id: string): number {
  let h = 0
  for (let i = 0; i < id.length; i++) h = (h + id.charCodeAt(i) * (i + 1)) % 9973
  return h
}

export function mockHiringContact(job: JobWithRole) {
  const h = hashId(job.id)
  return {
    name: RECRUITER_NAMES[h % RECRUITER_NAMES.length]!,
    title: MANAGER_TITLES[job.roleCategory] ?? "Talent Partner",
    initials: RECRUITER_NAMES[h % RECRUITER_NAMES.length]!
      .split(" ")
      .map((n) => n[0])
      .join("")
      .slice(0, 2),
  }
}

export function buildRoleAboutIntro(job: JobWithRole): string {
  if (job.company_info?.one_line_description) {
    return job.company_info.one_line_description
  }
  const focus = job.skills.slice(0, 3).join(", ")
  const remote = job.remote_type === "remote" ? "remote-first" : job.remote_type
  return `${job.company} is hiring a ${job.title} to help build and scale products on the ${job.roleCategory} track. This ${remote} role focuses on ${focus || "high-impact delivery"} and works closely with cross-functional partners from design through production.`
}

export function HiringTeamUpsell({ job, className }: { job: JobWithRole; className?: string }) {
  const contact = mockHiringContact(job)

  return (
    <div className={cn("relative min-h-[220px] overflow-hidden rounded-xl border border-border/70 bg-card", className)}>
      <div className="blur-[5px] select-none" aria-hidden="true">
        <div className="p-4">
          <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
            Hiring team
          </p>
          <div className="mt-3 flex items-center gap-3">
            <div className="flex size-11 shrink-0 items-center justify-center rounded-full bg-primary/15 text-sm font-bold text-primary">
              {contact.initials}
            </div>
            <div>
              <p className="font-semibold text-foreground">{contact.name}</p>
              <p className="text-sm text-muted-foreground">{contact.title}</p>
            </div>
          </div>
          <button
            type="button"
            tabIndex={-1}
            className="btn-brand mt-4 flex w-full items-center justify-center gap-2 rounded-lg py-2.5 text-sm font-semibold"
          >
            <Mail className="size-4" />
            Message recruiter
          </button>
        </div>
      </div>

      <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 bg-background/55 px-4 text-center backdrop-blur-[1px]">
        <span className="flex size-9 items-center justify-center rounded-full bg-primary/10 text-primary">
          <Lock className="size-4" />
        </span>
        <p className="text-sm font-bold text-foreground">Unlock with Plus</p>
        <p className="text-xs leading-relaxed text-muted-foreground">
          See hiring manager contact and message recruiters directly.
        </p>
        <button
          type="button"
          className="mt-1 rounded-full bg-primary px-4 py-1.5 text-xs font-bold text-primary-foreground"
        >
          Upgrade to Plus
        </button>
      </div>
    </div>
  )
}

export function JobScoutPlusUpsell({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-4 text-white shadow-lg",
        className,
      )}
    >
      <div className="flex items-center gap-2">
        <Sparkles className="size-4 text-violet-300" />
        <p className="text-sm font-bold">Job Scout Plus</p>
      </div>
      <p className="mt-2 text-xs leading-relaxed text-slate-300">
        Get recruiter contacts, priority applications, and 3× more visibility on top matches.
      </p>
      <button
        type="button"
        className="mt-3 w-full rounded-lg bg-white/10 py-2 text-xs font-semibold text-white transition-colors hover:bg-white/15"
      >
        Learn about Plus
      </button>
    </div>
  )
}

export function ResponsibilityList({ items }: { items: string[] }) {
  if (items.length === 0) return null
  return (
    <ul className="space-y-3">
      {items.map((item) => (
        <li key={item} className="flex gap-3 text-[15px] leading-relaxed text-foreground/90">
          <span className="mt-0.5 flex size-5 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
            <Check className="size-3" strokeWidth={2.5} />
          </span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}
