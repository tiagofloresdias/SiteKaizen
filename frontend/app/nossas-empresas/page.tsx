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

export default async function NossasEmpresasPage() {
  let companies: Company[] = []
  try {
    const companiesResponse = await getCompanies({ is_active: true, limit: 100 })
    companies = companiesResponse.data || []
  } catch (error) {
    console.warn('Erro ao buscar empresas:', error)
    companies = []
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
            {companies.length === 0 ? (
              <div className="text-center py-20">
                <p className="text-text-muted text-lg">
                  Nenhuma empresa cadastrada no momento.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {companies.map((company) => (
                  <Link
                    key={company.id}
                    href={`/nossas-empresas/${company.slug}`}
                    className="ka-card p-6 block group"
                  >
                    {company.logo_url && (
                      <div className="mb-4">
                        <Image
                          src={company.logo_url}
                          alt={company.name}
                          width={200}
                          height={80}
                          className="h-16 w-auto object-contain"
                        />
                      </div>
                    )}
                    <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-primary transition-colors">
                      {company.name}
                    </h3>
                    {company.tagline && (
                      <p className="text-primary mb-4 font-medium">{company.tagline}</p>
                    )}
                    {company.description && (
                      <p className="text-text-muted line-clamp-3" dangerouslySetInnerHTML={{ __html: company.description }} />
                    )}
                    {company.website_url && (
                      <span className="inline-block mt-4 text-primary text-sm font-medium group-hover:underline">
                        Saiba mais →
                      </span>
                    )}
                  </Link>
                ))}
              </div>
            )}
          </div>
        </section>
      </div>
    </>
  )
}

