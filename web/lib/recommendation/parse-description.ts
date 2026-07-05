import type { JobDescriptionSections } from "@/components/job-description-sections"
import { descriptionTextToHtml } from "@/lib/recommendation/description-html"

export interface JobDescriptionSource {
  description_text?: string | null
  description_preview?: string | null
  responsibilities?: string[]
  required_qualifications?: string[]
  preferred_qualifications?: string[]
  benefits?: string[]
}

export interface ResolvedJobDescription extends JobDescriptionSections {
  about: string | null
  fallbackHtml: string
}

type SectionKey = keyof JobDescriptionSections

const SECTION_HEADERS: Record<SectionKey, RegExp[]> = {
  responsibilities: [
    /^responsibilit/i,
    /^what you(?:'|')?ll do/i,
    /^what you will do/i,
    /^the role$/i,
    /^key responsibilit/i,
    /^your impact$/i,
    /^in this role/i,
    /^role overview$/i,
  ],
  required_qualifications: [
    /^required\s+qualifications?/i,
    /^minimum\s+qualifications?/i,
    /^basic\s+qualifications?/i,
    /^must\s+have/i,
    /^requirements?$/i,
    /^qualifications?$/i,
    /^what you(?:'|')?ll need/i,
    /^what we(?:'|')?re looking for/i,
    /^you have$/i,
    /^skills?\s*(?:&|and)\s*experience/i,
  ],
  preferred_qualifications: [
    /^preferred\s+qualifications?/i,
    /^nice\s+to\s+have/i,
    /^bonus\s+points?/i,
    /^desired\s+qualifications?/i,
    /^pluses?$/i,
  ],
  benefits: [
    /^benefits?$/i,
    /^perks?(?:\s+and\s+benefits?)?$/i,
    /^what we offer/i,
    /^compensation(?:\s+and\s+benefits?)?/i,
    /^why join/i,
  ],
}

const ABOUT_HEADERS = [
  /^about(\s+the\s+(role|job|position))?$/i,
  /^overview$/i,
  /^summary$/i,
  /^description$/i,
  /^the opportunity$/i,
  /^position overview$/i,
]

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}

function normalizeBulletLine(line: string): string {
  return line
    .replace(/^[\s•●▪◦\-–—*]+/, "")
    .replace(/^\d+[\.\)]\s*/, "")
    .trim()
}

function expandListItems(items: string[]): string[] {
  const expanded: string[] = []
  for (const item of items) {
    const chunks = item
      .split(/\n+/)
      .map(normalizeBulletLine)
      .filter(Boolean)
    if (chunks.length > 0) {
      expanded.push(...chunks)
    }
  }
  return expanded
}

function dedupeItems(items: string[]): string[] {
  const seen = new Set<string>()
  const result: string[] = []
  for (const item of items) {
    const key = item.trim().toLowerCase()
    if (!key || seen.has(key)) continue
    seen.add(key)
    result.push(item.trim())
  }
  return result
}

function isSentenceLike(item: string): boolean {
  const trimmed = item.trim()
  if (trimmed.length >= 55) return true
  if (/\b(build|design|develop|lead|own|work|collaborate|implement|maintain|create|drive|support|manage|architect|deliver|ensure|help|partner|contribute|analyze|improve|optimize|scale)\b/i.test(trimmed)) {
    return true
  }
  return trimmed.split(/\s+/).length >= 7
}

function cleanResponsibilityItems(items: string[]): string[] {
  const normalized = dedupeItems(expandListItems(items))
  const sentenceLike = normalized.filter(isSentenceLike)
  return sentenceLike.length > 0 ? sentenceLike : normalized
}

function looksLikeSkillOnlyList(items: string[]): boolean {
  if (items.length === 0) return false
  return items.every((item) => !isSentenceLike(item) && item.split(/\s+/).length <= 4)
}

function cleanQualificationItems(items: string[]): string[] {
  return dedupeItems(expandListItems(items)).filter((item) => item.length >= 3)
}

function matchSectionHeader(line: string): SectionKey | "about" | null {
  const cleaned = line.replace(/^#+\s*/, "").replace(/:$/, "").trim()
  if (!cleaned || cleaned.length > 120) return null

  if (ABOUT_HEADERS.some((pattern) => pattern.test(cleaned))) {
    return "about"
  }

  for (const key of Object.keys(SECTION_HEADERS) as SectionKey[]) {
    if (SECTION_HEADERS[key].some((pattern) => pattern.test(cleaned))) {
      return key
    }
  }

  if (
    cleaned.length <= 60 &&
    cleaned === cleaned.toUpperCase() &&
    /[A-Z]/.test(cleaned) &&
    !/[.!?]/.test(cleaned)
  ) {
    const lower = cleaned.toLowerCase()
    if (lower.includes("responsib")) return "responsibilities"
    if (lower.includes("require") || lower.includes("qualif")) return "required_qualifications"
    if (lower.includes("prefer") || lower.includes("nice")) return "preferred_qualifications"
    if (lower.includes("benefit") || lower.includes("perk")) return "benefits"
    if (lower.includes("about") || lower.includes("overview")) return "about"
  }

  return null
}

function parseDescriptionText(text: string): Pick<
  ResolvedJobDescription,
  "about" | "responsibilities" | "required_qualifications" | "preferred_qualifications" | "benefits"
> {
  const lines = text.split(/\r?\n/).map((line) => line.trim())
  const buckets: Record<SectionKey | "about", string[]> = {
    about: [],
    responsibilities: [],
    required_qualifications: [],
    preferred_qualifications: [],
    benefits: [],
  }

  let current: SectionKey | "about" = "about"
  let foundHeader = false

  for (const line of lines) {
    if (!line) continue
    const header = matchSectionHeader(line)
    if (header) {
      current = header
      foundHeader = true
      continue
    }

    const bullet = normalizeBulletLine(line)
    if (!bullet) continue
    buckets[current].push(bullet)
  }

  if (!foundHeader) {
    const nonEmpty = lines.filter(Boolean)
    const bulletLines = nonEmpty
      .map(normalizeBulletLine)
      .filter((line) => /^[\s•●▪◦\-–—*]/.test(line) || /^\d+[\.\)]\s/.test(line))
    if (bulletLines.length > 0) {
      buckets.about = []
      buckets.responsibilities = bulletLines
    } else if (nonEmpty.length > 0) {
      const firstParagraph: string[] = []
      const remainder: string[] = []
      let hitBreak = false
      for (const line of nonEmpty) {
        const normalized = normalizeBulletLine(line)
        if (!hitBreak && (normalized.length < 120 || firstParagraph.length === 0)) {
          firstParagraph.push(normalized)
          if (normalized.endsWith(".") && firstParagraph.join(" ").length >= 80) {
            hitBreak = true
          }
        } else {
          remainder.push(normalized)
        }
      }
      buckets.about = firstParagraph
      buckets.responsibilities = remainder
    }
  }

  const about = buckets.about.join(" ").replace(/\s+/g, " ").trim()

  return {
    about: about || null,
    responsibilities: cleanResponsibilityItems(buckets.responsibilities),
    required_qualifications: cleanQualificationItems(buckets.required_qualifications),
    preferred_qualifications: cleanQualificationItems(buckets.preferred_qualifications),
    benefits: cleanQualificationItems(buckets.benefits),
  }
}

function hasStructuredSections(sections: JobDescriptionSections): boolean {
  return (
    sections.responsibilities.length > 0 ||
    sections.required_qualifications.length > 0 ||
    sections.preferred_qualifications.length > 0 ||
    sections.benefits.length > 0
  )
}

function pickAbout(
  preview: string | null | undefined,
  parsedAbout: string | null,
  descriptionText: string | null | undefined,
): string | null {
  const previewText = preview?.trim()
  if (previewText && previewText.length >= 40) return previewText

  if (parsedAbout && parsedAbout.length >= 40) return parsedAbout

  const text = descriptionText?.trim()
  if (!text) return null

  const paragraph = text
    .split(/\n\s*\n/)
    .map((chunk) => chunk.replace(/\s+/g, " ").trim())
    .find((chunk) => chunk.length >= 40 && !matchSectionHeader(chunk.split("\n")[0] ?? ""))

  return paragraph ?? null
}

export function resolveJobDescription(source: JobDescriptionSource): ResolvedJobDescription {
  const fromApi: JobDescriptionSections = {
    responsibilities: cleanResponsibilityItems(source.responsibilities ?? []),
    required_qualifications: cleanQualificationItems(source.required_qualifications ?? []),
    preferred_qualifications: cleanQualificationItems(source.preferred_qualifications ?? []),
    benefits: cleanQualificationItems(source.benefits ?? []),
  }

  const parsed = source.description_text?.trim()
    ? parseDescriptionText(source.description_text)
    : {
        about: null,
        responsibilities: [],
        required_qualifications: [],
        preferred_qualifications: [],
        benefits: [],
      }

  const merged: JobDescriptionSections = {
    responsibilities:
      fromApi.responsibilities.length > 0 && !looksLikeSkillOnlyList(fromApi.responsibilities)
        ? fromApi.responsibilities
        : parsed.responsibilities.length > 0
          ? parsed.responsibilities
          : fromApi.responsibilities,
    required_qualifications:
      fromApi.required_qualifications.length > 0
        ? fromApi.required_qualifications
        : parsed.required_qualifications,
    preferred_qualifications:
      fromApi.preferred_qualifications.length > 0
        ? fromApi.preferred_qualifications
        : parsed.preferred_qualifications,
    benefits: fromApi.benefits.length > 0 ? fromApi.benefits : parsed.benefits,
  }

  const about = pickAbout(source.description_preview, parsed.about, source.description_text)
  const structured = hasStructuredSections(merged)

  return {
    about,
    ...merged,
    fallbackHtml: structured ? "" : descriptionTextToHtml(source.description_text),
  }
}
