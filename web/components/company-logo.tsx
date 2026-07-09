import { BrandLogo } from "@/components/brand-logo"

interface CompanyLogoProps {
  company: string
  size?: number
  className?: string
  shape?: "square" | "circle"
  /** Stored logo URL from API (cloud storage). */
  logoUrl?: string | null
}

export function CompanyLogo({
  company,
  size = 32,
  className = "",
  shape = "circle",
  logoUrl,
}: CompanyLogoProps) {
  return (
    <BrandLogo
      name={company}
      size={size}
      variant="company"
      shape={shape}
      className={className}
      logoUrl={logoUrl}
    />
  )
}
