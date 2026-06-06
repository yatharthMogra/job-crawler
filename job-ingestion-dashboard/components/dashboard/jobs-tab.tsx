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
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { 
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { 
  Search, 
  X, 
  AlertCircle, 
  FileWarning, 
  PenLine, 
  Clock,
  ExternalLink,
  ChevronDown,
  Save,
  Flag
} from 'lucide-react'
import { MetricCard, SummaryStrip } from './metric-card'
import { StatusBadge, PlatformBadge } from './status-badges'
import { RelativeTime } from './relative-time'
import { 
  type Job,
  type ProcessingState,
  type Platform
} from '@/lib/mock-data'
import { 
  failureReasonLabels, 
  seniorityOptions, 
  sponsorshipStatusOptions,
  sponsorshipConfidenceOptions,
  remoteTypeOptions
} from '@/lib/dashboard-utils'
import { cn } from '@/lib/utils'
import { flagJob, getJobDetail, getJobs, saveJobReview, type JobUpdateInput } from '@/lib/api'

type ProcessingStateFilter = ProcessingState | 'all'
type PlatformFilter = Platform | 'all'

const defaultFilterStates: ProcessingState[] = [
  'partial_success', 
  'extraction_failed', 
  'enrichment_failed', 
  'requires_review'
]

export function JobsTab() {
  const [processingStateFilter, setProcessingStateFilter] = useState<ProcessingStateFilter>('all')
  const [platformFilter, setPlatformFilter] = useState<PlatformFilter>('all')
  const [companyFilter, setCompanyFilter] = useState<string>('all')
  const [titleSearch, setTitleSearch] = useState('')
  const [showDefaultFilters, setShowDefaultFilters] = useState(true)
  const [selectedJob, setSelectedJob] = useState<Job | null>(null)
  const [jobs, setJobs] = useState<Job[]>([])
  const [error, setError] = useState<string | null>(null)

  const loadJobs = async () => {
    try {
      const rows = await getJobs({ limit: 300 })
      setJobs(rows)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load jobs')
    }
  }

  useEffect(() => {
    void loadJobs()
  }, [])

  // Get unique companies for filter
  const companies = useMemo(() => {
    const uniqueCompanies = [...new Set(jobs.map(j => j.company))]
    return uniqueCompanies.sort()
  }, [jobs])

  // Filter jobs
  const filteredJobs = useMemo(() => {
    return jobs.filter(job => {
      // Default filter for jobs needing attention
      if (showDefaultFilters && !defaultFilterStates.includes(job.processingState)) {
        return false
      }
      
      if (processingStateFilter !== 'all' && job.processingState !== processingStateFilter) {
        return false
      }
      if (platformFilter !== 'all' && job.platform !== platformFilter) {
        return false
      }
      if (companyFilter !== 'all' && job.company !== companyFilter) {
        return false
      }
      if (titleSearch && !job.title.toLowerCase().includes(titleSearch.toLowerCase())) {
        return false
      }
      return true
    })
  }, [jobs, processingStateFilter, platformFilter, companyFilter, titleSearch, showDefaultFilters])

  const stats = useMemo(() => {
    const jobsRequiringReview = jobs.filter((job) => job.processingState === 'requires_review').length
    const enrichmentFailures = jobs.filter(
      (job) => job.processingState === 'enrichment_failed' || job.processingState === 'extraction_failed'
    ).length
    const manualCorrectionsToday = jobs.filter(
      (job) => job.lastManualReview && job.lastManualReview.getTime() > Date.now() - 24 * 60 * 60 * 1000
    ).length
    const oldestPendingReview = jobs
      .filter((job) => job.processingState === 'requires_review')
      .sort((a, b) => a.lastSeen.getTime() - b.lastSeen.getTime())[0]
    return {
      requiresReview: jobsRequiringReview,
      enrichmentFailures,
      manualCorrectionsToday,
      oldestPendingReview: oldestPendingReview?.lastSeen ?? null,
    }
  }, [jobs])

  // Active filter chips
  const activeFilters = useMemo(() => {
    const filters: { key: string; label: string; onRemove: () => void }[] = []
    
    if (showDefaultFilters) {
      filters.push({
        key: 'default',
        label: 'Needs Attention',
        onRemove: () => setShowDefaultFilters(false)
      })
    }
    if (processingStateFilter !== 'all') {
      filters.push({
        key: 'state',
        label: `State: ${processingStateFilter.replace(/_/g, ' ')}`,
        onRemove: () => setProcessingStateFilter('all')
      })
    }
    if (platformFilter !== 'all') {
      filters.push({
        key: 'platform',
        label: `Platform: ${platformFilter}`,
        onRemove: () => setPlatformFilter('all')
      })
    }
    if (companyFilter !== 'all') {
      filters.push({
        key: 'company',
        label: `Company: ${companyFilter}`,
        onRemove: () => setCompanyFilter('all')
      })
    }
    if (titleSearch) {
      filters.push({
        key: 'title',
        label: `Title: "${titleSearch}"`,
        onRemove: () => setTitleSearch('')
      })
    }
    
    return filters
  }, [showDefaultFilters, processingStateFilter, platformFilter, companyFilter, titleSearch])

  return (
    <div className="space-y-6">
      {/* Summary Strip */}
      <SummaryStrip>
        <MetricCard
          title="Jobs Requiring Review"
          value={stats.requiresReview}
          valueClassName={stats.requiresReview > 0 ? 'text-error' : ''}
          icon={<AlertCircle className="size-5" />}
        />
        <MetricCard
          title="Enrichment Failures"
          value={stats.enrichmentFailures}
          valueClassName={stats.enrichmentFailures > 0 ? 'text-warning' : ''}
          icon={<FileWarning className="size-5" />}
        />
        <MetricCard
          title="Manual Corrections Today"
          value={stats.manualCorrectionsToday}
          icon={<PenLine className="size-5" />}
        />
        <MetricCard
          title="Oldest Pending Review"
          value={stats.oldestPendingReview ? <RelativeTime date={stats.oldestPendingReview} /> : 'None'}
          icon={<Clock className="size-5" />}
        />
      </SummaryStrip>

      {/* Filter Bar */}
      <Card>
        <CardContent className="py-4">
          <div className="flex items-center gap-4 flex-wrap">
            <div className="flex items-center gap-2">
              <Select 
                value={processingStateFilter} 
                onValueChange={(v) => setProcessingStateFilter(v as ProcessingStateFilter)}
              >
                <SelectTrigger className="w-44">
                  <SelectValue placeholder="Processing State" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All States</SelectItem>
                  <SelectItem value="success">Success</SelectItem>
                  <SelectItem value="partial_success">Partial Success</SelectItem>
                  <SelectItem value="extraction_failed">Extraction Failed</SelectItem>
                  <SelectItem value="enrichment_failed">Enrichment Failed</SelectItem>
                  <SelectItem value="requires_review">Requires Review</SelectItem>
                  <SelectItem value="manually_corrected">Manually Corrected</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Select 
              value={platformFilter} 
              onValueChange={(v) => setPlatformFilter(v as PlatformFilter)}
            >
              <SelectTrigger className="w-36">
                <SelectValue placeholder="Platform" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="greenhouse">Greenhouse</SelectItem>
                <SelectItem value="lever">Lever</SelectItem>
                <SelectItem value="ashby">Ashby</SelectItem>
              </SelectContent>
            </Select>

            <Select 
              value={companyFilter} 
              onValueChange={setCompanyFilter}
            >
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Company" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Companies</SelectItem>
                {companies.map(company => (
                  <SelectItem key={company} value={company}>{company}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
              <Input
                placeholder="Search job title..."
                value={titleSearch}
                onChange={(e) => setTitleSearch(e.target.value)}
                className="pl-9"
              />
            </div>

            {!showDefaultFilters && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setShowDefaultFilters(true)}
              >
                Show Needs Attention
              </Button>
            )}
          </div>

          {/* Active Filter Chips */}
          {activeFilters.length > 0 && (
            <div className="flex items-center gap-2 mt-3 flex-wrap">
              {activeFilters.map(filter => (
                <Badge 
                  key={filter.key}
                  variant="secondary"
                  className="gap-1 pr-1"
                >
                  {filter.label}
                  <button 
                    onClick={filter.onRemove}
                    className="ml-1 hover:bg-muted rounded-full p-0.5"
                  >
                    <X className="size-3" />
                  </button>
                </Badge>
              ))}
              {activeFilters.length > 1 && (
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => {
                    setShowDefaultFilters(false)
                    setProcessingStateFilter('all')
                    setPlatformFilter('all')
                    setCompanyFilter('all')
                    setTitleSearch('')
                  }}
                  className="text-xs h-6"
                >
                  Clear all
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Jobs Table */}
      <Card>
        <CardHeader>
          <CardTitle>Jobs ({filteredJobs.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Job Title</TableHead>
                <TableHead>Company</TableHead>
                <TableHead>Platform</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>Processing State</TableHead>
                <TableHead>Failure Reason</TableHead>
                <TableHead>Last Seen</TableHead>
                <TableHead>Last Enrichment</TableHead>
                <TableHead>Last Review</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredJobs.map((job) => (
                <TableRow 
                  key={job.id}
                  className="cursor-pointer hover:bg-muted/50"
                  onClick={async () => {
                    try {
                      const detail = await getJobDetail(job.id)
                      setSelectedJob(detail)
                    } catch (err) {
                      setError(err instanceof Error ? err.message : 'Failed to load job details')
                    }
                  }}
                >
                  <TableCell className="font-medium max-w-[200px] truncate">{job.title}</TableCell>
                  <TableCell>{job.company}</TableCell>
                  <TableCell><PlatformBadge platform={job.platform} /></TableCell>
                  <TableCell className="text-muted-foreground max-w-[150px] truncate">{job.location}</TableCell>
                  <TableCell><StatusBadge status={job.processingState} /></TableCell>
                  <TableCell>
                    {job.failureReason ? (
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger>
                            <AlertCircle className="size-4 text-warning" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>{failureReasonLabels[job.failureReason] || job.failureReason}</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell><RelativeTime date={job.lastSeen} /></TableCell>
                  <TableCell><RelativeTime date={job.lastEnrichmentAttempt} /></TableCell>
                  <TableCell><RelativeTime date={job.lastManualReview} /></TableCell>
                </TableRow>
              ))}
              {filteredJobs.length === 0 && (
                <TableRow>
                  <TableCell colSpan={9} className="text-center text-muted-foreground py-8">
                    {error || 'No jobs match the selected filters'}
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Job Detail Panel */}
      <JobDetailPanel 
        job={selectedJob}
        onClose={() => setSelectedJob(null)}
        onUpdated={async () => {
          await loadJobs()
          if (selectedJob) {
            const refreshed = await getJobDetail(selectedJob.id)
            setSelectedJob(refreshed)
          }
        }}
      />
    </div>
  )
}

interface JobDetailPanelProps {
  job: Job | null
  onClose: () => void
  onUpdated: () => Promise<void>
}

function JobDetailPanel({ job, onClose, onUpdated }: JobDetailPanelProps) {
  const [editedJob, setEditedJob] = useState<Job | null>(null)
  const [hasChanges, setHasChanges] = useState(false)
  const [showCommentDialog, setShowCommentDialog] = useState<'save' | 'flag' | null>(null)
  const [comment, setComment] = useState('')
  const [rawApiExpanded, setRawApiExpanded] = useState(false)
  const [rawHtmlExpanded, setRawHtmlExpanded] = useState(false)

  // Initialize edited job when job changes
  useEffect(() => {
    if (job) {
      setEditedJob({ ...job })
      setHasChanges(false)
    }
  }, [job])

  const handleFieldChange = <K extends keyof Job>(field: K, value: Job[K]) => {
    if (editedJob) {
      setEditedJob({ ...editedJob, [field]: value })
      setHasChanges(true)
    }
  }

  const handleSave = () => {
    setShowCommentDialog('save')
  }

  const handleFlag = () => {
    setShowCommentDialog('flag')
  }

  const handleConfirmAction = async () => {
    if (!showCommentDialog || !comment.trim() || !editedJob) return
    if (showCommentDialog === 'save') {
      const payload: JobUpdateInput = {
        seniority: editedJob.seniority,
        isInternship: editedJob.isInternship,
        isNewGrad: editedJob.isNewGrad,
        sponsorshipStatus: editedJob.sponsorshipStatus,
        sponsorshipConfidence: editedJob.sponsorshipConfidence,
        remoteType: editedJob.remoteType,
        techStack: editedJob.techStack,
        skills: editedJob.skills,
        comment: comment.trim(),
      }
      await saveJobReview(editedJob.id, payload)
    } else {
      await flagJob(editedJob.id, comment.trim())
    }
    await onUpdated()
    setShowCommentDialog(null)
    setComment('')
    setHasChanges(false)
  }

  if (!job || !editedJob) return null

  return (
    <>
      <Sheet open={!!job} onOpenChange={() => onClose()}>
        <SheetContent className="w-full sm:max-w-xl overflow-y-auto">
          {/* Section 1: Job Header */}
          <SheetHeader>
            <SheetTitle className="text-xl">{job.title}</SheetTitle>
            <SheetDescription asChild>
              <div className="flex items-center gap-2">
                <span>{job.company}</span>
                <PlatformBadge platform={job.platform} />
              </div>
            </SheetDescription>
          </SheetHeader>

          <div className="mt-4">
            <Button variant="outline" size="sm" asChild>
              <a href={job.postingUrl} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="size-4 mr-2" />
                View Job Posting
              </a>
            </Button>
          </div>

          {/* Section 2: Processing Status */}
          <div className="mt-6 space-y-3">
            <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">Processing Status</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Current State</span>
                <div className="mt-1"><StatusBadge status={job.processingState} /></div>
              </div>
              {job.failureReason && (
                <div>
                  <span className="text-muted-foreground">Failure Reason</span>
                  <div className="mt-1 text-warning">{failureReasonLabels[job.failureReason] || job.failureReason}</div>
                </div>
              )}
              <div>
                <span className="text-muted-foreground">Last Enrichment</span>
                <div className="mt-1"><RelativeTime date={job.lastEnrichmentAttempt} /></div>
              </div>
              <div>
                <span className="text-muted-foreground">Last Manual Review</span>
                <div className="mt-1"><RelativeTime date={job.lastManualReview} /></div>
              </div>
            </div>
          </div>

          {/* Section 3: Normalized Fields */}
          <div className="mt-6 space-y-4">
            <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">Job Details</h3>
            
            {/* Read-only fields */}
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Title</span>
                <div className="mt-1 font-medium">{job.title}</div>
              </div>
              <div>
                <span className="text-muted-foreground">Company</span>
                <div className="mt-1">{job.company}</div>
              </div>
              <div>
                <span className="text-muted-foreground">Location</span>
                <div className="mt-1">{job.location}</div>
              </div>
              <div>
                <span className="text-muted-foreground">Department</span>
                <div className="mt-1">{job.department}</div>
              </div>
              <div>
                <span className="text-muted-foreground">Employment Type</span>
                <div className="mt-1">{job.employmentType}</div>
              </div>
              <div>
                <span className="text-muted-foreground">Posted</span>
                <div className="mt-1"><RelativeTime date={job.postedAt} /></div>
              </div>
            </div>

            {/* Editable enrichment fields */}
            <div className="border-t pt-4 mt-4 space-y-4">
              <h4 className="text-sm font-medium">Enrichment Fields (Editable)</h4>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="seniority">Seniority</Label>
                  <Select 
                    value={editedJob.seniority} 
                    onValueChange={(v) => handleFieldChange('seniority', v)}
                  >
                    <SelectTrigger id="seniority">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {seniorityOptions.map(opt => (
                        <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="remoteType">Remote Type</Label>
                  <Select 
                    value={editedJob.remoteType} 
                    onValueChange={(v) => handleFieldChange('remoteType', v)}
                  >
                    <SelectTrigger id="remoteType">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {remoteTypeOptions.map(opt => (
                        <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sponsorshipStatus">Sponsorship Status</Label>
                  <Select 
                    value={editedJob.sponsorshipStatus} 
                    onValueChange={(v) => handleFieldChange('sponsorshipStatus', v)}
                  >
                    <SelectTrigger id="sponsorshipStatus">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {sponsorshipStatusOptions.map(opt => (
                        <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="sponsorshipConfidence">Sponsorship Confidence</Label>
                  <Select 
                    value={editedJob.sponsorshipConfidence} 
                    onValueChange={(v) => handleFieldChange('sponsorshipConfidence', v)}
                  >
                    <SelectTrigger id="sponsorshipConfidence">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {sponsorshipConfidenceOptions.map(opt => (
                        <SelectItem key={opt.value} value={opt.value}>{opt.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2">
                  <Switch 
                    id="isInternship"
                    checked={editedJob.isInternship}
                    onCheckedChange={(v) => handleFieldChange('isInternship', v)}
                  />
                  <Label htmlFor="isInternship">Is Internship</Label>
                </div>
                <div className="flex items-center gap-2">
                  <Switch 
                    id="isNewGrad"
                    checked={editedJob.isNewGrad}
                    onCheckedChange={(v) => handleFieldChange('isNewGrad', v)}
                  />
                  <Label htmlFor="isNewGrad">Is New Grad</Label>
                </div>
              </div>

              <div className="space-y-2">
                <Label>Tech Stack</Label>
                <div className="flex flex-wrap gap-2">
                  {editedJob.techStack.map((tech, idx) => (
                    <Badge key={idx} variant="secondary">{tech}</Badge>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Skills</Label>
                <div className="flex flex-wrap gap-2">
                  {editedJob.skills.map((skill, idx) => (
                    <Badge key={idx} variant="outline">{skill}</Badge>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Section 4: Actions */}
          <div className="mt-6 flex items-center gap-3 border-t pt-4">
            <Button 
              onClick={handleSave}
              disabled={!hasChanges}
            >
              <Save className="size-4 mr-2" />
              Save Changes
            </Button>
            <Button 
              variant="outline"
              onClick={handleFlag}
            >
              <Flag className="size-4 mr-2" />
              Flag for Engineering
            </Button>
          </div>

          {/* Section 5: Raw Payload */}
          <div className="mt-6 space-y-3">
            <Collapsible open={rawApiExpanded} onOpenChange={setRawApiExpanded}>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" className="w-full justify-between">
                  View Raw API Response
                  <ChevronDown className={cn("size-4 transition-transform", rawApiExpanded && "rotate-180")} />
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <pre className="mt-2 p-4 bg-muted rounded-lg text-xs overflow-auto max-h-[300px]">
                  {JSON.stringify(job.rawPayload, null, 2)}
                </pre>
              </CollapsibleContent>
            </Collapsible>

            <Collapsible open={rawHtmlExpanded} onOpenChange={setRawHtmlExpanded}>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" className="w-full justify-between">
                  View Raw HTML
                  <ChevronDown className={cn("size-4 transition-transform", rawHtmlExpanded && "rotate-180")} />
                </Button>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <pre className="mt-2 p-4 bg-muted rounded-lg text-xs overflow-auto max-h-[300px] whitespace-pre-wrap">
                  {job.rawHtml}
                </pre>
              </CollapsibleContent>
            </Collapsible>
          </div>
        </SheetContent>
      </Sheet>

      {/* Comment Dialog */}
      <Dialog open={!!showCommentDialog} onOpenChange={() => setShowCommentDialog(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {showCommentDialog === 'save' ? 'Save Changes' : 'Flag for Engineering Review'}
            </DialogTitle>
            <DialogDescription>
              {showCommentDialog === 'save' 
                ? 'Please add a comment explaining your changes.'
                : 'Please add a comment explaining why this job needs engineering review.'}
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Label htmlFor="comment">Comment (required)</Label>
            <Textarea
              id="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add your comment here..."
              className="mt-2"
              rows={4}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCommentDialog(null)}>
              Cancel
            </Button>
            <Button onClick={handleConfirmAction} disabled={!comment.trim()}>
              Confirm
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
