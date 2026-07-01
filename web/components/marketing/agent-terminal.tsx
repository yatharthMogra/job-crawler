"use client"

import { useEffect, useState } from "react"
import { useInView } from "@/lib/hooks/use-in-view"
import { cn } from "@/lib/utils"

const TERMINAL_LINES = [
  { text: "> initiating_scan --target 'Principal AI Engineer'", color: "text-slate-400" },
  { text: "> Accessing private venture networks...", color: "text-slate-400" },
  { text: "> Parsing 1,247 semantic skill vectors...", color: "text-emerald-400" },
  { text: "> Filtering H1-B eligible roles...", color: "text-blue-400" },
  { text: "> Match confirmed: 99% Overlap", color: "text-emerald-300" },
  { text: "> Salary band: $285k–$340k (verified)", color: "text-amber-300" },
  { text: "> Agent standing by. Next scan in 14ms.", color: "text-slate-500" },
]

export function AgentTerminal({ className }: { className?: string }) {
  const { ref, inView } = useInView<HTMLDivElement>()
  const [visibleLines, setVisibleLines] = useState(0)
  const [charIndex, setCharIndex] = useState(0)

  useEffect(() => {
    if (!inView) return

    const currentLine = TERMINAL_LINES[visibleLines]
    if (!currentLine) {
      const reset = setTimeout(() => {
        setVisibleLines(0)
        setCharIndex(0)
      }, 3000)
      return () => clearTimeout(reset)
    }

    if (charIndex < currentLine.text.length) {
      const timer = setTimeout(() => setCharIndex((c) => c + 1), 22)
      return () => clearTimeout(timer)
    }

    const next = setTimeout(() => {
      setVisibleLines((l) => l + 1)
      setCharIndex(0)
    }, 400)
    return () => clearTimeout(next)
  }, [inView, visibleLines, charIndex])

  return (
    <div
      ref={ref}
      className={cn(
        "overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-950 shadow-2xl shadow-primary/10",
        className,
      )}
    >
      <div className="flex items-center gap-2 border-b border-slate-800 px-4 py-3">
        <span className="size-2.5 rounded-full bg-red-500/80" />
        <span className="size-2.5 rounded-full bg-amber-400/80" />
        <span className="size-2.5 rounded-full bg-emerald-400/80" />
        <span className="ml-2 font-mono text-[11px] text-slate-500">job-scout-agent — zsh</span>
      </div>
      <div className="min-h-[220px] space-y-1.5 p-5 font-mono text-[13px] leading-relaxed">
        {TERMINAL_LINES.slice(0, visibleLines).map((line, i) => (
          <p key={i} className={line.color}>
            {line.text}
            <span className="animate-pulse text-emerald-400">▋</span>
          </p>
        ))}
        {visibleLines < TERMINAL_LINES.length && TERMINAL_LINES[visibleLines] ? (
          <p className={TERMINAL_LINES[visibleLines].color}>
            {TERMINAL_LINES[visibleLines].text.slice(0, charIndex)}
            <span className="animate-pulse text-emerald-400">▋</span>
          </p>
        ) : null}
      </div>
    </div>
  )
}
