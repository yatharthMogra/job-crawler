"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

export default function ConfirmPage() {
  const router = useRouter()

  useEffect(() => {
    router.replace("/jobs/recommended")
  }, [router])

  return null
}
