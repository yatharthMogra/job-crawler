"use client"

import { useEffect, useMemo, useState } from "react"
import { FileText, Star } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { FeedSkeleton } from "@/components/card-skeleton"
import { Button } from "@/components/ui/button"
import { ResumeUploadButton } from "@/components/resumes/resume-upload"
import { formatRelativeTime } from "@/lib/profile/map-profile"
import {
  formatResumeFileSize,
  MAX_RESUME_SLOTS,
  sortResumesByUploadedAt,
} from "@/lib/profile/resumes"
import { cn } from "@/lib/utils"

export function ResumesPage() {
  const { candidateId } = useSession()
  const { profileHome, loadProfileHome, uploadResumeInline } = useProfileFlow()
  const [loadError, setLoadError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [uploadError, setUploadError] = useState<string | null>(null)

  useEffect(() => {
    if (!candidateId) {
      setLoading(false)
      return
    }

    let cancelled = false
    setLoading(true)
    setLoadError(null)

    void loadProfileHome(candidateId)
      .catch((err) => {
        if (cancelled) return
        setLoadError(err instanceof Error ? err.message : "Could not load resumes")
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [candidateId, loadProfileHome])

  const sortedResumes = useMemo(
    () => (profileHome ? sortResumesByUploadedAt(profileHome.resumes) : []),
    [profileHome],
  )

  const resumeCount = profileHome?.resumeCount ?? 0
  const slotsRemaining = MAX_RESUME_SLOTS - resumeCount
  const canUploadMore = resumeCount < MAX_RESUME_SLOTS

  async function handleUpload(file: File) {
    setUploadError(null)
    try {
      await uploadResumeInline(file)
    } catch (err) {
      const message = err instanceof Error ? err.message : "Upload failed. Please try again."
      setUploadError(message)
      throw err
    }
  }

  if (loading && !profileHome) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-8">
        <FeedSkeleton count={2} />
      </div>
    )
  }

  if (loadError && !profileHome) {
    return (
      <div className="mx-auto max-w-3xl px-6 py-8">
        <div className="rounded-2xl border border-border/70 bg-card px-6 py-10 text-center">
          <p className="text-base font-semibold text-foreground">Could not load resumes</p>
          <p className="mt-2 text-sm text-muted-foreground">{loadError}</p>
          {candidateId ? (
            <Button
              className="mt-4"
              variant="secondary"
              onClick={() => {
                setLoading(true)
                setLoadError(null)
                void loadProfileHome(candidateId)
                  .catch((err) =>
                    setLoadError(err instanceof Error ? err.message : "Could not load resumes"),
                  )
                  .finally(() => setLoading(false))
              }}
            >
              Try again
            </Button>
          ) : null}
        </div>
      </div>
    )
  }

  if (!profileHome) {
    return null
  }

  return (
    <div className="mx-auto max-w-3xl px-6 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <p className="text-sm text-muted-foreground">
          PDF only, up to 5MB. Uploads save immediately — no need to restart onboarding.
        </p>
        <ResumeUploadButton
          className="btn-brand shrink-0"
          onUpload={handleUpload}
          disabled={!canUploadMore}
        >
          Upload resume
        </ResumeUploadButton>
      </div>

      <div className="mt-6 flex items-center gap-2 rounded-xl border border-primary/15 bg-primary/[0.04] px-4 py-3 text-sm text-foreground">
        <FileText className="size-4 shrink-0 text-primary" />
        <span>
          {resumeCount} of {MAX_RESUME_SLOTS} resume slots used
          {canUploadMore
            ? ` · ${slotsRemaining} remaining`
            : " · remove a resume to upload another"}
        </span>
      </div>

      {uploadError ? (
        <p className="mt-4 rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
          {uploadError}
        </p>
      ) : null}

      {sortedResumes.length === 0 ? (
        <div className="mt-10 rounded-2xl border border-dashed border-border/80 bg-card px-6 py-12 text-center">
          <p className="text-base font-semibold text-foreground">No resume uploaded yet</p>
          <p className="mx-auto mt-2 max-w-sm text-sm text-muted-foreground">
            Choose a PDF from your computer. It will be added to your profile without sending you
            back through setup.
          </p>
          <ResumeUploadButton
            className="btn-brand mt-6"
            onUpload={handleUpload}
            disabled={!canUploadMore}
          >
            Upload resume
          </ResumeUploadButton>
        </div>
      ) : (
        <div className="mt-8 space-y-4">
          {sortedResumes.map((resume, index) => (
            <ResumeCard key={resume.id} resume={resume} isLatest={index === 0} />
          ))}
        </div>
      )}
    </div>
  )
}

function ResumeCard({
  resume,
  isLatest,
}: {
  resume: {
    id: string
    originalFilename: string
    uploadedAt: string
    fileSizeBytes: number
  }
  isLatest: boolean
}) {
  return (
    <article
      className={cn(
        "rounded-2xl border bg-card p-5 shadow-sm transition-colors",
        isLatest ? "border-primary/25 shadow-primary/5" : "border-border/70",
      )}
    >
      <div className="flex items-start gap-4">
        <div className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-lg font-bold text-primary">
          {resume.originalFilename.charAt(0).toUpperCase()}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <p className="truncate font-semibold text-foreground">{resume.originalFilename}</p>
            {isLatest ? (
              <span className="inline-flex items-center gap-0.5 rounded-full border border-primary/20 bg-primary/10 px-2 py-0.5 text-[10px] font-semibold uppercase text-primary">
                <Star className="size-2.5 fill-current" />
                Latest
              </span>
            ) : null}
          </div>
          <p className="mt-2 text-xs text-muted-foreground">
            {formatResumeFileSize(resume.fileSizeBytes)} · uploaded{" "}
            {formatRelativeTime(resume.uploadedAt)}
          </p>
        </div>
      </div>
    </article>
  )
}
