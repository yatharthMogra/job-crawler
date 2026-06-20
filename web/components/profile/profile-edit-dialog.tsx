"use client"

import { useEffect, useState } from "react"
import type { ContactInfo } from "@/lib/profile/contact"
import { eeoFromApiPayload, eeoToApiPayload, emptyEeo, type EeoState } from "@/lib/profile/eeo"
import { EeoForm } from "@/components/profile/eeo-form"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import {
  DEGREE_OPTIONS,
  GRADUATION_DATE_OPTIONS,
  UNIVERSITY_OPTIONS,
} from "@/lib/profile/education-options"

export type EditSection = "constraints" | "preferences" | "education" | "eeo" | "contact"

interface ProfileEditDialogProps {
  section: EditSection | null
  onClose: () => void
  onSave: (section: EditSection, values: Record<string, unknown>) => Promise<void>
  initialValues?: Record<string, unknown>
  contactValues?: ContactInfo
  eeoValues?: EeoState
}

export function ProfileEditDialog({
  section,
  onClose,
  onSave,
  initialValues,
  contactValues,
  eeoValues,
}: ProfileEditDialogProps) {
  const [values, setValues] = useState<Record<string, string>>({})
  const [eeo, setEeo] = useState<EeoState>(emptyEeo())
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!section) {
      setValues({})
      setEeo(emptyEeo())
      return
    }
    if (section === "eeo") {
      setEeo(eeoValues ?? eeoFromApiPayload(initialValues))
      setValues({})
      return
    }
    if (section === "contact") {
      setValues({
        location: contactValues?.location ?? "",
        phone: contactValues?.phone ?? "",
        linkedin: contactValues?.linkedin ?? "",
        github: contactValues?.github ?? "",
      })
      return
    }
    if (!initialValues) {
      setValues({})
      return
    }
    if (section === "education") {
      setValues({
        degree: String(initialValues.degree ?? ""),
        university: String(initialValues.university ?? ""),
        graduation_date: String(initialValues.graduation_date ?? ""),
      })
    } else if (section === "constraints") {
      setValues({
        sponsorship_required: String(initialValues.sponsorship_required ?? "false"),
        visa_type: String(initialValues.visa_type ?? ""),
        work_authorization: String(initialValues.work_authorization ?? ""),
        minimum_hourly_rate: String(initialValues.minimum_hourly_rate ?? ""),
      })
    } else {
      setValues({
        primary_roles: Array.isArray(initialValues.primary_roles)
          ? initialValues.primary_roles.join(", ")
          : "",
        secondary_roles: Array.isArray(initialValues.secondary_roles)
          ? initialValues.secondary_roles.join(", ")
          : "",
        preferred_locations: Array.isArray(initialValues.preferred_locations)
          ? initialValues.preferred_locations.join(", ")
          : "",
        remote_preference: String(initialValues.remote_preference ?? ""),
        preferred_industries: Array.isArray(initialValues.preferred_industries)
          ? initialValues.preferred_industries.join(", ")
          : "",
      })
    }
    setError(null)
  }, [section, initialValues, contactValues, eeoValues])

  async function handleSave() {
    if (!section) return
    setLoading(true)
    setError(null)
    try {
      const payload: Record<string, unknown> = {}
      if (section === "eeo") {
        payload.eeo = eeoToApiPayload(eeo)
      } else if (section === "contact") {
        payload.contact = {
          location: values.location || null,
          phone: values.phone || null,
          linkedin: values.linkedin || null,
          github: values.github || null,
        }
      } else if (section === "education") {
        payload.degree = values.degree || null
        payload.university = values.university || null
        payload.graduation_date = values.graduation_date || null
      } else if (section === "constraints") {
        payload.sponsorship_required = values.sponsorship_required === "true"
        payload.visa_type = values.visa_type || null
        payload.work_authorization = values.work_authorization || null
        payload.minimum_hourly_rate = values.minimum_hourly_rate
          ? Number(values.minimum_hourly_rate)
          : null
      } else {
        payload.primary_roles = values.primary_roles
          ? values.primary_roles.split(",").map((s) => s.trim()).filter(Boolean)
          : []
        payload.secondary_roles = values.secondary_roles
          ? values.secondary_roles.split(",").map((s) => s.trim()).filter(Boolean)
          : []
        payload.preferred_locations = values.preferred_locations
          ? values.preferred_locations.split(",").map((s) => s.trim()).filter(Boolean)
          : []
        payload.remote_preference = values.remote_preference || null
        payload.preferred_industries = values.preferred_industries
          ? values.preferred_industries.split(",").map((s) => s.trim()).filter(Boolean)
          : []
      }
      await onSave(section, payload)
      onClose()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save")
    } finally {
      setLoading(false)
    }
  }

  const titles: Record<EditSection, string> = {
    constraints: "Edit constraints",
    preferences: "Edit preferences",
    education: "Edit education",
    eeo: "Edit equal employment authorization",
    contact: "Edit contact information",
  }

  return (
    <Dialog open={section !== null} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{section ? titles[section] : ""}</DialogTitle>
        </DialogHeader>

        {section === "education" ? (
          <div className="space-y-3">
            <SelectField
              label="Degree / major"
              value={values.degree ?? ""}
              onChange={(v) => setValues((s) => ({ ...s, degree: v }))}
              options={DEGREE_OPTIONS}
              placeholder="Select degree"
            />
            <SelectField
              label="University"
              value={values.university ?? ""}
              onChange={(v) => setValues((s) => ({ ...s, university: v }))}
              options={UNIVERSITY_OPTIONS}
              placeholder="Select university"
            />
            <SelectField
              label="Graduation date"
              value={values.graduation_date ?? ""}
              onChange={(v) => setValues((s) => ({ ...s, graduation_date: v }))}
              options={GRADUATION_DATE_OPTIONS.map((opt) => opt.value)}
              optionLabels={Object.fromEntries(
                GRADUATION_DATE_OPTIONS.map((opt) => [opt.value, opt.label]),
              )}
              placeholder="Select graduation date"
            />
          </div>
        ) : null}

        {section === "constraints" ? (
          <div className="space-y-3">
            <label className="block text-sm">
              <span className="mb-1 block text-muted-foreground">Sponsorship required</span>
              <select
                className="w-full rounded-md border border-border bg-background px-3 py-2 text-sm"
                value={values.sponsorship_required ?? "false"}
                onChange={(e) => setValues((s) => ({ ...s, sponsorship_required: e.target.value }))}
              >
                <option value="true">Yes</option>
                <option value="false">No</option>
              </select>
            </label>
            <Field label="Visa type" value={values.visa_type ?? ""} onChange={(v) => setValues((s) => ({ ...s, visa_type: v }))} />
            <Field label="Work authorization" value={values.work_authorization ?? ""} onChange={(v) => setValues((s) => ({ ...s, work_authorization: v }))} />
            <Field label="Minimum hourly rate" value={values.minimum_hourly_rate ?? ""} onChange={(v) => setValues((s) => ({ ...s, minimum_hourly_rate: v }))} />
          </div>
        ) : null}

        {section === "preferences" ? (
          <div className="space-y-3">
            <Field label="Primary roles (comma-separated)" value={values.primary_roles ?? ""} onChange={(v) => setValues((s) => ({ ...s, primary_roles: v }))} />
            <Field label="Secondary roles (comma-separated)" value={values.secondary_roles ?? ""} onChange={(v) => setValues((s) => ({ ...s, secondary_roles: v }))} />
            <Field label="Preferred locations (comma-separated)" value={values.preferred_locations ?? ""} onChange={(v) => setValues((s) => ({ ...s, preferred_locations: v }))} />
            <Field label="Remote preference" value={values.remote_preference ?? ""} onChange={(v) => setValues((s) => ({ ...s, remote_preference: v }))} />
            <Field label="Industries (comma-separated)" value={values.preferred_industries ?? ""} onChange={(v) => setValues((s) => ({ ...s, preferred_industries: v }))} />
          </div>
        ) : null}

        {section === "contact" ? (
          <div className="space-y-3">
            <Field label="Location" value={values.location ?? ""} onChange={(v) => setValues((s) => ({ ...s, location: v }))} />
            <Field label="Phone" value={values.phone ?? ""} onChange={(v) => setValues((s) => ({ ...s, phone: v }))} />
            <Field label="LinkedIn" value={values.linkedin ?? ""} onChange={(v) => setValues((s) => ({ ...s, linkedin: v }))} />
            <Field label="GitHub" value={values.github ?? ""} onChange={(v) => setValues((s) => ({ ...s, github: v }))} />
          </div>
        ) : null}

        {section === "eeo" ? <EeoForm state={eeo} onChange={setEeo} compact /> : null}

        {error ? <p className="text-sm text-remove">{error}</p> : null}

        <DialogFooter>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button disabled={loading} onClick={() => void handleSave()}>
            {loading ? "Saving..." : "Save"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

function SelectField({
  label,
  value,
  onChange,
  options,
  optionLabels,
  placeholder = "Select…",
}: {
  label: string
  value: string
  onChange: (v: string) => void
  options: readonly string[]
  optionLabels?: Record<string, string>
  placeholder?: string
}) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block text-muted-foreground">{label}</span>
      <select
        className="h-10 w-full rounded-md border border-border bg-background px-3 text-sm"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="">{placeholder}</option>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {optionLabels?.[opt] ?? opt}
          </option>
        ))}
      </select>
    </label>
  )
}

function Field({
  label,
  value,
  onChange,
}: {
  label: string
  value: string
  onChange: (v: string) => void
}) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block text-muted-foreground">{label}</span>
      <Input value={value} onChange={(e) => onChange(e.target.value)} />
    </label>
  )
}
