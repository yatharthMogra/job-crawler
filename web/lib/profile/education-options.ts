export const DEGREE_OPTIONS = [
  "BS Computer Science",
  "BA Computer Science",
  "B.Tech Computer Science",
  "B.Tech Electrical Engineering",
  "B.Tech Mechanical Engineering",
  "MS Computer Science",
  "MS Data Science",
  "MS Electrical Engineering",
  "MBA",
  "PhD Computer Science",
  "PhD Machine Learning",
  "Other",
] as const

export const UNIVERSITY_OPTIONS = [
  "NYU",
  "New York University",
  "MIT",
  "Stanford University",
  "Carnegie Mellon University",
  "Columbia University",
  "UC Berkeley",
  "Harvard University",
  "IIT Mandi",
  "Indian Institute of Technology Mandi",
  "Georgia Tech",
  "University of Michigan",
  "Cornell University",
  "University of Washington",
  "Other",
] as const

const MONTHS = [
  { value: "01", label: "January" },
  { value: "02", label: "February" },
  { value: "03", label: "March" },
  { value: "04", label: "April" },
  { value: "05", label: "May" },
  { value: "06", label: "June" },
  { value: "07", label: "July" },
  { value: "08", label: "August" },
  { value: "09", label: "September" },
  { value: "10", label: "October" },
  { value: "11", label: "November" },
  { value: "12", label: "December" },
] as const

function buildGraduationDateOptions(): { value: string; label: string }[] {
  const options: { value: string; label: string }[] = []
  const currentYear = new Date().getFullYear()
  for (let year = currentYear + 4; year >= currentYear - 15; year -= 1) {
    for (const month of MONTHS) {
      options.push({
        value: `${year}-${month.value}`,
        label: `${month.label} ${year}`,
      })
    }
  }
  return options
}

export const GRADUATION_DATE_OPTIONS = buildGraduationDateOptions()

export function graduationDateLabel(value: string): string {
  const match = GRADUATION_DATE_OPTIONS.find((opt) => opt.value === value)
  if (match) return match.label
  const [year, month] = value.split("-")
  if (year && month) {
    const monthEntry = MONTHS.find((m) => m.value === month)
    return monthEntry ? `${monthEntry.label} ${year}` : value
  }
  return value
}
