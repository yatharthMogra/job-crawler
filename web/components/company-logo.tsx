interface CompanyLogoProps {
  company: string
  size?: number
  className?: string
}

const COLORS = [
  "bg-primary",
  "bg-indigo-600",
  "bg-emerald-700",
  "bg-rose-600",
  "bg-amber-600",
  "bg-sky-700",
  "bg-violet-700",
  "bg-teal-700",
]

function colorFor(company: string) {
  let hash = 0
  for (let i = 0; i < company.length; i++) hash = company.charCodeAt(i) + ((hash << 5) - hash)
  return COLORS[Math.abs(hash) % COLORS.length]
}

export function CompanyLogo({ company, size = 32, className = "" }: CompanyLogoProps) {
  return (
    <div
      className={`flex shrink-0 items-center justify-center rounded-md font-semibold text-white ${colorFor(company)} ${className}`}
      style={{ width: size, height: size, fontSize: size * 0.42 }}
      aria-hidden="true"
    >
      {company.charAt(0).toUpperCase()}
    </div>
  )
}
