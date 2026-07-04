import path from "node:path"
import os from "node:os"

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Keep build cache off Desktop/iCloud locally; Vercel requires the default .next output.
  distDir: process.env.VERCEL
    ? ".next"
    : process.env.NEXT_DIST_DIR || path.join(os.tmpdir(), "jobcrawler-web-next"),
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
