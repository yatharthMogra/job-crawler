"use client"

import { useEffect, useMemo, useState } from "react"
import { Building2, FileText, Star } from "lucide-react"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { FeedSkeleton } from "@/components/card-skeleton"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ResumeUploadButton, ResumeUploadZone } from "@/components/resumes/resume-upload"
import { formatRelativeTime } from "@/lib/profile/map-profile"
import {
  formatResumeFileSize,
  MAX_RESUME_SLOTS,
  partitionResumes,
  sortResumesByUploadedAt,
} from "@/lib/profile/resumes"
import { cn } from "@/lib/utils"

export function ResumesPage() {
  const { candidateId } = useSession()
  const { profileHome, loadProfileHome, uploadResumeInline, handleResumeLabelSave } =
    useProfileFlow()
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

  const { general, company } = useMemo(
    () => partitionResumes(sortedResumes),
    [sortedResumes],
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

  const targetTitles = profileHome?.primaryRoles.join(", ") || "—"

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
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Resumes</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Upload a general resume for matching, or tailor versions for specific companies.
          </p>
        </div>
        <ResumeUploadButton
          className="btn-brand shrink-0"
          onUpload={handleUpload}
          disabled={!canUploadMore}
        >
          Add resume
        </ResumeUploadButton>
      </div>

      <div className="mt-6 flex items-center gap-2 rounded-xl border border-primary/15 bg-primary/[0.04] px-4 py-3 text-sm text-foreground">
        <FileText className="size-4 shrink-0 text-primary" />
        <span>
          {resumeCount} of {MAX_RESUME_SLOTS} resume slots used
          {canUploadMore
            ? ` · ${slotsRemaining} remaining`
            : " · remove or replace a resume to add another"}
        </span>
      </div>

      {uploadError ? (
        <p className="mt-4 rounded-lg border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
          {uploadError}
        </p>
      ) : null}

      {sortedResumes.length === 0 ? (
        <div>
          <ResumeUploadZone onUpload={handleUpload} disabled={!canUploadMore} />
          <p className="mt-4 text-center text-sm text-muted-foreground">
            Add company-specific versions later by labeling them &quot;for Google&quot;, &quot;for
            Meta&quot;, etc.
          </p>
        </div>
      ) : (
        <div className="mt-8 space-y-10">
          <ResumeSection
            title="General resumes"
            description="Used for profile extraction and broad job matching."
            resumes={general}
            targetTitles={targetTitles}
            onSaveLabel={handleResumeLabelSave}
            labelPlaceholder="e.g. Backend-focused version"
            emptyMessage="No general resumes yet."
          />

          <ResumeSection
            title="Company-specific resumes"
            description='Label resumes as "for [Company]" to track tailored versions per employer.'
            icon={Building2}
            resumes={company}
            targetTitles={targetTitles}
            onSaveLabel={handleResumeLabelSave}
            labelPlaceholder='e.g. for Google, for Stripe'
            emptyMessage="No company-specific resumes yet. Add a label like “for Google” on any resume."
          />
        </div>
      )}

      {sortedResumes.length > 0 && canUploadMore ? (
        <ResumeUploadButton
          className="mt-6"
          variant="secondary"
          onUpload={handleUpload}
        >
          Upload another resume
        </ResumeUploadButton>
      ) : null}
    </div>
  )
}

function ResumeSection({
  title,
  description,
  resumes,
  targetTitles,
  onSaveLabel,
  labelPlaceholder,
  emptyMessage,
  icon: Icon = FileText,
}: {
  title: string
  description: string
  resumes: {
    id: string
    originalFilename: string
    displayLabel: string | null
    uploadedAt: string
    fileSizeBytes: number
  }[]
  targetTitles: string
  onSaveLabel: (resumeId: string, label: string | null) => Promise<void>
  labelPlaceholder: string
  emptyMessage: string
  icon?: typeof FileText
}) {
  return (
    <section>
      <div className="mb-4 flex items-start gap-3">
        <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <Icon className="size-4" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-foreground">{title}</h2>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      </div>

      {resumes.length === 0 ? (
        <p className="rounded-xl border border-dashed border-border/70 px-4 py-6 text-center text-sm text-muted-foreground">
          {emptyMessage}
        </p>
      ) : (
        <div className="space-y-4">
          {resumes.map((resume, index) => (
            <ResumeCard
              key={resume.id}
              resume={resume}
              isPrimary={index === 0}
              targetTitles={targetTitles}
              onSaveLabel={onSaveLabel}
              labelPlaceholder={labelPlaceholder}
            />
          ))}
        </div>
      )}
    </section>
  )
}

function ResumeCard({
  resume,
  isPrimary,
  targetTitles,
  onSaveLabel,
  labelPlaceholder,
}: {
  resume: {
    id: string
    originalFilename: string
    displayLabel: string | null
    uploadedAt: string
    fileSizeBytes: number
  }
  isPrimary: boolean
  targetTitles: string
  onSaveLabel: (resumeId: string, label: string | null) => Promise<void>
  labelPlaceholder: string
}) {
  const [label, setLabel] = useState(resume.displayLabel ?? "")
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    setLabel(resume.displayLabel ?? "")
  }, [resume.displayLabel, resume.id])

  async function handleSaveLabel() {
    setSaving(true)
    try {
      const trimmed = label.trim()
      await onSaveLabel(resume.id, trimmed || null)
      setSaved(true)
      window.setTimeout(() => setSaved(false), 2000)
    } finally {
      setSaving(false)
    }
  }

  const labelChanged = label.trim() !== (resume.displayLabel ?? "")

  return (
    <article
      className={cn(
        "rounded-2xl border bg-card p-5 shadow-sm transition-colors",
        isPrimary ? "border-primary/25 shadow-primary/5" : "border-border/70",
      )}
    >
      <div className="flex items-start gap-4">
        <div className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-lg font-bold text-primary">
          {resume.originalFilename.charAt(0).toUpperCase()}
        </div>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <p className="truncate font-semibold text-foreground">{resume.originalFilename}</p>
            {isPrimary ? (
              <span className="inline-flex items-center gap-0.5 rounded-full border border-primary/20 bg-primary/10 px-2 py-0.5 text-[10px] font-semibold uppercase text-primary">
                <Star className="size-2.5 fill-current" />
                Latest
              </span>
            ) : null}
          </div>
          <p className="mt-0.5 truncate text-sm text-muted-foreground">
            {resume.displayLabel ?? targetTitles}
          </p>
          <p className="mt-2 text-xs text-muted-foreground">
            {formatResumeFileSize(resume.fileSizeBytes)} · uploaded{" "}
            {formatRelativeTime(resume.uploadedAt)}
          </p>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap items-end gap-2 border-t border-border/60 pt-4">
        <label className="min-w-0 flex-1">
          <span className="mb-1 block text-xs font-medium text-muted-foreground">Label</span>
          <Input
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            placeholder={labelPlaceholder}
            className="text-sm"
          />
        </label>
        <Button
          size="sm"
          variant="secondary"
          disabled={saving || !labelChanged}
          onClick={() => void handleSaveLabel()}
        >
          {saving ? "Saving..." : saved ? "Saved" : "Save label"}
        </Button>
      </div>
    </article>
  )
}
