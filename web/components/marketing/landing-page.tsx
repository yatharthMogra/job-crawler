import Link from "next/link"
import {
  ArrowRight,
  BadgeCheck,
  Brain,
  MapPin,
  Search,
  Sparkles,
  Users,
} from "lucide-react"
import { MarketingNav } from "@/components/layout/marketing-nav"
import { PageSection } from "@/components/marketing/page-section"
import { StatBlock } from "@/components/marketing/stat-block"
import { Accordion } from "@/components/ui/accordion"
import { Input } from "@/components/ui/input"

const FAQ_ITEMS = [
  {
    id: "linkedin",
    question: "How is CareerMatch different from LinkedIn?",
    answer:
      "CareerMatch uses semantic AI matching to understand executive-level nuance in your profile — not just keyword overlap. You get tailored recommendations, autofill applications, and insider connection suggestions in under a minute.",
  },
  {
    id: "security",
    question: "Is my personal information secure?",
    answer:
      "Yes. Your profile data is kept private and encrypted. We never sell your information to third parties, and you control what recruiters can see.",
  },
  {
    id: "resume",
    question: "Can I use the AI agent to write my resumes?",
    answer:
      "Absolutely. Upload your resume once and our AI tailors versions for each role, highlighting the experience and skills most relevant to that opportunity.",
  },
]

export function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      <MarketingNav />

      {/* Hero */}
      <section className="marketing-hero-bg border-b border-border/60">
        <div className="mx-auto grid max-w-7xl items-center gap-12 px-6 py-16 lg:grid-cols-2 lg:py-24">
          <div>
            <span className="inline-flex items-center rounded-full bg-primary px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-primary-foreground">
              No.1 AI Job Hunting Platform
            </span>
            <h1 className="mt-6 text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl">
              No More Solo Job Hunting.{" "}
              <span className="text-primary">Do it with AI.</span>
            </h1>
            <p className="mt-5 max-w-lg text-base leading-relaxed text-muted-foreground">
              Get matched jobs, autofill applications, tailored resumes, and recommended insider
              connections in less than 1 minute.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                href="/login"
                className="btn-brand inline-flex h-11 items-center rounded-lg px-6 text-sm font-semibold"
              >
                TRY FOR FREE
              </Link>
              <Link
                href="/login"
                className="inline-flex h-11 items-center rounded-lg border border-border bg-card px-6 text-sm font-semibold hover:bg-muted"
              >
                View Demo
              </Link>
            </div>
            <div className="mt-8 flex items-center gap-3">
              <div className="flex -space-x-2">
                {["A", "B", "C"].map((letter) => (
                  <div
                    key={letter}
                    className="flex size-8 items-center justify-center rounded-full border-2 border-card bg-primary/20 text-xs font-semibold text-primary"
                  >
                    {letter}
                  </div>
                ))}
              </div>
              <p className="text-sm text-muted-foreground">
                Trusted by <span className="font-semibold text-foreground">1.25M+</span> Executives
              </p>
            </div>
          </div>

          <div className="relative">
            <div className="card-elevated mx-auto max-w-md p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="flex size-12 items-center justify-center rounded-full bg-primary/15 text-lg font-bold text-primary">
                    J
                  </div>
                  <div>
                    <p className="font-semibold text-foreground">Jamie Parker</p>
                    <p className="text-sm text-muted-foreground">Senior Data Scientist</p>
                  </div>
                </div>
                <div className="flex size-14 flex-col items-center justify-center rounded-full border-4 border-primary/30 bg-accent text-center">
                  <span className="text-sm font-bold text-primary">9.0</span>
                  <span className="text-[8px] font-medium text-muted-foreground">AI Match</span>
                </div>
              </div>
              <div className="mt-5 rounded-xl border border-primary/20 bg-accent/50 p-4">
                <p className="text-[10px] font-bold uppercase tracking-wider text-primary">AI Agent</p>
                <p className="mt-2 text-sm leading-relaxed text-foreground/80">
                  Strong alignment with your ML background. Salary band identified at $180k–$220k.
                </p>
              </div>
              <div className="mt-4 flex gap-2">
                <span className="rounded-full bg-add-muted px-3 py-1 text-xs font-medium text-add-foreground">
                  Personalized Pitch
                </span>
                <span className="rounded-full bg-add-muted px-3 py-1 text-xs font-medium text-add-foreground">
                  Skill Check
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <PageSection className="py-12">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          <StatBlock value="1.25M+" label="Trusted Executives" />
          <StatBlock value="3x" label="Interview Landings" />
          <StatBlock value="80%" label="Time Saved" />
          <StatBlock value="No.1" label="C-Suite Choice" />
        </div>
      </PageSection>

      {/* Job Hub */}
      <PageSection id="job-hub" className="border-t border-border/60 bg-surface/50">
        <h2 className="text-center text-3xl font-bold tracking-tight text-foreground">
          ACCESS THE <span className="text-primary">LARGEST JOB HUB</span>
        </h2>
        <div className="mx-auto mt-8 max-w-4xl">
          <div className="flex flex-col gap-3 rounded-2xl border border-border bg-card p-3 shadow-md sm:flex-row sm:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="Job Title" className="h-11 border-0 bg-surface pl-9 shadow-none" />
            </div>
            <Input placeholder="Work Model" className="h-11 border-0 bg-surface shadow-none sm:w-40" />
            <div className="relative flex-1">
              <MapPin className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input placeholder="United States" className="h-11 border-0 bg-surface pl-9 shadow-none" />
            </div>
            <Link
              href="/login"
              className="btn-brand inline-flex h-11 shrink-0 items-center gap-1 rounded-lg px-6 font-semibold"
            >
              GO <ArrowRight className="size-4" />
            </Link>
          </div>
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          <div className="card-elevated relative overflow-hidden p-8">
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent" />
            <div className="relative">
              <p className="text-sm text-muted-foreground">Total Jobs</p>
              <p className="text-4xl font-bold text-primary">8,000,000+</p>
              <p className="mt-4 text-sm text-muted-foreground">Today&apos;s New Jobs</p>
              <p className="text-2xl font-bold text-foreground">400,000+</p>
            </div>
          </div>
          <div className="flex flex-col justify-center gap-8">
            <div className="flex gap-4">
              <div className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-accent text-primary">
                <Brain className="size-5" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">Semantic AI Matching</h3>
                <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                  Our engine understands executive-level nuance — leadership scope, industry context,
                  and career trajectory — not just keywords.
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-accent text-primary">
                <Users className="size-5" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">Verified Connections</h3>
                <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                  Identify the right people at each company with AI-generated icebreakers tailored to
                  your shared background.
                </p>
              </div>
            </div>
          </div>
        </div>
      </PageSection>

      {/* FAQ */}
      <PageSection id="faq">
        <h2 className="mb-8 text-center text-2xl font-bold uppercase tracking-wide text-foreground">
          Frequently Asked Questions
        </h2>
        <div className="mx-auto max-w-2xl">
          <Accordion items={FAQ_ITEMS} defaultOpen="linkedin" />
        </div>
      </PageSection>

      {/* Footer CTA */}
      <section className="navy-section py-16 text-center">
        <div className="mx-auto max-w-2xl px-6">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Take You to Your Next Opportunity.
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-white/70">
            Join the exclusive tier of high-performance executives landing their dream roles with
            precision.
          </p>
          <Link
            href="/login"
            className="btn-brand mt-8 inline-flex h-11 items-center rounded-lg px-8 text-sm font-semibold"
          >
            TRY FOR FREE NOW
          </Link>
        </div>
      </section>

      <footer className="border-t border-border py-8 text-center text-xs text-muted-foreground">
        <p className="flex items-center justify-center gap-1.5">
          <Sparkles className="size-3.5 text-primary" />
          CareerMatch — AI-powered executive job hunting
        </p>
        <p className="mt-2 flex items-center justify-center gap-1">
          <BadgeCheck className="size-3.5 text-add" />
          Verified listings · Secure profiles
        </p>
      </footer>
    </div>
  )
}
