'use client'

import { useCallback, useEffect, useState } from 'react'
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
import { Globe, RefreshCw } from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { SortableTableHead } from './sortable-table-head'
import { useTableSort } from '@/hooks/use-table-sort'
import {
  getCompanies,
  getH1bCoverage,
  getH1bReviewQueue,
  getH1bStats,
  linkH1bEmployer,
  triggerH1bIngest,
  type H1bCoverageResponse,
  type H1bReviewQueueResponse,
  type H1bStatsResponse,
} from '@/lib/api'
import { cn } from '@/lib/utils'
import { formatNumber } from '@/lib/dashboard-utils'

type ReviewItem = H1bReviewQueueResponse['items'][number]
type CoverageItem = H1bCoverageResponse['items'][number]

const reviewGetters = {
  employer: (r: ReviewItem) => r.employer_name_norm,
  method: (r: ReviewItem) => r.match_method,
  total_lca: (r: ReviewItem) => r.total_lca,
}

const coverageGetters = {
  pool_family: (r: CoverageItem) => r.pool_family,
  companies_with_data: (r: CoverageItem) => r.companies_with_data,
  tracked_companies: (r: CoverageItem) => r.tracked_companies,
  coverage_pct: (r: CoverageItem) => r.coverage_pct,
}

export function H1bTab() {
  const [stats, setStats] = useState<H1bStatsResponse | null>(null)
  const [queue, setQueue] = useState<H1bReviewQueueResponse | null>(null)
  const [coverage, setCoverage] = useState<H1bCoverageResponse | null>(null)
  const [companies, setCompanies] = useState<Array<{ id: string; name: string }>>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [linkingId, setLinkingId] = useState<number | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [statsRes, queueRes, coverageRes, companyRows] = await Promise.all([
        getH1bStats(),
        getH1bReviewQueue(),
        getH1bCoverage(),
        getCompanies({ includeJobCounts: false, limit: 500 }),
      ])
      setStats(statsRes)
      setQueue(queueRes)
      setCoverage(coverageRes)
      setCompanies(companyRows.map((c) => ({ id: c.id, name: c.companyName })))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load H-1B data')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void load()
  }, [load])

  const handleLink = async (employerId: number, companyId: string) => {
    setLinkingId(employerId)
    try {
      await linkH1bEmployer(employerId, companyId)
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to link employer')
    } finally {
      setLinkingId(null)
    }
  }

  const handleReingest = async () => {
    setLoading(true)
    try {
      await triggerH1bIngest()
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ingestion failed')
      setLoading(false)
    }
  }

  const reviewItems = queue?.items ?? []
  const coverageItems = coverage?.items ?? []
  const {
    sortedRows: sortedReview,
    sort: reviewSort,
    toggleSort: toggleReviewSort,
  } = useTableSort(reviewItems, reviewGetters)
  const {
    sortedRows: sortedCoverage,
    sort: coverageSort,
    toggleSort: toggleCoverageSort,
  } = useTableSort(coverageItems, coverageGetters)

  if (loading && !stats) {
    return <p className="text-sm text-muted-foreground">Loading H-1B stats…</p>
  }

  if (error && !stats) {
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

  if (!stats) return null

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-muted-foreground">
          <Globe className="size-4" />
          <span className="text-sm">DOL LCA + USCIS employer sponsorship data</span>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => void handleReingest()} disabled={loading}>
            Rebuild summary
          </Button>
          <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
            <RefreshCw className={cn('size-4 mr-2', loading && 'animate-spin')} />
            Refresh
          </Button>
        </div>
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <SummaryStrip>
        <MetricCard title="Employers tracked" value={formatNumber(stats.total_employers)} />
        <MetricCard title="Matched to companies" value={formatNumber(stats.matched_employers)} />
        <MetricCard title="Match rate" value={`${stats.match_rate_pct}%`} />
        <MetricCard title="LCA rows loaded" value={formatNumber(stats.total_lca_rows)} />
      </SummaryStrip>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Review queue (LCA volume &gt; 50)</CardTitle>
        </CardHeader>
        <CardContent>
          {!queue?.items.length ? (
            <p className="text-sm text-muted-foreground">No high-volume unmatched employers.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <SortableTableHead label="Employer" columnKey="employer" sort={reviewSort} onToggle={toggleReviewSort} />
                  <SortableTableHead label="Method" columnKey="method" sort={reviewSort} onToggle={toggleReviewSort} />
                  <SortableTableHead label="LCA count" columnKey="total_lca" sort={reviewSort} onToggle={toggleReviewSort} align="right" />
                  <TableHead>Link company</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sortedReview.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell className="font-medium">{item.employer_name_norm}</TableCell>
                    <TableCell>{item.match_method}</TableCell>
                    <TableCell className="text-right tabular-nums">{formatNumber(item.total_lca)}</TableCell>
                    <TableCell>
                      <Select
                        disabled={linkingId === item.id}
                        onValueChange={(companyId) => void handleLink(item.id, companyId)}
                      >
                        <SelectTrigger className="w-[220px]">
                          <SelectValue placeholder="Select company…" />
                        </SelectTrigger>
                        <SelectContent>
                          {companies.map((company) => (
                            <SelectItem key={company.id} value={company.id}>
                              {company.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Coverage by pool family</CardTitle>
        </CardHeader>
        <CardContent>
          {!coverage?.items.length ? (
            <p className="text-sm text-muted-foreground">No summary data yet. Run ingestion first.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <SortableTableHead label="Pool family" columnKey="pool_family" sort={coverageSort} onToggle={toggleCoverageSort} />
                  <SortableTableHead label="With data" columnKey="companies_with_data" sort={coverageSort} onToggle={toggleCoverageSort} align="right" />
                  <SortableTableHead label="Tracked" columnKey="tracked_companies" sort={coverageSort} onToggle={toggleCoverageSort} align="right" />
                  <SortableTableHead label="Coverage" columnKey="coverage_pct" sort={coverageSort} onToggle={toggleCoverageSort} align="right" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {sortedCoverage.map((row) => (
                  <TableRow key={row.pool_family}>
                    <TableCell>{row.pool_family}</TableCell>
                    <TableCell className="text-right tabular-nums">
                      {formatNumber(row.companies_with_data)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {formatNumber(row.tracked_companies)}
                    </TableCell>
                    <TableCell
                      className={cn(
                        'text-right font-semibold tabular-nums',
                        row.flagged ? 'text-amber-600' : 'text-green-600',
                      )}
                    >
                      {row.coverage_pct}%
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
