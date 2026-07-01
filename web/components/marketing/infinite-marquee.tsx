"use client"

import { cn } from "@/lib/utils"

export interface MarqueeItem {
  id: string
  label: string
  badge?: string
}

interface InfiniteMarqueeProps {
  items: MarqueeItem[]
  className?: string
  speed?: "slow" | "normal" | "fast"
}

export function InfiniteMarquee({ items, className, speed = "normal" }: InfiniteMarqueeProps) {
  const loop = [...items, ...items]

  return (
    <div className={cn("relative overflow-hidden", className)}>
      <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-24 bg-gradient-to-r from-background to-transparent" />
      <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-24 bg-gradient-to-l from-background to-transparent" />

      <div
        className={cn(
          "flex w-max gap-16 py-2",
          speed === "slow" && "animate-marquee-slow",
          speed === "normal" && "animate-marquee",
          speed === "fast" && "animate-marquee-fast",
        )}
      >
        {loop.map((item, index) => (
          <div
            key={`${item.id}-${index}`}
            className="group relative flex shrink-0 items-center"
          >
            <span className="text-lg font-semibold tracking-tight text-muted-foreground/70 transition-colors duration-300 group-hover:text-foreground">
              {item.label}
            </span>
            {item.badge ? (
              <span className="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-full border border-primary/20 bg-card px-2.5 py-0.5 text-[10px] font-semibold text-primary opacity-0 shadow-sm transition-all duration-300 group-hover:opacity-100">
                {item.badge}
              </span>
            ) : null}
          </div>
        ))}
      </div>
    </div>
  )
}
