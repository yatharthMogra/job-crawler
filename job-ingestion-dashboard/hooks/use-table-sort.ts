'use client'

import { useMemo, useState, useCallback } from 'react'

export type SortDirection = 'asc' | 'desc'
export type SortState = { key: string; direction: SortDirection } | null

export type SortValue = string | number | boolean | Date | null | undefined

function compareValues(a: SortValue, b: SortValue, direction: SortDirection): number {
  const mul = direction === 'asc' ? 1 : -1
  const aNull = a == null || a === ''
  const bNull = b == null || b === ''
  if (aNull && bNull) return 0
  if (aNull) return 1
  if (bNull) return -1

  if (a instanceof Date && b instanceof Date) {
    return (a.getTime() - b.getTime()) * mul
  }
  if (typeof a === 'number' && typeof b === 'number') {
    return (a - b) * mul
  }
  if (typeof a === 'boolean' && typeof b === 'boolean') {
    return (Number(a) - Number(b)) * mul
  }
  return String(a).localeCompare(String(b), undefined, { numeric: true, sensitivity: 'base' }) * mul
}

export function useTableSort<T>(
  rows: T[],
  getters: Record<string, (row: T) => SortValue>,
  defaultOrder?: (a: T, b: T) => number,
) {
  const [sort, setSort] = useState<SortState>(null)

  const toggleSort = useCallback((key: string) => {
    setSort((prev) => {
      if (!prev || prev.key !== key) return { key, direction: 'asc' }
      if (prev.direction === 'asc') return { key, direction: 'desc' }
      return null
    })
  }, [])

  const sortedRows = useMemo(() => {
    const copy = [...rows]
    if (!sort) {
      if (defaultOrder) copy.sort(defaultOrder)
      return copy
    }
    const getter = getters[sort.key]
    if (!getter) return copy
    copy.sort((a, b) => compareValues(getter(a), getter(b), sort.direction))
    return copy
  }, [rows, sort, getters, defaultOrder])

  return { sortedRows, sort, toggleSort }
}
