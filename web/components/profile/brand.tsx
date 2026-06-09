import { Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

export function Brand({ className }: { className?: string }) {
  return (
    <div className={className}>
      <div className="flex items-center gap-2.5">
        <span className="flex size-8 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-brand text-primary-foreground shadow-md shadow-primary/25">
          <Sparkles className="size-4" aria-hidden="true" />
        </span>
        <span className="text-base font-semibold tracking-tight text-foreground">
          Career<span className="gradient-text">Match</span>
        </span>
      </div>
    </div>
  )
}

export function BrandMark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "flex size-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-brand text-sm font-bold text-primary-foreground shadow-md shadow-primary/20",
        className,
      )}
    >
      C
    </span>
  )
}
