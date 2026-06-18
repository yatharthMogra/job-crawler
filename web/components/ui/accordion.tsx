"use client"

import { useState, type ReactNode } from "react"
import { Minus, Plus } from "lucide-react"
import { cn } from "@/lib/utils"

interface AccordionItem {
  id: string
  question: string
  answer: ReactNode
}

interface AccordionProps {
  items: AccordionItem[]
  defaultOpen?: string
  className?: string
}

export function Accordion({ items, defaultOpen, className }: AccordionProps) {
  const [openId, setOpenId] = useState<string | null>(defaultOpen ?? items[0]?.id ?? null)

  return (
    <div className={cn("flex flex-col gap-3", className)}>
      {items.map((item) => {
        const open = openId === item.id
        return (
          <div
            key={item.id}
            className="overflow-hidden rounded-xl border border-border bg-card shadow-sm"
          >
            <button
              type="button"
              onClick={() => setOpenId(open ? null : item.id)}
              className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left"
            >
              <span className="text-sm font-semibold text-foreground">{item.question}</span>
              <span className="flex size-7 shrink-0 items-center justify-center rounded-full border border-border text-muted-foreground">
                {open ? <Minus className="size-3.5" /> : <Plus className="size-3.5" />}
              </span>
            </button>
            {open ? (
              <div className="border-t border-border px-5 pb-5 pt-1 text-sm leading-relaxed text-muted-foreground">
                {item.answer}
              </div>
            ) : null}
          </div>
        )
      })}
    </div>
  )
}
