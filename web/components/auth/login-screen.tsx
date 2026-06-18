"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
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
    <div className="flow-page-bg flex min-h-screen flex-col">
      <header className="border-b border-border/60 bg-card/80 px-6 py-4 backdrop-blur-sm">
        <Link href="/">
          <Brand />
        </Link>
      </header>

      <main className="flex flex-1 items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          <div className="text-center">
            <h1 className="text-2xl font-bold text-foreground">Welcome to CareerMatch</h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Sign in to access your executive job dashboard
            </p>
          </div>

          <div className="card-elevated mt-8 p-6">
            <button
              type="button"
              onClick={() => void handleGoogleSignIn()}
              disabled={googleLoading}
              className="flex h-11 w-full items-center justify-center gap-3 rounded-lg border border-border bg-card text-sm font-medium transition-colors hover:bg-muted disabled:opacity-50"
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
                  className="h-11 border-border/80 bg-surface/50"
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
                  className="h-11 border-border/80 bg-surface/50"
                />
              </div>
              {error ? <p className="text-sm text-remove">{error}</p> : null}
              <Button type="submit" className="btn-brand h-11 w-full" disabled={loading}>
                {loading ? "Signing in..." : "Continue"}
              </Button>
            </form>
          </div>

          <p className="mt-6 text-center text-xs text-muted-foreground">
            By continuing, you agree to CareerMatch&apos;s Terms of Service and Privacy Policy.
          </p>
        </div>
      </main>
    </div>
  )
}
