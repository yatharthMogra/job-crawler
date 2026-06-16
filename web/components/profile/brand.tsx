import { Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

export function Brand({ className }: { className?: string }) {
  return (
    <div className={className}>
      <div className="flex items-center gap-2.5">
        <span className="flex size-8 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-md shadow-primary/25">
          <Sparkles className="size-4" aria-hidden="true" />
        </span>
        <span className="text-base font-bold tracking-tight text-foreground">
          Career<span className="text-primary">Match</span>
        </span>
      </div>
    </div>
  )
}

export function BrandMark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "flex size-9 items-center justify-center rounded-xl bg-primary text-sm font-bold text-primary-foreground shadow-md shadow-primary/20",
        className,
      )}
    >
      C
    </span>
  )
}

export function BrandWordmark({ className, size = "default" }: { className?: string; size?: "default" | "lg" }) {
  return (
    <span
      className={cn(
        "font-bold tracking-tight text-foreground",
        size === "lg" ? "text-xl" : "text-base",
        className,
      )}
    >
      Career<span className="text-primary">Match</span>
    </span>
  )
}
