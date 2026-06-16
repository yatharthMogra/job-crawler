"use client"

import { useEffect, useState } from "react"
import { getBrandInitial, getBrandLogoSources } from "@/lib/brand-logos"
import { cn } from "@/lib/utils"

interface BrandLogoProps {
  name: string
  size?: number
  variant?: "company" | "school"
  shape?: "square" | "circle"
  className?: string
}

const COLORS = [
  "bg-primary",
  "bg-indigo-600",
  "bg-emerald-700",
  "bg-rose-600",
  "bg-amber-600",
  "bg-sky-700",
  "bg-violet-700",
  "bg-teal-700",
]

function colorFor(name: string) {
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash)
  return COLORS[Math.abs(hash) % COLORS.length]
}

function LetterFallback({
  name,
  size,
  shape,
  className,
}: {
  name: string
  size: number
  shape: "square" | "circle"
  className?: string
}) {
  return (
    <div
      className={cn(
        "flex shrink-0 items-center justify-center font-semibold text-white",
        shape === "circle" ? "rounded-full" : "rounded-lg",
        colorFor(name),
        className,
      )}
      style={{ width: size, height: size, fontSize: size * 0.42 }}
      aria-hidden="true"
    >
      {getBrandInitial(name)}
    </div>
  )
}

export function BrandLogo({
  name,
  size = 32,
  variant = "company",
  shape = "square",
  className,
}: BrandLogoProps) {
  const sources = getBrandLogoSources(name, variant)
  const [sourceIndex, setSourceIndex] = useState(0)

  useEffect(() => {
    setSourceIndex(0)
  }, [name, variant])

  const roundedClass = shape === "circle" ? "rounded-full" : "rounded-lg"

  if (sourceIndex >= sources.length) {
    return <LetterFallback name={name} size={size} shape={shape} className={className} />
  }

  return (
    <div
      className={cn(
        "flex shrink-0 items-center justify-center overflow-hidden border border-border/50 bg-white shadow-sm",
        roundedClass,
        className,
      )}
      style={{ width: size, height: size }}
    >
      <img
        key={`${name}-${sources[sourceIndex]}`}
        src={sources[sourceIndex]}
        alt=""
        width={size}
        height={size}
        className="size-full object-cover"
        onError={() => setSourceIndex((i) => i + 1)}
      />
    </div>
  )
}
