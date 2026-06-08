import type { ReviewState } from "@/lib/profile/profile-data"

export interface Capability {
  name: string
  evidence: string[]
  depth: number
}

export interface CommittedProfile {
  skills: { category: string; names: string[] }[]
  skillCount: number
  experiences: { id: string; title: string; company: string; durationMonths: number; domains: string[]; keywords: string[] }[]
  projects: { id: string; name: string; type: string; domain: string; keywords: string[] }[]
  certifications: { id: string; name: string; issuer: string }[]
  capabilities: Capability[]
  preferences: { label: string; value: string }[]
}

export function buildCommittedProfile(state: ReviewState): CommittedProfile {
  const skills = state.skills.filter((s) => s.status === "approved")
  const experiences = state.experiences.filter((e) => e.status === "approved")
  const projects = state.projects.filter((p) => p.status === "approved")
  const certifications = state.certifications.filter((c) => c.status === "approved")
  const preferences = state.preferences.filter((p) => p.status === "confirmed")

  const skillCategories = Array.from(new Set(skills.map((s) => s.category))).map((category) => ({
    category,
    names: skills.filter((s) => s.category === category).map((s) => s.name),
  }))

  // Derive capabilities from approved evidence keywords + sources.
  const capabilityRules: { name: string; match: string[] }[] = [
    { name: "Backend Engineering", match: ["backend apis", "java", "fastapi", "kafka", "data pipelines", "apis"] },
    { name: "AI Systems", match: ["rag", "llms", "multi-agent systems", "voice ai", "ai product"] },
    { name: "Distributed Systems", match: ["distributed systems", "kafka", "real-time systems", "monitoring"] },
    { name: "Full Stack Development", match: ["react", "next.js", "typescript", "web app"] },
    { name: "Cloud Infrastructure", match: ["aws", "cloud"] },
  ]

  const evidenceItems: { source: string; tokens: string[] }[] = [
    ...experiences.map((e) => ({
      source: e.company,
      tokens: [...e.keywords, ...e.domains].map((t) => t.toLowerCase()),
    })),
    ...projects.map((p) => ({
      source: p.name,
      tokens: [...p.keywords, p.type, p.domain].map((t) => t.toLowerCase()),
    })),
    ...skills.map((s) => ({ source: s.name, tokens: [s.name.toLowerCase(), s.category.toLowerCase()] })),
  ]

  const capabilities: Capability[] = capabilityRules
    .map((rule) => {
      const evidence = new Set<string>()
      evidenceItems.forEach((item) => {
        if (item.tokens.some((tok) => rule.match.some((m) => tok.includes(m) || m.includes(tok)))) {
          evidence.add(item.source)
        }
      })
      return { name: rule.name, evidence: Array.from(evidence), depth: evidence.size }
    })
    .filter((c) => c.depth > 0)
    .sort((a, b) => b.depth - a.depth)

  return {
    skills: skillCategories,
    skillCount: skills.length,
    experiences: experiences.map((e) => ({
      id: e.id,
      title: e.title,
      company: e.company,
      durationMonths: e.durationMonths,
      domains: e.domains,
      keywords: e.keywords,
    })),
    projects: projects.map((p) => ({
      id: p.id,
      name: p.name,
      type: p.type,
      domain: p.domain,
      keywords: p.keywords,
    })),
    certifications: certifications.map((c) => ({ id: c.id, name: c.name, issuer: c.issuer })),
    capabilities,
    preferences: preferences.map((p) => ({ label: p.label, value: p.value })),
  }
}
