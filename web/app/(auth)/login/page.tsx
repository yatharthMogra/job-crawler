import { Suspense } from "react"
import { LoginScreen } from "@/components/auth/login-screen"

function LoginFallback() {
  return (
    <div className="flow-page-bg flex min-h-screen items-center justify-center">
      <div className="flex gap-1.5" aria-label="Loading">
        <span className="size-1.5 animate-bounce rounded-full bg-primary/40 [animation-delay:-0.3s]" />
        <span className="size-1.5 animate-bounce rounded-full bg-primary/50 [animation-delay:-0.15s]" />
        <span className="size-1.5 animate-bounce rounded-full bg-primary/40" />
      </div>
    </div>
  )
}

export default function LoginPage() {
  return (
    <Suspense fallback={<LoginFallback />}>
      <LoginScreen />
    </Suspense>
  )
}
