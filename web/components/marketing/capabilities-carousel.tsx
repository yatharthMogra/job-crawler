"use client"

import { useCallback, useEffect, useState } from "react"
import { BarChart3, ChevronLeft, ChevronRight, FileSearch, Globe } from "lucide-react"
import type { LucideIcon } from "lucide-react"
import { ScrollReveal } from "@/components/marketing/scroll-reveal"
import { cn } from "@/lib/utils"

interface Capability {
  id: string
  icon: LucideIcon
  title: string
  description: string
  tag: string
  metric: string
}

const CAPABILITIES: Capability[] = [
  {
    id: "match",
    icon: FileSearch,
    title: "Match Analysis",
    description:
      "Deep semantic vetting that correlates your career trajectory with board-level growth mandates.",
    tag: "LIVE INSIGHT",
    metric: "94% Accuracy",
  },
  {
    id: "salary",
    icon: BarChart3,
    title: "Salary Intelligence",
    description:
      "Real-time benchmarks pulled from private closed-offer networks. Never enter a negotiation blind.",
    tag: "MARKET DATA",
    metric: "+18% Delta",
  },
  {
    id: "sponsorship",
    icon: Globe,
    title: "Sponsorship Insights",
    description:
      "Global mobility filters that prioritize H1-B and O-1 friendly roles before you even apply.",
    tag: "NOTIFICATION",
    metric: "H1-B Enabled",
  },
]

function CapabilityCard({ cap }: { cap: Capability }) {
  const Icon = cap.icon
  return (
    <div className="h-full rounded-2xl border border-border/80 bg-card p-8 shadow-lg shadow-primary/5 transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-primary/10">
      <div className="flex size-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
        <Icon className="size-6" />
      </div>
      <h3 className="mt-6 text-xl font-semibold text-foreground">{cap.title}</h3>
      <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{cap.description}</p>
      <div className="mt-8 flex items-center justify-between border-t border-border/60 pt-5">
        <span className="text-[10px] font-bold tracking-widest text-muted-foreground">{cap.tag}</span>
        <span className="text-sm font-semibold text-primary">{cap.metric}</span>
      </div>
    </div>
  )
}

export function CapabilitiesCarousel() {
  const [index, setIndex] = useState(0)
  const [paused, setPaused] = useState(false)

  const next = useCallback(() => {
    setIndex((i) => (i + 1) % CAPABILITIES.length)
  }, [])

  const prev = useCallback(() => {
    setIndex((i) => (i - 1 + CAPABILITIES.length) % CAPABILITIES.length)
  }, [])

  useEffect(() => {
    if (paused) return
    const timer = setInterval(next, 5000)
    return () => clearInterval(timer)
  }, [next, paused])

  return (
    <div onMouseEnter={() => setPaused(true)} onMouseLeave={() => setPaused(false)}>
      <ScrollReveal>
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Platform Capabilities
          </h2>
          <p className="mx-auto mt-3 max-w-xl text-muted-foreground">
            Precision tools architected for the executive landscape.
          </p>
        </div>
      </ScrollReveal>

      {/* Desktop grid */}
      <div className="mt-12 hidden gap-6 lg:grid lg:grid-cols-3">
        {CAPABILITIES.map((cap, i) => (
          <ScrollReveal key={cap.id} delay={i * 100}>
            <CapabilityCard cap={cap} />
          </ScrollReveal>
        ))}
      </div>

      {/* Mobile carousel */}
      <div className="mt-12 lg:hidden">
        <div className="relative overflow-hidden">
          <div
            className="flex transition-transform duration-500 ease-out"
            style={{ transform: `translateX(-${index * 100}%)` }}
          >
            {CAPABILITIES.map((cap) => (
              <div key={cap.id} className="w-full shrink-0 px-1">
                <CapabilityCard cap={cap} />
              </div>
            ))}
          </div>
        </div>

        <div className="mt-8 flex items-center justify-center gap-3">
          <button
            type="button"
            onClick={prev}
            className="flex size-10 items-center justify-center rounded-full border border-border bg-card text-muted-foreground transition-colors hover:border-primary/30 hover:text-primary"
            aria-label="Previous capability"
          >
            <ChevronLeft className="size-5" />
          </button>
          <div className="flex gap-2">
            {CAPABILITIES.map((cap, i) => (
              <button
                key={cap.id}
                type="button"
                onClick={() => setIndex(i)}
                className={cn(
                  "h-2 rounded-full transition-all duration-300",
                  i === index ? "w-6 bg-primary" : "w-2 bg-border",
                )}
                aria-label={`Go to ${cap.title}`}
              />
            ))}
          </div>
          <button
            type="button"
            onClick={next}
            className="flex size-10 items-center justify-center rounded-full border border-border bg-card text-muted-foreground transition-colors hover:border-primary/30 hover:text-primary"
            aria-label="Next capability"
          >
            <ChevronRight className="size-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
