"use client"

import { useCallback, useRef, useState } from "react"
import { Brand } from "@/components/brand"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { CheckCircle2, FileText, UploadCloud, X } from "lucide-react"

interface UploadScreenProps {
  onAnalyze: (file: File) => void
  error?: string | null
  hasExistingResumes?: boolean
}

export function UploadScreen({ onAnalyze, error: externalError, hasExistingResumes }: UploadScreenProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [localError, setLocalError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  const error = externalError ?? localError

  const handleFiles = useCallback((files: FileList | null) => {
    setLocalError(null)
    const f = files?.[0]
    if (!f) return
    if (f.type !== "application/pdf" && !f.name.toLowerCase().endsWith(".pdf")) {
      setLocalError("Only PDF files are supported.")
      return
    }
    if (f.size > 5 * 1024 * 1024) {
      setLocalError("That file is over 5MB. Please upload a smaller PDF.")
      return
    }
    setFile(f)
  }, [])

  function handleAnalyze() {
    if (!file) return
    setUploading(true)
    onAnalyze(file)
  }

  const displaySize = file
    ? file.size / 1024 > 1024
      ? `${(file.size / 1024 / 1024).toFixed(1)} MB`
      : `${Math.round(file.size / 1024)} KB`
    : ""

  return (
    <main className="flex min-h-screen flex-col items-center bg-background px-6 py-10">
      <header className="w-full max-w-xl">
        <Brand />
      </header>

      <div className="flex w-full max-w-xl flex-1 flex-col justify-center py-10">
        <div className="mb-8 text-center">
          <h1 className="text-balance text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
            Build your profile
          </h1>
          <p className="mx-auto mt-3 max-w-md text-pretty leading-relaxed text-muted-foreground">
            Upload your resume and we&apos;ll extract your experience, skills, and projects. You choose
            what roles to pursue.
          </p>
        </div>

        <Card className="p-6 sm:p-8">
          <div
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
            onDragOver={(e) => {
              e.preventDefault()
              setDragging(true)
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={(e) => {
              e.preventDefault()
              setDragging(false)
              handleFiles(e.dataTransfer.files)
            }}
            onClick={() => inputRef.current?.click()}
            className={cn(
              "flex cursor-pointer flex-col items-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors",
              dragging ? "border-primary bg-accent/50" : "border-border hover:border-primary/40",
              error ? "border-remove" : file ? "border-add/50" : "",
            )}
          >
            <input
              ref={inputRef}
              type="file"
              accept="application/pdf,.pdf"
              className="hidden"
              onChange={(e) => handleFiles(e.target.files)}
            />
            {file ? (
              <>
                <CheckCircle2 className="mb-3 size-10 text-add" aria-hidden="true" />
                <p className="font-medium text-foreground">{file.name}</p>
                <p className="mt-1 text-sm text-muted-foreground">{displaySize}</p>
              </>
            ) : (
              <>
                <UploadCloud className="mb-3 size-10 text-muted-foreground" aria-hidden="true" />
                <p className="font-medium text-foreground">Drag your resume here or click to browse</p>
                <p className="mt-2 text-sm text-muted-foreground">PDF only · Max 5MB</p>
              </>
            )}
          </div>

          {error ? <p className="mt-3 text-sm text-remove">{error}</p> : null}

          <Button
            className="mt-6 w-full"
            size="lg"
            disabled={!file || uploading}
            onClick={handleAnalyze}
          >
            {uploading ? (
              "Uploading..."
            ) : (
              <>
                <FileText className="size-4" aria-hidden="true" />
                {hasExistingResumes ? "Add another resume" : "Analyze resume"}
              </>
            )}
          </Button>

          <p className="mt-4 text-center text-xs leading-relaxed text-muted-foreground">
            {hasExistingResumes
              ? "Each resume is added to your library. Label them on your profile to keep track."
              : "We'll show you what we found before saving anything. Target roles are always your choice."}
          </p>
        </Card>
      </div>
    </main>
  )
}
