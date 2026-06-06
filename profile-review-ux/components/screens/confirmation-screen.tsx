"use client"

import type { CommittedProfile } from "@/lib/build-profile"
import { Brand } from "@/components/brand"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { ArrowRight, Check, FolderGit2, Award as AwardIcon, Briefcase, Sparkles } from "lucide-react"

interface ConfirmationScreenProps {
  profile: CommittedProfile
  onViewProfile: () => void
}

export function ConfirmationScreen({ profile, onViewProfile }: ConfirmationScreenProps) {
  const allSkillNames = profile.skills.flatMap((s) => s.names)

  return (
    <main className="flex min-h-screen flex-col items-center bg-background px-6 py-10">
      <header className="w-full max-w-lg">
        <Brand />
      </header>

      <div className="flex w-full max-w-lg flex-1 flex-col justify-center py-8">
        <div className="mb-6 text-center">
          <span className="mx-auto flex size-14 items-center justify-center rounded-full bg-add-muted text-add">
            <Check className="size-7" aria-hidden="true" />
          </span>
          <h1 className="mt-4 text-balance text-2xl font-semibold tracking-tight text-foreground sm:text-3xl">
            Profile updated
          </h1>
          <p className="mt-2 text-muted-foreground">Here&apos;s what we saved to your profile.</p>
        </div>

        <Card className="divide-y divide-border p-0">
          {allSkillNames.length > 0 ? (
            <SummaryRow
              icon={<Sparkles className="size-4" aria-hidden="true" />}
              title={`Skills (${profile.skillCount})`}
              body={allSkillNames.join(", ")}
            />
          ) : null}

          {profile.experiences.length > 0 ? (
            <SummaryRow
              icon={<Briefcase className="size-4" aria-hidden="true" />}
              title={`Experiences (${profile.experiences.length})`}
              body={profile.experiences.map((e) => `${e.title} at ${e.company}`).join(" · ")}
            />
          ) : null}

          {profile.projects.length > 0 ? (
            <SummaryRow
              icon={<FolderGit2 className="size-4" aria-hidden="true" />}
              title={`Projects (${profile.projects.length})`}
              body={profile.projects.map((p) => p.name).join(", ")}
            />
          ) : null}

          {profile.certifications.length > 0 ? (
            <SummaryRow
              icon={<AwardIcon className="size-4" aria-hidden="true" />}
              title={`Certifications (${profile.certifications.length})`}
              body={profile.certifications.map((c) => c.name).join(", ")}
            />
          ) : null}
        </Card>

        {profile.capabilities.length > 0 ? (
          <div className="mt-4 rounded-xl border border-primary/30 bg-accent/50 p-4">
            <p className="text-sm font-medium text-accent-foreground">Capabilities generated</p>
            <div className="mt-2 flex flex-wrap gap-2">
              {profile.capabilities.map((c) => (
                <span
                  key={c.name}
                  className="rounded-full bg-card px-3 py-1 text-sm font-medium text-foreground shadow-sm"
                >
                  {c.name}
                </span>
              ))}
            </div>
            <p className="mt-3 text-xs leading-relaxed text-muted-foreground">
              Your capabilities have been automatically updated based on your approved evidence.
            </p>
          </div>
        ) : null}

        <Button className="mt-6 w-full" size="lg" onClick={onViewProfile}>
          View my profile
          <ArrowRight className="size-4" aria-hidden="true" />
        </Button>
      </div>
    </main>
  )
}

function SummaryRow({
  icon,
  title,
  body,
}: {
  icon: React.ReactNode
  title: string
  body: string
}) {
  return (
    <div className="flex gap-3 p-4">
      <span className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
        {icon}
      </span>
      <div className="min-w-0">
        <p className="text-sm font-semibold text-foreground">{title}</p>
        <p className="mt-0.5 text-pretty text-sm text-muted-foreground">{body}</p>
      </div>
    </div>
  )
}
