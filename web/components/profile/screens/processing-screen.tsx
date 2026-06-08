"use client"

import { useEffect, useRef, useState } from "react"
import { PROCESSING_MESSAGES } from "@/lib/profile/profile-data"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { AlertTriangle, FileText, Loader2 } from "lucide-react"

interface ProcessingScreenProps {
  fileName: string
  onProcess: () => Promise<void>
  onComplete: () => void
  onRetry: () => void
}

export function ProcessingScreen({ fileName, onProcess, onComplete, onRetry }: ProcessingScreenProps) {
  const [step, setStep] = useState(0)
  const [failed, setFailed] = useState(false)
  const onProcessRef = useRef(onProcess)
  const onCompleteRef = useRef(onComplete)

  onProcessRef.current = onProcess
  onCompleteRef.current = onComplete

  useEffect(() => {
    let cancelled = false
    let interval: number | undefined

    async function run() {
      interval = window.setInterval(() => {
        setStep((s) => Math.min(s + 1, PROCESSING_MESSAGES.length - 1))
      }, 1500)

      try {
        await onProcessRef.current()
        if (!cancelled) onCompleteRef.current()
      } catch {
        if (!cancelled) setFailed(true)
      } finally {
        if (interval) window.clearInterval(interval)
      }
    }

    run()
    return () => {
      cancelled = true
      if (interval) window.clearInterval(interval)
    }
  }, [])

  if (failed) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background px-6">
        <Card className="w-full max-w-sm p-8 text-center">
          <span className="mx-auto flex size-12 items-center justify-center rounded-full bg-remove-muted text-remove">
            <AlertTriangle className="size-6" aria-hidden="true" />
          </span>
          <h2 className="mt-4 text-lg font-semibold text-foreground">Something went wrong</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            We couldn&apos;t finish reading your resume. Please try again.
          </p>
          <Button className="mt-6 w-full" onClick={onRetry}>
            Try again
          </Button>
        </Card>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-background px-6 text-center">
      <div className="relative mb-8">
        <span className="flex size-16 items-center justify-center rounded-2xl bg-card shadow-sm">
          <FileText className="size-7 text-primary" aria-hidden="true" />
        </span>
        <span className="absolute -bottom-1 -right-1 flex size-7 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <Loader2 className="size-4 animate-spin" aria-hidden="true" />
        </span>
      </div>

      <p className="text-lg font-medium text-foreground" aria-live="polite">
        {PROCESSING_MESSAGES[step]}
      </p>
      <p className="mt-2 text-sm text-muted-foreground">This usually takes 10–15 seconds.</p>

      <div className="mt-6 flex items-center gap-1.5" aria-hidden="true">
        {PROCESSING_MESSAGES.map((_, i) => (
          <span
            key={i}
            className={`h-1.5 rounded-full transition-all duration-500 ${
              i <= step ? "w-8 bg-primary" : "w-4 bg-border"
            }`}
          />
        ))}
      </div>

      <p className="mt-8 max-w-xs truncate text-xs text-muted-foreground">{fileName}</p>
    </main>
  )
}
