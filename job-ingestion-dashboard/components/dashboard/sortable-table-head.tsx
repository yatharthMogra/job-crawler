'use client'

import { ArrowDown, ArrowUp, ArrowUpDown } from 'lucide-react'
import { TableHead } from '@/components/ui/table'
import { cn } from '@/lib/utils'
import type { SortState } from '@/hooks/use-table-sort'

type SortableTableHeadProps = {
  label: string
  columnKey: string
  sort: SortState
  onToggle: (key: string) => void
  className?: string
  align?: 'left' | 'right'
}

export function SortableTableHead({
  label,
  columnKey,
  sort,
  onToggle,
  className,
  align = 'left',
}: SortableTableHeadProps) {
  const active = sort?.key === columnKey
  const Icon = !active ? ArrowUpDown : sort.direction === 'asc' ? ArrowUp : ArrowDown

  return (
    <TableHead className={cn(align === 'right' && 'text-right', className)}>
      <button
        type="button"
        onClick={() => onToggle(columnKey)}
        className={cn(
          'inline-flex items-center gap-1 font-medium hover:text-foreground transition-colors',
          align === 'right' && 'flex-row-reverse',
          active ? 'text-foreground' : 'text-muted-foreground',
        )}
      >
        <span>{label}</span>
        <Icon className="size-3.5 opacity-70" />
      </button>
    </TableHead>
  )
}
