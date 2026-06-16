import { auth } from "@/auth"
import { NextResponse } from "next/server"

const PROFILE_FLOW_ROUTES = [
  "/profile/upload",
  "/profile/review",
  "/profile/processing",
  "/profile/confirm",
  "/profile/job-intent",
]

function isProfileFlowRoute(pathname: string) {
  return PROFILE_FLOW_ROUTES.some((route) => pathname === route || pathname.startsWith(`${route}/`))
}

export default auth((req) => {
  const { pathname } = req.nextUrl
  const isAuthPage = pathname === "/login" || pathname === "/signup"
  const candidateCookie = req.cookies.get("candidate_id")?.value
  const isAuthenticated = !!req.auth?.candidateId || !!candidateCookie

  const isProtected =
    pathname.startsWith("/jobs") ||
    pathname === "/profile" ||
    (pathname.startsWith("/profile/") && !isProfileFlowRoute(pathname)) ||
    pathname === "/resume" ||
    pathname === "/settings" ||
    pathname === "/filters" ||
    pathname.startsWith("/dashboard")

  if (isProtected && !isAuthenticated) {
    const loginUrl = new URL("/login", req.url)
    loginUrl.searchParams.set("callbackUrl", pathname)
    return NextResponse.redirect(loginUrl)
  }

  if (isAuthPage && isAuthenticated) {
    const dest = req.cookies.get("mock_onboarding_complete")?.value === "true"
      ? "/jobs/recommended"
      : "/app"
    return NextResponse.redirect(new URL(dest, req.url))
  }

  return NextResponse.next()
})

export const config = {
  matcher: [
    "/jobs/:path*",
    "/profile",
    "/profile/:path*",
    "/resume",
    "/settings",
    "/filters",
    "/dashboard/:path*",
    "/login",
    "/signup",
  ],
}
