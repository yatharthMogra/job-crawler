import path from "node:path"
import os from "node:os"

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Keep build cache off Desktop/iCloud — corrupted .next causes intermittent 500s.
  distDir: process.env.NEXT_DIST_DIR || path.join(os.tmpdir(), "jobcrawler-web-next"),
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
}

export default nextConfig
