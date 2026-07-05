const ACCOMPLISHMENT_STARTERS =
  /^(architected|built|developed|designed|implemented|led|managed|created|improved|reduced|increased|delivered|optimized|scaled|migrated|launched|established|automated|streamlined|collaborated|owned|drove|spearheaded|introduced|maintained|deployed)/i

export function isAccomplishmentKeyword(keyword: string): boolean {
  const trimmed = keyword.trim()
  if (!trimmed) return false
  if (trimmed.length >= 40) return true
  if (ACCOMPLISHMENT_STARTERS.test(trimmed)) return true
  const words = trimmed.split(/\s+/)
  return words.length >= 5
}

export function splitExperienceContent(keywords: string[], domains: string[]) {
  const accomplishments: string[] = []
  const technologies = new Set<string>()

  for (const domain of domains) {
    const trimmed = domain.trim()
    if (trimmed) technologies.add(trimmed)
  }

  for (const keyword of keywords) {
    const trimmed = keyword.trim()
    if (!trimmed) continue
    if (isAccomplishmentKeyword(trimmed)) {
      accomplishments.push(trimmed)
    } else {
      technologies.add(trimmed)
    }
  }

  return {
    accomplishments,
    technologies: [...technologies],
  }
}
