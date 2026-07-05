export function descriptionTextToHtml(text: string | null | undefined): string {
  if (!text?.trim()) return ""

  const normalized = text.replace(/\r\n/g, "\n").trim()
  const blocks = normalized.split(/\n\s*\n+/)
  const parts: string[] = []

  for (const block of blocks) {
    const lines = block
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean)
    if (lines.length === 0) continue

    const bulletLines = lines.filter(
      (line) => /^[\s•●▪◦\-–—*]/.test(line) || /^\d+[\.\)]\s/.test(line),
    )

    if (bulletLines.length >= 2 || (bulletLines.length === 1 && lines.length === 1)) {
      const items = lines
        .map((line) =>
          line
            .replace(/^[\s•●▪◦\-–—*]+/, "")
            .replace(/^\d+[\.\)]\s*/, "")
            .trim(),
        )
        .filter(Boolean)
      if (items.length > 0) {
        parts.push(`<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`)
        continue
      }
    }

    const paragraph = lines.join(" ").replace(/\s+/g, " ")
    if (paragraph) {
      parts.push(`<p>${escapeHtml(paragraph)}</p>`)
    }
  }

  return parts.join("")
}

function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
}
