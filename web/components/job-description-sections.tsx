export interface JobDescriptionSections {
  responsibilities: string[]
  required_qualifications: string[]
  preferred_qualifications: string[]
  benefits: string[]
}

export function hasDescriptionSections(sections: JobDescriptionSections): boolean {
  return (
    sections.responsibilities.length > 0
    || sections.required_qualifications.length > 0
    || sections.preferred_qualifications.length > 0
    || sections.benefits.length > 0
  )
}

function normalizeMatch(value: string): string {
  return value.trim().toLowerCase()
}

function isMatched(label: string, matchedLabels: Set<string>): boolean {
  const normalized = normalizeMatch(label)
  if (matchedLabels.has(normalized)) return true
  for (const match of matchedLabels) {
    if (normalized.includes(match) || match.includes(normalized)) return true
  }
  return false
}

function BulletList({
  items,
  matchedLabels,
}: {
  items: string[]
  matchedLabels: Set<string>
}) {
  if (items.length === 0) return null
  return (
    <ul>
      {items.map((item) => (
        <li
          key={item}
          className={
            isMatched(item, matchedLabels)
              ? "rounded-sm border border-emerald-500/30 bg-emerald-500/10 px-1 -mx-1"
              : undefined
          }
        >
          {item}
        </li>
      ))}
    </ul>
  )
}

export function JobDescriptionSectionsView({
  sections,
  matchedLabels = new Set<string>(),
}: {
  sections: JobDescriptionSections
  matchedLabels?: Set<string>
}) {
  if (!hasDescriptionSections(sections)) return null

  const blocks: { title: string; items: string[] }[] = [
    { title: "Responsibilities", items: sections.responsibilities },
    { title: "Required Qualifications", items: sections.required_qualifications },
    { title: "Preferred Qualifications", items: sections.preferred_qualifications },
    { title: "Benefits", items: sections.benefits },
  ]

  return (
    <div className="job-description space-y-4">
      {blocks.map(
        (block) =>
          block.items.length > 0 && (
            <section key={block.title}>
              <h4>{block.title}</h4>
              <BulletList items={block.items} matchedLabels={matchedLabels} />
            </section>
          ),
      )}
    </div>
  )
}

export function buildMatchedLabels(
  matchReasons: string[],
  profileSkillNames: string[],
): Set<string> {
  const labels = new Set<string>()
  for (const reason of matchReasons) {
    labels.add(normalizeMatch(reason))
  }
  for (const skill of profileSkillNames) {
    labels.add(normalizeMatch(skill))
  }
  return labels
}
