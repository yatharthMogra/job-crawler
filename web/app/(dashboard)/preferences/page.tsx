"use client"

import { useEffect, useMemo } from "react"
import type { EditSection } from "@/components/profile/profile-edit-dialog"
import { ProfileEditDialog } from "@/components/profile/profile-edit-dialog"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"
import { useSession } from "@/components/session-provider"
import { FeedSkeleton } from "@/components/card-skeleton"

function formatList(values: string[] | undefined) {
  if (!values?.length) return "Not set"
  return values.join(", ")
}

export default function PreferencesPage() {
  const { candidateId } = useSession()
  const { rawProfile, editSection, setEditSection, handleProfileEdit, loadProfileHome } =
    useProfileFlow()

  useEffect(() => {
    if (candidateId) {
      void loadProfileHome(candidateId).catch(() => undefined)
    }
  }, [candidateId, loadProfileHome])

  const rows = useMemo(() => {
    const prefs = rawProfile?.preferences as
      | {
          primary_roles?: string[]
          preferred_locations?: string[]
          remote_preference?: string
          preferred_industries?: string[]
        }
      | undefined
    const constraints = rawProfile?.constraints as
      | { work_authorization?: string; sponsorship_required?: boolean }
      | undefined
    return [
      {
        label: "Roles",
        value: formatList(prefs?.primary_roles),
        section: "preferences" as EditSection,
      },
      {
        label: "Locations",
        value: formatList(prefs?.preferred_locations),
        section: "preferences" as EditSection,
      },
      {
        label: "Remote preference",
        value: prefs?.remote_preference ?? "Not set",
        section: "preferences" as EditSection,
      },
      {
        label: "Industries",
        value: formatList(prefs?.preferred_industries),
        section: "preferences" as EditSection,
      },
      {
        label: "Work authorization",
        value: constraints?.work_authorization ?? "Not set",
        section: "constraints" as EditSection,
      },
      {
        label: "Sponsorship required",
        value: constraints?.sponsorship_required ? "Yes" : "No",
        section: "constraints" as EditSection,
      },
    ]
  }, [rawProfile])

  const initialValues = useMemo(() => {
    if (!editSection || !rawProfile) return undefined
    if (editSection === "preferences") return rawProfile.preferences as Record<string, unknown>
    if (editSection === "constraints") return rawProfile.constraints as Record<string, unknown>
    return rawProfile.education as Record<string, unknown>
  }, [editSection, rawProfile])

  if (!rawProfile) {
    return (
      <div>
        <div className="border-b border-zinc-200 bg-zinc-50 px-6 py-3">
          <h1 className="text-sm font-semibold text-zinc-900">Preferences</h1>
        </div>
        <div className="px-6 py-4">
          <FeedSkeleton count={4} />
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="border-b border-zinc-200 bg-zinc-50 px-6 py-3">
        <h1 className="text-sm font-semibold text-zinc-900">Preferences</h1>
        <p className="text-xs text-zinc-400">Job matching filters derived from your profile</p>
      </div>
      <div className="px-6 py-6">
        <div className="max-w-2xl space-y-5 rounded-md border border-zinc-200 bg-white p-6">
          {rows.map((row) => (
            <div
              key={row.label}
              className="flex items-center justify-between border-b border-zinc-100 pb-4 last:border-0 last:pb-0"
            >
              <div>
                <p className="text-sm font-medium text-zinc-800">{row.label}</p>
                <p className="text-xs text-zinc-500">{row.value}</p>
              </div>
              <button
                type="button"
                onClick={() => setEditSection(row.section)}
                className="h-7 rounded-md border border-zinc-200 px-2.5 text-xs font-medium text-zinc-600 hover:bg-zinc-50"
              >
                Edit
              </button>
            </div>
          ))}
        </div>
      </div>

      <ProfileEditDialog
        section={editSection}
        onClose={() => setEditSection(null)}
        onSave={async (section, values) => {
          await handleProfileEdit(section, values)
          setEditSection(null)
        }}
        initialValues={initialValues}
      />
    </div>
  )
}
