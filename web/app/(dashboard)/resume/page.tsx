"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { Plus, FileText, MoreHorizontal, Star } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { formatRelativeTime } from "@/lib/profile/map-profile"
import { Button } from "@/components/ui/button"
import { FeedSkeleton } from "@/components/card-skeleton"

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
        <div className="border-b border-border/80 bg-card/80 px-6 py-4 backdrop-blur-sm">
          <h1 className="text-lg font-bold tracking-tight text-foreground">Resume</h1>
        </div>
        <div className="px-6 py-4">
          <FeedSkeleton count={2} />
        </div>
      </div>
    )
  }

  const { resumes, primaryRoles, resumeCount } = profileHome
  const targetTitles = primaryRoles.join(", ") || "—"

  return (
    <div>
      <div className="flex items-center justify-between border-b border-border/80 bg-card/80 px-6 py-4 backdrop-blur-sm">
        <div>
          <h1 className="text-lg font-bold tracking-tight text-foreground">Resume</h1>
          <p className="text-xs text-muted-foreground">Manage versions used for matching</p>
        </div>
        <Button
          className="btn-brand"
          size="sm"
          onClick={resetForNewResume}
          disabled={resumeCount >= MAX_SLOTS}
        >
          <Plus className="size-4" />
          Add Resume
        </Button>
      </div>

      <div className="mx-6 mt-4 flex items-center gap-2 rounded-xl border border-brand-muted/80 bg-brand-muted/40 px-4 py-3 text-sm text-brand-foreground">
        <FileText className="size-4 text-primary" />
        You have {resumeCount} resume{resumeCount === 1 ? "" : "s"} saved out of {MAX_SLOTS}{" "}
        available slots.
      </div>

      <div className="card-elevated mx-6 mt-4 overflow-hidden border-0">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-border/60 bg-surface text-xs text-muted-foreground">
            <tr>
              <th className="px-4 py-3 font-medium">Resume</th>
              <th className="px-4 py-3 font-medium">Target Job Title</th>
              <th className="px-4 py-3 font-medium">Last Modified</th>
              <th className="px-4 py-3 font-medium">Created</th>
              <th className="px-4 py-3 w-10" />
            </tr>
          </thead>
          <tbody>
            {resumes.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-muted-foreground">
                  No resumes yet.{" "}
                  <button
                    type="button"
                    className="font-medium text-primary underline-offset-2 hover:underline"
                    onClick={resetForNewResume}
                  >
                    Upload your first resume
                  </button>
                </td>
              </tr>
            ) : (
              resumes.map((resume, index) => (
                <tr key={resume.id} className="border-b border-border/40 last:border-0">
                  <td className="px-4 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex size-9 items-center justify-center rounded-lg bg-gradient-to-br from-primary/15 to-brand-muted text-sm font-bold text-primary">
                        {resume.originalFilename.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <p className="font-medium text-foreground">{resume.originalFilename}</p>
                        <div className="mt-1 flex flex-wrap gap-1">
                          {index === 0 ? (
                            <span className="inline-flex items-center gap-0.5 rounded-md border border-primary/20 bg-accent px-1.5 py-0.5 text-[10px] font-semibold uppercase text-accent-foreground">
                              <Star className="size-2.5 fill-current" />
                              Primary
                            </span>
                          ) : null}
                          <span className="rounded-md bg-add-muted px-1.5 py-0.5 text-[10px] text-add-foreground">
                            Analysis complete
                          </span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-4 text-muted-foreground">{targetTitles}</td>
                  <td className="px-4 py-4 text-muted-foreground">
                    {formatRelativeTime(resume.uploadedAt)}
                  </td>
                  <td className="px-4 py-4 text-muted-foreground">
                    {formatRelativeTime(resume.uploadedAt)}
                  </td>
                  <td className="px-4 py-4">
                    <button
                      type="button"
                      className="rounded p-1 text-muted-foreground hover:bg-secondary"
                      onClick={() => router.push("/profile")}
                    >
                      <MoreHorizontal className="size-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
