"use client"

import type { ContactChange } from "@/lib/profile-data"
import { Code, Link, Mail, MapPin, Phone } from "lucide-react"

interface ContactSectionProps {
  contact: ContactChange
}

export function ContactSection({ contact }: ContactSectionProps) {
  const hasAny =
    contact.location || contact.phone || contact.linkedin || contact.github
  if (!hasAny) return null

  return (
    <div>
      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
        Contact
      </h3>
      <div className="grid gap-3 sm:grid-cols-2">
        {contact.location ? <ContactRow icon={MapPin} label="Location" value={contact.location} /> : null}
        {contact.phone ? <ContactRow icon={Phone} label="Phone" value={contact.phone} /> : null}
        {contact.linkedin ? (
          <ContactRow icon={Link} label="LinkedIn" value={contact.linkedin} />
        ) : null}
        {contact.github ? <ContactRow icon={Code} label="GitHub" value={contact.github} /> : null}
      </div>
      <p className="mt-3 text-xs text-muted-foreground">
        Parsed from your resume. Email is collected during onboarding.
      </p>
    </div>
  )
}

function ContactRow({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Mail
  label: string
  value: string
}) {
  return (
    <div className="flex items-start gap-3 rounded-xl border border-border bg-card p-4">
      <span className="flex size-9 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
        <Icon className="size-4" aria-hidden="true" />
      </span>
      <div>
        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{label}</p>
        <p className="mt-1 text-sm font-medium text-foreground">{value}</p>
      </div>
    </div>
  )
}
