'use client'

import { useEffect, useState } from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  LineChart,
  Line,
} from 'recharts'
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart'
import { Coins, ArrowUpRight, ArrowDownRight, AlertTriangle } from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { PlatformBadge } from './status-badges'
import { type PipelineRun, type TrendDataPoint, type UsageByCompany, type UsageByPlatform } from '@/lib/mock-data'
import { formatNumber, formatCost, calculateEstimatedCost } from '@/lib/dashboard-utils'
import { getCostTrend, getCostUsage, getPipelineRuns, type UsagePeriod, type UsageSplitBy } from '@/lib/api'

export function CostTab() {
  const [timePeriod, setTimePeriod] = useState<UsagePeriod>('day')
  const [splitBy, setSplitBy] = useState<UsageSplitBy>('platform')
  const [selectedRun, setSelectedRun] = useState<string>('')
  const [runs, setRuns] = useState<PipelineRun[]>([])
  const [usageByPlatform, setUsageByPlatform] = useState<UsageByPlatform[]>([])
  const [usageByCompany, setUsageByCompany] = useState<UsageByCompany[]>([])
  const [trendData, setTrendData] = useState<TrendDataPoint[]>([])
  const [summary, setSummary] = useState({
    total_input_tokens: 0,
    total_output_tokens: 0,
    estimated_cost: 0,
    enrichment_failure_rate: 0,
  })
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadRuns = async () => {
      try {
        const runRows = await getPipelineRuns(20, 0)
        setRuns(runRows)
        if (runRows[0]) {
          setSelectedRun(runRows[0].id)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load runs')
      }
    }
    void loadRuns()
  }, [])

  useEffect(() => {
    const loadUsage = async () => {
      try {
        const usage = await getCostUsage({
          period: timePeriod,
          splitBy,
          runId: timePeriod === 'run' ? selectedRun : undefined,
        })
        const trend = await getCostTrend(timePeriod, 30)
        setSummary(usage.summary)
        setUsageByPlatform(usage.usageByPlatform)
        setUsageByCompany(usage.usageByCompany)
        setTrendData(trend)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load cost data')
      }
    }
    if (timePeriod !== 'run' || selectedRun) {
      void loadUsage()
    }
  }, [timePeriod, splitBy, selectedRun])

  const chartConfig = {
    inputTokens: {
      label: 'Input Tokens',
      color: 'var(--chart-1)',
    },
    outputTokens: {
      label: 'Output Tokens',
      color: 'var(--chart-2)',
    },
    estimatedCost: {
      label: 'Est. Cost',
      color: 'var(--chart-3)',
    },
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Time Period:</span>
          <Select value={timePeriod} onValueChange={(v) => setTimePeriod(v as UsagePeriod)}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="run">Per Run</SelectItem>
              <SelectItem value="day">Day</SelectItem>
              <SelectItem value="month">Month</SelectItem>
            </SelectContent>
          </Select>
        </div>
        {timePeriod === 'run' && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-muted-foreground">Run:</span>
            <Select value={selectedRun} onValueChange={setSelectedRun}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {runs.map(run => (
                  <SelectItem key={run.id} value={run.id}>
                    {new Date(run.timestamp).toLocaleString('en-US', { 
                      month: 'short', 
                      day: 'numeric',
                      hour: 'numeric',
                      minute: '2-digit'
                    })}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Split By:</span>
          <Select value={splitBy} onValueChange={(v) => setSplitBy(v as UsageSplitBy)}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="platform">Platform</SelectItem>
              <SelectItem value="company">Company</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Summary Strip */}
      <SummaryStrip>
        <MetricCard
          title="Total Input Tokens"
          value={formatNumber(summary.total_input_tokens)}
          icon={<ArrowUpRight className="size-5" />}
        />
        <MetricCard
          title="Total Output Tokens"
          value={formatNumber(summary.total_output_tokens)}
          icon={<ArrowDownRight className="size-5" />}
        />
        <MetricCard
          title="Estimated Cost"
          value={formatCost(summary.estimated_cost)}
          subtitle="Estimate based on current pricing"
          icon={<Coins className="size-5" />}
        />
        <MetricCard
          title="Enrichment Failure Rate"
          value={`${summary.enrichment_failure_rate.toFixed(1)}%`}
          valueClassName={summary.enrichment_failure_rate > 5 ? 'text-warning' : ''}
          icon={<AlertTriangle className="size-5" />}
        />
      </SummaryStrip>

      {/* Breakdown View */}
      <Card>
        <CardHeader>
          <CardTitle>
            Usage Breakdown by {splitBy === 'platform' ? 'Platform' : 'Company'}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {splitBy === 'platform' ? (
            <div className="space-y-6">
              {/* Bar Chart for Platform */}
              <ChartContainer config={chartConfig} className="h-[300px]">
                <BarChart data={usageByPlatform}>
                  <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
                  <XAxis 
                    dataKey="platform" 
                    tickFormatter={(value) => value.charAt(0).toUpperCase() + value.slice(1)}
                    className="text-muted-foreground"
                  />
                  <YAxis tickFormatter={(value) => formatNumber(value)} className="text-muted-foreground" />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Bar dataKey="inputTokens" fill="var(--chart-1)" name="Input Tokens" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="outputTokens" fill="var(--chart-2)" name="Output Tokens" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ChartContainer>

              {/* Platform Table */}
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Platform</TableHead>
                    <TableHead className="text-right">Input Tokens</TableHead>
                    <TableHead className="text-right">Output Tokens</TableHead>
                    <TableHead className="text-right">Estimated Cost</TableHead>
                    <TableHead className="text-right">Enrichments</TableHead>
                    <TableHead className="text-right">Failures</TableHead>
                    <TableHead className="text-right">Avg Latency</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {usageByPlatform.map((data) => (
                    <TableRow key={data.platform}>
                      <TableCell><PlatformBadge platform={data.platform} /></TableCell>
                      <TableCell className="text-right font-mono">{formatNumber(data.inputTokens)}</TableCell>
                      <TableCell className="text-right font-mono">{formatNumber(data.outputTokens)}</TableCell>
                      <TableCell className="text-right font-mono">
                        {formatCost(calculateEstimatedCost(data.inputTokens, data.outputTokens))}
                      </TableCell>
                      <TableCell className="text-right">{data.enrichmentCount}</TableCell>
                      <TableCell className="text-right">
                        <span className={data.failureCount > 0 ? 'text-warning' : ''}>{data.failureCount}</span>
                      </TableCell>
                      <TableCell className="text-right text-muted-foreground">{data.avgLatency}ms</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            /* Company Table */
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Company</TableHead>
                  <TableHead className="text-right">Input Tokens</TableHead>
                  <TableHead className="text-right">Output Tokens</TableHead>
                  <TableHead className="text-right">Estimated Cost</TableHead>
                  <TableHead className="text-right">Enrichments</TableHead>
                  <TableHead className="text-right">Failures</TableHead>
                  <TableHead className="text-right">Avg Latency</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {usageByCompany.map((data) => (
                  <TableRow key={data.company}>
                    <TableCell className="font-medium">{data.company}</TableCell>
                    <TableCell className="text-right font-mono">{formatNumber(data.inputTokens)}</TableCell>
                    <TableCell className="text-right font-mono">{formatNumber(data.outputTokens)}</TableCell>
                    <TableCell className="text-right font-mono">
                      {formatCost(calculateEstimatedCost(data.inputTokens, data.outputTokens))}
                    </TableCell>
                    <TableCell className="text-right">{data.enrichmentCount}</TableCell>
                    <TableCell className="text-right">
                      <span className={data.failureCount > 0 ? 'text-warning' : ''}>{data.failureCount}</span>
                    </TableCell>
                    <TableCell className="text-right text-muted-foreground">{data.avgLatency}ms</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Trend Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Usage Trend (Last 30 Days)</CardTitle>
        </CardHeader>
        <CardContent>
          <ChartContainer config={chartConfig} className="h-[300px]">
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => {
                  const date = new Date(value)
                  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
                }}
                className="text-muted-foreground"
              />
              <YAxis 
                yAxisId="tokens"
                tickFormatter={(value) => formatNumber(value)} 
                className="text-muted-foreground"
              />
              <YAxis 
                yAxisId="cost"
                orientation="right"
                tickFormatter={(value) => `$${value}`} 
                className="text-muted-foreground"
              />
              <ChartTooltip content={<ChartTooltipContent />} />
              <Line 
                yAxisId="tokens"
                type="monotone" 
                dataKey="inputTokens" 
                stroke="var(--chart-1)" 
                strokeWidth={2}
                dot={false}
                name="Input Tokens"
              />
              <Line 
                yAxisId="tokens"
                type="monotone" 
                dataKey="outputTokens" 
                stroke="var(--chart-2)" 
                strokeWidth={2}
                dot={false}
                name="Output Tokens"
              />
              <Line 
                yAxisId="cost"
                type="monotone" 
                dataKey="estimatedCost" 
                stroke="var(--chart-3)" 
                strokeWidth={2}
                dot={false}
                name="Est. Cost ($)"
              />
            </LineChart>
          </ChartContainer>
        </CardContent>
      </Card>
      {error && <div className="text-sm text-warning">{error}</div>}
    </div>
  )
}
