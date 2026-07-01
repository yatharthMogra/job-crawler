import { Analytics } from '@vercel/analytics/next'
import type { Metadata } from 'next'
import { Caveat, Geist, Geist_Mono } from 'next/font/google'
import { SessionProvider as NextAuthSessionProvider } from 'next-auth/react'
import { SessionProvider } from '@/components/session-provider'
import './globals.css'

const geistSans = Geist({ variable: '--font-geist-sans', subsets: ['latin'] })
const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
})
const caveat = Caveat({
  variable: '--font-caveat',
  subsets: ['latin'],
  weight: ['500', '600', '700'],
})

export const metadata: Metadata = {
  title: 'Job Scout — Precision AI career matching',
  description:
    'High-density semantic matching for top talent. Get matched roles, sponsorship insights, and salary intelligence.',
  generator: 'v0.app',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} ${caveat.variable}`}>
      <body className="font-sans antialiased">
        <NextAuthSessionProvider>
          <SessionProvider>{children}</SessionProvider>
        </NextAuthSessionProvider>
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
