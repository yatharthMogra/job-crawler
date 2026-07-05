export const MAX_RESUME_SLOTS = 5

export function sortResumesByUploadedAt<T extends { uploadedAt: string }>(resumes: T[]): T[] {
  return [...resumes].sort(
    (a, b) => new Date(b.uploadedAt).getTime() - new Date(a.uploadedAt).getTime(),
  )
}

/** Labels like "for Google" or "for Meta" mark company-tailored resumes. */
export function isCompanyTailoredLabel(label: string | null | undefined): boolean {
  if (!label?.trim()) return false
  return /^for\s+\S/i.test(label.trim())
}

export function partitionResumes<T extends { displayLabel: string | null }>(resumes: T[]) {
  const general: T[] = []
  const company: T[] = []
  for (const resume of resumes) {
    if (isCompanyTailoredLabel(resume.displayLabel)) {
      company.push(resume)
    } else {
      general.push(resume)
    }
  }
  return { general, company }
}

export function formatResumeFileSize(bytes: number): string {
  if (bytes / 1024 > 1024) return `${(bytes / 1024 / 1024).toFixed(1)} MB`
  return `${Math.round(bytes / 1024)} KB`
}
