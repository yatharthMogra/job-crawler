'use client'

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Activity, Database, DollarSign, Briefcase, Layers, Globe, Timer } from 'lucide-react'
import { PipelineTab } from './pipeline-tab'
import { SourcesTab } from './sources-tab'
import { CostTab } from './cost-tab'
import { JobsTab } from './jobs-tab'
import { TaxonomyTab } from './taxonomy-tab'
import { H1bTab } from './h1b-tab'
import { CadenceTab } from './cadence-tab'

export function Dashboard() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card shadow-sm">
        <div className="container mx-auto px-6 py-4">
          <h1 className="text-xl font-semibold text-foreground">Job Ingestion Admin</h1>
          <p className="text-sm text-muted-foreground mt-1">Operations and review dashboard</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-6">
        <Tabs defaultValue="pipeline" className="space-y-6">
          <TabsList className="bg-card border border-border shadow-sm">
            <TabsTrigger value="pipeline" className="gap-2 data-[state=active]:bg-primary/10">
              <Activity className="size-4" />
              Pipeline
            </TabsTrigger>
            <TabsTrigger value="cadence" className="gap-2 data-[state=active]:bg-primary/10">
              <Timer className="size-4" />
              Cadence
            </TabsTrigger>
            <TabsTrigger value="sources" className="gap-2 data-[state=active]:bg-primary/10">
              <Database className="size-4" />
              Sources
            </TabsTrigger>
            <TabsTrigger value="cost" className="gap-2 data-[state=active]:bg-primary/10">
              <DollarSign className="size-4" />
              Cost
            </TabsTrigger>
            <TabsTrigger value="jobs" className="gap-2 data-[state=active]:bg-primary/10">
              <Briefcase className="size-4" />
              Jobs
            </TabsTrigger>
            <TabsTrigger value="taxonomy" className="gap-2 data-[state=active]:bg-primary/10">
              <Layers className="size-4" />
              Taxonomy
            </TabsTrigger>
            <TabsTrigger value="h1b" className="gap-2 data-[state=active]:bg-primary/10">
              <Globe className="size-4" />
              H-1B
            </TabsTrigger>
          </TabsList>

          <TabsContent value="pipeline">
            <PipelineTab />
          </TabsContent>

          <TabsContent value="cadence">
            <CadenceTab />
          </TabsContent>

          <TabsContent value="sources">
            <SourcesTab />
          </TabsContent>

          <TabsContent value="cost">
            <CostTab />
          </TabsContent>

          <TabsContent value="jobs">
            <JobsTab />
          </TabsContent>

          <TabsContent value="taxonomy">
            <TaxonomyTab />
          </TabsContent>

          <TabsContent value="h1b">
            <H1bTab />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
