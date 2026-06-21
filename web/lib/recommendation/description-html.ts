export function descriptionTextToHtml(text: string | null | undefined): string {
  if (!text) return ""
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
  return `<p>${escaped}</p>`
}
