import { redirect } from "next/navigation"

export default function AllJobsRedirect() {
  redirect("/jobs/recommended")
}
