import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

async function linkOAuthCandidate(profile: {
  email: string
  name: string
  googleSub: string
  avatarUrl?: string | null
}): Promise<string> {
  const baseUrl = process.env.PROFILE_API_URL ?? process.env.NEXT_PUBLIC_PROFILE_API_URL ?? "http://localhost:8001"
  const apiKey = process.env.PROFILE_API_KEY ?? process.env.NEXT_PUBLIC_PROFILE_API_KEY ?? "dev-key-change-me"

  const response = await fetch(`${baseUrl}/candidates/oauth`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": apiKey,
    },
    body: JSON.stringify({
      email: profile.email,
      name: profile.name,
      google_sub: profile.googleSub,
      avatar_url: profile.avatarUrl,
      email_verified: true,
    }),
  })

  if (!response.ok) {
    throw new Error(`Failed to link OAuth candidate (${response.status})`)
  }

  const data = (await response.json()) as { id: string }
  return data.id
}

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    ...(process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET
      ? [
          Google({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
          }),
        ]
      : []),
  ],
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, account, profile }) {
      if (account?.provider === "google" && profile) {
        const googleProfile = profile as {
          email?: string | null
          name?: string | null
          sub?: string
          picture?: string | null
        }
        if (googleProfile.email && googleProfile.sub) {
          const candidateId = await linkOAuthCandidate({
            email: googleProfile.email,
            name: googleProfile.name ?? googleProfile.email.split("@")[0] ?? "User",
            googleSub: googleProfile.sub,
            avatarUrl: googleProfile.picture,
          })
          token.candidateId = candidateId
        }
      }
      return token
    },
    async session({ session, token }) {
      if (token.candidateId) {
        session.candidateId = token.candidateId as string
      }
      return session
    },
  },
  trustHost: true,
})
