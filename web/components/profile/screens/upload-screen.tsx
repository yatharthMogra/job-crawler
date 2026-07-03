"use client"

import { useCallback, useEffect, useRef, useState } from "react"
import Link from "next/link"
import { Brand } from "@/components/profile/brand"
import { cn } from "@/lib/utils"
import {
  CheckCircle2,
  ChevronRight,
  FileUp,
  Info,
  ShieldCheck,
  Sparkles,
  X,
  Zap,
} from "lucide-react"

interface UploadScreenProps {
  onAnalyze: (file: File) => void
  error?: string | null
}

const MAX_BYTES = 5 * 1024 * 1024

function SkillMappingCard() {
  return (
    <div className="animate-float absolute -right-4 -top-6 hidden w-44 rounded-xl border border-border/60 bg-card p-3 shadow-lg shadow-primary/10 lg:block">
      <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
        Skill Mapping
      </p>
      <div className="mt-3 space-y-2">
        {[92, 78, 64].map((w, i) => (
          <div key={i} className="h-1.5 overflow-hidden rounded-full bg-muted">
            <div
              className="h-full rounded-full bg-primary transition-all duration-1000 ease-out"
              style={{ width: `${w}%`, transitionDelay: `${i * 200}ms` }}
            />
          </div>
        ))}
      </div>
    </div>
  )
}

function SecureParsingCard() {
  return (
    <div className="animate-float-delayed absolute -bottom-5 -left-6 hidden w-48 rounded-xl border border-border/60 bg-card p-3 shadow-lg shadow-primary/10 lg:block">
      <div className="flex items-start gap-2">
        <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <ShieldCheck className="size-4" />
        </span>
        <div>
          <p className="text-xs font-semibold text-foreground">Secure Parsing</p>
          <p className="mt-0.5 text-[9px] font-bold uppercase tracking-wider text-muted-foreground">
            Enterprise-grade encryption
          </p>
        </div>
      </div>
    </div>
  )
}

export function UploadScreen({ onAnalyze, error: externalError }: UploadScreenProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [localError, setLocalError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const error = externalError ?? localError

  useEffect(() => {
    const timer = setTimeout(() => setProgress(25), 400)
    return () => clearTimeout(timer)
  }, [])

  const handleFiles = useCallback((files: FileList | null) => {
    setLocalError(null)
    const f = files?.[0]
    if (!f) return
    if (f.type !== "application/pdf" && !f.name.toLowerCase().endsWith(".pdf")) {
      setLocalError("Only PDF files are supported.")
      return
    }
    if (f.size > MAX_BYTES) {
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
    <div className="landing-hero-bg relative flex min-h-screen flex-col">
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-32 top-1/4 size-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute -right-24 bottom-1/4 size-80 rounded-full bg-primary/8 blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-5">
        <Link href="/">
          <Brand />
        </Link>
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium text-muted-foreground">Step 1 of 4</span>
          <div className="h-1.5 w-24 overflow-hidden rounded-full bg-muted">
            <div
              className="h-full rounded-full bg-primary transition-all duration-700 ease-out"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      </header>

      <main className="relative z-10 mx-auto flex w-full max-w-2xl flex-1 flex-col px-6 pb-8 pt-4">
        <div className="animate-fade-in-up text-center opacity-0" style={{ animationFillMode: "forwards" }}>
          <span className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-primary">
            <span className="relative flex size-1.5">
              <span className="absolute inline-flex size-full animate-ping rounded-full bg-primary opacity-60" />
              <span className="relative inline-flex size-1.5 rounded-full bg-primary" />
            </span>
            Neural Engine Active
          </span>
          <h1 className="mt-6 text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            Initialize Your{" "}
            <span className="script-accent text-5xl font-semibold italic sm:text-6xl">Profile</span>
          </h1>
          <p className="mx-auto mt-4 max-w-lg text-sm leading-relaxed text-muted-foreground sm:text-base">
            Drop your resume to let our neural engine map your career trajectory and extract
            high-value insights.
          </p>
        </div>

        <div
          className="animate-fade-in-up relative mx-auto mt-10 w-full opacity-0"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          <SkillMappingCard />
          <SecureParsingCard />

          <div className="relative rounded-2xl border border-border/80 bg-card p-6 shadow-xl shadow-primary/5 sm:p-8">
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
                "group relative flex cursor-pointer flex-col items-center rounded-xl border-2 border-dashed px-6 py-14 text-center transition-all duration-300",
                dragging
                  ? "scale-[1.01] border-primary bg-primary/5 shadow-inner shadow-primary/10"
                  : "border-border/80 bg-gradient-to-b from-surface/50 to-background hover:border-primary/40 hover:shadow-md hover:shadow-primary/5",
                error && "border-remove/50",
                file && "border-primary/30 bg-primary/5",
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
                  <span className="mb-4 flex size-16 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-600 ring-4 ring-emerald-500/10">
                    <CheckCircle2 className="size-8" />
                  </span>
                  <p className="text-base font-semibold text-foreground">{file.name}</p>
                  <p className="mt-1 text-sm text-muted-foreground">{displaySize} · Ready to analyze</p>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation()
                      setFile(null)
                    }}
                    className="mt-3 inline-flex items-center gap-1 text-xs text-muted-foreground transition-colors hover:text-foreground"
                  >
                    <X className="size-3" />
                    Choose a different file
                  </button>
                </>
              ) : (
                <>
                  <span className="relative mb-5 flex size-16 items-center justify-center">
                    <span className="absolute inset-0 rounded-2xl bg-primary/20 blur-xl transition-all duration-300 group-hover:bg-primary/30" />
                    <span className="relative flex size-16 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-lg shadow-primary/30 transition-transform duration-300 group-hover:scale-105">
                      <FileUp className="size-7" />
                    </span>
                  </span>
                  <p className="text-base text-foreground">
                    Drag your resume here or{" "}
                    <span className="font-semibold text-primary">click to browse</span>
                  </p>
                  <p className="mt-2 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
                    PDF only · Max 5MB
                  </p>
                </>
              )}
            </div>

            {error ? <p className="mt-3 text-center text-sm text-remove">{error}</p> : null}

            <div className="mt-5 flex items-center justify-between rounded-lg border border-border/60 bg-surface/60 px-4 py-2.5 text-xs">
              <span className="flex items-center gap-2 font-medium text-foreground">
                <span className="relative flex size-2">
                  <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                  <span className="relative inline-flex size-2 rounded-full bg-emerald-500" />
                </span>
                AI Engine Ready
              </span>
              <span className="flex items-center gap-1 font-semibold text-primary">
                <Zap className="size-3.5" />
                98% Accuracy
              </span>
            </div>

            <button
              type="button"
              disabled={!file || uploading}
              onClick={handleAnalyze}
              className="btn-brand mt-5 flex h-12 w-full items-center justify-center gap-2 rounded-xl text-sm font-bold uppercase tracking-wide transition-all hover:gap-3 disabled:opacity-50"
            >
              {uploading ? (
                <>
                  <Sparkles className="size-4 animate-pulse" />
                  Analyzing...
                </>
              ) : (
                <>
                  Analyze with Neural Engine
                  <ChevronRight className="size-4" />
                </>
              )}
            </button>

            <div className="mt-4 flex items-start justify-center gap-2 text-center">
              <Info className="mt-0.5 size-3.5 shrink-0 text-muted-foreground" />
              <p className="text-xs leading-relaxed text-muted-foreground">
                Nothing is saved until you review and approve every extracted data point.
              </p>
            </div>
          </div>
        </div>
      </main>

      <footer className="relative z-10 flex flex-col items-center justify-between gap-3 border-t border-border/40 px-6 py-5 text-[10px] text-muted-foreground sm:flex-row">
        <p>© {new Date().getFullYear()} Job Scout · Data Privacy Architecture v2.4</p>
        <div className="flex gap-4">
          <Link href="#" className="transition-colors hover:text-foreground">
            Privacy Policy
          </Link>
          <Link href="#" className="transition-colors hover:text-foreground">
            Security Audit
          </Link>
          <Link href="#" className="transition-colors hover:text-foreground">
            Support
          </Link>
        </div>
      </footer>
    </div>
  )
}
