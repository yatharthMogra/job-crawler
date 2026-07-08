"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { signOut } from "next-auth/react"
import { useSession } from "@/components/session-provider"
import { SettingRow } from "@/components/settings/setting-controls"
import { Button } from "@/components/ui/button"
import { clearStoredCandidateId } from "@/lib/session"
import { cn } from "@/lib/utils"

const SECTIONS = [
  { id: "login", label: "Login & Security" },
  { id: "subscriptions", label: "Subscriptions" },
  { id: "logout", label: "Log out" },
] as const

type SectionId = (typeof SECTIONS)[number]["id"]

export function SettingsPage() {
  const router = useRouter()
  const { candidate } = useSession()
  const [section, setSection] = useState<SectionId>("login")

  async function handleLogout() {
    clearStoredCandidateId()
    await signOut({ callbackUrl: "/login" })
    router.replace("/login")
  }

  return (
    <div className="dashboard-page-bg flex min-h-screen flex-col">
      <div className="border-b border-border/80 bg-card/80 px-6 py-4 backdrop-blur-sm">
        <h1 className="text-lg font-bold tracking-tight text-foreground">Settings</h1>
        <p className="text-xs text-muted-foreground">Account and subscriptions</p>
      </div>

      <div className="flex flex-1">
        <aside className="w-52 shrink-0 border-r border-border/80 bg-card/60 p-3">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              type="button"
              onClick={() => setSection(s.id)}
              className={cn(
                "mb-0.5 w-full rounded-lg px-3 py-2.5 text-left text-sm transition-colors",
                section === s.id
                  ? "bg-accent font-medium text-accent-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-secondary/80",
              )}
            >
              {s.label}
            </button>
          ))}
        </aside>

        <main className="flex-1 p-6">
          {section === "login" ? (
            <div className="mx-auto max-w-2xl rounded-xl card-elevated border-0 p-6">
              <h2 className="text-base font-semibold text-foreground">Login & Security</h2>
              <div className="mt-6">
                <SettingRow title="Email" description={candidate?.email ?? "—"}>
                  <span className="text-xs text-muted-foreground/70">Verified</span>
                </SettingRow>
                <SettingRow title="Password" description="Last updated — not available in demo mode">
                  <Button variant="outline" size="sm" className="border-border" disabled>
                    Change password
                  </Button>
                </SettingRow>
              </div>
            </div>
          ) : null}

          {section === "subscriptions" ? (
            <div className="mx-auto max-w-2xl rounded-xl card-elevated border-0 p-6">
              <h2 className="text-base font-semibold text-foreground">Subscriptions</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Job pool subscriptions are synced from your profile filters.
              </p>
              <div className="mt-6 rounded-lg border border-border/60 bg-surface/50 p-4">
                <p className="text-sm font-medium text-foreground">Job Scout Plus — coming soon</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  $4.99/month for up to 25 watched companies with higher-frequency batched alerts. Manage email
                  alerts on the{" "}
                  <Link href="/emails" className="font-medium text-brand hover:underline">
                    Emails
                  </Link>{" "}
                  page.
                </p>
              </div>
            </div>
          ) : null}

          {section === "logout" ? (
            <div className="mx-auto max-w-2xl rounded-xl card-elevated border-0 p-6">
              <h2 className="text-base font-semibold text-foreground">Log out</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Sign out of your account on this device. Your profile and saved jobs remain stored.
              </p>
              <Button
                variant="outline"
                className="mt-6 border-border text-foreground hover:bg-surface"
                onClick={handleLogout}
              >
                Log out
              </Button>
            </div>
          ) : null}
        </main>
      </div>
    </div>
  )
}
