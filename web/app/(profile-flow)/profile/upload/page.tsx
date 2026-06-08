"use client"

import { useRouter } from "next/navigation"
import { UploadScreen } from "@/components/profile/screens/upload-screen"
import { useProfileFlow } from "@/components/profile/profile-flow-provider"

export default function UploadPage() {
  const router = useRouter()
  const { setUploadFile, uploadError } = useProfileFlow()

  return (
    <UploadScreen
      error={uploadError}
      onAnalyze={(file) => {
        setUploadFile(file)
        router.push("/profile/processing")
      }}
    />
  )
}
