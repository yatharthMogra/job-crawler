"use client"

import Link from "next/link"
import { BadgeCheck, MapPin, Search, ShieldCheck } from "lucide-react"
import { AgentTerminal } from "@/components/marketing/agent-terminal"
import { CapabilitiesCarousel } from "@/components/marketing/capabilities-carousel"
import { InfiniteMarquee } from "@/components/marketing/infinite-marquee"
import { LandingFooter } from "@/components/marketing/landing-footer"
import { ScrollReveal } from "@/components/marketing/scroll-reveal"
import { TestimonialsCarousel } from "@/components/marketing/testimonials-carousel"
import { MarketingNav } from "@/components/layout/marketing-nav"
import { Input } from "@/components/ui/input"
import { useCountUp } from "@/lib/hooks/use-count-up"
import { useInView } from "@/lib/hooks/use-in-view"

const COMPANY_LOGOS = [
  { id: "neuralink", label: "Neuralink" },
  { id: "openai", label: "OpenAI", badge: "H1-B Roles" },
  { id: "wayne", label: "Wayne Tech" },
  { id: "stark", label: "Stark Corp" },
  { id: "oscorp", label: "Oscorp" },
  { id: "anduril", label: "Anduril" },
]

function AgentStats() {
  const { ref, inView } = useInView<HTMLDivElement>()
  const roles = useCountUp(1200, inView)
  const latency = useCountUp(14, inView)

  return (
    <div ref={ref} className="mt-10 flex flex-wrap gap-8">
      <div>
        <p className="text-2xl font-bold text-foreground">{roles}+</p>
        <p className="text-sm text-muted-foreground">Hidden Roles Analyzed</p>
      </div>
      <div>
        <p className="text-2xl font-bold text-foreground">{latency}ms</p>
        <p className="text-sm text-muted-foreground">Matching Latency</p>
      </div>
    </div>
  )
}

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <MarketingNav />

      {/* Hero */}
      <section className="landing-hero-bg relative overflow-hidden pb-20 pt-12 sm:pt-16">
        <div className="mx-auto max-w-5xl px-6">
          <div
            className="animate-fade-in-up relative min-h-[220px] py-4 opacity-0 lg:min-h-[260px] lg:py-8"
            style={{ animationDelay: "0.1s", animationFillMode: "forwards" }}
          >
            {/* Side floats — only when there is room; never over the headline */}
            <span className="animate-float pointer-events-none absolute left-0 top-[42%] z-0 hidden -translate-y-1/2 rounded-full border border-emerald-200/80 bg-card/95 px-3 py-1.5 text-[11px] font-semibold text-emerald-700 shadow-md backdrop-blur-sm lg:inline-flex lg:items-center lg:gap-1.5">
              <BadgeCheck className="size-3.5 shrink-0" />
              98% Skill Overlap
            </span>
            <span className="animate-float-delayed pointer-events-none absolute right-0 top-[28%] z-0 hidden rounded-full border border-primary/20 bg-card/95 px-3 py-1.5 text-[11px] font-semibold text-primary shadow-md backdrop-blur-sm lg:inline-flex lg:items-center lg:gap-1.5">
              <ShieldCheck className="size-3.5 shrink-0" />
              Sponsorship Verified
            </span>

            <div className="relative z-10 mx-auto max-w-3xl text-center">
              {/* Compact row above title on smaller screens */}
              <div className="mb-5 flex flex-wrap items-center justify-center gap-2 lg:hidden">
                <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-200/80 bg-card px-3 py-1.5 text-[11px] font-semibold text-emerald-700 shadow-sm">
                  <BadgeCheck className="size-3.5 shrink-0" />
                  98% Skill Overlap
                </span>
                <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-card px-3 py-1.5 text-[11px] font-semibold text-primary shadow-sm">
                  <ShieldCheck className="size-3.5 shrink-0" />
                  Sponsorship Verified
                </span>
              </div>

              <h1 className="text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl lg:text-6xl">
                <span className="block">Engineering Your Next</span>
                <span className="script-accent mt-2 block text-5xl font-semibold italic leading-tight sm:text-6xl lg:text-7xl">
                  Paradigm Shift.
                </span>
              </h1>

              <p className="mx-auto mt-6 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
                High-density semantic matching for the top 1% of talent. Move beyond searches—start
                achieving outcomes.
              </p>
            </div>
          </div>

          <div
            className="animate-fade-in-up mx-auto mt-10 max-w-3xl opacity-0"
            style={{ animationDelay: "0.35s", animationFillMode: "forwards" }}
          >
            <div className="flex flex-col gap-2 rounded-2xl border border-border/80 bg-card p-2 shadow-lg shadow-primary/5 sm:flex-row sm:items-center">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Role or Tech Stack (e.g., L7 Staff Engineer)"
                  className="h-12 border-0 bg-transparent pl-11 shadow-none focus-visible:ring-0"
                />
              </div>
              <div className="hidden h-8 w-px bg-border sm:block" />
              <div className="relative sm:w-44">
                <MapPin className="absolute left-4 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Global / Remote"
                  className="h-12 border-0 bg-transparent pl-11 shadow-none focus-visible:ring-0"
                />
              </div>
              <Link
                href="/login"
                className="inline-flex h-12 shrink-0 items-center justify-center rounded-xl bg-primary px-8 text-sm font-semibold text-primary-foreground shadow-md shadow-primary/25 transition-all hover:bg-primary/90 hover:shadow-lg"
              >
                Initiate Match
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Company marquee */}
      <section className="border-y border-border/50 bg-surface/40 py-10">
        <ScrollReveal>
          <p className="mb-6 text-center text-[10px] font-bold uppercase tracking-[0.2em] text-muted-foreground">
            Powering the future of high-growth teams
          </p>
          <InfiniteMarquee items={COMPANY_LOGOS} speed="slow" />
        </ScrollReveal>
      </section>

      {/* Platform capabilities */}
      <section className="mx-auto max-w-7xl px-6 py-20 sm:py-28">
        <CapabilitiesCarousel />
      </section>

      {/* AI Agent */}
      <section className="border-y border-border/50 bg-surface/30 py-20 sm:py-28">
        <div className="mx-auto grid max-w-7xl items-center gap-12 px-6 lg:grid-cols-2 lg:gap-16">
          <ScrollReveal direction="left">
            <span className="inline-flex rounded-full bg-primary/10 px-3 py-1 text-[10px] font-bold tracking-widest text-primary">
              LIVE AI AGENT
            </span>
            <h2 className="mt-5 text-3xl font-bold leading-tight tracking-tight text-foreground sm:text-4xl">
              Your career agent,{" "}
              <span className="script-accent text-4xl font-semibold italic sm:text-5xl">
                always active.
              </span>
            </h2>
            <p className="mt-5 max-w-lg text-base leading-relaxed text-muted-foreground">
              While you focus on building, your Job Scout agent is negotiating, vetting, and matching
              in the background with terminal-grade precision.
            </p>
            <AgentStats />
          </ScrollReveal>

          <ScrollReveal direction="right" delay={150}>
            <AgentTerminal />
          </ScrollReveal>
        </div>
      </section>

      {/* Testimonials */}
      <section className="mx-auto max-w-7xl px-6 py-20 sm:py-28">
        <ScrollReveal>
          <h2 className="mb-12 text-center text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
            Trusted by leaders who ship
          </h2>
        </ScrollReveal>
        <div className="hidden lg:grid lg:grid-cols-3 lg:gap-6">
          <TestimonialsGrid />
        </div>
        <div className="lg:hidden">
          <TestimonialsCarousel />
        </div>
      </section>

      {/* CTA */}
      <section className="landing-cta-bg py-20 sm:py-28">
        <ScrollReveal>
          <div className="mx-auto max-w-3xl rounded-3xl border border-border/60 bg-card px-8 py-14 text-center shadow-xl shadow-primary/5 sm:px-16">
            <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              The elite network is waiting for{" "}
              <span className="script-accent text-4xl font-semibold italic sm:text-5xl">you.</span>
            </h2>
            <p className="mx-auto mt-4 max-w-lg text-muted-foreground">
              No resume black holes. Just precise, high-value career moves tailored to your unique
              trajectory.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Link
                href="/login"
                className="inline-flex h-12 w-full items-center justify-center rounded-full bg-primary px-8 text-sm font-semibold text-primary-foreground shadow-md shadow-primary/25 transition-all hover:bg-primary/90 sm:w-auto"
              >
                Build My Trajectory
              </Link>
              <Link
                href="/login"
                className="inline-flex h-12 w-full items-center justify-center rounded-full border border-border bg-background px-8 text-sm font-semibold text-foreground transition-colors hover:bg-muted sm:w-auto"
              >
                Talk to an Agent
              </Link>
            </div>
            <p className="mt-6 text-[10px] font-bold uppercase tracking-[0.15em] text-muted-foreground">
              Free for elite candidates · Always confidential
            </p>
          </div>
        </ScrollReveal>
      </section>

      <LandingFooter />
    </div>
  )
}

function TestimonialsGrid() {
  const items = [
    {
      score: "98%",
      quote:
        "Job Scout surfaced a Principal role I'd never find on LinkedIn. Match score was dead-on — interview in 9 days.",
      name: "Sarah Chen",
      title: "VP Engineering @ NextGen",
      initials: "SC",
      color: "bg-violet-100 text-violet-700",
    },
    {
      score: "96%",
      quote:
        "The sponsorship filter alone saved me weeks. Every role it surfaced was H1-B verified before I applied.",
      name: "Marcus Okonkwo",
      title: "Staff ML Engineer @ Helix",
      initials: "MO",
      color: "bg-blue-100 text-blue-700",
    },
    {
      score: "99%",
      quote:
        "Salary intelligence gave me leverage I didn't know I had. Closed 22% above my initial offer.",
      name: "Elena Vasquez",
      title: "Director of Product @ Arcadia",
      initials: "EV",
      color: "bg-emerald-100 text-emerald-700",
    },
  ]

  return (
    <>
      {items.map((t, i) => (
        <ScrollReveal key={t.name} delay={i * 100}>
          <div className="h-full rounded-2xl border border-border/80 bg-card p-8 shadow-md transition-all hover:-translate-y-1 hover:shadow-lg">
            <span className="inline-flex rounded-full bg-primary/10 px-3 py-1 text-[10px] font-bold tracking-widest text-primary">
              MATCH SCORE: {t.score}
            </span>
            <p className="mt-5 text-sm leading-relaxed text-foreground/90">&ldquo;{t.quote}&rdquo;</p>
            <div className="mt-6 flex items-center gap-3 border-t border-border/60 pt-5">
              <div
                className={`flex size-10 items-center justify-center rounded-full text-sm font-semibold ${t.color}`}
              >
                {t.initials}
              </div>
              <div>
                <p className="font-semibold text-foreground">{t.name}</p>
                <p className="text-sm text-muted-foreground">{t.title}</p>
              </div>
            </div>
          </div>
        </ScrollReveal>
      ))}
    </>
  )
}
