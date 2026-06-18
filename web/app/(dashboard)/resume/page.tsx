"use client"

import { useEffect } from "react"
import { FileText, MoreHorizontal, Plus, Star } from "lucide-react"
import { useRouter } from "next/navigation"
import { AppHeader } from "@/components/layout/app-header"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { formatRelativeTime } from "@/lib/profile/map-profile"
import { Button } from "@/components/ui/button"
import { FeedSkeleton } from "@/components/card-skeleton"
import { cn } from "@/lib/utils"

const MAX_SLOTS = 5

export default function ResumePage() {
  const router = useRouter()
  const { candidateId } = useSession()
  const { profileHome, loadProfileHome, resetForNewResume } = useProfileFlow()

  useEffect(() => {
    if (candidateId) void loadProfileHome(candidateId).catch(() => undefined)
  }, [candidateId, loadProfileHome])

  if (!profileHome) {
    return (
      <div>
        <AppHeader title="Resume" subtitle="Manage versions used for matching" showSearch={false} />
        <div className="px-6 py-4">
          <FeedSkeleton count={2} />
        </div>
      </div>
    )
  }

  const { resumes, primaryRoles, resumeCount } = profileHome
  const targetTitles = primaryRoles.join(", ") || "—"

  return (
    <div className="dashboard-page-bg min-h-screen">
      <AppHeader
        title="Resume"
        subtitle="Manage versions used for matching"
        showSearch={false}
        action={
          <Button
            className="btn-brand"
            size="sm"
            onClick={resetForNewResume}
            disabled={resumeCount >= MAX_SLOTS}
          >
            <Plus className="size-4" />
            Add Resume
          </Button>
        }
      />

      <div className="mx-6 mt-4 flex items-center gap-2 rounded-xl border border-primary/15 bg-accent/40 px-4 py-3 text-sm text-accent-foreground">
        <FileText className="size-4 text-primary" />
        You have {resumeCount} resume{resumeCount === 1 ? "" : "s"} saved out of {MAX_SLOTS}{" "}
        available slots.
      </div>

      <div className="space-y-4 p-6">
        {resumes.length === 0 ? (
          <div className="card-elevated px-6 py-12 text-center">
            <p className="text-muted-foreground">
              No resumes yet.{" "}
              <button
                type="button"
                className="font-medium text-primary underline-offset-2 hover:underline"
                onClick={resetForNewResume}
              >
                Upload your first resume
              </button>
            </p>
          </div>
        ) : (
          resumes.map((resume, index) => (
            <div
              key={resume.id}
              className={cn(
                "card-elevated flex items-center justify-between gap-4 p-5 transition-colors hover:border-primary/25",
                index === 0 && "border-primary/20",
              )}
            >
              <div className="flex min-w-0 items-center gap-4">
                <div className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-lg font-bold text-primary">
                  {resume.originalFilename.charAt(0).toUpperCase()}
                </div>
                <div className="min-w-0">
                  <p className="truncate font-semibold text-foreground">{resume.originalFilename}</p>
                  <p className="mt-0.5 truncate text-sm text-muted-foreground">{targetTitles}</p>
                  <div className="mt-2 flex flex-wrap gap-1.5">
                    {index === 0 ? (
                      <span className="inline-flex items-center gap-0.5 rounded-md border border-primary/20 bg-accent px-2 py-0.5 text-[10px] font-semibold uppercase text-primary">
                        <Star className="size-2.5 fill-current" />
                        Primary
                      </span>
                    ) : null}
                    <span className="rounded-md bg-add-muted px-2 py-0.5 text-[10px] font-medium text-add-foreground">
                      Analysis complete
                    </span>
                  </div>
                </div>
              </div>

              <div className="flex shrink-0 items-center gap-6 text-sm text-muted-foreground">
                <div className="hidden text-right sm:block">
                  <p className="text-[10px] uppercase tracking-wider">Modified</p>
                  <p>{formatRelativeTime(resume.uploadedAt)}</p>
                </div>
                <button
                  type="button"
                  className="rounded-lg p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
                  onClick={() => router.push("/profile")}
                  aria-label="More options"
                >
                  <MoreHorizontal className="size-5" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
