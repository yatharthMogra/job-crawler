"use client"

import { useCallback, useRef, useState } from "react"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import {
  FlowPage,
  FlowPageContent,
  FlowPageHeader,
  FlowPageHero,
  FlowPanel,
} from "@/components/ui/flow-page"
import { cn } from "@/lib/utils"
import { CheckCircle2, FileText, ShieldCheck, UploadCloud, X } from "lucide-react"

interface UploadScreenProps {
  onAnalyze: (file: File) => void
  error?: string | null
}

export function UploadScreen({ onAnalyze, error: externalError }: UploadScreenProps) {
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
    <FlowPage>
      <FlowPageHeader>
        <Brand />
      </FlowPageHeader>

      <FlowPageContent>
        <FlowPageHero
          icon={UploadCloud}
          iconTone="brand"
          step={{ current: 2, total: 4, label: "Upload resume" }}
          title="Build your profile"
          description="Drop your resume and we'll extract experience, skills, and education — you'll approve every change before it's saved."
        />

        <FlowPanel>
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
              "flex cursor-pointer flex-col items-center rounded-xl border-2 border-dashed px-6 py-12 text-center transition-all",
              dragging
                ? "scale-[1.01] border-primary bg-accent/60 shadow-inner"
                : "border-border bg-gradient-to-b from-surface/80 to-accent/20 hover:border-primary/50 hover:shadow-md",
              error ? "border-remove" : file ? "border-add/60 bg-add-muted/20" : "",
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
                <span className="mb-4 flex size-14 items-center justify-center rounded-2xl bg-add-muted text-add">
                  <CheckCircle2 className="size-7" aria-hidden="true" />
                </span>
                <p className="text-base font-semibold text-foreground">{file.name}</p>
                <p className="mt-1 text-sm text-muted-foreground">{displaySize} · Ready to analyze</p>
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation()
                    setFile(null)
                  }}
                  className="mt-3 inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground"
                >
                  <X className="size-3" />
                  Choose a different file
                </button>
              </>
            ) : (
              <>
                <span className="mb-4 flex size-14 items-center justify-center rounded-2xl bg-accent text-primary">
                  <UploadCloud className="size-7" aria-hidden="true" />
                </span>
                <p className="text-base font-semibold text-foreground">Drag your resume here</p>
                <p className="mt-1 text-sm text-muted-foreground">or click to browse · PDF only · Max 5MB</p>
              </>
            )}
          </div>

          {error ? <p className="mt-3 text-sm text-remove">{error}</p> : null}

          <Button
            className="btn-brand mt-6 h-11 w-full"
            size="lg"
            disabled={!file || uploading}
            onClick={handleAnalyze}
          >
            {uploading ? (
              "Uploading..."
            ) : (
              <>
                <FileText className="size-4" aria-hidden="true" />
                Analyze my resume
              </>
            )}
          </Button>

          <div className="mt-5 flex items-start gap-2 rounded-lg border border-border/60 bg-surface/60 px-3 py-2.5">
            <ShieldCheck className="mt-0.5 size-4 shrink-0 text-brand" aria-hidden="true" />
            <p className="text-xs leading-relaxed text-muted-foreground">
              Nothing is saved until you review and approve. You&apos;ll see every addition, update,
              and removal first.
            </p>
          </div>
        </FlowPanel>
      </FlowPageContent>
    </FlowPage>
  )
}
