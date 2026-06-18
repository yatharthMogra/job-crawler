import { BrandLogo } from "@/components/brand-logo"

interface CompanyLogoProps {
  company: string
  size?: number
  className?: string
  shape?: "square" | "circle"
}

export function CompanyLogo({
  company,
  size = 32,
  className = "",
  shape = "circle",
}: CompanyLogoProps) {
  return (
    <BrandLogo
      name={company}
      size={size}
      variant="company"
      shape={shape}
      className={className}
    />
  )
}
