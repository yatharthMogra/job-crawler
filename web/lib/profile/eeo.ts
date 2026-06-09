export interface EeoState {
  authorizedToWorkUs: boolean | null
  hasDisability: boolean | null
  gender: string
  requiresSponsorship: boolean | null
  identifiesLgbtq: boolean | null
  isVeteran: boolean | null
  race: string
  hispanicLatino: boolean | null
  sexualOrientation: string
}

export function emptyEeo(): EeoState {
  return {
    authorizedToWorkUs: null,
    hasDisability: null,
    gender: "",
    requiresSponsorship: null,
    identifiesLgbtq: null,
    isVeteran: null,
    race: "",
    hispanicLatino: null,
    sexualOrientation: "",
  }
}

export type EeoFieldType = "yesno" | "select"

export interface EeoFieldDef {
  key: keyof EeoState
  label: string
  type: EeoFieldType
  options?: string[]
}

export const EEO_FIELDS: EeoFieldDef[] = [
  {
    key: "authorizedToWorkUs",
    label: "Are you authorized to work in the US?",
    type: "yesno",
  },
  {
    key: "hasDisability",
    label: "Do you have a disability?",
    type: "yesno",
  },
  {
    key: "gender",
    label: "What is your gender?",
    type: "select",
    options: ["Male", "Female", "Non-binary", "Prefer not to say"],
  },
  {
    key: "requiresSponsorship",
    label: "Will you now or in the future require sponsorship for employment visa status?",
    type: "yesno",
  },
  {
    key: "identifiesLgbtq",
    label: "Do you identify as LGBTQ+?",
    type: "yesno",
  },
  {
    key: "isVeteran",
    label: "Are you a veteran?",
    type: "yesno",
  },
  {
    key: "race",
    label: "How would you identify your race?",
    type: "select",
    options: [
      "Asian",
      "Black or African American",
      "White",
      "Native American",
      "Pacific Islander",
      "Two or more races",
      "Prefer not to say",
    ],
  },
  {
    key: "hispanicLatino",
    label: "Are you Hispanic or Latino?",
    type: "yesno",
  },
  {
    key: "sexualOrientation",
    label: "How would you describe your sexual orientation?",
    type: "select",
    options: ["Heterosexual", "Homosexual", "Bisexual", "Asexual", "Prefer not to say"],
  },
]

export function eeoToApiPayload(state: EeoState): Record<string, unknown> {
  return {
    authorized_to_work_us: state.authorizedToWorkUs,
    has_disability: state.hasDisability,
    gender: state.gender || null,
    requires_sponsorship: state.requiresSponsorship,
    identifies_lgbtq: state.identifiesLgbtq,
    is_veteran: state.isVeteran,
    race: state.race || null,
    hispanic_latino: state.hispanicLatino,
    sexual_orientation: state.sexualOrientation || null,
  }
}

export function eeoFromApiPayload(raw: Record<string, unknown> | undefined): EeoState {
  if (!raw) return emptyEeo()
  return {
    authorizedToWorkUs:
      raw.authorized_to_work_us === null || raw.authorized_to_work_us === undefined
        ? null
        : Boolean(raw.authorized_to_work_us),
    hasDisability:
      raw.has_disability === null || raw.has_disability === undefined
        ? null
        : Boolean(raw.has_disability),
    gender: String(raw.gender ?? ""),
    requiresSponsorship:
      raw.requires_sponsorship === null || raw.requires_sponsorship === undefined
        ? null
        : Boolean(raw.requires_sponsorship),
    identifiesLgbtq:
      raw.identifies_lgbtq === null || raw.identifies_lgbtq === undefined
        ? null
        : Boolean(raw.identifies_lgbtq),
    isVeteran:
      raw.is_veteran === null || raw.is_veteran === undefined
        ? null
        : Boolean(raw.is_veteran),
    race: String(raw.race ?? ""),
    hispanicLatino:
      raw.hispanic_latino === null || raw.hispanic_latino === undefined
        ? null
        : Boolean(raw.hispanic_latino),
    sexualOrientation: String(raw.sexual_orientation ?? ""),
  }
}

export function formatEeoValue(key: keyof EeoState, value: EeoState[keyof EeoState]): string {
  if (value === null || value === undefined || value === "") return "—"
  if (typeof value === "boolean") return value ? "Yes" : "No"
  return String(value)
}

export function eeoToDisplayRows(state: EeoState): { label: string; value: string }[] {
  return EEO_FIELDS.map((field) => ({
    label: field.label,
    value: formatEeoValue(field.key, state[field.key]),
  })).filter((row) => row.value !== "—")
}
