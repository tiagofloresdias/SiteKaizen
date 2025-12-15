import { Metadata } from 'next'
import Link from 'next/link'
import Image from 'next/image'
import { getCompanies, Company } from '@/lib/api'
import Breadcrumb from '@/components/seo/Breadcrumb'
import { generateOrganizationSchema } from '@/components/seo/JsonLd'

export const metadata: Metadata = {
  title: 'Nossas Empresas',
  description: 'Mais que uma agência, um ecossistema de crescimento. Conheça as empresas do Grupo Kaizen que aceleram negócios em diferentes áreas.',
}

// Dados estáticos das empresas (fallback caso API não retorne)
const defaultCompanies = [
  {
    id: '1',
    name: 'Agência Kaizen',
    slug: 'agencia-kaizen',
    tagline: 'Marketing Digital de Alta Performance',
    description: 'A <strong>Agência Kaizen</strong> é a principal empresa do grupo, especializada em marketing digital de performance. Google Partner Premier, ajudamos empresas a escalar suas vendas com estratégias afiadas, dados precisos e um time de elite.<br/><br/>Desde 2015, já ajudamos mais de 1.000 empresas a crescerem exponencialmente.',
    logo_url: '/img/logos/logo-kaizen-header.webp',
    website_url: 'https://www.agenciakaizen.com.br',
    is_active: true,
    order: 0,
  },
  {
    id: '2',
    name: 'Leadspot',
    slug: 'leadspot',
    tagline: 'Geração de Leads Qualificados',
    description: '<strong>Leadspot</strong> é a empresa do grupo especializada em geração de leads qualificados B2B. Utilizamos tecnologia de ponta e estratégias data-driven para conectar empresas aos seus clientes ideais.<br/><br/>Nossa plataforma proprietária identifica, qualifica e nutre leads até que estejam prontos para a conversão.',
    logo_url: '/img/logo-leadspot.webp',
    website_url: 'https://www.leadspot.com.br',
    is_active: true,
    order: 1,
  },
  {
    id: '3',
    name: 'Launcher',
    slug: 'launcher',
    tagline: 'Estratégia, Escala e Resultados Reais',
    description: '<strong>Launcher</strong> é especializada em acelerar o crescimento de infoprodutores e criadores de conteúdo. Oferecemos estratégias completas de lançamento, automação e escalabilidade para transformar conhecimento em negócios de sucesso.',
    logo_url: '/img/logo-launcher.webp',
    website_url: 'https://www.launcherx.com.br',
    is_active: true,
    order: 2,
  },
  {
    id: '4',
    name: 'Hacker das Vendas',
    slug: 'hacker-das-vendas',
    tagline: 'Consultoria e Mentoria Estratégica',
    description: '<strong>Hacker das Vendas</strong> oferece consultoria e mentoria estratégica para escalar o crescimento de negócios. Com metodologias comprovadas e insights de mercado, ajudamos empresas a hackear o sistema de vendas e alcançar resultados exponenciais.',
    logo_url: '/img/logo-hacker-das-vendas.webp',
    website_url: 'https://www.hackerdasvendas.com.br',
    is_active: true,
    order: 3,
  },
  {
    id: '5',
    name: 'Fluxo',
    slug: 'fluxo',
    tagline: 'Automação, Eficiência e Escalabilidade',
    description: '<strong>Fluxo</strong> é nossa solução de automação e eficiência operacional. Desenvolvemos sistemas e processos que eliminam gargalos, otimizam recursos e permitem que empresas escalem sem aumentar proporcionalmente os custos operacionais.',
    logo_url: '/img/logo-fluxo.webp',
    website_url: 'https://lp.agenciakaizen.com.br/fluxo/',
    is_active: true,
    order: 4,
  },
]

export default async function NossasEmpresasPage() {
  let companies: Company[] = []
  try {
    const companiesResponse = await getCompanies({ is_active: true, limit: 100 })
    companies = companiesResponse.data || []
  } catch (error) {
    console.warn('Erro ao buscar empresas da API, usando dados estáticos:', error)
  }

  // Usar dados estáticos se API não retornar empresas
  if (companies.length === 0) {
    companies = defaultCompanies as Company[]
  } else {
    // Mesclar com dados estáticos para garantir que todas apareçam
    const staticSlugs = new Set(defaultCompanies.map(c => c.slug))
    const apiSlugs = new Set(companies.map(c => c.slug))
    const missingCompanies = defaultCompanies.filter(c => !apiSlugs.has(c.slug))
    companies = [...companies, ...missingCompanies as Company[]].sort((a, b) => {
      const aOrder = 'order' in a ? a.order : 0
      const bOrder = 'order' in b ? b.order : 0
      return aOrder - bOrder
    })
  }

  const organizationSchema = generateOrganizationSchema()
  const breadcrumbItems = [
    { name: 'Home', url: '/' },
    { name: 'Nossas Empresas', url: '/nossas-empresas' },
  ]

  return (
    <>
      {/* JSON-LD Organization */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />

      <div className="pt-20 min-h-screen bg-black">
        {/* Hero Section */}
        <section className="py-16 border-b border-ka-border">
          <div className="container mx-auto px-4">
            <Breadcrumb items={breadcrumbItems} />
            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-4">
              não somos apenas uma agência.
            </h1>
            <h2 className="text-3xl md:text-4xl font-bold text-primary mb-6">
              Criamos máquinas de vendas.
            </h2>
            <p className="text-lg text-text-muted max-w-3xl">
              Mais que uma agência, um ecossistema de crescimento. A Kaizen é um grupo de empresas que acelera 
              negócios em diferentes áreas.
            </p>
          </div>
        </section>

        {/* Companies Grid */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {companies.map((company) => (
                <div
                  key={company.id}
                  className="ka-card p-6 group"
                >
                  {company.logo_url && (
                    <div className="mb-6 flex items-center justify-center h-20">
                      <Image
                        src={company.logo_url}
                        alt={company.name}
                        width={200}
                        height={80}
                        className="max-h-16 w-auto object-contain filter brightness-0 invert group-hover:brightness-100 group-hover:invert-0 transition-all duration-300"
                      />
                    </div>
                  )}
                  <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-primary transition-colors">
                    {company.name}
                  </h3>
                  {company.tagline && (
                    <p className="text-primary mb-4 font-semibold text-sm uppercase tracking-wide">
                      {company.tagline}
                    </p>
                  )}
                  {company.description && (
                    <div 
                      className="text-text-muted text-sm leading-relaxed mb-4 line-clamp-4"
                      dangerouslySetInnerHTML={{ __html: company.description }} 
                    />
                  )}
                  {company.website_url && (
                    <a
                      href={company.website_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center mt-4 text-primary text-sm font-medium group-hover:underline transition-all"
                    >
                      Saiba mais
                      <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </>
  )
}

