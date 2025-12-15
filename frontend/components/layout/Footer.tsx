import Link from 'next/link'
import Image from 'next/image'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-ka-dark-2 border-t border-ka-border">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Logo e Descrição */}
          <div className="col-span-1 md:col-span-2">
            <Link href="/" className="block mb-4">
              <Image
                src="/img/logos/logo-kaizen-header.webp"
                alt="Agência Kaizen"
                width={150}
                height={50}
                className="h-10 w-auto"
              />
            </Link>
            <p className="text-text-muted mb-4 max-w-md">
              Com mais de 15 anos de experiência de mercado, a Agência Kaizen é uma empresa Partner do Google, 
              especializada em Marketing Digital de Alta Performance.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://www.linkedin.com/company/agenciakaizen/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-text-muted hover:text-primary transition-colors"
                aria-label="LinkedIn"
              >
                <span className="sr-only">LinkedIn</span>
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Links Rápidos */}
          <div>
            <h3 className="text-white font-bold mb-4">Links Rápidos</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-text-muted hover:text-primary transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/quem-somos" className="text-text-muted hover:text-primary transition-colors">
                  Quem Somos
                </Link>
              </li>
              <li>
                <Link href="/nossas-empresas" className="text-text-muted hover:text-primary transition-colors">
                  Nossas Empresas
                </Link>
              </li>
              <li>
                <Link href="/aprenda-marketing" className="text-text-muted hover:text-primary transition-colors">
                  Aprenda Marketing
                </Link>
              </li>
              <li>
                <Link href="/contato" className="text-text-muted hover:text-primary transition-colors">
                  Contato
                </Link>
              </li>
            </ul>
          </div>

          {/* Contato */}
          <div>
            <h3 className="text-white font-bold mb-4">Contato</h3>
            <ul className="space-y-2 text-text-muted">
              <li>
                <a href="tel:08005508000" className="hover:text-primary transition-colors">
                  📞 0800-550-8000
                </a>
              </li>
              <li>
                <a href="mailto:contato@agenciakaizen.com.br" className="hover:text-primary transition-colors">
                  ✉️ contato@agenciakaizen.com.br
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-ka-border pt-8 text-center text-text-muted text-sm">
          <p>© {currentYear} Agência Kaizen. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  )
}



