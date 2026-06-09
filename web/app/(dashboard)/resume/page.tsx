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
        <div className="border-b border-zinc-200/80 bg-white px-6 py-4">
          <h1 className="text-lg font-bold tracking-tight text-zinc-900">Resume</h1>
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
      <div className="flex items-center justify-between border-b border-zinc-200/80 bg-white px-6 py-4">
        <div>
          <h1 className="text-lg font-bold tracking-tight text-zinc-900">Resume</h1>
          <p className="text-xs text-zinc-500">Manage versions used for matching</p>
        </div>
        <Button
          className="bg-zinc-900 text-white hover:bg-zinc-800"
          size="sm"
          onClick={resetForNewResume}
          disabled={resumeCount >= MAX_SLOTS}
        >
          <Plus className="size-4" />
          Add Resume
        </Button>
      </div>

      <div className="mx-6 mt-4 flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-600">
        <FileText className="size-4" />
        You have {resumeCount} resume{resumeCount === 1 ? "" : "s"} saved out of {MAX_SLOTS}{" "}
        available slots.
      </div>

      <div className="mx-6 mt-4 overflow-hidden rounded-xl border border-zinc-200 bg-white">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-zinc-100 bg-zinc-50 text-xs text-zinc-500">
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
                <td colSpan={5} className="px-4 py-8 text-center text-zinc-500">
                  No resumes yet.{" "}
                  <button
                    type="button"
                    className="text-zinc-900 underline"
                    onClick={resetForNewResume}
                  >
                    Upload your first resume
                  </button>
                </td>
              </tr>
            ) : (
              resumes.map((resume, index) => (
                <tr key={resume.id} className="border-b border-zinc-50 last:border-0">
                  <td className="px-4 py-4">
                    <div className="flex items-center gap-3">
                      <div className="flex size-9 items-center justify-center rounded-lg bg-zinc-100 text-sm font-bold text-zinc-800">
                        {resume.originalFilename.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <p className="font-medium text-zinc-900">{resume.originalFilename}</p>
                        <div className="mt-1 flex flex-wrap gap-1">
                          {index === 0 ? (
                            <span className="inline-flex items-center gap-0.5 rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-zinc-700">
                              <Star className="size-2.5 fill-current" />
                              Primary
                            </span>
                          ) : null}
                          <span className="rounded bg-zinc-100 px-1.5 py-0.5 text-[10px] text-zinc-600">
                            Analysis complete
                          </span>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-4 text-zinc-600">{targetTitles}</td>
                  <td className="px-4 py-4 text-zinc-500">
                    {formatRelativeTime(resume.uploadedAt)}
                  </td>
                  <td className="px-4 py-4 text-zinc-500">
                    {formatRelativeTime(resume.uploadedAt)}
                  </td>
                  <td className="px-4 py-4">
                    <button
                      type="button"
                      className="rounded p-1 text-zinc-400 hover:bg-zinc-100"
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
