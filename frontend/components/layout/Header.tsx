'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'
import { generateOrganizationSchema } from '@/components/seo/JsonLd'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  // JSON-LD Organization
  const organizationSchema = generateOrganizationSchema()

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />
      
      <header className="fixed top-0 left-0 right-0 z-50 bg-black/90 backdrop-blur-lg border-b border-ka-border">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-20">
            {/* Logo */}
            <Link href="/" className="flex items-center">
              <Image
                src="/img/logos/logo-kaizen-header.webp"
                alt="Agência Kaizen"
                width={120}
                height={40}
                className="h-10 w-auto"
                priority
              />
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center space-x-6">
              <Link href="/" className="text-white hover:text-primary transition-colors text-sm font-medium">
                home
              </Link>
              <Link href="/quem-somos" className="text-white hover:text-primary transition-colors text-sm font-medium">
                quem somos
              </Link>
              <Link href="/nossas-empresas" className="text-white hover:text-primary transition-colors text-sm font-medium">
                nossas empresas
              </Link>
              <Link href="/onde-estamos" className="text-white hover:text-primary transition-colors text-sm font-medium">
                onde estamos
              </Link>
              <Link href="/aprenda-marketing" className="text-white hover:text-primary transition-colors text-sm font-medium">
                aprenda marketing
              </Link>
              
              {/* Dropdown Soluções */}
              <div className="relative group">
                <Link href="/solucoes" className="text-white hover:text-primary transition-colors text-sm font-medium flex items-center">
                  soluções
                  <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </Link>
              </div>

              <Link href="/contato" className="text-white hover:text-primary transition-colors text-sm font-medium">
                contato
              </Link>
              
              {/* Telefone em destaque */}
              <a
                href="tel:08005508000"
                className="bg-primary/10 text-primary font-bold px-4 py-2 rounded-full text-sm hover:bg-primary/20 transition-colors"
              >
                <span className="mr-1">📞</span>
                0800-550-8000
              </a>
            </nav>

            {/* Mobile Menu Button */}
            <button
              className="md:hidden text-white"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <nav className="md:hidden pb-4 border-t border-ka-border mt-4 pt-4">
              <div className="flex flex-col space-y-4">
                <Link href="/" className="text-white hover:text-primary transition-colors">home</Link>
                <Link href="/quem-somos" className="text-white hover:text-primary transition-colors">quem somos</Link>
                <Link href="/nossas-empresas" className="text-white hover:text-primary transition-colors">nossas empresas</Link>
                <Link href="/onde-estamos" className="text-white hover:text-primary transition-colors">onde estamos</Link>
                <Link href="/aprenda-marketing" className="text-white hover:text-primary transition-colors">aprenda marketing</Link>
                <Link href="/solucoes" className="text-white hover:text-primary transition-colors">soluções</Link>
                <Link href="/contato" className="text-white hover:text-primary transition-colors">contato</Link>
                <a
                  href="tel:08005508000"
                  className="bg-primary/10 text-primary font-bold px-4 py-2 rounded-full text-center"
                >
                  📞 0800-550-8000
                </a>
              </div>
            </nav>
          )}
        </div>
      </header>
    </>
  )
}



