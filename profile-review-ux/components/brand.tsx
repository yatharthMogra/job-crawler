import { Sparkles } from "lucide-react"

export function Brand({ className }: { className?: string }) {
  return (
    <div className={className}>
      <div className="flex items-center gap-2">
        <span className="flex size-7 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Sparkles className="size-4" aria-hidden="true" />
        </span>
        <span className="text-sm font-semibold tracking-tight text-foreground">
          Profile<span className="text-primary">IQ</span>
        </span>
      </div>
    </div>
  )
}
