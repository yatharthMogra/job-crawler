'use client'

import { Card, CardContent } from '@/components/ui/card'
import { cn } from '@/lib/utils'

interface MetricCardProps {
  title: string
  value: string | number
  subtitle?: string
  className?: string
  valueClassName?: string
  icon?: React.ReactNode
}

export function MetricCard({ title, value, subtitle, className, valueClassName, icon }: MetricCardProps) {
  return (
    <Card className={cn('py-4 border shadow-sm', className)}>
      <CardContent className="p-0 px-4">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">{title}</p>
            <p className={cn('text-2xl font-semibold tabular-nums', valueClassName)}>{value}</p>
            {subtitle && (
              <p className="text-xs text-muted-foreground">{subtitle}</p>
            )}
          </div>
          {icon && (
            <div className="text-muted-foreground">{icon}</div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

interface SummaryStripProps {
  children: React.ReactNode
  className?: string
}

export function SummaryStrip({ children, className }: SummaryStripProps) {
  return (
    <div className={cn('grid grid-cols-2 lg:grid-cols-4 gap-4', className)}>
      {children}
    </div>
  )
}
