"use client"

import type { ContactInfo } from "@/lib/profile/contact"
import { MapPin, Mail, Phone, Link } from "lucide-react"

interface ContactPillsProps {
  email: string
  contact: ContactInfo
}

export function ContactPills({ email, contact }: ContactPillsProps) {
  const items: { icon: typeof Mail; label: string; href?: string }[] = []

  if (contact.location) items.push({ icon: MapPin, label: contact.location })
  if (email) items.push({ icon: Mail, label: email, href: `mailto:${email}` })
  if (contact.phone) items.push({ icon: Phone, label: contact.phone, href: `tel:${contact.phone}` })
  if (contact.linkedin) {
    const href = contact.linkedin.startsWith("http") ? contact.linkedin : `https://${contact.linkedin}`
    items.push({ icon: Link, label: "LinkedIn", href })
  }
  if (contact.github) {
    const href = contact.github.startsWith("http") ? contact.github : `https://${contact.github}`
    items.push({ icon: Link, label: "GitHub", href })
  }

  if (items.length === 0) return null

  return (
    <div className="mt-3 flex flex-wrap gap-2">
      {items.map((item) => {
        const Icon = item.icon
        const inner = (
          <span className="inline-flex items-center gap-1.5 rounded-full bg-zinc-100 px-3 py-1 text-sm text-zinc-700">
            <Icon className="size-3.5 shrink-0" />
            {item.label}
          </span>
        )
        return item.href ? (
          <a key={item.label} href={item.href} target="_blank" rel="noreferrer" className="hover:opacity-80">
            {inner}
          </a>
        ) : (
          <span key={item.label}>{inner}</span>
        )
      })}
    </div>
  )
}
