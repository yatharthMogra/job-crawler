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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { ChevronDown, ChevronRight, Activity, Clock, Briefcase, AlertTriangle, Info, AlertCircle } from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { StatusBadge, PlatformBadge, SeverityBadge } from './status-badges'
import { RelativeTime } from './relative-time'
import { type CompanyRunDetail, type Event, type PipelineRun, type Severity } from '@/lib/mock-data'
import { formatNumber } from '@/lib/dashboard-utils'
import { getCompanyRunDetails, getEvents, getPipelineRuns } from '@/lib/api'

export function PipelineTab() {
  const [expandedRun, setExpandedRun] = useState<string | null>(null)
  const [severityFilter, setSeverityFilter] = useState<string>('all')
  const [platformFilter, setPlatformFilter] = useState<string>('all')
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [runs, setRuns] = useState<PipelineRun[]>([])
  const [events, setEvents] = useState<Event[]>([])
  const [detailsByRun, setDetailsByRun] = useState<Record<string, CompanyRunDetail[]>>({})
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [runsData, eventsData] = await Promise.all([getPipelineRuns(20, 0), getEvents({ limit: 100 })])
        setRuns(runsData)
        setEvents(eventsData)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load pipeline data')
      }
    }
    void load()
  }, [])

  useEffect(() => {
    if (!expandedRun || detailsByRun[expandedRun]) return
    const load = async () => {
      try {
        const details = await getCompanyRunDetails(expandedRun)
        setDetailsByRun((prev) => ({ ...prev, [expandedRun]: details }))
      } catch {
        setDetailsByRun((prev) => ({ ...prev, [expandedRun]: [] }))
      }
    }
    void load()
  }, [expandedRun, detailsByRun])

  const filteredEvents = useMemo(
    () =>
      events.filter((event) => {
        if (severityFilter !== 'all' && event.severity !== severityFilter) return false
        if (platformFilter !== 'all' && event.platform !== platformFilter) return false
        if (categoryFilter !== 'all' && event.category !== categoryFilter) return false
        return true
      }),
    [events, severityFilter, platformFilter, categoryFilter]
  )

  const latestRun = runs[0]
  const stats = {
    lastRunStatus: latestRun?.status ?? 'failed',
    lastRunTime: latestRun?.timestamp ?? null,
    jobsFetched: latestRun?.jobsFetched ?? 0,
    failedCompanies: latestRun?.failedCompanies ?? 0,
  }

  return (
    <div className="space-y-6">
      {/* Summary Strip */}
      <SummaryStrip>
        <MetricCard
          title="Last Run Status"
          value={<StatusBadge status={stats.lastRunStatus} />}
          icon={<Activity className="size-5" />}
        />
        <MetricCard
          title="Last Run Time"
          value={<RelativeTime date={stats.lastRunTime} />}
          icon={<Clock className="size-5" />}
        />
        <MetricCard
          title="Jobs Fetched (last run)"
          value={formatNumber(stats.jobsFetched)}
          icon={<Briefcase className="size-5" />}
        />
        <MetricCard
          title="Failed Companies (last run)"
          value={stats.failedCompanies}
          valueClassName={stats.failedCompanies > 0 ? 'text-warning' : ''}
          icon={<AlertTriangle className="size-5" />}
        />
      </SummaryStrip>

      {/* Run History Table */}
      <Card>
        <CardHeader>
          <CardTitle>Run History</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-8"></TableHead>
                <TableHead>Timestamp</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Total Companies</TableHead>
                <TableHead className="text-right">Successful</TableHead>
                <TableHead className="text-right">Failed</TableHead>
                <TableHead className="text-right">Jobs Fetched</TableHead>
                <TableHead className="text-right">New</TableHead>
                <TableHead className="text-right">Updated</TableHead>
                <TableHead className="text-right">Unchanged</TableHead>
                <TableHead className="text-right">Duration</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {runs.map((run) => (
                <RunRow 
                  key={run.id} 
                  run={run} 
                  details={detailsByRun[run.id] || []}
                  isExpanded={expandedRun === run.id}
                  onToggle={() => setExpandedRun(expandedRun === run.id ? null : run.id)}
                />
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Recent Events Panel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Recent Events</CardTitle>
            <div className="flex items-center gap-2">
              <Select value={severityFilter} onValueChange={setSeverityFilter}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Severity" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Severity</SelectItem>
                  <SelectItem value="info">Info</SelectItem>
                  <SelectItem value="warning">Warning</SelectItem>
                  <SelectItem value="error">Error</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
              <Select value={platformFilter} onValueChange={setPlatformFilter}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Platform" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Platforms</SelectItem>
                  <SelectItem value="greenhouse">Greenhouse</SelectItem>
                  <SelectItem value="lever">Lever</SelectItem>
                  <SelectItem value="ashby">Ashby</SelectItem>
                </SelectContent>
              </Select>
              <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="pipeline">Pipeline</SelectItem>
                  <SelectItem value="source">Source</SelectItem>
                  <SelectItem value="enrichment">Enrichment</SelectItem>
                  <SelectItem value="review">Review</SelectItem>
                  <SelectItem value="system">System</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {filteredEvents.map((event) => (
              <EventRow key={event.id} event={event} />
            ))}
            {filteredEvents.length === 0 && (
              <div className="text-center text-muted-foreground py-8">
                {error ? `Error: ${error}` : 'No events match the selected filters'}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

interface RunRowProps {
  run: PipelineRun
  details: CompanyRunDetail[]
  isExpanded: boolean
  onToggle: () => void
}

function RunRow({ run, details, isExpanded, onToggle }: RunRowProps) {
  return (
    <>
      <TableRow 
        className="cursor-pointer hover:bg-muted/50"
        onClick={onToggle}
      >
        <TableCell>
          {isExpanded ? (
            <ChevronDown className="size-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="size-4 text-muted-foreground" />
          )}
        </TableCell>
        <TableCell><RelativeTime date={run.timestamp} /></TableCell>
        <TableCell><StatusBadge status={run.status} /></TableCell>
        <TableCell className="text-right">{run.totalCompanies}</TableCell>
        <TableCell className="text-right text-success">{run.successfulCompanies}</TableCell>
        <TableCell className="text-right">
          <span className={run.failedCompanies > 0 ? 'text-error' : ''}>{run.failedCompanies}</span>
        </TableCell>
        <TableCell className="text-right font-medium">{formatNumber(run.jobsFetched)}</TableCell>
        <TableCell className="text-right text-success">{run.jobsNew}</TableCell>
        <TableCell className="text-right text-info">{run.jobsUpdated}</TableCell>
        <TableCell className="text-right text-muted-foreground">{run.jobsUnchanged}</TableCell>
        <TableCell className="text-right text-muted-foreground">{formatDuration(run.duration)}</TableCell>
      </TableRow>
      {isExpanded && details.length > 0 && (
        <TableRow>
          <TableCell colSpan={11} className="bg-muted/30 p-0">
            <div className="p-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Company</TableHead>
                    <TableHead>Platform</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Jobs Fetched</TableHead>
                    <TableHead className="text-right">New</TableHead>
                    <TableHead className="text-right">Updated</TableHead>
                    <TableHead className="text-right">Unchanged</TableHead>
                    <TableHead>Error</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {details.map((detail, idx) => (
                    <TableRow key={idx}>
                      <TableCell className="font-medium">{detail.companyName}</TableCell>
                      <TableCell><PlatformBadge platform={detail.platform} /></TableCell>
                      <TableCell>
                        <StatusBadge status={detail.status === 'success' ? 'success' : 'failed'} />
                      </TableCell>
                      <TableCell className="text-right">{detail.jobsFetched}</TableCell>
                      <TableCell className="text-right text-success">{detail.jobsNew}</TableCell>
                      <TableCell className="text-right text-info">{detail.jobsUpdated}</TableCell>
                      <TableCell className="text-right text-muted-foreground">{detail.jobsUnchanged}</TableCell>
                      <TableCell className="text-error">{detail.errorMessage || '-'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </TableCell>
        </TableRow>
      )}
    </>
  )
}

interface EventRowProps {
  event: Event
}

function EventRow({ event }: EventRowProps) {
  const severityIcons: Record<Severity, JSX.Element> = {
    info: <Info className="size-4 text-info" />,
    warning: <AlertTriangle className="size-4 text-warning" />,
    error: <AlertCircle className="size-4 text-error" />,
    critical: <AlertCircle className="size-4 text-error" />,
  }

  return (
    <div className="flex items-center gap-4 py-3 px-4 rounded-lg bg-card border border-border hover:bg-muted/30 transition-colors">
      <div className="flex-shrink-0">
        {severityIcons[event.severity]}
      </div>
      <div className="flex-shrink-0 w-24">
        <RelativeTime date={event.timestamp} className="text-sm text-muted-foreground" />
      </div>
      <div className="flex-shrink-0">
        <SeverityBadge severity={event.severity} />
      </div>
      <div className="flex-shrink-0">
        <Badge variant="outline" className="capitalize">{event.category}</Badge>
      </div>
      {event.company && (
        <div className="flex-shrink-0 text-sm font-medium">{event.company}</div>
      )}
      {event.platform && (
        <div className="flex-shrink-0">
          <PlatformBadge platform={event.platform} />
        </div>
      )}
      <div className="flex-1 text-sm text-foreground truncate">{event.message}</div>
    </div>
  )
}

function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}m ${secs}s`
}
