"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { ArrowLeft, ShieldCheck } from "lucide-react"
import { signIn } from "next-auth/react"
import { Brand } from "@/components/profile/brand"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ApiError, createCandidate, lookupCandidateByEmail } from "@/lib/profile/api"
import {
  MOCK_CANDIDATE_ID,
  setMockCandidateInfo,
  setStoredCandidateId,
  useMockData,
} from "@/lib/session"
import { resolveBootDestination } from "@/lib/boot-routing"

function GoogleIcon() {
  return (
    <svg className="size-5" viewBox="0 0 24 24" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
      />
    </svg>
  )
}

export function LoginScreen() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const mockMode = useMockData()
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [googleLoading, setGoogleLoading] = useState(false)
  const callbackUrl = searchParams.get("callbackUrl") ?? "/app"

  useEffect(() => {
    if (searchParams.get("error") === "exists") {
      setError("An account with this email already exists. Sign in with Google or enter your email below.")
    }
  }, [searchParams])

  async function handleGoogleSignIn() {
    setGoogleLoading(true)
    setError(null)
    try {
      await signIn("google", { callbackUrl })
    } catch {
      setError("Google sign-in failed. Please try again.")
      setGoogleLoading(false)
    }
  }

  async function handleEmailSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    if (!email.trim()) {
      setError("Please enter your email.")
      return
    }
    setLoading(true)
    try {
      if (mockMode) {
        setMockCandidateInfo(name.trim() || "Alex Rivera", email.trim())
        setStoredCandidateId(MOCK_CANDIDATE_ID)
        const dest = await resolveBootDestination()
        router.replace(dest)
        return
      }

      try {
        const existing = await lookupCandidateByEmail(email.trim())
        setStoredCandidateId(existing.id)
        const dest = await resolveBootDestination()
        router.replace(dest)
        return
      } catch (lookupErr) {
        if (!(lookupErr instanceof ApiError && lookupErr.status === 404)) {
          throw lookupErr
        }
      }

      if (!name.trim()) {
        setError("Please enter your name to create a new account.")
        return
      }

      const candidate = await createCandidate(name.trim(), email.trim())
      setStoredCandidateId(candidate.id)
      router.replace("/profile/upload")
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        setError("An account with this email already exists. Sign in with Google or enter your email to continue.")
      } else {
        setError(err instanceof Error ? err.message : "Something went wrong. Please try again.")
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="landing-hero-bg relative flex min-h-screen flex-col overflow-hidden">
      <div className="pointer-events-none absolute -left-24 top-20 size-72 rounded-full bg-primary/10 blur-3xl" />
      <div className="pointer-events-none absolute -right-16 bottom-16 size-64 rounded-full bg-primary/5 blur-3xl" />

      <header className="relative z-10 flex items-center justify-between px-6 py-5">
        <Link href="/">
          <Brand />
        </Link>
        <Link
          href="/"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="size-4" />
          Back to Landing Page
        </Link>
      </header>

      <main className="relative z-10 flex flex-1 items-center justify-center px-6 py-8">
        <div className="w-full max-w-md">
          <div className="text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-card px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-primary">
              <ShieldCheck className="size-3" />
              Secure Access
            </span>
            <h1 className="mt-5 text-3xl font-bold tracking-tight text-foreground">
              Enter your{" "}
              <span className="script-accent text-4xl font-semibold italic">command center.</span>
            </h1>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              Sign in to access personalized matches, saved roles, and your career trajectory.
            </p>
          </div>

          <div className="mt-8 rounded-2xl border border-border/80 bg-card p-6 shadow-lg shadow-primary/5">
            <button
              type="button"
              onClick={() => void handleGoogleSignIn()}
              disabled={googleLoading}
              className="flex h-12 w-full items-center justify-center gap-3 rounded-full border border-border bg-background text-sm font-semibold transition-colors hover:bg-muted disabled:opacity-50"
            >
              <GoogleIcon />
              {googleLoading ? "Redirecting..." : "Continue with Google"}
            </button>

            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-border" />
              <span className="text-xs text-muted-foreground">or continue with email</span>
              <div className="h-px flex-1 bg-border" />
            </div>

            <form onSubmit={(e) => void handleEmailSubmit(e)} className="space-y-4">
              <div>
                <label htmlFor="login-name" className="mb-1.5 block text-sm font-medium text-foreground">
                  Full name <span className="text-muted-foreground">(new accounts only)</span>
                </label>
                <Input
                  id="login-name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Alex Rivera"
                  autoComplete="name"
                  className="h-12 rounded-xl border-border/80 bg-surface/50"
                />
              </div>
              <div>
                <label htmlFor="login-email" className="mb-1.5 block text-sm font-medium text-foreground">
                  Email
                </label>
                <Input
                  id="login-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  autoComplete="email"
                  required
                  className="h-12 rounded-xl border-border/80 bg-surface/50"
                />
              </div>
              {error ? <p className="text-sm text-remove">{error}</p> : null}
              <Button
                type="submit"
                className="btn-brand h-12 w-full rounded-full text-sm font-semibold"
                disabled={loading}
              >
                {loading ? "Signing in..." : "Continue"}
              </Button>
            </form>
          </div>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            By continuing, you agree to Job Scout&apos;s Terms of Service and Privacy Policy.
          </p>
        </div>
      </main>
    </div>
  )
}
