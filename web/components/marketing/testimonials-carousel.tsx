"use client"

import { useCallback, useEffect, useState } from "react"
import { ScrollReveal } from "@/components/marketing/scroll-reveal"
import { cn } from "@/lib/utils"

interface Testimonial {
  id: string
  score: string
  quote: string
  name: string
  title: string
  initials: string
  color: string
}

const TESTIMONIALS: Testimonial[] = [
  {
    id: "sarah",
    score: "98%",
    quote:
      "Job Scout surfaced a Principal role I'd never find on LinkedIn. Match score was dead-on — interview in 9 days.",
    name: "Sarah Chen",
    title: "VP Engineering @ NextGen",
    initials: "SC",
    color: "bg-violet-100 text-violet-700",
  },
  {
    id: "marcus",
    score: "96%",
    quote:
      "The sponsorship filter alone saved me weeks. Every role it surfaced was H1-B verified before I applied.",
    name: "Marcus Okonkwo",
    title: "Staff ML Engineer @ Helix",
    initials: "MO",
    color: "bg-blue-100 text-blue-700",
  },
  {
    id: "elena",
    score: "99%",
    quote:
      "Salary intelligence gave me leverage I didn't know I had. Closed 22% above my initial offer.",
    name: "Elena Vasquez",
    title: "Director of Product @ Arcadia",
    initials: "EV",
    color: "bg-emerald-100 text-emerald-700",
  },
]

export function TestimonialsCarousel() {
  const [index, setIndex] = useState(0)

  const next = useCallback(() => {
    setIndex((i) => (i + 1) % TESTIMONIALS.length)
  }, [])

  useEffect(() => {
    const timer = setInterval(next, 6000)
    return () => clearInterval(timer)
  }, [next])

  return (
    <ScrollReveal>
      <div className="relative overflow-hidden">
        <div
          className="flex transition-transform duration-700 ease-out"
          style={{ transform: `translateX(-${index * 100}%)` }}
        >
          {TESTIMONIALS.map((t) => (
            <div key={t.id} className="w-full shrink-0 px-2 sm:px-4">
              <div className="mx-auto max-w-lg rounded-2xl border border-border/80 bg-card p-8 shadow-md transition-shadow hover:shadow-lg">
                <span className="inline-flex rounded-full bg-primary/10 px-3 py-1 text-[10px] font-bold tracking-widest text-primary">
                  MATCH SCORE: {t.score}
                </span>
                <p className="mt-5 text-base leading-relaxed text-foreground/90">&ldquo;{t.quote}&rdquo;</p>
                <div className="mt-6 flex items-center gap-3 border-t border-border/60 pt-5">
                  <div
                    className={cn(
                      "flex size-10 items-center justify-center rounded-full text-sm font-semibold",
                      t.color,
                    )}
                  >
                    {t.initials}
                  </div>
                  <div>
                    <p className="font-semibold text-foreground">{t.name}</p>
                    <p className="text-sm text-muted-foreground">{t.title}</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 flex justify-center gap-2">
          {TESTIMONIALS.map((t, i) => (
            <button
              key={t.id}
              type="button"
              onClick={() => setIndex(i)}
              className={cn(
                "h-2 rounded-full transition-all duration-300",
                i === index ? "w-6 bg-primary" : "w-2 bg-border",
              )}
              aria-label={`View testimonial from ${t.name}`}
            />
          ))}
        </div>
      </div>
    </ScrollReveal>
  )
}
