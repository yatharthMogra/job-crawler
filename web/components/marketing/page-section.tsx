import { cn } from "@/lib/utils"

interface PageSectionProps {
  children: React.ReactNode
  className?: string
  id?: string
}

export function PageSection({ children, className, id }: PageSectionProps) {
  return (
    <section id={id} className={cn("mx-auto max-w-7xl px-6 py-16 sm:py-20", className)}>
      {children}
    </section>
  )
}
