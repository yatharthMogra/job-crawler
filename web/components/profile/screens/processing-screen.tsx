"use client"

import { useEffect, useRef, useState } from "react"
import { PROCESSING_MESSAGES } from "@/lib/profile/profile-data"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import { FlowPage, FlowPageContent, FlowPageHeader, FlowPanel } from "@/components/ui/flow-page"
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
      <FlowPage>
        <FlowPageHeader>
          <Brand />
        </FlowPageHeader>
        <FlowPageContent narrow>
          <FlowPanel className="text-center">
            <span className="mx-auto flex size-14 items-center justify-center rounded-2xl bg-remove-muted text-remove">
              <AlertTriangle className="size-7" aria-hidden="true" />
            </span>
            <h2 className="mt-5 text-xl font-semibold text-foreground">Something went wrong</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              We couldn&apos;t finish reading your resume. Please try again.
            </p>
            <Button className="btn-brand mt-6 h-11 w-full" onClick={onRetry}>
              Try again
            </Button>
          </FlowPanel>
        </FlowPageContent>
      </FlowPage>
    )
  }

  return (
    <FlowPage>
      <FlowPageHeader>
        <Brand />
      </FlowPageHeader>
      <FlowPageContent narrow className="text-center">
        <FlowPanel>
          <div className="relative mx-auto mb-6 w-fit">
            <span className="flex size-16 items-center justify-center rounded-2xl bg-gradient-to-br from-accent to-brand-muted text-primary shadow-lg">
              <FileText className="size-8" aria-hidden="true" />
            </span>
            <span className="absolute -bottom-1 -right-1 flex size-8 items-center justify-center rounded-full bg-gradient-to-r from-primary to-brand text-primary-foreground shadow-md">
              <Loader2 className="size-4 animate-spin" aria-hidden="true" />
            </span>
          </div>

          <p className="text-lg font-semibold text-foreground" aria-live="polite">
            {PROCESSING_MESSAGES[step]}
          </p>
          <p className="mt-2 text-sm text-muted-foreground">This usually takes 10–15 seconds.</p>

          <div className="mt-8 flex items-center justify-center gap-1.5" aria-hidden="true">
            {PROCESSING_MESSAGES.map((_, i) => (
              <span
                key={i}
                className={`h-2 rounded-full transition-all duration-500 ${
                  i <= step ? "w-10 bg-gradient-to-r from-primary to-brand" : "w-5 bg-border"
                }`}
              />
            ))}
          </div>

          <p className="mt-8 truncate text-xs text-muted-foreground">{fileName}</p>
        </FlowPanel>
      </FlowPageContent>
    </FlowPage>
  )
}
