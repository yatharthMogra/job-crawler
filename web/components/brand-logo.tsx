"use client"

import { useEffect, useState } from "react"
import { getBrandInitial } from "@/lib/brand-logos"
import { cn } from "@/lib/utils"

interface BrandLogoProps {
  name: string
  size?: number
  variant?: "company" | "school"
  shape?: "square" | "circle"
  className?: string
  /** Stored logo URL from API (cloud storage). Letter avatar when missing or on error. */
  logoUrl?: string | null
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
      style={{ width: size, height: size, fontSize: size * 0.38 }}
      aria-hidden="true"
      title={name}
    >
      {getBrandInitial(name)}
    </div>
  )
}

export function BrandLogo({
  name,
  size = 32,
  shape = "square",
  className,
  logoUrl,
}: BrandLogoProps) {
  const storedUrl = logoUrl?.trim() ?? ""
  const [failed, setFailed] = useState(false)

  useEffect(() => {
    setFailed(false)
  }, [storedUrl, name])

  const roundedClass = shape === "circle" ? "rounded-full" : "rounded-xl"

  if (!name.trim() || !storedUrl || failed) {
    return <LetterFallback name={name || "?"} size={size} shape={shape} className={className} />
  }

  return (
    <div
      className={cn(
        "flex shrink-0 items-center justify-center overflow-hidden border border-border/40 bg-white shadow-sm",
        roundedClass,
        className,
      )}
      style={{ width: size, height: size }}
      title={name}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        key={`${name}-${storedUrl}`}
        src={storedUrl}
        alt=""
        width={size}
        height={size}
        loading="lazy"
        decoding="async"
        referrerPolicy="no-referrer"
        className="size-full object-contain p-[12%]"
        onError={() => setFailed(true)}
      />
    </div>
  )
}
