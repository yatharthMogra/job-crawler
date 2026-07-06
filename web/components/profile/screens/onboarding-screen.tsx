"use client"

import Link from "next/link"
import { Brand } from "@/components/profile/brand"
import {
  FlowPage,
  FlowPageContent,
  FlowPageHeader,
  FlowPageHero,
  FlowPanel,
} from "@/components/ui/flow-page"
import { HandMetal, Sparkles, Target, Zap } from "lucide-react"

export function OnboardingScreen() {
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
          <p className="mb-5 text-sm text-muted-foreground">
            Sign up with email and password, then verify your address with a one-time code.
          </p>
          <Link
            href="/login?mode=signup"
            className="btn-brand inline-flex h-11 w-full items-center justify-center rounded-lg text-sm font-medium"
          >
            Continue to sign up
          </Link>
        </FlowPanel>
      </FlowPageContent>
    </FlowPage>
  )
}
