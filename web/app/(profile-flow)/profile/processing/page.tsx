"use client"

import { useRouter } from "next/navigation"
import { ProcessingScreen } from "@/components/profile/screens/processing-screen"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"

export default function ProcessingPage() {
  const router = useRouter()
  const { fileName, processUpload } = useProfileFlow()

  return (
    <ProcessingScreen
      fileName={fileName || "resume.pdf"}
      onProcess={processUpload}
      onComplete={() => {}}
      onRetry={() => router.push("/profile/upload")}
    />
  )
}
