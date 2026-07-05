import { BrandLogo } from "@/components/brand-logo"
import { domainFromWebsite, resolveBrandDomain } from "@/lib/brand-logos"

interface CompanyLogoProps {
  company: string
  size?: number
  className?: string
  shape?: "square" | "circle"
  /** Company website URL or hostname for precise logo lookup */
  website?: string | null
  domain?: string | null
}

export function CompanyLogo({
  company,
  size = 32,
  className = "",
  shape = "circle",
  website,
  domain,
}: CompanyLogoProps) {
  const resolvedDomain =
    domain ?? domainFromWebsite(website) ?? resolveBrandDomain(company, "company")

  return (
    <BrandLogo
      name={company}
      size={size}
      variant="company"
      shape={shape}
      className={className}
      domain={resolvedDomain}
    />
  )
}
