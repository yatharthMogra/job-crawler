"use client"

import { Briefcase } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface ApplyFollowUpDialogProps {
  open: boolean
  jobTitle: string
  company: string
  onConfirmApplied: () => void
  onDeclineApplied: () => void
}

export function ApplyFollowUpDialog({
  open,
  jobTitle,
  company,
  onConfirmApplied,
  onDeclineApplied,
}: ApplyFollowUpDialogProps) {
  return (
    <Dialog open={open} onOpenChange={() => undefined}>
      <DialogContent className="sm:max-w-md" showCloseButton={false}>
        <div className="flex flex-col items-center px-2 pb-2 pt-4 text-center">
          <div className="mb-4 flex size-14 items-center justify-center rounded-2xl bg-gradient-to-br from-accent to-brand-muted text-primary shadow-md">
            <Briefcase className="size-6" strokeWidth={1.5} />
          </div>
          <DialogHeader className="items-center gap-2">
            <DialogTitle className="text-xl font-semibold text-foreground">Did you apply?</DialogTitle>
            <DialogDescription className="max-w-xs text-sm leading-relaxed text-muted-foreground">
              Let us know so we can help you track your application and refine future recommendations
              for you.
            </DialogDescription>
          </DialogHeader>
          <p className="mt-2 text-xs text-muted-foreground">
            {jobTitle} at {company}
          </p>
        </div>
        <div className="flex flex-col gap-2.5 pt-2">
          <Button className="btn-brand h-11" onClick={onConfirmApplied}>
            Yes, I applied!
          </Button>
          <Button variant="outline" className="h-11" onClick={onDeclineApplied}>
            No, I didn&apos;t apply
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
