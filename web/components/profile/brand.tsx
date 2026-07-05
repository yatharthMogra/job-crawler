import { Rocket } from "lucide-react"
import { cn } from "@/lib/utils"

export function Brand({ className }: { className?: string }) {
  return (
    <div className={className}>
      <div className="flex items-center gap-2.5">
        <span className="flex size-8 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-md shadow-primary/25">
          <Rocket className="size-4" aria-hidden="true" />
        </span>
        <span className="text-base font-bold tracking-tight text-foreground">
          Job Scout
        </span>
      </div>
    </div>
  )
}

export function BrandMark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-md shadow-primary/20",
        className,
      )}
    >
      <Rocket className="size-4" aria-hidden="true" />
      <span className="sr-only">Job Scout</span>
    </span>
  )
}

export function BrandWordmark({ className, size = "default" }: { className?: string; size?: "default" | "lg" }) {
  return <JobScoutWordmark className={className} size={size} />
}

export function JobScoutWordmark({
  className,
  size = "default",
}: {
  className?: string
  size?: "default" | "lg"
}) {
  return (
    <span
      className={cn(
        "font-bold tracking-tight text-foreground",
        size === "lg" ? "text-xl" : "text-base",
        className,
      )}
    >
      Job Scout
    </span>
  )
}
