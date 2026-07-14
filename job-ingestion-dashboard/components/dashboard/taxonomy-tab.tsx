'use client'

import { Fragment, useCallback, useEffect, useState } from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { ChevronDown, Layers, RefreshCw, AlertTriangle, CheckCircle2 } from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { SortableTableHead } from './sortable-table-head'
import { useTableSort } from '@/hooks/use-table-sort'
import {
  getTaxonomyHealth,
  setTaxonomyDomainAcknowledged,
  type TaxonomyGroupBy,
  type TaxonomyHealthResponse,
} from '@/lib/api'
import { cn } from '@/lib/utils'
import { formatNumber } from '@/lib/dashboard-utils'

const THRESHOLD_PCT = 10

type TaxonomyRow = TaxonomyHealthResponse['domains'][number]

function pctColor(pct: number, flagged: boolean): string {
  if (!flagged) return 'text-green-600'
  if (pct >= 50) return 'text-red-600'
  return 'text-amber-600'
}

function PctBadge({ pct, flagged }: { pct: number; flagged: boolean }) {
  return (
    <span className={cn('font-semibold tabular-nums', pctColor(pct, flagged))}>
      {pct.toFixed(1)}%
    </span>
  )
}

const taxonomyGetters = {
  key: (row: TaxonomyRow) => row.domain,
  total: (row: TaxonomyRow) => row.total,
  no_pool: (row: TaxonomyRow) => row.no_pool,
  no_pool_pct: (row: TaxonomyRow) => row.no_pool_pct,
  status: (row: TaxonomyRow) =>
    row.needs_review ? 2 : row.acknowledged && row.flagged ? 1 : 0,
}

export function TaxonomyTab() {
  const [groupBy, setGroupBy] = useState<TaxonomyGroupBy>('domain')
  const [data, setData] = useState<TaxonomyHealthResponse | null>(null)
  const [expanded, setExpanded] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async (nextGroupBy: TaxonomyGroupBy = groupBy) => {
    setLoading(true)
    setError(null)
    try {
      const response = await getTaxonomyHealth(nextGroupBy)
      setData(response)
      setExpanded(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load taxonomy health')
    } finally {
      setLoading(false)
    }
  }, [groupBy])

  useEffect(() => {
    void load(groupBy)
  }, [groupBy, load])

  const rows = data?.domains ?? []
  const { sortedRows, sort, toggleSort } = useTableSort(rows, taxonomyGetters)

  const handleGroupByChange = (value: string) => {
    setGroupBy(value as TaxonomyGroupBy)
  }

  if (loading && !data) {
    return <p className="text-sm text-muted-foreground">Loading taxonomy health…</p>
  }

  if (error && !data) {
    return (
      <Card className="border-destructive/50">
        <CardContent className="pt-6">
          <p className="text-sm text-destructive">{error}</p>
          <Button variant="outline" size="sm" className="mt-3" onClick={() => void load()}>
            Retry
          </Button>
        </CardContent>
      </Card>
    )
  }

  if (!data) return null

  const needsReviewCount = data.domains_needing_review
  const groupLabel = groupBy === 'role' ? 'Role' : 'Domain'
  const groupsLabel = groupBy === 'role' ? 'Roles' : 'Domains'

  const toggleAcknowledged = async (key: string, acknowledged: boolean) => {
    try {
      const response = await setTaxonomyDomainAcknowledged(key, acknowledged, groupBy)
      setData(response)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update acknowledgement')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-muted-foreground">
          <Layers className="size-4" />
          <span className="text-sm">
            No-pool rate by job {groupBy === 'role' ? 'role' : 'domain'} (enriched active jobs)
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Select value={groupBy} onValueChange={handleGroupByChange}>
            <SelectTrigger className="w-[160px]">
              <SelectValue placeholder="Split by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="domain">Split by: Domain</SelectItem>
              <SelectItem value="role">Split by: Role</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
            <RefreshCw className={cn('size-4 mr-2', loading && 'animate-spin')} />
            Refresh
          </Button>
        </div>
      </div>

      <SummaryStrip>
        <MetricCard
          title="Active enriched jobs"
          value={formatNumber(data.total_active_enriched)}
        />
        <MetricCard
          title="No-pool jobs (global)"
          value={formatNumber(data.global_no_pool_count)}
        />
        <MetricCard
          title="Global no-pool %"
          value={`${data.global_no_pool_pct}%`}
          valueClassName={pctColor(data.global_no_pool_pct, data.global_no_pool_pct >= THRESHOLD_PCT)}
        />
        <MetricCard
          title={`${groupsLabel} needing review`}
          value={needsReviewCount}
          subtitle={`${data.domains_flagged} flagged (≥${THRESHOLD_PCT}%)`}
          valueClassName={needsReviewCount > 0 ? 'text-red-600' : undefined}
        />
      </SummaryStrip>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-medium">Per-{groupBy} breakdown</CardTitle>
          {groupBy === 'role' && (
            <p className="text-xs text-muted-foreground font-normal">
              Jobs with multiple roles are counted once per role, so row totals can exceed active
              job count. Global metrics stay job-level.
            </p>
          )}
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <SortableTableHead label={groupLabel} columnKey="key" sort={sort} onToggle={toggleSort} />
                <SortableTableHead label="Total" columnKey="total" sort={sort} onToggle={toggleSort} align="right" />
                <SortableTableHead label="No-pool" columnKey="no_pool" sort={sort} onToggle={toggleSort} align="right" />
                <SortableTableHead label="No-pool %" columnKey="no_pool_pct" sort={sort} onToggle={toggleSort} align="right" />
                <SortableTableHead label="Status" columnKey="status" sort={sort} onToggle={toggleSort} />
                <TableHead className="w-[100px]" />
                <TableHead className="w-[130px]" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedRows.map((domain) => (
                <Fragment key={domain.domain}>
                  <TableRow
                    className={cn(
                      domain.needs_review && 'bg-destructive/5',
                      domain.acknowledged && domain.flagged && 'bg-muted/40',
                    )}
                  >
                    <TableCell>
                      <code className="text-xs">{domain.domain}</code>
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {formatNumber(domain.total)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {formatNumber(domain.no_pool)}
                    </TableCell>
                    <TableCell className="text-right">
                      <PctBadge pct={domain.no_pool_pct} flagged={domain.flagged} />
                    </TableCell>
                    <TableCell>
                      {domain.needs_review ? (
                        <span className="inline-flex items-center gap-1 text-xs text-amber-600">
                          <AlertTriangle className="size-3.5" />
                          Review taxonomy
                        </span>
                      ) : domain.acknowledged && domain.flagged ? (
                        <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
                          <CheckCircle2 className="size-3.5" />
                          Acknowledged
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-xs text-green-600">
                          <CheckCircle2 className="size-3.5" />
                          OK
                        </span>
                      )}
                    </TableCell>
                    <TableCell>
                      {domain.flagged && (
                        <Button
                          variant="outline"
                          size="sm"
                          className="h-7 text-xs"
                          onClick={() =>
                            void toggleAcknowledged(domain.domain, !domain.acknowledged)
                          }
                        >
                          {domain.acknowledged ? 'Unack' : 'Ack'}
                        </Button>
                      )}
                    </TableCell>
                    <TableCell>
                      {domain.top_no_pool_titles.length > 0 && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-7 text-xs"
                          onClick={() =>
                            setExpanded(
                              expanded === domain.domain ? null : domain.domain
                            )
                          }
                        >
                          <ChevronDown
                            className={cn(
                              'size-3.5 mr-1 transition-transform',
                              expanded === domain.domain && 'rotate-180'
                            )}
                          />
                          Top titles
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                  {expanded === domain.domain && domain.top_no_pool_titles.length > 0 && (
                    <TableRow className="bg-muted/30 hover:bg-muted/30">
                      <TableCell colSpan={7} className="py-3">
                        <p className="text-xs text-muted-foreground mb-2">
                          Top no-pool job titles in <strong>{domain.domain}</strong>
                          {domain.flagged && (
                            <> — consider adding a new pool/taxonomy entry</>
                          )}
                        </p>
                        <div className="grid gap-1 text-xs">
                          {domain.top_no_pool_titles.map((title) => (
                            <div
                              key={title.title}
                              className="flex justify-between max-w-xl"
                            >
                              <span>{title.title}</span>
                              <span className="text-muted-foreground tabular-nums">
                                {title.count} jobs
                              </span>
                            </div>
                          ))}
                        </div>
                      </TableCell>
                    </TableRow>
                  )}
                </Fragment>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <p className="text-xs text-muted-foreground">
        Generated {new Date(data.generated_at).toLocaleString()}. Threshold: flag {groupBy === 'role' ? 'roles' : 'domains'} with
        no-pool ≥ {THRESHOLD_PCT}%. To fix: expand titles above, update taxonomy/prompt if titles
        cluster, then re-enrich flagged jobs manually. Acknowledge groups with
        intentional exclusions to suppress repeat alerts.
      </p>
    </div>
  )
}
