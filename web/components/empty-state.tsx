import Link from "next/link"
import type { LucideIcon } from "lucide-react"

interface EmptyStateProps {
  icon: LucideIcon
  title: string
  description: string
  ctaLabel?: string
  ctaHref?: string
}

export function EmptyState({ icon: Icon, title, description, ctaLabel, ctaHref }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center px-6 py-24 text-center">
      <div className="mb-4 flex size-12 items-center justify-center rounded-2xl bg-gradient-to-br from-accent to-brand-muted text-primary shadow-sm">
        <Icon className="size-6" />
      </div>
      <h3 className="text-sm font-semibold text-foreground">{title}</h3>
      <p className="mt-1 max-w-xs text-pretty text-sm text-muted-foreground">{description}</p>
      {ctaLabel && ctaHref && (
        <Link href={ctaHref} className="btn-brand mt-4 inline-flex h-9 items-center rounded-lg px-4 text-xs font-medium">
          {ctaLabel}
        </Link>
      )}
    </div>
  )
}
