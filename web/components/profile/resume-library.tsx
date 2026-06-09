"use client"

import { useState } from "react"
import type { ProfileResumeItem } from "@/lib/profile/map-profile"
import { formatRelativeTime } from "@/lib/profile/map-profile"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { FileText, Plus, Upload } from "lucide-react"

interface ResumeLibraryProps {
  resumes: ProfileResumeItem[]
  onUploadNew: () => void
  onSaveLabel?: (resumeId: string, label: string | null) => Promise<void>
  readOnly?: boolean
}

export function ResumeLibrary({
  resumes,
  onUploadNew,
  onSaveLabel,
  readOnly = false,
}: ResumeLibraryProps) {
  if (resumes.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-border bg-card p-6 text-center">
        <FileText className="mx-auto size-8 text-muted-foreground" aria-hidden="true" />
        <p className="mt-3 text-sm font-medium text-foreground">No resumes yet</p>
        <p className="mt-1 text-sm text-muted-foreground">
          Upload a resume to build your profile. You can add more later and label each one on this
          page.
        </p>
        <Button size="sm" className="mt-4" onClick={onUploadNew}>
          <Upload className="size-4" aria-hidden="true" />
          Upload resume
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {resumes.map((resume) => (
        <ResumeRow
          key={resume.id}
          resume={resume}
          onSaveLabel={onSaveLabel}
          readOnly={readOnly}
        />
      ))}
      <Button variant="secondary" size="sm" onClick={onUploadNew}>
        <Plus className="size-4" aria-hidden="true" />
        Upload another resume
      </Button>
    </div>
  )
}

function ResumeRow({
  resume,
  onSaveLabel,
  readOnly,
}: {
  resume: ProfileResumeItem
  onSaveLabel?: (resumeId: string, label: string | null) => Promise<void>
  readOnly: boolean
}) {
  const [label, setLabel] = useState(resume.displayLabel ?? "")
  const [saving, setSaving] = useState(false)
  const [saved, setSaved] = useState(false)

  const displaySize =
    resume.fileSizeBytes / 1024 > 1024
      ? `${(resume.fileSizeBytes / 1024 / 1024).toFixed(1)} MB`
      : `${Math.round(resume.fileSizeBytes / 1024)} KB`

  async function handleSave() {
    if (!onSaveLabel || readOnly) return
    setSaving(true)
    try {
      const trimmed = label.trim()
      await onSaveLabel(resume.id, trimmed || null)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } finally {
      setSaving(false)
    }
  }

  return (
    <Card className="p-4">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-foreground">{resume.originalFilename}</p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {displaySize} · uploaded {formatRelativeTime(resume.uploadedAt)}
          </p>
        </div>
      </div>
      {!readOnly && onSaveLabel ? (
        <div className="mt-3 flex flex-wrap items-end gap-2">
          <label className="min-w-0 flex-1">
            <span className="mb-1 block text-xs font-medium text-muted-foreground">Label</span>
            <Input
              value={label}
              onChange={(e) => setLabel(e.target.value)}
              placeholder="e.g. Software Engineering focused"
              className="text-sm"
            />
          </label>
          <Button
            size="sm"
            variant="secondary"
            disabled={saving || label.trim() === (resume.displayLabel ?? "")}
            onClick={() => void handleSave()}
          >
            {saving ? "Saving..." : saved ? "Saved" : "Save label"}
          </Button>
        </div>
      ) : resume.displayLabel ? (
        <p className="mt-2 text-sm text-muted-foreground">
          <span className="font-medium text-foreground">{resume.displayLabel}</span>
        </p>
      ) : null}
    </Card>
  )
}
