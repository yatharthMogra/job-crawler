"use client"

import type { ReactNode } from "react"
import { useInView } from "@/lib/hooks/use-in-view"
import { cn } from "@/lib/utils"

interface ScrollRevealProps {
  children: ReactNode
  className?: string
  delay?: number
  direction?: "up" | "left" | "right" | "none"
}

export function ScrollReveal({
  children,
  className,
  delay = 0,
  direction = "up",
}: ScrollRevealProps) {
  const { ref, inView } = useInView<HTMLDivElement>()

  return (
    <div
      ref={ref}
      className={cn(
        "transition-all duration-700 ease-out",
        inView ? "translate-x-0 translate-y-0 opacity-100" : "opacity-0",
        !inView && direction === "up" && "translate-y-8",
        !inView && direction === "left" && "-translate-x-8",
        !inView && direction === "right" && "translate-x-8",
        className,
      )}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  )
}
