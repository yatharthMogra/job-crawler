"use client"

import { useCallback, useRef, useState, type ReactNode } from "react"
import { FileUp, Loader2, Upload } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const MAX_BYTES = 5 * 1024 * 1024

function validateResumeFile(file: File): string | null {
  if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
    return "Only PDF files are supported."
  }
  if (file.size > MAX_BYTES) {
    return "That file is over 5MB. Please upload a smaller PDF."
  }
  return null
}

export function useResumeUpload(onUpload: (file: File) => Promise<void>) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const openPicker = useCallback(() => {
    if (!uploading) inputRef.current?.click()
  }, [uploading])

  const handleFile = useCallback(
    async (file: File | undefined) => {
      if (!file) return
      const validationError = validateResumeFile(file)
      if (validationError) {
        setError(validationError)
        return
      }
      setError(null)
      setUploading(true)
      try {
        await onUpload(file)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed. Please try again.")
      } finally {
        setUploading(false)
        if (inputRef.current) inputRef.current.value = ""
      }
    },
    [onUpload],
  )

  const input = (
    <input
      ref={inputRef}
      type="file"
      accept="application/pdf,.pdf"
      className="sr-only"
      disabled={uploading}
      onChange={(e) => void handleFile(e.target.files?.[0])}
    />
  )

  return { inputRef, input, uploading, error, openPicker, handleFile, setError }
}

export function ResumeUploadButton({
  onUpload,
  disabled,
  className,
  children,
  variant = "default",
}: {
  onUpload: (file: File) => Promise<void>
  disabled?: boolean
  className?: string
  children: React.ReactNode
  variant?: "default" | "secondary"
}) {
  const { input, uploading, openPicker } = useResumeUpload(onUpload)

  return (
    <>
      {input}
      <Button
        className={className}
        size="sm"
        variant={variant === "secondary" ? "secondary" : undefined}
        disabled={disabled || uploading}
        onClick={openPicker}
      >
        {uploading ? <Loader2 className="size-4 animate-spin" /> : <Upload className="size-4" />}
        {children}
      </Button>
    </>
  )
}

export function ResumeUploadZone({
  onUpload,
  disabled,
}: {
  onUpload: (file: File) => Promise<void>
  disabled?: boolean
}) {
  const { input, uploading, error, handleFile, openPicker } = useResumeUpload(onUpload)
  const [dragging, setDragging] = useState(false)

  return (
    <div className="mt-6">
      {input}
      <div
        role="button"
        tabIndex={disabled || uploading ? -1 : 0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault()
            openPicker()
          }
        }}
        onClick={() => {
          if (!disabled && !uploading) openPicker()
        }}
        onDragOver={(e) => {
          e.preventDefault()
          if (!disabled && !uploading) setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          if (disabled || uploading) return
          void handleFile(e.dataTransfer.files?.[0])
        }}
        className={cn(
          "rounded-2xl border border-dashed px-6 py-12 text-center transition-colors",
          dragging
            ? "border-primary bg-primary/5"
            : "border-border/80 bg-card hover:border-primary/40",
          (disabled || uploading) && "pointer-events-none opacity-60",
        )}
      >
        <div className="mx-auto flex size-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
          {uploading ? (
            <Loader2 className="size-6 animate-spin" />
          ) : (
            <FileUp className="size-6" />
          )}
        </div>
        <p className="mt-4 text-base font-semibold text-foreground">
          {uploading ? "Uploading resume…" : "Drop your resume here"}
        </p>
        <p className="mx-auto mt-2 max-w-sm text-sm text-muted-foreground">
          PDF only, up to 5MB. Your resume is added immediately — no need to leave this page.
        </p>
        {!uploading ? (
          <span className="btn-brand mt-6 inline-flex h-9 items-center justify-center gap-2 rounded-md px-4 text-sm font-medium">
            <Upload className="size-4" />
            Choose file
          </span>
        ) : null}
      </div>
      {error ? <p className="mt-3 text-sm text-destructive">{error}</p> : null}
    </div>
  )
}
