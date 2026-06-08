import type { ReactNode } from "react"
import { ProfileFlowShell } from "@/components/profile-flow-shell"

export default function ProfileFlowLayout({ children }: { children: ReactNode }) {
  return <ProfileFlowShell>{children}</ProfileFlowShell>
}
