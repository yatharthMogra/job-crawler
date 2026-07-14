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
import { Button } from '@/components/ui/button'
import { ChevronDown, ChevronRight, Database, AlertTriangle, Pause, Flag, Play } from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { StatusBadge, PlatformBadge } from './status-badges'
import { RelativeTime } from './relative-time'
import { SortableTableHead } from './sortable-table-head'
import { useTableSort } from '@/hooks/use-table-sort'
import { type Event, type Source } from '@/lib/mock-data'
import { cn } from '@/lib/utils'
import { flagCompany, getCompanies, getEvents, patchCompany } from '@/lib/api'

const sourceGetters = {
  company: (s: Source) => s.companyName,
  platform: (s: Source) => s.platform,
  health: (s: Source) => s.health,
  activeJobs: (s: Source) => s.activeJobs,
  lastSuccessfulFetch: (s: Source) => s.lastSuccessfulFetch,
  lastFailure: (s: Source) => s.lastFailure,
  consecutiveFailures: (s: Source) => s.consecutiveFailures,
  status: (s: Source) => (s.isActive ? (s.requiresReview ? 1 : 0) : 2),
}

export function SourcesTab() {
  const [expandedSource, setExpandedSource] = useState<string | null>(null)
  const [sources, setSources] = useState<Source[]>([])
  const [eventsBySource, setEventsBySource] = useState<Record<string, Event[]>>({})
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      try {
        const rows = await getCompanies({ includeJobCounts: true, limit: 200 })
        setSources(rows)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load sources')
      }
    }
    void load()
  }, [])

  useEffect(() => {
    if (!expandedSource || eventsBySource[expandedSource]) return
    const load = async () => {
      try {
        const rows = await getEvents({ companyId: expandedSource, limit: 10 })
        setEventsBySource((prev) => ({ ...prev, [expandedSource]: rows }))
      } catch {
        setEventsBySource((prev) => ({ ...prev, [expandedSource]: [] }))
      }
    }
    void load()
  }, [expandedSource, eventsBySource])

  const { sortedRows, sort, toggleSort } = useTableSort(sources, sourceGetters)

  const handleTogglePause = async (sourceId: string, nextIsActive: boolean) => {
    await patchCompany(sourceId, { isActive: nextIsActive })
    setSources((prev) =>
      prev.map((source) => (source.id === sourceId ? { ...source, isActive: nextIsActive } : source)),
    )
  }

  const handleFlagForReview = async (sourceId: string) => {
    await flagCompany(sourceId)
    setSources((prev) =>
      prev.map((source) => (source.id === sourceId ? { ...source, requiresReview: true } : source)),
    )
  }

  const stats = useMemo(
    () => ({
      totalActive: sources.filter((source) => source.isActive).length,
      withFailures: sources.filter((source) => source.consecutiveFailures > 0).length,
      paused: sources.filter((source) => !source.isActive).length,
      flaggedForReview: sources.filter((source) => source.requiresReview).length,
    }),
    [sources],
  )

  return (
    <div className="space-y-6">
      <SummaryStrip>
        <MetricCard
          title="Total Active Sources"
          value={stats.totalActive}
          icon={<Database className="size-5" />}
        />
        <MetricCard
          title="Sources with Failures"
          value={stats.withFailures}
          valueClassName={stats.withFailures > 0 ? 'text-warning' : ''}
          icon={<AlertTriangle className="size-5" />}
        />
        <MetricCard
          title="Paused Sources"
          value={stats.paused}
          icon={<Pause className="size-5" />}
        />
        <MetricCard
          title="Flagged for Review"
          value={stats.flaggedForReview}
          valueClassName={stats.flaggedForReview > 0 ? 'text-error' : ''}
          icon={<Flag className="size-5" />}
        />
      </SummaryStrip>

      <Card>
        <CardHeader>
          <CardTitle>Company Sources</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-8"></TableHead>
                <SortableTableHead label="Company" columnKey="company" sort={sort} onToggle={toggleSort} />
                <SortableTableHead label="Platform" columnKey="platform" sort={sort} onToggle={toggleSort} />
                <SortableTableHead label="Health" columnKey="health" sort={sort} onToggle={toggleSort} />
                <SortableTableHead
                  label="Active Jobs"
                  columnKey="activeJobs"
                  sort={sort}
                  onToggle={toggleSort}
                  align="right"
                />
                <SortableTableHead
                  label="Last Successful Fetch"
                  columnKey="lastSuccessfulFetch"
                  sort={sort}
                  onToggle={toggleSort}
                />
                <SortableTableHead label="Last Failure" columnKey="lastFailure" sort={sort} onToggle={toggleSort} />
                <SortableTableHead
                  label="Consecutive Failures"
                  columnKey="consecutiveFailures"
                  sort={sort}
                  onToggle={toggleSort}
                  align="right"
                />
                <SortableTableHead label="Status" columnKey="status" sort={sort} onToggle={toggleSort} />
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedRows.map((source) => (
                <SourceRow
                  key={source.id}
                  source={source}
                  sourceEvents={eventsBySource[source.id] || []}
                  isExpanded={expandedSource === source.id}
                  onToggle={() => setExpandedSource(expandedSource === source.id ? null : source.id)}
                  onTogglePause={() => handleTogglePause(source.id, !source.isActive)}
                  onFlagForReview={() => handleFlagForReview(source.id)}
                />
              ))}
              {sortedRows.length === 0 && (
                <TableRow>
                  <TableCell colSpan={10} className="text-center text-muted-foreground py-8">
                    {error || 'No sources found'}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

interface SourceRowProps {
  source: Source
  sourceEvents: Event[]
  isExpanded: boolean
  onToggle: () => void
  onTogglePause: () => void
  onFlagForReview: () => void
}

function SourceRow({
  source,
  sourceEvents,
  isExpanded,
  onToggle,
  onTogglePause,
  onFlagForReview,
}: SourceRowProps) {
  return (
    <>
      <TableRow className="cursor-pointer hover:bg-muted/50">
        <TableCell onClick={onToggle}>
          {isExpanded ? (
            <ChevronDown className="size-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="size-4 text-muted-foreground" />
          )}
        </TableCell>
        <TableCell onClick={onToggle} className="font-medium">
          {source.companyName}
        </TableCell>
        <TableCell onClick={onToggle}>
          <PlatformBadge platform={source.platform} />
        </TableCell>
        <TableCell onClick={onToggle}>
          <StatusBadge status={source.health} />
        </TableCell>
        <TableCell onClick={onToggle} className="text-right">
          {source.activeJobs}
        </TableCell>
        <TableCell onClick={onToggle}>
          <RelativeTime date={source.lastSuccessfulFetch} />
        </TableCell>
        <TableCell onClick={onToggle}>
          {source.lastFailure ? (
            <span className="text-warning">
              <RelativeTime date={source.lastFailure} />
            </span>
          ) : (
            <span className="text-muted-foreground">-</span>
          )}
        </TableCell>
        <TableCell onClick={onToggle} className="text-right">
          <span
            className={cn(
              source.consecutiveFailures > 0 ? 'text-warning font-medium' : 'text-muted-foreground',
            )}
          >
            {source.consecutiveFailures}
          </span>
        </TableCell>
        <TableCell onClick={onToggle}>
          {!source.isActive ? (
            <StatusBadge status="pending" />
          ) : source.requiresReview ? (
            <StatusBadge status="requires_review" />
          ) : (
            <StatusBadge status="success" />
          )}
        </TableCell>
        <TableCell>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                onTogglePause()
              }}
            >
              {source.isActive ? (
                <>
                  <Pause className="size-3 mr-1" />
                  Pause
                </>
              ) : (
                <>
                  <Play className="size-3 mr-1" />
                  Resume
                </>
              )}
            </Button>
            <Button
              variant="outline"
              size="sm"
              disabled={source.requiresReview}
              onClick={(e) => {
                e.stopPropagation()
                onFlagForReview()
              }}
            >
              <Flag className="size-3 mr-1" />
              Flag
            </Button>
          </div>
        </TableCell>
      </TableRow>
      {isExpanded && (
        <TableRow>
          <TableCell colSpan={10} className="bg-muted/30 p-0">
            <div className="p-4">
              <h4 className="text-sm font-medium mb-3">Recent Events for {source.companyName}</h4>
              {sourceEvents.length > 0 ? (
                <div className="space-y-2">
                  {sourceEvents.map((event) => (
                    <div
                      key={event.id}
                      className="flex items-center gap-4 py-2 px-3 rounded bg-card border border-border text-sm"
                    >
                      <RelativeTime
                        date={event.timestamp}
                        className="text-muted-foreground w-24 flex-shrink-0"
                      />
                      <StatusBadge status={event.severity} />
                      <span className="text-foreground">{event.message}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-muted-foreground text-sm py-4 text-center">
                  No recent events for this source
                </div>
              )}
            </div>
          </TableCell>
        </TableRow>
      )}
    </>
  )
}
