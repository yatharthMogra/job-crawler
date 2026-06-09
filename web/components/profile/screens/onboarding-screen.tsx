"use client"

import { useState } from "react"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import {
  FlowPage,
  FlowPageContent,
  FlowPageHeader,
  FlowPageHero,
  FlowPanel,
} from "@/components/ui/flow-page"
import { Input } from "@/components/ui/input"
import { ApiError, createCandidate } from "@/lib/profile/api"
import {
  MOCK_CANDIDATE_ID,
  setMockCandidateInfo,
  setStoredCandidateId,
  useMockData,
} from "@/lib/session"
import { HandMetal, Sparkles, Target, Zap } from "lucide-react"

interface OnboardingScreenProps {
  onComplete: (candidateId: string) => void
}

export function OnboardingScreen({ onComplete }: OnboardingScreenProps) {
  const mockMode = useMockData()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    if (!name.trim() || !email.trim()) {
      setError("Please enter your name and email.")
      return
    }
    setLoading(true)
    try {
      if (mockMode) {
        setMockCandidateInfo(name.trim(), email.trim())
        setStoredCandidateId(MOCK_CANDIDATE_ID)
        onComplete(MOCK_CANDIDATE_ID)
        return
      }
      const candidate = await createCandidate(name.trim(), email.trim())
      onComplete(candidate.id)
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        setError("An account with this email already exists.")
      } else {
        setError(err instanceof Error ? err.message : "Something went wrong. Please try again.")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <FlowPage>
      <FlowPageHeader>
        <Brand />
      </FlowPageHeader>

      <FlowPageContent>
        <FlowPageHero
          icon={HandMetal}
          iconTone="welcome"
          step={{ current: 1, total: 4, label: "Get started" }}
          title="Welcome aboard"
          description="We'll turn your resume into a living profile and surface roles you're actually qualified for — then help you apply in one click."
          features={[
            {
              icon: Zap,
              title: "2-minute setup",
              description: "Upload once, review what we found, and you're ready to browse.",
            },
            {
              icon: Target,
              title: "Roles you want",
              description: "Recommendations follow your target titles — not random keyword guesses.",
            },
            {
              icon: Sparkles,
              title: "Apply with clarity",
              description: "Match scores and fit reasons so you know before you click Apply.",
            },
          ]}
        />

        <FlowPanel>
          <p className="mb-5 text-sm font-medium text-foreground">Create your account</p>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="name" className="mb-1.5 block text-sm font-medium text-foreground">
                Full name
              </label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Alex Rivera"
                autoComplete="name"
                className="h-11 border-border/80 bg-surface/50"
              />
            </div>
            <div>
              <label htmlFor="email" className="mb-1.5 block text-sm font-medium text-foreground">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                autoComplete="email"
                className="h-11 border-border/80 bg-surface/50"
              />
            </div>
            {error ? <p className="text-sm text-remove">{error}</p> : null}
            <Button type="submit" className="btn-brand h-11 w-full" disabled={loading}>
              {loading ? "Creating profile..." : "Continue to resume upload"}
            </Button>
          </form>
        </FlowPanel>
      </FlowPageContent>
    </FlowPage>
  )
}
