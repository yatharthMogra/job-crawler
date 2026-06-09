"use client"

import { useState, type ReactNode } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import type { NotInterestedReason, ReportIssueReason } from "@/lib/job-feedback"
import { cn } from "@/lib/utils"

const NOT_INTERESTED_OPTIONS: { id: NotInterestedReason; label: ReactNode }[] = [
  { id: "company", label: <>Not interested in this <strong>company</strong></> },
  { id: "job_title", label: <>Not interested in this <strong>job title</strong></> },
  { id: "industry", label: <>Not interested in this <strong>industry</strong></> },
  { id: "skills", label: <>I don&apos;t have the <strong>required skills</strong></> },
  { id: "location", label: <>This job is not at my <strong>target locations</strong></> },
  { id: "experience_level", label: <><strong>This doesn&apos;t match my experience level</strong></> },
  { id: "work_authorization", label: <>I don&apos;t meet the work <strong>authorization requirements</strong></> },
  { id: "other", label: <><strong>Other</strong></> },
]

const REPORT_ISSUE_OPTIONS: { id: ReportIssueReason; label: ReactNode }[] = [
  { id: "scam", label: <>I think it&apos;s a <strong>scam</strong> or a <strong>fake job</strong></> },
  { id: "discriminatory", label: <>I think it&apos;s <strong>discriminatory</strong> or <strong>offensive</strong></> },
  { id: "incorrect_info", label: <>Incorrect <strong>company info</strong> or <strong>job details</strong></> },
  { id: "no_longer_available", label: <>This job is <strong>no longer available</strong></> },
  { id: "not_in_us", label: <>This job is <strong>not in the U.S</strong></> },
]

function FeedbackOption<T extends string>({
  id,
  label,
  selected,
  onSelect,
}: {
  id: T
  label: ReactNode
  selected: T | null
  onSelect: (id: T) => void
}) {
  return (
    <label
      className={cn(
        "flex cursor-pointer items-center gap-3 rounded-lg border px-3 py-2.5 text-sm text-foreground transition-colors",
        selected === id ? "border-primary bg-accent shadow-sm" : "border-border bg-surface/80 hover:border-primary/30",
      )}
    >
      <input
        type="radio"
        name={id}
        checked={selected === id}
        onChange={() => onSelect(id)}
        className="size-4 accent-primary"
      />
      <span>{label}</span>
    </label>
  )
}

interface NotInterestedDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (reason: NotInterestedReason) => void
}

export function NotInterestedDialog({ open, onOpenChange, onSubmit }: NotInterestedDialogProps) {
  const [reason, setReason] = useState<NotInterestedReason | null>(null)

  function handleSubmit() {
    if (!reason) return
    onSubmit(reason)
    setReason(null)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md" showCloseButton>
        <DialogHeader>
          <DialogTitle className="text-base font-semibold">
            Tell us why it&apos;s not a fit to refine your matches
          </DialogTitle>
        </DialogHeader>
        <div className="flex flex-col gap-2 py-1">
          {NOT_INTERESTED_OPTIONS.map((opt) => (
            <FeedbackOption
              key={opt.id}
              id={opt.id}
              label={opt.label}
              selected={reason}
              onSelect={setReason}
            />
          ))}
        </div>
        <DialogFooter className="border-0 bg-transparent p-0 pt-2 sm:justify-between">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            className="btn-brand"
            disabled={!reason}
            onClick={handleSubmit}
          >
            Submit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

interface ReportIssueDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (reason: ReportIssueReason) => void
}

export function ReportIssueDialog({ open, onOpenChange, onSubmit }: ReportIssueDialogProps) {
  const [reason, setReason] = useState<ReportIssueReason | null>(null)

  function handleSubmit() {
    if (!reason) return
    onSubmit(reason)
    setReason(null)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md" showCloseButton>
        <DialogHeader>
          <DialogTitle className="text-base font-semibold">Tell us a little more</DialogTitle>
        </DialogHeader>
        <div className="flex flex-col gap-2 py-1">
          {REPORT_ISSUE_OPTIONS.map((opt) => (
            <FeedbackOption
              key={opt.id}
              id={opt.id}
              label={opt.label}
              selected={reason}
              onSelect={setReason}
            />
          ))}
        </div>
        <DialogFooter className="border-0 bg-transparent p-0 pt-2 sm:justify-between">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            className="btn-brand"
            disabled={!reason}
            onClick={handleSubmit}
          >
            Submit
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
