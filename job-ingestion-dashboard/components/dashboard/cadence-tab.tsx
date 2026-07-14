'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Building2, AlertTriangle, Timer, TrendingUp, ChevronDown } from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { SortableTableHead } from './sortable-table-head'
import { useTableSort } from '@/hooks/use-table-sort'
import { cn } from '@/lib/utils'
import {
  getCadenceStats,
  type CadenceCompany,
  type CadenceHealth,
  type CadenceStats,
} from '@/lib/api'

type AggView = 'source' | 'tier' | 'source_tier' | 'company'
type SortBy = 'drift_desc' | 'never_first' | 'slowest_actual' | 'alpha'

const ALL_TIERS = [1, 2, 3] as const


const HEALTH_META: Record<
  CadenceHealth,
  { label: string; className: string; barClassName: string }
> = {
  on_target: {
    label: 'On target',
    className: 'bg-emerald-100 text-emerald-700 border-emerald-200',
    barClassName: 'bg-emerald-600',
  },
  drifting: {
    label: 'Drifting',
    className: 'bg-amber-100 text-amber-700 border-amber-200',
    barClassName: 'bg-amber-600',
  },
  behind: {
    label: 'Behind',
    className: 'bg-red-100 text-red-700 border-red-200',
    barClassName: 'bg-red-600',
  },
  never_fetched: {
    label: 'Never fetched',
    className: 'bg-violet-100 text-violet-700 border-violet-200',
    barClassName: 'bg-violet-600',
  },
}

function formatHours(hours: number | null | undefined): string {
  if (hours == null) return '—'
  if (hours < 1) return `${Math.round(hours * 60)}m`
  if (hours < 10) return `${Math.round(hours * 10) / 10}h`
  return `${Math.round(hours)}h`
}

function formatLastFetch(date: Date | null): string {
  if (!date) return 'Never'
  const hours = (Date.now() - date.getTime()) / 3600000
  if (hours < 1) return `${Math.round(hours * 60)}m ago`
  if (hours < 48) return `${Math.round(hours)}h ago`
  return `${Math.round(hours / 24)}d ago`
}

function formatDrift(actual: number | null, target: number): string {
  if (actual == null || target <= 0) return '—'
  const pct = Math.round((actual / target - 1) * 100)
  return `${pct >= 0 ? '+' : ''}${pct}%`
}

function formatPlatform(platform: string): string {
  return platform
    .split('_')
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}

function barPercents(target: number, actual: number | null): { actualPct: number; targetPct: number } {
  const barMax = Math.max(target, actual || 0) * 1.3 || 1
  return {
    actualPct: actual != null ? Math.min(100, (actual / barMax) * 100) : 0,
    targetPct: Math.min(100, (target / barMax) * 100),
  }
}

function CadenceBar({
  target,
  actual,
  health,
}: {
  target: number
  actual: number | null
  health: CadenceHealth
}) {
  const { actualPct, targetPct } = barPercents(target, actual)
  return (
    <div className="relative h-2 w-40 rounded bg-muted">
      <div
        className={cn('absolute top-0 left-0 h-2 rounded', HEALTH_META[health].barClassName)}
        style={{ width: `${actualPct}%` }}
      />
      <div
        className="absolute top-[-2px] h-3 w-0.5 bg-foreground"
        style={{ left: `${targetPct}%` }}
      />
    </div>
  )
}

function HealthBadge({ health }: { health: CadenceHealth }) {
  const meta = HEALTH_META[health]
  return (
    <Badge variant="outline" className={meta.className}>
      {meta.label}
    </Badge>
  )
}

type AggRow = {
  key: string
  label: string
  count: number
  avgTarget: number
  avgActual: number | null
  ratio: number | null
  health: CadenceHealth
}

function aggregate(
  rows: CadenceCompany[],
  keyFn: (c: CadenceCompany) => string,
  labelFn: (c: CadenceCompany) => string,
  orderKeys?: Array<string | number>,
): AggRow[] {
  const map = new Map<string, { key: string; label: string; companies: CadenceCompany[] }>()
  for (const company of rows) {
    const key = keyFn(company)
    if (!map.has(key)) map.set(key, { key, label: labelFn(company), companies: [] })
    map.get(key)!.companies.push(company)
  }

  let arr: AggRow[] = Array.from(map.values()).map((group) => {
    const withActual = group.companies.filter((c) => c.actualCadenceHours != null)
    const avgActual =
      withActual.length > 0
        ? withActual.reduce((sum, c) => sum + (c.actualCadenceHours as number), 0) / withActual.length
        : null
    const avgTarget =
      group.companies.reduce((sum, c) => sum + c.targetCadenceHours, 0) / group.companies.length
    const ratio = avgActual != null && avgTarget > 0 ? avgActual / avgTarget : null
    let health: CadenceHealth
    if (avgActual == null) health = 'never_fetched'
    else if (ratio != null && ratio <= 1.1) health = 'on_target'
    else if (ratio != null && ratio <= 1.4) health = 'drifting'
    else health = 'behind'
    return {
      key: group.key,
      label: group.label,
      count: group.companies.length,
      avgTarget,
      avgActual,
      ratio,
      health,
    }
  })

  if (orderKeys) {
    arr.sort(
      (a, b) =>
        orderKeys.indexOf(a.key) - orderKeys.indexOf(b.key) || a.label.localeCompare(b.label),
    )
  } else {
    arr.sort((a, b) => a.label.localeCompare(b.label))
  }
  return arr
}

function sortCompanies(list: CadenceCompany[], sortBy: SortBy): CadenceCompany[] {
  const arr = [...list]
  const ratio = (c: CadenceCompany) =>
    c.actualCadenceHours == null || c.targetCadenceHours <= 0
      ? Number.POSITIVE_INFINITY
      : c.actualCadenceHours / c.targetCadenceHours

  if (sortBy === 'drift_desc') arr.sort((a, b) => ratio(b) - ratio(a))
  else if (sortBy === 'never_first')
    arr.sort(
      (a, b) =>
        (a.actualCadenceHours == null ? -1 : 1) - (b.actualCadenceHours == null ? -1 : 1) ||
        a.name.localeCompare(b.name),
    )
  else if (sortBy === 'slowest_actual')
    arr.sort((a, b) => (b.actualCadenceHours ?? -1) - (a.actualCadenceHours ?? -1))
  else arr.sort((a, b) => a.name.localeCompare(b.name))
  return arr
}

function toggleInList<T>(list: T[], value: T, allValues: readonly T[]): T[] {
  const exists = list.includes(value)
  if (exists) {
    const next = list.filter((item) => item !== value)
    // Keep at least one selection so the table doesn't go blank accidentally.
    return next.length > 0 ? next : list
  }
  const next = [...list, value]
  return allValues.filter((item) => next.includes(item))
}

function MultiFilterDropdown<T extends string | number>({
  label,
  options,
  selected,
  onToggle,
  onSelectAll,
  formatOption,
}: {
  label: string
  options: readonly T[]
  selected: T[]
  onToggle: (value: T) => void
  onSelectAll: () => void
  formatOption: (value: T) => string
}) {
  const allSelected = options.length > 0 && selected.length === options.length
  const triggerLabel = allSelected
    ? `All ${label.toLowerCase()}`
    : selected.length === 1
      ? formatOption(selected[0])
      : `${selected.length} ${label.toLowerCase()}`

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="min-w-[150px] justify-between font-normal">
          <span className="truncate">{triggerLabel}</span>
          <ChevronDown className="size-4 opacity-60" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>{label}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuCheckboxItem
          checked={allSelected}
          onCheckedChange={(checked) => {
            if (checked) onSelectAll()
          }}
          onSelect={(e) => e.preventDefault()}
        >
          All {label.toLowerCase()}
        </DropdownMenuCheckboxItem>
        <DropdownMenuSeparator />
        {options.map((option) => (
          <DropdownMenuCheckboxItem
            key={String(option)}
            checked={selected.includes(option)}
            onCheckedChange={() => onToggle(option)}
            onSelect={(e) => e.preventDefault()}
          >
            {formatOption(option)}
          </DropdownMenuCheckboxItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export function CadenceTab() {
  const [stats, setStats] = useState<CadenceStats | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([])
  const [selectedTiers, setSelectedTiers] = useState<number[]>([...ALL_TIERS])
  const [view, setView] = useState<AggView>('source_tier')
  const [search, setSearch] = useState('')
  const [healthFilter, setHealthFilter] = useState<CadenceHealth | 'all'>('all')
  const [sortBy, setSortBy] = useState<SortBy>('drift_desc')

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getCadenceStats(false)
        setStats(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load cadence data')
      }
    }
    void load()
  }, [])

  const platforms = useMemo(() => {
    if (!stats) return []
    return Array.from(new Set(stats.companies.map((c) => c.platform))).sort()
  }, [stats])

  // Default: all sources selected once catalog loads; keep selection if still valid.
  useEffect(() => {
    if (platforms.length === 0) return
    setSelectedPlatforms((prev) => {
      if (prev.length === 0) return platforms
      const kept = prev.filter((p) => platforms.includes(p))
      return kept.length > 0 ? kept : platforms
    })
  }, [platforms])

  const filtered = useMemo(() => {
    if (!stats) return []
    const platformSet = new Set(selectedPlatforms)
    const tierSet = new Set(selectedTiers)
    return stats.companies.filter((c) => {
      if (platformSet.size > 0 && !platformSet.has(c.platform)) return false
      if (tierSet.size > 0 && !tierSet.has(c.tier)) return false
      return true
    })
  }, [stats, selectedPlatforms, selectedTiers])

  const summary = useMemo(() => {
    const withActual = filtered.filter(
      (c) => c.actualCadenceHours != null && c.targetCadenceHours > 0,
    )
    const avgDriftPct =
      withActual.length > 0
        ? withActual.reduce(
            (sum, c) => sum + ((c.actualCadenceHours as number) / c.targetCadenceHours - 1) * 100,
            0,
          ) / withActual.length
        : 0
    return {
      total: filtered.length,
      neverFetched: filtered.filter((c) => c.health === 'never_fetched').length,
      behind: filtered.filter((c) => c.health === 'behind').length,
      avgDriftPct,
    }
  }, [filtered])

  const selectedPlatformOrder = useMemo(
    () => platforms.filter((p) => selectedPlatforms.includes(p)),
    [platforms, selectedPlatforms],
  )
  const selectedTierOrdered = useMemo(
    () => ALL_TIERS.filter((t) => selectedTiers.includes(t)),
    [selectedTiers],
  )

  const aggRows = useMemo(() => {
    if (view === 'source') {
      return aggregate(
        filtered,
        (c) => c.platform,
        (c) => formatPlatform(c.platform),
        selectedPlatformOrder,
      )
    }
    if (view === 'tier') {
      return aggregate(
        filtered,
        (c) => String(c.tier),
        (c) => `Tier ${c.tier}`,
        selectedTierOrdered.map(String),
      )
    }
    if (view === 'source_tier') {
      const orderKeys = selectedPlatformOrder.flatMap((p) =>
        selectedTierOrdered.map((t) => `${p}|${t}`),
      )
      return aggregate(
        filtered,
        (c) => `${c.platform}|${c.tier}`,
        (c) => `${formatPlatform(c.platform)} — Tier ${c.tier}`,
        orderKeys,
      )
    }
    return []
  }, [filtered, view, selectedPlatformOrder, selectedTierOrdered])

  const companyRows = useMemo(() => {
    let list = filtered
    if (healthFilter !== 'all') list = list.filter((c) => c.health === healthFilter)
    if (search.trim()) {
      const q = search.trim().toLowerCase()
      list = list.filter((c) => c.name.toLowerCase().includes(q))
    }
    return sortCompanies(list, sortBy)
  }, [filtered, healthFilter, search, sortBy])

  const avgDriftStr = `${summary.avgDriftPct >= 0 ? '+' : ''}${Math.round(summary.avgDriftPct)}%`

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-foreground">Ingestion Cadence</h2>
          <p className="text-sm text-muted-foreground">
            Target vs. actual fetch cadence across the catalog
            {stats ? ` · tick ${stats.tickMinutes}m · batch cap ${stats.batchCap}` : ''}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <MultiFilterDropdown
            label="Sources"
            options={platforms}
            selected={selectedPlatforms}
            onToggle={(platform) =>
              setSelectedPlatforms((prev) => toggleInList(prev, platform, platforms))
            }
            onSelectAll={() => setSelectedPlatforms(platforms)}
            formatOption={formatPlatform}
          />
          <MultiFilterDropdown
            label="Tiers"
            options={ALL_TIERS}
            selected={selectedTiers}
            onToggle={(tier) =>
              setSelectedTiers((prev) => toggleInList(prev, tier, ALL_TIERS))
            }
            onSelectAll={() => setSelectedTiers([...ALL_TIERS])}
            formatOption={(tier) => `Tier ${tier}`}
          />
        </div>
      </div>

      {error && (
        <Card className="border-destructive/40">
          <CardContent className="py-4 text-sm text-destructive">{error}</CardContent>
        </Card>
      )}

      <SummaryStrip>
        <MetricCard
          title="Active companies"
          value={summary.total}
          icon={<Building2 className="size-5" />}
        />
        <MetricCard
          title="Never fetched"
          value={summary.neverFetched}
          valueClassName={summary.neverFetched > 0 ? 'text-violet-700' : ''}
          icon={<Timer className="size-5" />}
        />
        <MetricCard
          title="Behind target"
          value={summary.behind}
          valueClassName={summary.behind > 0 ? 'text-destructive' : ''}
          icon={<AlertTriangle className="size-5" />}
        />
        <MetricCard
          title="Avg. cadence drift"
          value={avgDriftStr}
          icon={<TrendingUp className="size-5" />}
        />
      </SummaryStrip>

      <Tabs value={view} onValueChange={(value) => setView(value as AggView)}>
        <TabsList className="bg-card border border-border shadow-sm">
          <TabsTrigger value="source">By Source</TabsTrigger>
          <TabsTrigger value="tier">By Tier</TabsTrigger>
          <TabsTrigger value="source_tier">Source + Tier</TabsTrigger>
          <TabsTrigger value="company">By Company</TabsTrigger>
        </TabsList>

        <TabsContent value="source" className="mt-4">
          <AggTable rows={aggRows} colLabel="Source" />
        </TabsContent>
        <TabsContent value="tier" className="mt-4">
          <AggTable rows={aggRows} colLabel="Tier" />
        </TabsContent>
        <TabsContent value="source_tier" className="mt-4">
          <AggTable rows={aggRows} colLabel="Source + Tier" />
        </TabsContent>
        <TabsContent value="company" className="mt-4 space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <Input
              placeholder="Search companies…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-[220px]"
            />
            <Select value={sortBy} onValueChange={(value) => setSortBy(value as SortBy)}>
              <SelectTrigger className="w-[220px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="drift_desc">Sort: worst drift first</SelectItem>
                <SelectItem value="never_first">Sort: never fetched first</SelectItem>
                <SelectItem value="slowest_actual">Sort: slowest actual cadence</SelectItem>
                <SelectItem value="alpha">Sort: alphabetical</SelectItem>
              </SelectContent>
            </Select>
            <div className="ml-auto flex flex-wrap gap-2">
              {(
                [
                  ['all', 'All'],
                  ['on_target', 'On target'],
                  ['drifting', 'Drifting'],
                  ['behind', 'Behind'],
                  ['never_fetched', 'Never fetched'],
                ] as const
              ).map(([key, label]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setHealthFilter(key)}
                  className={cn(
                    'rounded-full border px-3 py-1 text-xs font-medium transition-colors',
                    healthFilter === key
                      ? 'border-foreground bg-foreground text-background'
                      : 'border-border bg-card text-muted-foreground hover:text-foreground',
                  )}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          <CompanyTable rows={companyRows} />
        </TabsContent>
      </Tabs>
    </div>
  )
}

function AggTable({ rows, colLabel }: { rows: AggRow[]; colLabel: string }) {
  const getters = useMemo(
    () => ({
      label: (r: AggRow) => r.label,
      count: (r: AggRow) => r.count,
      avgTarget: (r: AggRow) => r.avgTarget,
      avgActual: (r: AggRow) => r.avgActual,
      ratio: (r: AggRow) => r.ratio,
      health: (r: AggRow) => r.health,
    }),
    [],
  )
  const { sortedRows, sort, toggleSort } = useTableSort(rows, getters)

  return (
    <Card>
      <CardHeader>
        <CardTitle>{colLabel}</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <SortableTableHead label={colLabel} columnKey="label" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Companies" columnKey="count" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Avg. target" columnKey="avgTarget" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Avg. actual" columnKey="avgActual" sort={sort} onToggle={toggleSort} />
              <TableHead>Target vs. actual</TableHead>
              <SortableTableHead label="Ratio" columnKey="ratio" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Health" columnKey="health" sort={sort} onToggle={toggleSort} />
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedRows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-muted-foreground py-10">
                  No companies match the current filters.
                </TableCell>
              </TableRow>
            ) : (
              sortedRows.map((row) => (
                <TableRow key={row.key}>
                  <TableCell className="font-medium">{row.label}</TableCell>
                  <TableCell>{row.count}</TableCell>
                  <TableCell>{formatHours(row.avgTarget)}</TableCell>
                  <TableCell>{formatHours(row.avgActual)}</TableCell>
                  <TableCell>
                    <CadenceBar target={row.avgTarget} actual={row.avgActual} health={row.health} />
                  </TableCell>
                  <TableCell>
                    {row.ratio != null ? `${row.ratio.toFixed(2)}×` : '—'}
                  </TableCell>
                  <TableCell>
                    <HealthBadge health={row.health} />
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

function CompanyTable({ rows }: { rows: CadenceCompany[] }) {
  const getters = useMemo(
    () => ({
      name: (r: CadenceCompany) => r.name,
      platform: (r: CadenceCompany) => r.platform,
      tier: (r: CadenceCompany) => r.tier,
      target: (r: CadenceCompany) => r.targetCadenceHours,
      actual: (r: CadenceCompany) => r.actualCadenceHours,
      drift: (r: CadenceCompany) => r.driftRatio,
      health: (r: CadenceCompany) => r.health,
      lastFetch: (r: CadenceCompany) => r.lastSuccessfulFetchAt,
      failures: (r: CadenceCompany) => r.consecutiveFailures,
    }),
    [],
  )
  const { sortedRows, sort, toggleSort } = useTableSort(rows, getters)

  return (
    <Card>
      <CardContent className="pt-6">
        <Table>
          <TableHeader>
            <TableRow>
              <SortableTableHead label="Company" columnKey="name" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Platform" columnKey="platform" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Tier" columnKey="tier" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Target" columnKey="target" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Actual" columnKey="actual" sort={sort} onToggle={toggleSort} />
              <TableHead>Target vs. actual</TableHead>
              <SortableTableHead label="Drift" columnKey="drift" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Health" columnKey="health" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Last fetch" columnKey="lastFetch" sort={sort} onToggle={toggleSort} />
              <SortableTableHead label="Failures" columnKey="failures" sort={sort} onToggle={toggleSort} />
            </TableRow>
          </TableHeader>
          <TableBody>
            {sortedRows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={10} className="text-center text-muted-foreground py-10">
                  No companies match the current filters.
                </TableCell>
              </TableRow>
            ) : (
              sortedRows.map((row) => (
                <TableRow key={row.id}>
                  <TableCell className="font-medium whitespace-nowrap">{row.name}</TableCell>
                  <TableCell>{formatPlatform(row.platform)}</TableCell>
                  <TableCell>Tier {row.tier}</TableCell>
                  <TableCell>{formatHours(row.targetCadenceHours)}</TableCell>
                  <TableCell>{formatHours(row.actualCadenceHours)}</TableCell>
                  <TableCell>
                    <CadenceBar
                      target={row.targetCadenceHours}
                      actual={row.actualCadenceHours}
                      health={row.health}
                    />
                  </TableCell>
                  <TableCell>{formatDrift(row.actualCadenceHours, row.targetCadenceHours)}</TableCell>
                  <TableCell>
                    <HealthBadge health={row.health} />
                  </TableCell>
                  <TableCell className="text-muted-foreground whitespace-nowrap">
                    {formatLastFetch(row.lastSuccessfulFetchAt)}
                  </TableCell>
                  <TableCell>
                    {row.consecutiveFailures > 0 ? row.consecutiveFailures : '—'}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
