import type { DefaultSession } from "next-auth"

declare module "next-auth" {
  interface Session {
    candidateId?: string
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    candidateId?: string
  }
}

export type { DefaultSession }
