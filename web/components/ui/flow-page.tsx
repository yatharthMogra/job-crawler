"use client"

import type { LucideIcon } from "lucide-react"
import type { ReactNode } from "react"
import { cn } from "@/lib/utils"

interface FlowPageProps {
  children: ReactNode
  className?: string
  centered?: boolean
}

export function FlowPage({ children, className, centered = true }: FlowPageProps) {
  return (
    <div className={cn("flow-page-bg relative min-h-screen", className)}>
      <div
        className={cn(
          "relative flex min-h-screen flex-col px-6 py-10",
          centered && "items-center",
        )}
      >
        {children}
      </div>
    </div>
  )
}

export function FlowPageHeader({
  children,
  className,
}: {
  children: ReactNode
  className?: string
}) {
  return <header className={cn("mb-2 w-full max-w-xl", className)}>{children}</header>
}

export function FlowPageContent({
  children,
  className,
  narrow,
}: {
  children: ReactNode
  className?: string
  narrow?: boolean
}) {
  return (
    <div
      className={cn(
        "flex w-full flex-1 flex-col justify-center py-6",
        narrow ? "max-w-lg" : "max-w-xl",
        className,
      )}
    >
      {children}
    </div>
  )
}

export function FlowStepBar({
  current,
  total,
  label,
}: {
  current: number
  total: number
  label?: string
}) {
  return (
    <div className="mb-8 w-full">
      <div className="flex items-center justify-between gap-3 text-xs font-medium">
        <span className="rounded-full bg-accent px-3 py-1 text-accent-foreground">
          Step {current} of {total}
          {label ? <span className="text-muted-foreground"> · {label}</span> : null}
        </span>
        <span className="text-muted-foreground">{Math.round((current / total) * 100)}%</span>
      </div>
      <div className="mt-3 flex gap-1.5">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className={cn(
              "h-1.5 flex-1 rounded-full transition-all duration-500",
              i < current ? "bg-gradient-to-r from-primary to-brand" : "bg-border",
            )}
          />
        ))}
      </div>
    </div>
  )
}

export function FlowPageHero({
  title,
  description,
  icon: Icon,
  iconTone = "brand",
  step,
  features,
}: {
  title: string
  description: string
  icon?: LucideIcon
  iconTone?: "brand" | "success" | "welcome"
  step?: { current: number; total: number; label?: string }
  features?: { icon: LucideIcon; title: string; description: string }[]
}) {
  const iconStyles = {
    welcome:
      "bg-gradient-to-br from-primary/20 via-accent to-brand-muted text-primary shadow-lg shadow-primary/15",
    brand:
      "bg-gradient-to-br from-primary/15 to-brand-muted text-primary shadow-lg shadow-primary/10",
    success:
      "bg-gradient-to-br from-add-muted to-brand-muted text-add shadow-lg shadow-add/15",
  }

  return (
    <div className="mb-8 w-full">
      {step ? <FlowStepBar current={step.current} total={step.total} label={step.label} /> : null}

      <div className="text-center">
        {Icon ? (
          <span
            className={cn(
              "mx-auto mb-5 flex size-[4.5rem] items-center justify-center rounded-2xl",
              iconStyles[iconTone],
            )}
          >
            <Icon className="size-8" strokeWidth={1.5} aria-hidden="true" />
          </span>
        ) : null}

        <h1 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
          <span className="gradient-text">{title}</span>
        </h1>
        <p className="mx-auto mt-3 max-w-md text-pretty text-base leading-relaxed text-muted-foreground">
          {description}
        </p>
      </div>

      {features && features.length > 0 ? (
        <div className="mt-8 grid gap-3 sm:grid-cols-3">
          {features.map((f) => (
            <div
              key={f.title}
              className="rounded-xl border border-border/80 bg-card/80 p-4 text-left shadow-sm backdrop-blur-sm"
            >
              <span className="flex size-9 items-center justify-center rounded-lg bg-accent text-primary">
                <f.icon className="size-4" aria-hidden="true" />
              </span>
              <p className="mt-3 text-sm font-semibold text-foreground">{f.title}</p>
              <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{f.description}</p>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  )
}

export function FlowPanel({
  children,
  className,
}: {
  children: ReactNode
  className?: string
}) {
  return (
    <div
      className={cn(
        "rounded-2xl border-2 border-border/90 bg-card p-6 shadow-lg shadow-primary/8 sm:p-8",
        className,
      )}
    >
      {children}
    </div>
  )
}
