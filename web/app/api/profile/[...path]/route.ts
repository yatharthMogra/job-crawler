import type { NextRequest } from "next/server"
import { NextResponse } from "next/server"

const PROFILE_API_URL =
  process.env.PROFILE_API_URL ?? process.env.NEXT_PUBLIC_PROFILE_API_URL ?? "http://localhost:8001"
const PROFILE_API_KEY =
  process.env.PROFILE_API_KEY ?? process.env.NEXT_PUBLIC_PROFILE_API_KEY ?? "dev-key-change-me"

async function proxyRequest(request: NextRequest, path: string) {
  const url = new URL(path, PROFILE_API_URL)
  request.nextUrl.searchParams.forEach((value, key) => {
    url.searchParams.set(key, value)
  })

  const headers = new Headers(request.headers)
  headers.set("X-API-Key", PROFILE_API_KEY)
  headers.delete("host")
  headers.delete("connection")

  const init: RequestInit = {
    method: request.method,
    headers,
  }

  if (request.method !== "GET" && request.method !== "HEAD") {
    const body = await request.arrayBuffer()
    if (body.byteLength > 0) {
      init.body = body
    }
  }

  const response = await fetch(url, init)
  const responseHeaders = new Headers(response.headers)
  responseHeaders.delete("content-encoding")
  responseHeaders.delete("transfer-encoding")

  return new NextResponse(response.body, {
    status: response.status,
    headers: responseHeaders,
  })
}

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params
  return proxyRequest(request, `/${path.join("/")}`)
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params
  return proxyRequest(request, `/${path.join("/")}`)
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params
  return proxyRequest(request, `/${path.join("/")}`)
}

export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params
  return proxyRequest(request, `/${path.join("/")}`)
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const { path } = await params
  return proxyRequest(request, `/${path.join("/")}`)
}
