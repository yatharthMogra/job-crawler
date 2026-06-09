"use client"

import { useCallback, useEffect, useRef, useState } from "react"
import { usePathname } from "next/navigation"
import { useJobs } from "@/components/jobs-provider"
import { ApplyFollowUpDialog } from "@/components/jobs/apply-follow-up-dialog"
import type { PendingApply } from "@/lib/job-storage"

const RECOMMENDED_PATHS = new Set(["/jobs/recommended", "/recommended"])

function isRecommended(pathname: string) {
  return RECOMMENDED_PATHS.has(pathname)
}

export function ApplyFollowUpMount() {
  const pathname = usePathname()
  const { pendingApply, resolvePendingApply } = useJobs()
  const [open, setOpen] = useState(false)
  const [shown, setShown] = useState<PendingApply | null>(null)
  const tabWasHiddenRef = useRef(false)
  const prevPathRef = useRef(pathname)

  const onRecommended = isRecommended(pathname)

  const openDialog = useCallback(() => {
    if (!pendingApply || open) return
    setShown(pendingApply)
    setOpen(true)
  }, [pendingApply, open])

  useEffect(() => {
    function markLeft() {
      if (pendingApply) tabWasHiddenRef.current = true
    }

    function tryOpenOnReturn() {
      if (tabWasHiddenRef.current && pendingApply && onRecommended) {
        tabWasHiddenRef.current = false
        openDialog()
      }
    }

    function onVisibility() {
      if (document.visibilityState === "hidden") {
        markLeft()
        return
      }
      if (document.visibilityState === "visible") tryOpenOnReturn()
    }

    document.addEventListener("visibilitychange", onVisibility)
    window.addEventListener("blur", markLeft)
    window.addEventListener("focus", tryOpenOnReturn)
    return () => {
      document.removeEventListener("visibilitychange", onVisibility)
      window.removeEventListener("blur", markLeft)
      window.removeEventListener("focus", tryOpenOnReturn)
    }
  }, [pendingApply, onRecommended, openDialog])

  useEffect(() => {
    const wasRecommended = isRecommended(prevPathRef.current)
    const nowRecommended = isRecommended(pathname)
    if (!wasRecommended && nowRecommended && pendingApply) {
      openDialog()
    }
    prevPathRef.current = pathname
  }, [pathname, pendingApply, openDialog])

  function handleConfirm() {
    resolvePendingApply(true)
    setOpen(false)
    setShown(null)
  }

  function handleDecline() {
    resolvePendingApply(false)
    setOpen(false)
    setShown(null)
  }

  if (!shown) return null

  return (
    <ApplyFollowUpDialog
      open={open}
      jobTitle={shown.jobTitle}
      company={shown.company}
      onConfirmApplied={handleConfirm}
      onDeclineApplied={handleDecline}
    />
  )
}
