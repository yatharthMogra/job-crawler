"use client"

import type { CommittedProfile } from "@/lib/profile/build-profile"
import { educationLevelLabel } from "@/lib/profile/contact"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import {
  FlowPage,
  FlowPageContent,
  FlowPageHeader,
  FlowPageHero,
  FlowPanel,
} from "@/components/ui/flow-page"
import {
  ArrowRight,
  Award as AwardIcon,
  Briefcase,
  FolderGit2,
  GraduationCap,
  PartyPopper,
  Rocket,
  Sparkles,
} from "lucide-react"

interface ConfirmationScreenProps {
  profile: CommittedProfile
  onViewProfile: () => void
}

export function ConfirmationScreen({ profile, onViewProfile }: ConfirmationScreenProps) {
  const allSkillNames = profile.skills.flatMap((s) => s.names)

  const stats = [
    profile.skillCount > 0
      ? { label: "Skills", value: profile.skillCount, icon: Sparkles }
      : null,
    profile.experiences.length > 0
      ? { label: "Experience", value: profile.experiences.length, icon: Briefcase }
      : null,
    profile.primaryRoles.length > 0
      ? { label: "Target roles", value: profile.primaryRoles.length, icon: Rocket }
      : null,
    profile.educationEntries.length > 0
      ? { label: "Education", value: profile.educationEntries.length, icon: GraduationCap }
      : null,
  ].filter(Boolean) as { label: string; value: number; icon: typeof Sparkles }[]

  return (
    <FlowPage>
      <FlowPageHeader className="max-w-lg">
        <Brand />
      </FlowPageHeader>

      <FlowPageContent className="max-w-lg" narrow>
        <FlowPageHero
          icon={PartyPopper}
          iconTone="success"
          title="You're all set!"
          description="Your profile is ready. We've saved everything below — jump into matched roles and start applying."
        />

        {stats.length > 0 ? (
          <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {stats.map((s) => (
              <div
                key={s.label}
                className="rounded-xl border-2 border-border bg-card px-3 py-4 text-center shadow-sm"
              >
                <s.icon className="mx-auto size-4 text-primary" aria-hidden="true" />
                <p className="mt-2 text-2xl font-bold text-foreground">{s.value}</p>
                <p className="text-xs text-muted-foreground">{s.label}</p>
              </div>
            ))}
          </div>
        ) : null}

        <FlowPanel className="divide-y divide-border/60 p-0">
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

          {profile.primaryRoles.length > 0 ? (
            <SummaryRow
              icon={<Rocket className="size-4" aria-hidden="true" />}
              title={`Target roles (${profile.primaryRoles.length})`}
              body={profile.primaryRoles.join(", ")}
            />
          ) : null}

          {profile.educationEntries.length > 0 ? (
            <SummaryRow
              icon={<GraduationCap className="size-4" aria-hidden="true" />}
              title={`Education (${profile.educationEntries.length})`}
              body={profile.educationEntries
                .map(
                  (e) =>
                    `${educationLevelLabel(e.level)}: ${e.degree} at ${e.university}${
                      e.gpa ? ` (GPA ${e.gpa})` : ""
                    }`,
                )
                .join(" · ")}
            />
          ) : null}
        </FlowPanel>

        <div className="mt-6 space-y-3">
          <Button className="btn-brand h-12 w-full text-base" size="lg" onClick={onViewProfile}>
            Browse matched jobs
            <ArrowRight className="size-4" aria-hidden="true" />
          </Button>
          <p className="text-center text-xs text-muted-foreground">
            Each role shows a match score and why it fits — tap Apply when you&apos;re ready.
          </p>
        </div>
      </FlowPageContent>
    </FlowPage>
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
    <div className="flex gap-3 p-4 sm:p-5">
      <span className="mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-accent to-brand-muted text-primary">
        {icon}
      </span>
      <div className="min-w-0">
        <p className="text-sm font-semibold text-foreground">{title}</p>
        <p className="mt-1 text-pretty text-sm leading-relaxed text-muted-foreground">{body}</p>
      </div>
    </div>
  )
}
