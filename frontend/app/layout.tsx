import type { Metadata } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-poppins',
  display: 'swap',
})

export const metadata: Metadata = {
  title: {
    default: 'Agência Kaizen - Marketing Digital de Alta Performance',
    template: '%s | Agência Kaizen',
  },
  description: 'Aceleramos negócios e lançamos foguetes. Desde 2015, ajudamos empresas a crescer com estratégias afiadas, dados precisos e um time de elite.',
  keywords: ['marketing digital', 'agência digital', 'desenvolvimento web', 'SEO', 'mídia paga', 'automação'],
  authors: [{ name: 'Agência Kaizen' }],
  creator: 'Agência Kaizen',
  publisher: 'Agência Kaizen',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br'),
  openGraph: {
    type: 'website',
    locale: 'pt_BR',
    url: process.env.NEXT_PUBLIC_SITE_URL || 'https://site2025.agenciakaizen.com.br',
    siteName: 'Agência Kaizen',
    title: 'Agência Kaizen - Marketing Digital de Alta Performance',
    description: 'Aceleramos negócios e lançamos foguetes. Desde 2015, ajudamos empresas a crescer.',
    images: [
      {
        url: '/img/logos/logo-kaizen-maior.webp',
        width: 1200,
        height: 630,
        alt: 'Agência Kaizen',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Agência Kaizen - Marketing Digital de Alta Performance',
    description: 'Aceleramos negócios e lançamos foguetes. Desde 2015, ajudamos empresas a crescer.',
    images: ['/img/logos/logo-kaizen-maior.webp'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${poppins.variable}`}>
      <body className="font-base antialiased bg-background text-text">
        <Header />
        <main className="min-h-screen">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}



